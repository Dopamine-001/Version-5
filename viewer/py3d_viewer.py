import streamlit as st
from core.alphafold import calculate_plddt, get_alphafold_structure
from core.uniprot import normalize_uniprot_record, search_uniprot
from viewer.py3d_viewer import render_structure

def show_comparison(query1: str, query2: str) -> None:
    st.markdown(f"### Protein Structural Comparison: {query1} vs {query2}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### Protein 1: {query1}")
        raw1 = search_uniprot(query1)
        rec1 = normalize_uniprot_record(raw1)
        pdb1 = get_alphafold_structure(rec1.get("accession")) if rec1 else None
        plddt1 = calculate_plddt(pdb1) if pdb1 else None
        
        st.metric("Accession", rec1.get("accession", "N/A"))
        st.metric("Length", f"{rec1.get('length', 'N/A')} AA")
        st.metric("Mean pLDDT", f"{plddt1:.1f}" if plddt1 else "N/A")
        
        if pdb1:
            render_structure(pdb1, color_scheme="plddt", width=450, height=400)
        else:
            st.error("Could not load structure for Protein 1.")

    with col2:
        st.markdown(f"#### Protein 2: {query2}")
        raw2 = search_uniprot(query2)
        rec2 = normalize_uniprot_record(raw2)
        pdb2 = get_alphafold_structure(rec2.get("accession")) if rec2 else None
        plddt2 = calculate_plddt(pdb2) if pdb2 else None
        
        st.metric("Accession", rec2.get("accession", "N/A"))
        st.metric("Length", f"{rec2.get('length', 'N/A')} AA")
        st.metric("Mean pLDDT", f"{plddt2:.1f}" if plddt2 else "N/A")
        
        if pdb2:
            render_structure(pdb2, color_scheme="plddt", width=450, height=400)
        else:
            st.error("Could not load structure for Protein 2.")
