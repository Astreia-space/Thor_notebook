"""30 — Aero database: Cl/Cd/Cm vs Mach × α (todos regimes)."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import polars as pl

    from thor.io.handoff import save_table
    from thor.io.inputs import float_list, num
    return float_list, mo, np, num, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 3 — Aero Database\n\nInputs: `aero_db` in `thor_inputs.csv`")
    return


@app.cell
def _(float_list, np, num, pl):
    machs = float_list("aero_db", "mach_list")
    alphas = np.linspace(num("aero_db", "alpha_min"), num("aero_db", "alpha_max"), int(num("aero_db", "alpha_steps")))
    cd0 = num("aero_db", "cd0")
    cd_a = num("aero_db", "cd_alpha_coef")
    cl_a = num("aero_db", "cl_alpha_coef")
    cm_a = num("aero_db", "cm_alpha_coef")
    rows = []
    for M in machs:
        for a in alphas:
            cd = cd0 + 0.1 * max(0, M - 0.9) ** 2 + cd_a * abs(a) + (0.5 if M > 5 else 0) * (a / 20) ** 2
            cl = cl_a * a * (1 if M < 10 else 0.6)
            cm = cm_a * a
            rows.append({"Mach": M, "alpha_deg": a, "Cd": cd, "Cl": cl, "Cm": cm})
    df = pl.DataFrame(rows)
    return alphas, cd0, df, machs, rows


@app.cell
def _(df, mo, pl):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4))
    for M in df["Mach"].unique().sort():
        sub = df.filter(pl.col("Mach") == M)
        ax.plot(sub["alpha_deg"], sub["Cl"], label=f"M={M}")
    ax.set(xlabel="α [deg]", ylabel="Cl", title="Cl(α) por Mach")
    ax.legend(fontsize=8)
    mo.ui.pyplot(fig)
    return ax, fig, plt


@app.cell
def _(df, mo, save_table):
    save_table("aero_database", df)
    mo.md("✓ AeroDB → parquet")
    return


if __name__ == "__main__":
    app.run()
