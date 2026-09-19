"""
Figure styling for Protein Explorer.

Every chart and every 3D viewer goes through this module so they sit on the
same paper as the rest of the page. Import it once, then wrap each figure:

    import plot_theme as pt

    fig = px.scatter(...)
    st.plotly_chart(pt.style(fig), use_container_width=True)

Colour meaning is the same as in theme.py:
    blue  = observed / measured      amber = predicted / computed
    green = structural               clay  = outlier, needs attention

IMPORTANT: remove any `template="plotly_dark"` left in your chart code -
an explicit template on the figure wins over the default set here.
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio

# ------------------------------------------------------------------
# palette (mirrors theme.py)
# ------------------------------------------------------------------
PAPER = "#ffffff"
PLOT_BG = "#fbfdfb"
INK = "#12241d"
INK_SOFT = "#35503f"
MUTED = "#6b7f74"
GRID = "#e6ece7"
AXIS = "#b9c7bd"
GREEN = "#2e6f52"
GREEN_DEEP = "#1d4c37"
BLUE = "#2b5f86"
AMBER = "#9a6b1f"
CLAY = "#a8442f"          # outliers / violations only
VIOLET = "#5b4b8a"

SERIES = [BLUE, GREEN, AMBER, VIOLET, CLAY, "#4a8fa8", GREEN_DEEP, "#7d6b3f"]

# sequential: pale paper -> deep green. Good for contact maps, coverage.
SCALE_SEQUENTIAL = [
    [0.00, "#f7faf8"], [0.25, "#cfe0d4"], [0.50, "#8fbda2"],
    [0.75, "#4c8a68"], [1.00, GREEN_DEEP],
]

# diverging: hydrophilic (blue) <-> hydrophobic (amber). Use for GRAVY,
# Kyte-Doolittle, charge, any signed per-residue scale. zmid=0 required.
SCALE_HYDROPATHY = [
    [0.00, "#1f4f73"], [0.25, "#7ba3bf"], [0.50, "#f4f6f2"],
    [0.75, "#d6ae6a"], [1.00, "#7a5214"],
]

# AlphaFold pLDDT keeps its published bands - users read these by colour.
SCALE_PLDDT = [
    [0.00, "#ff7d45"], [0.50, "#ffdb13"], [0.70, "#65cbf3"], [1.00, "#0053d6"],
]

_AXIS = dict(
    showgrid=True, gridcolor=GRID, gridwidth=1,
    zeroline=True, zerolinecolor=AXIS, zerolinewidth=1,
    linecolor=AXIS, linewidth=1, ticks="outside", ticklen=4,
    tickcolor=AXIS, tickfont=dict(size=11, color=MUTED),
    title=dict(font=dict(size=12, color=INK_SOFT)),
    showline=True, mirror=False,
)

PROTEIN_TEMPLATE = go.layout.Template(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",   # inherits the white figure frame
        plot_bgcolor=PLOT_BG,
        font=dict(family="Inter, system-ui, sans-serif", size=12, color=INK),
        title=dict(
            font=dict(family="Spectral, Georgia, serif", size=16, color=INK),
            x=0, xanchor="left", y=0.97, pad=dict(b=12),
        ),
        colorway=SERIES,
        colorscale=dict(sequential=SCALE_SEQUENTIAL, diverging=SCALE_HYDROPATHY),
        xaxis=_AXIS, yaxis=_AXIS,
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)", bordercolor=GRID, borderwidth=1,
            font=dict(size=11, color=INK_SOFT),
            orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1,
        ),
        margin=dict(l=62, r=24, t=52, b=54),
        hoverlabel=dict(
            bgcolor="#ffffff", bordercolor=AXIS,
            font=dict(family="IBM Plex Mono, monospace", size=11, color=INK),
        ),
        scene=dict(
            xaxis=dict(backgroundcolor=PLOT_BG, gridcolor=GRID, color=MUTED, showbackground=True),
            yaxis=dict(backgroundcolor=PLOT_BG, gridcolor=GRID, color=MUTED, showbackground=True),
            zaxis=dict(backgroundcolor=PLOT_BG, gridcolor=GRID, color=MUTED, showbackground=True),
        ),
    )
)

pio.templates["protein"] = PROTEIN_TEMPLATE
pio.templates.default = "protein"


def style(fig: go.Figure, height: int | None = None, legend: bool = True) -> go.Figure:
    """Force a figure onto the theme. Safe to call on figures that were
    already built with a dark template - it overwrites those settings."""
    fig.update_layout(template="protein", showlegend=legend)
    if height:
        fig.update_layout(height=height)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=PLOT_BG)
    # markers built for a dark background are usually too bright / too small
    fig.update_traces(
        selector=dict(type="scatter", mode="markers"),
        marker=dict(line=dict(width=0.6, color="rgba(255,255,255,0.9)")),
    )
    return fig


# ------------------------------------------------------------------
# Ramachandran
# ------------------------------------------------------------------
def ramachandran(phi, psi, outlier_mask=None, title="Ramachandran plot") -> go.Figure:
    """Phi/psi scatter with the favoured regions shaded.

    outlier_mask: optional iterable of bool, same length as phi.
    """
    fig = go.Figure()

    # favoured regions: beta sheet, right-handed alpha, left-handed alpha
    regions = [
        (-180, -45, 90, 180, "beta sheet"),
        (-160, -45, -70, 10, "alpha helix"),
        (35, 85, 20, 80, "left-handed alpha"),
    ]
    for x0, x1, y0, y1, label in regions:
        fig.add_shape(
            type="rect", x0=x0, x1=x1, y0=y0, y1=y1, layer="below",
            fillcolor="rgba(46,111,82,0.09)",
            line=dict(color="rgba(46,111,82,0.35)", width=1, dash="dot"),
        )
        fig.add_annotation(
            x=(x0 + x1) / 2, y=y1 - 8, text=label, showarrow=False,
            font=dict(size=10, color=GREEN_DEEP), opacity=0.85,
        )

    if outlier_mask is None:
        outlier_mask = [False] * len(phi)
    ok_x = [p for p, o in zip(phi, outlier_mask) if not o]
    ok_y = [p for p, o in zip(psi, outlier_mask) if not o]
    bad_x = [p for p, o in zip(phi, outlier_mask) if o]
    bad_y = [p for p, o in zip(psi, outlier_mask) if o]

    fig.add_trace(go.Scatter(
        x=ok_x, y=ok_y, mode="markers", name="residues",
        marker=dict(size=6, color=BLUE, opacity=0.62,
                    line=dict(width=0.6, color="rgba(255,255,255,0.9)")),
        hovertemplate="phi %{x:.0f}<br>psi %{y:.0f}<extra></extra>",
    ))
    if bad_x:
        fig.add_trace(go.Scatter(
            x=bad_x, y=bad_y, mode="markers", name="outliers",
            marker=dict(size=9, color=CLAY, symbol="x", line=dict(width=1.2)),
            hovertemplate="outlier<br>phi %{x:.0f}<br>psi %{y:.0f}<extra></extra>",
        ))

    ticks = dict(tickmode="array", tickvals=[-180, -90, 0, 90, 180], range=[-180, 180])
    fig.update_xaxes(title="phi (degrees)", **ticks)
    fig.update_yaxes(title="psi (degrees)", **ticks)
    fig.update_layout(title=title, height=560)
    return style(fig)


# ------------------------------------------------------------------
# 3D structure viewer (py3Dmol / stmol)
# ------------------------------------------------------------------
VIEWER_BG = "#ffffff"

#: cartoon coloured by secondary structure, in the page palette
SS_COLORS = {"h": GREEN, "s": BLUE, "c": "#c3cfc6"}


def apply_viewer_style(view, mode: str = "secondary_structure", plddt: bool = False):
    """Style a py3Dmol view so the 3D panel matches the rest of the page.

        view = py3Dmol.view(width=900, height=560)
        view.addModel(pdb_text, "pdb")
        pt.apply_viewer_style(view, plddt=True)
        view.zoomTo()
    """
    view.setBackgroundColor(VIEWER_BG)
    if plddt:
        # colour by the B-factor column, which AlphaFold fills with pLDDT
        view.setStyle({"cartoon": {"colorscheme": {
            "prop": "b",
            "gradient": "roygb",
            "min": 50, "max": 90,
        }}})
    elif mode == "secondary_structure":
        view.setStyle({"cartoon": {"colorscheme": {"prop": "ss", "map": SS_COLORS}}})
    else:
        view.setStyle({"cartoon": {"color": GREEN, "opacity": 0.95}})
    view.addStyle({"hetflag": True},
                  {"stick": {"radius": 0.16, "color": AMBER}})
    view.setViewStyle({"style": "outline", "color": "#12241d", "width": 0.04})
    return view


# ------------------------------------------------------------------
# matplotlib, if any figure still uses it
# ------------------------------------------------------------------
def apply_matplotlib() -> None:
    import matplotlib as mpl

    mpl.rcParams.update({
        "figure.facecolor": "none",
        "axes.facecolor": PLOT_BG,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": INK_SOFT,
        "axes.titlesize": 12,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "DejaVu Sans"],
        "axes.prop_cycle": mpl.cycler(color=SERIES),
        "savefig.transparent": True,
    })
