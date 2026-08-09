# Markdown → YouTube pipeline

Discovery videos for handbook chapters. Website = docs, YouTube = discovery,
GitHub = reproducibility.

## Recommended flow (minimize manual work)

1. **Text pack** — Cursor skill [`youtube-text-pack`](../../.cursor/skills/youtube-text-pack)  
   → `youtube/packs/<slug>/` (5–8 min script, storyboard, subs, Description…)
2. **Assets** — chapter figures + SVG cards under `assets/`
3. **AI stills** (needs `OPENAI_API_KEY` with credits):

   ```bash
   python scripts/youtube/images_openai.py <slug>
   ```

4. **TTS** (needs real ElevenLabs secret `sk_…`):

   ```bash
   python scripts/youtube/tts_elevenlabs.py <slug> --lang en
   ```

5. **Slideshow draft** (ffmpeg):

   ```bash
   python scripts/youtube/render_slideshow.py <slug>
   # → youtube/renders/<slug>/draft.mp4  (gitignored)
   ```

6. **Produce checklist** — skill [`youtube-produce`](../../.cursor/skills/youtube-produce)  
   → `PRODUCE.md` (YouTube paste blocks; CapCut insert-screencast notes)

7. **You** — preview draft → optional CapCut screencast insert → upload.

## Setup

```bash
source .venv/bin/activate
pip install -r requirements-youtube.txt   # openai, elevenlabs, pyyaml, dotenv
# system: ffmpeg, librsvg2-bin (rsvg-convert) recommended
```

Repo-root `.env` (gitignored; see `.env.example`):

```bash
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=sk_...    # must be the secret, not the key ID
```

## Other helpers

```bash
python scripts/youtube/publish.py 03 --from-json youtube/packs/03-scoring-function/pack.json
python scripts/youtube/publish.py 03 --dry-run
python scripts/youtube/publish.py 03 --openai   # optional API text generation
```

## Layout

```text
youtube/packs/<slug>/
  … text pack files …
  slideshow.json
  assets/           # chapter + SVG PNG + scoring.toml.txt
  assets/ai/        # prompts.json + generated stills
  PRODUCE.md
youtube/audio/<slug>/en.mp3      # gitignored
youtube/renders/<slug>/draft.mp4 # gitignored
```
