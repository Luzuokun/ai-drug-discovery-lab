# Chemistry station

**Job:** de novo generation, transfer learning, descriptors, and filters — on human-written presets.

| | |
|-|-|
| **tool_ids** | `run_reinvent`, `smiles_prep`, `analyze_molecules` |
| **Gate** | `--approve-run` (and related preset gates) |
| **Spine** | [REINVENT4 12-chapter research practice course](../molecular-generation/reinvent4/index.md) |
| **Not** | LLM-written `reinvent.toml`; DrugEx / MolGPT / GraphGA as product columns |

## Course path

```text
01 Install → 03 Score → 04 RL → 05 Diversity → 07 TL → 08 Docking oracle → 11 BRAF
```

Full syllabus: [REINVENT4](../molecular-generation/reinvent4/index.md).

## Agent contract

- Planner selects **preset IDs** only; humans author TOML offline.
- SA / PAINS and descriptor filters run as deterministic analysis.
- Other generator names (DrugEx, MolGPT, …) are [appendix / textbook-only](../appendix/index.md) until wired.

[:octicons-arrow-right-24: Open REINVENT4 course](../molecular-generation/reinvent4/index.md){ .md-button .md-button--primary }
[:octicons-mark-github-16: reinvent-agent](https://github.com/Luzuokun/reinvent-agent){ .md-button }
