# PRODUCE — REINVENT4 Tutorial 02: Your Prior Is an Experiment — Prove It

Slug: `02-priors-in-practice`  
Text pack generator: `cursor-skill`  
Status: **human-approved checklist** — next: TTS → screencast → edit → upload  
Ready media: [`assets/ASSETS.md`](assets/ASSETS.md)  
`.env`: `ELEVENLABS_API_KEY` detected (value not logged)

## 0. Preconditions

- [x] `PRODUCE.md` reviewed by human (this run)
- [x] `ELEVENLABS_API_KEY` present in repo-root `.env`
- [ ] `REVIEW.md` checklist items / `verify_flags` accepted (or waived)
- [ ] Voice language track(s) chosen: EN / ZH / both

## 1. ElevenLabs (TTS) — Skill B does not auto-run

**Inputs:** `voiceover-en.txt` (~2301 chars), `voiceover-zh.txt`

Suggested settings:

| Track | File | Style notes |
|-------|------|-------------|
| EN | voiceover-en.txt | Clear science explainer; moderate pace; pause on blank lines |
| ZH | voiceover-zh.txt | Same beat timing intent as EN; multilingual model |

Dry-run (verified this session — no API call):

```bash
python scripts/youtube/tts_elevenlabs.py 02 --lang both --dry-run
# → youtube/audio/02-priors-in-practice/en.mp3
# → youtube/audio/02-priors-in-practice/zh.mp3
```

When you want audio generated (charges ElevenLabs quota), run locally or ask the agent explicitly to **run TTS**:

```bash
pip install -r requirements-youtube.txt
python scripts/youtube/tts_elevenlabs.py 02 --lang en
python scripts/youtube/tts_elevenlabs.py 02 --lang zh
# or: --lang both
```

Optional voice overrides in `.env`: `ELEVENLABS_VOICE_ID_EN`, `ELEVENLABS_VOICE_ID_ZH`, `ELEVENLABS_MODEL_ID`.

Output: `youtube/audio/02-priors-in-practice/` (gitignored).

## 2. Screencast / B-roll order

Follow `broll-checklist.md` and `storyboard.md`. Recommended record / import order:

1. **Hook cutaway** — `assets/01-first-molecules.png` (optional live `ls priors/…`)
2. **Problem title** — on-screen “Cover YOUR chemistry?”
3. **Fair A/B** — `assets/metrics-callout.svg`
4. **TL screencast** — `assets/tl_sulfonamide.toml.txt` + live `reinvent -s 42` if available
5. **Config diff** — `assets/sample_prior.toml.txt` vs `assets/sample_tl.toml.txt`
6. **Numbers** — `assets/prior-vs-tl-compare.png`, punch-in `assets/metrics-callout.svg`
7. **Molecules** — `assets/prior-sample-molecules.png` → `assets/tl-sample-molecules.png`
8. **Decision** — `assets/decision-table.svg`
9. **CTA card** — Site → GitHub (Tutorial 02/12)
10. **Optional** — `assets/compare-*-sample.csv` in editor

## 3. Edit timeline summary

| Timecode | Picture | Audio beat |
|----------|---------|------------|
| 0:00–0:15 | Title + `01-first-molecules.png` / prior filename | Hook — download ≠ decision |
| 0:15–1:15 | Quote / chemotype card | Will it cover your chemistry? |
| 1:15–2:20 | `metrics-callout.svg` | Fair A/B — same generator |
| 2:20–3:50 | Screencast TOMLs + terminal | Identical sampling protocol |
| 3:50–5:30 | `prior-vs-tl-compare.png` + molecule grids | The numbers that decide |
| 5:30–6:45 | `decision-table.svg` | Decision table |
| 6:45–8:00 | CTA slate | Site & GitHub |

Align cuts to `chapters.txt`. Soft-load or burn `subtitles-en.srt` / `subtitles-zh.srt`.

## 4. YouTube Studio paste blocks

### Title

REINVENT4 Tutorial 02: Your Prior Is an Experiment — Prove It

(Thumbnail overlay: **8% → 64% Sulfonamides**)

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

Generate from `thumbnail-prompt.md`; keep **8% → 64% Sulfonamides** readable on mobile. Optional base: `assets/metrics-callout.svg`.

## 5. After upload

1. Copy the public video URL.
2. Optionally add to playlist (`TODO_PLAYLIST_URL` → real URL).
3. Only then consider linking from the MkDocs chapter (explicit approval required).
4. Do **not** commit large media under `youtube/audio/` or `youtube/renders/`.

## Next manual actions (order)

1. ~~Review PRODUCE.md~~ (done)
2. **Run TTS** (say「运行 TTS」to the agent, or run `tts_elevenlabs.py` locally) — EN and/or ZH
3. Record remaining live terminal clips; import `assets/*`
4. Edit to the timeline above + subtitles
5. Upload with paste blocks → share URL for optional MkDocs link
