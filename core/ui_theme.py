import streamlit as st

def load_aesthetic_theme() -> None:
    """Injects an elite cyberpunk-bioinformatics laboratory theme featuring an integrated SVG double-helix DNA strand and molecular grid backdrop."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@500;700;900&family=Inter:wght@300;400;600&display=swap');

            /* Global Sci-Fi Biological Grid & DNA Double-Helix Backdrop */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #010308 !important;
                background-image: 
                    radial-gradient(circle at 15% 25%, rgba(5, 217, 232, 0.12) 0%, transparent 40%),
                    radial-gradient(circle at 85% 75%, rgba(255, 0, 127, 0.08) 0%, transparent 40%),
                    url("data:image/svg+xml,%3Csvg width='180' height='180' viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd' opacity='0.12'%3E%3Cpath d='M30 15c40 35 40 115 0 150M150 15c-40 35-40 115 0 150' stroke='%2305D9E8' stroke-width='2'/%3E%3Cpath d='M150 15c-40 35-40 115 0 150' stroke='%23ff007f' stroke-width='1.5' stroke-dasharray='4 4'/%3E%3Cline x1='60' y1='50' x2='120' y2='50' stroke='%2305D9E8' stroke-width='1.5'/%3E%3Cline x1='45' y1='90' x2='135' y2='90' stroke='%23ff007f' stroke-width='1.5'/%3E%3Cline x1='60' y1='130' x2='120' y2='130' stroke='%2305D9E8' stroke-width='1.5'/%3E%3Ccircle cx='60' cy='50' r='3' fill='%2305D9E8'/%3E%3Ccircle cx='120' cy='50' r='3' fill='%23ff007f'/%3E%3Ccircle cx='45' cy='90' r='3' fill='%23ff007f'/%3E%3Ccircle cx='135' cy='90' r='3' fill='%2305D9E8'/%3E%3Ccircle cx='60' cy='130' r='3' fill='%2305D9E8'/%3E%3Ccircle cx='120' cy='130' r='3' fill='%23ff007f'/%3E%3C/g%3E%3C/svg%3E") !important;
                background-size: auto, auto, 180px 180px !important;
                color: #e2e8f0 !important;
                font-family: 'Inter', sans-serif !important;
            }

            /* Custom Terminal Scrollbar */
            ::-webkit-scrollbar { width: 4px; height: 4px; }
            ::-webkit-scrollbar-track { background: #010308; }
            ::-webkit-scrollbar-thumb { background: #05D9E8; border-radius: 2px; }

            /* Sidebar Lab Control Panel */
            [data-testid="stSidebar"] {
                background-color: #030612 !important;
                border-right: 1px solid rgba(5, 217, 232, 0.2);
                box-shadow: inset -10px 0 20px rgba(0,0,0,0.8);
            }
            [data-testid="stSidebar"] * {
                color: #94a3b8 !important;
            }

            /* Cyberpunk Hero Command Header */
            .hero {
                background: linear-gradient(135deg, rgba(6, 12, 25, 0.95) 0%, rgba(1, 3, 8, 0.98) 100%);
                border: 1px solid rgba(5, 217, 232, 0.4);
                border-radius: 4px;
                padding: 2.5rem;
                margin-bottom: 2rem;
                position: relative;
                box-shadow: 0 0 30px rgba(5, 217, 232, 0.12), inset 0 0 15px rgba(5, 217, 232, 0.05);
            }
            .hero::before {
                content: "● LIVE TELEMETRY // PROTEIN_DB: ACTIVE";
                position: absolute;
                top: 12px;
                right: 15px;
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.65rem;
                color: #05D9E8;
                letter-spacing: 0.15em;
                animation: pulse-glow 2s infinite;
            }
            @keyframes pulse-glow {
                0% { opacity: 0.4; }
                50% { opacity: 1; text-shadow: 0 0 8px #05D9E8; }
                100% { opacity: 0.4; }
            }
            .kicker {
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.2em;
                color: #ff007f;
                margin-bottom: 0.5rem;
            }
            .hero-title {
                font-family: 'Orbitron', sans-serif;
                font-size: 2.4rem;
                font-weight: 700;
                color: #ffffff;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                margin-bottom: 0.75rem;
                text-shadow: 0 0 20px rgba(255,255,255,0.2);
            }
            .hero-copy {
                font-size: 0.95rem;
                color: #64748b;
                font-family: 'Share Tech Mono', monospace;
                letter-spacing: 0.05em;
            }

            /* High-Tech Telemetry Cards */
            .metric-card {
                background: rgba(4, 9, 20, 0.92);
                border: 1px solid #1e293b;
                border-left: 3px solid #05D9E8;
                border-radius: 2px;
                padding: 1.25rem;
                position: relative;
                transition: all 0.2s ease;
            }
            .metric-card:hover {
                border-color: #05D9E8;
                box-shadow: 0 0 20px rgba(5, 217, 232, 0.2);
                transform: translateY(-2px);
            }
            .metric-label {
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 0.15em;
                color: #64748b;
                margin-bottom: 0.3rem;
            }
            .metric-value {
                font-family: 'Orbitron', sans-serif;
                font-size: 1.6rem;
                font-weight: 700;
                color: #f8fafc;
            }
            .metric-sub {
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.75rem;
                color: #05D9E8;
                margin-top: 0.3rem;
            }

            /* Section Headers with Lab Grid Indicators */
            .section-title {
                font-family: 'Orbitron', sans-serif;
                font-size: 1.1rem;
                font-weight: 700;
                color: #f8fafc;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                margin-top: 2rem;
                margin-bottom: 1rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            .section-title::before {
                content: "[+]";
                font-family: 'Share Tech Mono', monospace;
                color: #ff007f;
                font-size: 1rem;
            }

            /* Monospace Source Badges */
            .source-badge {
                display: inline-block;
                background-color: rgba(5, 217, 232, 0.05);
                color: #05D9E8;
                border: 1px dashed rgba(5, 217, 232, 0.3);
                border-radius: 2px;
                padding: 0.2rem 0.6rem;
                font-size: 0.7rem;
                font-family: 'Share Tech Mono', monospace;
                letter-spacing: 0.1em;
                margin-right: 0.4rem;
                margin-bottom: 0.4rem;
            }

            /* Sci-Fi Action Buttons */
            .stButton button {
                background: #010308 !important;
                color: #05D9E8 !important;
                font-family: 'Orbitron', sans-serif !important;
                font-size: 0.8rem !important;
                font-weight: 700 !important;
                letter-spacing: 0.1em !important;
                border: 1px solid #05D9E8 !important;
                border-radius: 2px !important;
                padding: 0.5rem 1rem !important;
                box-shadow: inset 0 0 10px rgba(5, 217, 232, 0.1);
                transition: all 0.2s ease !important;
            }
            .stButton button:hover {
                background: #05D9E8 !important;
                color: #010308 !important;
                box-shadow: 0 0 15px rgba(5, 217, 232, 0.6);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
