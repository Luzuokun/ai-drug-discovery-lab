# REINVENT4 Tutorial 05: High Score Can Still Be Collapse

## [0:00–0:12] Hook

A high Score can be twenty near-copies of benzene. Tutorial 04 made RL work. This episode treats diversity as the experimental control.

## [0:12–0:50] Problem

Without diversity pressure, RL rediscovers the same easy Murcko core with tiny side-chain edits. The CSV looks great. Chemistry gets duplicates. A diversity filter memorizes scaffolds that already scored well and down-weights further hits in that bucket.

## [0:50–1:35] Mental model

We rerun the Tutorial 04 campaign twice. Same seed 42, same 25 steps, same scoring. One arm has no filter. The other adds a global IdenticalMurckoScaffold diversity filter with bucket_size 25 and minscore 0.4. One variable. Other filter types exist — pick one hypothesis per experiment.

## [1:35–2:55] Proof

Mean Score at step 25: 0.79 without the filter, 0.74 with it. Unique Murcko scaffolds: 1165 versus 1238. Count of the top scaffold, benzene: 120 versus 101. Step 1 Scores matched at 0.66. Each leg about 27 to 28 seconds on CPU. You trade a little mean Score for a wider library.

## [2:55–3:35] Decision

If top-scaffold occupancy barely moves, the bucket is too large or minscore never fires. If Score collapses, the filter is starving the agent — loosen bucket_size. Diversity is an experimental knob, not a checkbox you forget after Tutorial 04.

## [3:35–4:00] CTA

A/B CSVs and figures are on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 06 — escalate objectives across stages.
