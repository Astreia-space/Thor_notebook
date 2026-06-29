"""31 — Stability & trim: CG vs CP, margem estática."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_table
    from thor.io.inputs import num
    return load_state, mo, num, pl, save_table


@app.cell
def _(mo):
    mo.md("# Camada 3 — Stability & Trim\n\nInputs: `stability` section in `thor_inputs.csv`")
    return


@app.cell
def _(num):
    cg_x = num("stability", "cg_x_c")
    cp_x = num("stability", "cp_x_c")
    static_margin = cp_x - cg_x
    alpha_trim = num("stability", "alpha_trim_deg")
    return alpha_trim, cg_x, cp_x, static_margin


@app.cell
def _(alpha_trim, cg_x, cp_x, mo, pl, static_margin):
    df = pl.DataFrame(
        {
            "parameter": ["x_CG/c", "x_CP/c", "static_margin", "alpha_trim [deg]"],
            "value": [cg_x, cp_x, static_margin, alpha_trim],
        }
    )
    status = "estável" if static_margin < 0 else "instável — precisa superfície"
    mo.vstack(mo.md(f"**Status:** {status}"), mo.ui.table(df))
    return df, status


@app.cell
def _(df, mo, save_table):
    save_table("stability_trim", df)
    mo.md("✓ Trim → parquet")
    return


if __name__ == "__main__":
    app.run()
