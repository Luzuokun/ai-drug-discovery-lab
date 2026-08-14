# REINVENT4 Tutorial 06: Escalate Objectives — Don't Front-Load Hardness

## [0:00–0:12] Hook

Do not demand LogP on day one. Curriculum learning in REINVENT4 is multi-stage RL with different scoring setups — not a separate algorithm.

## [0:12–0:55] Problem

A single hard reward from step one is noisy. Medicinal chemistry stabilizes a series, then tightens ADMET. Stage 1 uses the Tutorial 04 stack: QED, molecular weight, alerts. Stage 2 adds SlogP with a reverse sigmoid. Auto curriculum is multiple stage blocks in one TOML. Manual curriculum hands a checkpoint to a new file.

## [0:55–1:40] The trap

If a stage ends because max_steps was reached, REINVENT terminates all remaining stages. Auto curriculum only advances when max_score fires after min_steps. Treat stage-one max_steps as a safety ceiling, not the plan.

## [1:40–2:55] Proof

Seed 42 auto run. Stage 1 early-stops at step 12, mean Score 0.74, above max_score 0.72. Stage 2 runs 20 steps. Score drops to 0.46 on the harder reward, then climbs to 0.59. About 29 seconds, peak RAM about 1.5 gibibytes. That cliff at the boundary is evidence the objective changed — not a crash.

## [2:55–3:35] Manual CL

Manual curriculum: agent_file is the stage-one checkpoint, prior_file stays the original prior. Use auto when stage 1 will early-stop. Use manual when you need to inspect CSV, retune transforms, or continue tomorrow.

## [3:35–4:00] CTA

Configs and stage CSVs are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 07 — adapt the prior with transfer learning before a long RL campaign.
