"""
Protein-vs-protein comparison.

render_comparison() does the actual work and expects protein 1's data to
already be loaded (used by the Comparison tab inside protein_workspace, so
protein 1 isn't re-fetched). show_comparison() is the standalone entry
point used by the landing page's "Compare two proteins" mode — it fetches
both proteins fresh and then delegates to render_comparison().
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from analysis.comparison import align_sequences
from charts.comparison_charts import comparison_composition_figure, comparison_hydrophobicity_figure
from core.alphafold import calculate_plddt, get_alphafold_structure
from core.helpers import esc
from core.uniprot import normalize_uniprot_record, search_uniprot
from analysis.sequence import sequence_properties
from viewer.structure_viewer import render_structure


def render_comparison(
    p1: dict, sequence1: str, properties1: dict, pdb1: Optional[str], plddt1: Optional[float], query2: str,
) -> None:
    """Render a full comparison of an already-loaded protein against a second, freshly-fetched one."""
    with st.spinner(f"Retrieving '{query2}' from UniProt..."):
        record2 = search_uniprot(query2)

    if not record2:
        st.error(f"Could not find a reviewed UniProt entry for '{query2}'.")
        return

    p2 = normalize_uniprot_record(record2)
    if not p2["sequence"]:
        st.error(f"'{query2}' has no sequence available for comparison.")
        return

    with st.spinner("Fetching the second AlphaFold structure..."):
        pdb2, meta2 = get_alphafold_structure(p2["accession"])

    props2 = sequence_properties(p2["sequence"])
    plddt2 = calculate_plddt(pdb2) if pdb2 else None

    with st.spinner("Aligning sequences..."):
        alignment = align_sequences(sequence1, p2["sequence"])

    align_cols = st.columns(4)
    align_cols[0].metric("Sequence identity", f"{alignment['identity']}%")
    align_cols[1].metric("Aligned length", alignment["aligned_length"])
    align_cols[2].metric("Length difference", abs(p1["length"] - p2["length"]))
    align_cols[3].metric("Alignment score", f"{alignment['score']:.0f}")
    st.caption(
        "Global pairwise alignment (Biopython, BLOSUM62). Identity is the share of aligned "
        "columns with an exact residue match — a quick similarity signal, not a phylogenetic analysis."
    )

    st.markdown("**Side-by-side metrics**")
    comparison_rows = [
        ("Gene", p1["gene"], p2["gene"]),
        ("Organism", p1["organism"], p2["organism"]),
        ("Length (aa)", p1["length"], p2["length"]),
        ("Molecular weight (kDa)", f"{properties1['molecular_weight']/1000:.2f}", f"{props2['molecular_weight']/1000:.2f}"),
        ("Theoretical pI", f"{properties1['pI']:.2f}", f"{props2['pI']:.2f}"),
        ("GRAVY", f"{properties1['gravy']:.2f}", f"{props2['gravy']:.2f}"),
        ("Aromaticity", f"{properties1['aromaticity']:.3f}", f"{props2['aromaticity']:.3f}"),
        ("Instability index", f"{properties1['instability']:.1f}", f"{props2['instability']:.1f}"),
        ("Charge at pH 7", f"{properties1['charge']:.2f}", f"{props2['charge']:.2f}"),
        ("Mean pLDDT", f"{plddt1:.1f}" if plddt1 is not None else "N/A", f"{plddt2:.1f}" if plddt2 is not None else "N/A"),
        ("Subcellular location", p1["location"], p2["location"]),
        ("Domains/regions", len(p1["domains"]), len(p2["domains"])),
        ("Functional sites", len(p1["sites"]), len(p2["sites"])),
        ("PTM features", len(p1["ptms"]), len(p2["ptms"])),
        ("Known variants", len(p1["variants"]), len(p2["variants"])),
    ]
    comparison_df = pd.DataFrame(comparison_rows, columns=["Property", p1["accession"], p2["accession"]])
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    st.markdown("**Hydrophobicity overlay**")
    st.plotly_chart(
        comparison_hydrophobicity_figure(sequence1, p1["accession"], p2["sequence"], p2["accession"]),
        use_container_width=True,
    )

    st.markdown("**Amino-acid class composition**")
    st.plotly_chart(
        comparison_composition_figure(sequence1, p1["accession"], p2["sequence"], p2["accession"]),
        use_container_width=True,
    )

    st.markdown("**Predicted 3D structures**")
    struct_cols = st.columns(2)
    for col, (protein, pdb_text, plddt) in zip(
        struct_cols, [(p1, pdb1, plddt1), (p2, pdb2, plddt2)]
    ):
        with col:
            st.markdown(f"**{esc(protein['accession'])} — {esc(protein['name'])}**")
            if pdb_text:
                html = render_structure(pdb_text, representation="Cartoon", color_style="Spectrum")
                components.html(html, height=380, scrolling=False)
                st.caption(f"Mean pLDDT: {plddt:.1f}" if plddt is not None else "Mean pLDDT: N/A")
            else:
                st.info("No AlphaFold prediction available for this accession.")

    with st.expander("Functions, as annotated in UniProt"):
        fc1, fc2 = st.columns(2)
        fc1.markdown(f"**{esc(p1['accession'])}**  \n{p1['function']}")
        fc2.markdown(f"**{esc(p2['accession'])}**  \n{p2['function']}")


def show_comparison(query1: str, query2: str) -> None:
    with st.spinner("Retrieving the first protein from UniProt..."):
        record1 = search_uniprot(query1)

    if not record1:
        st.error(f"Could not find a reviewed UniProt entry for '{query1}'.")
        return

    p1 = normalize_uniprot_record(record1)
    if not p1["sequence"]:
        st.error(f"'{query1}' has no sequence available for comparison.")
        return

    with st.spinner("Fetching the first AlphaFold structure..."):
        pdb1, meta1 = get_alphafold_structure(p1["accession"])

    properties1 = sequence_properties(p1["sequence"])
    plddt1 = calculate_plddt(pdb1) if pdb1 else None

    st.markdown(
        f"""
        <div class="hero">
            <div class="kicker">Protein comparison</div>
            <div class="hero-title" style="font-size:2.3rem;">{esc(p1['name'])}</div>
            <div class="hero-copy">{esc(p1['accession'])} ({esc(p1['organism'])})</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_comparison(p1, p1["sequence"], properties1, pdb1, plddt1, query2)
