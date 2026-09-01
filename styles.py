"""Dark black molecular theme for Protein Explorer."""

import streamlit as st


CUSTOM_CSS = """
<style>

:root {
    --bg: #050505;
    --panel: #0c0c0c;
    --border: #242424;
    --text: #f5f5f5;
    --muted: #999999;
    --accent: #7ee7d8;
}


/* Main application */

.stApp {
    background: #050505;
    color: #f5f5f5;
}


/* Main content */

.block-container {
    max-width: 1500px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}


/* Sidebar */

[data-testid="stSidebar"] {
    background: #070707;
    border-right: 1px solid #242424;
}

[data-testid="stSidebar"] * {
    color: #f5f5f5;
}


/* Headings */

h1, h2, h3, h4 {
    color: #f5f5f5 !important;
}


/* Hero */

.hero {
    padding: 2rem 0 1.1rem;
    margin-bottom: 1rem;
}

.kicker {
    color: #7ee7d8;
    font-family: monospace;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.hero-title {
    color: #ffffff !important;
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1.1;
    margin: 0.4rem 0;
}

.hero-copy {
    color: #999999;
    font-size: 1rem;
    line-height: 1.6;
}


/* Metric cards */

.metric-card {
    background: #0c0c0c;
    border: 1px solid #242424;
    border-radius: 14px;
    padding: 1rem;
    min-height: 88px;
}

.metric-label {
    color: #999999;
    font-family: monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
}

.metric-value {
    color: #ffffff;
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 0.25rem;
}

.metric-sub {
    color: #7ee7d8;
    font-size: 0.72rem;
}


/* Section titles */

.section-title {
    margin: 1.15rem 0 0.55rem;
    color: #ffffff;
    font-size: 1.2rem;
    font-weight: 700;
}


/* Containers */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #0c0c0c;
    border: 1px solid #242424 !important;
    border-radius: 14px;
}


/* Text inputs */

.stTextInput input,
.stTextArea textarea {
    background: #0d0d0d !important;
    color: #ffffff !important;
    border-color: #242424 !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #666666 !important;
}


/* Select boxes */

.stSelectbox div[data-baseweb="select"] > div {
    background: #0d0d0d;
    border-color: #242424;
    color: #ffffff;
}


/* Buttons */

.stButton > button {
    background: #111111;
    color: #ffffff;
    border: 1px solid #303030;
    border-radius: 9px;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #7ee7d8;
    color: #7ee7d8;
}


/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    border-bottom: 1px solid #242424;
}

.stTabs [data-baseweb="tab"] {
    color: #888888;
}

.stTabs [aria-selected="true"] {
    color: #7ee7d8 !important;
    font-weight: 700;
}


/* Dataframes */

[data-testid="stDataFrame"] {
    border: 1px solid #242424;
    border-radius: 10px;
}


/* Links */

a {
    color: #7ee7d8 !important;
}


/* Dividers */

hr {
    border-color: #242424 !important;
}

</style>
"""


def inject_css() -> None:
    st.markdown(
        CUSTOM_CSS,
        unsafe_allow_html=True,
    )
