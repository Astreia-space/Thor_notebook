"""80 — OML paramétrica: nose radius, volume, aero."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import polars as pl

    from thor.io.handoff import load_state, save_state, save_table
    from thor.io.inputs import num
    return load_state, mo, np, num, pl, save_state, save_table


@app.cell
def _(mo):
    mo.md("# Camada 8 — OML Parametric\n\nInputs: `geometry` + `aero` in `thor_inputs.csv`")
    return


@app.cell
def _(load_state, np, num):
    state = load_state()
    L = num("geometry", "length_m")
    W = num("geometry", "width_m")
    rn = num("aero", "nose_radius_m")
    x = np.linspace(0, L, 50)
    z = W / 2 * np.sqrt(np.maximum(0, 1 - ((x - L / 2) / (L / 2)) ** 2))
    return L, W, rn, state, x, z


@app.cell
def _(L, W, mo, rn, x, z):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 2))
    ax.fill_between(x, -z, z, alpha=0.4, color="#2563eb")
    ax.set(xlabel="x [m]", ylabel="z [m]", title=f"OML THOR (Rn={rn} m)")
    ax.set_aspect("equal")
    mo.ui.pyplot(fig)
    return ax, fig, plt


@app.cell
def _(L, W, load_state, mo, num, pl, rn, save_state, save_table):
    state = load_state()
    state.aero.nose_radius_m = rn
    state.aero.reference_area_m2 = L * W * num("geometry", "s_ref_factor")
    state.aero.cd = num("aero", "cd")
    state.aero.cl = num("aero", "cl")
    save_state(state)
    save_table("oml", pl.DataFrame({"L_m": [L], "W_m": [W], "Rn_m": [rn]}))
    mo.md("✓ OML → aero R_n, S_ref")
    return state


if __name__ == "__main__":
    app.run()
