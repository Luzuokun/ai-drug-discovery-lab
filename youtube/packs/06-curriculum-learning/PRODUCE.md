# PRODUCE — REINVENT4 Tutorial 06: Escalate Objectives — Don't Front-Load Hardness

Slug: `06-curriculum-learning`  
Generator: `cursor-skill`  
Target: 3–5 min Discovery (xAI TTS + Imagine + ffmpeg slideshow)

## Status

| Step | Status |
|------|--------|
| Text pack | Done |
| Chapter + SVG cards | Done (`assets/`) |
| xAI stills | Run `images_xai.py 06-curriculum-learning` |
| xAI TTS EN/ZH | Run `tts_xai.py 06-curriculum-learning --lang both` |
| Slideshow draft | Run `render_slideshow.py 06-curriculum-learning` → `youtube/renders/06-curriculum-learning/draft.mp4` |

```bash
python scripts/youtube/images_xai.py 06-curriculum-learning
python scripts/youtube/tts_xai.py 06-curriculum-learning --lang both
python scripts/youtube/render_slideshow.py 06-curriculum-learning
```

Audio/renders are gitignored. Optional: later insert live screencast in CapCut / 剪映 using `broll-checklist.md`.

## Slideshow map

| Id | Time | Image |
|----|------|-------|
| hook | 0–12s | `assets/ai/hook.png` |
| problem | 12–55s | `assets/pipeline.png` |
| model | 55–100s | `assets/ai/mental-model.png` |
| proof | 100–155s | `assets/curriculum-score-stages.png` |
| mols | 155–175s | `assets/stage2-top-molecules.png` |
| manual | 175–215s | `assets/manual-curriculum-scores.png` |
| cta | 215–240s | `assets/ai/cta.png` |

## YouTube Studio

### Title

REINVENT4 Tutorial 06: Escalate Objectives — Don't Front-Load Hardness

### Description

Paste English or 中文 block from `youtube-description.md`.

### Chapters

```
0:00 Not a new algorithm
0:12 Easy then hard
0:55 max_steps kills the rest
1:40 Early-stop at step 12
2:55 Auto vs manual
3:35 Site and GitHub
```

### Tags

```
REINVENT4, drug discovery, generative chemistry, AI drug design, cheminformatics, molecular generation, open science, AstraZeneca REINVENT, tutorial, machine learning, curriculum learning, staged learning
```

## After upload

Do **not** embed the YouTube iframe in MkDocs until a real URL exists.
Do **not** commit `youtube/audio/` or `youtube/renders/`.
