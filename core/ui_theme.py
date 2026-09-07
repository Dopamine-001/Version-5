import streamlit as st

def load_aesthetic_theme() -> None:
    """Injects a powerful, high-end bioinformatics workstation theme with a subtle DNA nucleotide structure background and neon glowing accents."""
    st.markdown(
        """
        <style>
            /* Import modern fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

            /* Global App & Viewport Overrides with a subtle SVG Nucleotide/DNA Matrix Background Pattern */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #060913 !important;
                background-image: 
                    radial-gradient(circle at 15% 20%, rgba(5, 217, 232, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 85% 80%, rgba(114, 9, 183, 0.08) 0%, transparent 40%),
                    url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M10 10c20 20 20 60 0 80M90 10c-20 20-20 60 0 80M30 30c10 10 10 30 0 40M70 30c-10 10-10 30 0 40' stroke='rgba(5, 217, 232, 0.03)' stroke-width='1.5' fill='none'/%3E%3C/svg%3E") !important;
                color: #c9d1d9 !important;
                font-family: 'Inter', sans-serif !important;
            }

            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #0a0e1a !important;
                border-right: 1px solid rgba(5, 217, 232, 0.1);
            }
            [data-testid="stSidebar"] * {
                color: #c9d1d9 !important;
            }

            /* Sleek Hero Header with Neon Gradient Border */
            .hero {
                background: linear-gradient(135deg, rgba(22, 27, 34, 0.9) 0%, rgba(13, 17, 23, 0.95) 100%);
                border: 1px solid rgba(5, 217, 232, 0.2);
                border-radius: 14px;
                padding: 2.2rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
            }
            .kicker {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: #05D9E8;
                margin-bottom: 0.5rem;
                text-shadow: 0 0 10px rgba(5, 217, 232, 0.4);
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
                background: linear-gradient(145deg, #121824 0%, #0d121c 100%);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: left;
                box-shadow: 0 6px 16px rgba(0,0,0,0.3);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .metric-card:hover {
                transform: translateY(-3px);
                border-color: rgba(5, 217, 232, 0.4);
                box-shadow: 0 10px 24px rgba(5, 217, 232, 0.15);
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
                box-shadow: 0 0 8px rgba(5, 217, 232, 0.1);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
