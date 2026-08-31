"""
AlphaFold Protein Structure Database: fetch the predicted PDB + metadata,
and a handful of small readers that pull numbers straight out of PDB text
(pLDDT, chain count, secondary-structure record counts) without needing a
full structure parse.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import streamlit as st

from config import ALPHAFOLD_API_URL
from core.helpers import safe_get


@st.cache_data(ttl=3600, show_spinner=False)
def get_alphafold_structure(accession: str) -> tuple[Optional[str], dict]:
    """Fetch the current AlphaFold prediction PDB and metadata."""
    response = safe_get(ALPHAFOLD_API_URL.format(accession=accession))
    if not response:
        return None, {}

    data = response.json()
    if not data:
        return None, {}

    entry = data[0]
    pdb_url = entry.get("pdbUrl")
    if not pdb_url:
        return None, entry

    pdb_response = safe_get(pdb_url)
    return (pdb_response.text if pdb_response else None), entry


def calculate_plddt(pdb_text: str) -> Optional[float]:
    """AlphaFold stores per-atom pLDDT in the PDB B-factor column."""
    values = []
    for line in pdb_text.splitlines():
        if line.startswith(("ATOM", "HETATM")):
            try:
                values.append(float(line[60:66].strip()))
            except (ValueError, IndexError):
                continue
    return round(sum(values) / len(values), 1) if values else None


def plddt_distribution(pdb_text: str) -> pd.DataFrame:
    values = []
    for line in pdb_text.splitlines():
        if line.startswith("ATOM"):
            try:
                values.append(float(line[60:66].strip()))
            except (ValueError, IndexError):
                pass
    return pd.DataFrame({"Atom pLDDT": values})


def structure_chain_count(pdb_text: str) -> int:
    chains = {
        line[21].strip() or "_"
        for line in pdb_text.splitlines()
        if line.startswith("ATOM") and len(line) > 21
    }
    return len(chains)


def secondary_structure_summary(pdb_text: str) -> dict:
    """Count residues covered by HELIX and SHEET records in the supplied PDB."""
    helix, sheet = set(), set()
    for line in pdb_text.splitlines():
        if line.startswith("HELIX") and len(line) >= 38:
            try:
                chain = line[19].strip() or "_"
                start = int(line[21:25])
                end = int(line[33:37])
                helix.update((chain, i) for i in range(start, end + 1))
            except ValueError:
                pass
        elif line.startswith("SHEET") and len(line) >= 38:
            try:
                chain = line[21].strip() or "_"
                start = int(line[22:26])
                end = int(line[33:37])
                sheet.update((chain, i) for i in range(start, end + 1))
            except ValueError:
                pass

    return {"alpha-helix residues": len(helix), "beta-sheet residues": len(sheet)}
