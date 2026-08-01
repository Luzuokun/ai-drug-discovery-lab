# B-roll checklist

Ready-to-import media lives in [`assets/`](assets/ASSETS.md).

- [ ] **Terminal: reinvent --version and ls priors/reinvent_pubchem.prior**
  - Why: Bridge from Tutorial 01 artifact
  - Source hint: live screencast; cutaway `assets/01-first-molecules.png`

- [ ] **Screencast editing TL config and running reinvent -s 42**
  - Why: Show short TL is cheap on CPU (~13 s / ~871 MiB)
  - Source hint: `assets/tl_sulfonamide.toml.txt` + live run; data files `assets/sulfonamide_tl_*.smi`

- [ ] **Side-by-side sampling configs**
  - Why: Prove only `model_file` / `output_file` change
  - Source hint: `assets/sample_prior.toml.txt` vs `assets/sample_tl.toml.txt`

- [ ] **Show prior-vs-tl-compare + metrics callout**
  - Why: Core visual payoff for 8.4% → 64.3%
  - Source hint: `assets/prior-vs-tl-compare.png`, `assets/metrics-callout.svg`

- [ ] **Cut between prior and TL molecule grids**
  - Why: Viewer sees preferential sulfonamides
  - Source hint: `assets/prior-sample-molecules.png`, `assets/tl-sample-molecules.png`

- [ ] **Decision table graphic**
  - Why: Memorable takeaway before CTA
  - Source hint: `assets/decision-table.svg` (Stay / TL / Switch generator)

- [ ] **Optional: flash CSV samples in editor**
  - Why: Reproducibility beat
  - Source hint: `assets/compare-prior-sample.csv`, `assets/compare-tl-sample.csv`
