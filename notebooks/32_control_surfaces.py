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
"""32 — Control surfaces: body flap / RCS authority."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import save_table
    return mo, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 3 — Control Surfaces")
    return


@app.cell
def _(mo, pl):
    # Lifting body: elevons; Cápsula: RCS
    q_dyn = 5000  # Pa @ hypersonic trim
    s_ref = 10  # m²
    cm_req = 0.05
    arm = 2.0  # m
    flap_area = cm_req * q_dyn * s_ref * 0.5 / (q_dyn * arm)  # simplificado
    df = pl.DataFrame(
        {
            "surface": ["body_flap_port", "body_flap_stbd", "RCS_pitch"],
            "area_m2": [flap_area, flap_area, 0],
            "deflection_deg": [15, 15, 0],
            "authority": ["primary", "primary", "backup"],
        }
    )
    mo.ui.table(df)
    return arm, cm_req, df, flap_area, q_dyn, s_ref


@app.cell
def _(df, mo, save_table):
    save_table("control_surfaces", df)
    mo.md("✓ Superfícies de controle dimensionadas")
    return


if __name__ == "__main__":
    app.run()
