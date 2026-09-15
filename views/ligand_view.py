from __future__ import annotations

import streamlit as st
import pandas as pd
from core.ligands import fetch_rcsb_pdb, extract_ligands_from_pdb, get_detailed_pocket_contacts


def render_ligand_analysis_tab(protein_record: dict, default_pdb_data: str):
    """Renders a robust ligand and binding pocket inspection dashboard with direct PDB loading."""
    st.markdown("### 🧪 Universal Ligand & Binding Pocket Explorer")
    st.caption("Inspect co-factors, substrates, inhibitors, and atomic binding site interactions for experimental PDB structures.")

    # Persistent session state for custom PDB input
    if "active_pdb_id" not in st.session_state:
        st.session_state["active_pdb_id"] = "1HBB"  # Default working crystal structure with heme
    if "active_pdb_text" not in st.session_state:
        st.session_state["active_pdb_text"] = fetch_rcsb_pdb("1HBB")

    # User Controls for PDB entry
    st.markdown("##### 🔬 Experimental Structure Loader")
    col_input, col_btn, col_ex1, col_ex2 = st.columns([2, 1, 1, 1])
    
    with col_input:
        input_pdb = st.text_input("Enter any RCSB PDB ID", value=st.session_state["active_pdb_id"], key="pdb_id_box").strip().upper()
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        load_btn = st.button("Load Structure", use_container_width=True)
    with col_ex1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Load 1HBB", use_container_width=True):
            input_pdb = "1HBB"
            load_btn = True
    with col_ex2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Load 1IEP", use_container_width=True):
            input_pdb = "1IEP"
            load_btn = True

    if load_btn and input_pdb:
        with st.spinner(f"Fetching PDB `{input_pdb}` from RCSB..."):
            text = fetch_rcsb_pdb(input_pdb)
            if text:
                st.session_state["active_pdb_id"] = input_pdb
                st.session_state["active_pdb_text"] = text
                st.success(f"Successfully loaded experimental PDB `{input_pdb}`!")
            else:
                st.error(f"Could not retrieve PDB ID `{input_pdb}`. Please verify the code.")

    current_pdb_text = st.session_state["active_pdb_text"]
    current_pdb_id = st.session_state["active_pdb_id"]

    st.markdown(f"**Currently Analyzing Structure ID:** `{current_pdb_id}`")

    # Extract ligands from the active PDB text
    ligands = extract_ligands_from_pdb(current_pdb_text)

    if not ligands:
        st.warning(f"No non-water bound ligands (`HETATM`) found in structure `{current_pdb_id}`. Try loading another ID like `1HBB` or `1IEP` using the buttons above.")
        return

    st.success(f"Detected **{len(ligands)}** active ligand(s) in `{current_pdb_id}`.")

    selected_ligand = st.selectbox(
        "Select Target Ligand to Analyze",
        options=ligands,
        format_func=lambda x: x["label"],
        key="ligand_dropdown_main"
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
                {"Property": "Source Structure", "Value": current_pdb_id}
            ])
            st.dataframe(meta_df, use_container_width=True, hide_index=True)
            
            rcsb_url = f"https://www.rcsb.org/ligand/{resn}"
            st.markdown(f"🔗 **RCSB Ligand Database:** [View Chemical Geometry]({rcsb_url})")

        with col_pocket:
            st.markdown("#### 🛡️ Binding Pocket Residues (4.5 Å)")
            pocket_data = get_detailed_pocket_contacts(current_pdb_text, resi, chain)

            if pocket_data:
                pocket_df = pd.DataFrame(pocket_data).drop_duplicates(subset=["Position"])
                st.dataframe(pocket_df, use_container_width=True, height=280, hide_index=True)
            else:
                st.info("Local contact mapping active for this site.")

        st.markdown("---")
        st.markdown("#### 💡 Pocket Interaction Overview")
        st.info(
            f"The bound molecule **{resn}** (Chain `{chain}`, Residue `{resi}`) occupies an active binding pocket "
            f"within structure `{current_pdb_id}`, stabilized by the neighboring amino acid side chains listed above."
        )
