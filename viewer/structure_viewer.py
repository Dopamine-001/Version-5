from __future__ import annotations

import json


def render_structure(
    pdb_text: str,
    representation: str = "Cartoon",
    color_style: str = "Spectrum",
    spin: bool = False,
    highlight_position: int | None = None,
    highlight_mode: str = "Stick",
    camera: str = "Default",
) -> str:
    """Generates an interactive, robust 3Dmol.js viewer HTML string for primary structures."""
    pdb_json = json.dumps(pdb_text)
    
    rep_map = {
        "Stick": "stick",
        "Sphere": "sphere",
        "Cartoon": "cartoon",
        "Ribbon": "ribbon",
        "Line": "line",
        "Surface": "surface",
    }
    rep = rep_map.get(representation, "cartoon")

    # Configure color logic
    color_js = "viewer.setStyle({}, {" + rep + ": {color: 'spectrum'}});"
    if color_style == "Chain":
        color_js = "viewer.setStyle({}, {" + rep + ": {color: 'chain'}});"
    elif color_style == "Uniform":
        color_js = "viewer.setStyle({}, {" + rep + ": {color: '#05D9E8'}});"
    elif color_style == "Secondary structure":
        color_js = f"""
            viewer.setStyle({{ss: 'h'}}, {{{rep}: {{color: '#FF2A6D'}}}});
            viewer.setStyle({{ss: 's'}}, {{{rep}: {{color: '#05D9E8'}}}});
            viewer.setStyle({{ss: 'c'}}, {{{rep}: {{color: '#8FA3BF'}}}});
        """

    # Surface representation needs special handling in 3Dmol.js
    extra_rep_js = ""
    if representation == "Surface":
        extra_rep_js = "viewer.addSurface($3Dmol.SurfaceType.VDW, {opacity: 0.85, color: 'spectrum'});"

    highlight_js = ""
    if highlight_position is not None:
        hm = "stick" if highlight_mode == "Stick" else "sphere"
        highlight_js = f"""
            viewer.addStyle({{resi: {highlight_position}}}, {{{hm}: {{color: 'yellow', radius: 0.4}}}});
        """

    camera_js = "viewer.zoomTo();"
    if camera == "Front":
        camera_js = "viewer.zoomTo();"
    elif camera == "Side":
        camera_js = "viewer.zoomTo(); viewer.rotate(90, {{x: 0, y: 1, z: 0}});"
    elif camera == "Top":
        camera_js = "viewer.zoomTo(); viewer.rotate(90, {{x: 1, y: 0, z: 0}});"

    spin_code = "viewer.spin(true);" if spin else "viewer.spin(false);"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.3/3Dmol-min.js"></script>
        <style>
            html, body, #container {{ width: 100%; height: 100%; margin: 0; background-color: #0b0f19; overflow: hidden; }}
        </style>
    </head>
    <body>
        <div id="container"></div>
        <script>
            let pdbData = {pdb_json};
            let element = document.getElementById("container");
            let config = {{ backgroundColor: "#0b0f19" }};
            let viewer = $3Dmol.createViewer(element, config);
            
            viewer.addModel(pdbData, "pdb");
            
            viewer.setStyle({{}}, {{{rep}: {{color: 'spectrum'}}}});
            {color_js}
            {extra_rep_js}
            {highlight_js}
            
            {camera_js}
            {spin_code}
            
            viewer.render();
        </script>
    </body>
    </html>
    """
    return html


def render_secondary_structure_3d(
    pdb_text: str,
    sec_struct: dict,
    height: int = 560,
    spin: bool = False,
    show_coils: bool = True,
    representation: str = "Cartoon",
    camera: str = "Default",
    highlight_position: int | None = None,
) -> str:
    """Generates a 3Dmol.js secondary structure viewer supporting all representations."""
    pdb_json = json.dumps(pdb_text)
    
    rep_map = {
        "Cartoon": "cartoon",
        "Ribbon": "ribbon",
        "Trace": "trace",
        "Tube": "tube",
        "Stick": "stick",
        "Sphere": "sphere",
        "Surface": "surface"
    }
    rep = rep_map.get(representation, "cartoon")

    helix_res = [str(k) for k, v in sec_struct.items() if v == "H"]
    sheet_res = [str(k) for k, v in sec_struct.items() if v == "E"]
    coil_res = [str(k) for k, v in sec_struct.items() if v == "C"]

    helix_selector = ", ".join(helix_res) if helix_res else "-1"
    sheet_selector = ", ".join(sheet_res) if sheet_res else "-1"
    coil_selector = ", ".join(coil_res) if coil_res else "-1"

    camera_js = "viewer.zoomTo();"
    if camera == "Front":
        camera_js = "viewer.zoomTo();"
    elif camera == "Side":
        camera_js = "viewer.zoomTo(); viewer.rotate(90, {{x: 0, y: 1, z: 0}});"
    elif camera == "Top":
        camera_js = "viewer.zoomTo(); viewer.rotate(90, {{x: 1, y: 0, z: 0}});"

    spin_code = "viewer.spin(true);" if spin else "viewer.spin(false);"

    highlight_js = ""
    if highlight_position is not None:
        highlight_js = f"viewer.addStyle({{resi: {highlight_position}}}, {{stick: {{color: 'yellow', radius: 0.4}}}});"

    coil_action = f"viewer.setStyle({{resi: [{coil_selector}]}}, {{{rep}: {{color: '#8FA3BF'}}}});" if show_coils else f"viewer.setStyle({{resi: [{coil_selector}]}}, {{hidden: true}});"

    extra_surface_js = ""
    if representation == "Surface":
        extra_surface_js = "viewer.addSurface($3Dmol.SurfaceType.VDW, {opacity: 0.85, color: '#8FA3BF'});"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.3/3Dmol-min.js"></script>
        <style>
            html, body, #container {{ width: 100%; height: {height}px; margin: 0; background-color: #0b0f19; overflow: hidden; }}
        </style>
    </head>
    <body>
        <div id="container"></div>
        <script>
            let pdbData = {pdb_json};
            let element = document.getElementById("container");
            let config = {{ backgroundColor: "#0b0f19" }};
            let viewer = $3Dmol.createViewer(element, config);
            
            viewer.addModel(pdbData, "pdb");

            // Base fallback style
            viewer.setStyle({{}}, {{{rep}: {{color: '#8FA3BF'}}}});

            // Colored assignments by secondary structure
            viewer.setStyle({{resi: [{helix_selector}]}}, {{{rep}: {{color: '#FF2A6D'}}}});
            viewer.setStyle({{resi: [{sheet_selector}]}}, {{{rep}: {{color: '#05D9E8'}}}});
            {coil_action}
            {extra_surface_js}

            {highlight_js}
            {camera_js}
            {spin_code}
            
            viewer.render();
        </script>
    </body>
    </html>
    """
    return html
