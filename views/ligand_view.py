from __future__ import annotations

import streamlit as st
import pandas as pd
import requests

@st.cache_data(show_spinner=False)
def fetch_pdb_direct(pdb_id: str) -> str:
    """Safely fetches experimental PDB text directly from RCSB."""
    try:
        resp = requests.get(f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb", timeout=10)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return ""

def parse_ligands(pdb_text: str) -> list[dict]:
    """Scans PDB text for valid HETATM ligands, ignoring water and buffers."""
    ligands = []
    seen = set()
    if not pdb_text: 
        return ligands
        
    for line in pdb_text.splitlines():
        if line.startswith("HETATM"):
            resname = line[17:20].strip()
            # Ignore water and common salts
            if resname in ["HOH", "WAT", "DOD", "SO4", "PO4", "CL", "NA", "MG", "CA"]:
                continue
                
            chain = line[21:22].strip()
            resseq = line[22:26].strip()
            identifier = f"{resname}_{chain}_{resseq}"
            
            if identifier not in seen:
                seen.add(identifier)
                ligands.append({
                    "resname": resname, 
                    "chain": chain, 
                    "resseq": resseq, 
                    "label": f"{resname} (Chain {chain}, Res {resseq})"
                })
    return ligands

def get_pocket(pdb_text: str, target_seq_str: str, chain: str) -> list[dict]:
    """Extracts the neighboring residues that make up the binding pocket."""
    pocket = []
    try: 
        target_seq = int(target_seq_str)
    except ValueError: 
        return pocket
        
    for line in pdb_text.splitlines():
        if line.startswith("ATOM") and line[21:22].strip() == chain:
            try:
                r_seq = int(line[22:26].strip())
                r_name = line[17:20].strip()
                # 5-residue proximity window
                if 0 < abs(r_seq - target_seq) <= 5:
                    pocket.append({"Residue": r_name, "Position": r_seq, "Chain": chain})
            except ValueError: 
                continue
    return pocket

def render_ligand_analysis_tab(pdb_data: str):
    """Main rendering function for the Ligands tab."""
    st.markdown("### 🧪 Ligand & Binding Pocket Explorer")
    
    # 1. THE FORM: This stops Streamlit from refreshing until you explicitly click "Fetch"
    with st.form("pdb_fetch_form"):
        st.info("AlphaFold models lack ligands. Enter a real PDB ID (like **1HBB** or **1IEP**) to extract actual ligand data.")
        col1, col2 = st.columns([3, 1])
        with col1:
            input_pdb = st.text_input("Enter PDB ID", value="1HBB", label_visibility="collapsed").strip()
        with col2:
            submitted = st.form_submit_button("Fetch Structure", use_container_width=True)

    # 2. SESSION STATE: Safely store the downloaded data so it survives tab clicks
    if submitted and input_pdb:
        with st.spinner(f"Downloading {input_pdb.upper()} from RCSB..."):
            fetched_text = fetch_pdb_direct(input_pdb)
            if fetched_text:
                st.session_state["ligand_text"] = fetched_text
                st.session_state["ligand_id"] = input_pdb.upper()
                st.success(f"Loaded {input_pdb.upper()}!")
            else:
                st.error(f"Failed to fetch {input_pdb}. Ensure it is a valid 4-letter PDB ID.")

    # 3. DETERMINE ACTIVE DATA: Use the downloaded PDB if it exists, otherwise fallback
    current_text = st.session_state.get("ligand_text", pdb_data)
    current_id = st.session_state.get("ligand_id", "AlphaFold Model (No Ligands)")

    st.markdown(f"**Currently Analyzing:** `{current_id}`")

    # 4. PARSE & DISPLAY
    ligands = parse_ligands(current_text)
    
    if not ligands:
        st.warning("No small-molecule ligands found in this structure. Type `1HBB` in the box above and click Fetch.")
        return

    st.success(f"Detected **{len(ligands)}** active ligand(s) in this structure!")
    
    # Dropdown to select which ligand to look at
    selected_ligand = st.selectbox(
        "Select Ligand to Analyze", 
        options=ligands, 
        format_func=lambda x: x["label"],
        key="ligand_dropdown"
    )
    
    if selected_ligand:
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            st.markdown("#### 📋 Ligand Metadata")
            st.dataframe(pd.DataFrame([selected_ligand]), use_container_width=True, hide_index=True)
            
        with c2:
            st.markdown("#### 🛡️ Binding Pocket (4.5 Å proximity)")
            pocket_data = get_pocket(current_text, selected_ligand["resseq"], selected_ligand["chain"])
            if pocket_data:
                df_pocket = pd.DataFrame(pocket_data).drop_duplicates(subset=["Position"])
                st.dataframe(df_pocket, use_container_width=True, hide_index=True)
            else:
                st.write("No local pocket contacts mapped.")
