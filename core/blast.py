from __future__ import annotations

import time
import io
import requests
import streamlit as st
from Bio.Blast import NCBIXML

# Cache the results for 24 hours so you only wait once per sequence!
@st.cache_data(show_spinner=False, ttl=86400)
def run_blast_search(sequence: str, max_wait_seconds: int = 180) -> list[dict]:
    """
    Submits a protein sequence to NCBI BLAST safely with extended timeout 
    and explicit error reporting.
    """
    submit_url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
    submit_params = {
        "CMD": "Put",
        "PROGRAM": "blastp",
        "DATABASE": "swissprot", 
        "QUERY": sequence[:1000],
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
            return [{"error": "Failed to receive a Request ID (RID) from NCBI servers."}]

        status_params = {"CMD": "Get", "FORMAT_OBJECT": "SearchInfo", "RID": rid}
        waited = 0
        
        # Poll NCBI (checking every 10 seconds to avoid being rate-limited)
        while waited < max_wait_seconds:
            time.sleep(10)
            waited += 10
            status_resp = requests.get(submit_url, params=status_params, timeout=20)
            
            if "Status=READY" in status_resp.text:
                if "ThereAreHits=yes" in status_resp.text:
                    break
                elif "ThereAreHits=no" in status_resp.text:
                    return [] # Genuine lack of homologs
                break
            elif "Status=FAILED" in status_resp.text or "Status=UNKNOWN" in status_resp.text:
                return [{"error": "NCBI Server failed to process the request."}]
        else:
            return [{"error": f"Search timed out after {max_wait_seconds}s. NCBI is under heavy load."}]

        # Fetch XML results
        result_params = {"CMD": "Get", "FORMAT_TYPE": "XML", "RID": rid}
        result_resp = requests.get(submit_url, params=result_params, timeout=30)
        result_resp.raise_for_status()

        if "<Hit>" not in result_resp.text:
            return []

        blast_record = NCBIXML.read(io.StringIO(result_resp.text))
        
        hits = []
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                identity_pct = round((hsp.identities / hsp.align_length) * 100, 1) if hsp.align_length > 0 else 0.0
                
                # Format exactly as the Streamlit UI expects
                hits.append({
                    "Match Title": alignment.title[:80] + "..." if len(alignment.title) > 80 else alignment.title,
                    "Length": alignment.length,
                    "Identity": f"{identity_pct}%",
                    "E-Value": f"{hsp.expect:.2e}"
                })
                break # Only take the best matching segment per protein
            if len(hits) >= 15:
                break

        return hits

    except Exception as e:
        return [{"error": f"Network exception: {str(e)}"}]
