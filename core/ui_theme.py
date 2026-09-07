import streamlit as st

def load_aesthetic_theme() -> None:
    """Injects a high-end, editorial dark-mode aesthetic with rich gradients, glassmorphic panels, and refined typography."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Space+Mono:wght@400;700&display=swap');

            /* Global App Styling: Deep Obsidian with Ambient Indigo/Violet Glows */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #0c0e15 !important;
                background-image: 
                    radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.08) 0%, transparent 45%),
                    radial-gradient(circle at 90% 90%, rgba(236, 72, 153, 0.06) 0%, transparent 45%) !important;
                color: #e2e8f0 !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            /* Custom Refined Scrollbar */
            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-track { background: #0c0e15; }
            ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
            ::-webkit-scrollbar-thumb:hover { background: #6366f1; }

            /* Editorial Sidebar */
            [data-testid="stSidebar"] {
                background-color: #10131d !important;
                border-right: 1px solid rgba(255, 255, 255, 0.04);
            }
            [data-testid="stSidebar"] * {
                color: #94a3b8 !important;
            }

            /* Premium Glassmorphic Hero Banner */
            .hero {
                background: linear-gradient(135deg, rgba(25, 30, 45, 0.6) 0%, rgba(15, 18, 28, 0.8) 100%);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 16px;
                padding: 2.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
            }
            .hero::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background: linear-gradient(to bottom, #6366f1, #ec4899);
            }
            .kicker {
                font-family: 'Space Mono', monospace;
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.15em;
                color: #818cf8;
                margin-bottom: 0.75rem;
            }
            .hero-title {
                font-size: 2.5rem;
                font-weight: 700;
                color: #f8fafc;
                letter-spacing: -0.03em;
                margin-bottom: 0.75rem;
            }
            .hero-copy {
                font-size: 1rem;
                color: #94a3b8;
                max-width: 650px;
                line-height: 1.6;
            }

            /* Floating Glass Cards */
            .metric-card {
                background: rgba(20, 24, 38, 0.7);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 1.5rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .metric-card:hover {
                transform: translateY(-3px);
                border-color: rgba(99, 102, 241, 0.3);
                box-shadow: 0 12px 30px -10px rgba(99, 102, 241, 0.15);
            }
            .metric-label {
                font-family: 'Space Mono', monospace;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: #64748b;
                margin-bottom: 0.5rem;
            }
            .metric-value {
                font-size: 1.8rem;
                font-weight: 700;
                color: #f8fafc;
                letter-spacing: -0.02em;
            }
            .metric-sub {
                font-size: 0.75rem;
                color: #818cf8;
                margin-top: 0.4rem;
                font-family: 'Space Mono', monospace;
            }

            /* Editorial Section Titles */
            .section-title {
                font-size: 1.25rem;
                font-weight: 600;
                color: #f8fafc;
                margin-top: 2.5rem;
                margin-bottom: 1.25rem;
                letter-spacing: -0.01em;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            .section-title::before {
                content: "";
                display: inline-block;
                width: 6px;
                height: 6px;
                background-color: #6366f1;
                border-radius: 50%;
                box-shadow: 0 0 10px #6366f1;
            }

            /* Sleek Source Badges */
            .source-badge {
                display: inline-block;
                background-color: rgba(99, 102, 241, 0.1);
                color: #a5b4fc;
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 6px;
                padding: 0.25rem 0.75rem;
                font-size: 0.75rem;
                font-family: 'Space Mono', monospace;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
            }

            /* Modern Buttons */
            .stButton button {
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
                color: #ffffff !important;
                font-weight: 600 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.6rem 1.2rem !important;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
                transition: all 0.2s ease !important;
            }
            .stButton button:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
