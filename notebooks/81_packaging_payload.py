"""81 — Payload packaging & CG."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_table
    from thor.io.inputs import items_with_params
    return items_with_params, load_state, mo, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 8 — Payload Packaging\n\nInputs: `payload` section in `thor_inputs.csv`")
    return


@app.cell
def _(items_with_params):
    rows = items_with_params("payload", "mass_kg", "x_m")
    items = [(r["item"], float(r["mass_kg"]), float(r["x_m"])) for r in rows]
    m_total = sum(i[1] for i in items)
    x_cg = sum(m * x for _, m, x in items) / m_total if m_total else 0
    return items, m_total, x_cg


@app.cell
def _(items, mo, pl, x_cg):
    df = pl.DataFrame({"item": [i[0] for i in items], "mass_kg": [i[1] for i in items], "x_m": [i[2] for i in items]})
    mo.vstack(mo.md(f"**x_CG payload:** {x_cg:.2f} m"), mo.ui.table(df))
    return df


@app.cell
def _(df, mo, save_table):
    save_table("payload_packaging", df)
    mo.md("✓ Layout → 50_mass_properties, 31_stability")
    return


if __name__ == "__main__":
    app.run()
