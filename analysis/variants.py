"""
UniProt feature tables (variants, domains, sites, PTMs) and the manual
"inspect a mutation" tool used in the Mutations tab.
"""

from __future__ import annotations

import re
from typing import Optional

import pandas as pd

from config import AMINO_ACIDS, KYTEL_DOOLITTLE
from core.helpers import feature_description, feature_position


def variants_dataframe(features: list[dict]) -> pd.DataFrame:
    rows = []
    for f in features:
        start, end = feature_position(f)
        desc = feature_description(f)
        original = f.get("original", "")
        variation = f.get("variation", "")
        if isinstance(variation, list):
            variation = ", ".join(str(x) for x in variation)
        rows.append({
            "Position": (start if start == end else f"{start}-{end}") if start is not None else "—",
            "Original": original or "—",
            "Variant": variation or "—",
            "Description": desc or "Not specified",
            "Feature": f.get("type", "VARIANT"),
        })
    return pd.DataFrame(rows)


def feature_dataframe(features: list[dict]) -> pd.DataFrame:
    rows = []
    for f in features:
        start, end = feature_position(f)
        rows.append({
            "Type": f.get("type", "—"),
            "Position": (start if start == end else f"{start}-{end}") if start is not None else "—",
            "Description": feature_description(f) or "Not specified",
        })
    return pd.DataFrame(rows)


def parse_mutation_input(text: str) -> tuple[Optional[int], Optional[str], Optional[str]]:
    """
    Accepts common simple forms such as V6E, Val6Glu, or 6V>E.
    This is an educational locator, not a clinical variant interpreter.
    """
    text = text.strip().upper().replace(" ", "")
    match = re.fullmatch(r"([A-Z])(\d+)([A-Z])", text)
    if match:
        return int(match.group(2)), match.group(1), match.group(3)

    match = re.fullmatch(r"(\d+)([A-Z])>([A-Z])", text)
    if match:
        return int(match.group(1)), match.group(2), match.group(3)

    three = {
        "ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C","GLN":"Q",
        "GLU":"E","GLY":"G","HIS":"H","ILE":"I","LEU":"L","LYS":"K",
        "MET":"M","PHE":"F","PRO":"P","SER":"S","THR":"T","TRP":"W",
        "TYR":"Y","VAL":"V",
    }
    match = re.fullmatch(r"([A-Z]{3})(\d+)([A-Z]{3})", text)
    if match and match.group(1) in three and match.group(3) in three:
        return int(match.group(2)), three[match.group(1)], three[match.group(3)]

    return None, None, None


def mutation_interpretation(sequence: str, position: int, new_residue: str) -> dict:
    if not sequence or position < 1 or position > len(sequence):
        return {"valid": False, "message": "Position is outside the sequence."}

    old = sequence[position - 1]
    new = new_residue.upper()

    if new not in AMINO_ACIDS:
        return {"valid": False, "message": "Use a one-letter amino-acid code."}

    hyd_change = KYTEL_DOOLITTLE[new] - KYTEL_DOOLITTLE[old]
    charge_change = {
        "K": 1, "R": 1, "H": 0.1, "D": -1, "E": -1,
    }.get(new, 0) - {
        "K": 1, "R": 1, "H": 0.1, "D": -1, "E": -1,
    }.get(old, 0)

    return {
        "valid": True,
        "old": old,
        "new": new,
        "hydrophobicity_change": hyd_change,
        "charge_change": charge_change,
        "same": old == new,
    }
