# core/blast.py
from __future__ import annotations

import time
import io
import requests
from Bio.Blast import NCBIXML


def run_blast_search(sequence: str, max_wait_seconds: int = 60) -> list[dict]:
    """
    Submits a protein sequence to NCBI BLAST (blastp against swissprot) 
    for fast, reliable homology matching.
    """
    submit_url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
    submit_params = {
        "CMD": "Put",
        "PROGRAM": "blastp",
        "DATABASE": "swissprot",  # swissprot is much faster and more reliable than 'nr'
        "QUERY": sequence[:1000],   # Truncate long sequences for faster processing
        "EXPECT": "10",
        "FORMAT_TYPE": "XML",
    }
    
    try:
        submit_resp = requests.post(submit_url, data=submit_params, timeout=20)
        submit_resp.raise_for_status()

        rid = None
        for line in submit_resp.text.splitlines():
            if "RID = " in line:
                rid = line.split("RID = ")[1].strip()
                break

        if not rid:
            return []

        status_params = {"CMD": "Get", "FORMAT_OBJECT": "SearchInfo", "RID": rid}
        waited = 0
        
        # Poll NCBI for results with status checking
        while waited < max_wait_seconds:
            time.sleep(4)
            waited += 4
            status_resp = requests.get(submit_url, params=status_params, timeout=20)
            
            if "Status=READY" in status_resp.text:
                # Check if it actually has hit data ready
                if "ThereAreHits=yes" in status_resp.text or "Status=READY" in status_resp.text:
                    break
            elif "Status=FAILED" in status_resp.text or "Status=UNKNOWN" in status_resp.text:
                return []
        else:
            return []  # Timed out

        # Fetch XML results
        result_params = {"CMD": "Get", "FORMAT_TYPE": "XML", "RID": rid}
        result_resp = requests.get(submit_url, params=result_params, timeout=25)
        result_resp.raise_for_status()

        if "<Hit>" not in result_resp.text:
            return []

        blast_record = NCBIXML.read(io.StringIO(result_resp.text))
        
        hits = []
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                identity_pct = round((hsp.identities / hsp.align_length) * 100, 1) if hsp.align_length > 0 else 0.0
                hits.append({
                    "title": alignment.title,
                    "accession": alignment.accession,
                    "length": alignment.length,
                    "e_value": f"{hsp.expect:.2e}",
                    "identities_pct": f"{identity_pct}%",
                    "score": hsp.score
                })
                break
            if len(hits) >= 10:
                break

        return hits

    except Exception as e:
        print(f"BLAST Execution Error: {e}")
        return []
