"""Write a validated pack dict into youtube/packs/<slug>/."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .schema import validate_pack

ROOT = Path(__file__).resolve().parents[2]
PACKS_DIR = ROOT / "youtube" / "packs"


def _sec_to_srt_time(sec: float) -> str:
    if sec < 0:
        sec = 0
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    seconds = int(sec % 60)
    millis = int(round((sec - int(sec)) * 1000))
    if millis == 1000:
        seconds += 1
        millis = 0
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def _cues_to_srt(cues: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for i, cue in enumerate(cues, start=1):
        start = _sec_to_srt_time(float(cue["start_sec"]))
        end = _sec_to_srt_time(float(cue["end_sec"]))
        text = str(cue["text"]).strip()
        blocks.append(f"{i}\n{start} --> {end}\n{text}")
    return "\n\n".join(blocks) + "\n"


def _storyboard_md(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Storyboard",
        "",
        "| Timecode | Shot | On-screen text | Voice beat | Asset type |",
        "|----------|------|----------------|------------|------------|",
    ]
    for row in rows:
        lines.append(
            "| {timecode} | {shot} | {on_screen_text} | {voice_beat} | `{asset_type}` |".format(
                **{k: str(row.get(k, "")).replace("|", "\\|") for k in (
                    "timecode",
                    "shot",
                    "on_screen_text",
                    "voice_beat",
                    "asset_type",
                )}
            )
        )
    return "\n".join(lines) + "\n"


def _broll_md(items: list[dict[str, Any]]) -> str:
    lines = ["# B-roll checklist", ""]
    for i, item in enumerate(items, start=1):
        lines.append(f"- [ ] **{item.get('item', '')}**")
        lines.append(f"  - Why: {item.get('why', '')}")
        lines.append(f"  - Source hint: {item.get('source_hint', '')}")
        lines.append("")
    return "\n".join(lines)


def _chapters_txt(chapters: list[dict[str, Any]]) -> str:
    return "\n".join(f"{c['timecode']} {c['title']}" for c in chapters) + "\n"


def _review_md(
    *,
    title: str,
    slug: str,
    is_outline: bool,
    verify_flags: list[str],
    generator: str,
) -> str:
    flags = "\n".join(f"- {f}" for f in verify_flags) or "- (none)"
    outline_note = (
        "\n> **Source chapter is Coming Soon / outline-only.** "
        "Treat protocol details as provisional until the full MkDocs chapter ships.\n"
        if is_outline
        else ""
    )
    return f"""# REVIEW — {title}

Slug: `{slug}`  
Generator: `{generator}`  
{outline_note}
## Checklist

- [ ] Hook lands in ≤15s and states a concrete curiosity gap
- [ ] Runtime feels 5–8 minutes (read script aloud once)
- [ ] No invented metrics/commands without `[VERIFY]`
- [ ] CTA includes site deep-link + GitHub path
- [ ] EN/ZH beats stay aligned
- [ ] Thumbnail title is readable on mobile
- [ ] B-roll list is filmable with assets we actually have (or plan to record)

## verify_flags

{flags}

## Next step (V2 — after you approve this pack)

1. xAI TTS from `voiceover-en.txt` / `voiceover-zh.txt`
2. Record screencast items in `broll-checklist.md`
3. Edit to `storyboard.md` + burn `subtitles-*.srt`
4. Upload; paste real URL back into the MkDocs chapter
"""


def write_pack(
    data: dict[str, Any],
    *,
    brief: dict[str, Any],
    model: str,
    generator: str,
    site_base_url: str,
    github_repo_url: str,
    out_dir: Path | None = None,
) -> Path:
    errors = validate_pack(data)
    if errors:
        raise ValueError("Cannot write invalid pack:\n- " + "\n- ".join(errors))

    slug = brief["slug"]
    dest = out_dir or (PACKS_DIR / slug)
    dest.mkdir(parents=True, exist_ok=True)

    source_md = brief["path"]
    try:
        source_md = str(Path(source_md).resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        pass

    meta = {
        "slug": slug,
        "title_en": data["title_en"],
        "title_zh": data["title_zh"],
        "source_md": source_md,
        "is_outline": brief.get("is_outline", False),
        "generator": generator,
        "model": model,
        "target_duration_seconds": data["target_duration_seconds"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "site_url_en": f"{site_base_url.rstrip('/')}/{brief['site_path_en']}",
        "site_url_zh": f"{site_base_url.rstrip('/')}/{brief['site_path_zh']}",
        "github_repo_url": github_repo_url,
        "verify_flags": data.get("verify_flags", []),
    }
    (dest / "meta.yaml").write_text(
        yaml.safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    (dest / "script.md").write_text(data["script_en"].rstrip() + "\n", encoding="utf-8")
    (dest / "script-zh.md").write_text(
        data["script_zh"].rstrip() + "\n", encoding="utf-8"
    )
    (dest / "voiceover-en.txt").write_text(
        data["voiceover_en"].rstrip() + "\n", encoding="utf-8"
    )
    (dest / "voiceover-zh.txt").write_text(
        data["voiceover_zh"].rstrip() + "\n", encoding="utf-8"
    )
    (dest / "storyboard.md").write_text(
        _storyboard_md(data["storyboard"]), encoding="utf-8"
    )
    (dest / "thumbnail-prompt.md").write_text(
        f"# Thumbnail\n\n**Title:** {data['thumbnail_title']}\n\n"
        f"## Image prompt\n\n{data['thumbnail_prompt'].rstrip()}\n",
        encoding="utf-8",
    )
    (dest / "broll-checklist.md").write_text(_broll_md(data["broll"]), encoding="utf-8")
    (dest / "youtube-description.md").write_text(
        "# YouTube Description\n\n## English\n\n"
        + data["youtube_description_en"].rstrip()
        + "\n\n## 中文\n\n"
        + data["youtube_description_zh"].rstrip()
        + "\n",
        encoding="utf-8",
    )
    (dest / "chapters.txt").write_text(_chapters_txt(data["chapters"]), encoding="utf-8")
    (dest / "tags.txt").write_text(", ".join(data["tags"]) + "\n", encoding="utf-8")
    (dest / "subtitles-en.srt").write_text(
        _cues_to_srt(data["subtitles_en"]), encoding="utf-8"
    )
    (dest / "subtitles-zh.srt").write_text(
        _cues_to_srt(data["subtitles_zh"]), encoding="utf-8"
    )
    (dest / "pack.json").write_text(
        __import__("json").dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (dest / "REVIEW.md").write_text(
        _review_md(
            title=data["title_en"],
            slug=slug,
            is_outline=bool(brief.get("is_outline")),
            verify_flags=list(data.get("verify_flags") or []),
            generator=generator,
        ),
        encoding="utf-8",
    )
    return dest
