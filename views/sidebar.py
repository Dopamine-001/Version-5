"""Dark navigation sidebar."""

import streamlit as st


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

        # Push the footer towards the bottom
        st.markdown("<br>" * 4, unsafe_allow_html=True)

        st.divider()

        # DATA footer — no HTML
        st.caption("#### DATA")
        st.caption("UniProt · AlphaFold DB · Biopython")
        st.caption("Protein Explorer 3.0 · Educational use")