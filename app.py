"""
Protein Explorer
A professional Streamlit application for protein study and exploration.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Force the repository root into sys.path so submodules can find top-level packages
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from config import APP_NAME
from core.ui_theme import load_aesthetic_theme
from core.database import init_db, log_search 
from styles import inject_css
from views.landing import render_landing
from views.sidebar import render_sidebar

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_aesthetic_theme()
inject_css()
render_sidebar()
render_landing()
