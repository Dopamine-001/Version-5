"""
Sequence-identity scoring for the protein-vs-protein comparison feature.
"""

from __future__ import annotations

import streamlit as st
from Bio import Align


@st.cache_data(show_spinner=False)
def align_sequences(seq1: str, seq2: str) -> dict:
    """Global pairwise alignment (Biopython) to quantify sequence similarity."""
    aligner = Align.PairwiseAligner()
    aligner.mode = "global"
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -0.5
    try:
        aligner.substitution_matrix = Align.substitution_matrices.load("BLOSUM62")
    except Exception:
        aligner.match_score = 1
        aligner.mismatch_score = -1

    alignment = aligner.align(seq1, seq2)[0]
    a1, a2 = str(alignment[0]), str(alignment[1])
    matches = sum(1 for x, y in zip(a1, a2) if x == y and x != "-")
    aligned_columns = len(a1)
    identity = round(matches / aligned_columns * 100, 1) if aligned_columns else 0.0
    return {
        "identity": identity,
        "aligned_length": aligned_columns,
        "matches": matches,
        "score": alignment.score,
    }
