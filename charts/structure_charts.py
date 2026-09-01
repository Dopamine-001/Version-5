"""
Plotly figures built from a protein's predicted 3D structure.
"""

from __future__ import annotations

from typing import Optional

import plotly.graph_objects as go

from core.alphafold import plddt_distribution


def ramachandran_figure(
    phi: list[float],
    psi: list[float],
    residue_numbers: list[int],
) -> go.Figure:
    """
    Interactive Ramachandran plot with density-style heat-map regions
    and individual residue positions.
    """

    import numpy as np

    # ---------------------------------------------------------
    # Grid covering the complete Ramachandran angle space
    # ---------------------------------------------------------

    x = np.linspace(-180, 180, 181)
    y = np.linspace(-180, 180, 181)

    X, Y = np.meshgrid(x, y)

    # ---------------------------------------------------------
    # Approximate major allowed conformational regions.
    #
    # These are smooth Gaussian-like regions centered around
    # common protein backbone conformations.
    # ---------------------------------------------------------

    def gaussian(cx, cy, sx, sy, amplitude=1.0):
        return amplitude * np.exp(
            -(
                ((X - cx) ** 2) / (2 * sx ** 2)
                + ((Y - cy) ** 2) / (2 * sy ** 2)
            )
        )

    density = (
        gaussian(-65, -40, 28, 22, 1.00)      # alpha helix
        + gaussian(-120, 130, 32, 28, 0.95)   # beta sheet
        + gaussian(-80, 150, 24, 25, 0.65)   # beta/extended
        + gaussian(60, 40, 25, 25, 0.55)     # left-handed helix
    )

    # Normalize
    density = density / density.max()

    # ---------------------------------------------------------
    # Create figure
    # ---------------------------------------------------------

    fig = go.Figure()

    # ---------------------------------------------------------
    # Heat-map background
    # ---------------------------------------------------------

    fig.add_trace(
        go.Heatmap(
            x=x,
            y=y,
            z=density,
            zmin=0,
            zmax=1,
            colorscale=[
                [0.00, "#f5f5f5"],
                [0.25, "#e8dfc9"],
                [0.50, "#d8c98f"],
                [0.70, "#a9b66a"],
                [1.00, "#6f8f55"],
            ],
            opacity=0.82,
            hoverinfo="skip",
            showscale=False,
            name="Conformational density",
        )
    )

    # ---------------------------------------------------------
    # Residue positions
    # ---------------------------------------------------------

    fig.add_trace(
        go.Scattergl(
            x=phi,
            y=psi,
            mode="markers",
            marker=dict(
                size=7,
                color="#b3814f",
                opacity=0.92,
                line=dict(
                    width=0.7,
                    color="#ffffff",
                ),
            ),
            customdata=residue_numbers,
            hovertemplate=(
                "<b>Residue %{customdata}</b>"
                "<br>φ %{x:.1f}°"
                "<br>ψ %{y:.1f}°"
                "<extra></extra>"
            ),
            name="Backbone angles",
        )
    )

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------

    fig.update_layout(
        height=560,
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f5f5f5"),

        xaxis=dict(
            title="Phi (φ)",
            range=[-180, 180],
            dtick=60,
            gridcolor="rgba(255,255,255,0.15)",
            zeroline=False,
            constrain="domain",
        ),

        yaxis=dict(
            title="Psi (ψ)",
            range=[-180, 180],
            dtick=60,
            gridcolor="rgba(255,255,255,0.15)",
            zeroline=False,
        ),

        margin=dict(
            l=55,
            r=20,
            t=40,
            b=55,
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
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
