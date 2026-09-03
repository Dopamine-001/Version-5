from __future__ import annotations

import xml.etree.ElementTree as ET

from core.helpers import safe_get

import requests
from Bio import Entrez

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _text(element, path, default=""):
    """Safely extract text from an XML element."""
    node = element.find(path)

    if node is not None and node.text:
        return node.text.strip()

    return default


def _collect_texts(element, path):
    """Collect multiple XML text values."""
    values = []

    for node in element.findall(path):
        if node.text and node.text.strip():
            values.append(node.text.strip())

    return values


def _safe_json(response):
    """Safely decode a JSON response."""
    try:
        return response.json()
    except Exception:
        return {}


def _get_related_ids(gene_id, database):
    """
    Use NCBI ELink to retrieve IDs related to the Gene record.
    """
    url = f"{NCBI_BASE}/elink.fcgi"

    params = {
        "dbfrom": "gene",
        "db": database,
        "id": gene_id,
        "retmode": "json",
    }

    try:
        response = safe_get(url, params=params)
        data = _safe_json(response)

        ids = []

        for linkset in data.get("linksets", []):
            for linksetdb in linkset.get("linksetdbs", []):
                ids.extend(linksetdb.get("links", []))

        return list(dict.fromkeys(str(x) for x in ids))

    except Exception:
        return []


def _search_database(term, database, retmax=20):
    """
    Generic NCBI ESearch helper.
    """
    url = f"{NCBI_BASE}/esearch.fcgi"

    params = {
        "db": database,
        "term": term,
        "retmode": "json",
        "retmax": retmax,
    }

    try:
        response = safe_get(url, params=params)
        data = _safe_json(response)

        return (
            data
            .get("esearchresult", {})
            .get("idlist", [])
        )

    except Exception:
        return []


