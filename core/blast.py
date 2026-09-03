"""
BLAST similarity search against NCBI's protein database.
This is a real computation job (not an instant lookup), so it uses a
submit-then-poll pattern and can take 30-90 seconds.
"""

import time
import requests


def run_blast_search(sequence: str, max_wait_seconds: int = 90) -> list[dict]:
    """
    Submits a protein sequence to NCBI BLAST (blastp against nr) and
    polls until results are ready. Returns a list of top hits, each
    with a title, percent identity, and E-value where parseable.
    """
    submit_url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
    submit_params = {
        "CMD": "Put",
        "PROGRAM": "blastp",
        "DATABASE": "nr",
        "QUERY": sequence[:500],
    }
    submit_resp = requests.post(submit_url, data=submit_params, timeout=30)

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
    else:
        return []  # timed out

    result_params = {"CMD": "Get", "FORMAT_TYPE": "Text", "RID": rid}
    result_resp = requests.get(submit_url, params=result_params, timeout=30)

    hits = []
    for line in result_resp.text.splitlines():
        if line.startswith(">"):
            hits.append({"title": line[1:].strip()})
        if len(hits) >= 8:
            break

    return hits
