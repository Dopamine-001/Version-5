"""
gene_db_integrator.py
----------------------
Integrates gene information from three public databases:
  1. Ensembl (REST API)          -> gene ID, location, biotype, description
  2. NCBI Entrez Gene (E-utils)  -> Entrez Gene ID, official name, summary
  3. Human Protein Atlas (API)   -> tissue/protein expression, subcellular
                                     location, reliability scores

Given one or more human gene SYMBOLS (e.g. "TP53", "BRCA1"), this script
queries all three databases, merges the results into a single row per gene,
and saves the combined table as both CSV and JSON in the same folder.

Requirements:
    pip install requests pandas --break-system-packages

Usage:
    python gene_db_integrator.py TP53 BRCA1 EGFR
    python gene_db_integrator.py --file genes.txt
        (genes.txt = one gene symbol per line)

Output:
    integrated_genes.csv
    integrated_genes.json
"""

import sys
import json
import time
import argparse
import requests
import pandas as pd


# ----------------------------------------------------------------------
# 1. ENSEMBL
# ----------------------------------------------------------------------
def get_ensembl_data(symbol: str, species: str = "human") -> dict:
    """
    Look up a gene symbol on Ensembl and return core annotation fields.
    Docs: https://rest.ensembl.org/documentation/info/symbol_lookup
    """
    url = f"https://rest.ensembl.org/lookup/symbol/{species}/{symbol}"
    params = {"content-type": "application/json", "expand": 0}
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return {
            "ensembl_id": data.get("id"),
            "ensembl_description": data.get("description"),
            "ensembl_biotype": data.get("biotype"),
            "chromosome": data.get("seq_region_name"),
            "start": data.get("start"),
            "end": data.get("end"),
            "strand": data.get("strand"),
        }
    except requests.exceptions.RequestException as e:
        return {"ensembl_error": str(e)}


# ----------------------------------------------------------------------
# 2. NCBI ENTREZ GENE (via E-utils)
# ----------------------------------------------------------------------
def get_entrez_data(symbol: str, organism: str = "Homo sapiens") -> dict:
    """
    Search NCBI Gene database for the symbol, then fetch a summary.
    Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/
    """
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esummary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    search_term = f"{symbol}[sym] AND {organism}[orgn]"
    try:
        r1 = requests.get(
            esearch_url,
            params={"db": "gene", "term": search_term, "retmode": "json"},
            timeout=15,
        )
        r1.raise_for_status()
        ids = r1.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return {"entrez_error": "No Entrez Gene ID found"}

        gene_id = ids[0]
        time.sleep(0.34)  # be polite to NCBI (max ~3 req/sec without an API key)

        r2 = requests.get(
            esummary_url,
            params={"db": "gene", "id": gene_id, "retmode": "json"},
            timeout=15,
        )
        r2.raise_for_status()
        summary = r2.json().get("result", {}).get(gene_id, {})

        return {
            "entrez_gene_id": gene_id,
            "entrez_official_name": summary.get("description"),
            "entrez_summary": summary.get("summary"),
            "entrez_gene_type": summary.get("genetype"),
            "entrez_map_location": summary.get("maplocation"),
        }
    except requests.exceptions.RequestException as e:
        return {"entrez_error": str(e)}


# ----------------------------------------------------------------------
# 3. HUMAN PROTEIN ATLAS
# ----------------------------------------------------------------------
def get_hpa_data(ensembl_id: str) -> dict:
    """
    Fetch protein/tissue expression data from the Human Protein Atlas
    using the Ensembl gene ID (HPA indexes genes by Ensembl ID).
    Docs: https://www.proteinatlas.org/about/help/dataaccess
    """
    if not ensembl_id:
        return {"hpa_error": "No Ensembl ID available to query HPA"}

    url = f"https://www.proteinatlas.org/{ensembl_id}.json"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return {
            "hpa_gene_name": data.get("Gene"),
            "hpa_subcellular_location": data.get("Subcellular location"),
            "hpa_tissue_expression_cluster": data.get("Tissue expression cluster"),
            "hpa_rna_tissue_specificity": data.get("RNA tissue specificity"),
            "hpa_protein_class": data.get("Protein class"),
        }
    except requests.exceptions.RequestException as e:
        return {"hpa_error": str(e)}


# ----------------------------------------------------------------------
# MASTER INTEGRATION FUNCTION
# ----------------------------------------------------------------------
def integrate_gene(symbol: str) -> dict:
    """Combine Ensembl + Entrez + HPA data for one gene symbol into one record."""
    print(f"Fetching data for {symbol} ...")
    record = {"gene_symbol": symbol}

    ensembl = get_ensembl_data(symbol)
    record.update(ensembl)

    entrez = get_entrez_data(symbol)
    record.update(entrez)

    hpa = get_hpa_data(ensembl.get("ensembl_id"))
    record.update(hpa)

    return record


def main():
    parser = argparse.ArgumentParser(
        description="Integrate gene data from Ensembl, NCBI Entrez Gene, and Human Protein Atlas."
    )
    parser.add_argument("genes", nargs="*", help="Gene symbols, e.g. TP53 BRCA1")
    parser.add_argument("--file", help="Text file with one gene symbol per line")
    args = parser.parse_args()

    symbols = list(args.genes)
    if args.file:
        with open(args.file) as f:
            symbols += [line.strip() for line in f if line.strip()]

    if not symbols:
        print("No gene symbols given. Example: python gene_db_integrator.py TP53 BRCA1")
        sys.exit(1)

    records = [integrate_gene(sym) for sym in symbols]

    df = pd.DataFrame(records)
    df.to_csv("integrated_genes.csv", index=False)
    with open("integrated_genes.json", "w") as f:
        json.dump(records, f, indent=2)

    print("\nDone. Saved: integrated_genes.csv, integrated_genes.json")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
