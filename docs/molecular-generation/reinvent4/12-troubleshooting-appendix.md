# REINVENT4 Tutorial 12: Troubleshooting Appendix

!!! abstract "Chapter 12 of the REINVENT4 course"
    Hands-on chapters already carry **Common Errors** next to the command that
    fails. This appendix is the **index**: where that error was measured, a
    handful of *new* cross-cutting cases, and the edge topics we refused to
    turn into extra chapters (custom vocabulary, parallel sampling, RDKit as a
    product tour). Official PARAMS / SCORING stay the parameter reference;
    each link below has a one-line “use this when.”

## Learning Objectives

After completing this chapter, you will be able to:

- [ ] Jump from a traceback to the tutorial that already reproduces it.
- [ ] Distinguish **config-schema** failures from **science** failures
      (flat Score, scaffold collapse, analog-remote Tanimoto).
- [ ] Decide when to open official PARAMS.md / SCORING.md versus re-running a
      handbook protocol.
- [ ] Apply short notes on custom vocabulary, `scoring.parallel`, and RDKit
      without a separate mini-course.

## Why It Matters

Search traffic wants “CUDA out of memory” and “FileNotFoundError prior.” A
second copy of those answers as a standalone FAQ page drifts out of date the
moment Tutorial 04 changes a TOML key. One appendix that **points at** the
measured chapters stays honest: the fix lives next to the seed, the log, and
the artifact.

## Hands-on Practice

There is no new overnight job. Keep a failing log from Tutorials 01–11 and
walk the index. If your error is not here, add it to the chapter where you
hit it — not as a fourth FAQ page.

### Diagnostic path

```text
Does reinvent --version run?
  no  → env / install (Tutorial 01): scipy, RDKit, CUDA wheel vs device
  yes → Is the traceback ValidationError / Extra inputs?
          yes → schema: [stage.scoring], unique_sequences, sample_batch_size
          no  → FileNotFoundError → prior / SMILES / checkpoint paths (01, 04)
              → CUDA / device → 01, 04, 09
              → Job runs, chemistry looks wrong → 03 (score), 04/10 (RL),
                05 (DF), 06 (curriculum abort), 07 (overfit TL), 08 (poses),
                11 (oracle vs claim)
```

### Error index (already taught)

| Symptom | Go to | What that chapter measured |
|---------|-------|----------------------------|
| `No module named 'scipy'` | [01](01-installation-first-molecule.md) | Missing optional dep in the active env |
| RDKit `ImportError` | [01](01-installation-first-molecule.md), [03](03-scoring-function.md) | Wrong env; reinstall via `install.py` |
| `FileNotFoundError` prior / SMILES / chkpt | [01](01-installation-first-molecule.md), [03](03-scoring-function.md), [04](04-reinforcement-learning.md) | Path relative to **cwd**, not to the TOML |
| Vocabulary / token errors on a *standard* prior | [01](01-installation-first-molecule.md) | Truncated Zenodo download; re-fetch |
| `invalid hash` warning on the prior | [02](02-priors-in-practice.md), [07](07-transfer-learning.md) | File mismatch; don't ignore if sampling looks insane |
| `sample_batch_size` validation error | [02](02-priors-in-practice.md), [07](07-transfer-learning.md) | TL requires `sample_batch_size ≥ 100` in 4.8.24 |
| Scores look like raw MW (~300) | [03](03-scoring-function.md) | Missing transform; aggregation saw Daltons |
| Almost every `Score ≈ 0` | [03](03-scoring-function.md), [04](04-reinforcement-learning.md), [05](05-diversity-filter.md) | Alerts, transforms, or DF buckets |
| `ValidationError` Extra inputs / missing stage scoring | [04](04-reinforcement-learning.md), [06](06-curriculum-learning.md), [08](08-docking-guided-design.md) | `[scoring]` vs `[stage.scoring]` |
| RL Score stays flat | [04](04-reinforcement-learning.md), [10](10-ablations-and-hyperparameters.md) | Broken reward or tiny `sigma` |
| `unique_sequences` rejected | [04](04-reinforcement-learning.md) | 4.8.24 RL schema; omit the key |
| DF has no effect | [05](05-diversity-filter.md) | Section nested under `[[stage]]` or global vs per-stage |
| Stage 2 never starts | [06](06-curriculum-learning.md) | `max_steps` abort; need `max_score` after `min_steps` |
| Picked last TL epoch | [07](07-transfer-learning.md) | Val NLL vs mem%; ep 8 won on that set |
| `ExternalProcess` JSON / Vina PDBQT | [08](08-docking-guided-design.md) | Payload keys; Open Babel vs Meeko |
| `Torch not compiled with CUDA enabled` | [09](09-scaling-and-monitoring.md) | CPU wheel + `device = "cuda:0"` |
| Empty TensorBoard | [09](09-scaling-and-monitoring.md) | Events are in `tb_logdir_{run}/` |
| `scoring.parallel` made CPU RL **slower** | [09](09-scaling-and-monitoring.md) | Cheap RDKit; overhead > gain |
| Step-1 Score differs in an ablation | [10](10-ablations-and-hyperparameters.md) | Seed / TOML drift |
| Vemurafenib Score ≠ 1.0 | [11](11-case-study-braf.md) | Geometric mean includes QED/MW |

