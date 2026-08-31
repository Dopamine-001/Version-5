"""
Plotly figures built from a protein's predicted 3D structure.
"""

from __future__ import annotations

from typing import Optional

import plotly.graph_objects as go

from core.alphafold import plddt_distribution


def ramachandran_figure(phi: list[float], psi: list[float], residue_numbers: list[int]) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scattergl(
        x=phi, y=psi, mode="markers",
        marker=dict(size=7, color="#b3814f", opacity=.82),
        customdata=residue_numbers,
        hovertemplate="Residue %{customdata}<br>φ %{x:.1f}°<br>ψ %{y:.1f}°<extra></extra>",
        name="Backbone angles",
    ))
    fig.add_shape(type="rect", x0=-100, x1=-35, y0=-70, y1=-5,
                  line=dict(color="#7c8f5e", dash="dot"))
    fig.add_shape(type="rect", x0=-180, x1=-90, y0=90, y1=180,
                  line=dict(color="#c1793a", dash="dot"))
    fig.update_layout(
        height=560,
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3b2f22"),
        # NOTE: deliberately no yaxis scaleanchor="x" here. That equal-
        # aspect lock fights Streamlit's use_container_width resizing and
        # can collapse this plot to zero visible height in the browser.
        # constrain="domain" on the x-axis keeps the square look safely.
        xaxis=dict(title="Phi (φ)", range=[-180, 180], dtick=60, gridcolor="#e6d9bc", constrain="domain"),
        yaxis=dict(title="Psi (ψ)", range=[-180, 180], dtick=60, gridcolor="#e6d9bc"),
        margin=dict(l=55, r=20, t=30, b=50),
    )
    return fig


def plddt_figure(pdb_text: str) -> Optional[go.Figure]:
    """Display pLDDT distribution as a compact histogram."""
    df = plddt_distribution(pdb_text)
    if df.empty:
        return None
    fig = go.Figure(go.Histogram(
        x=df["Atom pLDDT"],
        nbinsx=20,
        marker_color="#7c8f5e",
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=35, r=20, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3b2f22"),
        xaxis_title="pLDDT",
        yaxis_title="Atoms",
        xaxis=dict(gridcolor="#e6d9bc"),
        yaxis=dict(gridcolor="#e6d9bc"),
    )
    return fig
