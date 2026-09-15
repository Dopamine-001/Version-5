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
    """Renders an automated ligand & pocket explorer using mapped experimental PDBs."""
    st.markdown("### 🧪 Universal Ligand & Binding Pocket Explorer")
    st.caption("Automatically scanning experimental crystal structures and bound co-factors for this protein.")

    accession = protein_record.get("accession", "")
    
    # Session state key to keep track of selected structure per protein
    cache_key = f"auto_pdb_{accession}"

    if cache_key not in st.session_state:
        with st.spinner("Finding experimental crystal structures with bound ligands..."):
            pdb_ids = get_pdb_ids_for_uniprot(accession)
            st.session_state[cache_key] = pdb_ids

    experimental_pdb_ids = st.session_state.get(cache_key, [])

    # Let user choose or fallback to manual input/AlphaFold
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_pdb = st.selectbox(
            "Mapped Experimental PDB Structures",
            options=experimental_pdb_ids if experimental_pdb_ids else ["No experimental PDB mapped"],
            key=f"select_pdb_{accession}"
        )
    with col2:
        manual_override = st.text_input("Or enter PDB ID", placeholder="e.g. 1BEN", key=f"manual_{accession}").strip()

    target_id = manual_override.upper() if manual_override else (selected_pdb if selected_pdb != "No experimental PDB mapped" else "")

    # Fetch PDB text
    pdb_data = default_pdb_data
    active_source_label = "AlphaFold Model (No Ligands)"

    if target_id:
        with st.spinner(f"Fetching structure `{target_id}` from RCSB PDB..."):
            fetched_text = fetch_rcsb_pdb(target_id)
            if fetched_text:
                pdb_data = fetched_text
                active_source_label = f"Experimental PDB: {target_id}"
            else:
                st.error(f"Failed to download structure for `{target_id}`.")
    elif experimental_pdb_ids:
        # Automatically pull the first available experimental structure if none chosen manually
        auto_id = experimental_pdb_ids[0]
        with st.spinner(f"Auto-loading primary experimental structure `{auto_id}`..."):
            fetched_text = fetch_rcsb_pdb(auto_id)
            if fetched_text:
                pdb_data = fetched_text
                active_source_label = f"Experimental PDB: {auto_id}"

    st.markdown(f"**Active Source:** `{active_source_label}`")

    # Extract ligands
    ligands = extract_ligands_from_pdb(pdb_data)

    if not ligands:
        st.warning(
            "No non-water bound ligands (`HETATM`) were detected in this structure file. "
            "Try selecting a different PDB ID from the dropdown above or typing a known structure ID (e.g., `1HBB` for hemoglobin, `1BEN` for insulin complexes)."
        )
        return

    st.success(f"Successfully detected **{len(ligands)}** active ligand(s) / co-factor(s).")

    selected_ligand = st.selectbox(
        "Select Ligand to Analyze",
        options=ligands,
        format_func=lambda x: x["label"],
        key=f"lig_drop_{accession}"
    )

    if selected_ligand:
        resn = selected_ligand["resname"]
        chain = selected_ligand["chain"]
        resi = selected_ligand["resseq"]

        col_meta, col_pocket = st.columns([1, 1], gap="large")

        with col_meta:
            st.markdown("#### 📋 Ligand Profile")
            meta_df = pd.DataFrame([
                {"Attribute": "Chemical Code", "Details": resn},
                {"Attribute": "Chain ID", "Details": chain},
                {"Attribute": "Residue Number", "Details": resi},
                {"Attribute": "Type", "Details": "Co-crystallized Heteroatom / Inhibitor"}
            ])
            st.dataframe(meta_df, use_container_width=True, hide_index=True)
            
            rcsb_link = f"https://www.rcsb.org/ligand/{resn}"
            st.markdown(f"🔗 **External Reference:** [View Chemical Card on RCSB]({rcsb_link})")

        with col_pocket:
            st.markdown("#### 🔬 Binding Pocket Contact Matrix")
            pocket_data = get_detailed_pocket_contacts(pdb_data, resi, chain)

            if pocket_data:
                pocket_df = pd.DataFrame(pocket_data).drop_duplicates(subset=["Position"])
                st.dataframe(pocket_df, use_container_width=True, height=260, hide_index=True)
            else:
                st.info("Mapped local sequence spatial neighborhood.")

        st.markdown("---")
        st.info(f"💡 **Analysis Summary:** The binding pocket for **{resn}** (Position {resi}, Chain {chain}) shows close non-covalent proximity to the neighboring amino acids listed in the contact matrix above.")
