"""24 — Hypersonic aero: Newtoniano modificado → Cl/Cd/Cm."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import polars as pl

    from thor.io.handoff import load_state, save_state, save_table
    from thor.physics.aero import hypersonic_cd_cl
    return hypersonic_cd_cl, load_state, mo, np, pl, save_state, save_table


@app.cell
def _(mo):
    mo.md("# Camada 2 — Hypersonic Aero (Cp = Cp_max·sin²θ)")
    return


@app.cell
def _(hypersonic_cd_cl, np):
    cp_max = 1.8
    alphas = np.linspace(-20, 20, 41)
    rows = []
    for a in alphas:
        cd, cl = hypersonic_cd_cl(cp_max, np.radians(a))
        rows.append({"alpha_deg": a, "Cd": cd, "Cl": cl, "L_D": cl / cd if cd else 0})
    df = pl.DataFrame(rows)
    return alphas, cp_max, df, rows


@app.cell
def _(df, mo):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["alpha_deg"], df["Cd"], label="Cd")
    ax.plot(df["alpha_deg"], df["Cl"], label="Cl")
    ax.set(xlabel="α [deg]", ylabel="Coeff", title="Hipersônico (Newtoniano mod.)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    mo.ui.pyplot(fig)
    return ax, fig, plt


@app.cell
def _(df, load_state, mo, pl, save_state, save_table):
    state = load_state()
    trim = df.filter(pl.col("L_D") == df["L_D"].max()).row(0, named=True)
    state.aero.cd = trim["Cd"]
    state.aero.cl = trim["Cl"]
    save_state(state)
    save_table("hypersonic_aero", df)
    mo.md(f"✓ Trim L/D={trim['L_D']:.2f} @ α={trim['alpha_deg']:.0f}° → fecha loop com 21")
    return state, trim


if __name__ == "__main__":
    app.run()
