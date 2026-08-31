"""
Sequence-level analysis: ProtParam biochemical properties, amino-acid
composition, and the per-residue Kyte-Doolittle hydrophobicity table that
both the single-protein and comparison views chart from.
"""

from __future__ import annotations

from collections import Counter

import pandas as pd
import streamlit as st
from Bio.SeqUtils.ProtParam import ProteinAnalysis

from config import AMINO_ACIDS, KYTEL_DOOLITTLE


@st.cache_data(show_spinner=False)
def sequence_properties(sequence: str) -> dict:
    if not sequence:
        return {}
    analysis = ProteinAnalysis(sequence)
    return {
        "molecular_weight": analysis.molecular_weight(),
        "pI": analysis.isoelectric_point(),
        "gravy": analysis.gravy(),
        "aromaticity": analysis.aromaticity(),
        "instability": analysis.instability_index(),
        "flexibility": analysis.flexibility(),
        "charge": analysis.charge_at_pH(7.0),
    }


def amino_acid_composition(sequence: str) -> pd.DataFrame:
    counts = Counter(sequence)
    rows = []
    for aa in AMINO_ACIDS:
        n = counts.get(aa, 0)
        rows.append({
            "Amino acid": aa,
            "Count": n,
            "Percentage": round(n / len(sequence) * 100, 2) if sequence else 0,
        })
    return pd.DataFrame(rows)


def hydrophobicity_table(sequence: str) -> pd.DataFrame:
    values = [KYTEL_DOOLITTLE.get(aa, 0) for aa in sequence]
    return pd.DataFrame({
        "Position": range(1, len(sequence) + 1),
        "Residue": list(sequence),
        "Kyte-Doolittle": values,
    })
