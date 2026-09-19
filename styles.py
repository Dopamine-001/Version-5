"""
Vibrant Biological Theme for Protein Explorer.
Features an SVG nucleotide/DNA pattern, fluid gradients, and organic glassmorphism.
"""

import streamlit as st

VIBRANT_BIO_CSS = """
<style>
/* =========================================================
   1. FONTS & VIBRANT DESIGN TOKENS
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --text-main: #0f172a;
    --text-muted: #334155;
    --text-light: #64748b;
    
    --bio-cyan: #06b6d4;
    --bio-blue: #0ea5e9;
    --bio-emerald: #10b981;
    
    --card-bg: rgba(255, 255, 255, 0.75);
    --card-border: rgba(255, 255, 255, 0.6);
    --card-shadow: 0 8px 32px rgba(15, 23, 42, 0.08);
}

/* =========================================================
   2. FLUID NUCLEOTIDE CANVAS
   ========================================================= */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main) !important;
    
    /* Vibrant fluid gradient + repeating DNA/Nucleotide SVG pattern */
    background-color: #f0f9ff !important;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(6, 182, 212, 0.12), transparent 50%),
        radial-gradient(circle at 85% 20%, rgba(16, 185, 129, 0.12), transparent 50%),
        url("data:image/svg+xml,%3Csvg width='120' height='120' xmlns='http://www.w3.org/2000/svg'%3E%3Cg opacity='0.06'%3E%3Cpath d='M10,60 Q30,20 60,60 T110,60' fill='none' stroke='%230ea5e9' stroke-width='3' stroke-linecap='round'/%3E%3Cpath d='M10,60 Q30,100 60,60 T110,60' fill='none' stroke='%2310b981' stroke-width='3' stroke-linecap='round'/%3E%3Cline x1='35' y1='40' x2='35' y2='80' stroke='%2306b6d4' stroke-width='2'/%3E%3Cline x1='85' y1='40' x2='85' y2='80' stroke='%23059669' stroke-width='2'/%3E%3Ccircle cx='35' cy='40' r='3' fill='%230ea5e9'/%3E%3Ccircle cx='35' cy='80' r='3' fill='%2310b981'/%3E%3Ccircle cx='85' cy='40' r='3' fill='%230ea5e9'/%3E%3Ccircle cx='85' cy='80' r='3' fill='%2310b981'/%3E%3C/g%3E%3C/svg%3E") !important;
    background-size: 100% 100%, 100% 100%, 120px 120px !important;
    background-attachment: fixed !important;
}

#MainMenu, header, footer {
    visibility: hidden;
    display: none;
}

.block-container {
    max-width: 1400px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* =========================================================
   3. OVERRIDING THE SCI-FI TYPOGRAPHY
   ========================================================= */
h1, h2, h3, h4, h5, h6, .hero-title, .section-title {
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    color: var(--text-main) !important;
}

p, label, span, .hero-copy {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-muted);
}

code, pre, .mono-text, .bio-badge {
    font-family: 'JetBrains Mono', monospace !important;
}

/* =========================================================
   4. VIBRANT HERO CARD
   ========================================================= */
.hero {
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    box-shadow: var(--card-shadow);
    position: relative;
    overflow: hidden;
}

/* Vibrant colored top edge for the hero */
.hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--bio-cyan), var(--bio-emerald));
}

.kicker {
    color: var(--bio-cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.hero-title {
    font-size: clamp(2rem, 4vw, 3.2rem) !important;
    line-height: 1.1;
    margin: 0.2rem 0 0.8rem;
    background: linear-gradient(90deg, #0f172a, #334155);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* =========================================================
   5. REPLACING THE BLACK METRIC CARDS
   ========================================================= */
[data-testid="stMetric"] {
    background: var(--card-bg) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid var(--card-border) !important;
    border-left: 4px solid var(--bio-blue) !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.5rem !important;
    box-shadow: var(--card-shadow) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(6, 182, 212, 0.15) !important;
    border-left-color: var(--bio-emerald) !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-light) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: var(--bio-blue) !important;
    letter-spacing: -0.05em !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--bio-emerald) !important;
}

/* =========================================================
   6. VIBRANT BADGES & STATUS PILLS
   ========================================================= */
.bio-badge {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 99px;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
    background: rgba(6, 182, 212, 0.1);
    color: var(--bio-cyan);
    border: 1px solid rgba(6, 182, 212, 0.2);
    box-shadow: 0 2px 8px rgba(6, 182, 212, 0.05);
}

/* =========================================================
   7. INPUTS & VIBRANT BUTTONS
   ========================================================= */
.stTextInput input, .stTextArea textarea {
    background: rgba(255, 255, 255, 0.9) !important;
    color: var(--text-main) !important;
    border: 1px solid rgba(15, 23, 42, 0.1) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
}

.stTextInput input:focus {
    border-color: var(--bio-cyan) !important;
    box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--bio-cyan), var(--bio-blue)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(14, 165, 233, 0.4) !important;
    background: linear-gradient(135deg, var(--bio-blue), var(--bio-emerald)) !important;
}

/* =========================================================
   8. CLEAN DATAFRAMES
   ========================================================= */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(15, 23, 42, 0.1) !important;
    border-radius: 12px !important;
    background: var(--card-bg);
    box-shadow: var(--card-shadow);
}

/* =========================================================
   9. MOBILE RESPONSIVE
   ========================================================= */
@media screen and (max-width: 768px) {
    .block-container {
        padding: 1rem 0.75rem !important;
    }
    .hero-title {
        font-size: 1.6rem !important;
    }
    .hero {
        padding: 1.5rem !important;
    }
    .stButton > button {
        width: 100% !important;
    }
}
</style>
"""

def inject_css() -> None:
    st.markdown(VIBRANT_BIO_CSS, unsafe_allow_html=True)
