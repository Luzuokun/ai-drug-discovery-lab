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


def _srt_ts_to_sec(ts: str) -> float:
    # HH:MM:SS,mmm
    hms, ms = ts.strip().split(",")
    h, m, s = hms.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def _sec_to_srt_ts(sec: float) -> str:
    if sec < 0:
        sec = 0.0
    ms_total = int(round(sec * 1000))
    h, rem = divmod(ms_total, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _scale_srt(src: Path, dest: Path, scale: float) -> None:
    """Scale subtitle cue times by factor (storyboard → actual audio)."""
    lines = src.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for line in lines:
        if "-->" in line:
            left, right = line.split("-->", 1)
            start = _sec_to_srt_ts(_srt_ts_to_sec(left) * scale)
            end = _sec_to_srt_ts(_srt_ts_to_sec(right) * scale)
            out.append(f"{start} --> {end}")
        else:
            out.append(line)
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")


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
            print(f"ERROR: missing audio {audio}. Run tts_xai.py first.", file=sys.stderr)
            return 2

    audio_dur = _ffprobe_duration(audio)
    planned_end = max(float(s["end_sec"]) for s in segments)
    # Fit all slides into the real voiceover length (storyboard times are targets).
    scale = (audio_dur / planned_end) if planned_end > 0 else 1.0
    print(f"Pack: {pack}")
    print(f"Audio: {audio} ({audio_dur:.1f}s)")
    if abs(scale - 1.0) > 0.02:
        print(
            f"  scaling slideshow {planned_end:.1f}s → {audio_dur:.1f}s "
            f"(factor {scale:.3f})"
        )

    out_dir = RENDERS_DIR / pack.name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_mp4 = out_dir / "draft.mp4"

    with tempfile.TemporaryDirectory(prefix="yt-slide-") as tmp:
        tmp_path = Path(tmp)
        clip_paths: list[Path] = []
        scaled_ends: list[float] = []

        for i, seg in enumerate(segments):
            start = float(seg["start_sec"]) * scale
            end = float(seg["end_sec"]) * scale
            if i == len(segments) - 1:
                end = audio_dur
            if i > 0:
                start = scaled_ends[-1]
            dur = max(0.5, end - start)
            scaled_ends.append(start + dur)
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
        subs_for_burn = None
        if not args.no_subs and subs.is_file():
            if abs(scale - 1.0) > 0.02:
                scaled_subs = tmp_path / "subtitles-scaled.srt"
                _scale_srt(subs, scaled_subs, scale)
                subs_for_burn = scaled_subs
            else:
                subs_for_burn = subs

        if subs_for_burn is not None:
            # Escape path for ffmpeg subtitles filter
            subs_esc = (
                str(subs_for_burn).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
            )
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
                str(muxed),
            ]

        print("  muxing audio" + (" + burned subs" if subs_for_burn is not None else ""))
        subprocess.run(cmd_mux, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        shutil.copy2(muxed, out_mp4)

    final_dur = _ffprobe_duration(out_mp4)
    print(f"Wrote {out_mp4} ({out_mp4.stat().st_size} bytes, {final_dur:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
