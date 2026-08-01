# PRODUCE — REINVENT4 Tutorial 02: Your Prior Is an Experiment — Prove It

Slug: `02-priors-in-practice`  
Text pack generator: `cursor-skill`  
Status: awaiting TTS / screencast / edit / upload  
Ready media: [`assets/ASSETS.md`](assets/ASSETS.md)

## 0. Preconditions

- [ ] `REVIEW.md` approved (or explicitly waived)
- [ ] `verify_flags` resolved or accepted
- [ ] Voice language track(s): EN / ZH / both
- [ ] Repo-root `.env` has `ELEVENLABS_API_KEY` (copy from `.env.example`; never commit `.env`)

## 1. ElevenLabs (TTS) — do not auto-run in Skill B

**Inputs:** `voiceover-en.txt`, `voiceover-zh.txt`

Suggested settings (adjust to your voice library):

| Track | File | Style notes |
|-------|------|-------------|
| EN | voiceover-en.txt | Clear science explainer; moderate pace; pause on blank lines |
| ZH | voiceover-zh.txt | Same beat timing intent as EN; prefer multilingual voice |

Local commands:

```bash
# Key in repo-root .env (gitignored):
#   ELEVENLABS_API_KEY=...
# Optional:
#   ELEVENLABS_VOICE_ID_EN=...
#   ELEVENLABS_VOICE_ID_ZH=...
#   ELEVENLABS_MODEL_ID=eleven_multilingual_v2

pip install -r requirements-youtube.txt
python scripts/youtube/tts_elevenlabs.py 02 --lang both --dry-run
python scripts/youtube/tts_elevenlabs.py 02 --lang en
python scripts/youtube/tts_elevenlabs.py 02 --lang zh
```

Output target: `youtube/audio/02-priors-in-practice/en.mp3` and/or `zh.mp3` (gitignored).

## 2. Screencast / B-roll order

Follow `broll-checklist.md` and `storyboard.md`. Recommended record / import order:

1. **Hook cutaway** — `assets/01-first-molecules.png` (optional live `ls priors/…`)
2. **Problem title** — on-screen text “Cover YOUR chemistry?” (simple card OK)
3. **Fair A/B diagram** — `assets/metrics-callout.svg` (or animate prior → TL)
4. **TL screencast** — open `assets/tl_sulfonamide.toml.txt`; live `reinvent -s 42` if available
5. **Config diff** — side-by-side `assets/sample_prior.toml.txt` vs `assets/sample_tl.toml.txt`
6. **Numbers** — full bleed `assets/prior-vs-tl-compare.png`, then punch-in `assets/metrics-callout.svg`
7. **Molecules** — hard cut `assets/prior-sample-molecules.png` → `assets/tl-sample-molecules.png`
8. **Decision** — `assets/decision-table.svg`
9. **CTA card** — Site → GitHub (Tutorial 02/12)
10. **Optional** — flash `assets/compare-*-sample.csv` in an editor

## 3. Edit timeline summary

| Timecode | Picture | Audio beat |
|----------|---------|------------|
| 0:00–0:15 | Title + `01-first-molecules.png` / prior filename | Hook — download ≠ decision |
| 0:15–1:15 | Quote / chemotype card | Will it cover your chemistry? |
| 1:15–2:20 | `metrics-callout.svg` (left panel focus) | Fair A/B — same generator |
| 2:20–3:50 | Screencast TOMLs + terminal | Identical sampling protocol |
| 3:50–5:30 | `prior-vs-tl-compare.png` + molecule grids | The numbers that decide |
| 5:30–6:45 | `decision-table.svg` | Decision table |
| 6:45–8:00 | CTA slate | Site & GitHub |

Align picture cuts to `chapters.txt`. Burn or soft-load `subtitles-en.srt` / `subtitles-zh.srt`.

## 4. YouTube Studio paste blocks

### Title

REINVENT4 Tutorial 02: Your Prior Is an Experiment — Prove It

(Thumbnail title overlay: **8% → 64% Sulfonamides**)

### Description (English)

```
REINVENT4 Tutorial 02 — Priors in Practice

Downloading reinvent_pubchem.prior is not a research decision. This episode runs a fair A/B: same Reinvent generator, PubChem prior vs a short sulfonamide transfer-learning checkpoint (seed 42, CPU). Chemotype hit rate jumps from 8.4% to 64.3% while Murcko scaffolds stay high — then we use a decision table before RL.

🔗 Full tutorial (site)
https://luzuokun.github.io/ai-drug-discovery-lab/molecular-generation/reinvent4/02-priors-in-practice/
中文: https://luzuokun.github.io/ai-drug-discovery-lab/zh/molecular-generation/reinvent4/02-priors-in-practice/

🧪 Tutorial 01 (install + first sample)
https://luzuokun.github.io/ai-drug-discovery-lab/molecular-generation/reinvent4/01-installation-first-molecule/

💻 GitHub
https://github.com/Luzuokun/ai-drug-discovery-lab/blob/main/docs/molecular-generation/reinvent4/02-priors-in-practice.md

📺 Series playlist
TODO_PLAYLIST_URL

Chapters:
0:00 Hook — download ≠ decision
0:15 Will it cover your chemistry?
1:15 Fair A/B — same generator, new weights
2:20 Identical sampling protocol
3:50 The numbers that decide
5:30 Decision table
6:45 CTA — site & GitHub

#REINVENT4 #DrugDiscovery #GenerativeAI #TransferLearning #Cheminformatics
```

### Chapters

```
0:00 Hook — download ≠ decision
0:15 Will it cover your chemistry?
1:15 Fair A/B — same generator, new weights
2:20 Identical sampling protocol
3:50 The numbers that decide
5:30 Decision table
6:45 CTA — site & GitHub
```

### Tags

```
REINVENT4, AI drug discovery, molecular generation, transfer learning, prior model, sulfonamide, cheminformatics, de novo design, generative chemistry, PubChem, drug design, AI Drug Discovery Lab, 分子生成, 迁移学习, 药物发现
```

### Thumbnail

Generate from `thumbnail-prompt.md`; keep title **8% → 64% Sulfonamides** readable on mobile. Optional base art: `assets/metrics-callout.svg` / molecule grids.

## 5. After upload

1. Copy the public video URL.
2. Optionally add to playlist (`TODO_PLAYLIST_URL` → real URL).
3. Only then consider linking from the MkDocs chapter (user approval required).
4. Do **not** commit large media under `youtube/audio/` or `youtube/renders/`.

## Next manual actions (order)

1. Approve `REVIEW.md`
2. Put `ELEVENLABS_API_KEY` in `.env` → run `tts_elevenlabs.py`
3. Record remaining live terminal clips; import `assets/*`
4. Edit to the timeline above + subtitles
5. Upload with paste blocks → share URL back for optional MkDocs link
