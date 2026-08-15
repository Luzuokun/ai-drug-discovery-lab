# REINVENT4 Tutorial 04: RL Makes High Scores More Probable

## [0:00–0:12] Hook

Scoring ranks a list you already have. Reinforcement learning changes what the generator emits next. That is the jump from Tutorial 03 to 04.

## [0:12–0:48] Problem

Drug discovery needs more molecules like the good ones — not a static spreadsheet. Each RL step samples a batch, scores it, and updates the agent so high-scoring sequences become more probable. The prior stays frozen as a chemical-grammar anchor. That is DAP — Direct Augmented Prior.

## [0:48–1:35] Mental model

run_type is staged_learning even for one stage. prior_file and agent_file start as the same PubChem prior. Scoring must nest under stage.scoring — a bare scoring section fails validation. That is the number-one copy-paste trap from Tutorial 03. Unique_sequences is not accepted in REINVENT 4.8.24 RL schema. DAP sigma 128 and rate 1e-4 are the handbook defaults.

## [1:35–2:55] Proof

Twenty-five steps, batch 64, CPU, seed 42. About 27 seconds, peak RAM about 1.5 gibibytes. Mean Score 0.66 to 0.79. Agent NLL 34.79 to 27.15. Fraction above 0.8 goes 53 percent to 66 percent. Checkpoint rl_agent.chkpt is about 23 megabytes. Demo length is not a production campaign — scale max_steps when the library matters.

## [2:55–3:35] Failure modes

Scores stuck near zero? Debug the reward with run_type scoring on a fixed list first. No diversity filter here on purpose — that is Tutorial 05. To continue later, point agent_file at the checkpoint and keep prior_file as the original prior.

## [3:35–4:00] CTA

Full TOML, CSV, and the Score-versus-step figure are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 05 — stop scaffold collapse once RL starts working.
