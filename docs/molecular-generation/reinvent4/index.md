# REINVENT4

!!! abstract "Research practice course — not an API tour"
    This series teaches a **reproducible REINVENT4 campaign**: sample → score →
    optimize → control failure modes → adapt data/oracles → scale → prove on a
    real target. Official docs remain the parameter reference; this lab answers
    *what to run, why, and how to judge the result*.

**Principle:** Every tutorial is reproducible (fixed seed, reported resources,
downloadable artifacts).

| # | Chapter | Role in the campaign | Status |
|---|---------|----------------------|--------|
| 01 | [Installation & First Molecule](01-installation-first-molecule.md) | Get a working env and a real `sampled.csv` | Available |
| 02 | [Priors in Practice](02-priors-in-practice.md) | Choose and validate a generative prior for your chemotype | Available |
| 03 | [Scoring Function](03-scoring-function.md) | Debug the reward *before* spending RL steps | Available |
| 04 | [Reinforcement Learning](04-reinforcement-learning.md) | Train an agent so high scores become more probable | Available |
| 05 | [Diversity Filter](05-diversity-filter.md) | Stop scaffold collapse once RL starts working | Available |
| 06 | [Curriculum Learning](06-curriculum-learning.md) | Escalate objectives across stages / checkpoints | Coming Soon |
| 07 | [Transfer Learning](07-transfer-learning.md) | Adapt the prior to project-specific chemistry | Coming Soon |
| 08 | [Docking-Guided Design](08-docking-guided-design.md) | Put a structure-based oracle into the generation loop | Coming Soon |
| 09 | [Scaling & Monitoring](09-scaling-and-monitoring.md) | GPU runs, logs, and TensorBoard for long campaigns | Coming Soon |
| 10 | [Ablations & Hyperparameters](10-ablations-and-hyperparameters.md) | One-variable experiments with your own tables | Coming Soon |
| 11 | [Case Study: BRAF](11-case-study-braf.md) | End-to-end campaign on a published-style target | Coming Soon |
| 12 | [Troubleshooting Appendix](12-troubleshooting-appendix.md) | Cross-cutting errors, demoted edge topics, FAQ | Coming Soon |

## Reading path

```text
01 Install → 02 Prior (optional deep dive) → 03 Score → 04 RL
    → 05 Diversity → 06 Curriculum → 07 Transfer Learning
    → 08 Docking oracle → 09 Scale/monitor → 10 Ablate → 11 BRAF case
```

Skip **02** if Tutorial 01 already gave you a prior you trust; return to it when
you need to *choose* among priors or diagnose domain shift.

## What we deliberately do *not* teach as standalone chapters

Topics that belong in official `PARAMS.md` / site-wide sections, or as short
notes in [Tutorial 12](12-troubleshooting-appendix.md):

- Custom vocabulary, parallel sampling flags, RDKit-as-a-product tour
- Logging or TensorBoard alone (folded into Scaling & Monitoring)
- Duplicate FAQ / Common Errors pages (each hands-on chapter already has errors)

## Further reading

- [REINVENT4 repository](https://github.com/MolecularAI/REINVENT4) — source and configs
- [CONTRIBUTING](https://github.com/Luzuokun/ai-drug-discovery-lab/blob/main/CONTRIBUTING.md) — research practice, not API docs
