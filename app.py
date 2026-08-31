"""
Protein Explorer
================
A professional Streamlit application for protein study and exploration.

Data sources:
- UniProt REST API: protein identity, sequence, variants, domains, sites, PTMs
- AlphaFold Protein Structure Database: predicted 3D structure and pLDDT

Run locally:
    python -m streamlit run app.py

For Streamlit Community Cloud:

Project layout (see also this folder's README.md):
    config.py            constants (URLs, amino-acid tables)
    styles.py             theme CSS
    core/                 external data access (UniProt, AlphaFold) + shared helpers
    analysis/              pure computation (sequence, variants, structure, comparison)
    charts/                Plotly figure builders
    viewer/                 py3Dmol structure rendering
    views/                 Streamlit page/tab rendering (this is the only layer
                           that should feel "big" — everything below it is
                           small, focused, and independently testable)
"""

from __future__ import annotations

import streamlit as st

from config import APP_NAME
from styles import inject_css
from views.landing import render_landing
from views.sidebar import render_sidebar

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
render_sidebar()
render_landing()
