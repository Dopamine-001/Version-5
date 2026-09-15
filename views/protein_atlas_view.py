import streamlit as st
import requests
import pandas as pd

@st.cache_data(show_spinner=False)
def fetch_deep_annotation_data(accession: str) -> dict:
    """Fetches rich functional, location, and GO data directly from the EBI Proteins API."""
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{accession}"
    try:
        res = requests.get(url, headers={"Accept": "application/json"}, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return {}

def render_protein_atlas_tab(protein_record: dict):
    """Renders a comprehensive Gene Ontology and Protein Atlas dashboard."""
    st.markdown("### 🧬 Advanced Expression & Protein Atlas")
    st.caption("Comprehensive subcellular location, tissue specificity, and Gene Ontology (GO) profiling.")
    
    accession = protein_record.get("accession", "")
    if not accession:
        st.warning("No valid UniProt accession provided to fetch Atlas data.")
        return
        
    with st.spinner("Mining deep functional and expression data..."):
        data = fetch_deep_annotation_data(accession)
        
    if not data:
        st.error("Failed to retrieve deep annotation data. The EBI database might be temporarily unreachable.")
        return

    # --- 1. DATA EXTRACTION ---
    tissue = "No specific tissue expression data mapped."
    disease = "No specific pathology associations mapped."
    subcellular_locations = []
    
    # Extract Comments
    for comment in data.get("comments", []):
        if comment.get("type") == "TISSUE_SPECIFICITY":
            tissue = comment.get("text", [{}])[0].get("value", tissue)
        elif comment.get("type") == "DISEASE":
            disease = comment.get("text", [{}])[0].get("value", disease)
        elif comment.get("type") == "SUBCELLULAR_LOCATION":
            for loc in comment.get("locations", []):
                if "location" in loc:
                    subcellular_locations.append(loc["location"]["value"])

    # Extract GO Terms & Ensembl Cross-References
    go_components, go_functions, go_processes = [], [], []
    ensembl_id = ""
    
    for db in data.get("dbReferences", []):
        if db.get("type") == "Ensembl" and not ensembl_id:
            ensembl_id = db.get("id")
        
        if db.get("type") == "GO":
            term = db.get("properties", {}).get("term", "")
            if term.startswith("C:"): go_components.append(term[2:])
            elif term.startswith("F:"): go_functions.append(term[2:])
            elif term.startswith("P:"): go_processes.append(term[2:])

    # --- 2. UI DASHBOARD RENDERING ---
    
    # Direct link to the actual Human Protein Atlas using the extracted Ensembl ID
    if ensembl_id:
        hpa_url = f"https://www.proteinatlas.org/{ensembl_id}"
        st.info(f"🔗 **Human Protein Atlas Database:** [View Original Tissue & Cell Images for {protein_record.get('gene', 'this gene')}]({hpa_url})")

    st.markdown("#### 🔬 Subcellular Localization")
    if subcellular_locations:
        # Deduplicate and join with a clean separator
        formatted_locs = " ⸰ ".join(sorted(set(subcellular_locations)))
        st.success(f"**{formatted_locs}**")
    else:
        st.info("Subcellular location not explicitly mapped.")
        
    col_t, col_p = st.columns([1, 1], gap="large")
    with col_t:
        st.markdown("#### 🧬 Tissue Expression Profile")
        st.info(tissue)
    with col_p:
        st.markdown("#### ⚠️ Pathology & Disease")
        st.warning(disease)
        
    st.markdown("---")
    st.markdown("#### 📊 Gene Ontology (GO) Profiling")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("**🏛️ Cellular Component**")
        if go_components:
            st.dataframe(pd.DataFrame(go_components, columns=["Location"]), use_container_width=True, hide_index=True)
        else:
            st.write("No data")
            
    with c2:
        st.markdown("**⚙️ Molecular Function**")
        if go_functions:
            st.dataframe(pd.DataFrame(go_functions, columns=["Function"]), use_container_width=True, hide_index=True)
        else:
            st.write("No data")
            
    with c3:
        st.markdown("**🔄 Biological Process**")
        if go_processes:
            st.dataframe(pd.DataFrame(go_processes, columns=["Process"]), use_container_width=True, hide_index=True)
        else:
            st.write("No data")
