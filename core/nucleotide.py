"""
Optional nucleotide/CDS information for Protein Explorer.

This module never interferes with the protein sequence.
If a UniProt record has an EMBL or RefSeq cross-reference,
we expose it. If it does not, we simply return an empty result.
"""

from __future__ import annotations


def get_nucleotide_references(uniprot_record: dict) -> list[dict]:
    """
    Extract nucleotide/CDS cross-references from a UniProt record.

    Returns an empty list when no nucleotide reference exists.
    """

    references = []

    for ref in uniprot_record.get("uniProtKBCrossReferences", []) or []:
        database = str(ref.get("database", "")).upper()

        if database not in {"EMBL", "REFSEQ", "DDBJ"}:
            continue

        accession = ref.get("id")

        if not accession:
            continue

        properties = ref.get("properties", []) or []

        ref_data = {
            "database": database,
            "accession": accession,
            "properties": properties,
        }

        references.append(ref_data)

    return references


def cds_status(uniprot_record: dict) -> dict:
    """
    Return a simple status describing whether nucleotide/CDS
    information is available.
    """

    references = get_nucleotide_references(uniprot_record)

    return {
        "available": bool(references),
        "references": references,
        "message": (
            "Nucleotide/CDS reference available."
            if references
            else "No nucleotide/CDS cross-reference is available for this record."
        ),
    }
