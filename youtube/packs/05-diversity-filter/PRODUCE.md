# PRODUCE — REINVENT4 Tutorial 05: High Score Can Still Be Collapse

Slug: `05-diversity-filter`  
Generator: `cursor-skill`  
Target: 3–5 min Discovery (xAI TTS + Imagine + ffmpeg slideshow)

## Status

| Step | Status |
|------|--------|
| Text pack | Done |
| Chapter + SVG cards | Done (`assets/`) |
| xAI stills | Run `images_xai.py 05-diversity-filter` |
| xAI TTS EN/ZH | Run `tts_xai.py 05-diversity-filter --lang both` |
| Slideshow draft | Run `render_slideshow.py 05-diversity-filter` → `youtube/renders/05-diversity-filter/draft.mp4` |

```bash
python scripts/youtube/images_xai.py 05-diversity-filter
python scripts/youtube/tts_xai.py 05-diversity-filter --lang both
python scripts/youtube/render_slideshow.py 05-diversity-filter
```

Audio/renders are gitignored. Optional: later insert live screencast in CapCut / 剪映 using `broll-checklist.md`.

## Slideshow map

| Id | Time | Image |
|----|------|-------|
| hook | 0–12s | `assets/ai/hook.png` |
| problem | 12–50s | `assets/pipeline.png` |
| model | 50–95s | `assets/ai/mental-model.png` |
| proof | 95–145s | `assets/df-ab-compare.png` |
| scaf | 145–175s | `assets/no-df-top-scaffold.png` |
| fail | 175–215s | `assets/metrics-callout.png` |
| cta | 215–240s | `assets/ai/cta.png` |

## YouTube Studio

### Title

REINVENT4 Tutorial 05: High Score Can Still Be Collapse

### Description

Paste English or 中文 block from `youtube-description.md`.

### Chapters

```
0:00 Score is not a library
0:12 Why filters exist
0:50 A/B protocol
1:35 0.79 vs 0.74
2:55 Tune the knob
3:35 Site and GitHub
```

### Tags

```
REINVENT4, drug discovery, generative chemistry, AI drug design, cheminformatics, molecular generation, open science, AstraZeneca REINVENT, tutorial, machine learning, diversity filter, Murcko scaffold
```

## After upload

Do **not** embed the YouTube iframe in MkDocs until a real URL exists.
Do **not** commit `youtube/audio/` or `youtube/renders/`.
