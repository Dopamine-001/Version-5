import streamlit as st


def load_aesthetic_theme() -> None:
    """Injects high-end, custom CSS styling to transform the Streamlit app into a modern bioinformatics workstation."""
    st.markdown(
        """
        <style>
            /* Import modern font */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

            /* Global App Styling */
            .stApp {
                background-color: #0b0f19;
                color: #c9d1d9;
                font-family: 'Inter', sans-serif;
            }

            /* Sleek Hero Header */
            .hero {
                background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 2rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            }
            .kicker {
                font-family: 'JetBrains Mono', monospace;
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
                letter-spacing: -0.02em;
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
                text-align: left;
                transition: transform 0.2s ease, border-color 0.2s ease;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                border-color: rgba(5, 217, 232, 0.4);
            }
            .metric-label {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: #8b949e;
                margin-bottom: 0.3rem;
            }
            .metric-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: #f0f6fc;
            }
            .metric-sub {
                font-size: 0.75rem;
                color: #05D9E8;
                margin-top: 0.3rem;
            }

            /* Section Titles */
            .section-title {
                font-size: 1.25rem;
                font-weight: 600;
                color: #f0f6fc;
                margin-top: 1.5rem;
                margin-bottom: 1rem;
                letter-spacing: -0.01em;
                border-left: 3px solid #05D9E8;
                padding-left: 0.75rem;
            }

            /* Source Badges */
            .source-badge {
                display: inline-block;
                background-color: rgba(5, 217, 232, 0.1);
                color: #05D9E8;
                border: 1px solid rgba(5, 217, 232, 0.2);
                border-radius: 6px;
                padding: 0.2rem 0.6rem;
                font-size: 0.75rem;
                font-family: 'JetBrains Mono', monospace;
                margin-right: 0.4rem;
                margin-bottom: 0.4rem;
            }

            /* Custom Tabs Styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: #0d1117;
                padding: 6px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.06);
            }
            .stTabs [data-baseweb="tab"] {
                background-color: transparent;
                border-radius: 6px;
                color: #8b949e;
                font-weight: 500;
                padding: 8px 16px;
                height: auto;
            }
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, rgba(5, 217, 232, 0.2), rgba(5, 217, 232, 0.05));
                color: #05D9E8;
                border: 1px solid rgba(5, 217, 232, 0.3);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
