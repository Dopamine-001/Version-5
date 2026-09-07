import streamlit as st

def load_aesthetic_theme() -> None:
    """Injects high-end, custom CSS styling with guaranteed selectors."""
    st.markdown(
        """
        <style>
            /* Force global dark background across the entire Streamlit frame */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #0b0f19 !important;
                color: #c9d1d9 !important;
            }

            /* Sleek Hero Header Container */
            .hero {
                background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 2rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            }
            .kicker {
                font-family: monospace;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: #05D9E8;
                margin-bottom: 0.5rem;
            }
            .hero-title {
                font-size: 2.2rem;
                font-weight: 700;
                color: #f0f6fc;
                margin-bottom: 0.5rem;
            }
            .hero-copy {
                font-size: 0.95rem;
                color: #8b949e;
            }

            /* Metric Cards */
            .metric-card {
                background-color: #161b22;
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 10px;
                padding: 1.2rem;
            }
            .metric-label {
                font-size: 0.75rem;
                text-transform: uppercase;
                color: #8b949e;
            }
            .metric-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: #f0f6fc;
            }
            .metric-sub {
                font-size: 0.75rem;
                color: #05D9E8;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
