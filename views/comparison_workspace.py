from __future__ import annotations

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from analysis.sequence import sequence_properties
from core.alphafold import calculate_plddt, get_alphafold_structure
from core.helpers import esc
from core.uniprot import normalize_uniprot_record, search_uniprot
from viewer.structure_viewer import render_structure


def show_comparison(
    p1: dict,
    sequence1: str,
    properties1: dict,
    pdb1: str | None,
    plddt1: float | None,
    query2: str,
) -> None:
    """Fetches a second protein and renders a side-by-side comparison workspace."""
    with st.spinner(f"Searching UniProt for comparison target: '{query2}'..."):
        record2 = search_uniprot(query2)

    if not record2:
        st.error(f"Could not find a protein matching '{query2}'.")
        return

    p2 = normalize_uniprot_record(record2)
    sequence2 = p2["sequence"]

    if not sequence2:
        st.error("The comparison protein was found, but no sequence data was available.")
        return

    with st.spinner(f"Fetching AlphaFold structure for {p2['accession']}..."):
        pdb2, af_meta2 = get_alphafold_structure(p2["accession"])

    properties2 = sequence_properties(sequence2)
    plddt2 = calculate_plddt(pdb2) if pdb2 else None

    st.markdown(
        f"""
        <div class="section-title">Comparative Analysis: {esc(p1['name'])} vs {esc(p2['name'])}</div>
        """,
        unsafe_allow_html=True,
    )

    # Side-by-side metrics table
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### Protein 1: {esc(p1['accession'])}")
        st.write(f"**Name:** {p1['name']}")
        st.write(f"**Gene:** {p1['gene']}")
        st.write(f"**Organism:** {p1['organism']}")
        st.metric("Length", f"{p1['length']} aa")
        st.metric("Molecular Weight", f"{properties1['molecular_weight'] / 1000:.2f} kDa")
        st.metric("Theoretical pI", f"{properties1['pI']:.2f}")
        st.metric("GRAVY", f"{properties1['gravy']:.2f}")
        st.metric("Mean pLDDT", f"{plddt1:.1f}" if plddt1 is not None else "N/A")

    with col2:
        st.markdown(f"### Protein 2: {esc(p2['accession'])}")
        st.write(f"**Name:** {p2['name']}")
        st.write(f"**Gene:** {p2['gene']}")
        st.write(f"**Organism:** {p2['organism']}")
        st.metric("Length", f"{p2['length']} aa")
        st.metric("Molecular Weight", f"{properties2['molecular_weight'] / 1000:.2f} kDa")
        st.metric("Theoretical pI", f"{properties2['pI']:.2f}")
        st.metric("GRAVY", f"{properties2['gravy']:.2f}")
        st.metric("Mean pLDDT", f"{plddt2:.1f}" if plddt2 is not None else "N/A")

    st.markdown("---")
    st.markdown('<div class="section-title">Side-by-Side 3D Structural Comparison</div>', unsafe_allow_html=True)

    view_col1, view_col2 = st.columns(2)

    with view_col1:
        st.subheader(f"3D Structure: {p1['accession']}")
        if pdb1:
            html1 = render_structure(pdb1, representation="Cartoon", color_style="Spectrum")
            components.html(html1, height=450, scrolling=False)
        else:
            st.info("No structure available for Protein 1.")

    with view_col2:
        st.subheader(f"3D Structure: {p2['accession']}")
        if pdb2:
            html2 = render_structure(pdb2, representation="Cartoon", color_style="Spectrum")
            components.html(html2, height=450, scrolling=False)
        else:
            st.info("No structure available for Protein 2.")
