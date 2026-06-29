"""10 — Orbit design: órbita-alvo, elementos, janelas."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.constants import ORBIT_ALT_KM, ORBIT_INC_DEG
    from thor.io.handoff import load_state, save_state, save_table
    from thor.models.vehicle_state import OrbitState
    from thor.physics.astro import circular_velocity, mean_motion
    return (
        ORBIT_ALT_KM,
        ORBIT_INC_DEG,
        OrbitState,
        circular_velocity,
        load_state,
        mean_motion,
        mo,
        pl,
        save_state,
        save_table,
    )


@app.cell
def _(mo):
    mo.md("# Camada 1 — Orbit Design")
    return


@app.cell
def _(ORBIT_ALT_KM, ORBIT_INC_DEG, OrbitState):
    orbit = OrbitState(
        altitude_km=ORBIT_ALT_KM,
        inclination_deg=ORBIT_INC_DEG,
        eccentricity=0.001,
        raan_deg=120.0,
        arg_perigee_deg=0.0,
        true_anomaly_deg=0.0,
    )
    return orbit


@app.cell
def _(circular_velocity, mean_motion, mo, orbit, pl):
    alt_m = orbit.altitude_km * 1000
    vc = circular_velocity(alt_m)
    n = mean_motion(alt_m)
    period_s = 2 * 3.14159265 / n
    df = pl.DataFrame(
        {
            "parameter": ["a [km]", "i [deg]", "V_circ [m/s]", "T [min]", "n [rad/s]"],
            "value": [
                orbit.altitude_km + 6371,
                orbit.inclination_deg,
                round(vc, 1),
                round(period_s / 60, 1),
                f"{n:.2e}",
            ],
        }
    )
    mo.ui.table(df)
    return alt_m, df, n, period_s, vc


@app.cell
def _(load_state, mo, orbit, save_state):
    state = load_state()
    state.orbit = orbit
    save_state(state)
    mo.md("✓ OrbitState → vehicle_state (Orekit/poliastro plug-in aqui)")
    return state


if __name__ == "__main__":
    app.run()
