"""
TATVAM (तत्त्वम्) - Molecular Biology Theme.
"""

from __future__ import annotations

import base64
import math

import streamlit as st

PAPER = "#eef2ee"
PAPER_DEEP = "#e3e9e3"
CARD = "#ffffff"
INK = "#12241d"
INK_SOFT = "#35503f"
MUTED = "#6b7f74"
RULE = "#cfd9d1"
RULE_SOFT = "#e2e9e3"
GREEN = "#2e6f52"
GREEN_DEEP = "#1d4c37"
BLUE = "#2b5f86"
AMBER = "#9a6b1f"

_HELIX_W = 220.0        
_HELIX_TURN = 260.0     
_HELIX_AMP = 74.0       
_HELIX_RIBBON = 6.0     
_HELIX_PHASE = 2.30     
_HELIX_BP = 10          


def _helix_svg(alpha: float = 0.55) -> str:
    cx, turn, amp = _HELIX_W / 2, _HELIX_TURN, _HELIX_AMP

    def x_at(y: float, phase: float) -> float:
        return cx + amp * math.sin(2 * math.pi * y / turn + phase)

    def depth(y: float, phase: float) -> float:
        return (math.cos(2 * math.pi * y / turn + phase) + 1) / 2

    def backbone(phase: float, steps: int = 200) -> str:
        near, far = [], []
        for i in range(steps + 1):
            y = turn * i / steps
            x = x_at(y, phase)
            w = _HELIX_RIBBON * (0.45 + 0.55 * depth(y, phase))
            near.append((x - w, y))
            far.append((x + w, y))
        pts = near + far[::-1]
        d = "M%.1f %.1f" % pts[0]
        d += "".join("L%.1f %.1f" % p for p in pts[1:])
        return d + "Z"

    rungs = []
    for i in range(_HELIX_BP):
        y = turn * (i + 0.5) / _HELIX_BP
        xa, xb = sorted((x_at(y, 0.0), x_at(y, _HELIX_PHASE)))
        if xb - xa < 14:
            continue
        mid, gap = (xa + xb) / 2, 5.0
        front = max(depth(y, 0.0), depth(y, _HELIX_PHASE))
        op = (0.10 + 0.16 * front) * alpha
        width = 2.0 + 1.4 * front
        rungs.append(
            "<path d='M%.1f %.1fH%.1f M%.1f %.1fH%.1f' stroke='%s' "
            "stroke-opacity='%.3f' stroke-width='%.1f' stroke-linecap='round'/>"
            % (xa + 2, y, mid - gap / 2, mid + gap / 2, y, xb - 2, BLUE, op, width)
        )
        rungs.append(
            "<path d='M%.1f %.1fh%.1f' stroke='%s' stroke-opacity='%.3f' "
            "stroke-width='1' stroke-dasharray='1.5 2'/>"
            % (mid - gap / 2, y, gap, BLUE, op * 0.8)
        )

    return (
        "<svg xmlns='http://www.w3.org/2000/svg' width='%.0f' height='%.0f' "
        "viewBox='0 0 %.0f %.0f'>%s"
        "<path d='%s' fill='%s' fill-opacity='%.3f'/>"
        "<path d='%s' fill='%s' fill-opacity='%.3f'/></svg>"
        % (
            _HELIX_W, turn, _HELIX_W, turn, "".join(rungs),
            backbone(0.0), GREEN, 0.20 * alpha,
            backbone(_HELIX_PHASE), GREEN, 0.13 * alpha,
        )
    )


def _data_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


_BG_HELIX = _data_uri(_helix_svg(0.55))    
_HERO_HELIX = _data_uri(_helix_svg(0.40))  


def _css() -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+Devanagari:wght@500;600;700&family=Spectral:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {{
    --paper: {PAPER}; --paper-deep: {PAPER_DEEP}; --card: {CARD};
    --ink: {INK}; --ink-soft: {INK_SOFT}; --muted: {MUTED};
    --rule: {RULE}; --rule-soft: {RULE_SOFT};
    --green: {GREEN}; --green-deep: {GREEN_DEEP};
    --blue: {BLUE}; --amber: {AMBER};
    --radius: 4px;
}}

html body .stApp * {{ text-shadow: none !important; box-shadow: none !important; }}
html body .hero-title, html body .metric-value, html body .section-title,
html body h1, html body h2, html body h3 {{
    -webkit-text-fill-color: currentColor !important;
    background-clip: border-box !important;
    -webkit-background-clip: border-box !important;
    filter: none !important; opacity: 1 !important;
}}
html body .hero::before, html body .hero::after,
html body .metric-card::after {{ content: none !important; }}

html, body, [data-testid="stAppViewContainer"], .stApp {{
    background-color: var(--paper) !important;
    background-image:
        radial-gradient(ellipse 900px 600px at 50% -10%, rgba(46,111,82,0.06), transparent 70%),
        url("{_BG_HELIX}"),
        url("{_BG_HELIX}") !important;
    background-repeat: no-repeat, repeat-y, repeat-y !important;
    background-position: center top, left -55px top, right -55px top -130px !important;
    background-size: auto, 220px 260px, 220px 260px !important;
    background-attachment: fixed !important;
    color: var(--ink) !important;
}}

