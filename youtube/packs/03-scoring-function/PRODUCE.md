# PRODUCE — REINVENT4 Tutorial 03: Debug the Reward Before You Burn RL

Slug: `03-scoring-function`  
Generator: `cursor-skill`  
Target: ~6:30 (5–8 min Discovery)  

## Status

| Step | Status |
|------|--------|
| Text pack | Done |
| Chapter + SVG assets | Done (`assets/`) |
| xAI AI stills | Prefer `images_xai.py` (`XAI_API_KEY`) |
| xAI EN TTS | Prefer `tts_xai.py` (`XAI_API_KEY`) |
| Slideshow draft MP4 | `render_slideshow.py` → `youtube/renders/…/draft.mp4` |

### Regenerate (xAI)

```bash
# .env — see .env.example
# XAI_API_KEY=...
# XAI_TTS_VOICE_ID=eve
# XAI_IMAGE_MODEL=grok-imagine-image-quality

python scripts/youtube/images_xai.py 03
python scripts/youtube/tts_xai.py 03 --lang en
python scripts/youtube/render_slideshow.py 03
```

## 0. Preconditions

- [x] Text pack written
- [ ] xAI stills under `assets/ai/`
- [ ] EN voiceover `youtube/audio/03-scoring-function/en.mp3`
- [ ] Preview `draft.mp4`

## 1. Your remaining work (short)

1. Run the three commands above (or ask the agent to run them).
2. Optional: in CapCut, replace the 2:45–4:05 segment with a live `scoring.toml` screencast.
3. Upload to YouTube using paste blocks below.
4. Do **not** commit `youtube/audio/` or `youtube/renders/`.

## 2. Slideshow map (`slideshow.json`)

| Time | Visual |
|------|--------|
| 0:00–0:15 | AI hook (fallback: pipeline) |
| 0:15–0:55 | `pipeline.png` |
| 0:55–2:00 | AI mental-model (fallback: metrics) |
| 2:00–2:45 | AI score-before-rl |
| 2:45–4:05 | `metrics-callout.png` |
| 4:05–4:45 | `score-distribution.png` |
| 4:45–5:20 | `top-scored-molecules.png` |
| 5:20–6:30 | AI CTA |

## 3. YouTube Studio paste blocks

### Title

REINVENT4 Tutorial 03: Debug the Reward Before You Burn RL

### Description (English)

```
REINVENT4 Tutorial 03 — Scoring Function

Sampling gives you molecules. Reinforcement learning optimizes a reward. This episode is the missing step: debug the scoring function on a fixed list before you burn RL compute. We score 96 molecules from Tutorial 01 with QED + molecular weight (double sigmoid 200–500 Da) + CustomAlerts — geometric mean, ~2 seconds on CPU — and read scoring.csv like an experimentalist.

🔗 Full tutorial (site)
https://luzuokun.github.io/ai-drug-discovery-lab/molecular-generation/reinvent4/03-scoring-function/
中文: https://luzuokun.github.io/ai-drug-discovery-lab/zh/molecular-generation/reinvent4/03-scoring-function/

💻 GitHub
https://github.com/Luzuokun/ai-drug-discovery-lab/blob/main/docs/molecular-generation/reinvent4/03-scoring-function.md

📺 Series playlist
TODO_PLAYLIST_URL

Chapters:
0:00 Hook — debug the reward first
0:15 Worth making?
0:55 Components, transforms, filters
2:00 Score before RL
2:45 The function we ran
4:05 How to read the scores
5:20 CTA — site, GitHub, Tutorial 04

#REINVENT4 #DrugDiscovery #QED #GenerativeAI #Cheminformatics
```

### Chapters

```
0:00 Hook — debug the reward first
0:15 Worth making?
0:55 Components, transforms, filters
2:00 Score before RL
2:45 The function we ran
4:05 How to read the scores
5:20 CTA — site, GitHub, Tutorial 04
```

### Tags

```
REINVENT4, scoring function, QED, AI drug discovery, molecular generation, reinforcement learning, cheminformatics, drug-likeness, CustomAlerts, geometric mean, AI Drug Discovery Lab, 分子生成, 评分函数, 药物发现
```

### Thumbnail

Prefer `assets/ai/thumbnail.png` after xAI generation; until then use `assets/metrics-callout.png` + title **Debug the Reward First**.
