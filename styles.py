"""
Biological & Life-Sciences Theme for Protein Explorer.
Inspired by modern biotech platforms (Benchling, RCSB PDB, UniProt).
"""

import streamlit as st

BIOLOGICAL_CSS = """
<style>
/* =========================================================
   1. FONTS & ORGANIC DESIGN TOKENS
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-canvas: #f8fafc;
    --bg-surface: #ffffff;
    --bg-sidebar: #f1f5f9;
    --border-light: #e2e8f0;
    --border-strong: #cbd5e1;
    
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #64748b;
    
    /* Biological Accent Colors */
    --bio-green: #15803d;
    --bio-green-light: #f0fdf4;
    --bio-green-border: #bbf7d0;
    
    --bio-teal: #0f766e;
    --bio-teal-light: #ccfbf1;
    
    --bio-amber: #b45309;
    --bio-amber-light: #fef3c7;
    
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* =========================================================
   2. GLOBAL CANVAS RESET (CLEAN LIGHT/SLATE BIOLOGY)
   ========================================================= */
html, body, [data-testid="stAppViewContainer"] {
    font-family: var(--font-sans) !important;
    background-color: var(--bg-canvas) !important;
    color: var(--text-primary) !important;
}

#MainMenu, header, footer {
    visibility: hidden;
    display: none;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.75rem;
    padding-bottom: 3rem;
}

/* =========================================================
   3. TYPOGRAPHY
   ========================================================= */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

p, label, span {
    color: var(--text-secondary);
}

code, pre, .mono-text {
    font-family: var(--font-mono) !important;
}

/* =========================================================
   4. BIOLOGICAL HERO / WORKSPACE HEADER
   ========================================================= */
.hero {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-left: 4px solid var(--bio-green);
    border-radius: 8px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.kicker {
    color: var(--bio-green) !important;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.hero-title {
    color: var(--text-primary) !important;
    font-size: 1.85rem;
    font-weight: 700;
    margin: 0.1rem 0 0.4rem;
}

.hero-copy {
    color: var(--text-secondary) !important;
    font-size: 0.925rem;
    line-height: 1.5;
}

/* =========================================================
   5. METRICS & DATA CARDS
   ========================================================= */
[data-testid="stMetric"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 8px !important;
    padding: 0.85rem 1.1rem !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
}

[data-testid="stMetricLabel"] {
    font-family: var(--font-sans) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted) !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    font-size: 1.35rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* =========================================================
   6. BIOLOGICAL STATUS PILLS & BADGES
   ========================================================= */
.bio-badge {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    font-weight: 500;
    border-radius: 4px;
    margin-right: 0.4rem;
}

.bio-badge-green {
    background-color: var(--bio-green-light);
    color: var(--bio-green);
    border: 1px solid var(--bio-green-border);
}

.bio-badge-teal {
    background-color: var(--bio-teal-light);
    color: var(--bio-teal);
    border: 1px solid #99f6e4;
}

/* =========================================================
   7. INPUT CONTROLS & TACTILE BUTTONS
   ========================================================= */
.stTextInput input, .stTextArea textarea {
    background: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 6px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.9rem !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--bio-green) !important;
    box-shadow: 0 0 0 2px rgba(21, 128, 61, 0.15) !important;
}

.stButton > button {
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 6px !important;
    font-family: var(--font-sans) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 1rem !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    border-color: var(--bio-green) !important;
    color: var(--bio-green) !important;
    background-color: var(--bio-green-light) !important;
}

.stButton > button[kind="primary"] {
    background-color: var(--bio-green) !important;
    color: #ffffff !important;
    border: 1px solid var(--bio-green) !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: #166534 !important;
    color: #ffffff !important;
}

/* =========================================================
   8. SIDEBAR
   ========================================================= */
[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-light) !important;
}

/* =========================================================
   9. DATAFRAMES & TABLES
   ========================================================= */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 6px !important;
}

/* =========================================================
   10. MOBILE RESPONSIVE
   ========================================================= */
@media screen and (max-width: 768px) {
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 1rem !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-size: 1.4rem !important;
    }

    .stButton > button {
        width: 100% !important;
    }
}
</style>
"""

def inject_css() -> None:
    st.markdown(BIOLOGICAL_CSS, unsafe_allow_html=True)