@media (max-width: 1500px) {{
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-image: radial-gradient(ellipse 900px 600px at 50% -10%, rgba(46,111,82,0.06), transparent 70%) !important;
    }}
}}

#MainMenu, footer {{ visibility: hidden; display: none; }}
[data-testid="stHeader"] {{ background: transparent !important; }}
.block-container {{ max-width: 1320px !important; padding-top: 2.25rem !important; padding-bottom: 5rem !important; }}

html body, html body .stApp, html body p, html body li, html body label,
html body [data-testid="stMarkdownContainer"] {{
    font-family: 'Inter', system-ui, sans-serif !important;
    color: var(--ink) !important; font-size: 0.95rem; line-height: 1.6;
}}
html body p {{ max-width: 72ch; color: var(--ink-soft) !important; }}
html body h1, html body h2, html body h3, html body h4 {{
    font-family: 'Noto Serif Devanagari', 'Spectral', Georgia, serif !important;
    color: var(--ink) !important; font-weight: 600 !important;
    letter-spacing: -0.01em !important; text-transform: none !important;
}}
html body code, html body pre, html body .mono-text {{
    font-family: 'IBM Plex Mono', ui-monospace, monospace !important; font-size: 0.86em !important;
}}
html body code {{
    background: var(--paper-deep) !important; color: var(--green-deep) !important;
    border: 1px solid var(--rule-soft) !important; border-radius: 3px !important;
    padding: 0.08em 0.36em !important;
}}

html body .hero {{
    position: relative; background: var(--card) !important;
    border: 1px solid var(--rule) !important;
    border-left: 5px solid var(--green) !important;
    border-radius: var(--radius) !important;
    padding: 2.25rem 2.5rem 2rem !important; margin-bottom: 2.25rem !important;
    overflow: hidden;
    background-image: url("{_HERO_HELIX}") !important;
    background-repeat: repeat-y !important;
    background-position: right 2rem top -40px !important;
    background-size: 200px 236px !important;
}}
html body .kicker {{
    display: inline-block; font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important; font-weight: 500 !important;
    letter-spacing: 0 !important; text-transform: none !important;
    color: var(--muted) !important; border-bottom: 1px solid var(--rule) !important;
    padding-bottom: 0.4rem !important; margin-bottom: 0.9rem !important;
}}
html body .hero-title {{
    font-family: 'Noto Serif Devanagari', 'Spectral', Georgia, serif !important;
    font-size: clamp(1.9rem, 3.4vw, 2.7rem) !important; font-weight: 600 !important;
    line-height: 1.12 !important; letter-spacing: -0.02em !important;
    text-transform: none !important; color: var(--ink) !important;
    margin: 0 0 0.7rem !important; max-width: 22ch;
}}
html body .hero-copy {{ font-size: 0.92rem !important; color: var(--muted) !important; margin: 0 !important; }}
html body .hero-copy em, html body .hero-copy i {{
    font-family: 'Spectral', Georgia, serif !important; font-style: italic; color: var(--ink-soft) !important;
}}

