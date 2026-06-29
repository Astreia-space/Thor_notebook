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
"""02 — ΔV Budget: injeção, phasing, rendezvous, deorbit, RCS."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_state, save_table
    from thor.models.vehicle_state import DeltaVBudget, DeltaVItem
    return DeltaVBudget, DeltaVItem, load_state, mo, pl, save_state, save_table


@app.cell
def _(mo):
    mo.md("# Camada 0 — ΔV Budget")
    return


@app.cell
def _(DeltaVItem):
    # ΔV por fase [m/s] + margem por item
    dv_items = [
        DeltaVItem(phase="injection (launcher)", delta_v_m_s=9500, margin_frac=0.0),
        DeltaVItem(phase="phasing", delta_v_m_s=15, margin_frac=0.10),
        DeltaVItem(phase="rendezvous/braking", delta_v_m_s=45, margin_frac=0.10),
        DeltaVItem(phase="station_keeping", delta_v_m_s=2, margin_frac=0.20),
        DeltaVItem(phase="deorbit", delta_v_m_s=100, margin_frac=0.05),
        DeltaVItem(phase="RCS/dispersions", delta_v_m_s=20, margin_frac=0.15),
    ]
    return dv_items


@app.cell
def _(DeltaVBudget, dv_items, mo, pl):
    budget = DeltaVBudget(items=dv_items)
    df = pl.DataFrame(
        {
            "phase": [i.phase for i in dv_items],
            "delta_v_m_s": [i.delta_v_m_s for i in dv_items],
            "margin_frac": [i.margin_frac for i in dv_items],
            "with_margin_m_s": [i.delta_v_m_s * (1 + i.margin_frac) for i in dv_items],
        }
    )
    onboard = sum(i.delta_v_m_s * (1 + i.margin_frac) for i in dv_items if "launcher" not in i.phase)
    mo.vstack(
        mo.md(f"**ΔV onboard (pós-injeção):** {onboard:.0f} m/s"),
        mo.md(f"**ΔV total missão:** {budget.total_m_s:.0f} m/s"),
        mo.ui.table(df),
    )
    return budget, df, onboard


@app.cell
def _(budget, df, load_state, mo, save_state, save_table):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(df["phase"], df["with_margin_m_s"], color="#dc2626")
    ax.set_ylabel("ΔV [m/s]")
    ax.set_title("Orçamento ΔV THOR")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    mo.ui.pyplot(fig)

    state = load_state()
    state.delta_v = budget
    save_state(state)
    save_table("delta_v_budget", df)
    mo.md("✓ ΔV budget → vehicle_state")
    return ax, fig, plt, state


if __name__ == "__main__":
    app.run()
