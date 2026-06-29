# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.9.0",
#     "polars",
#     "matplotlib",
#     "numpy",
#     "pydantic>=2",
#     "duckdb",
#     "thor-notebook",
# ]
#
# [tool.uv.sources]
# thor-notebook = { path = "..", editable = true }
# ///
"""50 — Mass properties: inércia, CG tracking."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_table
    return load_state, mo, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 5 — Mass Properties")
    return


@app.cell
def _(load_state):
    state = load_state()
    m = state.mass.dry_mass_kg or 3500
    # Slender lifting body approx: Ixx < Iyy ≈ Izz
    L, W, H = 8.0, 3.0, 1.2  # m
    ixx = m / 12 * (W**2 + H**2)
    iyy = m / 12 * (L**2 + H**2)
    izz = m / 12 * (L**2 + W**2)
    cg = [4.8, 0, 0]  # m from nose
    return H, L, W, cg, ixx, iyy, izz, m, state


@app.cell
def _(cg, ixx, iyy, izz, mo, pl):
    df = pl.DataFrame(
        {
            "parameter": ["Ixx", "Iyy", "Izz", "x_CG [m]"],
            "value": [round(ixx, 0), round(iyy, 0), round(izz, 0), cg[0]],
        }
    )
    mo.ui.table(df)
    return df


@app.cell
def _(df, mo, save_table):
    save_table("mass_properties", df)
    mo.md("✓ Inércia/CG → parquet (consome geometria 80)")
    return


if __name__ == "__main__":
    app.run()
