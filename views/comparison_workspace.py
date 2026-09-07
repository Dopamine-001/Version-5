from __future__ import annotations

import sys
from pathlib import Path

# Force the parent root directory into sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import streamlit.components.v1 as components

from core.alphafold import calculate_plddt, get_alphafold_structure
from core.uniprot import normalize_uniprot_record, search_uniprot
from viewer.py3d_viewer import render_structure

# Robust import for analysis module with fallback
try:
    from analysis.sequence_analysis import sequence_properties
except ModuleNotFoundError:
    try:
        from sequence_analysis import sequence_properties
    except ImportError:
        # Fallback dummy function if module path is unresolved
        def sequence_properties(seq: str) -> dict:
            return {"molecular_weight": 0.0, "pI": 7.0, "gravy": 0.0}
