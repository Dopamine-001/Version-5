"""
Main single-protein workspace.

This module:
- searches UniProt;
- retrieves NCBI Gene information;
- retrieves AlphaFold structure data;
- renders protein-analysis tabs;
- retrieves CDS/nucleotide information;
- displays sequence, structure, mutation, PTM, BLAST, and comparison tools.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from analysis.sequence import (
    hydrophobicity_table,
    sequence_properties,
)
from analysis.structure import (
    calculate_ramachandran_angles,
    secondary_structure_with_fallback,
)
from analysis.variants import (
    feature_dataframe,
    mutation_interpretation,
    parse_mutation_input,
    variants_dataframe,
)
from charts.sequence_charts import (
    composition_figure,
    hydrophobicity_figure,
)
from charts.structure_charts import (
    plddt_figure,
    ramachandran_figure,
)
from config import AA_GROUPS, KYTEL_DOOLITTLE
from core.alphafold import (
    calculate_plddt,
    get_alphafold_structure,
    structure_chain_count,
)
from core.blast import run_blast_search
from core.disprot import get_disprot_regions
from core.helpers import esc
from core.ncbi import (
    fetch_cds_nucleotide_sequence,
    get_ncbi_gene_info,
)
from core.uniprot import (
    normalize_uniprot_record,
    search_uniprot,
)
from viewer.structure_viewer import (
    render_secondary_structure_3d,
    render_structure,
)
from views.comparison_workspace import render_comparison


# ============================================================
# Main workspace
# ============================================================

def show_protein(protein_query: str) -> None:
    """Search for a protein and render its complete workspace."""

    with st.spinner(
        "Searching UniProt and preparing the protein workspace..."
    ):
        record = search_uniprot(protein_query)

    if not record:
        st.error(
            "Protein not found. Try a protein name, gene symbol, "
            "or UniProt accession."
        )
        return

    protein = normalize_uniprot_record(record)

    # Preserve the original UniProt API response.
    # The CDS function may need the original cross-references.
    protein["_raw_uniprot_record"] = record

    sequence = protein.get("sequence", "")
    gene_symbol = protein.get("gene", "")

    if not sequence:
        st.error(
            "UniProt returned the entry, but no sequence was available."
        )
        return

    with st.spinner("Retrieving NCBI Gene information..."):
        ncbi_info = get_ncbi_gene_info(gene_symbol)

    with st.spinner("Fetching AlphaFold structure..."):
        pdb_text, alphafold_metadata = get_alphafold_structure(
            protein["accession"]
        )

    properties = sequence_properties(sequence)
    plddt = calculate_plddt(pdb_text) if pdb_text else None

    _render_header(
        protein=protein,
        properties=properties,
        plddt=plddt,
    )

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
            "BLAST Similarity",
            "Disorder (DisProt)",
            "Comparison",
        ]
    )

    with tabs[0]:
        _render_overview_tab(
            protein=protein,
            properties=properties,
            plddt=plddt,
            pdb_text=pdb_text,
            sequence=sequence,
        )

    with tabs[1]:
        _render_ncbi_tab(ncbi_info)

    with tabs[2]:
        _render_primary_structure_tab(
            protein=protein,
            sequence=sequence,
        )

    with tabs[3]:
        _render_3d_structure_tab(
            protein=protein,
            pdb_text=pdb_text,
            alphafold_metadata=alphafold_metadata,
            plddt=plddt,
            sequence=sequence,
        )

    with tabs[4]:
        _render_hydrophobicity_tab(
            protein=protein,
            sequence=sequence,
        )

    with tabs[5]:
        _render_mutations_tab(
            protein=protein,
            sequence=sequence,
        )

    with tabs[6]:
        _render_domains_sites_tab(protein)

    with tabs[7]:
        _render_ptms_tab(protein)

    with tabs[8]:
        _render_ramachandran_tab(pdb_text)

    with tabs[9]:
        _render_blast_tab(
            protein=protein,
            sequence=sequence,
        )

    with tabs[10]:
        _render_disorder_tab(protein)

    with tabs[11]:
        _render_comparison_tab(
            protein=protein,
            sequence=sequence,
            properties=properties,
            pdb_text=pdb_text,
            plddt=plddt,
        )


# ============================================================
# Header
# ============================================================

def _render_header(
    protein: dict,
    properties: dict,
    plddt: float | None,
) -> None:
    """Render the main protein header and metrics."""

    accession = protein.get("accession", "Unknown")
    name = protein.get("name", "Unknown protein")
    organism = protein.get("organism", "Unknown organism")
    gene = protein.get("gene", "Unknown")

    st.markdown(
        f"""
        <div class="hero">
            <div class="kicker">
                Protein workspace · {esc(accession)}
            </div>

            <div class="hero-title">
                {esc(name)}
            </div>

            <div class="hero-copy">
                {esc(organism)} · Gene: {esc(gene)}
                · UniProt: {esc(accession)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metrics = [
        (
            "Length",
            f"{protein.get('length', 0)} aa",
            "UniProt sequence",
        ),
        (
            "Molecular weight",
            f"{properties.get('molecular_weight', 0) / 1000:.2f} kDa",
            "Calculated",
        ),
        (
            "Theoretical pI",
            f"{properties.get('pI', 0):.2f}",
            "Calculated",
        ),
        (
            "GRAVY",
            f"{properties.get('gravy', 0):.2f}",
            "Kyte-Doolittle",
        ),
        (
            "Instability",
            f"{properties.get('instability', 0):.1f}",
            "ProtParam index",
        ),
        (
            "Mean pLDDT",
            f"{plddt:.1f}" if plddt is not None else "N/A",
            "AlphaFold",
        ),
    ]

    columns = st.columns(len(metrics))

    for column, (label, value, subtitle) in zip(
        columns,
        metrics,
    ):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        {esc(label)}
                    </div>
                    <div class="metric-value">
                        {esc(value)}
                    </div>
                    <div class="metric-sub">
                        {esc(subtitle)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div style="margin-top:.75rem">
            <span class="source-badge">UniProt</span>
            <span class="source-badge">AlphaFold DB</span>
            <span class="source-badge">NCBI</span>
            <span class="source-badge">Sequence analysis</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Overview tab
# ============================================================

def _render_overview_tab(
    protein: dict,
    properties: dict,
    plddt: float | None,
    pdb_text: str | None,
    sequence: str,
) -> None:
    """Render the overview tab."""

    left, right = st.columns([1.25, 1])

    with left:
        st.markdown(
            '<div class="section-title">Biological identity</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown(
                f"**Function**  \n"
                f"{protein.get('function', 'Not available')}"
            )

            st.markdown(
                f"**Subcellular location**  \n"
                f"{protein.get('location', 'Not available')}"
            )

            st.markdown(
                f"**Catalytic activity**  \n"
                f"{protein.get('catalytic_activity', 'Not available')}"
            )

            st.markdown(
                f"**Disease associations**  \n"
                f"{protein.get('disease', 'Not available')}"
            )

            keywords = protein.get("keywords", [])

            if keywords:
                st.markdown("**Keywords**")
                st.write(", ".join(str(item) for item in keywords))

            st.markdown("**Protein interactions**")

            interactions = protein.get("interactions", [])

            if interactions:
                st.dataframe(
                    pd.DataFrame(interactions).head(12),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.caption(
                    "No interaction annotations were returned."
                )

    with right:
        st.markdown(
            '<div class="section-title">Protein chemistry</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.write(
                f"**Aromaticity:** "
                f"{properties.get('aromaticity', 0):.3f}"
            )

            st.write(
                f"**Charge at pH 7:** "
                f"{properties.get('charge', 0):.2f}"
            )

            st.write(
                f"**Instability index:** "
                f"{properties.get('instability', 0):.2f}"
            )

            st.write(
                f"**Mean residue hydropathy (GRAVY):** "
                f"{properties.get('gravy', 0):.3f}"
            )

            if plddt is not None:
                st.write(
                    f"**AlphaFold confidence:** "
                    f"{_plddt_label(plddt)}"
                )

    st.markdown(
        '<div class="section-title">'
        "Four levels of protein structure"
        "</div>",
        unsafe_allow_html=True,
    )

    chain_text = (
        f"{structure_chain_count(pdb_text)} chain(s) are present "
        "in the AlphaFold model."
        if pdb_text
        else
        "Assembly information is not available."
    )

    levels = [
        (
            "Primary",
            f"{len(sequence)} amino acids in the UniProt sequence.",
        ),
        (
            "Secondary",
            "Local backbone organization such as α-helices "
            "and β-sheets.",
        ),
        (
            "Tertiary",
            "The complete three-dimensional fold represented "
            "by the AlphaFold model.",
        ),
        (
            "Quaternary",
            chain_text,
        ),
    ]

    columns = st.columns(4)

    for column, (title, description) in zip(columns, levels):
        with column:
            st.markdown(f"**{title}**")
            st.caption(description)

    st.markdown(
        '<div class="section-title">Amino-acid composition</div>',
        unsafe_allow_html=True,
    )

    chart_column, table_column = st.columns([1.3, 1])

    with chart_column:
        st.plotly_chart(
            composition_figure(sequence),
            use_container_width=True,
        )

    with table_column:
        groups = {
            group: sum(sequence.count(aa) for aa in amino_acids)
            for group, amino_acids in AA_GROUPS.items()
        }

        st.dataframe(
            pd.DataFrame(
                {
                    "Class": list(groups.keys()),
                    "Count": list(groups.values()),
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


def _plddt_label(plddt: float) -> str:
    """Convert pLDDT into a human-readable confidence label."""

    if plddt >= 90:
        return "Very high confidence"

    if plddt >= 70:
        return "High confidence"

    if plddt >= 50:
        return "Low confidence"

    return "Very low confidence"


# ============================================================
# NCBI Gene tab
# ============================================================

def _render_ncbi_tab(ncbi_info: dict | None) -> None:
    """Render NCBI Gene information defensively."""

    st.markdown(
        '<div class="section-title">NCBI Gene information</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Gene-level information retrieved from NCBI "
        "using the UniProt gene symbol."
    )

    if not ncbi_info:
        st.info("No NCBI Gene information was returned.")
        return

    if not isinstance(ncbi_info, dict):
        st.write(ncbi_info)
        return

    gene_id = _first_value(
        ncbi_info,
        "gene_id",
        "geneId",
        "uid",
        "id",
    )

    gene_symbol = _first_value(
        ncbi_info,
        "gene",
        "symbol",
        "gene_symbol",
        "geneSymbol",
    )

    description = _first_value(
        ncbi_info,
        "description",
        "gene_description",
        "summary",
    )

    organism = _first_value(
        ncbi_info,
        "organism",
        "organism_name",
        "scientific_name",
    )

    chromosome = _first_value(
        ncbi_info,
        "chromosome",
        "chr",
    )

    location = _first_value(
        ncbi_info,
        "location",
        "map_location",
        "genomic_location",
    )

    aliases = _first_value(
        ncbi_info,
        "aliases",
        "synonyms",
        "other_aliases",
    )

    summary = _first_value(
        ncbi_info,
        "summary",
        "function",
    )

    st.markdown(
        '<div class="section-title">Gene identity</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        column_1, column_2, column_3 = st.columns(3)

        column_1.metric(
            "NCBI Gene ID",
            str(gene_id) if gene_id else "N/A",
        )

        column_2.metric(
            "Gene symbol",
            str(gene_symbol) if gene_symbol else "N/A",
        )

        column_3.metric(
            "Chromosome",
            str(chromosome) if chromosome else "N/A",
        )

        if organism:
            st.markdown(f"**Organism**  \n{organism}")

        if location:
            st.markdown(f"**Genomic location**  \n{location}")

        if description:
            st.markdown(f"**Description**  \n{description}")

    if aliases:
        st.markdown(
            '<div class="section-title">Gene aliases / synonyms</div>',
            unsafe_allow_html=True,
        )

        if isinstance(aliases, (list, tuple, set)):
            st.write(", ".join(str(item) for item in aliases))
        else:
            st.write(str(aliases))

    if summary and summary != description:
        st.markdown(
            '<div class="section-title">NCBI summary</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.write(summary)

    known_fields = {
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

    additional_rows = []

    for key, value in ncbi_info.items():
        if key in known_fields:
            continue

        if value in (None, "", [], {}):
            continue

        if isinstance(value, (list, tuple, set)):
            value = ", ".join(str(item) for item in value)

        if isinstance(value, dict):
            value = str(value)

        additional_rows.append(
            {
                "Field": str(key),
                "Value": str(value),
            }
        )

    if additional_rows:
        st.markdown(
            '<div class="section-title">'
            "Additional NCBI information"
            "</div>",
            unsafe_allow_html=True,
        )

        st.dataframe(
            pd.DataFrame(additional_rows),
            use_container_width=True,
            hide_index=True,
        )


def _first_value(data: dict, *keys):
    """Return the first non-empty value from a dictionary."""

    for key in keys:
        value = data.get(key)

        if value not in (None, "", [], {}):
            return value

    return None


# ============================================================
# Primary structure tab
# ============================================================

def _render_primary_structure_tab(
    protein: dict,
    sequence: str,
) -> None:
    """Render CDS and amino-acid sequence information."""

    accession = protein.get("accession", "protein")
    raw_uniprot_record = protein.get(
        "_raw_uniprot_record",
        protein,
    )

    with st.expander(
        "🧬 View Coding DNA / Nucleotide Sequence (CDS)",
        expanded=False,
    ):
        with st.spinner("Retrieving CDS/nucleotide sequence..."):
            nucleotide_info = fetch_cds_nucleotide_sequence(
                raw_uniprot_record,
                gene_symbol=protein.get("gene"),
            )

        nucleotide_sequence = nucleotide_info.get(
            "sequence",
            "",
        )

        if nucleotide_sequence:
            _render_nucleotide_result(
                nucleotide_info=nucleotide_info,
                protein_accession=accession,
            )
        else:
            st.warning(
                nucleotide_info.get(
                    "error",
                    "No CDS or nucleotide sequence was found.",
                )
            )

    st.markdown(
        '<div class="section-title">Primary structure</div>',
        unsafe_allow_html=True,
    )

    protein_name = protein.get("name", "protein")

    fasta = (
        f">{accession}|{protein_name}\n"
        f"{sequence}"
    )

    st.download_button(
        "Download FASTA",
        data=fasta,
        file_name=f"{accession}.fasta",
        mime="text/plain",
        key=f"fasta_{accession}",
    )

    st.caption(
        "The amino-acid sequence was retrieved directly from UniProt."
    )

    st.code(sequence, language="text")

    hydropathy_values = [
        KYTEL_DOOLITTLE.get(amino_acid, 0.0)
        for amino_acid in sequence
    ]

    sequence_df = pd.DataFrame(
        {
            "Position": range(1, len(sequence) + 1),
            "Residue": list(sequence),
            "Hydropathy": hydropathy_values,
        }
    )

    st.dataframe(
        sequence_df,
        use_container_width=True,
        height=420,
        hide_index=True,
    )


def _render_nucleotide_result(
    nucleotide_info: dict,
    protein_accession: str,
) -> None:
    """Render a retrieved nucleotide sequence and download button."""

    accession = nucleotide_info.get(
        "accession",
        "nucleotide_sequence",
    )

    sequence = nucleotide_info.get("sequence", "")
    source = nucleotide_info.get("source", "Unknown")
    description = nucleotide_info.get(
        "description",
        "Nucleotide sequence",
    )

    column_1, column_2, column_3 = st.columns(3)

    column_1.metric(
        "Nucleotide Length",
        f"{nucleotide_info.get('length', len(sequence))} bp",
    )

    column_2.metric(
        "GC Content",
        f"{nucleotide_info.get('gc_content', 0.0)}%",
    )

    column_3.metric(
        "Source",
        str(source).replace("_", " ").title(),
    )

    st.caption(f"**Record:** {description}")

    fasta = f">{accession}\n{sequence}"

    st.text_area(
        "FASTA Sequence",
        fasta,
        height=180,
        key=f"nucleotide_text_{protein_accession}",
    )

    st.download_button(
        "Download Nucleotide FASTA",
        data=fasta,
        file_name=f"{accession}_cds.fasta",
        mime="text/plain",
        key=f"nucleotide_download_{protein_accession}",
    )


# ============================================================
# 3D structure tab
# ============================================================

def _render_3d_structure_tab(
    protein: dict,
    pdb_text: str | None,
    alphafold_metadata: dict,
    plddt: float | None,
    sequence: str,
) -> None:
    """Render the AlphaFold structure views."""

    if not pdb_text:
        st.warning(
            "No AlphaFold prediction was returned for this accession."
        )
        return

    accession = protein["accession"]

    view_mode = st.radio(
        "Structure view",
        [
            "Main 3D structure",
            "Secondary structure",
        ],
        horizontal=True,
        key=f"view_mode_{accession}",
    )

    if view_mode == "Secondary structure":
        _render_secondary_structure_view(
            protein=protein,
            pdb_text=pdb_text,
            sequence=sequence,
            accession=accession,
        )
        return

    _render_main_structure_view(
        protein=protein,
        pdb_text=pdb_text,
        alphafold_metadata=alphafold_metadata,
        plddt=plddt,
        sequence=sequence,
    )


def _render_secondary_structure_view(
    protein: dict,
    pdb_text: str,
    sequence: str,
    accession: str,
) -> None:
    """Render the secondary-structure viewer."""

    st.markdown(
        '<div class="section-title">Secondary structure map</div>',
        unsafe_allow_html=True,
    )

    secondary_structure = secondary_structure_with_fallback(
        protein,
        pdb_text,
    )

    column_1, column_2, column_3, column_4 = st.columns(4)

    column_1.markdown(
        "🔴 **α-Helices**",
    )
    column_2.markdown(
        "🔵 **β-Sheets**",
    )
    column_3.markdown(
        "🟡 **Turns**",
    )
    column_4.markdown(
        "⚪ **Coils / loops**",
    )

    option_1, option_2 = st.columns(2)

    spin = option_1.toggle(
        "Spin structure",
        value=False,
        key=f"secondary_spin_{accession}",
    )

    show_coils = option_2.toggle(
        "Show coils",
        value=True,
        key=f"secondary_coils_{accession}",
    )

    components.html(
        render_secondary_structure_3d(
            pdb_text,
            secondary_structure,
            height=560,
            spin=spin,
            show_coils=show_coils,
        ),
        height=580,
        scrolling=False,
    )

    helix_residues = sum(
        item["end"] - item["start"] + 1
        for item in secondary_structure.get("helices", [])
    )

    sheet_residues = sum(
        item["end"] - item["start"] + 1
        for item in secondary_structure.get("sheets", [])
    )

    total_residues = len(sequence) or 1

    column_1, column_2, column_3 = st.columns(3)

    column_1.metric(
        "α-Helix residues",
        f"{helix_residues} "
        f"({helix_residues / total_residues:.0%})",
    )

    column_2.metric(
        "β-Strand residues",
        f"{sheet_residues} "
        f"({sheet_residues / total_residues:.0%})",
    )

    column_3.metric(
        "Elements",
        f"{len(secondary_structure.get('helices', []))} H / "
        f"{len(secondary_structure.get('sheets', []))} E",
    )

    if secondary_structure.get("source") == "geometry":
        st.caption(
            "Elements were assigned from AlphaFold backbone geometry."
        )
    else:
        st.caption(
            "Elements were taken from UniProt annotations."
        )


def _render_main_structure_view(
    protein: dict,
    pdb_text: str,
    alphafold_metadata: dict,
    plddt: float | None,
    sequence: str,
) -> None:
    """Render the main interactive AlphaFold viewer."""

    accession = protein["accession"]

    st.markdown(
        '<div class="section-title">'
        "Interactive AlphaFold structure"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Drag to rotate, scroll to zoom, and use the controls to "
        "change the structure representation."
    )

    column_1, column_2, column_3, column_4 = st.columns(4)

    representation = column_1.selectbox(
        "Representation",
        [
            "Stick",
            "Sphere",
            "Cartoon",
            "Ribbon",
            "Line",
            "Surface",
        ],
        key=f"representation_{accession}",
    )

    color_style = column_2.selectbox(
        "Color by",
        [
            "Spectrum",
            "Chain",
            "Secondary structure",
            "Uniform",
        ],
        key=f"color_{accession}",
    )

    highlight_mode = column_3.selectbox(
        "Highlight style",
        [
            "Stick",
            "Sphere",
        ],
        key=f"highlight_mode_{accession}",
    )

    spin = column_4.toggle(
        "Spin structure",
        value=False,
        key=f"spin_{accession}",
    )

    camera = st.selectbox(
        "Orientation",
        [
            "Default",
            "Front",
            "Side",
            "Top",
        ],
        key=f"camera_{accession}",
    )

    residue_position = st.number_input(
        "Highlight residue position (optional)",
        min_value=1,
        max_value=len(sequence),
        value=None,
        step=1,
        key=f"highlight_position_{accession}",
    )

    structure_html = render_structure(
        pdb_text,
        representation=representation,
        color_style=color_style,
        spin=spin,
        highlight_position=(
            int(residue_position)
            if residue_position
            else None
        ),
        highlight_mode=highlight_mode,
        camera=camera,
    )

    components.html(
        structure_html,
        height=590,
        scrolling=False,
    )

    column_1, column_2, column_3 = st.columns(3)

    column_1.metric(
        "Chains",
        structure_chain_count(pdb_text),
    )

    column_2.metric(
        "Mean pLDDT",
        f"{plddt:.1f}" if plddt is not None else "N/A",
    )

    column_3.metric(
        "AlphaFold model",
        alphafold_metadata.get(
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

    if alphafold_metadata:
        with st.expander("AlphaFold metadata"):
            _render_alphafold_metadata(alphafold_metadata)


def _render_alphafold_metadata(metadata: dict) -> None:
    """Render AlphaFold metadata."""

    column_1, column_2 = st.columns(2)

    with column_1:
        if metadata.get("entryId"):
            st.markdown(
                f"**Entry ID**  \n{metadata['entryId']}"
            )

        if metadata.get("gene"):
            st.markdown(
                f"**Gene**  \n{metadata['gene']}"
            )

        if metadata.get("latestVersion") is not None:
            st.markdown(
                f"**Latest version**  \n"
                f"{metadata['latestVersion']}"
            )

    with column_2:
        if metadata.get("organismScientificName"):
            st.markdown(
                f"**Organism**  \n"
                f"{metadata['organismScientificName']}"
            )

        if metadata.get("modelCreatedDate"):
            st.markdown(
                f"**Model created**  \n"
                f"{metadata['modelCreatedDate']}"
            )


# ============================================================
# Hydrophobicity tab
# ============================================================

def _render_hydrophobicity_tab(
    protein: dict,
    sequence: str,
) -> None:
    """Render hydrophobicity analysis."""

    accession = protein["accession"]

    st.markdown(
        '<div class="section-title">'
        "Hydrophobicity analysis"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Positive Kyte-Doolittle values indicate greater hydrophobicity; "
        "negative values indicate hydrophilicity."
    )

    window = st.slider(
        "Moving-average window",
        min_value=3,
        max_value=21,
        value=9,
        step=2,
        key=f"hydrophobicity_window_{accession}",
    )

    st.plotly_chart(
        hydrophobicity_figure(sequence, window),
        use_container_width=True,
    )

    hydropathy = hydrophobicity_table(sequence)

    hydrophobic = hydropathy[
        hydropathy["Kyte-Doolittle"] >= 1.6
    ]

    hydrophilic = hydropathy[
        hydropathy["Kyte-Doolittle"] <= -1.6
    ]

    column_1, column_2 = st.columns(2)

    with column_1:
        st.markdown("**Hydrophobic residues / regions**")
        st.dataframe(
            hydrophobic.head(100),
            use_container_width=True,
            hide_index=True,
        )

    with column_2:
        st.markdown("**Hydrophilic residues / regions**")
        st.dataframe(
            hydrophilic.head(100),
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# Mutations tab
# ============================================================

def _render_mutations_tab(
    protein: dict,
    sequence: str,
) -> None:
    """Render known variants and manual mutation analysis."""

    accession = protein["accession"]

    st.markdown(
        '<div class="section-title">'
        "Mutations & variants"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Known variants are UniProt annotations. Manual mutation analysis "
        "only compares sequence-level properties."
    )

    known_variants = variants_dataframe(
        protein.get("variants", [])
    )

    if known_variants.empty:
        st.info(
            "No UniProt VARIANT features were returned."
        )
    else:
        st.dataframe(
            known_variants,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("#### Inspect a mutation")

    mutation_text = st.text_input(
        "Mutation notation",
        placeholder="Examples: V6E, 6V>E, Val6Glu",
        key=f"mutation_{accession}",
    )

    if not mutation_text:
        return

    position, old_residue, new_residue = parse_mutation_input(
        mutation_text
    )

    if position is None:
        st.warning(
            "Use a simple form such as V6E or 6V>E."
        )
        return

    result = mutation_interpretation(
        sequence,
        position,
        new_residue,
    )

    if not result["valid"]:
        st.error(result["message"])
        return

    actual_residue = result["old"]

    if old_residue and old_residue != actual_residue:
        st.warning(
            f"The sequence contains **{actual_residue}{position}**, "
            f"not **{old_residue}{position}**."
        )

    column_1, column_2, column_3 = st.columns(3)

    column_1.metric(
        "Reference residue",
        f"{actual_residue}{position}",
    )

    column_2.metric(
        "New residue",
        new_residue,
    )

    column_3.metric(
        "Hydropathy change",
        f"{result['hydrophobicity_change']:+.2f}",
    )

    if result["same"]:
        st.info(
            "The requested substitution does not change the residue."
        )
    else:
        st.write(
            "This is a sequence-level interpretation only. "
            "Functional effects require structural, conservation, "
            "interaction, and experimental evidence."
        )


# ============================================================
# Domains and sites tab
# ============================================================

def _render_domains_sites_tab(protein: dict) -> None:
    """Render domains, motifs, sites, and PDB references."""

    st.markdown(
        '<div class="section-title">'
        "Domains, motifs & functional sites"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Annotations are read from the UniProt feature table."
    )

    domain_df = feature_dataframe(
        protein.get("domains", [])
    )

    site_df = feature_dataframe(
        protein.get("sites", [])
    )

    column_1, column_2 = st.columns(2)

    with column_1:
        st.markdown("**Domains, regions & motifs**")

        if domain_df.empty:
            st.info("No domain annotations were returned.")
        else:
            st.dataframe(
                domain_df,
                use_container_width=True,
                hide_index=True,
                height=330,
            )

    with column_2:
        st.markdown("**Active, binding & functional sites**")

        if site_df.empty:
            st.info("No site annotations were returned.")
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
            f"and {len(site_df)} site annotations."
        )
    elif protein.get("all_features"):
        st.markdown("**Other UniProt sequence annotations**")

        st.dataframe(
            feature_dataframe(protein["all_features"]),
            use_container_width=True,
            hide_index=True,
            height=260,
        )

    pdb_references = protein.get("pdb_refs", [])

    if pdb_references:
        st.markdown("**Cross-referenced PDB structures**")
        st.write(" · ".join(pdb_references[:40]))


# ============================================================
# PTM tab
# ============================================================

def _render_ptms_tab(protein: dict) -> None:
    """Render post-translational modifications."""

    st.markdown(
        '<div class="section-title">'
        "Post-translational modifications & processing"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Modified residues, glycosylation, lipidation, cross-links, "
        "and processing events are read from UniProt annotations."
    )

    ptm_df = feature_dataframe(
        protein.get("ptms", [])
    )

    if ptm_df.empty:
        st.info(
            "No PTM or processing annotations were returned."
        )
        return

    st.dataframe(
        ptm_df,
        use_container_width=True,
        hide_index=True,
        height=430,
    )

    st.success(
        f"Loaded {len(ptm_df)} PTM/processing annotations."
    )


# ============================================================
# Ramachandran tab
# ============================================================

def _render_ramachandran_tab(
    pdb_text: str | None,
) -> None:
    """Render Ramachandran analysis."""

    st.markdown(
        '<div class="section-title">'
        "Ramachandran analysis"
        "</div>",
        unsafe_allow_html=True,
    )

    if not pdb_text:
        st.info(
            "A PDB structure is required for backbone-angle analysis."
        )
        return

    try:
        phi, psi, residue_numbers = (
            calculate_ramachandran_angles(pdb_text)
        )

        if not phi:
            st.info(
                "No complete φ/ψ angle pairs were available."
            )
            return

        st.plotly_chart(
            ramachandran_figure(
                phi,
                psi,
                residue_numbers,
            ),
            use_container_width=True,
        )

        st.caption(
            "Angles were calculated from the supplied AlphaFold PDB "
            f"for {len(phi)} residues."
        )

    except Exception as exc:
        st.warning(
            f"Ramachandran analysis failed: {exc}"
        )


# ============================================================
# BLAST tab
# ============================================================

def _render_blast_tab(
    protein: dict,
    sequence: str,
) -> None:
    """Render an optional BLAST search."""

    accession = protein["accession"]

    st.markdown(
        '<div class="section-title">'
        "BLAST similarity search"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "BLAST searches the sequence against NCBI databases. "
        "The search may take several seconds."
    )

    run_search = st.button(
        "Run BLAST search",
        key=f"blast_{accession}",
    )

    if not run_search:
        return

    with st.spinner(
        "Running BLAST. This may take up to a minute..."
    ):
        hits = run_blast_search(sequence)

    if not hits:
        st.warning(
            "No BLAST results were returned, or the search timed out."
        )
        return

    st.success(
        f"Found {len(hits)} similar sequences."
    )

    for hit in hits:
        st.write(
            f"- {hit.get('title', 'Untitled hit')}"
        )


# ============================================================
# DisProt tab
# ============================================================

def _render_disorder_tab(protein: dict) -> None:
    """Render intrinsically disordered regions."""

    st.markdown(
        '<div class="section-title">'
        "Intrinsically disordered regions"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "DisProt contains curated annotations for flexible "
        "or intrinsically disordered protein regions."
    )

    regions = get_disprot_regions(
        protein["accession"]
    )

    if not regions:
        st.info(
            "No DisProt regions were found for this protein."
        )
        return

    for region in regions:
        st.markdown(
            f"**Residues {region['start']}–{region['end']}:** "
            f"{region.get('term', 'Disordered region')}"
        )


# ============================================================
# Comparison tab
# ============================================================

def _render_comparison_tab(
    protein: dict,
    sequence: str,
    properties: dict,
    pdb_text: str | None,
    plddt: float | None,
) -> None:
    """Render comparison controls."""

    accession = protein["accession"]

    st.markdown(
        '<div class="section-title">'
        "Compare with another protein"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        f"Compare another protein against {accession} "
        "using sequence, chemistry, hydrophobicity, composition, "
        "and structure information."
    )

    input_column, button_column = st.columns([4, 1])

    with input_column:
        query = st.text_input(
            "Second protein",
            placeholder=(
                "e.g. hemoglobin subunit beta, TP63, P68871"
            ),
            key=f"comparison_query_{accession}",
        )

    with button_column:
        st.markdown(
            "<div style='height:1.7rem'></div>",
            unsafe_allow_html=True,
        )

        run_comparison = st.button(
            "Compare",
            type="primary",
            use_container_width=True,
            key=f"comparison_button_{accession}",
        )

    if not run_comparison:
        return

    if not query.strip():
        st.warning(
            "Enter a second protein to compare."
        )
        return

    render_comparison(
        p1=protein,
        sequence1=sequence,
        properties1=properties,
        pdb1=pdb_text,
        plddt1=plddt,
        query2=query.strip(),
    )
