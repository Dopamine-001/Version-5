from __future__ import annotations

import base64

def render_structure(
    pdb_text: str,
    representation: str = "Cartoon",
    color_style: str = "Spectrum",
    spin: bool = False,
    highlight_position: int | None = None,
    highlight_mode: str = "Stick",
    camera: str = "Default",
) -> str:
    """Generates an interactive 3Dmol.js viewer HTML string for primary structures."""
    encoded_pdb = base64.b64encode(pdb_text.encode("utf-8")).decode("utf-8")
    
    rep_map = {
        "Stick": "stick",
        "Sphere": "sphere",
        "Cartoon": "cartoon",
        "Ribbon": "ribbon",
        "Line": "line",
        "Surface": "surface",
    }
    rep = rep_map.get(representation, "cartoon")

    color_js = "viewer.setStyle({}, {cartoon: {color: 'spectrum'}});"
    if color_style == "Chain":
        color_js = "viewer.setStyle({}, {cartoon: {color: 'chain'}});"
    elif color_style == "Uniform":
        color_js = "viewer.setStyle({}, {cartoon: {color: '#05D9E8'}});"
    elif color_style == "Secondary structure":
        color_js = """
            viewer.setStyle({ss: 'h'}, {cartoon: {color: '#FF2A6D'}});
            viewer.setStyle({ss: 's'}, {cartoon: {color: '#05D9E8'}});
            viewer.setStyle({ss: 'c'}, {cartoon: {color: '#8FA3BF'}});
        """

    highlight_js = ""
    if highlight_position is not None:
        hm = "stick" if highlight_mode == "Stick" else "sphere"
        highlight_js = f"""
            viewer.addStyle({{resi: {highlight_position}}}, {{{hm}: {{color: 'yellow', radius: 0.3}}}});
        """

    camera_js = ""
    if camera == "Front":
        camera_js = "viewer.zoomTo();"
    elif camera == "Side":
        camera_js = "viewer.rotate(90, {x: 0, y: 1, z: 0});"
    elif camera == "Top":
        camera_js = "viewer.rotate(90, {x: 1, y: 0, z: 0});"

    spin_code = "viewer.spin(true);" if spin else "viewer.spin(false);"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax5/libs/3Dmol/2.0.3/3Dmol-min.js"></script>
        <style>
            html, body, #container {{ width: 100%; height: 100%; margin: 0; background-color: #0b0f19; }}
        </style>
    </head>
    <body>
        <div id="container"></div>
        <script>
            let pdbData = atob("{encoded_pdb}");
            let element = document.getElementById("container");
            let config = {{ backgroundColor: "#0b0f19" }};
            let viewer = $3Dmol.createViewer(element, config);
            viewer.addModel(pdbData, "pdb");
            
            viewer.setStyle({{}}, {{{rep}: {{color: 'spectrum'}}}});
            {color_js}
            {highlight_js}
            
            viewer.zoomTo();
            {camera_js}
            {spin_code}
            
            let rotationTimer = null;
            function toggleSpin(enabled) {{
                viewer.spin(enabled);
            }}
            
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
    """Generates a 3Dmol.js viewer explicitly colored by computed secondary structure across all chains."""
    encoded_pdb = base64.b64encode(pdb_text.encode("utf-8")).decode("utf-8")
    
    rep_map = {
        "Cartoon": "cartoon",
        "Ribbon": "ribbon",
        "Trace": "trace",
        "Tube": "tube"
    }
    rep = rep_map.get(representation, "cartoon")

    # Build individual residue color selectors based on sec_struct dictionary
    helix_res = [str(k) for k, v in sec_struct.items() if v == "H"]
    sheet_res = [str(k) for k, v in sec_struct.items() if v == "E"]
    coil_res = [str(k) for k, v in sec_struct.items() if v == "C"]

    helix_selector = ", ".join(helix_res) if helix_res else "-1"
    sheet_selector = ", ".join(sheet_res) if sheet_res else "-1"
    coil_selector = ", ".join(coil_res) if coil_res else "-1"

    coil_display = "true" if show_coils else "false"

    camera_js = ""
    if camera == "Front":
        camera_js = "viewer.zoomTo();"
    elif camera == "Side":
        camera_js = "viewer.rotate(90, {x: 0, y: 1, z: 0});"
    elif camera == "Top":
        camera_js = "viewer.rotate(90, {x: 1, y: 0, z: 0});"

    spin_code = "viewer.spin(true);" if spin else "viewer.spin(false);"

    highlight_js = ""
    if highlight_position is not None:
        highlight_js = f"viewer.addStyle({{resi: {highlight_position}}}, {{stick: {{color: 'yellow', radius: 0.3}}}});"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.3/3Dmol-min.js"></script>
        <style>
            html, body, #container {{ width: 100%; height: {height}px; margin: 0; background-color: #0b0f19; }}
        </style>
    </head>
    <body>
        <div id="container"></div>
        <script>
            let pdbData = atob("{encoded_pdb}");
            let element = document.getElementById("container");
            let config = {{ backgroundColor: "#0b0f19" }};
            let viewer = $3Dmol.createViewer(element, config);
            viewer.addModel(pdbData, "pdb");

            // Default base style
            viewer.setStyle({{}}, {{{rep}: {{color: '#8FA3BF'}}}});

            // Color helices (Alpha-helix: Red/Pink #FF2A6D)
            viewer.setStyle({{resi: [{helix_selector}]}}, {{{rep}: {{color: '#FF2A6D'}}}});

            // Color sheets (Beta-sheet: Cyan #05D9E8)
            viewer.setStyle({{resi: [{sheet_selector}]}}, {{{rep}: {{color: '#05D9E8'}}}});

            // Color coils / loops
            if ({coil_display}) {{
                viewer.setStyle({{resi: [{coil_selector}]}}, {{{rep}: {{color: '#8FA3BF'}}}});
            }} else {{
                viewer.setStyle({{resi: [{coil_selector}]}}, {{hidden: true}});
            }}

            {highlight_js}
            viewer.zoomTo();
            {camera_js}
            {spin_code}
            viewer.render();
        </script>
    </body>
    </html>
    """
    return html
