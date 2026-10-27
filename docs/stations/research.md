# Research station

**Job:** bring cited literature and public data into a campaign — with provenance, not vibes.

| | |
|-|-|
| **tool_id** | `literature` |
| **Gate** | `--approve-literature` |
| **Output** | `<project>/output/literature/` |
| **Not** | planner/MCP write-paper steps; invented PMIDs |

## What you do

1. Write a PubMed query yourself.
2. Approve the literature pull once.
3. Keep only entries with URL and/or PMID (or DOI).
4. Hand Critic evidence JSON that already carries citations — Critic may not invent more.

## Handbook links

- Campaign reading: [Campaigns](../campaigns/index.md)
- Agent mapping: `python -m tools.handbook_map` in [reinvent-agent](https://github.com/Luzuokun/reinvent-agent)

!!! note "Assay / ChEMBL"
    Predefined ChEMBL download + `smiles_prep` is a planned Assay station (Phase D on the company roadmap). Until then, keep assay CSVs human-curated.
