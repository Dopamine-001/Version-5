"""
Vibrant Biological & Chemical Theme for Protein Explorer.
Overrides custom HTML classes to force clean, readable, scientific UI.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
/* =========================================================
   1. FONTS & THEME TOKENS
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg-color: #f4f7f9;
    --card-bg: #ffffff;
    --text-main: #0f172a;
    --text-muted: #475569;
    --accent-teal: #0d9488;
    --accent-emerald: #059669;
    --accent-blue: #0284c7;
    --border-color: #cbd5e1;
}

/* =========================================================
   2. CHEMICAL RING LATTICE BACKGROUND
   ========================================================= */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: var(--bg-color) !important;
    
    /* Authentic, subtle hexagonal chemical ring pattern */
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(13, 148, 136, 0.05), transparent 60%),
        radial-gradient(circle at 85% 20%, rgba(5, 150, 105, 0.05), transparent 60%),
        url("data:image/svg+xml,%3Csvg width='60' height='103.923' viewBox='0 0 60 103.923' xmlns='http://www.w3.org/2000/svg'%3E%3Cg stroke='%2394a3b8' stroke-width='1' stroke-opacity='0.25' fill='none'%3E%3Cpath d='M30 17.32L60 0v34.64L30 51.96 0 34.64V0l30 17.32zM30 69.28L60 51.96v34.64L30 103.92 0 86.6V51.96l30 17.32z'/%3E%3C/g%3E%3C/svg%3E") !important;
    background-size: 100% 100%, 100% 100%, 60px 104px !important;
    background-attachment: fixed !important;
    
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main) !important;
}

#MainMenu, header, footer { visibility: hidden; display: none; }

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* =========================================================
   3. FORCE CLEAN SCIENTIFIC TYPOGRAPHY (KILL THE SCI-FI FONT)
   ========================================================= */
* {
    font-family: 'Inter', sans-serif;
}
code, pre, .mono-text {
    font-family: 'Fira Code', monospace !important;
}

/* =========================================================
   4. HERO BANNER (FORCE LIGHT THEME)
   ========================================================= */
.hero {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 2.5rem 3rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
    position: relative;
}

/* Top vibrant biological accent line */
.hero::before {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 5px;
    background: linear-gradient(90deg, var(--accent-teal), var(--accent-emerald)) !important;
    opacity: 1 !important;
}

/* Remove decorative text dots from original code */
.hero::after { display: none !important; }

.kicker {
    color: var(--accent-teal) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

.hero-title {
    color: var(--text-main) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: clamp(2rem, 4vw, 2.8rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    text-transform: none !important;
    margin: 0.5rem 0 1rem !important;
}

.hero-copy {
    color: var(--text-muted) !important;
    font-size: 1rem !important;
}

/* =========================================================
   5. METRIC CARDS (FORCE WHITE CARDS, REMOVE DARK BLOCKS)
   ========================================================= */
.metric-card {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-left: 4px solid var(--accent-teal) !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
    padding: 1.25rem 1.5rem !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    min-height: auto !important;
}

.metric-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.15) !important;
    border-left-color: var(--accent-emerald) !important;
}

.metric-label {
    color: var(--text-muted) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

.metric-value {
    color: var(--text-main) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    margin-top: 0.4rem !important;
}

.metric-sub {
    color: var(--accent-blue) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    margin-top: 0.4rem !important;
}

/* =========================================================
   6. UI CONTROLS & BADGES
   ========================================================= */
.source-badge {
    background: rgba(13, 148, 136, 0.1) !important;
    color: var(--accent-teal) !important;
    border: 1px solid rgba(13, 148, 136, 0.2) !important;
    font-family: 'Fira Code', monospace !important;
    font-weight: 500 !important;
    padding: 0.3rem 0.7rem !important;
}

.section-title {
    color: var(--text-main) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 0.5rem;
}

.stButton > button {
    background: var(--card-bg) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border-color) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}

.stButton > button:hover {
    border-color: var(--accent-teal) !important;
    color: var(--accent-teal) !important;
}

/* =========================================================
   7. DATAFRAMES & CONTAINERS
   ========================================================= */
[data-testid="stDataFrame"], div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}
</style>
"""

def inject_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
