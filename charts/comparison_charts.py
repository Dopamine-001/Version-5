"""
Two-protein overlay charts for the Comparison tab / landing-page comparison
mode.
"""

from __future__ import annotations

import plotly.graph_objects as go

from analysis.sequence import hydrophobicity_table
from config import AA_GROUPS


def comparison_hydrophobicity_figure(seq1: str, name1: str, seq2: str, name2: str, window: int = 9) -> go.Figure:
    fig = go.Figure()
    colors = ["#b3814f", "#7c8f5e"]
    for seq, name, color in ((seq1, name1, colors[0]), (seq2, name2, colors[1])):
        df = hydrophobicity_table(seq)
        rolling = df["Kyte-Doolittle"].rolling(window, center=True, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=df["Position"], y=rolling, mode="lines", name=name,
            line=dict(width=3, color=color),
            hovertemplate="Position %{x}<br>Average: %{y:.2f}<extra></extra>",
        ))
    fig.add_hline(y=0, line_dash="dot", line_color="#a3906f")
    fig.update_layout(
        height=360,
        margin=dict(l=45, r=20, t=25, b=45),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3b2f22"),
        xaxis_title="Residue position",
        yaxis_title="Hydropathy (moving average)",
        legend=dict(orientation="h", y=1.1),
        xaxis=dict(gridcolor="#e6d9bc"),
        yaxis=dict(gridcolor="#e6d9bc"),
    )
    return fig


def comparison_composition_figure(seq1: str, name1: str, seq2: str, name2: str) -> go.Figure:
    def group_percentages(sequence: str) -> list[float]:
        total = len(sequence) or 1
        return [round(sum(sequence.count(aa) for aa in aas) / total * 100, 1) for aas in AA_GROUPS.values()]

    fig = go.Figure()
    fig.add_trace(go.Bar(name=name1, x=list(AA_GROUPS.keys()), y=group_percentages(seq1), marker_color="#b3814f"))
    fig.add_trace(go.Bar(name=name2, x=list(AA_GROUPS.keys()), y=group_percentages(seq2), marker_color="#7c8f5e"))
    fig.update_layout(
        barmode="group",
        height=340,
        margin=dict(l=35, r=20, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3b2f22"),
        yaxis_title="Share of sequence (%)",
        legend=dict(orientation="h", y=1.12),
        xaxis=dict(gridcolor="#e6d9bc"),
        yaxis=dict(gridcolor="#e6d9bc"),
    )
    return fig
