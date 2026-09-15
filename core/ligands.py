from __future__ import annotations
import requests
import streamlit as st

@st.cache_data(show_spinner=False)
def get_pdb_ids_for_uniprot(uniprot_accession: str) -> list[str]:
    """Queries PDBe API to find experimental PDB structures associated with a UniProt accession."""
    if not uniprot_accession:
        return []
    url = f"https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{uniprot_accession.upper()}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            acc_data = data.get(uniprot_accession.upper(), {})
            mappings = acc_data.get("mappings", [])
            pdb_ids = list(set(m.get("pdb_id") for m in mappings if m.get("pdb_id")))
            return sorted(pdb_ids)
    except Exception:
        pass
    return []

@st.cache_data(show_spinner=False)
def fetch_rcsb_pdb(pdb_id: str) -> str:
    """Fetches experimental PDB coordinate text from RCSB."""
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return ""

def extract_ligands_from_pdb(pdb_text: str) -> list[dict]:
    """Scans PDB text content for HETATM lines to identify bound ligands with rich details."""
    ligands = []
    seen = set()
    
    if not pdb_text:
        return ligands

    for line in pdb_text.splitlines():
        if line.startswith("HETATM"):
            resname = line[17:20].strip()
            chain = line[21:22].strip()
            resseq = line[22:26].strip()
            
            # Filter out standard water molecules and common crystallization buffers/ions
            if resname in ["HOH", "WAT", "DOD", "SO4", "PO4", "CL", "NA", "MG", "CA", "EDTA"]:
                continue
                
            identifier = f"{resname}_{chain}_{resseq}"
            if identifier not in seen:
                seen.add(identifier)
                ligands.append({
                    "resname": resname,
                    "chain": chain,
                    "resseq": resseq,
                    "label": f"Ligand: {resname} (Chain {chain}, Position {resseq})"
                })
                
    return ligands

def get_detailed_pocket_contacts(pdb_text: str, ligand_resseq: str, ligand_chain: str) -> list[dict]:
    """Extracts detailed binding pocket residues surrounding the target ligand."""
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
                
                # Identify neighboring residues within a local sequence/spatial proximity window
                if 0 < abs(r_seq - target_seq) <= 6 and r_seq != target_seq:
                    pocket.append({
                        "Residue": r_name,
                        "Position": r_seq,
                        "Chain": ligand_chain,
                        "Contact Atom": atom_name,
                        "Interaction Type": "Non-covalent Proximity"
                    })
            except ValueError:
                continue
    return pocket
