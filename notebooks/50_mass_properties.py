"""50 — Mass properties: inércia, CG tracking."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_table
    from thor.io.inputs import item_table, num
    return item_table, load_state, mo, num, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 5 — Mass Properties\n\nInputs: `geometry` + `mass_props` + payload CG")
    return


@app.cell
def _(item_table, load_state, num):
    state = load_state()
    m = state.mass.dry_mass_kg or 3500
    L = num("geometry", "length_m")
    W = num("geometry", "width_m")
    H = num("mass_props", "height_m")
    ixx = m / 12 * (W**2 + H**2)
    iyy = m / 12 * (L**2 + H**2)
    izz = m / 12 * (L**2 + W**2)
    payload = item_table("payload")
    cg = float((payload["mass_kg"] * payload["x_m"]).sum() / payload["mass_kg"].sum()) if len(payload) else L * 0.6
    return H, L, W, cg, ixx, iyy, izz, m, payload, state


@app.cell
def _(cg, ixx, iyy, izz, mo, pl):
    df = pl.DataFrame(
        {"parameter": ["Ixx", "Iyy", "Izz", "x_CG [m]"], "value": [round(ixx, 0), round(iyy, 0), round(izz, 0), round(cg, 2)]}
    )
    mo.ui.table(df)
    return df


@app.cell
def _(df, mo, save_table):
    save_table("mass_properties", df)
    mo.md("✓ Inércia/CG → parquet")
    return


if __name__ == "__main__":
    app.run()
