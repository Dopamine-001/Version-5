"""
Plotly figures built from one protein's sequence: the hydrophobicity trace
and the amino-acid composition bar chart. All chart colors live here — edit
these hex values to re-theme just the plots without touching styles.py.
"""

from __future__ import annotations

import plotly.graph_objects as go

from analysis.sequence import amino_acid_composition, hydrophobicity_table


def hydrophobicity_figure(sequence: str, window: int = 9) -> go.Figure:
    df = hydrophobicity_table(sequence)
    if df.empty:
        return go.Figure()

    rolling = df["Kyte-Doolittle"].rolling(window, center=True, min_periods=1).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Position"], y=df["Kyte-Doolittle"],
        mode="lines", name="Residue score",
        line=dict(width=1, color="#c9a06b"),
        opacity=.5,
        hovertemplate="Position %{x}<br>%{text}: %{y:.2f}<extra></extra>",
        text=df["Residue"],
    ))
    fig.add_trace(go.Scatter(
        x=df["Position"], y=rolling,
        mode="lines", name=f"{window}-residue moving average",
        line=dict(width=3, color="#7c8f5e"),
        hovertemplate="Position %{x}<br>Average: %{y:.2f}<extra></extra>",
    ))
    fig.add_hline(y=0, line_dash="dot", line_color="#a3906f")
    fig.update_layout(
        height=390,
        margin=dict(l=45, r=20, t=25, b=45),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3b2f22"),
        xaxis_title="Residue position",
        yaxis_title="Hydropathy",
        legend=dict(orientation="h", y=1.08),
        xaxis=dict(gridcolor="#e6d9bc"),
        yaxis=dict(gridcolor="#e6d9bc"),
    )
    return fig


def composition_figure(sequence: str) -> go.Figure:
    df = amino_acid_composition(sequence)
    df = df[df["Count"] > 0]
    fig = go.Figure(go.Bar(
        x=df["Amino acid"],
        y=df["Count"],
        text=df["Count"],
        textposition="auto",
        marker_color="#b3814f",
    ))
    fig.update_layout(
        height=330,
        margin=dict(l=35, r=20, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3b2f22"),
        xaxis_title="Amino acid",
        yaxis_title="Count",
        xaxis=dict(gridcolor="#e6d9bc"),
        yaxis=dict(gridcolor="#e6d9bc"),
    )
    return fig
