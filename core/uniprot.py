"""UniProt REST API access and normalization for Protein Explorer."""
from __future__ import annotations

import re
from typing import Optional

import streamlit as st

from config import UNIPROT_RECORD_URL, UNIPROT_SEARCH_URL
from core.helpers import comment_text, location_text, safe_get


@st.cache_data(ttl=3600, show_spinner=False)
def search_uniprot(query: str) -> Optional[dict]:
    """Find a reviewed UniProt entry from a protein name, gene or accession."""
    query = query.strip()
    if not query:
        return None

    if re.fullmatch(r"[A-Z0-9]{6,10}", query, flags=re.I):
        direct = safe_get(UNIPROT_RECORD_URL.format(accession=query.upper()))
        if direct:
            return direct.json()

    params = {
        "query": f"({query}) AND reviewed:true",
        "fields": "accession,protein_name,gene_names,organism_name,length",
        "format": "json",
        "size": 5,
    }
    response = safe_get(UNIPROT_SEARCH_URL, params=params)
    if not response:
        return None

    results = response.json().get("results", [])
    if not results:
        return None

    accession = results[0].get("primaryAccession")
    if not accession:
        return None

    full = safe_get(UNIPROT_RECORD_URL.format(accession=accession))
    return full.json() if full else results[0]


def _feature_type(feature: dict) -> str:
    """Normalize UniProt feature names to a stable internal spelling."""
    return re.sub(r"[^A-Z0-9]+", "_", str(feature.get("type", "")).upper()).strip("_")


def normalize_uniprot_record(record: dict) -> dict:
    """Extract identity, sequence and all relevant feature annotations."""
    protein_desc = record.get("proteinDescription", {}) or {}
    recommended = protein_desc.get("recommendedName", {}) or {}
    full_name = recommended.get("fullName", {}).get("value", "Unknown protein")

    alt_names = []
    for item in protein_desc.get("alternativeNames", []) or []:
        value = item.get("fullName", {}).get("value")
        if value:
            alt_names.append(value)

    gene_names = []
    for gene in record.get("genes", []) or []:
        for key in ("geneName", "orderedLocusNames", "orfNames"):
            values = gene.get(key, []) or []
            if isinstance(values, dict):
                values = [values]
            for item in values:
                if item.get("value"):
                    gene_names.append(item["value"])

    sequence = record.get("sequence", {}).get("value", "")
    organism = record.get("organism", {}).get("scientificName", "Unknown organism")
    keywords = [x.get("name") for x in record.get("keywords", []) if x.get("name")]
    features = record.get("features", []) or []

    # UniProt feature names are intentionally grouped broadly. This is more
    # robust than assuming every protein contains the same small set of types.
    variant_types = {"VARIANT", "MUTAGEN"}
    domain_types = {
        "DOMAIN", "REGION", "MOTIF", "COILED_COIL", "COMPBIAS", "REPEAT",
        "CHAIN", "PEPTIDE", "DNA_BIND", "DNA_BINDING", "NP_BIND", "RNA_BIND",
        "ZINC_FINGER", "ZN_FING", "CROSSLINK",
    }
    site_types = {
        "SITE", "BINDING", "ACT_SITE", "METAL", "CALCIUM", "CALCIUM_BIND",
        "DNA_BIND", "DNA_BINDING", "NP_BIND", "RNA_BIND", "DISULFID",
        "CROSSLNK",
    }
    ptm_types = {
        "MOD_RES", "CARBOHYD", "LIPID", "CROSSLNK", "CROSSLINK", "INIT_MET",
        "PROPEP", "SIGNAL", "TRANSIT", "CHAIN", "PEPTIDE",
    }

    variants = [f for f in features if _feature_type(f) in variant_types]
    domains = [f for f in features if _feature_type(f) in domain_types]
    sites = [f for f in features if _feature_type(f) in site_types]
    ptms = [f for f in features if _feature_type(f) in ptm_types]

    # Keep every feature available so the UI can fall back gracefully when a
    # particular UniProt entry has unusual annotation types.
    all_features = features

    interactions = []
    for comment in record.get("comments", []) or []:
        if comment.get("commentType") == "INTERACTION":
            for item in comment.get("interactions", []) or []:
                interactions.append({
                    "Partner": item.get("interactantOne", {}).get("uniProtKBAccession", "Unknown"),
                    "Organism": item.get("organismDifferentiation", "Not specified"),
                    "Experimental": item.get("interactantTwo", {}).get("uniProtKBAccession", "Unknown"),
                })

    pdb_refs = [
        ref.get("id")
        for ref in record.get("uniProtKBCrossReferences", []) or []
        if ref.get("database") == "PDB" and ref.get("id")
    ]

    return {
        "accession": record.get("primaryAccession", ""),
        "entry_name": record.get("uniProtkbId", ""),
        "name": full_name,
        "alternative_names": alt_names,
        "gene": ", ".join(dict.fromkeys(gene_names)) or "Not specified",
        "organism": organism,
        "sequence": sequence,
        "length": len(sequence),
        "function": comment_text(record, "FUNCTION"),
        "location": location_text(next(
            (c for c in record.get("comments", []) or [] if c.get("commentType") == "SUBCELLULAR LOCATION"),
            {},
        )),
        "catalytic_activity": comment_text(record, "CATALYTIC ACTIVITY", "Not listed."),
        "disease": comment_text(record, "DISEASE", "No disease association listed."),
        "similarity": comment_text(record, "SIMILARITY", "Not listed."),
        "keywords": keywords,
        "variants": variants,
        "domains": domains,
        "sites": sites,
        "ptms": ptms,
        "all_features": all_features,
        "interactions": interactions,
        "pdb_refs": pdb_refs,
        "reviewed": bool(record.get("entryAudit")),
    }
