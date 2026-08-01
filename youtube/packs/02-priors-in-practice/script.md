# REINVENT4 Tutorial 02 — Your Prior Is an Experiment — Prove It

Target: ~8:00

## [0:00–0:15 Hook]
Tutorial 01 gave you reinvent_pubchem.prior. Downloading it was not a research decision. This episode is.

## [0:15–1:15 Will it cover your chemistry?]
Official docs list prior filenames. Lab work asks: will this generative starting point cover the chemistry you care about? If your project is sulfonamide-rich — or macrocycles, peptides, covalent warheads — and the prior almost never emits that motif, RL burns its first hours rediscovering it. Or never finds it.

## [1:15–2:20 Fair A/B]
Many Zenodo files are different generators (Mol2Mol, LibInvent) — different tasks. Keep the Reinvent generator fixed; change only weights. Compare reinvent_pubchem.prior vs tl_sulfonamide.model (8 TL epochs on sulfonamides).

## [2:20–3:50 Identical protocol]
CPU. Seed 42. ~200 SMILES. unique_molecules on. TOMLs differ only in model_file / output_file. Demo TL: ~13 s, ~871 MiB peak. After uniqueness: 191 vs 196 rows — expected.

## [3:50–5:30 The numbers]
SMARTS S(=O)(=O)N. Sulfonamide %: 8.4% → 64.3%. Murcko scaffolds: 168 vs 172. Mean QED 0.59 → 0.65 (side effect). Short TL enriched the motif without scaffold collapse in this seed-42 draw.

## [5:30–6:45 Decision table]
Prior OK → Tutorial 03. TL helps → use checkpoint for RL. Need linkers/R-groups/seed analogues → wrong generator. Peptides/exotics → check tokens / Pepinvent.

## [6:45–8:00 CTA]
Compare → measure → decide → then RL. Full tutorial on the site. Code on GitHub.
