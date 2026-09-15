from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components
import py3dmol
from core.ligands import extract_ligands_from_pdb


def render_ligand_analysis_tab(pdb_data: str):
    """Renders the interactive ligand and binding pocket inspection tool."""
    st.markdown("### 🧪 Ligand & Binding Pocket Explorer")
    st.caption("Inspect bound co-factors, substrates, or inhibitors and highlight neighboring pocket residues.")

    if not pdb_data:
        st.warning("No structural PDB coordinate data available for ligand analysis.")
        return

    ligands = extract_ligands_from_pdb(pdb_data)
    
    if not ligands:
        st.info("No non-water bound ligands (HETATM) found in this structure file.")
        return
        
    st.success(f"Detected **{len(ligands)}** potential ligand/heteroatom entity(ies).")
    
    # Selection dropdown if multiple ligands exist
    selected_ligand = st.selectbox(
        "Select Target Ligand", 
        options=ligands, 
        format_func=lambda x: x["label"],
        key="ligand_selector"
    )
    
    if selected_ligand:
        resn = selected_ligand["resname"]
        chain = selected_ligand["chain"]
        resi = selected_ligand["resseq"]
        
        col1, col2 = st.columns([2, 1], gap="large")
        
        with col1:
            # Initialize Py3Dmol view focusing on protein + ligand + binding pocket
            view = py3dmol.view(width=700, height=500)
            view.addModel(pdb_data, "pdb")
            
            # 1. Style base protein cartoon
            view.setStyle({'model': -1}, {'cartoon': {'color': 'lightgray', 'opacity': 0.7}})
            
            # 2. Style and highlight target ligand in bright cyan sticks
            view.addStyle(
                {'resn': resn, 'chain': chain, 'resi': resi},
                {'stick': {'colorscheme': 'cyanCarbon', 'radius': 0.3}}
            )
            
            # 3. Highlight neighboring pocket residues within 4.5 Angstroms in green sticks
            view.addStyle(
                {'within': {'distance': 4.5, 'sel': {'resn': resn, 'resi': resi}}},
                {'stick': {'colorscheme': 'greenCarbon'}}
            )
            
            view.zoomTo({'resn': resn, 'resi': resi})
            
            # Render natively using Streamlit components
            components.html(view._make_html(), height=520, scrolling=False)
            
        with col2:
            st.markdown("#### Pocket Interaction Key")
            st.markdown(
                "🟢 **Green residues:** Surrounding amino acid side chains within a $4.5\\text{ \\AA}$ binding pocket radius.\n\n"
                "🔵 **Cyan molecule:** The active ligand/heteroatom."
            )
            st.divider()
            st.info(f"**Residue Name:** `{resn}`\n\n**Chain:** `{chain}`\n\n**Position:** `{resi}`")
