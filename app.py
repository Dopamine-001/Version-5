"""
TATVA (तत्त्व)
A professional Streamlit application for biomolecular study and protein exploration.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Force the repository root into sys.path so submodules can find top-level packages
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

import plot_theme as pt
from config import APP_NAME
from core.database import init_db, log_search  
from styles import inject_css
from views.landing import render_landing
from views.sidebar import render_sidebar

st.set_page_config(
    page_title="तत्त्व | Biomolecular Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize the SQLite database table on app startup
init_db()

# Inject design system CSS so background margins and typography take priority
inject_css()

# If you capture search queries in session state or user input, log them here:
if "protein_query" in st.session_state and st.session_state["protein_query"]:
    log_search(st.session_state["protein_query"])

render_sidebar()
render_landing()
