from __future__ import annotations

import math
import numpy as np
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import drei_to_ein

def calculate_ramachandran_angles(pdb_text: str):
    """Calculates Phi and Psi torsion angles from PDB text coordinates."""
    parser = PDBParser(QUIET=True)
    try:
        from io import StringIO
        structure = parser.get_structure("protein", StringIO(pdb_text))
    except Exception:
        return [], [], []

    phi_list = []
    psi_list = []
    res_nums = []

    for model in structure:
        for chain in model:
            from Bio.PDB.PPBuilder import PPBuilder
            ppb = PPBuilder()
            for pp in ppb.build_peptides(chain):
                phi_psi = pp.get_phi_psi()
                for i, residue in enumerate(pp):
                    phi, psi = phi_psi[i]
                    if phi is not None and psi is not None:
                        phi_list.append(math.degrees(phi))
                        psi_list.append(math.degrees(psi))
                        res_nums.append(residue.get_id()[1])
        break  # Use first model

    return phi_list, psi_list, res_nums


def secondary_structure_with_fallback(protein: dict, pdb_text: str) -> dict[int, str]:
    """
    Robust secondary structure assignment using backbone dihedral angles (Phi/Psi).
    Classifies residues into Helix ('H'), Sheet ('E'), or Coil ('C').
    """
    sec_struct = {}
    sequence = protein.get("sequence", "")
    
    # Default everything to coil first
    for i in range(1, len(sequence) + 1):
        sec_struct[i] = "C"

    if not pdb_text:
        return sec_struct

    try:
        phi_list, psi_list, res_nums = calculate_ramachandran_angles(pdb_text)
        
        for res_id, phi, psi in zip(res_nums, phi_list, psi_list):
            # Standard Ramachandran boundaries for Alpha Helix ('H') and Beta Sheet ('E')
            if -100 <= phi <= -40 and -70 <= psi <= -10:
                sec_struct[res_id] = "H"
            elif -150 <= phi <= -80 and (90 <= psi <= 180 or -180 <= psi <= -150):
                sec_struct[res_id] = "E"
            else:
                sec_struct[res_id] = "C"
                
    except Exception:
        # Fallback heuristic based on sequence patterns if coordinate parsing fails
        for i, aa in enumerate(sequence, start=1):
            if aa in "EALQK":
                sec_struct[i] = "H"
            elif aa in "VIFYW":  
                sec_struct[i] = "E"
            else:
                sec_struct[i] = "C"

    return sec_struct
