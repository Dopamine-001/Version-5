"""
Landing page: hero banner plus the two entry points into the app —
exploring a single protein, or jumping straight into a two-protein
comparison. (Comparison is also reachable from inside a protein's own
tab bar; see views/protein_workspace.py's Comparison tab.)
"""

import streamlit as st

from views.comparison_workspace import show_comparison
from views.protein_workspace import show_protein


def render_landing() -> None:
    # Streamlit reruns the script whenever a widget changes. Keep the active
    # workspace in session state so changing a 3D representation does NOT
    # send the user back to the landing page.
    active_protein = st.session_state.get("active_protein_query")
    active_compare = st.session_state.get("active_compare_queries")

    if active_protein:
        if st.button("← Back to Protein Explorer", key="back_to_landing"):
            st.session_state.pop("active_protein_query", None)
            st.rerun()
        show_protein(active_protein)
        return

    if active_compare:
        if st.button("← Back to Protein Explorer", key="back_to_landing_compare"):
            st.session_state.pop("active_compare_queries", None)
            st.rerun()
        show_comparison(*active_compare)
        return

    st.markdown(
        """
        <div class="hero">
            <div class="kicker">Structural biology · Bioinformatics · Protein science</div>
            <div class="hero-title">Protein Explorer <span style="color:#43d9d0">3.0</span></div>
            <div class="hero-copy">
                A professional workspace for moving from amino-acid sequence to
                biochemical properties, predicted structure, hydrophobicity,
                variants, functional sites and structural analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Mode",
        ["Explore a protein", "Compare two proteins"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if mode == "Explore a protein":
        _render_explore_mode()
    else:
        _render_compare_mode()


def _render_explore_mode() -> None:
    search_col, button_col = st.columns([5, 1])
    with search_col:
        protein_query = st.text_input(
            "Protein, gene or UniProt accession",
            placeholder="Try: hemoglobin, insulin, TP53, P68871",
            label_visibility="collapsed",
            key="protein_search",
        )
    with button_col:
        explore = st.button("Explore", type="primary", use_container_width=True, key="explore_button")

    if explore and protein_query.strip():
        st.session_state["active_protein_query"] = protein_query.strip()
        st.rerun()

    st.markdown(
        """
        ### Start with a protein
        Enter a **protein name, gene symbol or UniProt accession** above.
        <div class="small-note">The workspace combines UniProt annotations, AlphaFold structure and sequence analysis in one place.</div>

        The workspace will retrieve the protein sequence and annotations from
        UniProt and, when available, its predicted structure from AlphaFold.
        """
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("#### 🧬 Sequence")
        st.caption("Composition, amino-acid properties, pI, molecular weight and primary structure.")
    with c2:
        st.markdown("#### 🧊 Structure")
        st.caption("Interactive AlphaFold model with cartoon, ribbon, stick, sphere, line and surface views.")
    with c3:
        st.markdown("#### 🧪 Analysis")
        st.caption("Hydrophobicity, variants, PTMs, domains, sites and Ramachandran analysis.")
    with c4:
        st.markdown("#### ⚖️ Comparison")
        st.caption("Switch to \"Compare two proteins\" above to line up two entries side by side.")

def _render_compare_mode() -> None:
    st.markdown(
        """
        ### Compare two proteins
        Enter **two** protein names, gene symbols or UniProt accessions to see
        their properties, hydrophobicity, composition and predicted structures side by side.
        """
    )
    c1, c2, c3 = st.columns([3, 3, 1])
    with c1:
        query1 = st.text_input("First protein", placeholder="e.g. hemoglobin subunit alpha")
    with c2:
        query2 = st.text_input("Second protein", placeholder="e.g. hemoglobin subunit beta")
    with c3:
        st.markdown("<div style='height:1.85rem'></div>", unsafe_allow_html=True)
        compare = st.button("Compare", type="primary", use_container_width=True)

    if compare and query1.strip() and query2.strip():
        st.session_state["active_compare_queries"] = (query1.strip(), query2.strip())
        st.rerun()
    elif compare:
        st.warning("Enter both proteins to run a comparison.")
