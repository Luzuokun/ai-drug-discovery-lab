# PRODUCE — REINVENT4 Tutorial 07: Stop TL Before It Memorizes

Slug: `07-transfer-learning`  
Generator: `cursor-skill`  
Target: 3–5 min Discovery (xAI TTS + Imagine + ffmpeg slideshow)

## Status

| Step | Status |
|------|--------|
| Text pack | Done |
| Chapter + SVG cards | Done (`assets/`) |
| xAI stills | Run `images_xai.py 07-transfer-learning` |
| xAI TTS EN/ZH | Run `tts_xai.py 07-transfer-learning --lang both` |
| Slideshow draft | Run `render_slideshow.py 07-transfer-learning` → `youtube/renders/07-transfer-learning/draft.mp4` |

```bash
python scripts/youtube/images_xai.py 07-transfer-learning
python scripts/youtube/tts_xai.py 07-transfer-learning --lang both
python scripts/youtube/render_slideshow.py 07-transfer-learning
```

Audio/renders are gitignored. Optional: later insert live screencast in CapCut / 剪映 using `broll-checklist.md`.

## Slideshow map

| Id | Time | Image |
|----|------|-------|
| hook | 0–12s | `assets/ai/hook.png` |
| problem | 12–50s | `assets/pipeline.png` |
| proof_tl | 50–130s | `assets/tl-overfit-curve.png` |
| proof_rl | 130–175s | `assets/tl-vs-rl-compare.png` |
| mols | 175–190s | `assets/tl-ep24-molecules.png` |
| decision | 190–215s | `assets/metrics-callout.png` |
| cta | 215–240s | `assets/ai/cta.png` |

## YouTube Studio

### Title

REINVENT4 Tutorial 07: Stop TL Before It Memorizes

### Description

Paste English or 中文 block from `youtube-description.md`.

### Chapters

```
0:00 Eight epochs was a taste
0:12 The stop rule
0:50 Overfitting on 145 SMILES
2:10 TL then RL vs RL-only
3:10 What to keep
3:35 Site and GitHub
```

### Tags

```
REINVENT4, drug discovery, generative chemistry, AI drug design, cheminformatics, molecular generation, open science, AstraZeneca REINVENT, tutorial, machine learning, transfer learning, overfitting
```

## After upload

Do **not** embed the YouTube iframe in MkDocs until a real URL exists.
Do **not** commit `youtube/audio/` or `youtube/renders/`.
