from __future__ import annotations

import urllib.request
import urllib.parse
import json

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def search_ncbi_gene(query: str, db: str = "gene", retmax: int = 5) -> list[dict]:
    """Searches NCBI databases (e.g., gene, nuccore, protein) and returns matching records."""
    search_url = f"{BASE_URL}esearch.fcgi?db={db}&term={urllib.parse.quote(query)}&retmax={retmax}&sort=relevant&format=json"
    
    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": "ProteinExplorer/1.0"})
        with urllib.request.urlopen(req) as response:
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


def get_ncbi_gene_info(gene_symbol: str) -> dict:
    """Convenience wrapper to fetch gene info for a single symbol."""
    results = search_ncbi_gene(gene_symbol, db="gene", retmax=1)
    return results[0] if results else {}


def fetch_cds_nucleotide_sequence(protein: dict) -> dict:
    """Fetches a linked CDS nucleotide sequence or searches Nuccore based on gene info."""
    gene_symbol = protein.get("gene", "").split(",")[0].strip()
    if not gene_symbol:
        return {"sequence": "", "length": 0, "gc_content": 0.0, "accession": "", "description": ""}

    search_url = f"{BASE_URL}esearch.fcgi?db=nuccore&term={urllib.parse.quote(gene_symbol + '[Gene] AND homo sapiens[Organism] AND biomol_mrna[PROP]')}&retmax=1&format=json"
    
    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": "ProteinExplorer/1.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            id_list = data.get("esearchresult", {}).get("idlist", [])
            
            if not id_list:
                return {"sequence": "", "length": 0, "gc_content": 0.0, "accession": "", "description": ""}
                
            nucl_id = id_list[0]
            
            # Fetch fasta sequence
            fetch_url = f"{BASE_URL}efetch.fcgi?db=nuccore&id={nucl_id}&rettype=fasta&retmode=text"
            req_fasta = urllib.request.Request(fetch_url, headers={"User-Agent": "ProteinExplorer/1.0"})
            with urllib.request.urlopen(req_fasta) as fasta_resp:
                fasta_text = fasta_resp.read().decode()
                lines = fasta_text.splitlines()
                header = lines[0] if lines else "Unknown"
                seq = "".join(line.strip() for line in lines[1:])
                
                if not seq:
                    return {"sequence": "", "length": 0, "gc_content": 0.0, "accession": "", "description": ""}
                
                length = len(seq)
                gc_count = seq.upper().count("G") + seq.upper().count("C")
                gc_content = round((gc_count / length) * 100, 2) if length > 0 else 0.0
                
                return {
                    "sequence": seq,
                    "length": length,
                    "gc_content": gc_content,
                    "accession": nucl_id,
                    "description": header,
                }
    except Exception as e:
        print(f"NCBI CDS Fetch Error: {e}")
        return {"sequence": "", "length": 0, "gc_content": 0.0, "accession": "", "description": ""}