html body .metric-card {{
    background: var(--card) !important; border: 1px solid var(--rule) !important;
    border-left: 3px solid var(--rule) !important; border-radius: var(--radius) !important;
    padding: 1rem 1.15rem 1.05rem !important; min-height: 100% !important;
    transition: border-left-color .18s ease, background .18s ease;
}}
html body .metric-card:hover {{ transform: none !important; border-left-color: var(--green) !important; background: #fbfdfb !important; }}
html body .metric-label {{
    font-size: 0.72rem !important; font-weight: 500 !important; letter-spacing: 0 !important;
    text-transform: none !important; color: var(--muted) !important; display: block;
}}
html body .metric-value {{
    font-family: 'Noto Serif Devanagari', 'Spectral', Georgia, serif !important; font-size: 1.85rem !important;
    font-weight: 600 !important; letter-spacing: -0.015em !important; line-height: 1.1 !important;
    color: var(--ink) !important; margin-top: 0.35rem !important; font-variant-numeric: tabular-nums;
}}
html body .metric-sub {{
    font-family: 'IBM Plex Mono', monospace !important; font-size: 0.7rem !important;
    color: var(--blue) !important; margin-top: 0.45rem !important;
}}
html body .metric-card.predicted {{ border-left-color: var(--amber) !important; }}
html body .metric-card.predicted .metric-sub {{ color: var(--amber) !important; }}

html body .source-badge {{
    display: inline-block; background: transparent !important; color: var(--green-deep) !important;
    border: 1px solid var(--rule) !important; border-radius: 999px !important;
    font-family: 'IBM Plex Mono', monospace !important; font-size: 0.74rem !important;
    padding: 0.28rem 0.75rem !important; margin-right: 0.4rem; text-decoration: none !important;
}}
html body .source-badge:hover {{ border-color: var(--green) !important; background: rgba(46,111,82,0.07) !important; }}
html body .section-title {{
    font-family: 'Noto Serif Devanagari', 'Spectral', Georgia, serif !important; font-size: 1.22rem !important;
    font-weight: 600 !important; text-transform: none !important; color: var(--ink) !important;
    border-bottom: 1px solid var(--rule) !important; padding-bottom: 0.5rem !important;
    margin: 2rem 0 1rem !important;
}}

html body .stButton > button, html body .stDownloadButton > button, html body .stFormSubmitButton > button {{
    background: var(--card) !important; color: var(--ink) !important;
    border: 1px solid var(--rule) !important; border-radius: var(--radius) !important;
    font-size: 0.87rem !important; font-weight: 500 !important; padding: 0.42rem 0.95rem !important;
}}
html body .stButton > button:hover {{ border-color: var(--green) !important; color: var(--green-deep) !important; }}
html body .stButton > button[kind="primary"], html body .stFormSubmitButton > button {{
    background: var(--green) !important; border-color: var(--green) !important; color: #fff !important;
}}
html body button:focus-visible, html body a:focus-visible, html body input:focus-visible {{
    outline: 2px solid var(--blue) !important; outline-offset: 2px !important;
}}
html body [data-baseweb="input"] input, html body [data-baseweb="select"] > div, html body textarea {{
    background: var(--card) !important; border-color: var(--rule) !important;
    border-radius: var(--radius) !important; color: var(--ink) !important;
}}

html body [data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: transparent !important; border-bottom: 1px solid var(--rule) !important; gap: 0.25rem !important;
}}
html body [data-testid="stTabs"] [data-baseweb="tab"] {{
    background: transparent !important; font-size: 0.87rem !important; font-weight: 500 !important;
    color: var(--muted) !important; padding: 0.55rem 0.8rem !important;
}}
html body [data-testid="stTabs"] [aria-selected="true"] {{
    color: var(--green-deep) !important; border-bottom: 2px solid var(--green) !important;
}}
html body [data-testid="stTabs"] [data-baseweb="tab-highlight"],
html body [data-testid="stTabs"] [data-baseweb="tab-border"] {{ background: transparent !important; }}

html body [data-testid="stPlotlyChart"],
html body [data-testid="stPyplotChart"],
html body [data-testid="stVegaLiteChart"],
html body .stPlotlyChart,
html body .figure-frame {{
    background: var(--card) !important;
    border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem !important;
    overflow: hidden;
}}
html body [data-testid="stPlotlyChart"] .main-svg,
html body [data-testid="stPlotlyChart"] .svg-container {{ background: transparent !important; }}
html body [data-testid="stPlotlyChart"] .modebar {{ background: transparent !important; }}
html body [data-testid="stPlotlyChart"] .modebar-btn path {{ fill: {MUTED} !important; }}

html body iframe[title*="stmol"], html body iframe[title*="molstar"],
html body iframe[title*="showmol"], html body .viewer_3Dmoljs {{
    background: var(--card) !important;
    border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important;
}}

html body .figure-caption {{
    font-family: 'Inter', sans-serif !important; font-size: 0.78rem !important;
    color: var(--muted) !important; border-top: 1px solid var(--rule-soft);
    padding-top: 0.5rem; margin-top: 0.5rem; max-width: none;
}}
html body .figure-caption b {{ color: var(--ink-soft) !important; font-weight: 600; }}

html body [data-testid="stExpander"] {{
    background: var(--card) !important; border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important;
}}
html body [data-testid="stExpander"] summary {{
    font-family: 'Noto Serif Devanagari', 'Spectral', Georgia, serif !important; font-size: 1rem !important;
    font-weight: 600 !important; text-transform: none !important; color: var(--ink) !important;
}}
html body [data-testid="stDataFrame"], html body div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--card) !important; border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important;
}}
html body [data-testid="stDataFrame"] * {{ font-family: 'IBM Plex Mono', monospace !important; font-size: 0.8rem !important; }}
html body [data-testid="stSidebar"] {{ background: var(--paper-deep) !important; border-right: 1px solid var(--rule) !important; }}
html body hr {{ border-color: var(--rule) !important; }}
html body a {{ color: var(--blue) !important; }}
html body a:hover {{ color: var(--green-deep) !important; }}

html body .seq {{
    display: block; background: var(--card) !important; border: 1px solid var(--rule) !important;
    border-radius: var(--radius) !important; padding: 1rem 1.15rem !important;
    line-height: 1.85 !important; letter-spacing: 0.08em !important;
    color: var(--ink) !important; word-break: break-all; font-size: 0.84rem !important;
}}
html body .seq .hydrophobic {{ color: var(--amber) !important; font-weight: 500; }}
html body .seq .polar {{ color: var(--blue) !important; }}
html body .seq .charged {{ color: var(--green-deep) !important; font-weight: 500; }}

@media (max-width: 820px) {{
    html body .hero {{ padding: 1.5rem 1.35rem !important; background-image: none !important; }}
    html body .hero-title {{ font-size: 1.6rem !important; }}
    html body .metric-value {{ font-size: 1.5rem !important; }}
}}
@media (prefers-reduced-motion: reduce) {{ html body * {{ transition: none !important; animation: none !important; }} }}
</style>
"""


def inject_css() -> None:
    st.markdown(_css(), unsafe_allow_html=True)
