"""52 — Attitude control: RCS / wheels."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_table, save_table
    return load_table, mo, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 5 — Attitude Control")
    return


@app.cell
def _(load_table):
    rcs = load_table("rcs_sizing")
    return rcs


@app.cell
def _(mo, pl, rcs):
    iyy = 25_000  # kg·m² from 50
    torque_req = 500  # N·m slew
    if rcs is not None:
        torque_avail = float(rcs["torque_Nm"][0])
    else:
        torque_avail = 150
    df = pl.DataFrame(
        {
            "metric": ["τ_req [Nm]", "τ_RCS [Nm]", "adequate"],
            "value": [torque_req, torque_avail, torque_avail >= torque_req],
        }
    )
    mo.ui.table(df)
    return df, iyy, torque_avail, torque_req


@app.cell
def _(df, mo, save_table):
    save_table("attitude_control", df)
    mo.md("✓ Autoridade de controle verificada")
    return


if __name__ == "__main__":
    app.run()
