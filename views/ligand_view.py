import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from core.ligands import fetch_rcsb_pdb, extract_ligands_from_pdb, get_detailed_pocket_contacts

def render_3d_visualizer(pdb_id: str, resn: str, chain: str, resi: str):
    """Bypasses Python py3dmol and renders 3Dmol.js directly in the browser."""
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    </head>
    <body style="margin:0; padding:0; background-color:#0e1117;">
        <div id="container" style="height: 450px; width: 100%; position: relative;"></div>
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                let element = document.querySelector('#container');
                let viewer = $3Dmol.createViewer(element, {{backgroundColor: '#0e1117'}});
                
                // Let the browser download the PDB directly from RCSB
                $3Dmol.download("pdb:{pdb_id.lower()}", viewer, {{}}, function() {{
                    
                    // 1. Style the base protein (Semi-transparent gray cartoon)
                    viewer.setStyle({{}}, {{cartoon: {{color: '#aaaaaa', opacity: 0.5}}}});
                    
                    // 2. Style the Binding Pocket (Green sticks)
                    let pocket_sel = {{within: {{distance: 5.0, sel: {{resn: '{resn}', chain: '{chain}', resi: '{resi}'}}}}}};
                    viewer.addStyle(pocket_sel, {{stick: {{colorscheme: 'greenCarbon', radius: 0.15}}}});
                    
                    // 3. Style the Target Ligand (Cyan sticks, thicker)
                    let ligand_sel = {{resn: '{resn}', chain: '{chain}', resi: '{resi}'}};
                    viewer.addStyle(ligand_sel, {{stick: {{colorscheme: 'cyanCarbon', radius: 0.3}}}});
                    
                    // Zoom specifically to the ligand
                    viewer.zoomTo(ligand_sel);
                    viewer.render();
                }});
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=450)


def render_ligand_analysis_tab(*args, **kwargs):
    """Crash-proof signature that safely extracts PDB text."""
    default_pdb_data = ""
    for arg in args:
        if isinstance(arg, str) and "ATOM " in arg:
            default_pdb_data = arg
    if not default_pdb_data and "pdb_data" in kwargs:
        default_pdb_data = kwargs["pdb_data"]

    st.markdown("### 🧪 Universal Ligand & Binding Pocket Explorer")
    
    if "ligand_pdb_id" not in st.session_state:
        st.session_state["ligand_pdb_id"] = ""
    if "ligand_pdb_text" not in st.session_state:
        st.session_state["ligand_pdb_text"] = ""

    st.markdown("##### 🔬 Load Experimental Structure")
    c_input, c_btn = st.columns([3, 1])
    
    with c_input:
        input_pdb = st.text_input("Enter 4-letter RCSB PDB ID (e.g. 1HBB, 1IEP)", value="1HBB").strip()
    with c_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Fetch Ligands", type="primary", use_container_width=True):
            with st.spinner(f"Downloading {input_pdb.upper()}..."):
                result = fetch_rcsb_pdb(input_pdb)
                if result["success"]:
                    st.session_state["ligand_pdb_id"] = input_pdb.upper()
                    st.session_state["ligand_pdb_text"] = result["text"]
                    st.success(f"Downloaded {input_pdb.upper()} successfully!")
                else:
                    st.error(f"Download Failed for {input_pdb}: {result['error']}")
                    st.session_state["ligand_pdb_id"] = ""
                    st.session_state["ligand_pdb_text"] = ""

    active_text = st.session_state["ligand_pdb_text"] if st.session_state["ligand_pdb_text"] else default_pdb_data
    active_id = st.session_state["ligand_pdb_id"] if st.session_state["ligand_pdb_text"] else "AlphaFold (No Ligands)"

    st.markdown(f"**Current Structure:** `{active_id}`")

    ligands = extract_ligands_from_pdb(active_text)

    if not ligands:
        st.warning("No non-water bound ligands (HETATM) found in this structure file.")
        if not st.session_state["ligand_pdb_text"]:
            st.info("💡 **Hint:** AlphaFold predictions do not contain ligands. Type `1HBB` in the box above and click **Fetch Ligands**.")
        return

    st.success(f"Detected **{len(ligands)}** ligand(s)!")

    selected = st.selectbox("Select Ligand", options=ligands, format_func=lambda x: x["label"])

    if selected:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("#### 📋 Metadata")
            df_meta = pd.DataFrame([selected])
            st.dataframe(df_meta, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### 🛡️ Binding Pocket Contacts")
            pocket = get_detailed_pocket_contacts(active_text, selected["resseq"], selected["chain"])
            if pocket:
                df_pocket = pd.DataFrame(pocket).drop_duplicates(subset=["Position"])
                st.dataframe(df_pocket, use_container_width=True, height=200, hide_index=True)
            else:
                st.info("No localized contacts detected within window.")

        st.markdown("---")
        st.markdown("#### 🧬 3D Interaction Viewer")
        st.caption(f"Visualizing {selected['resname']} in pocket (Cyan = Ligand, Green = 5Å Contact Residues)")
        
        # Inject the 3Dmol.js HTML viewer using the current active ID
        if active_id != "AlphaFold (No Ligands)":
            render_3d_visualizer(active_id, selected["resname"], selected["chain"], selected["resseq"])
