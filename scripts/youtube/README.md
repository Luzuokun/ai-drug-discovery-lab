# Markdown → YouTube text pack

Turn one MkDocs chapter into a **reviewable YouTube text pack** (script, storyboard,
ElevenLabs voiceover text, thumbnail prompt, B-roll list, description, chapters,
tags, EN/ZH subtitles). No TTS, editing, or upload here.

## Recommended path (no OpenAI API key)

Use the Cursor Agent skill:

- **Text pack:** [`.cursor/skills/youtube-text-pack`](../../.cursor/skills/youtube-text-pack)  
  Invoke with `/youtube-text-pack` or ask the agent to generate a video text pack.
- **After text approval — production checklist:**  
  [`.cursor/skills/youtube-produce`](../../.cursor/skills/youtube-produce)  
  (`/youtube-produce` → writes `PRODUCE.md`; does not call ElevenLabs).

The agent writes files under `youtube/packs/<slug>/` directly.

## Optional CLI helpers

```bash
source .venv/bin/activate
# only needed for --openai
pip install -r requirements-youtube.txt
```

```bash
# Materialize files from an existing pack.json (no LLM)
python scripts/youtube/publish.py 02 --from-json youtube/packs/02-priors-in-practice/pack.json

# Inspect the legacy OpenAI prompt brief
python scripts/youtube/publish.py 02 --dry-run

# Optional API path (explicit)
export OPENAI_API_KEY=sk-...
python scripts/youtube/publish.py 02 --openai
```

Coming Soon / outline chapters still need `--allow-outline` when using `--openai`.

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
  PRODUCE.md          # after /youtube-produce
```

Human next step: check `REVIEW.md`. After approval, run `/youtube-produce`.

## Design notes

- One chapter = one ~6–9 minute video (discovery). Site keeps the full tutorial.
- Keep youtube Python deps in `requirements-youtube.txt` (not MkDocs CI).
- `.env`, `youtube/audio/`, and `youtube/renders/` are gitignored.
