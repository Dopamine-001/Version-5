import requests
import streamlit as st

@st.cache_data(show_spinner=False)
def fetch_rcsb_pdb(pdb_id: str) -> dict:
    """Fetches PDB and returns a status dictionary to stop silent network failures."""
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return {"success": True, "text": res.text, "error": None}
        else:
            return {"success": False, "text": "", "error": f"HTTP {res.status_code} - ID might not exist."}
    except Exception as e:
        return {"success": False, "text": "", "error": str(e)}

def extract_ligands_from_pdb(pdb_text: str) -> list[dict]:
    """Scans PDB text for valid ligands, ignoring water."""
    ligands = []
    seen = set()
    if not pdb_text: 
        return ligands

    for line in pdb_text.splitlines():
        if line.startswith("HETATM"):
            resname = line[17:20].strip()
            # Filter out water and common salts
            if resname in ["HOH", "WAT", "DOD", "SO4", "PO4", "CL", "NA", "MG", "CA"]:
                continue
            
            chain = line[21:22].strip()
            resseq = line[22:26].strip()
            uid = f"{resname}_{chain}_{resseq}"
            
            if uid not in seen:
                seen.add(uid)
                ligands.append({
                    "resname": resname,
                    "chain": chain,
                    "resseq": resseq,
                    "label": f"{resname} (Chain {chain}, Position {resseq})"
                })
    return ligands

def get_detailed_pocket_contacts(pdb_text: str, ligand_resseq: str, ligand_chain: str) -> list[dict]:
    """Finds neighboring protein residues around the ligand."""
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
                if 0 < abs(r_seq - target_seq) <= 5:
                    pocket.append({
                        "Residue": r_name,
                        "Position": r_seq,
                        "Chain": ligand_chain,
                        "Atom": atom_name
                    })
            except ValueError:
                continue
    return pocket
