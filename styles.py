"""
Refined Molecular Dark Theme for Protein Explorer.
Precision typography, clean border hierarchy, and mobile-first responsiveness.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
/* =========================================================
   1. FONTS & ROOT DESIGN TOKENS
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-base: #050505;
    --bg-card: #0b0b0b;
    --bg-input: #0d0d0d;
    --border-subtle: #222222;
    --border-active: #7ee7d8;
    --text-primary: #f5f5f5;
    --text-secondary: #a0a0a0;
    --text-muted: #666666;
    --accent-teal: #7ee7d8;
    --accent-blue: #38bdf8;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* =========================================================
   2. GLOBAL CANVAS & BACKGROUND
   ========================================================= */
html, body, [data-testid="stAppViewContainer"] {
    font-family: var(--font-sans) !important;
    background:
        radial-gradient(circle at 15% 10%, rgba(126, 231, 216, 0.04), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(56, 189, 248, 0.03), transparent 25%),
        var(--bg-base) !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

/* Grid overlay background */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 36px 36px;
    mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
}

.stApp > * {
    position: relative;
    z-index: 1;
}

#MainMenu, header, footer {
    visibility: hidden;
    display: none;
}

.block-container {
    max-width: 1440px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* =========================================================
   3. TYPOGRAPHY & HEADINGS
   ========================================================= */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.025em;
}

p, label, span {
    color: var(--text-secondary);
}

code, pre, .mono-text {
    font-family: var(--font-mono) !important;
}

/* =========================================================
   4. HERO BANNER
   ========================================================= */
.hero {
    position: relative;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.5rem;
    background:
        radial-gradient(circle at 90% 20%, rgba(126, 231, 216, 0.06), transparent 40%),
        linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.003));
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    overflow: hidden;
}

.hero::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-teal), transparent);
}

.kicker {
    color: var(--accent-teal) !important;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.hero-title {
    color: var(--text-primary) !important;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin: 0.2rem 0 0.6rem;
}

.hero-copy {
    color: var(--text-secondary) !important;
    font-size: 0.95rem;
    line-height: 1.6;
    max-width: 800px;
}

/* =========================================================
   5. METRICS & CONTROL CARDS
   ========================================================= */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(126, 231, 216, 0.3) !important;
    transform: translateY(-1px);
}

[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted) !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* =========================================================
   6. INPUTS & TACTILE BUTTONS
   ========================================================= */
.stTextInput input, .stTextArea textarea {
    background: var(--bg-input) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.9rem !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 0 1px rgba(126, 231, 216, 0.2) !important;
}

.stButton > button {
    background: linear-gradient(180deg, #161616 0%, #0d0d0d 100%) !important;
    color: var(--text-primary) !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    font-family: var(--font-sans) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    border-color: var(--accent-teal) !important;
    color: var(--accent-teal) !important;
    transform: translateY(-1px);
}

.stButton > button[kind="primary"] {
    background: var(--accent-teal) !important;
    color: #050505 !important;
    border: none !important;
}

.stButton > button[kind="primary"]:hover {
    background: #62d4c3 !important;
    color: #050505 !important;
}

/* =========================================================
   7. SIDEBAR & NAVIGATION
   ========================================================= */
[data-testid="stSidebar"] {
    background: var(--bg-base) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

/* =========================================================
   8. MOBILE RESPONSIVE
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
        margin-bottom: 0.75rem;
    }

    .hero-title {
        font-size: 1.8rem !important;
    }

    .stButton > button {
        width: 100% !important;
    }
}
</style>
"""

def inject_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
