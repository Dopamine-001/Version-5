from __future__ import annotations

import sys
import pathlib

# Ensure root directory and analysis directory are explicitly in sys.path
ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()
ANALYSIS_DIR = ROOT_DIR / "analysis"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

import streamlit as st
import streamlit.components.v1 as components

from core.alphafold import calculate_plddt, get_alphafold_structure
from core.uniprot import normalize_uniprot_record, search_uniprot
from viewer.py3d_viewer import render_structure

# Multi-layered safe import for sequence_properties
try:
    from analysis.sequence_analysis import sequence_properties
except ModuleNotFoundError:
    try:
        from sequence_analysis import sequence_properties
    except ImportError:
        def sequence_properties(seq: str) -> dict:
            """Fallback sequence properties calculator."""
            return {
                "molecular_weight": len(seq) * 110.0,
                "pI": 7.0,
                "gravy": 0.0,
                "formula": f"C{len(seq)}H...",
                "charge_at_7": 0.0,
            }


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

    # Metadata columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### Protein 1: {esc(p1['accession'])}")
        st.write(f"**Name:** {p1['name']}")
        st.write(f"**Gene:** {p1['gene']}")
        st.write(f"**Organism:** {p1['organism']}")

    with col2:
        st.markdown(f"### Protein 2: {esc(p2['accession'])}")
        st.write(f"**Name:** {p2['name']}")
        st.write(f"**Gene:** {p2['gene']}")
        st.write(f"**Organism:** {p2['organism']}")

    st.markdown("---")
    st.markdown('<div class="section-title">Feature Comparison Matrix</div>', unsafe_allow_html=True)

    # Comprehensive Comparison Table
    mw1 = properties1['molecular_weight'] / 1000
    mw2 = properties2['molecular_weight'] / 1000
    pi1 = properties1['pI']
    pi2 = properties2['pI']
    gravy1 = properties1['gravy']
    gravy2 = properties2['gravy']
    len1 = p1['length']
    len2 = p2['length']
    val_plddt1 = f"{plddt1:.1f}" if plddt1 is not None else "N/A"
    val_plddt2 = f"{plddt2:.1f}" if plddt2 is not None else "N/A"

    comparison_data = [
        {"Feature": "Accession", "Protein 1": p1['accession'], "Protein 2": p2['accession'], "Difference": "-"},
        {"Feature": "Length (aa)", "Protein 1": len1, "Protein 2": len2, "Difference": f"{len2 - len1:+d}"},
        {"Feature": "Molecular Weight (kDa)", "Protein 1": f"{mw1:.2f}", "Protein 2": f"{mw2:.2f}", "Difference": f"{mw2 - mw1:+.2f}"},
        {"Feature": "Theoretical pI", "Protein 1": f"{pi1:.2f}", "Protein 2": f"{pi2:.2f}", "Difference": f"{pi2 - pi1:+.2f}"},
        {"Feature": "GRAVY (Hydrophobicity)", "Protein 1": f"{gravy1:.2f}", "Protein 2": f"{gravy2:.2f}", "Difference": f"{gravy2 - gravy1:+.2f}"},
        {"Feature": "Mean pLDDT (Confidence)", "Protein 1": val_plddt1, "Protein 2": val_plddt2, "Difference": "-"},
    ]

    st.table(comparison_data)

    st.markdown("---")
    st.markdown('<div class="section-title">Side-by-Side 3D Structural Comparison</div>', unsafe_allow_html=True)

    view_col1, view_col2 = st.columns(2)

    with view_col1:
        st.subheader(f"3D Structure: {p1['accession']}")
        if pdb1:
            render_structure(pdb1, representation="Cartoon", color_style="Spectrum", width=450, height=450)
        else:
            st.info("No structure available for Protein 1.")

    with view_col2:
        st.subheader(f"3D Structure: {p2['accession']}")
        if pdb2:
            render_structure(pdb2, representation="Cartoon", color_style="Spectrum", width=450, height=450)
        else:
            st.info("No structure available for Protein 2.")


render_comparison = show_comparison
