"""
Protein Explorer - Molecular Biology theme.

Design intent:
  paper      : pale buffer/agarose green-grey, not white, not cream
  ink        : deep chlorophyll near-black
  green      : structural accent (headings, rules, primary)
  blue       : EXPERIMENTAL / measured values (UniProt, PDB, sequence-derived)
  amber      : PREDICTED / computed values (AlphaFold, ProtParam, models)
  background : tiled B-DNA double helix with base-pair rungs

Colour is semantic here - blue vs amber tells the user whether a number was
measured or predicted. Keep that meaning if you extend this file.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
/* ============================================================
   1. TYPEFACES
   Spectral  - protein names, numerals, section heads (journal feel)
   Inter     - interface text
   IBM Plex Mono - sequences, accessions, anything a machine wrote
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --paper:      #eef2ee;
    --paper-deep: #e3e9e3;
    --card:       #ffffff;
    --ink:        #12241d;
    --ink-soft:   #35503f;
    --muted:      #6b7f74;
    --rule:       #cfd9d1;
    --rule-soft:  #e2e9e3;

    --green:      #2e6f52;   /* primary / structural */
    --green-deep: #1d4c37;
    --blue:       #2b5f86;   /* experimental, measured */
    --amber:      #9a6b1f;   /* predicted, computed */

    --radius:     4px;
}

/* ============================================================
   2. RESET THE OLD THEME
   Kills the neon glow, the blur on the title and any dark block
   left over from the previous stylesheet.
   ============================================================ */
html body .stApp *,
html body [data-testid="stAppViewContainer"] * {
    text-shadow: none !important;
    box-shadow: none !important;
}
html body .hero-title,
html body .metric-value,
html body .section-title,
html body h1, html body h2, html body h3 {
    -webkit-text-fill-color: currentColor !important;
    -webkit-background-clip: border-box !important;
    background-clip: border-box !important;
    filter: none !important;
    opacity: 1 !important;
}
html body .hero::after,
html body .metric-card::after,
html body .hero::before { content: none !important; }

/* ============================================================
   3. PAPER + DNA DOUBLE HELIX BACKGROUND
   Two sugar-phosphate backbones crossing every half turn, with
   base-pair rungs that narrow at each crossing. Low contrast on
   purpose - it should read as watermark, never as pattern noise.
   ============================================================ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
.stApp {
    background-color: var(--paper) !important;
    background-image:
        radial-gradient(ellipse at 12% 0%, rgba(46, 111, 82, 0.07), transparent 55%),
        radial-gradient(ellipse at 88% 30%, rgba(43, 95, 134, 0.06), transparent 55%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='100' viewBox='0 0 120 100'%3E%3Cg fill='none' stroke='%232e6f52' stroke-opacity='0.16' stroke-width='1.6' stroke-linecap='round'%3E%3Cpath d='M30 0C30 12 90 13 90 25C90 37 30 38 30 50C30 62 90 63 90 75C90 87 30 88 30 100'/%3E%3Cpath d='M90 0C90 12 30 13 30 25C30 37 90 38 90 50C90 62 30 63 30 75C30 87 90 88 90 100'/%3E%3C/g%3E%3Cg fill='none' stroke='%232b5f86' stroke-opacity='0.13' stroke-width='1.3' stroke-linecap='round'%3E%3Cpath d='M32 1h56 M38 6h44 M52 11h16 M52 19h16 M38 25h44 M32 25h56 M38 31h44 M52 36h16 M52 44h16 M38 50h44 M32 50h56 M38 56h44 M52 61h16 M52 69h16 M38 75h44 M32 75h56 M38 81h44 M52 86h16 M52 94h16 M32 99h56'/%3E%3C/g%3E%3C/svg%3E") !important;
    background-size: 900px 700px, 900px 700px, 120px 100px !important;
    background-repeat: no-repeat, no-repeat, repeat !important;
    background-attachment: fixed !important;
    color: var(--ink) !important;
}

#MainMenu, footer { visibility: hidden; display: none; }
[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    max-width: 1320px !important;
    padding-top: 2.25rem !important;
    padding-bottom: 5rem !important;
}

/* ============================================================
   4. BASE TYPOGRAPHY
   ============================================================ */
html body, html body .stApp,
html body p, html body li, html body label,
html body [data-testid="stMarkdownContainer"] {
    font-family: 'Inter', system-ui, sans-serif !important;
    color: var(--ink) !important;
    font-size: 0.95rem;
    line-height: 1.6;
}
html body p { max-width: 72ch; color: var(--ink-soft) !important; }

html body h1, html body h2, html body h3, html body h4 {
    font-family: 'Spectral', Georgia, serif !important;
    color: var(--ink) !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    text-transform: none !important;
}

html body code, html body pre, html body .mono-text,
html body [data-testid="stCode"] * {
    font-family: 'IBM Plex Mono', ui-monospace, monospace !important;
    font-size: 0.86em !important;
}
html body code {
    background: var(--paper-deep) !important;
    color: var(--green-deep) !important;
    border: 1px solid var(--rule-soft) !important;
    border-radius: 3px !important;
    padding: 0.08em 0.36em !important;
}

/* ============================================================
   5. HERO - the protein record header
   A quiet paper panel; the protein name is the loudest thing on
   the page and the only place the design raises its voice.
   ============================================================ */
html body .hero {
    position: relative;
    background: var(--card) !important;
    border: 1px solid var(--rule) !important;
    border-left: 5px solid var(--green) !important;
    border-radius: var(--radius) !important;
    padding: 2.25rem 2.5rem 2rem !important;
    margin-bottom: 2.25rem !important;
    overflow: hidden;
}

/* helix watermark inside the record header */
html body .hero {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='100' viewBox='0 0 120 100'%3E%3Cg fill='none' stroke='%232e6f52' stroke-opacity='0.09' stroke-width='1.6'%3E%3Cpath d='M30 0C30 12 90 13 90 25C90 37 30 38 30 50C30 62 90 63 90 75C90 87 30 88 30 100'/%3E%3Cpath d='M90 0C90 12 30 13 30 25C30 37 90 38 90 50C90 62 30 63 30 75C30 87 90 88 90 100'/%3E%3C/g%3E%3C/svg%3E") !important;
    background-repeat: repeat-y !important;
    background-position: right 3rem top !important;
    background-size: 120px 100px !important;
}

html body .kicker {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    color: var(--muted) !important;
    border-bottom: 1px solid var(--rule) !important;
    padding-bottom: 0.4rem !important;
    margin-bottom: 0.9rem !important;
}

html body .hero-title {
    font-family: 'Spectral', Georgia, serif !important;
    font-size: clamp(1.9rem, 3.4vw, 2.7rem) !important;
    font-weight: 600 !important;
    line-height: 1.12 !important;
    letter-spacing: -0.02em !important;
    text-transform: none !important;
    color: var(--ink) !important;
    margin: 0 0 0.7rem !important;
    max-width: 22ch;
}

html body .hero-copy {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    color: var(--muted) !important;
    margin: 0 !important;
}
html body .hero-copy em,
html body .hero-copy i {
    font-family: 'Spectral', Georgia, serif !important;
    font-style: italic;
    color: var(--ink-soft) !important;
}

/* ============================================================
   6. MEASUREMENT STRIP
   One continuous row of readings separated by hairlines, rather
   than six floating cards. Numbers set in the serif so they read
   as data in a paper, not as dashboard tiles.
   ============================================================ */
html body .metric-card {
    background: var(--card) !important;
    border: 1px solid var(--rule) !important;
    border-left: 3px solid var(--rule) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.15rem 1.05rem !important;
    min-height: 100% !important;
    transition: border-left-color 0.18s ease, background 0.18s ease;
}
html body .metric-card:hover {
    transform: none !important;
    border-left-color: var(--green) !important;
    background: #fbfdfb !important;
}

html body .metric-label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    color: var(--muted) !important;
    display: block;
}

html body .metric-value {
    font-family: 'Spectral', Georgia, serif !important;
    font-size: 1.85rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.015em !important;
    line-height: 1.1 !important;
    color: var(--ink) !important;
    margin-top: 0.35rem !important;
    font-variant-numeric: tabular-nums;
}

/* provenance line: blue = measured, amber = predicted */
html body .metric-sub {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 400 !important;
    color: var(--blue) !important;
    margin-top: 0.45rem !important;
}
html body .metric-sub.predicted,
html body .metric-card.predicted .metric-sub { color: var(--amber) !important; }
html body .metric-card.predicted { border-left-color: var(--amber) !important; }

/* ============================================================
   7. SOURCE BADGES + SECTION RULES
   ============================================================ */
html body .source-badge {
    display: inline-block;
    background: transparent !important;
    color: var(--green-deep) !important;
    border: 1px solid var(--rule) !important;
    border-radius: 999px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.74rem !important;
    font-weight: 400 !important;
    padding: 0.28rem 0.75rem !important;
    margin-right: 0.4rem;
    text-decoration: none !important;
}
html body .source-badge:hover {
    border-color: var(--green) !important;
    background: rgba(46, 111, 82, 0.07) !important;
}

html body .section-title {
    font-family: 'Spectral', Georgia, serif !important;
    font-size: 1.22rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    text-transform: none !important;
    color: var(--ink) !important;
    border-bottom: 1px solid var(--rule) !important;
    padding-bottom: 0.5rem !important;
    margin: 2rem 0 1rem !important;
}

/* ============================================================
   8. CONTROLS
   ============================================================ */
html body .stButton > button,
html body .stDownloadButton > button,
html body .stFormSubmitButton > button {
    background: var(--card) !important;
    color: var(--ink) !important;
    border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.87rem !important;
    font-weight: 500 !important;
    padding: 0.42rem 0.95rem !important;
    transition: border-color 0.15s ease, color 0.15s ease;
}
html body .stButton > button:hover,
html body .stDownloadButton > button:hover {
    border-color: var(--green) !important;
    color: var(--green-deep) !important;
}
html body .stButton > button[kind="primary"],
html body .stFormSubmitButton > button {
    background: var(--green) !important;
    border-color: var(--green) !important;
    color: #ffffff !important;
}
html body .stButton > button[kind="primary"]:hover {
    background: var(--green-deep) !important;
    color: #ffffff !important;
}
html body button:focus-visible,
html body a:focus-visible,
html body input:focus-visible {
    outline: 2px solid var(--blue) !important;
    outline-offset: 2px !important;
}

html body [data-baseweb="input"] input,
html body [data-baseweb="select"] > div,
html body textarea {
    background: var(--card) !important;
    border-color: var(--rule) !important;
    border-radius: var(--radius) !important;
    color: var(--ink) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ============================================================
   9. TABS
   ============================================================ */
html body [data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--rule) !important;
    gap: 0.25rem !important;
}
html body [data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.87rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    padding: 0.55rem 0.8rem !important;
}
html body [data-testid="stTabs"] [aria-selected="true"] {
    color: var(--green-deep) !important;
    border-bottom: 2px solid var(--green) !important;
}
html body [data-testid="stTabs"] [data-baseweb="tab-highlight"],
html body [data-testid="stTabs"] [data-baseweb="tab-border"] { background: transparent !important; }

/* ============================================================
   10. EXPANDERS, TABLES, PLOTS, SIDEBAR
   ============================================================ */
html body [data-testid="stExpander"] {
    background: var(--card) !important;
    border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important;
}
html body [data-testid="stExpander"] summary {
    font-family: 'Spectral', Georgia, serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    text-transform: none !important;
    color: var(--ink) !important;
}
html body [data-testid="stExpander"] summary:hover { color: var(--green-deep) !important; }

html body [data-testid="stDataFrame"],
html body div[data-testid="stVerticalBlockBorderWrapper"],
html body [data-testid="stPlotlyChart"],
html body [data-testid="stPyplotChart"] {
    background: var(--card) !important;
    border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important;
    padding: 0.2rem !important;
}
html body [data-testid="stDataFrame"] * {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}

html body [data-testid="stSidebar"] {
    background: var(--paper-deep) !important;
    border-right: 1px solid var(--rule) !important;
}
html body [data-testid="stSidebar"] * { color: var(--ink) !important; }

html body hr { border-color: var(--rule) !important; }
html body a { color: var(--blue) !important; text-decoration-thickness: 1px; }
html body a:hover { color: var(--green-deep) !important; }

/* ============================================================
   11. SEQUENCE VIEWER
   Wrap <span class="mono-text seq"> around raw sequence output.
   ============================================================ */
html body .seq {
    display: block;
    background: var(--card) !important;
    border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.15rem !important;
    line-height: 1.85 !important;
    letter-spacing: 0.08em !important;
    color: var(--ink) !important;
    word-break: break-all;
    font-size: 0.84rem !important;
}
html body .seq .hydrophobic { color: var(--amber) !important; font-weight: 500; }
html body .seq .polar       { color: var(--blue) !important; }
html body .seq .charged     { color: var(--green-deep) !important; font-weight: 500; }

/* ============================================================
   12. RESPONSIVE + REDUCED MOTION
   ============================================================ */
@media (max-width: 820px) {
    html body .hero { padding: 1.5rem 1.35rem !important; background-image: none !important; }
    html body .hero-title { font-size: 1.6rem !important; }
    html body .metric-value { font-size: 1.5rem !important; }
    .block-container { padding-top: 1.25rem !important; }
}
@media (prefers-reduced-motion: reduce) {
    html body * { transition: none !important; animation: none !important; }
}
</style>
"""

def inject_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
