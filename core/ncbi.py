from core.helpers import safe_get

def get_ncbi_gene_info(protein_name):
    """
    Searches NCBI Entrez for a matching gene and returns basic info:
    Gene ID, chromosome location, and a plain-text summary.
    """
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "gene",
        "term": f"{protein_name}[Gene Name] AND human[Organism]",
        "retmode": "json",
        "retmax": 1,
    }
    search_resp = safe_get(search_url, params=search_params)
    search_data = search_resp.json()
    id_list = search_data.get("esearchresult", {}).get("idlist", [])

    if not id_list:
        return None

    gene_id = id_list[0]

    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    summary_params = {"db": "gene", "id": gene_id, "retmode": "json"}
    summary_resp = safe_get(summary_url, params=summary_params)
    summary_data = summary_resp.json()
    result = summary_data.get("result", {}).get(gene_id, {})

    return {
        "gene_id": gene_id,
        "chromosome": result.get("chromosome", "Unknown"),
        "map_location": result.get("maplocation", "Unknown"),
        "summary": result.get("summary", "No summary available."),
        "aliases": result.get("otheraliases", "None listed."),
    }

def get_ncbi_gene_info(protein_name):
    """
    Searches NCBI Entrez for a matching gene and returns basic info:
    Gene ID, chromosome location, and a plain-text summary.
    """
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "gene",
        "term": f"{protein_name}[Gene Name] AND human[Organism]",
        "retmode": "json",
        "retmax": 1,
    }
    search_resp = requests.get(search_url, params=search_params)
    search_data = search_resp.json()
    id_list = search_data.get("esearchresult", {}).get("idlist", [])

    if not id_list:
        return None

    gene_id = id_list[0]

    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    summary_params = {"db": "gene", "id": gene_id, "retmode": "json"}
    summary_resp = requests.get(summary_url, params=summary_params)
    summary_data = summary_resp.json()
    result = summary_data.get("result", {}).get(gene_id, {})

    return {
        "gene_id": gene_id,
        "chromosome": result.get("chromosome", "Unknown"),
        "map_location": result.get("maplocation", "Unknown"),
        "summary": result.get("summary", "No summary available."),
        "aliases": result.get("otheraliases", "None listed."),
    }
