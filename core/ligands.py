from __future__ import annotations

def extract_ligands_from_pdb(pdb_text: str) -> list[dict]:
    """Scans PDB text content for HETATM lines to identify bound ligands/molecules."""
    ligands = []
    seen = set()
    
    if not pdb_text:
        return ligands

    for line in pdb_text.splitlines():
        if line.startswith("HETATM"):
            # Standard PDB format slicing for residue name, chain, and sequence number
            resname = line[17:20].strip()
            chain = line[21:22].strip()
            resseq = line[22:26].strip()
            
            # Filter out standard water molecules and ions like HOH, WAT, DOD
            if resname in ["HOH", "WAT", "DOD"]:
                continue
                
            identifier = f"{resname}_{chain}_{resseq}"
            if identifier not in seen:
                seen.add(identifier)
                ligands.append({
                    "resname": resname,
                    "chain": chain,
                    "resseq": resseq,
                    "label": f"{resname} (Chain {chain}, Res {resseq})"
                })
                
    return ligands
