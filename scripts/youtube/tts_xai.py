#!/usr/bin/env python3
"""Generate TTS audio from a YouTube pack voiceover via xAI TTS API.

Reads XAI_API_KEY from the environment or repo-root .env (gitignored).
Writes under youtube/audio/<slug>/ (gitignored).

Long voiceovers are split on blank lines (beats) and concatenated with ffmpeg.

Examples:
  python scripts/youtube/tts_xai.py 03
  python scripts/youtube/tts_xai.py 03 --lang zh
  python scripts/youtube/tts_xai.py 03 --lang both --dry-run
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parents[1]
if str(_SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR.parent))

from youtube.parse_chapter import resolve_chapter_path  # noqa: E402

PACKS_DIR = _ROOT / "youtube" / "packs"
AUDIO_DIR = _ROOT / "youtube" / "audio"
XAI_TTS_URL = "https://api.x.ai/v1/tts"

DEFAULT_VOICE = os.environ.get("XAI_TTS_VOICE_ID", "eve")
# Soft char budget per request; split on blank-line beats if longer.
MAX_CHARS = int(os.environ.get("XAI_TTS_MAX_CHARS", "1800"))


def _load_dotenv() -> None:
    env_path = _ROOT / ".env"
    if not env_path.is_file():
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
        return
    load_dotenv(env_path)


def _pack_dir_from_arg(chapter: str) -> Path:
    candidate = PACKS_DIR / chapter
    if (candidate / "voiceover-en.txt").is_file():
        return candidate
    for child in PACKS_DIR.iterdir() if PACKS_DIR.is_dir() else []:
        if child.is_dir() and (
            child.name == chapter
            or child.name.startswith(f"{chapter}-")
            or child.name.startswith(chapter.zfill(2) if chapter.isdigit() else chapter)
        ):
            if (child / "voiceover-en.txt").is_file():
                return child
    path = resolve_chapter_path(chapter)
    pack = PACKS_DIR / path.stem
    if not (pack / "voiceover-en.txt").is_file():
        raise FileNotFoundError(
            f"No voiceover pack at {pack}. Run youtube-text-pack first."
        )
    return pack


def _split_beats(text: str) -> list[str]:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not parts:
        return [text.strip()] if text.strip() else []
    # Merge small beats so we don't spam the API; split oversized ones by sentence.
    chunks: list[str] = []
    buf = ""
    for part in parts:
        if len(part) > MAX_CHARS:
            if buf:
                chunks.append(buf)
                buf = ""
            # hard split by sentences
            sentences = part.replace("? ", "?\n").replace(". ", ".\n").split("\n")
            cur = ""
            for s in sentences:
                s = s.strip()
                if not s:
                    continue
                if len(cur) + len(s) + 1 <= MAX_CHARS:
                    cur = f"{cur} {s}".strip()
                else:
                    if cur:
                        chunks.append(cur)
                    cur = s
            if cur:
                chunks.append(cur)
            continue
        if not buf:
            buf = part
        elif len(buf) + 2 + len(part) <= MAX_CHARS:
            buf = f"{buf}\n\n{part}"
        else:
            chunks.append(buf)
            buf = part
    if buf:
        chunks.append(buf)
    return chunks


def _tts_chunk(text: str, *, api_key: str, voice_id: str, language: str) -> bytes:
    import urllib.error
    import urllib.request
    import json

    payload = json.dumps(
        {"text": text, "voice_id": voice_id, "language": language}
    ).encode("utf-8")
    req = urllib.request.Request(
        XAI_TTS_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:  # noqa: S310
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"xAI TTS HTTP {exc.code}: {detail[:500]}") from exc


def _concat_mp3(parts: list[Path], dest: Path) -> None:
    if len(parts) == 1:
        shutil.copy2(parts[0], dest)
        return
    if not shutil.which("ffmpeg"):
        # naive concat (may glitch) if no ffmpeg
        with dest.open("wb") as out:
            for p in parts:
                out.write(p.read_bytes())
        return
    lst = dest.with_suffix(".concat.txt")
    lst.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in parts) + "\n",
        encoding="utf-8",
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c",
            "copy",
            str(dest),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    lst.unlink(missing_ok=True)


def _synthesize(
    text: str,
    *,
    api_key: str,
    voice_id: str,
    language: str,
    out: Path,
) -> None:
    chunks = _split_beats(text)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="xai-tts-") as tmp:
        tmp_path = Path(tmp)
        part_paths: list[Path] = []
        for i, chunk in enumerate(chunks):
            print(f"    chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)")
            audio = _tts_chunk(
                chunk, api_key=api_key, voice_id=voice_id, language=language
            )
            part = tmp_path / f"part_{i:02d}.mp3"
            part.write_bytes(audio)
            part_paths.append(part)
        _concat_mp3(part_paths, out)


def main(argv: list[str] | None = None) -> int:
    _load_dotenv()
    # Re-read defaults after dotenv
    voice_default = os.environ.get("XAI_TTS_VOICE_ID", DEFAULT_VOICE)

    p = argparse.ArgumentParser(description="xAI TTS for a YouTube text pack.")
    p.add_argument("chapter", help="Pack slug, chapter number, or path (e.g. 03)")
    p.add_argument(
        "--lang",
        choices=("en", "zh", "both"),
        default="en",
        help="Which voiceover track(s) to synthesize (default: en)",
    )
    p.add_argument("--voice-en", default=voice_default, help="xAI voice_id for EN")
    p.add_argument("--voice-zh", default=voice_default, help="xAI voice_id for ZH")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths and character counts; do not call the API.",
    )
    args = p.parse_args(argv)

    pack = _pack_dir_from_arg(args.chapter)
    slug = pack.name
    api_key = os.environ.get("XAI_API_KEY", "").strip()

    tracks: list[tuple[str, Path, str, str, Path]] = []
    if args.lang in ("en", "both"):
        tracks.append(("en", pack / "voiceover-en.txt", args.voice_en, "en", AUDIO_DIR / slug / "en.mp3"))
    if args.lang in ("zh", "both"):
        tracks.append(("zh", pack / "voiceover-zh.txt", args.voice_zh, "zh", AUDIO_DIR / slug / "zh.mp3"))

    print(f"Pack: {pack}")
    for lang, src, voice, language, dest in tracks:
        if not src.is_file():
            print(f"ERROR: missing {src}", file=sys.stderr)
            return 2
        text = src.read_text(encoding="utf-8").strip()
        n_chunks = len(_split_beats(text))
        print(
            f"  [{lang}] {src.name}: {len(text)} chars → {dest} "
            f"(voice={voice}, chunks={n_chunks})"
        )
        if args.dry_run:
            continue
        if not api_key:
            print(
                "ERROR: XAI_API_KEY not set.\n"
                "Put it in the repo-root .env (gitignored):\n"
                "  XAI_API_KEY=...\n",
                file=sys.stderr,
            )
            return 2
        print(f"  Synthesizing {lang}…")
        _synthesize(
            text,
            api_key=api_key,
            voice_id=voice,
            language=language,
            out=dest,
        )
        print(f"  Wrote {dest} ({dest.stat().st_size} bytes)")

    if args.dry_run:
        print("Dry-run complete (no API call).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
