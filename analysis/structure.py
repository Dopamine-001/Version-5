"""
Structure-derived analysis that needs a full Biopython parse of the PDB
(as opposed to core.alphafold's cheap line-scanning readers).
"""

from __future__ import annotations

import io
import math

import streamlit as st
from Bio.PDB import PDBParser, PPBuilder


@st.cache_data(show_spinner=False)
def calculate_ramachandran_angles(pdb_text: str) -> tuple[list[float], list[float], list[int]]:
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", io.StringIO(pdb_text))
    phi_angles, psi_angles, residue_numbers = [], [], []

    def collect(builder) -> None:
        for model in structure:
            for chain in model:
                for poly in builder.build_peptides(chain):
                    angles = poly.get_phi_psi_list()
                    residues = list(poly)
                    for residue, (phi, psi) in zip(residues, angles):
                        if phi is not None and psi is not None:
                            phi_angles.append(math.degrees(phi))
                            psi_angles.append(math.degrees(psi))
                            residue_numbers.append(residue.id[1])

    # The strict PPBuilder (uses a tight peptide-bond distance cutoff) can
    # fail to link consecutive residues in some AlphaFold PDBs and silently
    # return zero peptides, which left this plot blank. CaPPBuilder uses
    # CA-CA distance instead and is more tolerant of minor geometry quirks,
    # so fall back to it if the strict builder finds nothing.
    collect(PPBuilder())
    if not phi_angles:
        from Bio.PDB import CaPPBuilder
        collect(CaPPBuilder())

    return phi_angles, psi_angles, residue_numbers
