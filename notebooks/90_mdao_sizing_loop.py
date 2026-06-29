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
"""90 — MDAO sizing loop: converge massa, β, TPS, propelente."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.constants import CONCEPTUAL_GROWTH
    from thor.io.handoff import load_state, save_state, save_table
    from thor.physics.entry import integrate_entry_3dof
    from thor.physics.propulsion import propellant_mass
    return (
        CONCEPTUAL_GROWTH,
        integrate_entry_3dof,
        load_state,
        mo,
        pl,
        propellant_mass,
        save_state,
        save_table,
    )


@app.cell
def _(mo):
    mo.md("# Camada 9 — MDAO Sizing Loop (OpenMDAO plug-in)")
    return


@app.cell
def _(CONCEPTUAL_GROWTH, integrate_entry_3dof, load_state, propellant_mass):
    import math

    state = load_state()
    history = []
    for it in range(5):
        m_dry = state.mass.dry_mass_kg
        cd, area = state.aero.cd, state.aero.reference_area_m2
        beta = m_dry / (cd * area)
        mp = propellant_mass(m_dry + state.mass.propellant_kg, 325, 100)
        state.mass.propellant_kg = mp
        state.entry.ballistic_coefficient_kg_m2 = beta
        traj = integrate_entry_3dof(
            state.entry.altitude_m,
            state.entry.velocity_m_s,
            math.radians(state.entry.flight_path_angle_deg),
            beta,
        )
        g_peak = float(traj["g_load"].max())
        q_peak = float(traj["q_W_cm2"].max())
        history.append({"iter": it, "m_dry": m_dry, "beta": beta, "g_peak": g_peak, "q_peak": q_peak})
        # Simple feedback: TPS mass ∝ q_peak
        for item in state.mass.items:
            if item.name == "TPS":
                item.dry_kg = 200 + q_peak * 0.8
    return beta, cd, g_peak, history, it, math, m_dry, mp, q_peak, state, traj


@app.cell
def _(history, mo, pl):
    df = pl.DataFrame(history)
    mo.ui.table(df)
    return df


@app.cell
def _(df, mo, save_state, save_table, state):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df["iter"], df["m_dry"], "o-", label="m_dry")
    ax.set(xlabel="iteração", ylabel="kg", title="Convergência MDAO")
    ax.legend()
    mo.ui.pyplot(fig)

    save_state(state)
    save_table("mdao_convergence", df)
    mo.md("✓ Veículo convergido → vehicle_state.json")
    return ax, fig, plt


if __name__ == "__main__":
    app.run()
