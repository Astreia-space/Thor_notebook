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
"""22 — Aeroheating: Sutton-Graves, calor integrado → TPS."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_table, save_table
    from thor.physics.entry import sutton_graves
    return load_table, mo, pl, save_table, sutton_graves


@app.cell
def _(mo):
    mo.md(
        """
        # Camada 2 — Aeroheating

        Convectivo: Sutton-Graves q̇ ∝ √(ρ/Rn)·V³  
        Radiativo: relevante se V > ~9 km/s
        """
    )
    return


@app.cell
def _(load_table):
    traj = load_table("entry_trajectory")
    return traj


@app.cell
def _(mo, pl, save_table, traj):
    import numpy as np

    if traj is None:
        mo.md("⚠ Execute 21_entry_trajectory_3dof primeiro")
        return None

    rn = 0.5  # m
    dt = np.diff(traj["t_s"].to_numpy(), prepend=0)
    q = traj["q_W_cm2"].to_numpy()
    Q_J_cm2 = np.cumsum(q * dt) / 1e4  # W/cm² · s → J/cm² approx

    df = pl.DataFrame({"t_s": traj["t_s"], "q_W_cm2": q, "Q_integrated_J_cm2": Q_J_cm2})
    q_total = float(Q_J_cm2[-1])

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(df["t_s"], df["q_W_cm2"], label="q̇")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("W/cm²")
    ax2 = ax.twinx()
    ax2.plot(df["t_s"], df["Q_integrated_J_cm2"], "r--", label="∫Q")
    ax2.set_ylabel("J/cm²")
    ax.set_title(f"Calor total ≈ {q_total:.0f} J/cm²")
    mo.ui.pyplot(fig)

    save_table("aeroheating", df)
    mo.md(f"✓ Q_total = **{q_total:.0f} J/cm²** → dimensiona TPS (23)")
    return ax, ax2, df, dt, fig, np, plt, q, q_total, rn


if __name__ == "__main__":
    app.run()
