# PRODUCE.md template

Write this file to `youtube/packs/<slug>/PRODUCE.md`.

```markdown
# PRODUCE — <title_en>

Slug: `<slug>`
Text pack generator: `<meta.generator>`
Status: awaiting TTS / screencast / edit / upload

## 0. Preconditions

- [ ] `REVIEW.md` approved (or explicitly waived)
- [ ] `verify_flags` resolved or accepted
- [ ] Voice language track(s): EN / ZH / both

## 1. ElevenLabs (TTS) — do not auto-run in Skill B

**Inputs:** `voiceover-en.txt`, `voiceover-zh.txt`

Suggested settings (adjust to your voice library):

| Track | File | Style notes |
|-------|------|-------------|
| EN | voiceover-en.txt | Clear science explainer; moderate pace; pause on blank lines |
| ZH | voiceover-zh.txt | Same beat timing intent as EN |

Local command stubs:

```bash
# 1) Put the key in repo-root .env (gitignored) — see .env.example
#    ELEVENLABS_API_KEY=...
# 2) Install optional deps once
pip install -r requirements-youtube.txt
# 3) Dry-run, then synthesize
python scripts/youtube/tts_elevenlabs.py <slug> --lang both --dry-run
python scripts/youtube/tts_elevenlabs.py <slug> --lang en
python scripts/youtube/tts_elevenlabs.py <slug> --lang zh
```

Output target: `youtube/audio/<slug>/en.mp3` and/or `zh.mp3` (gitignored).

## 2. Screencast / B-roll order

Follow `broll-checklist.md` and `storyboard.md`. Recommended record order:

1. …
2. …

## 3. Edit timeline summary

| Timecode | Picture | Audio beat |
|----------|---------|------------|
| … | … | … |

Align picture cuts to `chapters.txt`. Burn or soft-load `subtitles-*.srt`.

## 4. YouTube Studio paste blocks

### Title

<from meta / thumbnail title>

### Description

<paste from youtube-description.md — chosen language>

### Chapters

```
<paste chapters.txt>
```

### Tags

```
<paste tags.txt>
```

### Thumbnail

Generate from `thumbnail-prompt.md`; keep title readable on mobile.

## 5. After upload

1. Copy the public video URL.
2. Optionally add to playlist (`TODO_PLAYLIST_URL` → real URL).
3. Only then consider linking from the MkDocs chapter (user approval required).
4. Do **not** commit large media under `youtube/audio/` or `youtube/renders/`.
```

Fill every `…` from the specific pack. Keep checkboxes actionable.
