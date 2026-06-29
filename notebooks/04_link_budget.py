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
"""04 — Link Budget RF (blackout de plasma na reentrada)."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import math
    import polars as pl

    from thor.io.handoff import load_state, save_state, save_table
    from thor.models.vehicle_state import LinkBudget
    return LinkBudget, load_state, math, mo, pl, save_state, save_table


@app.cell
def _(mo):
    mo.md(
        """
        # Camada 0 — Link Budget

        **Nota:** deorbit/reentry → blackout de plasma (~40–80 km).
        Telemetria via store-and-forward ou relay.
        """
    )
    return


@app.cell
def _(LinkBudget):
    scenarios = [
        LinkBudget(
            frequency_hz=2.2e9,
            tx_power_W=10,
            tx_gain_dBi=0,
            rx_gain_dBi=30,
            path_loss_dB=180,
            required_snr_dB=10,
            margin_dB=3,
        ),
        LinkBudget(
            frequency_hz=2.2e9,
            tx_power_W=10,
            tx_gain_dBi=0,
            rx_gain_dBi=30,
            path_loss_dB=200,
            required_snr_dB=10,
            margin_dB=3,
            blackout_notes="Reentry blackout — link indisponível",
        ),
    ]
    return scenarios


@app.cell
def _(math, mo, pl, scenarios):
    rows = []
    for i, lb in enumerate(scenarios):
        noise_floor = -174 + 10 * math.log10(lb.frequency_hz)
        required = noise_floor + lb.required_snr_dB + lb.margin_dB
        rows.append(
            {
                "scenario": ["On-orbit", "Reentry (blackout)"][i],
                "rx_power_dBm": lb.received_power_dBm,
                "required_dBm": required,
                "link_ok": lb.link_ok,
                "notes": lb.blackout_notes[:40],
            }
        )
    df = pl.DataFrame(rows)
    mo.ui.table(df)
    return df, rows


@app.cell
def _(df, load_state, mo, save_state, save_table):
    state = load_state()
    state.link = LinkBudget()  # nominal on-orbit
    save_state(state)
    save_table("link_budget", df)
    mo.md(f"✓ Link budget → vehicle_state\n\n{state.link.blackout_notes}")
    return state


if __name__ == "__main__":
    app.run()
