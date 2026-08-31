"""Interactive py3Dmol renderer for AlphaFold PDB structures."""
from __future__ import annotations

from typing import Optional

import py3Dmol


COLOR_SCHEMES = {
    "Spectrum": "spectrum",
    "Chain": "chain",
    "Secondary structure": "ssPyMOL",
}


def _atom_style(representation: str, color_style: str) -> dict:
    rep = representation.strip().lower()

    if color_style == "Uniform":
        if rep == "stick":
            return {"stick": {"color": "#57d6ff", "radius": 0.18}}
        if rep == "sphere":
            return {"sphere": {"color": "#57d6ff", "scale": 0.34}}
        if rep == "line":
            return {"line": {"color": "#57d6ff", "linewidth": 1.5}}
        if rep == "ribbon":
            return {
                "cartoon": {
                    "color": "#57d6ff",
                    "ribbon": True,
                    "thickness": 0.35,
                }
            }
        return {"cartoon": {"color": "#57d6ff"}}

    scheme = COLOR_SCHEMES.get(color_style, "spectrum")

    if rep == "stick":
        return {"stick": {"colorscheme": scheme, "radius": 0.18}}
    if rep == "sphere":
        return {"sphere": {"colorscheme": scheme, "scale": 0.34}}
    if rep == "line":
        return {"line": {"colorscheme": scheme, "linewidth": 1.5}}
    if rep == "ribbon":
        return {
            "cartoon": {
                "colorscheme": scheme,
                "ribbon": True,
                "thickness": 0.35,
            }
        }
    
    return {"cartoon": {"colorscheme": scheme}}


def render_structure(
    pdb_text: str,
    representation: str = "Stick",
    color_style: str = "Spectrum",
    spin: bool = False,
    highlight_position: Optional[int] = None,
    highlight_mode: str = "Stick",
    camera: str = "Default",
) -> str:
    if not pdb_text or not pdb_text.strip():
        return (
            "<div style='padding:2rem;color:#d7e8ff;font-family:Arial'>"
            "No PDB structure available.</div>"
        )

    viewer = py3Dmol.view(width="100%", height=560)
    viewer.setBackgroundColor("#061126")
    viewer.addModel(pdb_text, "pdb")
    selection = {"model": 0}

    # Always clear the model before applying exactly one requested base
    # representation. This prevents a previous Cartoon/Ribbon style from
    # leaking into Stick/Sphere when Streamlit reruns the page.
    viewer.setStyle(selection, {})

    rep = representation.strip().lower()
    if rep == "surface":
        # Surface is the only mode that intentionally adds a surface object.
        viewer.addSurface(
            py3Dmol.VDW,
            {
                "opacity": 0.72,
                "colorscheme": COLOR_SCHEMES.get(color_style, "spectrum")
                if color_style != "Uniform"
                else None,
                "color": "#57d6ff" if color_style == "Uniform" else None,
            },
            selection,
        )
    else:
        viewer.setStyle(selection, _atom_style(representation, color_style))

    if highlight_position is not None:
        try:
            residue = int(highlight_position)
            residue_sel = {"model": 0, "resi": residue}
            if highlight_mode == "Sphere":
                viewer.addStyle(
                    residue_sel,
                    {"sphere": {"color": "#ffd166", "scale": 0.62}},
                )
            else:
                viewer.addStyle(
                    residue_sel,
                    {"stick": {"color": "#ffd166", "radius": 0.32}},
                )
        except (TypeError, ValueError):
            pass

    # Fit before and after orientation. 3Dmol documents zoomTo() as the
    # method that centers the selected atoms and adjusts the slab.
    viewer.zoomTo(selection)

    if camera == "Front":
        viewer.rotate(90, "x")
    elif camera == "Side":
        viewer.rotate(90, "y")
    elif camera == "Top":
        viewer.rotate(90, "z")

    viewer.zoomTo(selection)
    viewer.spin("y", 1) if spin else viewer.spin(False)
    viewer.render()

    return viewer._make_html()
