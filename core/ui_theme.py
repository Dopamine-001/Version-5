import streamlit as st

def load_aesthetic_theme() -> None:
    """Injects a powerful, high-end bioinformatics workstation theme featuring a custom repeating DNA double-helix vector pattern and neon glowing accents."""
    st.markdown(
        """
        <style>
            /* Import modern fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

            /* Global App & Viewport Overrides with an Embedded DNA Double-Helix Pattern */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #040711 !important;
                background-image: 
                    radial-gradient(circle at 10% 15%, rgba(5, 217, 232, 0.12) 0%, transparent 45%),
                    radial-gradient(circle at 90% 85%, rgba(114, 9, 183, 0.12) 0%, transparent 45%),
                    url("data:image/svg+xml,%3Csvg width='140' height='140' viewBox='0 0 140 140' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cpath d='M20 10c30 30 30 90 0 120M120 10c-30 30-30 90 0 120' stroke='rgba(5, 217, 232, 0.07)' stroke-width='2'/%3E%3Cpath d='M120 10c-30 30-30 90 0 120' stroke='rgba(114, 9, 183, 0.05)' stroke-width='1.5'/%3E%3Cline x1='45' y1='45' x2='95' y2='45' stroke='rgba(5, 217, 232, 0.06)' stroke-width='1.5'/%3E%3Cline x1='30' y1='70' x2='110' y2='70' stroke='rgba(114, 9, 183, 0.06)' stroke-width='1.5'/%3E%3Cline x1='45' y1='95' x2='95' y2='95' stroke='rgba(5, 217, 232, 0.06)' stroke-width='1.5'/%3E%3C/g%3E%3C/svg%3E") !important;
                color: #c9d1d9 !important;
                font-family: 'Inter', sans-serif !important;
            }

            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #070b17 !important;
                border-right: 1px solid rgba(5, 217, 232, 0.12);
            }
            [data-testid="stSidebar"] * {
                color: #c9d1d9 !important;
            }

            /* Sleek Hero Header with Neon Gradient Border */
            .hero {
                background: linear-gradient(135deg, rgba(18, 24, 38, 0.85) 0%, rgba(10, 15, 26, 0.92) 100%);
                border: 1px solid rgba(5, 217, 232, 0.25);
                border-radius: 14px;
                padding: 2.2rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.12);
                backdrop-filter: blur(12px);
            }
            .kicker {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: #05D9E8;
                margin-bottom: 0.5rem;
                text-shadow: 0 0 12px rgba(5, 217, 232, 0.5);
            }
            .hero-title {
                font-size: 2.3rem;
                font-weight: 700;
                color: #f0f6fc;
                letter-spacing: -0.02em;
                margin-bottom: 0.5rem;
            }
            .hero-copy {
                font-size: 0.95rem;
                color: #8b949e;
            }

            /* Metric Cards with Glowing Hover Effects */
            .metric-card {
                background: linear-gradient(145deg, rgba(18, 25, 38, 0.9) 0%, rgba(11, 17, 28, 0.95) 100%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: left;
                box-shadow: 0 6px 20px rgba(0,0,0,0.4);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                backdrop-filter: blur(8px);
            }
            .metric-card:hover {
                transform: translateY(-3px);
                border-color: rgba(5, 217, 232, 0.5);
                box-shadow: 0 12px 28px rgba(5, 217, 232, 0.2);
            }
            .metric-label {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                color: #8b949e;
                margin-bottom: 0.3rem;
            }
            .metric-value {
                font-size: 1.6rem;
                font-weight: 700;
                color: #f0f6fc;
            }
            .metric-sub {
                font-size: 0.75rem;
                color: #05D9E8;
                margin-top: 0.3rem;
                font-family: 'JetBrains Mono', monospace;
            }

            /* Source Badges */
            .source-badge {
                display: inline-block;
                background-color: rgba(5, 217, 232, 0.08);
                color: #05D9E8;
                border: 1px solid rgba(5, 217, 232, 0.25);
                border-radius: 6px;
                padding: 0.2rem 0.65rem;
                font-size: 0.75rem;
                font-family: 'JetBrains Mono', monospace;
                margin-right: 0.4rem;
                margin-bottom: 0.4rem;
                box-shadow: 0 0 10px rgba(5, 217, 232, 0.12);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
