from __future__ import annotations

import requests

ENSEMBL_BASE = "https://rest.ensembl.org"


def _ensembl_get(endpoint: str, params: dict | None = None, timeout: int = 20):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = f"{ENSEMBL_BASE}{endpoint}"
    response = requests.get(url, headers=headers, params=params or {}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def lookup_ensembl_id(ensembl_id: str, expand: bool = True) -> dict:
    """
    Return Ensembl metadata for a gene/transcript/protein stable ID.
    """
    params = {"expand": int(bool(expand))}
    try:
        return _ensembl_get(f"/lookup/id/{ensembl_id}", params=params)
    except Exception as exc:
        return {"error": str(exc), "id": ensembl_id}


def fetch_ensembl_sequence(
    ensembl_id: str,
    seq_type: str = "cds",
    object_type: str | None = None,
    species: str | None = None,
) -> dict:
    """
    Fetch sequence from Ensembl.
    seq_type: genomic, cds, cdna, protein
    """
    params = {
        "type": seq_type,
    }

    if object_type:
        params["object_type"] = object_type

    if species:
        params["species"] = species

    try:
        headers = {
            "Content-Type": "text/plain",
            "Accept": "text/plain",
        }
        url = f"{ENSEMBL_BASE}/sequence/id/{ensembl_id}"
        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()

        seq = response.text.strip()

        if not seq:
            return {
                "id": ensembl_id,
                "sequence": "",
                "length": 0,
                "type": seq_type,
                "error": "Empty sequence returned by Ensembl",
            }

        return {
            "id": ensembl_id,
            "sequence": seq,
            "length": len(seq),
            "type": seq_type,
        }

    except Exception as exc:
        return {
            "id": ensembl_id,
            "sequence": "",
            "length": 0,
            "type": seq_type,
            "error": str(exc),
        }


def resolve_gene_to_transcripts(ensembl_gene_id: str) -> dict:
    """
    Return gene metadata including transcripts.
    """
    try:
        data = _ensembl_get(f"/lookup/id/{ensembl_gene_id}", params={"expand": 1})
        return data
    except Exception as exc:
        return {"error": str(exc), "gene_id": ensembl_gene_id}
