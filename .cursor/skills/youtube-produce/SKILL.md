---
name: youtube-produce
description: >-
  After a YouTube text pack is human-approved, prepare the production checklist
  (xAI TTS guidance, screencast order, edit timeline, YouTube upload
  paste blocks, MkDocs URL write-back). Use when the user asks for voiceover
  production, B-roll recording plan, editing prep, upload checklist, or
  /youtube-produce. Does not call xAI TTS/images or upload videos in this skill
  unless the user explicitly requests a production run.
---

# YouTube produce (Skill B)

Turn an approved `youtube/packs/<slug>/` text pack into a **production checklist**
(`PRODUCE.md`). Humans (or later tools) still run TTS, record, edit, and upload.

## When to use

- Text pack `REVIEW.md` checklist is mostly done / user approved the script
- User asks for TTS prep, screencast order, edit timeline, or upload paste
- User invokes `/youtube-produce`

## When not to use

- No pack exists yet → run `youtube-text-pack` first
- User only wants script changes → stay on `youtube-text-pack`

## Hard boundaries (this skill)

1. **Do not** call TTS/image APIs or write audio binaries unless the user
   explicitly asks to run production **and** `XAI_API_KEY` is available.
2. **Do not** auto-upload to YouTube.
3. **Do not** embed YouTube iframes into MkDocs until the user provides a real URL.
4. If API keys are missing, still write `PRODUCE.md` with copy-pasteable local command templates.

## Procedure

1. Confirm pack path: `youtube/packs/<slug>/` (ask if ambiguous).
2. Read: `REVIEW.md`, `voiceover-en.txt`, `voiceover-zh.txt`, `storyboard.md`,
   `broll-checklist.md`, `youtube-description.md`, `chapters.txt`, `tags.txt`,
   `meta.yaml`.
3. Read [references/produce-checklist.md](references/produce-checklist.md).
4. Write/overwrite `youtube/packs/<slug>/PRODUCE.md` with all sections from the
   reference template, filled with pack-specific content.
5. Summarize for the user: next manual actions in order (TTS → record → edit → upload → optional MkDocs link).

## Full pipeline helpers (document in PRODUCE.md)

```bash
# After text pack + assets exist (preferred: xAI):
python scripts/youtube/images_xai.py <slug>          # XAI_API_KEY
python scripts/youtube/tts_xai.py <slug> --lang en   # XAI_API_KEY
python scripts/youtube/render_slideshow.py <slug>    # → youtube/renders/<slug>/draft.mp4
```

Do not execute network TTS/image/upload unless the user explicitly requests it
**and** credentials are available. `render_slideshow.py` may run when local
audio + images already exist.
