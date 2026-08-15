# REINVENT4 Tutorial 07: Stop TL Before It Memorizes

## [0:00–0:12] Hook

Tutorial 02 was eight epochs of transfer learning. This episode asks when to stop — and whether TL actually changes the RL campaign.

## [0:12–0:50] Problem

A tiny sulfonamide set keeps enriching if you train long enough — and then it memorizes. Official docs list flags. Lab work needs a stop rule, an overfitting checklist, and a TL-then-RL versus RL-only A/B under the same scoring function.

## [0:50–2:10] Overfit curve

Same Tutorial 02 SMILES. Forty epochs, checkpoints every eight, CPU, seed 42, about 62 seconds. Epoch 0: 8.4 percent sulfonamide, 168 scaffolds, zero exact train SMILES. Epoch 8: 64.3 percent, still zero memorized — and best validation NLL. Epoch 24: 83 percent hits but 12 percent exact train SMILES. Epoch 40: 86 percent hits, 40 percent memorized, unique rows fall from 191 to 165. Last epoch is not the winner.

## [2:10–3:10] TL then RL

Same QED, molecular weight, alerts as Tutorial 04. Twenty-five steps. RL-only last-five mean Score 0.775 and 4.4 percent sulfonamide. TL-then-RL from the epoch-24 checkpoint: Score 0.847 and 66.6 percent sulfonamide — even though the reward does not pay for the motif. Set both prior_file and agent_file to the TL checkpoint so DAP anchors to the adapted distribution.

## [3:10–3:35] Decision

Keep the checkpoint where validation NLL bottoms and mem percent is still near zero. Need linkers or R-groups? Wrong generator — not more epochs. Curriculum changes the reward schedule. TL changes the starting distribution. They compose.

## [3:35–4:00] CTA

Curves, CSVs, and configs are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 08 — put a docking oracle in the loop.
