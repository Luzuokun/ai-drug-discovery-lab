# REINVENT4 Tutorial 01: Your First AI Molecules in 4 Minutes

## [0:00–0:12] Hook

You do not have a generative model until you have a real sampled.csv. This episode installs REINVENT4 and proves it with molecules — on CPU, seed 42.

## [0:12–0:50] Problem

pip install reinvent will not work. REINVENT4 is cloned and installed with install.py so PyTorch matches CPU or CUDA. Python must be 3.11 or newer. The prior is not a filename trophy. It is the trained distribution that emits SMILES.

## [0:50–1:35] Mental model

Three words. Prior: the frozen chemical brain from Zenodo — here reinvent_pubchem.prior. Agent: a trainable copy you will later fine-tune with reinforcement learning. Vocabulary: the SMILES tokens stored inside the prior file. Sampling asks the prior for molecules. It does not score them yet.

## [1:35–2:50] Proof

Config: run_type sampling, device cpu, num_smiles 100, unique_molecules true, seed 42. The handbook run finished in about 3.5 seconds and peaked near 550 mebibytes. One hundred requested. Four invalid strings dropped. Ninety-six unique valid molecules written. Columns: SMILES, SMILES_state, NLL. NLL min 21.37, mean 36.44, max 76.98. Lower NLL means the model was more confident. There is no Score column — sampling has no reward.

## [2:50–3:35] Failure modes

unique_molecules true is a request, not a guarantee — duplicates and invalids vanish after generation. High NLL is unusual chemistry, not a crash. If you ever see Score all zeros, that is a scoring bug in a later run_type, not a failed sample. Wrong prior file or a truncated Zenodo download is a FileNotFound or load error — check the path.

## [3:35–4:00] CTA

Full install commands, the sampling TOML, and sampled.csv live on the AI Drug Discovery Lab site. Code is on GitHub. Next: Tutorial 02 if you must choose a prior — or Tutorial 03 to attach a reward. Links in the description.
