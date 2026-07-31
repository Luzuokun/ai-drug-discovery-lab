# REINVENT4 Tutorial 02 — Don't Trust a Prior You Haven't Stress-Tested

Target: ~8:00

## [0:00–0:15 Hook]
You downloaded reinvent_pubchem.prior. Congrats — that is not the same as choosing a prior for your chemotype.

## [0:15–1:10 The hidden assumption]
Tutorial 01 got you a working environment and a real sampled.csv. That prior was trained on a broad chemical distribution — think PubChem-scale grammar. Your project is not PubChem. Kinase hinges, macrocycles, covalent warheads, natural-product-like scaffolds — if your chemotype is rare in the pretraining soup, the model will still smile and emit SMILES. Validity is not relevance.

## [1:10–2:20 Prior vs Agent vs Vocabulary]
Three words every README skips. The prior is the frozen pretrained brain — chemical grammar. The agent starts as a copy you will later train with rewards. The vocabulary is the alphabet inside the prior file. In this chapter we are not training yet. We are asking: which frozen brain should we even start from?

## [2:20–3:50 Fair comparison protocol]
Rule one: same protocol, different brains. Fix the seed, the number of samples n, and the device. Sample from at least two priors — or one public prior versus a transfer-learning checkpoint. If you change seed and model at once, you learned nothing. [VERIFY] Reuse the Tutorial 01 sampling config shape; only swap model_file.

## [3:50–5:20 What to measure]
Measure like an experimentalist: validity %, unique Bemis-Murcko scaffolds (not just unique SMILES), and simple property histograms — MW, logP, HBD/HBA, maybe QED. Look for coverage of your region without scaffold collapse. Pretty molecules from the wrong neighborhood lose later in scoring and RL.

## [5:20–6:30 When NOT to start from PubChem]
Write this down. Domain shift. Rare chemotypes. Libraries far from drug-like averages. Then prefer an in-domain prior or a TL warm start (Tutorial 07). Popularity is not a control experiment.

## [6:30–8:00 CTA]
Compare → measure → decide with evidence → lock the prior before RL burns GPU. Full chapter on the site (Coming Soon hands-on); Tutorial 01 already live; code on GitHub. Link in the description.
