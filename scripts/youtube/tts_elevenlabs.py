#!/usr/bin/env python3
"""Generate TTS audio from a YouTube pack voiceover via ElevenLabs.

Reads ELEVENLABS_API_KEY from the environment or repo-root .env (gitignored).
Does not commit audio; writes under youtube/audio/<slug>/ (gitignored).

Examples:
  python scripts/youtube/tts_elevenlabs.py 02
  python scripts/youtube/tts_elevenlabs.py 02 --lang zh
  python scripts/youtube/tts_elevenlabs.py 02 --lang both --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parents[1]
if str(_SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR.parent))

from youtube.parse_chapter import resolve_chapter_path  # noqa: E402

PACKS_DIR = _ROOT / "youtube" / "packs"
AUDIO_DIR = _ROOT / "youtube" / "audio"

# Defaults — override with env or CLI.
# Premade "Adam" — works on free API keys. Library voices often return 402.
DEFAULT_VOICE_EN = os.environ.get("ELEVENLABS_VOICE_ID_EN", "pNInz6obpgDQGcFmaJgB")
DEFAULT_VOICE_ZH = os.environ.get("ELEVENLABS_VOICE_ID_ZH", DEFAULT_VOICE_EN)
DEFAULT_MODEL = os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


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
    # Prefer existing pack slug; fall back to resolving chapter path stem.
    candidate = PACKS_DIR / chapter
    if (candidate / "voiceover-en.txt").is_file():
        return candidate
    # numeric / slug without packs prefix
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


def _synthesize(text: str, *, voice_id: str, model_id: str, api_key: str, out: Path) -> None:
    try:
        from elevenlabs.client import ElevenLabs
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Missing dependency 'elevenlabs'. Install with:\n"
            "  pip install -r requirements-youtube.txt"
        ) from exc

    client = ElevenLabs(api_key=api_key)
    audio_iter = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=text,
        output_format="mp3_44100_128",
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        for chunk in audio_iter:
            if chunk:
                fh.write(chunk)


def main(argv: list[str] | None = None) -> int:
    _load_dotenv()
    p = argparse.ArgumentParser(description="ElevenLabs TTS for a YouTube text pack.")
    p.add_argument("chapter", help="Pack slug, chapter number, or path (e.g. 02)")
    p.add_argument(
        "--lang",
        choices=("en", "zh", "both"),
        default="en",
        help="Which voiceover track(s) to synthesize (default: en)",
    )
    p.add_argument("--voice-en", default=DEFAULT_VOICE_EN, help="ElevenLabs voice id (EN)")
    p.add_argument("--voice-zh", default=DEFAULT_VOICE_ZH, help="ElevenLabs voice id (ZH)")
    p.add_argument("--model-id", default=DEFAULT_MODEL, help="ElevenLabs model id")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths and character counts; do not call the API.",
    )
    args = p.parse_args(argv)

    pack = _pack_dir_from_arg(args.chapter)
    slug = pack.name
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()

    tracks: list[tuple[str, Path, str, Path]] = []
    if args.lang in ("en", "both"):
        tracks.append(
            (
                "en",
                pack / "voiceover-en.txt",
                args.voice_en,
                AUDIO_DIR / slug / "en.mp3",
            )
        )
    if args.lang in ("zh", "both"):
        tracks.append(
            (
                "zh",
                pack / "voiceover-zh.txt",
                args.voice_zh,
                AUDIO_DIR / slug / "zh.mp3",
            )
        )

    print(f"Pack: {pack}")
    for lang, src, voice, dest in tracks:
        if not src.is_file():
            print(f"ERROR: missing {src}", file=sys.stderr)
            return 2
        text = src.read_text(encoding="utf-8").strip()
        print(f"  [{lang}] {src.name}: {len(text)} chars → {dest} (voice={voice})")
        if args.dry_run:
            continue
        if not api_key:
            print(
                "ERROR: ELEVENLABS_API_KEY not set.\n"
                "Put it in the repo-root .env (gitignored) or export it:\n"
                "  ELEVENLABS_API_KEY=...\n",
                file=sys.stderr,
            )
            return 2
        print(f"  Synthesizing {lang}…")
        _synthesize(text, voice_id=voice, model_id=args.model_id, api_key=api_key, out=dest)
        print(f"  Wrote {dest} ({dest.stat().st_size} bytes)")

    if args.dry_run:
        print("Dry-run complete (no API call).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
