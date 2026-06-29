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
"""31 — Stability & trim: CG vs CP, margem estática."""

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
    mo.md("# Camada 3 — Stability & Trim")
    return


@app.cell
def _(load_state):
    state = load_state()
    cg_x = 0.62  # x/c — lifting body: CG aft
    cp_x = 0.58
    static_margin = (cp_x - cg_x)  # neg = instável em α
    alpha_trim = 8.0  # deg — from aero DB
    return alpha_trim, cg_x, cp_x, state, static_margin


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
