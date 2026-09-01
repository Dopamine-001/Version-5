"""Dark molecular theme for Protein Explorer."""

import streamlit as st


CUSTOM_CSS = """
<style>

/* =========================================================
   GLOBAL MOLECULAR BACKGROUND
   ========================================================= */

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(126, 231, 216, 0.055), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(100, 150, 255, 0.045), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(126, 231, 216, 0.035), transparent 30%),
        #050505 !important;

    color: #f5f5f5;
    min-height: 100vh;
}


/* Subtle molecular/grid texture */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background-image:
        linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);

    background-size: 42px 42px;
    mask-image: linear-gradient(to bottom, black, transparent 85%);
}


/* Keep Streamlit content above background */

.stApp > * {
    position: relative;
    z-index: 1;
}


/* =========================================================
   MAIN CONTENT
   ========================================================= */

.block-container {
    max-width: 1500px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 20% 10%, rgba(126,231,216,0.04), transparent 30%),
        #070707 !important;

    border-right: 1px solid #242424;
}

[data-testid="stSidebar"] * {
    color: #f5f5f5;
}


/* =========================================================
   GENERAL TEXT
   ========================================================= */

h1, h2, h3, h4, h5, h6 {
    color: #f5f5f5 !important;
}

p, label {
    color: #d0d0d0;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    position: relative;

    padding: 2.4rem 2.5rem 2rem;
    margin: 0 0 1.5rem;

    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(126, 231, 216, 0.08),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            rgba(255,255,255,0.025),
            rgba(255,255,255,0.005)
        );

    border: 1px solid #242424;
    border-radius: 20px;

    overflow: hidden;
}


/* Molecular accent line */

.hero::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;

    width: 100%;
    height: 2px;

    background: linear-gradient(
        90deg,
        transparent,
        #7ee7d8,
        transparent
    );

    opacity: 0.8;
}


/* Decorative molecular nodes */

.hero::after {
    content: "◦   ·   ◦      ·      ◦";
    position: absolute;

    right: 2rem;
    top: 1.2rem;

    color: rgba(126,231,216,0.18);
    font-size: 2rem;
    letter-spacing: 0.7rem;

    pointer-events: none;
}


/* Hero kicker */

.kicker {
    color: #7ee7d8 !important;

    font-family: monospace;
    font-size: 0.72rem;
    font-weight: 700;

    letter-spacing: 0.14em;
    text-transform: uppercase;

    margin-bottom: 0.5rem;
}


/* Hero title */

.hero-title {
    display: block;

    color: #ffffff !important;

    font-size: clamp(2.2rem, 5vw, 3.7rem);
    font-weight: 750;

    line-height: 1.05;

    margin: 0.3rem 0 0.7rem;

    letter-spacing: -0.035em;
}


/* Hero description */

.hero-copy {
    display: block;

    color: #999999 !important;

    font-size: 0.98rem;
    line-height: 1.6;

    margin-top: 0.3rem;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

.metric-card {
    position: relative;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.035),
            rgba(255,255,255,0.008)
        ),
        #0b0b0b;

    border: 1px solid #242424;
    border-radius: 14px;

    padding: 1.1rem;

    min-height: 92px;

    transition:
        border-color 0.2s ease,
        transform 0.2s ease;
}

.metric-card:hover {
    border-color: rgba(126,231,216,0.45);
    transform: translateY(-2px);
}

.metric-label {
    color: #888888 !important;

    font-family: monospace;
    font-size: 0.65rem;

    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.metric-value {
    color: #ffffff !important;

    font-size: 1.35rem;
    font-weight: 700;

    margin-top: 0.25rem;
}

.metric-sub {
    color: #7ee7d8 !important;

    font-size: 0.72rem;
    margin-top: 0.25rem;
}


/* =========================================================
   SOURCE BADGES
   ========================================================= */

.source-badge {
    display: inline-block;

    padding: 0.3rem 0.65rem;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;

    border: 1px solid #292929;
    border-radius: 999px;

    background: #0b0b0b;

    color: #8d8d8d !important;

    font-family: monospace;
    font-size: 0.65rem;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    margin: 1.25rem 0 0.65rem;

    color: #ffffff !important;

    font-size: 1.15rem;
    font-weight: 700;
}


/* =========================================================
   CONTAINERS / CARDS
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.025),
            rgba(255,255,255,0.005)
        ),
        #0b0b0b !important;

    border: 1px solid #242424 !important;
    border-radius: 14px;
}


/* =========================================================
   INPUTS
   ========================================================= */

.stTextInput input,
.stTextArea textarea {
    background: #0d0d0d !important;

    color: #ffffff !important;

    border: 1px solid #292929 !important;
    border-radius: 9px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #666666 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #7ee7d8 !important;
    box-shadow: 0 0 0 1px rgba(126,231,216,0.15) !important;
}


/* =========================================================
   SELECT BOXES
   ========================================================= */

.stSelectbox div[data-baseweb="select"] > div {
    background: #0d0d0d !important;

    border: 1px solid #292929 !important;

    color: #ffffff !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    background:
        linear-gradient(
            145deg,
            #151515,
            #0d0d0d
        ) !important;

    color: #ffffff !important;

    border: 1px solid #303030 !important;
    border-radius: 9px !important;

    font-weight: 600;

    transition:
        border-color 0.2s ease,
        color 0.2s ease,
        transform 0.2s ease;
}

.stButton > button:hover {
    border-color: #7ee7d8 !important;
    color: #7ee7d8 !important;

    transform: translateY(-1px);
}


/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;

    border-bottom: 1px solid #242424;
}

.stTabs [data-baseweb="tab"] {
    color: #777777 !important;

    font-size: 0.85rem;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: #7ee7d8 !important;
    font-weight: 700;
}


/* =========================================================
   DATAFRAMES
   ========================================================= */

[data-testid="stDataFrame"] {
    border: 1px solid #242424;
    border-radius: 10px;
    overflow: hidden;
}


/* =========================================================
   LINKS
   ========================================================= */

a {
    color: #7ee7d8 !important;
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {
    border-color: #242424 !important;
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #050505;
}

::-webkit-scrollbar-thumb {
    background: #292929;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #3a3a3a;
}

</style>
"""


def inject_css() -> None:
    st.markdown(
        CUSTOM_CSS,
        unsafe_allow_html=True,
    )
