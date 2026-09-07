from __future__ import annotations

import plotly.graph_objects as go
import numpy as np


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
    """Generates an enhanced Ramachandran plot with region contours, Gly/Pro differentiation, and outlier detection."""
    fig = go.Figure()

    # Add background shaded zones for core favored regions (approximate general Ramachandran favored areas)
    # Alpha helix region (~-60, -43) and Beta sheet region (~-135, +135)
    fig.add_shape(
        type="rect",
        x0=-100, y0=-80, x1=-40, y1=-10,
        fillcolor="rgba(5, 217, 232, 0.08)",
        line=dict(width=0),
        layer="below",
    )
    fig.add_shape(
        type="rect",
        x0=-160, y0=90, x1=-100, y1=160,
        fillcolor="rgba(255, 42, 109, 0.08)",
        line=dict(width=0),
        layer="below",
    )

    # Categorize residues if sequence is provided
    res_list = list(sequence) if sequence and len(sequence) == len(phi) else ["X"] * len(phi)
    
    reg_phi, reg_psi, reg_text = [], [], []
    gly_phi, gly_psi, gly_text = [], [], []
    pro_phi, pro_psi, pro_text = [], [], []
    out_phi, out_psi, out_text = [], [], []

    for p, ps, rn, aa in zip(phi, psi, residue_numbers, res_list):
        # Simple heuristic for disallowed / outlier space (e.g., positive phi outside specific loops)
        is_outlier = (p > 0 and not (-90 < ps < 90)) or (abs(p) < 20 and abs(ps) < 20)
        
        label = f"{aa}{rn}"
        if is_outlier:
            out_phi.append(p)
            out_psi.append(ps)
            out_text.append(f"<b>OUTLIER</b><br>{label}<br>φ: {p:.1f}°<br>ψ: {ps:.1f}°")
        elif aa == "G":
            gly_phi.append(p)
            gly_psi.append(ps)
            gly_text.append(f"Glycine<br>{label}<br>φ: {p:.1f}°<br>ψ: {ps:.1f}°")
        elif aa == "P":
            pro_phi.append(p)
            pro_psi.append(ps)
            pro_text.append(f"Proline<br>{label}<br>φ: {p:.1f}°<br>ψ: {ps:.1f}°")
        else:
            reg_phi.append(p)
            reg_psi.append(ps)
            reg_text.append(f"Residue<br>{label}<br>φ: {p:.1f}°<br>ψ: {ps:.1f}°")

    # Regular residues
    if reg_phi:
        fig.add_trace(
            go.Scatter(
                x=reg_phi,
                y=reg_psi,
                mode="markers",
                name="General Residues",
                marker=dict(size=6, color="#05D9E8", opacity=0.7),
                text=reg_text,
                hoverinfo="text",
            )
        )

    # Glycine
    if gly_phi:
        fig.add_trace(
            go.Scatter(
                x=gly_phi,
                y=gly_psi,
                mode="markers",
                name="Glycine (G)",
                marker=dict(size=7, color="#FFB703", symbol="triangle-up"),
                text=gly_text,
                hoverinfo="text",
            )
        )

    # Proline
    if pro_phi:
        fig.add_trace(
            go.Scatter(
                x=pro_phi,
                y=pro_psi,
                mode="markers",
                name="Proline (P)",
                marker=dict(size=7, color="#2ec4b6", symbol="square"),
                text=pro_text,
                hoverinfo="text",
            )
        )

    # Outliers
    if out_phi:
        fig.add_trace(
            go.Scatter(
                x=out_phi,
                y=out_psi,
                mode="markers",
                name="Outliers / Disallowed",
                marker=dict(size=9, color="#FF2A6D", symbol="x"),
                text=out_text,
                hoverinfo="text",
            )
        )

    fig.update_layout(
        title="Ramachandran Plot (φ / ψ Angles)",
        xaxis_title="Dihedral Angle φ (degrees)",
        yaxis_title="Dihedral Angle ψ (degrees)",
        xaxis=dict(range=[-180, 180], zeroline=True, zerolinecolor="#333"),
        yaxis=dict(range=[-180, 180], zeroline=True, zerolinecolor="#333"),
        template="plotly_dark",
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        margin=dict(l=50, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