def get_ncbi_gene_info(protein_name):
    """
    Retrieve detailed human NCBI Gene information.

    Uses:
    ESearch
    ESummary
    EFetch
    ELink
    Additional Entrez searches for related records.
    """

    # =========================================================
    # 1. ESEARCH
    # =========================================================

    search_url = f"{NCBI_BASE}/esearch.fcgi"

    search_params = {
        "db": "gene",
        "term": f"{protein_name}[Gene Name] AND Homo sapiens[Organism]",
        "retmode": "json",
        "retmax": 1,
    }

    try:
        search_response = safe_get(
            search_url,
            params=search_params,
        )

        search_data = _safe_json(search_response)

        id_list = (
            search_data
            .get("esearchresult", {})
            .get("idlist", [])
        )

        # -----------------------------------------------------
        # Fallback search
        # -----------------------------------------------------

        if not id_list:
            id_list = _search_database(
                f"{protein_name}[All Fields] AND Homo sapiens[Organism]",
                "gene",
                retmax=1,
            )

        if not id_list:
            return None

        gene_id = str(id_list[0])

        # =========================================================
        # 2. ESUMMARY
        # =========================================================

        summary_url = f"{NCBI_BASE}/esummary.fcgi"

        summary_params = {
            "db": "gene",
            "id": gene_id,
            "retmode": "json",
        }

        summary_response = safe_get(
            summary_url,
            params=summary_params,
        )

        summary_data = _safe_json(summary_response)

        result = (
            summary_data
            .get("result", {})
            .get(gene_id, {})
        )

        # =========================================================
        # 3. EFETCH
        # =========================================================

        fetch_url = f"{NCBI_BASE}/efetch.fcgi"

        fetch_params = {
            "db": "gene",
            "id": gene_id,
            "retmode": "xml",
        }

        fetch_response = safe_get(
            fetch_url,
            params=fetch_params,
        )

        xml_root = ET.fromstring(fetch_response.text)

        # =========================================================
        # 4. BASIC GENE IDENTITY
        # =========================================================

        gene_symbol = (
            result.get("name")
            or _text(
                xml_root,
                ".//Gene-ref/Gene-ref_locus",
            )
            or protein_name
        )

        gene_name = (
            result.get("description")
            or _text(
                xml_root,
                ".//Gene-ref/Gene-ref_desc",
            )
            or "Not available"
        )

        # =========================================================
        # 5. ORGANISM
        # =========================================================

        organism = result.get("organism", {})

        if isinstance(organism, dict):
            organism_name = organism.get(
                "scientificname",
                "Homo sapiens",
            )
        else:
            organism_name = str(
                organism or "Homo sapiens"
            )

        # =========================================================
        # 6. ALIASES
        # =========================================================

        aliases = []

        aliases.extend(
            _collect_texts(
                xml_root,
                ".//Gene-ref_syn/Gene-ref_syn_E",
            )
        )

        aliases.extend(
            _collect_texts(
                xml_root,
                ".//Gene-ref_syn/Gene-ref_syn_N",
            )
        )

        if not aliases:
            other_aliases = result.get("otheraliases")

            if other_aliases:
                aliases = [
                    x.strip()
                    for x in str(other_aliases).split(",")
                    if x.strip()
                ]

        aliases = list(dict.fromkeys(aliases))

        # =========================================================
        # 7. CHROMOSOME
        # =========================================================

        chromosome = (
            result.get("chromosome")
            or _text(
                xml_root,
                ".//Gene-commentary_chromosome",
            )
            or "Unknown"
        )

        # =========================================================
        # 8. MAP LOCATION
        # =========================================================

        map_location = (
            result.get("maplocation")
            or "Unknown"
        )

        # =========================================================
        # 9. GENE TYPE
        # =========================================================

        gene_type = (
            result.get("genetype")
            or "Not available"
        )

        # =========================================================
        # 10. STATUS
        # =========================================================

        status = (
            result.get("status")
            or "Not available"
        )

        # =========================================================
        # 11. SUMMARY
        # =========================================================

        summary = (
            result.get("summary")
            or "No summary available."
        )

        # =========================================================
        # 12. OTHER DESIGNATIONS
        # =========================================================

        designations = _collect_texts(
            xml_root,
            ".//Gene-ref_syn/Gene-ref_syn_Other",
        )

        # =========================================================
        # 13. NOMENCLATURE
        # =========================================================

        nomenclature_symbol = (
            result.get("nomenclaturesymbol")
            or gene_symbol
        )

        nomenclature_full_name = (
            result.get("nomenclaturefullname")
            or gene_name
        )

        # =========================================================
        # 14. CROSS REFERENCES
        # =========================================================

        db_references = []

        for dbtag in xml_root.findall(".//Dbtag"):

            db = _text(
                dbtag,
                "Dbtag_db",
            )

            tag = dbtag.find(
                "Dbtag_tag/Object-id/Object-id_str"
            )

            if tag is None:
                tag = dbtag.find(
                    "Dbtag_tag/Object-id/Object-id_id"
                )

            if db and tag is not None and tag.text:

                db_references.append(
                    {
                        "database": db,
                        "identifier": tag.text.strip(),
                    }
                )

        # =========================================================
        # 15. RELATED RECORDS USING ELINK
        # =========================================================

        related_databases = {
            "pubmed": "pubmed",
            "protein": "protein",
            "nucleotide": "nuccore",
            "snp": "snp",
            "clinvar": "clinvar",
            "omim": "omim",
        }

        related_records = {}

        for label, database in related_databases.items():

            related_records[label] = _get_related_ids(
                gene_id,
                database,
            )

        # =========================================================
        # 16. DIRECT DATABASE SEARCHES
        # =========================================================

        pubmed_ids = _search_database(
            f"{gene_symbol}[Title/Abstract]",
            "pubmed",
            retmax=20,
        )

        protein_ids = related_records.get(
            "protein",
            [],
        )

        nucleotide_ids = related_records.get(
            "nucleotide",
            [],
        )

        snp_ids = related_records.get(
            "snp",
            [],
        )

        clinvar_ids = related_records.get(
            "clinvar",
            [],
        )

        # =========================================================
        # 17. RETURN COMPLETE DATASET
        # =========================================================

        return {

            # Identity
            "gene_id": gene_id,
            "gene_symbol": gene_symbol,
            "gene_name": gene_name,
            "description": gene_name,
            "organism": organism_name,

            # Location
            "chromosome": chromosome,
            "map_location": map_location,
            "genomic_location": map_location,

            # Classification
            "gene_type": gene_type,
            "status": status,

            # Names
            "aliases": aliases,
            "other_designations": designations,

            # Function
            "summary": summary,

            # Nomenclature
            "nomenclature_symbol": nomenclature_symbol,
            "nomenclature_full_name": nomenclature_full_name,

            # Cross references
            "cross_references": db_references,

            # Related databases
            "related_records": related_records,

            # Individual record collections
            "pubmed_ids": pubmed_ids,
            "protein_ids": protein_ids,
            "nucleotide_ids": nucleotide_ids,
            "snp_ids": snp_ids,
            "clinvar_ids": clinvar_ids,

            # Useful counts
            "pubmed_count": len(pubmed_ids),
            "protein_count": len(protein_ids),
            "nucleotide_count": len(nucleotide_ids),
            "snp_count": len(snp_ids),
            "clinvar_count": len(clinvar_ids),

            # NCBI URL
            "ncbi_gene_url": (
                "https://www.ncbi.nlm.nih.gov/"
                f"gene/{gene_id}"
            ),
        }

    except Exception as exc:

        # Return a controlled error instead of crashing
        # the entire Streamlit application.
        return {
            "error": str(exc),
            "gene_id": None,
            "gene_symbol": protein_name,
            "gene_name": "NCBI retrieval failed",
            "organism": "Homo sapiens",
            "aliases": [],
            "other_designations": [],
            "cross_references": [],
            "related_records": {},
            "pubmed_ids": [],
            "protein_ids": [],
            "nucleotide_ids": [],
            "snp_ids": [],
            "clinvar_ids": [],
        }


