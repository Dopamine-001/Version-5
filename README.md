# Protein Explorer

A Streamlit bioinformatics workspace for exploring protein sequences, AlphaFold structures and UniProt annotations.

## Features

- UniProt protein search and annotation retrieval
- AlphaFold 3D structure viewer with Stick, Sphere, Cartoon, Ribbon, Line and Surface modes
- Protein sequence and physicochemical analysis
- Hydrophobicity analysis
- UniProt variants and mutation inspection
- Domains, regions, motifs and functional sites
- PTM and processing annotations
- Ramachandran analysis from the AlphaFold PDB
- Two-protein comparison
- Dark navy/cyan molecular interface with a subtle DNA background

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Streamlit Community Cloud

- Repository: your GitHub repository
- Branch: `main`
- Main file path: `app.py`

No API key is required by this version. Data are retrieved from UniProt and AlphaFold when the services are available.
