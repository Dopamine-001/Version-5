from __future__ import annotations

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def search_ncbi_gene(query: str, db: str = "gene", retmax: int = 5) -> list[dict]:
    """Searches NCBI databases (e.g., gene, nuccore, protein) and returns matching records."""
    search_url = f"{BASE_URL}esearch.fcgi?db={db}&term={urllib.parse.quote(query)}&retmax={retmax}&sort=relevant&format=json"
    
    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": "ProteinExplorer/1.0"})
        with urllib.request.urlopen(req) as response:
            import json
            data = json.loads(response.read().decode())
            id_list = data.get("esearchresult", {}).get("idlist", [])
            
            if not id_list:
                return []
                
            return fetch_ncbi_summaries(db, id_list)
    except Exception as e:
        print(f"NCBI Search Error: {e}")
        return []


def fetch_ncbi_summaries(db: str, id_list: list[str]) -> list[dict]:
    """Fetches summary details for a list of NCBI UIDs."""
    ids_str = ",".join(id_list)
    summary_url = f"{BASE_URL}esummary.fcgi?db={db}&id={ids_str}&format=json"
    
    try:
        req = urllib.request.Request(summary_url, headers={"User-Agent": "ProteinExplorer/1.0"})
        with urllib.request.urlopen(req) as response:
            import json
            data = json.loads(response.read().decode())
            result = data.get("result", {})
            
            summaries = []
            for uid in id_list:
                if uid in result:
                    item = result[uid]
                    summaries.append({
                        "uid": uid,
                        "name": item.get("name", item.get("title", "Unknown")),
                        "description": item.get("description", item.get("caption", "")),
                        "organism": item.get("organism", {}).get("scientificname", "Unknown"),
                        "chromosome": item.get("chromosome", ""),
                    })
            return summaries
    except Exception as e:
        print(f"NCBI Summary Error: {e}")
        return []
