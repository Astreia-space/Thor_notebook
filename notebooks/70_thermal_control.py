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
"""70 — Thermal control on-orbit."""

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
    mo.md("# Camada 7 — Thermal Control")
    return


@app.cell
def _(load_state):
    state = load_state()
    q_abs = 1361  # W/m² solar
    area_rad = 4.0  # m²
    emiss = 0.85
    q_rej = emiss * 5.67e-8 * (300**4 - 200**4) * area_rad  # Stefan-Boltzmann approx
    power_diss = 500  # W avionics
    return area_rad, emiss, power_diss, q_abs, q_rej, state


@app.cell
def _(area_rad, mo, pl, power_diss, q_rej):
    balance = q_rej - power_diss
    df = pl.DataFrame(
        {
            "parameter": ["A_rad [m²]", "Q_reject [W]", "Q_diss [W]", "balance [W]"],
            "value": [area_rad, round(q_rej, 0), power_diss, round(balance, 0)],
        }
    )
    mo.ui.table(df)
    return balance, df


@app.cell
def _(df, mo, save_table):
    save_table("thermal_control", df)
    mo.md("✓ Balanço térmico on-orbit")
    return


if __name__ == "__main__":
    app.run()
