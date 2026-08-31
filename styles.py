"""Dark navy/teal molecular theme for Protein Explorer."""

import streamlit as st

CUSTOM_CSS = r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
:root{--line:#1d3a61;--text:#f4f8ff;--muted:#b5c7df;--cyan:#43d9d0;}
.stApp{color:var(--text);background:radial-gradient(circle at 80% 0%,rgba(77,163,255,.13),transparent 30%),radial-gradient(circle at 10% 90%,rgba(154,124,255,.10),transparent 30%),linear-gradient(135deg,#030713,#07152d 55%,#040917);}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.09;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='380' height='560' viewBox='0 0 380 560'%3E%3Cg fill='none' stroke='%2343d9d0' stroke-width='2'%3E%3Cpath d='M70 0 C300 70 300 210 70 280 C-160 350 -160 490 70 560'/%3E%3Cpath d='M310 0 C80 70 80 210 310 280 C540 350 540 490 310 560'/%3E%3Cpath d='M100 35L280 35M78 105L302 105M82 175L298 175M110 245L270 245M110 315L270 315M82 385L298 385M78 455L302 455M100 525L280 525' opacity='.7'/%3E%3C/g%3E%3C/svg%3E");background-position:right top;background-repeat:repeat-y;background-size:380px 560px;}
.block-container{max-width:1500px;padding-top:1.05rem;padding-bottom:4rem;position:relative;z-index:1;}
[data-testid="stSidebar"]{background:rgba(3,9,22,.97);border-right:1px solid var(--line);}[data-testid="stSidebar"] *{color:var(--text);}
h1,h2,h3,h4{color:var(--text)!important;letter-spacing:-.02em;}
.hero{padding: 2rem 0 1.1rem;margin-bottom:1rem;}.kicker{font:700 1rem 'Space Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--cyan);}.hero-title{font-size:clamp(2.2rem,5vw,4rem);font-weight:700;line-height:1;margin:.35rem 0;}.hero-copy{color:var(--muted);max-width:900px;font-size:1rem;line-height:1.6;}
.metric-card{background:linear-gradient(145deg,rgba(14,35,66,.96),rgba(7,18,37,.96));border:1px solid var(--line);border-radius:14px;padding:.9rem 1rem;min-height:88px;box-shadow:0 12px 32px rgba(0,0,0,.2);}.metric-label{color:var(--muted);font:500 .64rem 'Space Mono',monospace;text-transform:uppercase;letter-spacing:.07em;}.metric-value{color:var(--text);font-size:1.35rem;font-weight:700;margin-top:.25rem;}.metric-sub{color:var(--cyan);font-size:.72rem;}
.section-title{margin:1.15rem 0 .55rem;color:var(--text);font-size:1.2rem;font-weight:700;}.section-caption,.small-note{color:var(--muted);font-size:.84rem;line-height:1.5;}.source-badge{display:inline-block;padding:.2rem .48rem;margin:.15rem .2rem .15rem 0;border:1px solid var(--line);border-radius:999px;color:#b9d5f2;background:#0b1c36;font:500 .65rem 'Space Mono',monospace;}
.stButton>button{border-radius:9px;border:1px solid #245277;background:#0d2746;color:var(--text);font-weight:600;}.stButton>button:hover{border-color:var(--cyan);background:#103457;color:white;}.stButton>button[kind="primary"]{background:linear-gradient(90deg,#087f86,#1769a8);border-color:#32cbd0;}
div[data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--line)!important;background:rgba(11,27,51,.90);border-radius:14px;}.stTextInput input,.stTextArea textarea{background:#0b1e38!important;color:var(--text)!important;border-color:var(--line)!important;}.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#6682a6!important;}.stSelectbox div[data-baseweb="select"]>div{background:#0b1e38;border-color:var(--line);color:var(--text);}.stTabs [data-baseweb="tab-list"]{gap:.2rem;border-bottom:1px solid var(--line);}.stTabs [data-baseweb="tab"]{color:var(--muted);}.stTabs [aria-selected="true"]{color:var(--cyan)!important;font-weight:700;}[data-testid="stMetricValue"]{color:var(--text)!important;}[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:10px;overflow:hidden;}a{color:var(--cyan)!important;}hr{border-color:var(--line)!important;}
</style>
'''

def inject_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
