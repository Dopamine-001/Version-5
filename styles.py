"""Dark black molecular theme for Protein Explorer."""

import streamlit as st

CUSTOM_CSS = r'''
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root{
    --bg:#050505;
    --panel:#0b0b0b;
    --panel-2:#101010;
    --line:#242424;
    --text:#f5f5f5;
    --muted:#a6a6a6;
    --accent:#7ee7d8;
    --accent-2:#9b9b9b;
}

/* =========================================================
   MAIN APPLICATION
   ========================================================= */

.stApp{
    color:var(--text);
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(126,231,216,.07),
            transparent 28%
        ),
        radial-gradient(
            circle at 5% 90%,
            rgba(255,255,255,.035),
            transparent 30%
        ),
        #050505;
}

/* Subtle molecular background */

.stApp:before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    z-index:0;
    opacity:.035;

    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='380' height='560' viewBox='0 0 380 560'%3E%3Cg fill='none' stroke='%237ee7d8' stroke-width='2'%3E%3Cpath d='M70 0 C300 70 300 210 70 280 C-160 350 -160 490 70 560'/%3E%3Cpath d='M310 0 C80 70 80 210 310 280 C540 350 540 490 310 560'/%3E%3Cpath d='M100 35L280 35M78 105L302 105M82 175L298 175M110 245L270 245M110 315L270 315M82 385L298 385M78 455L302 455M100 525L280 525' opacity='.7'/%3E%3C/g%3E%3C/svg%3E");

    background-position:right top;
    background-repeat:repeat-y;
    background-size:380px 560px;
}

/* =========================================================
   CONTENT
   ========================================================= */

.block-container{
    max-width:1500px;
    padding-top:3rem;
    padding-bottom:4rem;
    position:relative;
    z-index:1;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"]{
    background:#070707;
    border-right:1px solid #202020;
}

[data-testid="stSidebar"] *{
    color:var(--text);
}

/* =========================================================
   HEADINGS
   ========================================================= */

h1,h2,h3,h4{
    color:var(--text)!important;
    letter-spacing:-.02em;
}

/* =========================================================
   HERO
   ========================================================= */

.hero{
    padding:2rem 0 1.1rem;
    margin-bottom:1rem;
}

.kicker{
    font:700 1rem 'Space Mono',monospace;
    letter-spacing:.14em;
    text-transform:uppercase;
    color:var(--accent);
}

.hero-title{
    color:#ffffff!important;
    font-size:clamp(2.2rem,5vw,4rem);
    font-weight:700;
    line-height:1;
    margin:.35rem 0;
}

.hero-copy{
    color:var(--muted);
    max-width:900px;
    font-size:1rem;
    line-height:1.6;
}

/* =========================================================
   METRIC CARDS
   ========================================================= */

.metric-card{
    background:
        linear-gradient(
            145deg,
            rgba(18,18,18,.98),
            rgba(8,8,8,.98)
        );

    border:1px solid var(--line);
    border-radius:14px;
    padding:.9rem 1rem;
    min-height:88px;

    box-shadow:
        0 12px 32px rgba(0,0,0,.35);
}

.metric-label{
    color:#999;
    font:500 .64rem 'Space Mono',monospace;
    text-transform:uppercase;
    letter-spacing:.07em;
}

.metric-value{
    color:#fff;
    font-size:1.35rem;
    font-weight:700;
    margin-top:.25rem;
}

.metric-sub{
    color:var(--accent);
    font-size:.72rem;
}

/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title{
    margin:1.15rem 0 .55rem;
    color:#f5f5f5;
    font-size:1.2rem;
    font-weight:700;
}

.section-caption,
.small-note{
    color:var(--muted);
    font-size:.84rem;
    line-height:1.5;
}

/* =========================================================
   SOURCE BADGES
   ========================================================= */

.source-badge{
    display:inline-block;
    padding:.2rem .48rem;
    margin:.15rem .2rem .15rem 0;

    border:1px solid #292929;
    border-radius:999px;

    color:#cfcfcf;
    background:#111;

    font:500 .65rem 'Space Mono',monospace;
}

/* =========================================================
   BUTTONS
   ========================================================= */

.stButton>button{
    border-radius:9px;
    border:1px solid #303030;
    background:#111;
    color:#f5f5f5;
    font-weight:600;
}

.stButton>button:hover{
    border-color:var(--accent);
    background:#151515;
    color:#fff;
}

.stButton>button[kind="primary"]{
    background:#151515;
    border-color:var(--accent);
    color:var(--accent);
}

/* =========================================================
   CONTAINERS
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"]{
    border-color:#252525!important;
    background:rgba(13,13,13,.94);
    border-radius:14px;
}

/* =========================================================
   INPUTS
   ========================================================= */

.stTextInput input,
.stTextArea textarea{
    background:#0d0d0d!important;
    color:#f5f5f5!important;
    border-color:#292929!important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder{
    color:#666!important;
}

/* =========================================================
   SELECT BOXES
   ========================================================= */

.stSelectbox div[data-baseweb="select"]>div{
    background:#0d0d0d;
    border-color:#292929;
    color:#f5f5f5;
}

/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"]{
    gap:.2rem;
    border-bottom:1px solid #242424;
}

.stTabs [data-baseweb="tab"]{
    color:#888;
}

.stTabs [aria-selected="true"]{
    color:var(--accent)!important;
    font-weight:700;
}

/* =========================================================
   METRICS
   ========================================================= */

[data-testid="stMetricValue"]{
    color:#f5f5f5!important;
}

/* =========================================================
   DATAFRAMES
   ========================================================= */

[data-testid="stDataFrame"]{
    border:1px solid #242424;
    border-radius:10px;
    overflow:hidden;
}

/* =========================================================
   LINKS
   ========================================================= */

a{
    color:var(--accent)!important;
}

/* =========================================================
   DIVIDERS
   ========================================================= */

hr{
    border-color:#242424!important;
}

</style>
'''


def inject_css() -> None:
    st.markdown(
        CUSTOM_CSS,
        unsafe_allow_html=True,
    )
```
