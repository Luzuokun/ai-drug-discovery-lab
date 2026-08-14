#!/usr/bin/env python3
"""Materialize 3–5 min Discovery packs + slideshow maps for REINVENT4 01–08.

Writes youtube/packs/<slug>/ text files, SVG/PNG cards, slideshow.json,
assets/ai/prompts.json, and PRODUCE.md. Does not call xAI APIs.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parents[1]
if str(_SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR.parent))

from youtube.writer import write_pack  # noqa: E402

SITE = "https://luzuokun.github.io/ai-drug-discovery-lab"
REPO = "https://github.com/Luzuokun/ai-drug-discovery-lab"
PACKS = _ROOT / "youtube" / "packs"
DOCS_ASSETS = _ROOT / "docs" / "assets" / "reinvent4"

TEAL = "#0f2a2e"
INK = "#e8f4f3"
MUTED = "#8fb8b4"
ACCENT = "#7fd4b8"
GOLD = "#f0c674"


def _cues_from_beats(beats: list[dict]) -> tuple[list[dict], list[dict]]:
    en, zh = [], []
    for b in beats:
        en.append(
            {
                "start_sec": b["start_sec"],
                "end_sec": b["end_sec"],
                "text": b["sub_en"],
            }
        )
        zh.append(
            {
                "start_sec": b["start_sec"],
                "end_sec": b["end_sec"],
                "text": b["sub_zh"],
            }
        )
    return en, zh


def _voice(beats: list[dict], key: str) -> str:
    return "\n\n".join(b[key].strip() for b in beats) + "\n"


def _script(title: str, beats: list[dict], lang: str) -> str:
    lines = [f"# {title}", ""]
    for b in beats:
        lines.append(f"## [{b['tc']}] {b['label_en'] if lang == 'en' else b['label_zh']}")
        lines.append("")
        lines.append(b["narration_en"] if lang == "en" else b["narration_zh"])
        lines.append("")
    return "\n".join(lines)


def _desc(slug: str, title_en: str, blurb_en: str, blurb_zh: str, chapters: list[dict]) -> tuple[str, str]:
    ch = "\n".join(f"{c['timecode']} {c['title']}" for c in chapters)
    site_en = f"{SITE}/molecular-generation/reinvent4/{slug}/"
    site_zh = f"{SITE}/zh/molecular-generation/reinvent4/{slug}/"
    gh = f"{REPO}/blob/main/docs/molecular-generation/reinvent4/{slug}.md"
    en = f"""{title_en}

{blurb_en}

This is a Discovery cut. The handbook is the knowledge base. GitHub is the reproducible configs and artifacts.

🔗 Full tutorial (site)
{site_en}
中文: {site_zh}

💻 GitHub
{gh}

📺 Series playlist
TODO_PLAYLIST_URL

Chapters
{ch}

#REINVENT4 #DrugDiscovery #GenerativeAI #Cheminformatics #OpenScience
"""
    zh = f"""{title_en}

{blurb_zh}

视频负责发现；完整命令与产物在网站；可复现配置在 GitHub。

🔗 完整教程
{site_zh}
English: {site_en}

💻 GitHub
{gh}

📺 系列播放列表
TODO_PLAYLIST_URL

章节
{ch}

