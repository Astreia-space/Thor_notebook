# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.9.0",
#     "polars",
#     "matplotlib",
#     "numpy",
#     "pydantic>=2",
#     "duckdb",
#     "thor-notebook",
# ]
#
# [tool.uv.sources]
# thor-notebook = { path = "..", editable = true }
# ///
"""91 — Trade studies: cápsula vs lifting body, Pareto."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import polars as pl

    from thor.io.handoff import save_table
    from thor.physics.entry import integrate_entry_3dof
    return integrate_entry_3dof, mo, np, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 9 — Trade Studies")
    return


@app.cell
def _(integrate_entry_3dof, np):
    import math

    betas = np.linspace(100, 400, 7)
    configs = ["capsule", "lifting_body"]
    rows = []
    for cfg in configs:
        cd = 1.5 if cfg == "capsule" else 0.8
        cl = 0.1 if cfg == "capsule" else 0.4
        for beta in betas:
            m = beta * cd * 10
            traj = integrate_entry_3dof(122e3, 7800, math.radians(-1.5), beta)
            rows.append(
                {
                    "config": cfg,
                    "beta": beta,
                    "mass_kg": m,
                    "g_peak": float(traj["g_load"].max()),
                    "q_peak": float(traj["q_W_cm2"].max()),
                    "L_D": cl / cd,
                }
            )
    df = pl.DataFrame(rows)
    return beta, betas, cd, cfg, cl, configs, df, math, m, rows, traj


@app.cell
def _(df, mo, pl):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 5))
    for cfg in df["config"].unique():
        sub = df.filter(pl.col("config") == cfg)
        ax.scatter(sub["mass_kg"], sub["q_peak"], label=cfg, s=60)
    ax.set(xlabel="Massa [kg]", ylabel="q_peak [W/cm²]", title="Pareto: massa × calor")
    ax.legend()
    ax.grid(True, alpha=0.3)
    mo.ui.pyplot(fig)
    return ax, fig, plt


@app.cell
def _(df, mo, pl, save_table):
    save_table("trade_studies", df)
    best = df.filter(pl.col("config") == "lifting_body").sort("q_peak").row(0, named=True)
    mo.md(f"**Lifting body mínimo q:** m={best['mass_kg']:.0f} kg, q={best['q_peak']:.0f} W/cm²")
    return best


if __name__ == "__main__":
    app.run()
