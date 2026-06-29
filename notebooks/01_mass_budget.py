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
"""01 — Mass Budget: MBS com margem AIAA S-120 (~30% conceitual)."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.constants import CONCEPTUAL_GROWTH
    from thor.io.handoff import load_state, save_state, save_table
    from thor.models.vehicle_state import MassBudget, MassItem
    return CONCEPTUAL_GROWTH, MassBudget, MassItem, load_state, mo, pl, save_state, save_table


@app.cell
def _(mo):
    mo.md("# Camada 0 — Mass Budget (MBS)")
    return


@app.cell
def _(CONCEPTUAL_GROWTH, MassItem):
    # Mass Breakdown Structure — valores iniciais [kg]
    base_items = [
        ("TPS", 800),
        ("Primary structure", 1200),
        ("Propulsion (dry)", 400),
        ("Avionics / GNC", 150),
        ("Power / EPS", 200),
        ("Thermal", 80),
        ("Payload", 500),
        ("Margin reserve", 0),
    ]
    items = [
        MassItem(name=n, dry_kg=m, growth_kg=m * CONCEPTUAL_GROWTH)
        for n, m in base_items
    ]
    return base_items, items


@app.cell
def _(CONCEPTUAL_GROWTH, items, mo, pl):
    df = pl.DataFrame(
        {
            "subsystem": [i.name for i in items],
            "dry_kg": [i.dry_kg for i in items],
            "growth_kg": [i.growth_kg for i in items],
            "total_kg": [i.total_kg for i in items],
        }
    )
    budget = MassBudget(items=items, growth_allowance=CONCEPTUAL_GROWTH, propellant_kg=600)
    totals = mo.vstack(
        mo.md(f"**Dry mass:** {budget.dry_mass_kg:.0f} kg"),
        mo.md(f"**Propellant:** {budget.propellant_kg:.0f} kg"),
        mo.md(f"**Wet mass:** {budget.wet_mass_kg:.0f} kg"),
        mo.md(f"**Com margem {CONCEPTUAL_GROWTH*100:.0f}%:** {budget.total_with_margin_kg:.0f} kg"),
        mo.ui.table(df),
    )
    totals
    return budget, df, totals


@app.cell
def _(budget, df, load_state, mo, pl, save_state, save_table):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(
        df["total_kg"],
        labels=df["subsystem"],
        autopct="%1.0f%%",
        startangle=90,
    )
    ax.set_title("MBS THOR (com growth allowance)")
    mo.ui.pyplot(fig)

    state = load_state()
    state.mass = budget
    save_state(state)
    save_table("mass_budget", df)
    mo.md("✓ Mass budget → vehicle_state (loop com propulsão em 42)")
    return ax, fig, plt, state


if __name__ == "__main__":
    app.run()
