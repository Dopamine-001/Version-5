"""
DisProt lookup: flags intrinsically disordered regions — parts of a
protein with no fixed 3D shape.
"""

import requests


def get_disprot_regions(uniprot_id: str) -> list[dict]:
    """
    Queries DisProt for known disordered regions for a given UniProt
    accession. Returns an empty list if the protein isn't in DisProt
    (most proteins won't be — it's a curated, smaller database).
    """
    url = f"https://disprot.org/api/{uniprot_id}"
    try:
        response = requests.get(url, timeout=15)
    except requests.RequestException:
        return []

    if response.status_code != 200:
        return []

    data = response.json()
    regions = data.get("disprot_consensus", {}).get("full", [])

    return [
        {
            "start": r.get("start"),
            "end": r.get("end"),
            "term": r.get("term_name", "Disordered region"),
        }
        for r in regions
    ]
