---
name: youtube-text-pack
description: >-
  Generate a reviewable YouTube text pack (5–8 min script, storyboard,
  TTS voiceover text, thumbnail prompt, B-roll, description, chapters,
  tags, EN/ZH subtitles) from one MkDocs chapter. Use when the user asks for
  YouTube script, video text pack, Markdown→YouTube, or /youtube-text-pack.
  Does NOT require an API key for text — the Cursor agent writes the pack files.
---

# YouTube text pack (Skill A)

Convert **one** handbook chapter into a discovery-oriented YouTube text pack.
Website = full tutorial. YouTube = discovery. GitHub = reproducibility.

## When to use

- User asks to generate a YouTube script / text pack / video assets for a chapter
- User invokes `/youtube-text-pack`
- After a chapter becomes Available and they want a reviewable pack before TTS

## When not to use

- User wants TTS audio, screencast editing, or upload → use `youtube-produce`
- User explicitly asks to call OpenAI via `publish.py --openai` → follow that path instead

## Hard rules

Read [references/style-guide.md](references/style-guide.md) before writing.

1. **No extra OpenAI API.** Do not install `requirements-youtube.txt` or call
   `publish.py` without `--from-json` unless the user explicitly requests `--openai`.
2. **Do not invent** metrics, filenames, or command outputs absent from the chapter.
   Speculative lines get `[VERIFY]` and must appear in `REVIEW.md` / `verify_flags`.
3. Video is **not** a read-aloud of the tutorial. Teach the decision frame.
4. Target **5–8 minutes** (300–480 s). EN primary; ZH mirrors the same beats.
5. One chapter = one pack under `youtube/packs/<slug>/`.
6. Set `meta.yaml` → `generator: cursor-skill`.

## Procedure

1. Resolve the chapter path (number, slug, or `.md`). Prefer EN under `docs/`;
   optionally skim `docs/zh/` if a full translation exists.
2. Read the full chapter. Note Learning Objectives, Why It Matters, key numbers
   in Expected Output, decision tables, and Common Errors.
3. Read [references/pack-layout.md](references/pack-layout.md) and
   [references/cta-links.md](references/cta-links.md).
4. Write **all** pack files listed in pack-layout (overwrite the slug directory).
5. Fill `REVIEW.md` with a human checklist and every `[VERIFY]` item.
6. Tell the user to start review at `youtube/packs/<slug>/REVIEW.md`.
   After approval, point them to `/youtube-produce`.

## Outline / Coming Soon chapters

Still allowed: frame the *decision problem* the chapter owns. Mark
`is_outline: true` in `meta.yaml`, warn in `REVIEW.md`, and expand `verify_flags`.

## Optional helper (no LLM)

If you already wrote a complete `pack.json` matching the schema in
`scripts/youtube/schema.py`, you may materialize files with:

```bash
python scripts/youtube/publish.py <slug> --from-json youtube/packs/<slug>/pack.json
```

This is optional — writing the markdown/txt/srt files directly is preferred.
