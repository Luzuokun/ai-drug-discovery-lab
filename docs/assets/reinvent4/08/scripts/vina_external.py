#!/usr/bin/env python3
"""ExternalProcess scorer: AutoDock Vina docking for REINVENT4.

Reads SMILES on stdin (one per line). Writes JSON:
  {"version": 1, "payload": {"vina_score": [...], "vina_ok": [...]}}

vina_score is the best affinity in kcal/mol (more negative = better).
Failed ligands get 0.0 (neutral after reverse_sigmoid — treat as non-binders).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation, PDBQTWriterLegacy

# Script may live next to pocket/ or under scripts/ beside ../pocket/
_HERE = Path(__file__).resolve().parent
POCKET = _HERE / "pocket" if (_HERE / "pocket").is_dir() else _HERE.parent / "pocket"
RECEPTOR = POCKET / "receptor.pdbqt"
BOX = POCKET / "box.txt"

# Demo defaults: fast enough for short RL on CPU.
EXHAUSTIVENESS = int(os.environ.get("VINA_EXHAUSTIVENESS", "1"))
CPU = int(os.environ.get("VINA_CPU", "1"))
SEED = int(os.environ.get("VINA_SEED", "42"))
TIMEOUT = int(os.environ.get("VINA_TIMEOUT", "60"))


def load_box():
    cx, cy, cz, sx, sy, sz = map(float, BOX.read_text().split())
    return cx, cy, cz, sx, sy, sz


def smiles_to_pdbqt(smiles: str) -> str | None:
    mol = Chem.MolFromSmiles(smiles.strip())
    if mol is None:
        return None
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = SEED
    if AllChem.EmbedMolecule(mol, params) != 0:
        return None
    try:
        AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
    except Exception:
        pass
    prep = MoleculePreparation()
    setups = prep.prepare(mol)
    if not setups:
        return None
    pdbqt_string, is_ok, _ = PDBQTWriterLegacy.write_string(setups[0])
    if not is_ok:
        return None
    return pdbqt_string


def dock_pdbqt(pdbqt: str, box) -> float | None:
    cx, cy, cz, sx, sy, sz = box
    with tempfile.TemporaryDirectory() as td:
        lig = Path(td) / "lig.pdbqt"
        out = Path(td) / "out.pdbqt"
        lig.write_text(pdbqt)
        cmd = [
            "vina",
            "--receptor",
            str(RECEPTOR),
            "--ligand",
            str(lig),
            "--center_x",
            str(cx),
            "--center_y",
            str(cy),
            "--center_z",
            str(cz),
            "--size_x",
            str(sx),
            "--size_y",
            str(sy),
            "--size_z",
            str(sz),
            "--exhaustiveness",
            str(EXHAUSTIVENESS),
            "--cpu",
            str(CPU),
            "--num_modes",
            "1",
            "--seed",
            str(SEED),
            "--out",
            str(out),
        ]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TIMEOUT,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return None
        if proc.returncode != 0 or not out.exists():
            return None
        # Parse best affinity from stdout table or REMARK in out
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0] == "1":
                try:
                    return float(parts[1])
                except ValueError:
                    pass
        for line in out.read_text().splitlines():
            if "VINA RESULT:" in line or "REMARK VINA RESULT:" in line:
                try:
                    return float(line.split()[3])
                except (IndexError, ValueError):
                    return None
        return None


def main():
    smilies = [line.strip() for line in sys.stdin if line.strip()]
    box = load_box()
    scores = []
    oks = []
    for smi in smilies:
        pdbqt = smiles_to_pdbqt(smi)
        if pdbqt is None:
            scores.append(0.0)
            oks.append(0)
            continue
        aff = dock_pdbqt(pdbqt, box)
        if aff is None:
            scores.append(0.0)
            oks.append(0)
        else:
            scores.append(float(aff))
            oks.append(1)
    print(json.dumps({"version": 1, "payload": {"vina_score": scores, "vina_ok": oks}}))


if __name__ == "__main__":
    main()
