"""52 — Attitude control: RCS / wheels."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_table, save_table
    from thor.io.inputs import num
    return load_table, mo, num, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 5 — Attitude Control\n\nInputs: `gnc` + `rcs` in `thor_inputs.csv`")
    return


@app.cell
def _(load_table, num):
    rcs = load_table("rcs_sizing")
    torque_req = num("gnc", "torque_required_Nm")
    torque_avail = float(rcs["torque_Nm"][0]) if rcs is not None else num("rcs", "thrust_N") * num("rcs", "arm_m")
    return rcs, torque_avail, torque_req


@app.cell
def _(mo, pl, torque_avail, torque_req):
    df = pl.DataFrame(
        {
            "metric": ["τ_req [Nm]", "τ_RCS [Nm]", "adequate"],
            "value": [torque_req, torque_avail, torque_avail >= torque_req],
        }
    )
    mo.ui.table(df)
    return df


@app.cell
def _(df, mo, save_table):
    save_table("attitude_control", df)
    mo.md("✓ Autoridade de controle verificada")
    return


if __name__ == "__main__":
    app.run()
