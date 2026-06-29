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
"""61 — Primary structure sizing."""

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
    mo.md("# Camada 6 — Primary Structure")
    return


@app.cell
def _(load_state):
    state = load_state()
    m_struct = 1200
    material = "Al-Li 2195 + CFRP"
    sigma_allow = 300e6  # Pa
    load_g = 6
    mass = state.mass.dry_mass_kg or 3500
    area_load = mass * 9.81 * load_g / sigma_allow
    return area_load, load_g, m_struct, mass, material, sigma_allow, state


@app.cell
def _(area_load, material, mo, m_struct, pl):
    df = pl.DataFrame(
        {
            "item": ["material", "m_structure [kg]", "A_min [m²]"],
            "value": [material, m_struct, round(area_load, 3)],
        }
    )
    mo.ui.table(df)
    return df


@app.cell
def _(df, mo, save_table):
    save_table("primary_structure", df)
    mo.md("✓ Estrutura primária → parquet")
    return


if __name__ == "__main__":
    app.run()
