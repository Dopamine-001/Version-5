import streamlit as st

def load_aesthetic_theme() -> None:
    """Injects a high-performance, dark-mode computational biology workstation design system."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

            /* Global Viewport & Background Setup */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #030712 !important;
                color: #e2e8f0 !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            /* Custom Sleek Scrollbar */
            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            ::-webkit-scrollbar-track {
                background: #030712;
            }
            ::-webkit-scrollbar-thumb {
                background: #1e293b;
                border-radius: 3px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #05D9E8;
            }

            /* Sidebar Transformation */
            [data-testid="stSidebar"] {
                background-color: #050b18 !important;
                border-right: 1px solid rgba(5, 217, 232, 0.15);
            }
            [data-testid="stSidebar"] * {
                color: #cbd5e1 !important;
            }

            /* Tactical Command Hero Header */
            .hero {
                background: linear-gradient(135deg, #0b132b 0%, #030712 100%);
                border: 1px solid rgba(5, 217, 232, 0.3);
                border-left: 4px solid #05D9E8;
                border-radius: 8px;
                padding: 2.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
            }
            .hero::after {
                content: "BIO-NODE // v5.0";
                position: absolute;
                right: 20px;
                bottom: 10px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.65rem;
                color: rgba(5, 217, 232, 0.2);
                letter-spacing: 0.2em;
            }
            .kicker {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.15em;
                color: #05D9E8;
                margin-bottom: 0.75rem;
                display: inline-block;
                background: rgba(5, 217, 232, 0.08);
                padding: 0.25rem 0.6rem;
                border-radius: 4px;
                border: 1px solid rgba(5, 217, 232, 0.2);
            }
            .hero-title {
                font-size: 2.6rem;
                font-weight: 700;
                color: #ffffff;
                letter-spacing: -0.03em;
                margin-bottom: 0.75rem;
            }
            .hero-copy {
                font-size: 1rem;
                color: #94a3b8;
                max-width: 650px;
                line-height: 1.6;
            }

            /* Asymmetric Data Cards */
            .metric-card {
                background: #080e1e;
                border: 1px solid #1e293b;
                border-top: 2px solid #3b82f6;
                border-radius: 8px;
                padding: 1.5rem;
                position: relative;
                transition: all 0.25s ease;
            }
            .metric-card:hover {
                border-color: #05D9E8;
                transform: translateY(-2px);
                box-shadow: 0 10px 30px -10px rgba(5, 217, 232, 0.2);
            }
            .metric-label {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: #64748b;
                margin-bottom: 0.4rem;
            }
            .metric-value {
                font-size: 1.8rem;
                font-weight: 700;
                color: #f8fafc;
                font-family: 'JetBrains Mono', monospace;
            }
            .metric-sub {
                font-size: 0.75rem;
                color: #05D9E8;
                margin-top: 0.4rem;
                font-family: 'JetBrains Mono', monospace;
            }

            /* Section Headers */
            .section-title {
                font-size: 1.35rem;
                font-weight: 600;
                color: #f8fafc;
                margin-top: 2rem;
                margin-bottom: 1rem;
                letter-spacing: -0.01em;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            .section-title::before {
                content: "";
                display: inline-block;
                width: 4px;
                height: 1.2rem;
                background-color: #05D9E8;
                border-radius: 2px;
            }

            /* Data Badges */
            .source-badge {
                display: inline-block;
                background-color: rgba(5, 217, 232, 0.06);
                color: #05D9E8;
                border: 1px solid rgba(5, 217, 232, 0.2);
                border-radius: 4px;
                padding: 0.25rem 0.7rem;
                font-size: 0.75rem;
                font-family: 'JetBrains Mono', monospace;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
            }

            /* Streamlit Inputs & Buttons Overhaul */
            .stButton button {
                background: linear-gradient(135deg, #05D9E8 0%, #0077b6 100%) !important;
                color: #030712 !important;
                font-weight: 600 !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.5rem 1rem !important;
                transition: filter 0.2s ease !important;
            }
            .stButton button:hover {
                filter: brightness(1.2);
            }
            
            /* Input boxes framing */
            [data-testid="stTextInput"] input {
                background-color: #050b18 !important;
                border: 1px solid #1e293b !important;
                color: #f8fafc !important;
                border-radius: 6px !important;
            }
            [data-testid="stTextInput"] input:focus {
                border-color: #05D9E8 !important;
                box-shadow: 0 0 10px rgba(5, 217, 232, 0.2) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
