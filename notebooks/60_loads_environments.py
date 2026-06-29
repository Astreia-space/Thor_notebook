"""60 — Loads environments: launch, reentry, docking, landing."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_table, save_table
    return load_table, mo, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 6 — Loads Environments")
    return


@app.cell
def _(load_table, pl):
    traj = load_table("entry_trajectory")
    g_peak = float(traj["g_load"].max()) if traj is not None else 4.0
    docking = load_table("docking_approach")
    f_dock = 175 if docking is None else 3500 * 0.05
    df = pl.DataFrame(
        {
            "case": ["Launch quasi-static", "Launch acoustic", "Reentry", "Docking", "Landing"],
            "load": [6.0, 140, g_peak, f_dock, 8.0],
            "unit": ["g", "dB OASPL", "g", "N", "g"],
        }
    )
    return df, docking, f_dock, g_peak, traj


@app.cell
def _(df, mo, save_table):
    mo.ui.table(df)
    save_table("loads_environments", df)
    mo.md("✓ Casos de carga → 61_primary_structure")
    return


if __name__ == "__main__":
    app.run()
