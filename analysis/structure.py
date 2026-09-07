from __future__ import annotations

import math
import numpy as np
from Bio.PDB import PDBParser
from io import StringIO

def calculate_ramachandran_angles(pdb_text: str):
    """Calculates Phi and Psi torsion angles from PDB text coordinates using atom vectors."""
    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure("protein", StringIO(pdb_text))
    except Exception:
        return [], [], []

    phi_list = []
    psi_list = []
    res_nums = []

    for model in structure:
        for chain in model:
            residues = [r for r in chain if r.get_id()[0] == " "]
            for i in range(len(residues)):
                res = residues[i]
                res_id = res.get_id()[1]
                
                if not ("N" in res and "CA" in res and "C" in res):
                    continue
                
                phi = None
                if i > 0:
                    prev_res = residues[i-1]
                    if "C" in prev_res:
                        try:
                            v1 = prev_res["C"].get_vector()
                            v2 = res["N"].get_vector()
                            v3 = res["CA"].get_vector()
                            v4 = res["C"].get_vector()
                            from Bio.PDB.vectors import calc_dihedral
                            phi = math.degrees(calc_dihedral(v1, v2, v3, v4))
                        except Exception:
                            pass
                
                psi = None
                if i < len(residues) - 1:
                    next_res = residues[i+1]
                    if "N" in next_res:
                        try:
                            v1 = res["N"].get_vector()
                            v2 = res["CA"].get_vector()
                            v3 = res["C"].get_vector()
                            v4 = next_res["N"].get_vector()
                            from Bio.PDB.vectors import calc_dihedral
                            psi = math.degrees(calc_dihedral(v1, v2, v3, v4))
                        except Exception:
                            pass
                
                if phi is not None and psi is not None:
                    phi_list.append(phi)
                    psi_list.append(psi)
                    res_nums.append(res_id)
        break

    return phi_list, psi_list, res_nums


def secondary_structure_with_fallback(protein: dict, pdb_text: str) -> dict[int, str]:
    """
    Robust secondary structure assignment using backbone dihedral angles (Phi/Psi).
    Classifies residues into Helix ('H'), Sheet ('E'), or Coil ('C').
    """
    sec_struct = {}
    sequence = protein.get("sequence", "")
    
    for i in range(1, len(sequence) + 1):
        sec_struct[i] = "C"

    if not pdb_text:
        return sec_struct

    try:
        phi_list, psi_list, res_nums = calculate_ramachandran_angles(pdb_text)
        
        for res_id, phi, psi in zip(res_nums, phi_list, psi_list):
            if -100 <= phi <= -40 and -70 <= psi <= -10:
                sec_struct[res_id] = "H"
            elif -150 <= phi <= -80 and (90 <= psi <= 180 or -180 <= psi <= -150):
                sec_struct[res_id] = "E"
            else:
                sec_struct[res_id] = "C"
                
    except Exception:
        for i, aa in enumerate(sequence, start=1):
            if aa in "EALQK":
                sec_struct[i] = "H"
            elif aa in "VIFYW":  
                sec_struct[i] = "E"
            else:
                sec_struct[i] = "C"

    return sec_struct
