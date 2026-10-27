# Dynamics station

**Job:** short MD and protocol packs that validate poses — separate from generation.

| | |
|-|-|
| **tool_ids** | `md`, `md_carb` |
| **Engine in main path** | GROMACS |
| **Appendix** | [Amber](../molecular-dynamics/amber.md) (empty product column removed from main nav) |
| **Not** | LLM-edited full `.mdp`; 2 ns sold as free-energy proof |

## What you approve

- Production length / free-energy protocol (separate from short demo MD)
- New mdp scalar whitelist entries
- Carbohydrate MD protocol packs (`md_carb`)

## Pages

- [GROMACS](../molecular-dynamics/gromacs.md) — protein–ligand short MD
- Agent: [reinvent-agent](https://github.com/Luzuokun/reinvent-agent) `tools.md` / `tools.md.carb`

Long MD and MM-PBSA stay Phase H — independent tool, separate approval.
