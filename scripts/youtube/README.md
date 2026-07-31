# Markdown → YouTube text pack (V1)

Turn one MkDocs chapter into a **reviewable YouTube text pack** (script, storyboard,
ElevenLabs voiceover text, thumbnail prompt, B-roll list, description, chapters,
tags, EN/ZH subtitles). No TTS, editing, or upload in V1.

## Setup

```bash
source .venv/bin/activate
pip install -r requirements-youtube.txt   # keep separate from MkDocs CI deps
export OPENAI_API_KEY=sk-...              # or put in repo-root .env
```

Optional env vars: `YOUTUBE_OPENAI_MODEL` (default `gpt-4o`),
`YOUTUBE_SITE_BASE_URL`, `YOUTUBE_GITHUB_REPO_URL`, `YOUTUBE_PLAYLIST_URL`.

## Usage

```bash
# Available chapter (full text) → OpenAI → youtube/packs/<slug>/
python scripts/youtube/publish.py 01

# Coming Soon / outline chapter (acceptance bar + enrichment)
python scripts/youtube/publish.py 02 --allow-outline

# Inspect prompts without calling the API
python scripts/youtube/publish.py 02 --allow-outline --dry-run

# Re-materialize files from an existing pack.json (no API)
python scripts/youtube/publish.py 02 --from-json youtube/packs/02-priors-in-practice/pack.json
```

Accepts a path, slug, or chapter number (`02`, `02-priors-in-practice`, or a `.md` path).

## Output layout

```text
youtube/packs/<slug>/
  meta.yaml
  script.md / script-zh.md
  voiceover-en.txt / voiceover-zh.txt
  storyboard.md
  thumbnail-prompt.md
  broll-checklist.md
  youtube-description.md
  chapters.txt
  tags.txt
  subtitles-en.srt / subtitles-zh.srt
  pack.json
  REVIEW.md
```

Human next step: check `REVIEW.md`, especially `verify_flags`. After approval, V2 can
wire ElevenLabs + screencast editing.

## Design notes

- One chapter = one ~6–9 minute video (discovery). Site keeps the full tutorial.
- Outline chapters need `--allow-outline`; packs must not invent untagged metrics.
- Do not add `requirements-youtube.txt` packages to root `requirements.txt`.
