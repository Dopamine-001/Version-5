"""Dark navigation sidebar."""

import streamlit as st
from core.database import get_recent_searches


def render_sidebar() -> None:

    with st.sidebar:

        # Logo / title
        st.markdown("# 🧬 Protein Explorer")
        st.caption("Explore · Visualize · Understand")

        st.divider()

        # Navigation
        st.markdown("### Analysis modules")

        st.markdown(
            "**◈ Overview**  \n\n"
            "**◇ 3D Structure**  \n\n"
            "**⌁ Sequence**  \n\n"
            "**⊙ Domains & Sites**  \n\n"
            "**✣ PTM / Modifications**  \n\n"
            "**⑂ Mutations**  \n\n"
            "**△ Physicochemical**  \n\n"
            "**⌁ Ramachandran**  \n\n"
            "**⇄ Comparison**"
        )

        st.divider()

        # Recent Searches Section
        st.markdown("### 📜 Recent Searches")
        
        recent_df = get_recent_searches(limit=5)
        
        if not recent_df.empty:
            for _, row in recent_df.iterrows():
                query = row["query"]
                timestamp = row["timestamp"]
                # Display each past query as an interactive button
                if st.button(f"🔍 {query}", key=f"hist_{timestamp}_{query}", use_container_width=True):
                    st.session_state["protein_query"] = query
                    st.rerun()
        else:
            st.caption("No search history yet.")

        # Push the footer towards the bottom
        st.markdown("<br>" * 2, unsafe_allow_html=True)

        st.divider()

        # DATA footer — no HTML
        st.caption("#### DATA")
        st.caption("UniProt · AlphaFold DB · Biopython")
        st.caption("Protein Explorer 3.0 · Educational use")
