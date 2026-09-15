from __future__ import annotations

import streamlit as st
import pandas as pd
from core.ligands import (
    get_ligand_containing_pdb, 
    fetch_rcsb_pdb, 
    extract_ligands_from_pdb, 
    get_detailed_pocket_contacts
)


def render_ligand_analysis_tab(protein_record: dict, default_pdb_data: str):
    """Renders the automated ligand and binding pocket explorer for any protein."""
    st.markdown("### 🧪 Universal Ligand & Binding Pocket Explorer")
    st.caption("Automatically retrieves experimental crystal structures containing bound co-factors, inhibitors, or substrates.")

    accession = protein_record.get("accession", "")
    
    # Session state to cache the fetched experimental structure per protein
    cache_key = f"ligand_pdb_cache_{accession}"
    
    if cache_key not in st.session_state:
        with st.spinner("Searching PDB database for experimental structures with bound ligands..."):
            pdb_id, pdb_text = get_ligand_containing_pdb(accession)
            st.session_state[cache_key] = {"id": pdb_id, "text": pdb_text}

    cached = st.session_state[cache_key]
    active_pdb_id = cached["id"]
    active_pdb_text = cached["text"]

    # Allow manual override if needed
    col_info, col_man = st.columns([2, 1])
    with col_info:
        st.markdown(f"**Auto-Detected Structure:** `{active_pdb_id if active_pdb_id else 'None found via API'}`")
    with col_man:
        manual_override = st.text_input("Override PDB ID", placeholder="e.g. 1HBB", key=f"override_{accession}").strip().upper()

    if manual_override:
        with st.spinner(f"Fetching PDB `{manual_override}`..."):
            forced_text = fetch_rcsb_pdb(manual_override)
            if forced_text:
                active_pdb_text = forced_text
                active_pdb_id = manual_override
                st.success(f"Loaded structure `{manual_override}` successfully!")
            else:
                st.error(f"Could not load `{manual_override}`.")

    # Fallback to default if nothing found
    target_data = active_pdb_text if active_pdb_text else default_pdb_data

    ligands = extract_ligands_from_pdb(target_data)

    if not ligands:
        st.warning(
            "No experimental crystal structure with bound ligands (`HETATM`) could be automatically linked to this protein entry. "
            "You can manually type a known PDB ID containing ligands (such as **1HBB** for hemoglobin or **1IEP** for a kinase inhibitor) into the override box above."
        )
        return

    st.success(f"Successfully detected **{len(ligands)}** bound ligand(s) from structure `{active_pdb_id or 'Custom'}`.")

    selected_ligand = st.selectbox(
        "Select Target Ligand to Analyze",
        options=ligands,
        format_func=lambda x: x["label"],
        key=f"lig_select_{accession}"
    )

    if selected_ligand:
        resn = selected_ligand["resname"]
        chain = selected_ligand["chain"]
        resi = selected_ligand["resseq"]

        col_meta, col_pocket = st.columns([1, 1], gap="large")

        with col_meta:
            st.markdown("#### 📋 Ligand Metadata")
            meta_df = pd.DataFrame([
                {"Property": "Chemical Code", "Value": resn},
                {"Property": "Chain", "Value": chain},
                {"Property": "Position", "Value": resi},
                {"Property": "Source PDB", "Value": active_pdb_id or "Custom"}
            ])
            st.dataframe(meta_df, use_container_width=True, hide_index=True)
            
            rcsb_url = f"https://www.rcsb.org/ligand/{resn}"
            st.markdown(f"🔗 **RCSB Database:** [View Chemical Geometry]({rcsb_url})")

        with col_pocket:
            st.markdown("#### 🛡️ Binding Pocket Residues (4.5 Å)")
            pocket_data = get_detailed_pocket_contacts(target_data, resi, chain)

            if pocket_data:
                pocket_df = pd.DataFrame(pocket_data).drop_duplicates(subset=["Position"])
                st.dataframe(pocket_df, use_container_width=True, height=260, hide_index=True)
            else:
                st.info("Local contact mapping active.")

        st.markdown("---")
        st.markdown("#### 💡 Pocket Interaction Overview")
        st.info(
            f"The bound molecule **{resn}** (Chain `{chain}`, Residue `{resi}`) interacts with the protein core "
            f"via the non-covalent contact residues listed in the table above."
        )
