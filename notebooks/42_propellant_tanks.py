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
"""42 — Propellant tanks: volume, pressão, blowdown."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_state, save_table
    return load_state, mo, pl, save_state, save_table


@app.cell
def _(mo):
    mo.md("# Camada 4 — Propellant Tanks")
    return


@app.cell
def _(load_state):
    state = load_state()
    mp = state.mass.propellant_kg or 600
    rho_prop = 1100  # kg/m³ storable
    volume_m3 = mp / rho_prop * 1.05  # 5% ullage
    p_tank = 2.5e6  # Pa regulated
    tank_mass = volume_m3 * 50  # kg/m³ shell heuristic
    return mp, p_tank, rho_prop, state, tank_mass, volume_m3


@app.cell
def _(mo, mp, p_tank, pl, tank_mass, volume_m3):
    df = pl.DataFrame(
        {
            "parameter": ["V_tank [m³]", "P [bar]", "m_prop [kg]", "m_tank [kg]"],
            "value": [round(volume_m3, 2), p_tank / 1e5, mp, round(tank_mass, 0)],
        }
    )
    mo.ui.table(df)
    return df


@app.cell
def _(load_state, mo, pl, save_state, save_table, tank_mass):
    state = load_state()
    for item in state.mass.items:
        if "Propulsion" in item.name:
            item.dry_kg += tank_mass
    save_state(state)
    save_table("propellant_tanks", pl.DataFrame({"tank_mass_kg": [tank_mass]}))
    mo.md("✓ Tanques → mass budget (loop fechado com 01)")
    return state


if __name__ == "__main__":
    app.run()
