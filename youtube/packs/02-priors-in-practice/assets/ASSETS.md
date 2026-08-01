# Tutorial 02 pack assets (ready for edit)

Self-contained copies / graphics for the YouTube cut. Canonical handbook copies remain under `docs/assets/reinvent4/02/`.

| File | Role in video |
|------|----------------|
| `01-first-molecules.png` | Hook bridge from Tutorial 01 |
| `prior-vs-tl-compare.png` | Core comparison figure (histograms + metrics) |
| `prior-sample-molecules.png` | PubChem prior molecule grid |
| `tl-sample-molecules.png` | TL checkpoint molecule grid |
| `metrics-callout.svg` | Clean 8.4% → 64.3% title card overlay |
| `decision-table.svg` | Stay / TL / switch-generator decision graphic |
| `compare-prior-sample.csv` | Spreadsheet / terminal B-roll |
| `compare-tl-sample.csv` | Spreadsheet / terminal B-roll |
| `sulfonamide_tl_train.smi` | TL data prep shot (145 molecules) |
| `sulfonamide_tl_val.smi` | TL validation hold-outs |
| `sample_prior.toml.txt` | Config text for side-by-side screencast |
| `sample_tl.toml.txt` | Config text (only model/output differ) |
| `tl_sulfonamide.toml.txt` | Short TL config for screencast |

## Still record locally (not in repo)

- Live terminal: `reinvent --version`, TL run (~13 s), dual sampling
- Thumbnail render from `../thumbnail-prompt.md`
- TTS audio → `youtube/audio/02-priors-in-practice/` (gitignored)
