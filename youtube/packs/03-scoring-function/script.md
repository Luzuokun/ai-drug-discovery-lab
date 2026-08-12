# REINVENT4 Tutorial 03 — Debug the Reward Before You Burn RL

Target: ~6:30

## [0:00–0:15 Hook]
Tutorial 01 gave you molecules. Tutorial 04 will train an agent. Skip this chapter and you may spend GPU hours optimizing a broken reward.

## [0:15–0:55 Sampling vs worth making]
Sampling asks: give me drug-like molecules. Discovery asks: which are worth making? Scoring turns objectives into one number in [0,1] for RL.

## [0:55–2:00 Mental model]
Components → transforms → aggregation → filters. CustomAlerts zeros globally. Geometric mean is harsh on weak objectives; arithmetic mean forgives.

## [2:00–2:45 Score before RL]
run_type=scoring needs no prior. RL calls the scorer thousands of times — debug once on a fixed list first.

## [2:45–4:05 Protocol]
96 molecules. geometric_mean. QED + MW double_sigmoid 200–500. CustomAlerts. ~2 s CPU. scoring.csv.

## [4:05–5:20 Numbers]
Mean 0.66, max 0.97, 44 above 0.8, one alert zero, MW=151 collapses via transform.

## [5:20–6:30 CTA]
Site + GitHub. Next: Tutorial 04 RL.
