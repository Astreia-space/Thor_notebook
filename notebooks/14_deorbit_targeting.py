"""14 — Deorbit targeting → estado na Entry Interface (122 km)."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import math
    import polars as pl

    from thor.constants import EI_ALTITUDE_M, MU_EARTH, R_EARTH
    from thor.io.handoff import load_state, save_state, save_table
    from thor.models.vehicle_state import EntryState
    return (
        EI_ALTITUDE_M,
        EntryState,
        MU_EARTH,
        R_EARTH,
        load_state,
        math,
        mo,
        pl,
        save_state,
        save_table,
    )


@app.cell
def _(mo):
    mo.md("# Camada 1 — Deorbit Targeting → Entry Interface")
    return


@app.cell
def _(EI_ALTITUDE_M, MU_EARTH, R_EARTH, load_state, math):
    state = load_state()
    alt_orbit = state.orbit.altitude_km * 1000
    r = R_EARTH + alt_orbit
    v_circ = math.sqrt(MU_EARTH / r)
    dv_deorbit = 100.0  # m/s retrograde
    v_ei = math.sqrt(v_circ**2 + dv_deorbit**2 - 2 * v_circ * dv_deorbit)  # approx
    entry = EntryState(
        altitude_m=EI_ALTITUDE_M,
        velocity_m_s=v_ei,
        flight_path_angle_deg=-1.5,
        heading_deg=90.0,
        ballistic_coefficient_kg_m2=200.0,
    )
    return alt_orbit, dv_deorbit, entry, r, state, v_circ, v_ei


@app.cell
def _(entry, mo, pl):
    df = pl.DataFrame(
        {
            "parameter": ["h_EI [km]", "V_EI [m/s]", "γ [deg]", "ψ [deg]", "β [kg/m²]"],
            "value": [
                entry.altitude_m / 1000,
                round(entry.velocity_m_s, 1),
                entry.flight_path_angle_deg,
                entry.heading_deg,
                entry.ballistic_coefficient_kg_m2,
            ],
        }
    )
    mo.ui.table(df)
    return df


@app.cell
def _(entry, load_state, mo, pl, save_state, save_table):
    state = load_state()
    state.entry = entry
    save_state(state)
    save_table("entry_interface", pl.DataFrame({"key": ["h", "V", "gamma"], "value": [entry.altitude_m, entry.velocity_m_s, entry.flight_path_angle_deg]}))
    mo.md("✓ EntryState → vehicle_state (entrada Camada 2)")
    return state


if __name__ == "__main__":
    app.run()
