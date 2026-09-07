"""
Human Protein Atlas integration: tissue expression, cell-type specificity,
and pathology/disease associations.
"""

from __future__ import annotations

from core.helpers import safe_get


def get_hpa_data(gene_symbol: str) -> dict:
    """
    Fetch tissue expression and pathology data for a given gene symbol
    using the Human Protein Atlas JSON API.
    """
    if not gene_symbol:
        return {}
        
    url = f"https://www.proteinatlas.org/api/search_download.php?search={gene_symbol}&format=json&columns=g,gs,tissues,pathology&compress=no"
    response = safe_get(url)
    
    if not response:
        return {}
        
    try:
        data = response.json()
        if data and isinstance(data, list):
            return data[0]
    except Exception:
        pass
        
    return {}
