# PRODUCE — REINVENT4 Tutorial 01: Your First AI Molecules in 4 Minutes

Slug: `01-installation-first-molecule`  
Generator: `cursor-skill`  
Target: 3–5 min Discovery (xAI TTS + Imagine + ffmpeg slideshow)

## Status

| Step | Status |
|------|--------|
| Text pack | Done |
| Chapter + SVG cards | Done (`assets/`) |
| xAI stills | Run `images_xai.py 01-installation-first-molecule` |
| xAI TTS EN/ZH | Run `tts_xai.py 01-installation-first-molecule --lang both` |
| Slideshow draft | Run `render_slideshow.py 01-installation-first-molecule` → `youtube/renders/01-installation-first-molecule/draft.mp4` |

```bash
python scripts/youtube/images_xai.py 01-installation-first-molecule
python scripts/youtube/tts_xai.py 01-installation-first-molecule --lang both
python scripts/youtube/render_slideshow.py 01-installation-first-molecule
```

Audio/renders are gitignored. Optional: later insert live screencast in CapCut / 剪映 using `broll-checklist.md`.

## Slideshow map

| Id | Time | Image |
|----|------|-------|
| hook | 0–12s | `assets/ai/hook.png` |
| problem | 12–50s | `assets/pipeline.png` |
| model | 50–95s | `assets/ai/mental-model.png` |
| proof | 95–140s | `assets/metrics-callout.png` |
| mols | 140–170s | `assets/first-molecules.png` |
| fail | 170–215s | `assets/ai/failures.png` |
| cta | 215–240s | `assets/ai/cta.png` |

## YouTube Studio

### Title

REINVENT4 Tutorial 01: Your First AI Molecules in 4 Minutes

### Description

Paste English or 中文 block from `youtube-description.md`.

### Chapters

```
0:00 You need sampled.csv
0:12 Install for real
0:50 Prior vs agent
1:35 96 molecules, seed 42
2:50 What NLL is not
3:35 Site and GitHub
```

### Tags

```
REINVENT4, drug discovery, generative chemistry, AI drug design, cheminformatics, molecular generation, open science, AstraZeneca REINVENT, tutorial, machine learning, installation, SMILES, sampling
```

## After upload

Do **not** embed the YouTube iframe in MkDocs until a real URL exists.
Do **not** commit `youtube/audio/` or `youtube/renders/`.