def fetch_cds_nucleotide_sequence(uniprot_data: dict) -> dict:
    """
    Fetch the nucleotide CDS sequence associated with a UniProt protein.

    Uses UniProt cross-references to identify an EMBL/RefSeq nucleotide
    accession and retrieves the corresponding sequence from NCBI.
    """

    result = {
        "accession": None,
        "sequence": "",
        "length": 0,
        "gc_content": 0.0,
        "description": ""
    }

    cross_refs = uniprot_data.get("uniProtKBCrossReferences", [])

    nucleotide_id = None

    # ---------------------------------------------------------
    # Find a suitable EMBL / RefSeq nucleotide accession
    # ---------------------------------------------------------
    for ref in cross_refs:
        database = ref.get("database", "")
        ref_id = ref.get("id", "")
        properties = {
            item.get("key"): item.get("value")
            for item in ref.get("properties", [])
        }

        if database == "RefSeq":
            nucleotide_id = (
                properties.get("nucleotide sequence ID")
                or properties.get("NucleotideSequenceID")
                or ref_id
            )

            if nucleotide_id:
                break

        elif database == "EMBL":
            # Prefer nucleotide accession rather than ProteinId
            nucleotide_id = (
                properties.get("NucleotideSequenceID")
                or properties.get("Nucleotide sequence ID")
                or ref_id
            )

            if nucleotide_id:
                break

    if not nucleotide_id:
        return result

    # ---------------------------------------------------------
    # Query NCBI
    # ---------------------------------------------------------
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    params = {
        "db": "nuccore",
        "id": nucleotide_id,
        "rettype": "fasta",
        "retmode": "text"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        fasta = response.text.strip()

        if not fasta.startswith(">"):
            return result

        # -----------------------------------------------------
        # Parse FASTA
        # -----------------------------------------------------
        lines = fasta.splitlines()

        description = lines[0][1:].strip()

        sequence = "".join(
            line.strip()
            for line in lines[1:]
            if line.strip()
        ).upper()

        # Keep only valid DNA characters
        sequence = "".join(
            base for base in sequence
            if base in "ACGTN"
        )

        if not sequence:
            return result

        # -----------------------------------------------------
        # Calculate GC content
        # -----------------------------------------------------
        gc_count = sequence.count("G") + sequence.count("C")
        gc_content = round(
            (gc_count / len(sequence)) * 100,
            2
        )

        return {
            "accession": nucleotide_id,
            "sequence": sequence,
            "length": len(sequence),
            "gc_content": gc_content,
            "description": description
        }

    except requests.RequestException:
        return result

    except Exception:
        return result
            }
    except Exception:
        pass

    return results
