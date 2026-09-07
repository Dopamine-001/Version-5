from __future__ import annotations

import sys
import pathlib

# Ensure root directory is in path so top-level packages resolve reliably
ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import streamlit.components.v1 as components

from core.alphafold import calculate_plddt, get_alphafold_structure
from core.uniprot import normalize_uniprot_record, search_uniprot
from ..analysis.sequence_analysis import sequence_properties
from viewer.py3d_viewer import render_structure


def esc(text: str) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def show_comparison(*args, **kwargs) -> None:
    """
    Flexible comparison handler supporting two invocation styles:
    1. show_comparison((query1, query2)) from the landing page.
    2. show_comparison(p1, sequence1, properties1, pdb1, plddt1, query2) from a protein workspace.
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)) and len(args[0]) == 2:
        query1, query2 = args[0]
        
        with st.spinner("Searching UniProt for comparison targets..."):
            record1 = search_uniprot(query1)
            record2 = search_uniprot(query2)

        if not record1:
            st.error(f"Could not find a protein matching '{query1}'.")
            return
        if not record2:
            st.error(f"Could not find a protein matching '{query2}'.")
            return

        p1 = normalize_uniprot_record(record1)
        sequence1 = p1["sequence"]
        if not sequence1:
            st.error(f"No sequence data available for '{query1}'.")
            return

        p2 = normalize_uniprot_record(record2)
        sequence2 = p2["sequence"]
        if not sequence2:
            st.error(f"No sequence data available for '{query2}'.")
            return

        with st.spinner("Fetching AlphaFold structures..."):
            pdb1, _ = get_alphafold_structure(p1["accession"])
            pdb2, _ = get_alphafold_structure(p2["accession"])

        properties1 = sequence_properties(sequence1)
        properties2 = sequence_properties(sequence2)
        plddt1 = calculate_plddt(pdb1) if pdb1 else None
        plddt2 = calculate_plddt(pdb2) if pdb2 else None

    elif len(args) == 6:
        p1, sequence1, properties1, pdb1, plddt1, query2 = args
        
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
            pdb2, _ = get_alphafold_structure(p2["accession"])

        properties2 = sequence_properties(sequence2)
        plddt2 = calculate_plddt(pdb2) if pdb2 else None
    else:
        st.error("Invalid comparison parameters passed.")
        return

    st.markdown(
        f"""
        <div class="section-title">Comparative Analysis: {esc(p1['name'])} vs {esc(p2['name'])}</div>
        """,
        unsafe_allow_html=True,
    )

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


render_comparison = show_comparison