#REINVENT4 #药物发现 #生成式AI
"""
    return en.strip() + "\n", zh.strip() + "\n"


def _storyboard(beats: list[dict]) -> list[dict]:
    rows = []
    for b in beats:
        rows.append(
            {
                "timecode": b["tc"],
                "shot": b["shot"],
                "on_screen_text": b["on_screen"],
                "voice_beat": b["label_en"],
                "asset_type": b["asset_type"],
            }
        )
    return rows


def write_svg_metrics(path: Path, title: str, rows: list[tuple[str, str]]) -> None:
    n = len(rows)
    h = 720
    box_h = min(90, 420 // max(n, 1))
    y0 = 160
    items = []
    for i, (k, v) in enumerate(rows):
        y = y0 + i * (box_h + 12)
        items.append(
            f'<rect x="120" y="{y}" width="1040" height="{box_h}" rx="12" fill="#14363a" stroke="#3d6b70"/>'
            f'<text x="160" y="{y + box_h * 0.62}" fill="{MUTED}" font-family="Helvetica, Arial, sans-serif" font-size="22">{_xml(k)}</text>'
            f'<text x="1160" y="{y + box_h * 0.62}" text-anchor="end" fill="{ACCENT}" font-family="Helvetica, Arial, sans-serif" font-size="28" font-weight="700">{_xml(v)}</text>'
        )
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{h}" viewBox="0 0 1280 {h}">
  <rect width="1280" height="{h}" fill="{TEAL}"/>
  <text x="640" y="80" text-anchor="middle" fill="{INK}" font-family="Georgia, serif" font-size="34" font-weight="700">{_xml(title)}</text>
  <text x="640" y="118" text-anchor="middle" fill="{MUTED}" font-family="Helvetica, Arial, sans-serif" font-size="18">Numbers from the handbook — seed 42 · CPU</text>
  {''.join(items)}
  <text x="640" y="690" text-anchor="middle" fill="#5f7f7c" font-family="Helvetica, Arial, sans-serif" font-size="14">AI Drug Discovery Lab · Discovery cut</text>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def write_svg_pipeline(path: Path, title: str, boxes: list[tuple[str, str, bool]]) -> None:
    w = 340
    gap = 40
    total = len(boxes) * w + (len(boxes) - 1) * gap
    x0 = (1280 - total) / 2
    parts = []
    for i, (name, sub, hot) in enumerate(boxes):
        x = x0 + i * (w + gap)
        fill = "#1b4a3a" if hot else "#14363a"
        stroke = "#4a9b78" if hot else "#3d6b70"
        sw = 3 if hot else 2
        parts.append(
            f'<rect x="{x}" y="220" width="{w}" height="280" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<text x="{x + w/2}" y="310" text-anchor="middle" fill="{INK}" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700">{_xml(name)}</text>'
            f'<text x="{x + w/2}" y="360" text-anchor="middle" fill="{MUTED}" font-family="Helvetica, Arial, sans-serif" font-size="16">{_xml(sub)}</text>'
        )
        if i < len(boxes) - 1:
            parts.append(
                f'<text x="{x + w + gap/2}" y="370" text-anchor="middle" fill="{ACCENT}" font-family="Helvetica, Arial, sans-serif" font-size="36">&gt;</text>'
            )
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="{TEAL}"/>
  <text x="640" y="90" text-anchor="middle" fill="{INK}" font-family="Georgia, serif" font-size="34" font-weight="700">{_xml(title)}</text>
  {''.join(parts)}
  <text x="640" y="620" text-anchor="middle" fill="{GOLD}" font-family="Helvetica, Arial, sans-serif" font-size="20">Website = docs · YouTube = discovery · GitHub = reproduce</text>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def _xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_to_png(svg: Path, png: Path) -> None:
    import subprocess

    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        proc = subprocess.run(
            [rsvg, "-w", "1920", "-h", "1080", "-o", str(png), str(svg)],
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0 and png.is_file():
            return
        print(f"  rsvg-convert failed for {svg.name}: {(proc.stderr or '')[-200:]}")
    try:
        import cairosvg  # type: ignore

        cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=1920, output_height=1080)
        return
    except Exception:
        pass
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
        fig.patch.set_facecolor(TEAL)
        ax.set_facecolor(TEAL)
        ax.axis("off")
        ax.text(
            0.5,
            0.5,
            svg.stem.replace("-", " "),
            ha="center",
            va="center",
            color=INK,
            fontsize=28,
        )
        fig.savefig(png, facecolor=TEAL)
        plt.close(fig)
    except Exception as exc:
        print(f"  skip rasterize {svg.name}: {exc}")


def write_produce(dest: Path, spec: dict) -> None:
    slug = spec["slug"]
    title = spec["title_en"]
    segs = spec["slideshow"]
    rows = "\n".join(
        f"| {s['id']} | {s['start_sec']}–{s['end_sec']}s | `{s['image']}` |"
        for s in segs
    )
    text = f"""# PRODUCE — {title}

Slug: `{slug}`  
Generator: `cursor-skill`  
Target: 3–5 min Discovery (xAI TTS + Imagine + ffmpeg slideshow)

## Status

| Step | Status |
|------|--------|
| Text pack | Done |
| Chapter + SVG cards | Done (`assets/`) |
| xAI stills | Run `images_xai.py {slug}` |
| xAI TTS EN/ZH | Run `tts_xai.py {slug} --lang both` |
| Slideshow draft | Run `render_slideshow.py {slug}` → `youtube/renders/{slug}/draft.mp4` |

```bash
python scripts/youtube/images_xai.py {slug}
python scripts/youtube/tts_xai.py {slug} --lang both
python scripts/youtube/render_slideshow.py {slug}
```

Audio/renders are gitignored. Optional: later insert live screencast in CapCut / 剪映 using `broll-checklist.md`.

