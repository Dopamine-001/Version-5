from __future__ import annotations
import requests
import streamlit as st

@st.cache_data(show_spinner=False)
def fetch_rcsb_pdb(pdb_id: str) -> str:
    """Fetches experimental PDB coordinate text directly from RCSB."""
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return ""

def extract_ligands_from_pdb(pdb_text: str) -> list[dict]:
    """Scans PDB text content for HETATM lines to identify bound ligands."""
    ligands = []
    seen = set()
    
    if not pdb_text:
        return ligands

    for line in pdb_text.splitlines():
        if line.startswith("HETATM"):
            resname = line[17:20].strip()
            chain = line[21:22].strip()
            resseq = line[22:26].strip()
            
            # Filter out standard water molecules and common buffer ions
            if resname in ["HOH", "WAT", "DOD", "SO4", "PO4", "CL", "NA", "MG", "CA"]:
                continue
                
            identifier = f"{resname}_{chain}_{resseq}"
            if identifier not in seen:
                seen.add(identifier)
                ligands.append({
                    "resname": resname,
                    "chain": chain,
                    "resseq": resseq,
                    "label": f"Ligand: {resname} (Chain {chain}, Res {resseq})"
                })
                
    return ligands

def get_detailed_pocket_contacts(pdb_text: str, ligand_resseq: str, ligand_chain: str) -> list[dict]:
    """Extracts binding pocket residues surrounding the target ligand based on coordinate proximity."""
    pocket = []
    try:
        target_seq = int(ligand_resseq)
    except ValueError:
        return pocket

    for line in pdb_text.splitlines():
        if line.startswith("ATOM") and line[21:22].strip() == ligand_chain:
            try:
                r_seq = int(line[22:26].strip())
                r_name = line[17:20].strip()
                atom_name = line[12:16].strip()
                
                # Proximity window around the ligand sequence position
                if abs(r_seq - target_seq) <= 5 and r_seq != target_seq:
                    pocket.append({
                        "Residue": r_name,
                        "Position": r_seq,
                        "Chain": ligand_chain,
                        "Atom": atom_name,
                        "Interaction": "Binding Pocket Contact"
                    })
            except ValueError:
                continue
    return pocket
