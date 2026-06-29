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
    return mo, np, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 3 — Aero Database (subsônico → hipersônico)")
    return


@app.cell
def _(np, pl):
    machs = [0.3, 0.8, 1.2, 3, 8, 15]
    alphas = np.linspace(-10, 20, 7)
    rows = []
    for M in machs:
        for a in alphas:
            # Modelo enxuto: transonic bump + hipersônico Newtoniano
            cd0 = 0.15 + 0.1 * max(0, M - 0.9) ** 2
            cd = cd0 + 0.02 * abs(a) + (0.5 if M > 5 else 0) * (a / 20) ** 2
            cl = 0.08 * a * (1 if M < 10 else 0.6)
            cm = -0.02 * a
            rows.append({"Mach": M, "alpha_deg": a, "Cd": cd, "Cl": cl, "Cm": cm})
    df = pl.DataFrame(rows)
    return alphas, df, machs, rows


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
    mo.md("✓ AeroDB → parquet (AeroSandbox plug-in)")
    return


if __name__ == "__main__":
    app.run()
