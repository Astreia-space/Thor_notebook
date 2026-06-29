"""33 — Terminal descent: paraquedas ou glide subsônico."""

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
    mo.md("# Camada 3 — Terminal Descent\n\nInputs: `terminal` in `thor_inputs.csv`")
    return


@app.cell
def _(load_state, num):
    state = load_state()
    ld = state.aero.ld if state.aero.ld else num("aero", "cl") / num("aero", "cd")
    df = pl.DataFrame(
        {
            "mode": ["supersonic_drogue", "main_chute", "glide_approach"],
            "altitude_km": [num("terminal", "drogue_alt_km"), num("terminal", "main_chute_alt_km"), num("terminal", "glide_alt_km")],
            "velocity_m_s": [num("terminal", "drogue_vel_m_s"), num("terminal", "main_chute_vel_m_s"), num("terminal", "v_terminal_m_s")],
            "notes": ["Mortar deploy", f"L/D={ld:.2f}", f"slope={num('terminal', 'glide_slope_deg')}°"],
        }
    )
    return df, ld, state


@app.cell
def _(df, mo, save_table):
    mo.ui.table(df)
    save_table("terminal_descent", df)
    mo.md("✓ Perfil terminal → parquet")
    return


if __name__ == "__main__":
    app.run()