### New cross-cutting cases

??? failure "`AssertionError: Torch not compiled with CUDA enabled`"
    Measured in Tutorial 09 on `2.12.0+cpu` with `device = "cuda:0"`. This is
    **not** “the GPU is busy.” `torch.cuda.is_available()` is False until you
    reinstall CUDA wheels (`python install.py cu124` or matching tag from
    Tutorial 01). A missing driver (`nvidia-smi` not found) is a second,
    separate problem: even a CUDA wheel cannot help a VM without a device.

??? failure "TensorBoard `--logdir tb_rl` is empty"
    Staged learning writes `f"{tb_logdir}_{run}"` → `tb_rl_0`. Point
    TensorBoard at `tb_rl_0` or at the parent directory. `tb_logdir = ""`
    disables logging.

??? failure "`unique_sequences` in a copied official TOML"
    `configs/staged_learning.toml` in the REINVENT repo may still show
    `unique_sequences = true`. REINVENT **4.8.24** rejects that key on RL
    validation. Delete the line. Sampling still has `unique_molecules`.

??? failure "Two tutorials, two wall-clocks, same Score"
    Tutorial 04 published ~27 s; Tutorial 09 re-measured **61 s** on a
    4-core Xeon for the same seed-42 Score curve. Chemistry is the portable
    artifact. Always publish host + clock + Score.

