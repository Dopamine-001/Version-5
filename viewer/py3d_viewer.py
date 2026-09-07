import py3Dmol
import streamlit as st
import streamlit.components.v1 as components


def render_structure(
    pdb_string: str,
    plddt_scores: list = None,
    color_scheme: str = "plddt",
    width: int = 700,
    height: int = 500,
) -> None:
    """Renders a 3D protein structure using py3Dmol within Streamlit."""
    view = py3Dmol.view(width=width, height=height)
    view.addModel(pdb_string, "pdb")

    if color_scheme == "plddt" and plddt_scores:
        view.setStyle(
            {},
            {
                "cartoon": {
                    "colorscheme": {
                        "prop": "b",
                        "gradient": "roygb",
                        "min": 50,
                        "max": 90,
                    }
                }
            },
        )
    else:
        view.setStyle({}, {"cartoon": {"color": "spectrum"}})

    view.zoomTo()
    html_code = view._make_html()
    components.html(html_code, height=height, width=width)
