from __future__ import annotations

import sys
from pathlib import Path

# Add root directory to path so top-level folders are discoverable as packages
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import streamlit.components.v1 as components

from core.alphafold import calculate_plddt, get_alphafold_structure
from core.uniprot import normalize_uniprot_record, search_uniprot
from analysis.sequence_analysis import sequence_properties
from viewer.py3d_viewer import render_structure
