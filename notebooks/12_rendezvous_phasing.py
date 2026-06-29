"""12 — Rendezvous phasing: Hohmann + Clohessy-Wiltshire → ΔV braking."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import polars as pl

    from thor.io.handoff import load_state, save_state, save_table
    from thor.physics.astro import hohmann_delta_v, hill_clohessy_wiltshire, mean_motion
    return (
        hill_clohessy_wiltshire,
        hohmann_delta_v,
        load_state,
        mean_motion,
        mo,
        np,
        pl,
        save_state,
        save_table,
    )


@app.cell
def _(mo):
    mo.md("# Camada 1 — Rendezvous & Phasing (Hohmann + Hill)")
    return


@app.cell
def _(hohmann_delta_v, load_state):
    state = load_state()
    chaser_alt = 380e3
    target_alt = state.orbit.altitude_km * 1000 if state.orbit else 400e3
    dv1, dv2 = hohmann_delta_v(chaser_alt, target_alt)
    dv_braking = abs(dv2) + 15  # CW terminal + margin
    return chaser_alt, dv1, dv2, dv_braking, state, target_alt


@app.cell
def _(chaser_alt, dv1, dv2, dv_braking, mean_motion, mo, np, pl, target_alt):
    n = mean_motion(target_alt)
    x0 = np.array([500.0, 0, 0, 0, -0.5, 0])  # 500 m atrás, approach lento
    xf = hill_clohessy_wiltshire(n, 3600, x0)
    df = pl.DataFrame(
        {
            "maneuver": ["Hohmann burn 1", "Hohmann burn 2", "Braking (CW)"],
            "delta_v_m_s": [dv1, dv2, dv_braking],
        }
    )
    mo.vstack(
        mo.md(f"**ΔV phasing total:** {dv1 + dv2 + dv_braking:.1f} m/s"),
        mo.md(f"Estado relativo final: x={xf[0]:.0f} m, y={xf[1]:.0f} m"),
        mo.ui.table(df),
    )
    return df, n, x0, xf


@app.cell
def _(df, dv_braking, load_state, mo, save_state, save_table):
    state = load_state()
    for item in state.delta_v.items:
        if "phasing" in item.phase or "rendezvous" in item.phase:
            item.delta_v_m_s = dv_braking if "rendezvous" in item.phase else item.delta_v_m_s
    save_state(state)
    save_table("phasing_dv", df)
    mo.md("✓ ΔV braking → delta_v budget")
    return state


if __name__ == "__main__":
    app.run()
