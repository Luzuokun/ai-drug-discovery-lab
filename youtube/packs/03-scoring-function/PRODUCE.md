# PRODUCE — REINVENT4 Tutorial 03: Debug the Reward Before You Burn RL

Slug: `03-scoring-function`  
Generator: `cursor-skill`  
Target: ~6:30 (5–8 min Discovery)  

## Status (this Cloud run)

| Step | Status |
|------|--------|
| Text pack | Done |
| Chapter + SVG assets | Done (`assets/`) |
| OpenAI AI stills | **Blocked** — `OPENAI_API_KEY` returned `credit_balance_exhausted` |
| ElevenLabs EN TTS | **Blocked** — key looks like an API *key ID*, not a secret starting with `sk_` |
| Slideshow draft MP4 | Done with **silent audio + burned EN subs** (watchable structure) |

### Local artifacts (gitignored)

- `youtube/renders/03-scoring-function/draft.mp4` (~5 MB, 390 s, hard subs)
- `youtube/audio/03-scoring-function/en.mp3` — currently **silence placeholder** (390 s)

### Fix keys, then regenerate (minimal work)

```bash
# .env — use a real ElevenLabs secret (sk_...) and fund OpenAI credits
# OPENAI_API_KEY=sk-...
# ELEVENLABS_API_KEY=sk_...

pip install -r requirements-youtube.txt
python scripts/youtube/images_openai.py 03
python scripts/youtube/tts_elevenlabs.py 03 --lang en
python scripts/youtube/render_slideshow.py 03
```

Then replace the silent draft with a voiced one.

## 0. Preconditions

- [x] Text pack written
- [ ] OpenAI credits available → AI stills
- [ ] Valid ElevenLabs `sk_` key → EN voiceover
- [ ] Preview `draft.mp4`

## 1. Your remaining work (short)

1. Fix `.env` keys / billing as above and re-run the three commands.
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

Prefer `assets/ai/thumbnail.png` after OpenAI generation; until then use `assets/metrics-callout.png` + title **Debug the Reward First**.
