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



def extract_secondary_structure_ranges(uniprot_data: dict) -> dict:
    """
    Extracts residue ranges for Alpha-helices and Beta-strands/sheets from UniProt features.
    """
    # normalize_uniprot_record() stores the raw feature list under
    # "all_features"; raw UniProt JSON uses "features". Accept both.
    features = (
        uniprot_data.get("features")
        or uniprot_data.get("all_features")
        or []
    )
    helices = []
    strands = []
    turns = []
    
    for feat in features:
        feat_type = feat.get("type", "").lower()
        location = feat.get("location", {})
        start = location.get("start", {}).get("value")
        end = location.get("end", {}).get("value")
        
        if start and end:
            item = {"start": int(start), "end": int(end), "description": feat.get("description", "")}
            if "helix" in feat_type:
                helices.append(item)
            elif "strand" in feat_type or "beta" in feat_type:
                strands.append(item)
            elif "turn" in feat_type:
                turns.append(item)
                
    return {
        "helices": helices,
        "sheets": strands,
        "turns": turns
    }


# ------------------------------------------------------------------
# Geometric secondary-structure fallback
# ------------------------------------------------------------------
# UniProt only lists HELIX / STRAND features for proteins with an
# experimental structure. For AlphaFold-only entries the feature list is
# empty, which used to make the secondary-structure viewer all grey.
# This assigns helix / strand from the model's own phi-psi angles.

@st.cache_data(show_spinner=False)
def assign_secondary_structure_from_pdb(pdb_text: str) -> dict:
    phi_angles, psi_angles, residue_numbers = calculate_ramachandran_angles(pdb_text)

    labels: list[tuple[int, str]] = []
    for phi, psi, resi in zip(phi_angles, psi_angles, residue_numbers):
        if -160.0 <= phi <= -20.0 and -90.0 <= psi <= 10.0:
            labels.append((resi, "H"))          # right-handed alpha helix
        elif -180.0 <= phi <= -45.0 and (90.0 <= psi <= 180.0 or -180.0 <= psi <= -170.0):
            labels.append((resi, "E"))          # extended / beta strand
        else:
            labels.append((resi, "C"))

    helices: list[dict] = []
    sheets: list[dict] = []

    run_label = None
    run_start = None
    prev_resi = None

    def close_run() -> None:
        if run_label is None or run_start is None:
            return
        length = prev_resi - run_start + 1
        item = {"start": run_start, "end": prev_resi, "description": "predicted"}
        # Minimum lengths keep single noisy residues out of the render.
        if run_label == "H" and length >= 4:
            helices.append(item)
        elif run_label == "E" and length >= 3:
            sheets.append(item)

    for resi, label in labels:
        contiguous = prev_resi is not None and resi == prev_resi + 1
        if label != run_label or not contiguous:
            close_run()
            run_label, run_start = label, resi
        prev_resi = resi
    close_run()

    return {"helices": helices, "sheets": sheets, "turns": [], "source": "geometry"}


def secondary_structure_with_fallback(uniprot_data: dict, pdb_text: str) -> dict:
    """UniProt annotations when available, otherwise geometric assignment."""
    annotated = extract_secondary_structure_ranges(uniprot_data)
    if annotated.get("helices") or annotated.get("sheets"):
        annotated["source"] = "uniprot"
        return annotated
    try:
        return assign_secondary_structure_from_pdb(pdb_text)
    except Exception:
        annotated["source"] = "uniprot"
        return annotated
