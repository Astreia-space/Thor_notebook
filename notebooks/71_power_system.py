"""71 — Power system: arrays, baterias, EPS."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_table
    from thor.io.inputs import num
    return load_state, mo, num, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 7 — Power System\n\nInputs: `power` + mission energy from 03")
    return


@app.cell
def _(load_state, num):
    state = load_state()
    e_total = state.power.total_wh or 5000
    battery_wh = e_total * num("power", "battery_margin_frac")
    array_power = num("power", "array_power_W")
    return array_power, battery_wh, e_total, state


@app.cell
def _(array_power, battery_wh, e_total, mo, pl):
    df = pl.DataFrame(
        {
            "parameter": ["E_missão [Wh]", "Bateria [Wh]", "Array [W]"],
            "value": [round(e_total, 0), round(battery_wh, 0), array_power],
        }
    )
    mo.ui.table(df)
    return df


@app.cell
def _(df, mo, save_table):
    save_table("power_system", df)
    mo.md("✓ EPS dimensionado (fecha com 03)")
    return


if __name__ == "__main__":
    app.run()
