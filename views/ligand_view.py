from __future__ import annotations

import streamlit as st
import pandas as pd
from core.ligands import (
    get_pdb_ids_for_uniprot, 
    fetch_rcsb_pdb, 
    extract_ligands_from_pdb, 
    get_detailed_pocket_contacts
)


def render_ligand_analysis_tab(protein_record: dict, default_pdb_data: str):
    """Renders a detailed, comprehensive ligand and binding pocket inspection dashboard."""
    st.markdown("### 🧪 Universal Ligand & Binding Pocket Explorer")
    st.caption("Inspect co-factors, inhibitors, and detailed atomic binding site interactions for experimental structures.")

    accession = protein_record.get("accession", "")
    
    with st.spinner("Querying PDBe for experimental structures..."):
        experimental_pdb_ids = get_pdb_ids_for_uniprot(accession)

    col_sel, col_man = st.columns([2, 1])
    with col_sel:
        selected_pdb = st.selectbox(
            "Select Experimental PDB Structure",
            options=experimental_pdb_ids if experimental_pdb_ids else ["No mapped PDBs found"],
            key=f"pdb_select_{accession}"
        )
    with col_man:
        manual_id = st.text_input("Or type PDB ID", placeholder="e.g. 1HBB, 1IEP", key=f"manual_pdb_{accession}").strip()

    target_pdb_id = manual_id.upper() if manual_id else (selected_pdb if selected_pdb != "No mapped PDBs found" else "")

    pdb_data = default_pdb_data
    if target_pdb_id and target_pdb_id != "NO MAPPED PDBS FOUND":
        with st.spinner(f"Fetching structure {target_pdb_id} from RCSB..."):
            fetched_text = fetch_rcsb_pdb(target_pdb_id)
            if fetched_text:
                pdb_data = fetched_text
                st.success(f"Successfully loaded experimental structure `{target_pdb_id}`.")
            else:
                st.error(f"Could not retrieve PDB file for `{target_pdb_id}`.")

    ligands = extract_ligands_from_pdb(pdb_data)

    if not ligands:
        st.warning("No active bound ligands (`HETATM`) found in this structure file. Please choose an alternative experimental PDB ID from the dropdown or enter one manually.")
        return

    st.markdown(f"**Found {len(ligands)} bound ligand entity(ies) in structure `{target_pdb_id or 'Model'}`.**")

    selected_ligand = st.selectbox(
        "Choose Ligand to Examine",
        options=ligands,
        format_func=lambda x: x["label"],
        key=f"ligand_dropdown_{accession}"
    )

    if selected_ligand:
        resn = selected_ligand["resname"]
        chain = selected_ligand["chain"]
        resi = selected_ligand["resseq"]

        # Detailed Layout Split
        col_summary, col_details = st.columns([1, 1], gap="large")

        with col_summary:
            st.markdown("#### 📋 Chemical Metadata")
            meta_df = pd.DataFrame([
                {"Metric": "Ligand Code", "Detail": resn},
                {"Metric": "Chain Identifier", "Detail": chain},
                {"Metric": "Residue Index", "Detail": resi},
                {"Metric": "Classification", "Detail": "Co-crystallized Heteroatom / Inhibitor"}
            ])
            st.dataframe(meta_df, use_container_width=True, hide_index=True)

            st.markdown("#### 🔗 External Cross-References")
            rcsb_url = f"https://www.rcsb.org/ligand/{resn}"
            st.markdown(f"- [View Chemical Geometry on RCSB Ligand Summary]({rcsb_url})")

        with col_details:
            st.markdown("#### 🛡️ Binding Pocket Interacting Residues")
            pocket_data = get_detailed_pocket_contacts(pdb_data, resi, chain)

            if pocket_data:
                pocket_df = pd.DataFrame(pocket_data).drop_duplicates(subset=["Position"])
                st.dataframe(pocket_df, use_container_width=True, height=280, hide_index=True)
            else:
                st.info("Detailed contact profiling mapped local spatial coordinates.")

        st.markdown("---")
        st.markdown("#### 💡 Structural Interaction Summary")
        st.info(
            f"The ligand **{resn}** at position **{resi}** on chain **{chain}** forms a stable microenvironment "
            f"within the protein core, stabilized by surrounding amino acid residues listed in the binding pocket matrix."
        )
