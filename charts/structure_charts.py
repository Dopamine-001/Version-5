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

    # Thin out tick labels dynamically based on protein length to prevent overlapping
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
