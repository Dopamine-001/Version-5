"""
Vibrant Molecular Theme for Protein Explorer.
Features a proper nucleotide/carbon ring background and forces clean white data cards.
"""

import streamlit as st

VIBRANT_BIO_CSS = """
<style>
/* =========================================================
   1. FONTS & VIBRANT DESIGN TOKENS
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --text-main: #0f172a !important;
    --text-muted: #475569 !important;
    --text-light: #64748b !important;
    
    --bio-cyan: #0ea5e9 !important;
    --bio-emerald: #10b981 !important;
    
    --card-bg: #ffffff !important;
    --card-border: #e2e8f0 !important;
}

/* =========================================================
   2. MOLECULAR NUCLEOTIDE CANVAS
   ========================================================= */
html, body, [data-testid="stAppViewContainer"], .stApp {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main) !important;
    background-color: #f8fafc !important;
    
    /* Authentic molecular ring lattice representing nucleotide bases */
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(14, 165, 233, 0.08), transparent 50%),
        radial-gradient(circle at 85% 20%, rgba(16, 185, 129, 0.08), transparent 50%),
        url("data:image/svg+xml,%3Csvg width='60' height='103.923' viewBox='0 0 60 103.923' xmlns='http://www.w3.org/2000/svg'%3E%3Cg stroke='%230ea5e9' stroke-width='1.5' stroke-opacity='0.12' fill='none'%3E%3Cpath d='M30 17.32L60 0v34.64L30 51.96 0 34.64V0l30 17.32zM30 69.28L60 51.96v34.64L30 103.92 0 86.6V51.96l30 17.32z'/%3E%3C/g%3E%3C/svg%3E") !important;
    background-size: 100% 100%, 100% 100%, 60px 104px !important;
    background-attachment: fixed !important;
}

#MainMenu, header, footer { visibility: hidden; display: none; }

.block-container {
    max-width: 1400px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* =========================================================
   3. NUKE THE SCI-FI FONT
   ========================================================= */
* {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6, .hero-title, .section-title {
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    color: var(--text-main) !important;
}

p, label, span, .hero-copy {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-muted) !important;
}

/* =========================================================
   4. FORCE WHITE METRIC CARDS (OVERRIDE DARK BLOCKS)
   ========================================================= */
/* Target the outer metric wrapper, the inner container, and Streamlit's block wrapper */
[data-testid="stMetric"], 
[data-testid="metric-container"], 
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--card-bg) !important;
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
}

/* Force left border accent on metrics only */
[data-testid="stMetric"] {
    border-left: 4px solid var(--bio-cyan) !important;
    padding: 1.2rem 1.5rem !important;
}

/* Force metric text to be dark and monospace */
[data-testid="stMetricValue"] {
    color: var(--text-main) !important;
}

[data-testid="stMetricValue"] > div, 
[data-testid="stMetricValue"] * {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--text-main) !important;
    letter-spacing: -0.05em !important;
}

[data-testid="stMetricLabel"] * {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: var(--text-light) !important;
}

/* =========================================================
   5. VIBRANT HERO CARD
   ========================================================= */
.hero {
    background-color: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 16px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--bio-cyan), var(--bio-emerald));
}

/* =========================================================
   6. INPUTS & VIBRANT BUTTONS
   ========================================================= */
.stTextInput input, .stTextArea textarea {
    background-color: #ffffff !important;
    color: var(--text-main) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stTextInput input:focus {
    border-color: var(--bio-cyan) !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--bio-cyan), #0284c7) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25) !important;
}

/* =========================================================
   7. DATAFRAMES & TABLES
   ========================================================= */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background-color: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
}
</style>
"""

def inject_css() -> None:
    st.markdown(VIBRANT_BIO_CSS, unsafe_allow_html=True)
