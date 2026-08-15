# REINVENT4 Tutorial 08: Docking in the Loop — Not a Vina Class

## [0:00–0:12] Hook

A high QED molecule can sit nowhere near the pocket. This episode puts a structure-based oracle into the generation loop — not a Vina command-line class.

## [0:12–0:55] Design loop

Pocket prep, then a scoring component, then a short generation, then pose sanity checks. DockStream is marked superseded. We use AutoDock Vina through REINVENT ExternalProcess so you can see every byte on the wire. Ligands via meeko. Receptor via Open Babel. Public pocket: PDB 1IEP, Abl plus imatinib.

## [0:55–1:40] Debug the oracle

Same discipline as Tutorial 03: run_type scoring before RL. Geometric mean of QED weight 0.3 and Vina weight 1. Reverse sigmoid maps about minus 5 to minus 12 kilocalories into zero to one. Exhaustiveness 1 is a smoke test. Production uses higher exhaustiveness, diversity filters, and queues.

## [1:40–2:55] Proof

Seed 42 prior pool: 37 unique SMILES. Vina raw from minus 12.1 to minus 4.6. About 199 seconds. Imatinib in the same box at exhaustiveness 1 is about minus 9.4. The best raw dock can have low QED — geometric mean is allowed to disagree. Short RL, five steps times batch 8, about 123 seconds, is noisy on purpose. It proves the loop runs. It does not prove a hit series.

## [2:55–3:35] When docking lies

Wrong box, low exhaustiveness, bad tautomer, wrong protein chain — affinities look great and poses are nonsense. Always open top PDBQTs on the receptor. Scoring 0.0 often means embed or Vina failed. Keep QED or alerts so you do not invent greasy bricks.

## [3:35–4:00] CTA

Pocket files, the ExternalProcess script, and CSVs are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 09 — scale and monitor expensive oracles.
