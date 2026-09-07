from __future__ import annotations

import io
import plotly.graph_objects as go
import numpy as np
from Bio.PDB import PDBParser


def plddt_figure(plddt_scores: list[float]) -> go.Figure:
    """Generates a confidence score distribution chart for AlphaFold models."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=plddt_scores,
            mode="lines",
            name="pLDDT",
            line=dict(color="#05D9E8", width=2),
        )
    )
    fig.update_layout(
        title="AlphaFold pLDDT Confidence per Residue",
        xaxis_title="Residue Index",
        yaxis_title="pLDDT Score",
        template="plotly_dark",
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        margin=dict(l=40, r=40, t=40, b=40),
    )
    return fig


def ramachandran_figure(
    phi: list[float],
    psi: list[float],
    residue_numbers: list[int],
    sequence: str | None = None,
) -> go.Figure:
    """Generates a high-end, publication-quality aesthetic Ramachandran plot with smooth quadrant styling."""
    fig = go.Figure()

    fig.add_shape(
        type="rect",
        x0=-140, y0=-70, x1=-30, y1=-10,
        fillcolor="rgba(5, 217, 232, 0.12)",
        line=dict(color="rgba(5, 217, 232, 0.3)", width=1, dash="dot"),
        layer="below",
    )
    fig.add_shape(
        type="rect",
        x0=-160, y0=70, x1=-80, y1=160,
        fillcolor="rgba(255, 42, 109, 0.10)",
        line=dict(color="rgba(255, 42, 109, 0.3)", width=1, dash="dot"),
        layer="below",
    )

    res_list = list(sequence) if sequence and len(sequence) == len(phi) else ["X"] * len(phi)
    
    reg_phi, reg_psi, reg_text = [], [], []
    gly_phi, gly_psi, gly_text = [], [], []
    pro_phi, pro_psi, pro_text = [], [], []
    out_phi, out_psi, out_text = [], [], []

    for p, ps, rn, aa in zip(phi, psi, residue_numbers, res_list):
        is_outlier = (p > 0 and not (-90 < ps < 90)) or (abs(p) < 20 and abs(ps) < 20)
        
        label = f"{aa}{rn}"
        if is_outlier:
            out_phi.append(p)
            out_psi.append(ps)
            out_text.append(f"<b>⚠️ OUTLIER</b><br>Residue: {label}<br>φ: {p:.1f}° | ψ: {ps:.1f}°")
        elif aa == "G":
            gly_phi.append(p)
            gly_psi.append(ps)
            gly_text.append(f"<b>Glycine (G)</b><br>Residue: {label}<br>φ: {p:.1f}° | ψ: {ps:.1f}°")
        elif aa == "P":
            pro_phi.append(p)
            pro_psi.append(ps)
            pro_text.append(f"<b>Proline (P)</b><br>Residue: {label}<br>φ: {p:.1f}° | ψ: {ps:.1f}°")
        else:
            reg_phi.append(p)
            reg_psi.append(ps)
            reg_text.append(f"<b>Residue</b><br>Name: {label}<br>φ: {p:.1f}° | ψ: {ps:.1f}°")

    if reg_phi:
        fig.add_trace(
            go.Scatter(
                x=reg_phi,
                y=reg_psi,
                mode="markers",
                name="General Residues",
                marker=dict(size=7, color="#05D9E8", opacity=0.85, line=dict(width=0.5, color="#ffffff")),
                text=reg_text,
                hoverinfo="text",
            )
        )

    if gly_phi:
        fig.add_trace(
            go.Scatter(
                x=gly_phi,
                y=gly_psi,
                mode="markers",
                name="Glycine (G)",
                marker=dict(size=8, color="#FFB703", symbol="triangle-up", line=dict(width=0.5, color="#ffffff")),
                text=gly_text,
                hoverinfo="text",
            )
        )

    if pro_phi:
        fig.add_trace(
            go.Scatter(
                x=pro_phi,
                y=pro_psi,
                mode="markers",
                name="Proline (P)",
                marker=dict(size=8, color="#2ec4b6", symbol="square", line=dict(width=0.5, color="#ffffff")),
                text=pro_text,
                hoverinfo="text",
            )
        )

    if out_phi:
        fig.add_trace(
            go.Scatter(
                x=out_phi,
                y=out_psi,
                mode="markers",
                name="Outliers",
                marker=dict(size=10, color="#FF2A6D", symbol="x", line=dict(width=1.5, color="#ffffff")),
                text=out_text,
                hoverinfo="text",
            )
        )

    fig.update_layout(
        title=dict(text="<b>Ramachandran Conformational Space</b>", font=dict(size=16, color="#f0f6fc")),
        xaxis_title=dict(text="Dihedral Angle φ (degrees)", font=dict(color="#8b949e")),
        yaxis_title=dict(text="Dihedral Angle ψ (degrees)", font=dict(color="#8b949e")),
        xaxis=dict(
            range=[-185, 185],
            zeroline=True,
            zerolinecolor="rgba(255, 255, 255, 0.15)",
            gridcolor="rgba(255, 255, 255, 0.05)",
            tickfont=dict(color="#8b949e"),
        ),
        yaxis=dict(
            range=[-185, 185],
            zeroline=True,
            zerolinecolor="rgba(255, 255, 255, 0.15)",
            gridcolor="rgba(255, 255, 255, 0.05)",
            tickfont=dict(color="#8b949e"),
        ),
        template="plotly_dark",
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        margin=dict(l=60, r=40, t=60, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1,
            bgcolor="rgba(11, 15, 25, 0.6)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1,
            font=dict(color="#c9d1d9"),
        ),
        hoverlabel=dict(
            bgcolor="#161b22",
            font_color="#f0f6fc",
            font_family="monospace",
            bordercolor="rgba(255, 255, 255, 0.2)",
        ),
    )
    return fig


def contact_map_figure(pdb_text: str) -> go.Figure:
    """Generates an interactive residue-residue distance matrix contact map with clean, uncluttered axes."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", io.StringIO(pdb_text))
    
    ca_atoms = []
    residue_labels = []
    
    for model in structure:
        for chain in model:
            for residue in chain:
                if "CA" in residue:
                    ca_atoms.append(residue["CA"].get_coord())
                    residue_labels.append(f"{residue.resname}{residue.id[1]}")
        break

    if not ca_atoms:
        return go.Figure()

    coords = np.array(ca_atoms)
    dist_matrix = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1)
    n_residues = len(residue_labels)

    step = max(1, n_residues // 15)
    tick_vals = list(range(0, n_residues, step))
    tick_text = [residue_labels[i] for i in tick_vals]

    fig = go.Figure(
        data=go.Heatmap(
            z=dist_matrix,
            colorscale="Viridis",
            colorbar=dict(title="Distance (Å)"),
            hovertemplate="Residue 1: %{y}<br>Residue 2: %{x}<br>Distance: %{z:.2f} Å<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="<b>Residue-Residue Contact Map (Cα Distance Matrix)</b>", font=dict(size=16, color="#f0f6fc")),
        xaxis=dict(
            title="Residue Index",
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_text,
            tickfont=dict(color="#8b949e"),
            gridcolor="rgba(255,255,255,0.05)",
        ),
        yaxis=dict(
            title="Residue Index",
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_text,
            tickfont=dict(color="#8b949e"),
            gridcolor="rgba(255,255,255,0.05)",
            autorange="reversed",
        ),
        template="plotly_dark",
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        margin=dict(l=60, r=40, t=60, b=50),
    )
    return fig