??? failure "Mixing generator priors in an A/B"
    Tutorial 02: a Mol2Mol `.prior` is not a drop-in control for Reinvent de
    novo. Match **file ↔ task**. Zenodo catalogue:
    [DOI 10.5281/zenodo.15641296](https://doi.org/10.5281/zenodo.15641296).

??? failure "Curriculum silently skipped stage 2"
    Tutorial 06: if stage 1 hits `max_steps` (not `max_score`), later stages
    are aborted. Early-stop must be a score threshold after `min_steps`.

### Short notes (demoted topics)

#### Custom vocabulary

Standard PubChem / ChEMBL priors **bundle** the vocabulary inside the `.prior`
file. You do not pass a separate vocab path for Tutorials 01–11.

A **custom** vocabulary is a research project: tokenize your library, train or
adapt a prior, then never mix that agent with a different vocab at sampling
time. Token errors on a *standard* prior are almost always a truncated
download (Tutorial 01), not an invitation to edit vocab files. If you truly
need a custom alphabet, start from the REINVENT4 source models and treat it as
a methods paper, not a handbook checkbox.

#### Parallel sampling / `scoring.parallel`

There is no extra “parallel sampling” flag on Reinvent RNN `staged_learning`
in this course. Throughput knobs we *did* measure (Tutorial 09):

| Knob | When it helped |
|------|----------------|
| `device = "cuda:0"` | When the wheel and GPU exist (not measured here; CPU wheel failed) |
| `batch_size` | Changes work per step; mol/s was ~flat at 32 vs 64 on this CPU |
| `scoring.parallel` | **Hurt** QED+MW+alerts (31 s → 56 s for 10 steps at 4 processes) |

Use `scoring.parallel > 1` when the **oracle** is slow (Vina, a network QSAR)
and a probe run shows a wall-clock drop. Data-pipeline `num_procs` is a
different `run_type`.

#### RDKit

REINVENT4 already depends on RDKit for scoring, Murcko DF, and Tanimoto.
Handbook recipes for fingerprints, scaffolds, and descriptors live under
[RDKit](../../rdkit/index.md) (Coming Soon pages plus whatever is published).
Do not fork a second RDKit tutorial inside REINVENT4. If an RDKit traceback
appears during a REINVENT job, it is usually an invalid SMILES the sampler
emitted (`SMILES_state`) or a SMARTS you wrote — fix the scoring component
(Tutorial 03) or the prior (Tutorial 02 / 07).

### Official docs — use this when

| Document | Use this when… |
|----------|----------------|
| [PARAMS.md](https://github.com/MolecularAI/REINVENT4/blob/main/configs/PARAMS.md) | You need the factory default or a flag this handbook never ablated (`tb_isim`, inception, transformer `sample_strategy`). |
| [SCORING.md](https://github.com/MolecularAI/REINVENT4/blob/main/configs/SCORING.md) | You need a component's parameter list (Tanimoto radius, ExternalProcess JSON, QSAR). Tutorial 03/08/11 show *which* components to pick for a decision. |
| [staged_learning.toml](https://github.com/MolecularAI/REINVENT4/blob/main/configs/staged_learning.toml) | You want an upstream multi-stage example. Strip keys 4.8.24 rejects (`unique_sequences`) and nest scoring under `[[stage]]`. |
| [REINVENT4 README](https://github.com/MolecularAI/REINVENT4) | Installer tags (`cpu` / `cu124`) and Zenodo prior DOI. |
| This lab, Tutorials 01–11 | You need a **measured** protocol: seed, clock, artifact, *why*, failure mode. |

## Code Walkthrough

No new TOML. The “code” is the map:

| If you are editing… | Primary chapter |
|---------------------|-----------------|
| Env, prior download, first `sampled.csv` | 01 |
| Which `.prior` / short TL taste | 02 |
| Reward geometry, transforms, alerts | 03 |
| DAP RL loop | 04 |
| Scaffold memory | 05 |
| Multi-stage / chkpt hand-off | 06 |
| Overfitting TL → RL | 07 |
| Docking oracle + poses | 08 |
| GPU, TB, throughput | 09 |
| One-variable `sigma` table | 10 |
| Target story + pre-registered criteria | 11 |

## Expected Output

After using this appendix you should have:

- A **chapter link**, not a second conflicting fix.
- A decision: schema bug vs scientific bug.
- If you file a handbook improvement, the Common Error lands **in the tutorial
  that runs the command**, with a one-line pointer added here.

## Think About It

1. **Why keep Common Errors inside each tutorial *and* this index?** The
   tutorial has the log line and the seed; the index has the search terms.
2. **When is “read PARAMS.md” the wrong next step?** When the flag already has
   a measured handbook table (`sigma`, `tb_logdir`, `stage.scoring`). PARAMS
   will not tell you that `sigma = 256` lost to 128 on this prior.
3. **Why was custom vocabulary demoted?** It is a model-training project. A
   13th chapter would read like an API tour and skip the BRAF campaign.
4. **If validity is high and Score is flat, is that an appendix error?** No —
   that is Tutorial 03/04 science (reward not aligned). Appendix errors are
   mostly “the job did not run as configured.”
5. **Should docking failures live here or in the Docking section?** Both: the
   *loop* (ExternalProcess JSON) is Tutorial 08; Vina flags belong to
   [Docking](../../docking/index.md).

## Exercises

1. **Easy:** From a teammate's log, pick three lines and map each to a row in
   the index. If you cannot, the appendix has a gap — open a docs PR on the
   *chapter*, then add a row here.
2. **Medium:** Break a working Tutorial 04 TOML on purpose (`[scoring]` at top
   level, `unique_sequences = true`, `device = "cuda:0"` on a CPU wheel).
   Save the three tracebacks. Match them without scrolling this page first.
3. **Challenge:** Add a Common Error to Tutorial 11 for a failure *you* hit
   that is not listed (for example a malformed vemurafenib SMILES). Link it
   from this index in the same PR.

## Further Reading

- [REINVENT4 `configs/PARAMS.md`](https://github.com/MolecularAI/REINVENT4/blob/main/configs/PARAMS.md) — run-mode flags. Use as the default catalogue.
- [REINVENT4 `configs/SCORING.md`](https://github.com/MolecularAI/REINVENT4/blob/main/configs/SCORING.md) — component catalogue. Use when adding an oracle this lab did not measure.
- Loeffler et al., *REINVENT 4*, **J. Cheminformatics** (2024). [Open Access](https://doi.org/10.1186/s13321-024-00812-5).
- Handbook: course [syllabus](index.md), [CONTRIBUTING](https://github.com/Luzuokun/ai-drug-discovery-lab/blob/main/CONTRIBUTING.md).

---

You now have a 12-chapter, seed-42, artifact-backed REINVENT4 campaign path:
sample → score → optimize → control collapse → curriculum → transfer → dock →
monitor → ablate → BRAF case → this index.
