# core/blast.py
from __future__ import annotations

import time
import io
import requests
from Bio.Blast import NCBIXML


def run_blast_search(sequence: str, max_wait_seconds: int = 90) -> list[dict]:
    """
    Submits a protein sequence to NCBI BLAST (blastp against nr) and
    polls until results are ready. Returns a list of top hits, each
    with a title, percent identity, and E-value.
    """
    submit_url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
    submit_params = {
        "CMD": "Put",
        "PROGRAM": "blastp",
        "DATABASE": "nr",
        "QUERY": sequence[:2000],
        "EXPECT": "10",
        "FORMAT_TYPE": "XML",
    }
    
    try:
        submit_resp = requests.post(submit_url, data=submit_params, timeout=30)
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
        while waited < max_wait_seconds:
            time.sleep(5)
            waited += 5
            status_resp = requests.get(submit_url, params=status_params, timeout=30)
            if "Status=READY" in status_resp.text:
                break
            elif "Status=FAILED" in status_resp.text or "Status=UNKNOWN" in status_resp.text:
                return []
        else:
            return []  # Timed out

        result_params = {"CMD": "Get", "FORMAT_TYPE": "XML", "RID": rid}
        result_resp = requests.get(submit_url, params=result_params, timeout=30)
        result_resp.raise_for_status()

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
