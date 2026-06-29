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
"""33 — Terminal descent: paraquedas ou glide subsônico."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_table
    return load_state, mo, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 3 — Terminal Descent")
    return


@app.cell
def _(load_state):
    state = load_state()
    mass = state.mass.dry_mass_kg if state.mass.dry_mass_kg else 3500
    ld = state.aero.ld if state.aero.ld else 0.5
    v_terminal = 55  # m/s antes paraquedas
    # Glide subsônico: V L/D ≈ mg → V = mg/(ρ S Cl) ...
    glide_slope = 4.0  # deg
    df = pl.DataFrame(
        {
            "mode": ["supersonic_drogue", "main_chute", "glide_approach"],
            "altitude_km": [10, 3, 0.5],
            "velocity_m_s": [450, 120, v_terminal],
            "notes": ["Mortar deploy", f"L/D={ld:.2f}", f"slope={glide_slope}°"],
        }
    )
    return df, glide_slope, ld, mass, state, v_terminal


@app.cell
def _(df, mo, save_table):
    mo.ui.table(df)
    save_table("terminal_descent", df)
    mo.md("✓ Perfil terminal → parquet")
    return


if __name__ == "__main__":
    app.run()
