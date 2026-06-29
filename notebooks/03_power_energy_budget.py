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
"""03 — Power / Energy Budget: Wh por fase."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.handoff import load_state, save_state, save_table
    from thor.models.vehicle_state import PowerBudget, PowerItem
    return PowerBudget, PowerItem, load_state, mo, pl, save_state, save_table


@app.cell
def _(mo):
    mo.md("# Camada 0 — Power / Energy Budget")
    return


@app.cell
def _(PowerItem, load_state):
    state = load_state()
    # Potência média [W] × duração [s] por fase
    defaults = [
        ("phasing", 200, 86400),
        ("rendezvous", 150, 3600),
        ("docking", 100, 1800),
        ("loiter", 500, 604800),
        ("deorbit", 80, 600),
        ("reentry (battery only)", 50, 900),
        ("landing", 30, 600),
    ]
    if state.mission:
        # Sobrescreve durações da missão quando disponível
        dur_map = {p.phase.value: p.duration_s for p in state.mission.phases}
        items = []
        for name, pwr, _ in defaults:
            key = name.split()[0]
            dur = dur_map.get(key, defaults[[d[0] for d in defaults].index(name)][2])
            items.append(PowerItem(phase=name, average_power_W=pwr, duration_s=dur))
    else:
        items = [PowerItem(phase=n, average_power_W=p, duration_s=d) for n, p, d in defaults]
    return defaults, items, state


@app.cell
def _(PowerBudget, items, mo, pl):
    budget = PowerBudget(items=items)
    df = pl.DataFrame(
        {
            "phase": [i.phase for i in items],
            "power_W": [i.average_power_W for i in items],
            "duration_h": [i.duration_s / 3600 for i in items],
            "energy_Wh": [i.energy_wh for i in items],
        }
    )
    mo.vstack(
        mo.md(f"**Energia total:** {budget.total_wh:.0f} Wh ({budget.total_wh/1000:.1f} kWh)"),
        mo.ui.table(df),
    )
    return budget, df


@app.cell
def _(budget, df, load_state, mo, save_state, save_table):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(df["phase"], df["energy_Wh"], color="#16a34a")
    ax.set_ylabel("Energia [Wh]")
    ax.set_title("Orçamento energético por fase")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    mo.ui.pyplot(fig)

    state = load_state()
    state.power = budget
    save_state(state)
    save_table("power_budget", df)
    mo.md("✓ Power budget → vehicle_state")
    return ax, fig, plt, state


if __name__ == "__main__":
    app.run()
