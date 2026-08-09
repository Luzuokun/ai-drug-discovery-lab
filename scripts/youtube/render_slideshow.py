#!/usr/bin/env python3
"""Render a near-final slideshow MP4 from pack visuals + EN TTS.

Uses ffmpeg: static slides with short fade, burned-in EN subtitles, AAC audio.

Examples:
  python scripts/youtube/render_slideshow.py 03
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parents[1]
PACKS_DIR = _ROOT / "youtube" / "packs"
RENDERS_DIR = _ROOT / "youtube" / "renders"


def _resolve_pack(chapter: str) -> Path:
    for child in sorted(PACKS_DIR.iterdir()) if PACKS_DIR.is_dir() else []:
        if not child.is_dir():
            continue
        if child.name == chapter or child.name.startswith(f"{chapter}-") or (
            chapter.isdigit() and child.name.startswith(chapter.zfill(2))
        ):
            return child
    raise FileNotFoundError(f"No pack for chapter '{chapter}'")


def _ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def _resolve_image(pack: Path, rel: str, fallback: str) -> Path:
    primary = (pack / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
    # slideshow.json paths are relative to pack/
    cand = pack / rel
    if cand.is_file():
        return cand
    fb = pack / fallback
    if fb.is_file():
        return fb
    raise FileNotFoundError(f"Missing image {rel} and fallback {fallback}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="ffmpeg slideshow renderer for a YouTube pack.")
    p.add_argument("chapter", help="Pack slug or number (e.g. 03)")
    p.add_argument("--no-subs", action="store_true", help="Skip burning subtitles")
    args = p.parse_args(argv)

    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg not found on PATH. Install ffmpeg and retry.", file=sys.stderr)
        return 2

    pack = _resolve_pack(args.chapter)
    slide_path = pack / "slideshow.json"
    if not slide_path.is_file():
        print(f"ERROR: missing {slide_path}", file=sys.stderr)
        return 2

    cfg = json.loads(slide_path.read_text(encoding="utf-8"))
    width = int(cfg.get("width") or 1920)
    height = int(cfg.get("height") or 1080)
    fade = float(cfg.get("fade_sec") or 0.3)
    segments = cfg["segments"]

    audio_rel = cfg.get("audio") or f"youtube/audio/{pack.name}/en.mp3"
    audio = _ROOT / audio_rel if not Path(audio_rel).is_absolute() else Path(audio_rel)
    if not audio.is_file():
        # also try pack-relative convention
        alt = _ROOT / "youtube" / "audio" / pack.name / "en.mp3"
        if alt.is_file():
            audio = alt
        else:
            print(f"ERROR: missing audio {audio}. Run tts_elevenlabs.py first.", file=sys.stderr)
            return 2

    audio_dur = _ffprobe_duration(audio)
    print(f"Pack: {pack}")
    print(f"Audio: {audio} ({audio_dur:.1f}s)")

    out_dir = RENDERS_DIR / pack.name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_mp4 = out_dir / "draft.mp4"

    with tempfile.TemporaryDirectory(prefix="yt-slide-") as tmp:
        tmp_path = Path(tmp)
        clip_paths: list[Path] = []

        for i, seg in enumerate(segments):
            start = float(seg["start_sec"])
            end = float(seg["end_sec"])
            # stretch/clamp last segment to audio end if needed
            if i == len(segments) - 1:
                end = max(end, audio_dur)
            dur = max(0.5, end - start)
            img = _resolve_image(pack, seg["image"], seg.get("fallback") or seg["image"])
            clip = tmp_path / f"clip_{i:02d}.mp4"
            # scale/pad to 1080p, hold still, optional fade-in
            fade_d = min(fade, dur / 3)
            vf = (
                f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
                f"format=yuv420p,fade=t=in:st=0:d={fade_d}"
            )
            cmd = [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                str(img),
                "-t",
                f"{dur:.3f}",
                "-vf",
                vf,
                "-r",
                "30",
                "-an",
                str(clip),
            ]
            print(f"  clip {i}: {img.name} ({dur:.1f}s)")
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            clip_paths.append(clip)

        concat_list = tmp_path / "concat.txt"
        concat_list.write_text(
            "\n".join(f"file '{c.as_posix()}'" for c in clip_paths) + "\n",
            encoding="utf-8",
        )
        silent = tmp_path / "video_silent.mp4"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-c",
                "copy",
                str(silent),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        subs = pack / "subtitles-en.srt"
        muxed = tmp_path / "with_audio.mp4"
        cmd_mux = [
            "ffmpeg",
            "-y",
            "-i",
            str(silent),
            "-i",
            str(audio),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
        ]
        if not args.no_subs and subs.is_file():
            # burn-in subtitles
            # Escape path for ffmpeg subtitles filter
            subs_esc = str(subs).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
            cmd_mux = [
                "ffmpeg",
                "-y",
                "-i",
                str(silent),
                "-i",
                str(audio),
                "-vf",
                f"subtitles={subs_esc}:force_style='FontSize=22,Outline=1'",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
                "-movflags",
                "+faststart",
                str(muxed),
            ]
        else:
            cmd_mux.append(str(muxed))

        print("  muxing audio" + (" + burned subs" if not args.no_subs and subs.is_file() else ""))
        subprocess.run(cmd_mux, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        shutil.copy2(muxed, out_mp4)

    final_dur = _ffprobe_duration(out_mp4)
    print(f"Wrote {out_mp4} ({out_mp4.stat().st_size} bytes, {final_dur:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
