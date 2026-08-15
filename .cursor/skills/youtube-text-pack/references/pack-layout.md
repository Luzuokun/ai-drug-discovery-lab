# Pack layout

Output directory: `youtube/packs/<slug>/`  
Example slug: `02-priors-in-practice`

| File | Purpose |
|------|---------|
| `meta.yaml` | slug, titles, source_md (repo-relative), generator, duration, site URLs, verify_flags |
| `script.md` | EN shooting script with beat headers `[0:00–0:15 Hook]` |
| `script-zh.md` | ZH shooting script, same beat structure |
| `voiceover-en.txt` | Plain TTS text (no markdown); blank line between beats |
| `voiceover-zh.txt` | ZH TTS text |
| `storyboard.md` | Table: Timecode / Shot / On-screen text / Voice beat / Asset type |
| `thumbnail-prompt.md` | Thumbnail title + image-gen prompt (safe text zone) |
| `broll-checklist.md` | Checkbox list: item, why, source_hint |
| `youtube-description.md` | EN + ZH descriptions with site/GitHub/playlist links |
| `chapters.txt` | YouTube chapters (`0:00 Title`) |
| `tags.txt` | Comma-separated tags |
| `subtitles-en.srt` | EN cues aligned to beats |
| `subtitles-zh.srt` | ZH cues |
| `pack.json` | Structured JSON (optional but recommended for re-materialize) |
| `REVIEW.md` | Human checklist + verify_flags |

## `meta.yaml` required fields

```yaml
slug: 02-priors-in-practice
title_en: "..."
title_zh: "..."
source_md: docs/molecular-generation/reinvent4/02-priors-in-practice.md
is_outline: false
generator: cursor-skill
model: n/a
target_duration_seconds: 240
generated_at: "<ISO-8601 UTC>"
site_url_en: https://luzuokun.github.io/ai-drug-discovery-lab/molecular-generation/reinvent4/<slug>/
site_url_zh: https://luzuokun.github.io/ai-drug-discovery-lab/zh/molecular-generation/reinvent4/<slug>/
github_repo_url: https://github.com/Luzuokun/ai-drug-discovery-lab
verify_flags: []
```

## Storyboard `asset_type` enum

`talking_head` | `screencast` | `diagram` | `molecule_anim` | `terminal` | `broll` | `title_card` | `cta_card`