## Slideshow map

| Id | Time | Image |
|----|------|-------|
{rows}

## YouTube Studio

### Title

{title}

### Description

Paste English or 中文 block from `youtube-description.md`.

### Chapters

```
{(dest / 'chapters.txt').read_text(encoding='utf-8').strip()}
```

### Tags

```
{(dest / 'tags.txt').read_text(encoding='utf-8').strip()}
```

## After upload

Do **not** embed the YouTube iframe in MkDocs until a real URL exists.
Do **not** commit `youtube/audio/` or `youtube/renders/`.
"""
    (dest / "PRODUCE.md").write_text(text, encoding="utf-8")


def materialize(spec: dict) -> Path:
    slug = spec["slug"]
    beats = spec["beats"]
    chapters = spec["chapters"]
    desc_en, desc_zh = _desc(slug, spec["title_en"], spec["blurb_en"], spec["blurb_zh"], chapters)
    sub_en, sub_zh = _cues_from_beats(beats)
    data = {
        "title_en": spec["title_en"],
        "title_zh": spec["title_zh"],
        "target_duration_seconds": spec["duration"],
        "hook_en": beats[0]["narration_en"],
        "hook_zh": beats[0]["narration_zh"],
        "beats": [
            {
                "id": b["id"],
                "start_sec": b["start_sec"],
                "end_sec": b["end_sec"],
                "label_en": b["label_en"],
                "label_zh": b["label_zh"],
                "narration_en": b["narration_en"],
                "narration_zh": b["narration_zh"],
                "visual": b["shot"],
            }
            for b in beats
        ],
        "script_en": _script(spec["title_en"], beats, "en"),
        "script_zh": _script(spec["title_zh"], beats, "zh"),
        "voiceover_en": _voice(beats, "narration_en"),
        "voiceover_zh": _voice(beats, "narration_zh"),
        "storyboard": _storyboard(beats),
        "thumbnail_title": spec["thumb_title"],
        "thumbnail_prompt": spec["thumb_prompt"],
        "broll": spec["broll"],
        "youtube_description_en": desc_en,
        "youtube_description_zh": desc_zh,
        "chapters": chapters,
        "tags": spec["tags"],
        "subtitles_en": sub_en,
        "subtitles_zh": sub_zh,
        "verify_flags": spec.get("verify_flags")
        or ["[VERIFY] Playlist URL still TODO_PLAYLIST_URL"],
    }
    brief = {
        "slug": slug,
        "path": str(_ROOT / "docs" / "molecular-generation" / "reinvent4" / f"{slug}.md"),
        "is_outline": False,
        "site_path_en": f"molecular-generation/reinvent4/{slug}/",
        "site_path_zh": f"zh/molecular-generation/reinvent4/{slug}/",
    }
    dest = write_pack(
        data,
        brief=brief,
        model="n/a",
        generator="cursor-skill",
        site_base_url=SITE,
        github_repo_url=REPO,
    )
    assets = dest / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "ai").mkdir(parents=True, exist_ok=True)

    write_svg_metrics(assets / "metrics-callout.svg", spec["metrics_title"], spec["metrics_rows"])
    write_svg_pipeline(assets / "pipeline.svg", spec["pipeline_title"], spec["pipeline_boxes"])
    svg_to_png(assets / "metrics-callout.svg", assets / "metrics-callout.png")
    svg_to_png(assets / "pipeline.svg", assets / "pipeline.png")

    for src_rel, name in spec.get("copy_images") or []:
        src = DOCS_ASSETS / src_rel
        if src.is_file():
            shutil.copy2(src, assets / name)

    prompts = {
        "model_preference": ["grok-imagine-image-quality"],
        "aspect_ratio": "16:9",
        "images": spec["ai_images"],
    }
    (assets / "ai" / "prompts.json").write_text(
        json.dumps(prompts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (assets / "ASSETS.md").write_text(
        f"# {slug} pack assets\n\nHandbook figures + SVG cards + `ai/` Imagine stills.\n"
        "Slideshow: `../slideshow.json`.\n",
        encoding="utf-8",
    )
    slideshow = {
        "slug": slug,
        "audio": f"youtube/audio/{slug}/en.mp3",
        "subtitles": f"youtube/packs/{slug}/subtitles-en.srt",
        "width": 1920,
        "height": 1080,
        "fade_sec": 0.25,
        "segments": spec["slideshow"],
    }
    (dest / "slideshow.json").write_text(
        json.dumps(slideshow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_produce(dest, spec)
    return dest
