"""70 — Thermal control on-orbit."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import save_table
    from thor.io.inputs import num
    return mo, num, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 7 — Thermal Control\n\nInputs: `thermal` in `thor_inputs.csv`")
    return


@app.cell
def _(mo, num, pl):
    emiss = num("thermal", "emissivity")
    t_hot = num("thermal", "radiator_temp_K")
    t_cold = num("thermal", "cold_temp_K")
    area_rad = num("thermal", "radiator_area_m2")
    q_rej = emiss * 5.67e-8 * (t_hot**4 - t_cold**4) * area_rad
    power_diss = num("thermal", "avionics_dissipation_W")
    balance = q_rej - power_diss
    df = pl.DataFrame(
        {
            "parameter": ["A_rad [m²]", "Q_reject [W]", "Q_diss [W]", "balance [W]"],
            "value": [area_rad, round(q_rej, 0), power_diss, round(balance, 0)],
        }
    )
    mo.ui.table(df)
    return balance, df, power_diss, q_rej


@app.cell
def _(df, mo, save_table):
    save_table("thermal_control", df)
    mo.md("✓ Balanço térmico on-orbit")
    return


if __name__ == "__main__":
    app.run()
