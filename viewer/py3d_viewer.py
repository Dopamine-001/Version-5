import py3Dmol
import streamlit as st
import streamlit.components.v1 as components


def render_structure(
    pdb_string: str,
    plddt_scores: list = None,
    color_scheme: str = "plddt",
    representation: str = "Cartoon",
    color_style: str = "Spectrum",
    width: int = 700,
    height: int = 500,
) -> str:
    """Renders a 3D protein structure using py3Dmol within Streamlit and returns HTML."""
    view = py3Dmol.view(width=width, height=height)
    view.addModel(pdb_string, "pdb")

    rep_lower = representation.lower()
    style_dict = {}
    if "cartoon" in rep_lower:
        style_dict["cartoon"] = {}
    elif "stick" in rep_lower:
        style_dict["stick"] = {}
    else:
        style_dict["cartoon"] = {}

    if color_scheme == "plddt" and plddt_scores:
        style_dict[list(style_dict.keys())[0]]["colorscheme"] = {
            "prop": "b",
            "gradient": "roygb",
            "min": 50,
            "max": 90,
        }
    else:
        style_dict[list(style_dict.keys())[0]]["color"] = "spectrum"

    view.setStyle({}, style_dict)
    view.zoomTo()
    html_code = view._make_html()
    
    components.html(html_code, height=height, width=width)
    return html_code
