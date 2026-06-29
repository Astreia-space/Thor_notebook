"""32 — Control surfaces: body flap / RCS authority."""

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
    mo.md("# Camada 3 — Control Surfaces\n\nInputs: `control` + `aero` in `thor_inputs.csv`")
    return


@app.cell
def _(load_state, num):
    state = load_state()
    q_dyn = num("control", "q_dyn_Pa")
    s_ref = state.aero.reference_area_m2 or num("aero", "reference_area_m2")
    cm_req = num("control", "cm_required")
    arm = num("control", "moment_arm_m")
    flap_area = cm_req * q_dyn * s_ref * 0.5 / (q_dyn * arm)
    df = pl.DataFrame(
        {
            "surface": ["body_flap_port", "body_flap_stbd", "RCS_pitch"],
            "area_m2": [flap_area, flap_area, 0],
            "deflection_deg": [15, 15, 0],
            "authority": ["primary", "primary", "backup"],
        }
    )
    return arm, cm_req, df, flap_area, q_dyn, s_ref, state


@app.cell
def _(df, mo, save_table):
    mo.ui.table(df)
    save_table("control_surfaces", df)
    mo.md("✓ Superfícies de controle dimensionadas")
    return


if __name__ == "__main__":
    app.run()
