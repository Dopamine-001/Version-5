"""
The main single-protein workspace: fetches UniProt + AlphaFold data for one
query and renders the header metrics plus all ten analysis tabs. Each tab's
content is delegated to the relevant analysis/charts/viewer module — this
file is mostly Streamlit layout glue.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from core.ncbi import fetch_cds_nucleotide_sequence
from analysis.structure import secondary_structure_with_fallback
from viewer.structure_viewer import render_secondary_structure_3d

from analysis.sequence import hydrophobicity_table, sequence_properties
from analysis.structure import calculate_ramachandran_angles
from analysis.variants import (
    feature_dataframe,
    mutation_interpretation,
    parse_mutation_input,
    variants_dataframe,
)
from charts.sequence_charts import composition_figure, hydrophobicity_figure
from charts.structure_charts import plddt_figure, ramachandran_figure
from config import AA_GROUPS, KYTEL_DOOLITTLE
from core.alphafold import (
    calculate_plddt,
    get_alphafold_structure,
    structure_chain_count,
)
from core.helpers import esc
from core.ncbi import get_ncbi_gene_info
from core.disprot import get_disprot_regions
from core.uniprot import normalize_uniprot_record, search_uniprot
from viewer.structure_viewer import render_structure
from views.comparison_workspace import render_comparison


# ============================================================
# MAIN PROTEIN WORKSPACE
# ============================================================

def show_protein(protein_query: str) -> None:
    with st.spinner("Searching UniProt and preparing the protein workspace..."):
        record = search_uniprot(protein_query)

    if not record:
        st.error(
            "Protein not found. Try a protein name, gene symbol, or UniProt accession."
        )
        return

    protein = normalize_uniprot_record(record)
    sequence = protein["sequence"]

    # NCBI information is retrieved using the gene symbol from UniProt.
    ncbi_info = get_ncbi_gene_info(protein["gene"])

    if not sequence:
        st.error("UniProt returned the entry, but no sequence was available.")
        return

    with st.spinner("Fetching AlphaFold structure..."):
        pdb_text, af_meta = get_alphafold_structure(protein["accession"])

    properties = sequence_properties(sequence)
    plddt = calculate_plddt(pdb_text) if pdb_text else None

    _render_header(protein, properties, plddt)

    # ========================================================
    # TEN ANALYSIS TABS
    # ========================================================

    tabs = st.tabs(
        [
            "Overview",
            "NCBI Gene",
            "Primary Structure",
            "3D Structure",
            "Hydrophobicity",
            "Mutations",
            "Domains & Sites",
            "PTMs",
            "Ramachandran",
            "Comparison",
        ]
    )

    with tabs[0]:
        _render_overview_tab(
            protein,
            properties,
            plddt,
            pdb_text,
            sequence,
        )

    with tabs[1]:
        _render_ncbi_tab(ncbi_info)

    with tabs[2]:
        _render_primary_structure_tab(
            protein,
            sequence,
        )

    with tabs[3]:
        _render_3d_structure_tab(
            protein,
            pdb_text,
            af_meta,
            plddt,
            sequence,
        )

    with tabs[4]:
        _render_hydrophobicity_tab(
            protein,
            sequence,
        )

    with tabs[5]:
        _render_mutations_tab(
            protein,
            sequence,
        )

    with tabs[6]:
        _render_domains_sites_tab(protein)

    with tabs[7]:
        _render_ptms_tab(protein)

    with tabs[8]:
        _render_ramachandran_tab(pdb_text)

    with tabs[9]:
        _render_comparison_tab(
            protein,
            sequence,
            properties,
            pdb_text,
            plddt,
        )


# ============================================================
# HEADER
# ============================================================

def _render_header(protein: dict, properties: dict, plddt) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="kicker">
                Protein workspace · {esc(protein['accession'])}
            </div>

            <div class="hero-title">
                {esc(protein['name'])}
            </div>

            <div class="hero-copy">
                {esc(protein['organism'])} · Gene: {esc(protein['gene'])}
                · UniProt: {esc(protein['accession'])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metrics = [
        (
            "Length",
            f"{protein['length']} aa",
            "UniProt sequence",
        ),
        (
            "Molecular weight",
            f"{properties['molecular_weight'] / 1000:.2f} kDa",
            "calculated",
        ),
        (
            "Theoretical pI",
            f"{properties['pI']:.2f}",
            "calculated",
        ),
        (
            "GRAVY",
            f"{properties['gravy']:.2f}",
            "Kyte-Doolittle",
        ),
        (
            "Instability",
            f"{properties['instability']:.1f}",
            "ProtParam index",
        ),
        (
            "Mean pLDDT",
            f"{plddt:.1f}" if plddt is not None else "N/A",
            "AlphaFold",
        ),
    ]

    cols = st.columns(len(metrics))

    for col, (label, value, sub) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{esc(label)}</div>
                    <div class="metric-value">{esc(value)}</div>
                    <div class="metric-sub">{esc(sub)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="margin-top:.75rem">'
        '<span class="source-badge">UniProt</span>'
        '<span class="source-badge">AlphaFold DB</span>'
        '<span class="source-badge">NCBI</span>'
        '<span class="source-badge">Sequence analysis</span>'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# OVERVIEW TAB
# ============================================================

def _render_overview_tab(
    protein: dict,
    properties: dict,
    plddt,
    pdb_text,
    sequence: str,
) -> None:

    left, right = st.columns([1.25, 1])

    # --------------------------------------------------------
    # Biological identity
    # --------------------------------------------------------

    with left:
        st.markdown(
            '<div class="section-title">Biological identity</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown(
                f"**Function**  \n{protein['function']}"
            )

            st.markdown(
                f"**Subcellular location**  \n{protein['location']}"
            )

            st.markdown(
                f"**Catalytic activity**  \n{protein['catalytic_activity']}"
            )

            st.markdown(
                f"**Disease associations**  \n{protein['disease']}"
            )

            if protein["keywords"]:
                st.markdown("**Keywords**")
                st.write(", ".join(protein["keywords"]))

            st.markdown("**Protein interactions**")

            if protein["interactions"]:
                interaction_df = pd.DataFrame(
                    protein["interactions"]
                )

                st.dataframe(
                    interaction_df.head(12),
                    use_container_width=True,
                    hide_index=True,
                )

            else:
                st.caption(
                    "No interaction annotations were returned for this entry."
                )

    # --------------------------------------------------------
    # Protein chemistry
    # --------------------------------------------------------

    with right:
        st.markdown(
            '<div class="section-title">Protein chemistry</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.write(
                f"**Aromaticity:** "
                f"{properties['aromaticity']:.3f}"
            )

            st.write(
                f"**Charge at pH 7:** "
                f"{properties['charge']:.2f}"
            )

            st.write(
                f"**Instability index:** "
                f"{properties['instability']:.2f}"
            )

            st.write(
                f"**Mean residue hydropathy (GRAVY):** "
                f"{properties['gravy']:.3f}"
            )

            if plddt is not None:
                if plddt >= 90:
                    label = "Very high confidence"
                elif plddt >= 70:
                    label = "High confidence"
                elif plddt >= 50:
                    label = "Low confidence"
                else:
                    label = "Very low confidence"

                st.write(
                    f"**AlphaFold confidence:** {label}"
                )

    # --------------------------------------------------------
    # Four levels of protein structure
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Four levels of protein structure</div>',
        unsafe_allow_html=True,
    )

    levels = [
        (
            "Primary",
            f"{protein['length']} amino acids in the UniProt sequence.",
        ),
        (
            "Secondary",
            "Local backbone organization such as α-helices and β-sheets.",
        ),
        (
            "Tertiary",
            "The complete three-dimensional fold represented by "
            "the AlphaFold model when available.",
        ),
        (
            "Quaternary",
            (
                f"{structure_chain_count(pdb_text)} chain(s) are present "
                "in the supplied AlphaFold PDB."
                if pdb_text
                else
                "Assembly information is not available from the AlphaFold model."
            ),
        ),
    ]

    level_cols = st.columns(4)

    for col, (title, description) in zip(level_cols, levels):
        with col:
            st.markdown(f"**{title}**")
            st.caption(description)

    # --------------------------------------------------------
    # Amino-acid composition
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Amino-acid composition</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1.3, 1])

    with c1:
        st.plotly_chart(
            composition_figure(sequence),
            use_container_width=True,
        )

    with c2:
        groups = {}

        for group, aas in AA_GROUPS.items():
            groups[group] = sum(
                sequence.count(aa)
                for aa in aas
            )

        group_df = pd.DataFrame(
            {
                "Class": list(groups),
                "Count": list(groups.values()),
            }
        )

        st.dataframe(
            group_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# NCBI GENE TAB
# ============================================================

def _render_ncbi_tab(ncbi_info) -> None:
    """
    Render NCBI Gene information.

    The function is deliberately defensive because the exact set of fields
    returned by core.ncbi can vary depending on what NCBI returns for a gene.
    """

    st.markdown(
        '<div class="section-title">NCBI Gene information</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Gene-level information retrieved from NCBI using the UniProt gene symbol."
    )

    if not ncbi_info:
        st.info(
            "No NCBI Gene information was returned for this protein."
        )
        return

    # If the NCBI module returned something other than a dictionary,
    # display it safely instead of crashing the application.
    if not isinstance(ncbi_info, dict):
        st.write(ncbi_info)
        return

    # --------------------------------------------------------
    # Common NCBI fields
    # --------------------------------------------------------

    gene_id = (
        ncbi_info.get("gene_id")
        or ncbi_info.get("geneId")
        or ncbi_info.get("uid")
        or ncbi_info.get("id")
    )

    gene_symbol = (
        ncbi_info.get("gene")
        or ncbi_info.get("symbol")
        or ncbi_info.get("gene_symbol")
        or ncbi_info.get("geneSymbol")
    )

    description = (
        ncbi_info.get("description")
        or ncbi_info.get("gene_description")
        or ncbi_info.get("summary")
    )

    organism = (
        ncbi_info.get("organism")
        or ncbi_info.get("organism_name")
        or ncbi_info.get("scientific_name")
    )

    chromosome = (
        ncbi_info.get("chromosome")
        or ncbi_info.get("chr")
    )

    location = (
        ncbi_info.get("location")
        or ncbi_info.get("map_location")
        or ncbi_info.get("genomic_location")
    )

    aliases = (
        ncbi_info.get("aliases")
        or ncbi_info.get("synonyms")
        or ncbi_info.get("other_aliases")
    )

    summary = (
        ncbi_info.get("summary")
        or ncbi_info.get("function")
    )

    # --------------------------------------------------------
    # Main gene card
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Gene identity</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "NCBI Gene ID",
                str(gene_id) if gene_id else "N/A",
            )

        with c2:
            st.metric(
                "Gene symbol",
                str(gene_symbol) if gene_symbol else "N/A",
            )

        with c3:
            st.metric(
                "Chromosome",
                str(chromosome) if chromosome else "N/A",
            )

        if organism:
            st.markdown(
                f"**Organism**  \n{organism}"
            )

        if location:
            st.markdown(
                f"**Genomic location**  \n{location}"
            )

        if description:
            st.markdown(
                f"**Description**  \n{description}"
            )

    # --------------------------------------------------------
    # Gene aliases
    # --------------------------------------------------------

    if aliases:
        st.markdown(
            '<div class="section-title">Gene aliases / synonyms</div>',
            unsafe_allow_html=True,
        )

        if isinstance(aliases, (list, tuple, set)):
            st.write(", ".join(str(x) for x in aliases))
        else:
            st.write(str(aliases))

    # --------------------------------------------------------
    # Gene summary
    # --------------------------------------------------------

    if summary and summary != description:
        st.markdown(
            '<div class="section-title">NCBI summary</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.write(summary)

    # --------------------------------------------------------
    # Additional NCBI fields
    # --------------------------------------------------------

    known_labels = {
        "gene_id",
        "geneId",
        "uid",
        "id",
        "gene",
        "symbol",
        "gene_symbol",
        "geneSymbol",
        "description",
        "gene_description",
        "summary",
        "organism",
        "organism_name",
        "scientific_name",
        "chromosome",
        "chr",
        "location",
        "map_location",
        "genomic_location",
        "aliases",
        "synonyms",
        "other_aliases",
    }

    additional = {
        key: value
        for key, value in ncbi_info.items()
        if key not in known_labels
        and value not in (None, "", [], {})
    }

    if additional:
        st.markdown(
            '<div class="section-title">Additional NCBI information</div>',
            unsafe_allow_html=True,
        )

        rows = []

        for key, value in additional.items():
            if isinstance(value, (list, tuple, set)):
                value = ", ".join(
                    str(item) for item in value
                )

            elif isinstance(value, dict):
                value = str(value)

            rows.append(
                {
                    "Field": str(key),
                    "Value": str(value),
                }
            )

        if rows:
            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# PRIMARY STRUCTURE TAB
# ============================================================

def _render_primary_structure_tab(
    protein: dict,
    sequence: str,
) -> None:
    with st.expander("🧬 View Coding DNA / Nucleotide Sequence (CDS)", expanded=False):
        nuc_info = fetch_cds_nucleotide_sequence(protein)

        if nuc_info["sequence"]:
            c1, c2, c3 = st.columns(3)
            c1.metric("Nucleotide Length", f"{nuc_info['length']} bp")
            c2.metric("GC Content", f"{nuc_info['gc_content']}%")
            c3.metric("NCBI Accession", nuc_info["accession"])

            st.caption(f"**Record:** {nuc_info['description']}")
            st.text_area(
                "FASTA Sequence",
                f">{nuc_info['accession']} CDS\n{nuc_info['sequence']}",
                height=180,
            )
            st.download_button(
                "Download Nucleotide FASTA",
                data=f">{nuc_info['accession']}\n{nuc_info['sequence']}",
                file_name=f"{nuc_info['accession']}_cds.fasta",
                mime="text/plain",
            )
        else:
            st.info(
                "No directly linked CDS/nucleotide accession found in "
                "cross-references for this record."
            )

    st.markdown(
        '<div class="section-title">Primary structure</div>',
        unsafe_allow_html=True,
    )

    fasta = (
        f">{protein['accession']}|{protein['name']}\n"
        f"{sequence}"
    )

    st.download_button(
        "Download FASTA",
        data=fasta,
        file_name=f"{protein['accession']}.fasta",
        mime="text/plain",
        key=f"fasta_{protein['accession']}",
    )

    st.caption(
        "The amino-acid sequence is retrieved directly from UniProt."
    )

    st.code(
        sequence,
        language="text",
    )

    seq_df = pd.DataFrame(
        {
            "Position": range(
                1,
                len(sequence) + 1,
            ),
            "Residue": list(sequence),
            "Hydropathy": [
                KYTEL_DOOLITTLE[a]
                for a in sequence
            ],
        }
    )

    st.dataframe(
        seq_df,
        use_container_width=True,
        height=420,
        hide_index=True,
    )


# ============================================================
# 3D STRUCTURE TAB
# ============================================================

def _render_3d_structure_tab(
    protein: dict,
    pdb_text,
    af_meta: dict,
    plddt,
    sequence: str,
) -> None:
    if not pdb_text:
        st.warning("No AlphaFold prediction was returned for this accession.")
        return

    acc = protein["accession"]

    view_mode = st.radio(
        "Structure view",
        ["Main 3D structure", "Secondary structure"],
        horizontal=True,
        key=f"view_mode_{acc}",
        help=(
            "Switch between the configurable atom/fold viewer and the "
            "secondary-structure colour map."
        ),
    )

    # ------------------------------------------------------------------
    # SECONDARY STRUCTURE VIEW
    # ------------------------------------------------------------------
    if view_mode == "Secondary structure":
        st.markdown(
            '<div class="section-title">Secondary structure map</div>',
            unsafe_allow_html=True,
        )

        sec_struct = secondary_structure_with_fallback(protein, pdb_text)

        col_h, col_s, col_t, col_l = st.columns(4)
        col_h.markdown("🔴 **α-Helices** &nbsp;`#FF2A6D`", unsafe_allow_html=True)
        col_s.markdown("🔵 **β-Sheets** &nbsp;`#05D9E8`", unsafe_allow_html=True)
        col_t.markdown("🟡 **Turns** &nbsp;`#FFB703`", unsafe_allow_html=True)
        col_l.markdown("⚪ **Coils / loops** &nbsp;`#8FA3BF`", unsafe_allow_html=True)

        opt1, opt2 = st.columns(2)
        ss_spin = opt1.toggle("Spin structure", value=False, key=f"ss_spin_{acc}")
        show_coils = opt2.toggle("Show coils", value=True, key=f"ss_coils_{acc}")

        components.html(
            render_secondary_structure_3d(
                pdb_text,
                sec_struct,
                height=560,
                spin=ss_spin,
                show_coils=show_coils,
            ),
            height=580,
            scrolling=False,
        )

        helix_res = sum(h["end"] - h["start"] + 1 for h in sec_struct["helices"])
        sheet_res = sum(x["end"] - x["start"] + 1 for x in sec_struct["sheets"])
        total = len(sequence) or 1

        m1, m2, m3 = st.columns(3)
        m1.metric("α-Helix residues", f"{helix_res} ({helix_res / total:.0%})")
        m2.metric("β-Strand residues", f"{sheet_res} ({sheet_res / total:.0%})")
        m3.metric("Elements", f"{len(sec_struct['helices'])} H / {len(sec_struct['sheets'])} E")

        if sec_struct.get("source") == "geometry":
            st.caption(
                "UniProt has no experimental helix/strand annotation for this "
                "entry, so elements were assigned from the AlphaFold model's "
                "backbone phi-psi angles."
            )
        else:
            st.caption("Elements taken from UniProt experimental annotations.")

        return

    # ------------------------------------------------------------------
    # MAIN 3D STRUCTURE VIEW
    # ------------------------------------------------------------------
    st.markdown(
        '<div class="section-title">Interactive AlphaFold structure</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Drag to rotate, scroll to zoom, and use the controls below to "
        "switch between atom-level and fold-level representations. "
        "AlphaFold is a prediction; pLDDT describes local model confidence."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        representation = st.selectbox(
            "Representation",
            [
                "Stick",
                "Sphere",
                "Cartoon",
                "Ribbon",
                "Line",
                "Surface",
            ],
            index=0,
            key=f"repr_v3_{protein['accession']}",
        )

    with c2:
        color_style = st.selectbox(
            "Color by",
            [
                "Spectrum",
                "Chain",
                "Secondary structure",
                "Uniform",
            ],
            key=f"color_{protein['accession']}",
        )

    with c3:
        highlight_mode = st.selectbox(
            "Highlight style",
            [
                "Stick",
                "Sphere",
            ],
            key=f"highlight_{protein['accession']}",
        )

    with c4:
        spin = st.toggle(
            "Spin structure",
            value=False,
            key=f"spin_{protein['accession']}",
        )

    camera = st.selectbox(
        "Orientation",
        [
            "Default",
            "Front",
            "Side",
            "Top",
        ],
        key=f"camera_v3_{protein['accession']}",
        help="Rotate the fitted model to inspect it from another orientation.",
    )

    mutation_pos = st.number_input(
        "Highlight residue position (optional)",
        min_value=1,
        max_value=len(sequence),
        value=None,
        step=1,
        key=f"highlight_pos_{protein['accession']}",
    )

    html = render_structure(
        pdb_text,
        representation=representation,
        color_style=color_style,
        spin=spin,
        highlight_position=(
            int(mutation_pos)
            if mutation_pos
            else None
        ),
        highlight_mode=highlight_mode,
        camera=camera,
    )

    components.html(
        html,
        height=590,
        scrolling=False,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Chains",
        structure_chain_count(pdb_text),
    )

    c2.metric(
        "Mean pLDDT",
        f"{plddt:.1f}" if plddt is not None else "N/A",
    )

    c3.metric(
        "AlphaFold model",
        af_meta.get(
            "entryId",
            "Prediction",
        ),
    )

    plddt_chart = plddt_figure(pdb_text)

    if plddt_chart:
        st.plotly_chart(
            plddt_chart,
            use_container_width=True,
        )

    if af_meta:
        with st.expander("AlphaFold metadata"):
            c1, c2 = st.columns(2)

            with c1:
                if af_meta.get("entryId"):
                    st.markdown(
                        f"**Entry ID**  \n{af_meta['entryId']}"
                    )

                if af_meta.get("gene"):
                    st.markdown(
                        f"**Gene**  \n{af_meta['gene']}"
                    )

                if af_meta.get("latestVersion") is not None:
                    st.markdown(
                        f"**Latest Version**  \n"
                        f"{af_meta['latestVersion']}"
                    )

            with c2:
                if af_meta.get("organismScientificName"):
                    st.markdown(
                        f"**Organism**  \n"
                        f"{af_meta['organismScientificName']}"
                    )

                if af_meta.get("modelCreatedDate"):
                    st.markdown(
                        f"**Model Created**  \n"
                        f"{af_meta['modelCreatedDate']}"
                    )


# ============================================================
# HYDROPHOBICITY TAB
# ============================================================

def _render_hydrophobicity_tab(
    protein: dict,
    sequence: str,
) -> None:

    st.markdown(
        '<div class="section-title">Hydrophobicity analysis</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Kyte-Doolittle scale: positive values indicate greater "
        "hydrophobic character; negative values indicate hydrophilic character."
    )

    window = st.slider(
        "Moving-average window",
        3,
        21,
        9,
        step=2,
        key=f"hydro_{protein['accession']}",
    )

    st.plotly_chart(
        hydrophobicity_figure(
            sequence,
            window,
        ),
        use_container_width=True,
    )

    hydro = hydrophobicity_table(sequence)

    high = hydro[
        hydro["Kyte-Doolittle"] >= 1.6
    ]

    low = hydro[
        hydro["Kyte-Doolittle"] <= -1.6
    ]

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            "**Hydrophobic residues / regions**"
        )

        st.dataframe(
            high.head(100),
            use_container_width=True,
            hide_index=True,
        )

    with c2:
        st.markdown(
            "**Hydrophilic residues / regions**"
        )

        st.dataframe(
            low.head(100),
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# MUTATIONS TAB
# ============================================================

def _render_mutations_tab(
    protein: dict,
    sequence: str,
) -> None:

    st.markdown(
        '<div class="section-title">Mutations & variants</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Known variants below are UniProt annotations. The manual mutation "
        "tool only performs sequence-level chemical comparisons; it does "
        "not predict pathogenicity."
    )

    known = variants_dataframe(
        protein["variants"]
    )

    if known.empty:
        st.info(
            "No UniProt VARIANT features were returned for this entry."
        )
    else:
        st.dataframe(
            known,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown(
        "#### Inspect a mutation"
    )

    mutation_text = st.text_input(
        "Mutation notation",
        placeholder="Examples: V6E, 6V>E, Val6Glu",
        key=f"mutation_{protein['accession']}",
    )

    if not mutation_text:
        return

    pos, old_input, new = parse_mutation_input(
        mutation_text
    )

    if pos is None:
        st.warning(
            "Use a simple form such as V6E or 6V>E."
        )
        return

    result = mutation_interpretation(
        sequence,
        pos,
        new,
    )

    if not result["valid"]:
        st.error(
            result["message"]
        )
        return

    actual = result["old"]

    if old_input and old_input != actual:
        st.warning(
            f"The sequence contains **{actual}{pos}**, not "
            f"**{old_input}{pos}**. The analysis below uses the "
            "actual UniProt sequence."
        )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Reference residue",
        f"{actual}{pos}",
    )

    c2.metric(
        "New residue",
        new,
    )

    c3.metric(
        "Hydropathy change",
        f"{result['hydrophobicity_change']:+.2f}",
    )

    if result["same"]:
        st.info(
            "The requested substitution does not change the residue."
        )
    else:
        st.write(
            "This is a **sequence-level interpretation only**. "
            "A real functional effect depends on structural context, "
            "conservation, interactions, dynamics and experimental evidence."
        )


# ============================================================
# DOMAINS & SITES TAB
# ============================================================

def _render_domains_sites_tab(
    protein: dict,
) -> None:

    st.markdown(
        '<div class="section-title">Domains, motifs & functional sites</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Position-specific annotations are read from the UniProt feature "
        "table. Coverage varies between proteins."
    )

    domain_df = feature_dataframe(
        protein.get("domains", [])
    )

    site_df = feature_dataframe(
        protein.get("sites", [])
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            "**Domains, regions & motifs**"
        )

        if domain_df.empty:
            st.info(
                "No domain-like annotations were returned for this entry."
            )
        else:
            st.dataframe(
                domain_df,
                use_container_width=True,
                hide_index=True,
                height=330,
            )

    with c2:
        st.markdown(
            "**Active, binding & functional sites**"
        )

        if site_df.empty:
            st.info(
                "No site annotations were returned for this entry."
            )
        else:
            st.dataframe(
                site_df,
                use_container_width=True,
                hide_index=True,
                height=330,
            )

    if not domain_df.empty or not site_df.empty:
        st.success(
            f"Loaded {len(domain_df)} domain/region annotations "
            f"and {len(site_df)} site annotations from UniProt."
        )

    elif protein.get("all_features"):
        st.markdown(
            "**Other UniProt sequence annotations**"
        )

        st.dataframe(
            feature_dataframe(
                protein["all_features"]
            ),
            use_container_width=True,
            hide_index=True,
            height=260,
        )

    if protein.get("pdb_refs"):
        st.markdown(
            "**Cross-referenced PDB structures**"
        )

        st.write(
            " · ".join(
                protein["pdb_refs"][:40]
            )
        )


# ============================================================
# PTM TAB
# ============================================================

def _render_ptms_tab(
    protein: dict,
) -> None:

    st.markdown(
        '<div class="section-title">'
        'Post-translational modifications & processing'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Modified residues, glycosylation, lipidation, cross-links and "
        "processing events are read from UniProt feature annotations."
    )

    ptm_df = feature_dataframe(
        protein.get("ptms", [])
    )

    if ptm_df.empty:
        st.info(
            "No PTM/processing feature annotations were returned for this entry."
        )
        return

    st.dataframe(
        ptm_df,
        use_container_width=True,
        hide_index=True,
        height=430,
    )

    st.success(
        f"Loaded {len(ptm_df)} PTM/processing annotations from UniProt."
    )


# ============================================================
# RAMACHANDRAN TAB
# ============================================================

def _render_ramachandran_tab(
    pdb_text,
) -> None:

    st.markdown(
        '<div class="section-title">Ramachandran analysis</div>',
        unsafe_allow_html=True,
    )

    if not pdb_text:
        st.info(
            "A PDB structure is required for backbone-angle analysis."
        )
        return

    try:
        phi, psi, residue_numbers = calculate_ramachandran_angles(
            pdb_text
        )

        if phi:
            st.plotly_chart(
                ramachandran_figure(
                    phi,
                    psi,
                    residue_numbers,
                ),
                use_container_width=True,
            )

            st.caption(
                "Calculated from the supplied AlphaFold PDB using "
                "Biopython. "
                f"{len(phi)} residues had both φ and ψ angles available."
            )

        else:
            st.info(
                "No complete φ/ψ pairs were available."
            )

    except Exception as exc:
        st.warning(
            f"Ramachandran analysis could not be calculated: {exc}"
        )


# ============================================================
# COMPARISON TAB
# ============================================================

def _render_comparison_tab(
    protein: dict,
    sequence: str,
    properties: dict,
    pdb_text,
    plddt,
) -> None:

    st.markdown(
        '<div class="section-title">Compare with another protein</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Enter a second protein, gene symbol or UniProt accession to line "
        "it up against "
        f"**{esc(protein['accession'])}** on sequence identity, "
        "biochemistry, hydrophobicity, composition and predicted structure."
    )

    compare_col, button_col = st.columns(
        [4, 1]
    )

    with compare_col:
        compare_query = st.text_input(
            "Second protein",
            placeholder="e.g. hemoglobin subunit beta, TP63, P68871",
            key=f"compare_query_{protein['accession']}",
        )

    with button_col:
        st.markdown(
            "<div style='height:1.7rem'></div>",
            unsafe_allow_html=True,
        )

        run_compare = st.button(
            "Compare",
            type="primary",
            use_container_width=True,
            key=f"compare_btn_{protein['accession']}",
        )

    if run_compare and compare_query.strip():

        render_comparison(
            p1=protein,
            sequence1=sequence,
            properties1=properties,
            pdb1=pdb_text,
            plddt1=plddt,
            query2=compare_query.strip(),
        )

    elif run_compare:

        st.warning(
            "Enter a second protein to compare against."
        )
