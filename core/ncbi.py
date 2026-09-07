# core/ncbi.py
from __future__ import annotations

import urllib.request
import urllib.parse
import json

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL_PARAMS = "&tool=ProteinExplorer&email=user@example.com"


def search_ncbi_gene(query: str, db: str = "gene", retmax: int = 5) -> list[dict]:
    """Searches NCBI databases and returns matching records with robust key mapping."""
    search_url = f"{BASE_URL}esearch.fcgi?db={db}&term={urllib.parse.quote(query)}&retmax={retmax}&sort=relevant&format=json{TOOL_PARAMS}"
    
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
    """Fetches and parses summary details for a list of NCBI UIDs safely."""
    ids_str = ",".join(id_list)
    summary_url = f"{BASE_URL}esummary.fcgi?db={db}&id={ids_str}&format=json{TOOL_PARAMS}"
    
    try:
        req = urllib.request.Request(summary_url, headers={"User-Agent": "ProteinExplorer/1.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            result = data.get("result", {})
            
            summaries = []
            for uid in id_list:
                if uid in result:
                    item = result[uid]
                    
                    gene_id = item.get("uid", item.get("geneid", uid))
                    symbol = item.get("name", item.get("symbol", item.get("title", "Unknown")))
                    description = item.get("description", item.get("summary", item.get("caption", "")))
                    
                    org_info = item.get("organism", {})
                    if isinstance(org_info, dict):
                        organism = org_info.get("scientificname", org_info.get("name", "Unknown"))
                    else:
                        organism = str(org_info)

                    loc = item.get("chromosome", item.get("genomicinfo", ""))
                    if isinstance(loc, list) and len(loc) > 0:
                        chromosome = loc[0].get("chrsort", loc[0].get("chrid", ""))
                    else:
                        chromosome = str(loc)

                    summaries.append({
                        "gene_id": str(gene_id),
                        "uid": str(uid),
                        "symbol": str(symbol),
                        "name": str(symbol),
                        "description": str(description),
                        "organism": str(organism),
                        "chromosome": str(chromosome),
                        "summary": str(item.get("summary", "")),
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
    """Fetches a linked CDS nucleotide sequence with multi-tier fallback including UniProt accession and protein names."""
    gene_symbol = protein.get("gene", "").split(",")[0].split()[0].strip()
    organism = protein.get("organism", "Homo sapiens").split("(")[0].strip()
    accession = protein.get("accession", "")
    protein_name = protein.get("name", "").split(",")[0].strip()
    
    if not gene_symbol:
        gene_symbol = protein_name.split()[0] if protein_name else ""

    # Build comprehensive search queries including gene symbol, protein name, and UniProt accession
    queries = []
    if gene_symbol:
        queries.extend([
            f"{gene_symbol}[Gene] AND {organism}[Organism] AND mRNA[Filter]",
            f"{gene_symbol}[Gene] AND {organism}[Organism]",
            f"{gene_symbol} AND {organism}"
        ])
    if accession:
        queries.append(f"{accession}[Accession]")
    if protein_name:
        queries.append(f"{protein_name} AND {organism}")

    nucl_id = None
    for term in queries:
        search_url = f"{BASE_URL}esearch.fcgi?db=nuccore&term={urllib.parse.quote(term)}&retmax=1&format=json{TOOL_PARAMS}"
        try:
            req = urllib.request.Request(search_url, headers={"User-Agent": "ProteinExplorer/1.0"})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                id_list = data.get("esearchresult", {}).get("idlist", [])
                if id_list:
                    nucl_id = id_list[0]
                    break
        except Exception:
            continue

    if not nucl_id:
        return {"sequence": "", "length": 0, "gc_content": 0.0, "accession": "", "description": ""}

    try:
        fetch_url = f"{BASE_URL}efetch.fcgi?db=nuccore&id={nucl_id}&rettype=fasta&retmode=text{TOOL_PARAMS}"
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
