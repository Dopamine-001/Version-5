from __future__ import annotations

import xml.etree.ElementTree as ET

from core.helpers import safe_get


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


def get_ncbi_gene_info(protein_name):
    """
    Retrieve detailed human Gene information from NCBI.

    Uses:
    - ESearch to identify the NCBI Gene record.
    - ESummary for basic Gene metadata.
    - EFetch for the detailed Gene XML record.
    """

    # ======================================================
    # 1. SEARCH NCBI GENE
    # ======================================================

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

        search_data = search_response.json()

        id_list = (
            search_data
            .get("esearchresult", {})
            .get("idlist", [])
        )

        if not id_list:
            return None

        gene_id = id_list[0]

        # ==================================================
        # 2. E-SUMMARY
        # ==================================================

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

        summary_data = summary_response.json()

        result = (
            summary_data
            .get("result", {})
            .get(gene_id, {})
        )

        # ==================================================
        # 3. E-FETCH FULL GENE XML
        # ==================================================

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

        xml_root = ET.fromstring(
            fetch_response.text
        )

        # ==================================================
        # 4. BASIC IDENTITY
        # ==================================================

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

        organism = (
            result.get("organism", {})
        )

        if isinstance(organism, dict):
            organism_name = organism.get(
                "scientificname",
                "Homo sapiens",
            )
        else:
            organism_name = str(
                organism or "Homo sapiens"
            )

        # ==================================================
        # 5. ALIASES
        # ==================================================

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
            other_aliases = result.get(
                "otheraliases"
            )

            if other_aliases:
                aliases = [
                    x.strip()
                    for x in str(
                        other_aliases
                    ).split(",")
                    if x.strip()
                ]

        # Remove duplicates
        aliases = list(
            dict.fromkeys(aliases)
        )

        # ==================================================
        # 6. CHROMOSOME / MAP LOCATION
        # ==================================================

        chromosome = (
            result.get("chromosome")
            or _text(
                xml_root,
                ".//Gene-commentary_chromosome",
            )
            or "Unknown"
        )

        map_location = (
            result.get("maplocation")
            or "Unknown"
        )

        # ==================================================
        # 7. GENE TYPE
        # ==================================================

        gene_type = (
            result.get("genetype")
            or "Not available"
        )

        # ==================================================
        # 8. STATUS
        # ==================================================

        status = (
            result.get("status")
            or "Not available"
        )

        # ==================================================
        # 9. SUMMARY / DESCRIPTION
        # ==================================================

        summary = (
            result.get("summary")
            or "No summary available."
        )

        # ==================================================
        # 10. OTHER DESIGNATIONS
        # ==================================================

        designations = _collect_texts(
            xml_root,
            ".//Gene-ref_syn/Gene-ref_syn_Other",
        )

        # ==================================================
        # 11. NOMENCLATURE
        # ==================================================

        nomenclature_symbol = (
            result.get(
                "nomenclaturesymbol"
            )
            or gene_symbol
        )

        nomenclature_full_name = (
            result.get(
                "nomenclaturefullname"
            )
            or gene_name
        )

        # ==================================================
        # 12. CROSS REFERENCES
        # ==================================================

        db_references = []

        for dbtag in xml_root.findall(
            ".//Dbtag"
        ):
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

        # ==================================================
        # 13. RETURN EVERYTHING
        # ==================================================

        return {
            "gene_id": gene_id,

            "gene_symbol": gene_symbol,

            "gene_name": gene_name,

            "description": gene_name,

            "organism": organism_name,

            "chromosome": chromosome,

            "map_location": map_location,

            "genomic_location": map_location,

            "gene_type": gene_type,

            "status": status,

            "aliases": aliases,

            "other_designations": designations,

            "summary": summary,

            "nomenclature_symbol": nomenclature_symbol,

            "nomenclature_full_name": nomenclature_full_name,

            "cross_references": db_references,

            "ncbi_gene_url": (
                "https://www.ncbi.nlm.nih.gov/"
                f"gene/{gene_id}"
            ),
        }

    except Exception:
        return None
