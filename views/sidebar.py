"""Dark navigation sidebar."""
import streamlit as st

def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("# 🧬 Protein Explorer")
        st.caption("Explore · Visualize · Understand")
        st.divider()
        st.markdown("### Analysis modules")
        st.markdown("**◈ Overview**  \n**◇ 3D Structure**  \n**⌁ Sequence**  \n**⊙ Domains & Sites**  \n**✣ PTM / Modifications**  \n**⑂ Mutations**  \n**△ Physicochemical**  \n**⌁ Ramachandran**  \n**⇄ Comparison**")
        st.divider()
        st.markdown("### Data")
        st.caption("UniProt · AlphaFold DB · Biopython")
        st.caption("Protein Explorer 3.0 · educational use")
