"""Interactive py3Dmol renderer for AlphaFold PDB structures."""
from __future__ import annotations

import json
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


def _escape_pdb_for_js(pdb_text: str) -> str:
    """Make a PDB string safe inside a JS template literal."""
    return (
        pdb_text.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )


def _ranges_to_resi(ranges) -> list:
    """Flatten [{'start':a,'end':b}, ...] into a sorted unique residue list."""
    resi = []
    for item in ranges or []:
        try:
            start, end = int(item["start"]), int(item["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if end < start:
            start, end = end, start
        resi.extend(range(start, end + 1))
    return sorted(set(resi))


def render_secondary_structure_3d(
    pdb_text: str,
    sec_struct: dict,
    height: int = 560,
    spin: bool = False,
    show_coils: bool = True,
    background: str = "#061126",
) -> str:
    """Render a detailed 3D secondary-structure view.

    α-helices -> red/pink cartoon
    β-sheets  -> cyan directional arrows
    turns     -> amber cartoon
    coils     -> neutral grey trace
    ligands   -> green sticks
    """

    if not pdb_text or not pdb_text.strip():
        return (
            "<div style='padding:2rem;color:#d7e8ff;"
            "font-family:Arial'>"
            "No PDB structure available."
            "</div>"
        )

    sec_struct = sec_struct or {}

    helix_resi = _ranges_to_resi(
        sec_struct.get("helices")
    )

    sheet_resi = _ranges_to_resi(
        sec_struct.get("sheets")
    )

    turn_resi = _ranges_to_resi(
        sec_struct.get("turns")
    )

    # ---------------------------------------------------------
    # Prevent residues from being assigned to two categories.
    # Priority:
    # helix > sheet > turn > coil
    # ---------------------------------------------------------

    helix_set = set(helix_resi)
    sheet_set = set(sheet_resi)

    turn_resi = [
        r for r in turn_resi
        if r not in helix_set
        and r not in sheet_set
    ]

    claimed = (
        helix_set
        | sheet_set
        | set(turn_resi)
    )

    viewer = py3Dmol.view(
        width="100%",
        height=height,
    )

    viewer.setBackgroundColor(background)

    viewer.addModel(
        pdb_text,
        "pdb",
    )

    selection = {
        "model": 0,
    }

    # ---------------------------------------------------------
    # Start with a clean model.
    # ---------------------------------------------------------

    viewer.setStyle(
        selection,
        {},
    )

    # ---------------------------------------------------------
    # COILS / LOOPS
    # ---------------------------------------------------------

    if show_coils:
        viewer.setStyle(
            {
                "model": 0,
                "hetflag": False,
                "resi": [
                    r
                    for r in range(
                        1,
                        max(
                            helix_resi
                            + sheet_resi
                            + turn_resi
                            + [1]
                        )
                        + 1,
                    )
                    if r not in claimed
                ],
            },
            {
                "cartoon": {
                    "color": "#8FA3BF",
                    "style": "trace",
                    "thickness": 0.35,
                    "opacity": 0.90,
                }
            },
        )

    # ---------------------------------------------------------
    # ALPHA HELICES
    # ---------------------------------------------------------

    if helix_resi:
        viewer.setStyle(
            {
                "model": 0,
                "resi": helix_resi,
            },
            {
                "cartoon": {
                    "color": "#FF2A6D",
                    "style": "oval",
                    "thickness": 0.9,
                    "arrows": False,
                    "opacity": 1.0,
                }
            },
        )

    # ---------------------------------------------------------
    # BETA SHEETS
    # ---------------------------------------------------------

    if sheet_resi:
        viewer.setStyle(
            {
                "model": 0,
                "resi": sheet_resi,
            },
            {
                "cartoon": {
                    "color": "#05D9E8",
                    "style": "arrow",
                    "thickness": 0.9,
                    "arrows": True,
                    "opacity": 1.0,
                }
            },
        )

    # ---------------------------------------------------------
    # TURNS
    # ---------------------------------------------------------

    if turn_resi:
        viewer.setStyle(
            {
                "model": 0,
                "resi": turn_resi,
            },
            {
                "cartoon": {
                    "color": "#FFB703",
                    "style": "oval",
                    "thickness": 0.55,
                    "opacity": 0.95,
                }
            },
        )

    # ---------------------------------------------------------
    # LIGANDS / HETEROATOMS
    # ---------------------------------------------------------

    viewer.addStyle(
        {
            "model": 0,
            "hetflag": True,
        },
        {
            "stick": {
                "radius": 0.18,
                "colorscheme": "greenCarbon",
            },
            "sphere": {
                "scale": 0.22,
            },
        },
    )

    # ---------------------------------------------------------
    # WATER
    # ---------------------------------------------------------

    viewer.setStyle(
        {
            "model": 0,
            "resn": "HOH",
        },
        {
            "sphere": {
                "scale": 0.18,
                "color": "#6EC6FF",
                "opacity": 0.45,
            }
        },
    )

    # ---------------------------------------------------------
    # FRAME THE COMPLETE STRUCTURE
    # ---------------------------------------------------------

    viewer.zoomTo(selection)

    # ---------------------------------------------------------
    # Spin
    # ---------------------------------------------------------

    if spin:
        viewer.spin("y", 1)
    else:
        viewer.spin(False)

    viewer.render()

    return viewer._make_html()
