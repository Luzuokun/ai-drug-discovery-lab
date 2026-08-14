# PRODUCE — REINVENT4 Tutorial 08: Docking in the Loop — Not a Vina Class

Slug: `08-docking-guided-design`  
Generator: `cursor-skill`  
Target: 3–5 min Discovery (xAI TTS + Imagine + ffmpeg slideshow)

## Status

| Step | Status |
|------|--------|
| Text pack | Done |
| Chapter + SVG cards | Done (`assets/`) |
| xAI stills | Run `images_xai.py 08-docking-guided-design` |
| xAI TTS EN/ZH | Run `tts_xai.py 08-docking-guided-design --lang both` |
| Slideshow draft | Run `render_slideshow.py 08-docking-guided-design` → `youtube/renders/08-docking-guided-design/draft.mp4` |

```bash
python scripts/youtube/images_xai.py 08-docking-guided-design
python scripts/youtube/tts_xai.py 08-docking-guided-design --lang both
python scripts/youtube/render_slideshow.py 08-docking-guided-design
```

Audio/renders are gitignored. Optional: later insert live screencast in CapCut / 剪映 using `broll-checklist.md`.

## Slideshow map

| Id | Time | Image |
|----|------|-------|
| hook | 0–12s | `assets/ai/hook.png` |
| loop | 12–55s | `assets/pipeline.png` |
| oracle | 55–100s | `assets/ai/mental-model.png` |
| proof | 100–155s | `assets/docking-score-dist.png` |
| mols | 155–175s | `assets/top-docked-molecules.png` |
| poses | 175–215s | `assets/metrics-callout.png` |
| cta | 215–240s | `assets/ai/cta.png` |

## YouTube Studio

### Title

REINVENT4 Tutorial 08: Docking in the Loop — Not a Vina Class

### Description

Paste English or 中文 block from `youtube-description.md`.

### Chapters

```
0:00 QED is not a pose
0:12 The design loop
0:55 Debug the oracle first
1:40 Pool scores and honest RL
2:55 When docking misleads
3:35 Site and GitHub
```

### Tags

```
REINVENT4, drug discovery, generative chemistry, AI drug design, cheminformatics, molecular generation, open science, AstraZeneca REINVENT, tutorial, machine learning, molecular docking, AutoDock Vina, structure-based design
```

## After upload

Do **not** embed the YouTube iframe in MkDocs until a real URL exists.
Do **not** commit `youtube/audio/` or `youtube/renders/`.
