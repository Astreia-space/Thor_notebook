"""13 — Proximity ops & docking: V-bar/R-bar, closing velocity."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import save_table
    return mo, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 1 — Proximity Ops & Docking")
    return


@app.cell
def _(mo, pl):
    # Elipsoide de aproximação simplificado (Keep-out + approach)
    approach = pl.DataFrame(
        {
            "gate": ["Waypoint 4", "Waypoint 3", "Waypoint 2", "Capture"],
            "range_m": [300, 30, 3, 0.1],
            "closing_vel_m_s": [0.10, 0.05, 0.03, 0.01],
            "mode": ["V-bar", "V-bar", "R-bar", "R-bar"],
        }
    )
    # Carga de docking: F = m · a
    m_dock = 3500  # kg
    a_contact = 0.05  # m/s²
    f_dock = m_dock * a_contact
    mo.vstack(
        mo.md(f"**Carga de contato estimada:** {f_dock:.0f} N → alimenta 60_loads"),
        mo.ui.table(approach),
    )
    return a_contact, approach, f_dock, m_dock


@app.cell
def _(approach, mo, save_table):
    save_table("docking_approach", approach)
    mo.md("✓ Approach profile → parquet")
    return


if __name__ == "__main__":
    app.run()
