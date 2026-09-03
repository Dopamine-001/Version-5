import requests
2
 
3
NCBI_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
4
 
5
 
6
def lookup_ensembl_id(gene_symbol, organism="human"):
7
"""
8
Returns NCBI Gene ID.
9
"""
10
 
11
response = requests.get(
12
f"{NCBI_EUTILS}/esearch.fcgi",
13
params={
14
"db": "gene",
15
"term": f"{gene_symbol}[Gene Name] AND {organism}[Organism]",
16
"retmode": "json",
17
},
18
timeout=30,
19
)
20
 
21
response.raise_for_status()
22
 
23
data = response.json()
24
 
25
ids = data["esearchresult"]["idlist"]
26
 
27
if not ids:
28
return None
29
 
30
return ids[0]
31
 
32
 
33
def fetch_ensembl_sequence(gene_symbol):
34
"""
35
Fetches nucleotide sequence from NCBI.
36
"""
37
 
38
gene_id = lookup_ensembl_id(gene_symbol)
39
 
40
if not gene_id:
41
return None
42
 
43
link_response = requests.get(
44
f"{NCBI_EUTILS}/elink.fcgi",
45
params={
46
"dbfrom": "gene",
47
"db": "nuccore",
48
"id": gene_id,
49
"retmode": "json",
50
},
51
timeout=30,
52
)
53
 
54
link_response.raise_for_status()
55
 
56
link_data = link_response.json()
57
 
58
nucleotide_ids = []
59
 
60
for linkset in link_data.get("linksets", []):
61
for db in linkset.get("linksetdbs", []):
62
nucleotide_ids.extend(db.get("links", []))
63
 
64
if not nucleotide_ids:
65
return None
66
 
67
nucleotide_id = nucleotide_ids[0]
68
 
69
fasta_response = requests.get(
70
f"{NCBI_EUTILS}/efetch.fcgi",
71
params={
72
"db": "nuccore",
73
"id": nucleotide_id,
74
"rettype": "fasta",
75
"retmode": "text",
76
},
77
timeout=30,
78
)
79
 
80
fasta_response.raise_for_status()
81
 
82
fasta = fasta_response.text
83
 
84
lines = fasta.splitlines()
85
 
86
if len(lines) < 2:
87
return None
88
 
89
return "".join(lines[1:])
