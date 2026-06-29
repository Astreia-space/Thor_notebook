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
    from thor.io.inputs import num
    from thor.models.vehicle_state import LinkBudget
    return LinkBudget, load_state, math, mo, num, pl, save_state, save_table


@app.cell
def _(mo):
    mo.md("# Camada 0 — Link Budget\n\nInputs: `link` section in `thor_inputs.csv`")
    return


@app.cell
def _(LinkBudget, num):
    def link_cfg(item: str) -> LinkBudget:
        return LinkBudget(
            frequency_hz=num("link", "frequency_hz", item),
            tx_power_W=num("link", "tx_power_W", item),
            tx_gain_dBi=num("link", "tx_gain_dBi", item),
            rx_gain_dBi=num("link", "rx_gain_dBi", item),
            path_loss_dB=num("link", "path_loss_dB", item),
            required_snr_dB=num("link", "required_snr_dB", item),
            margin_dB=num("link", "margin_dB", item),
            blackout_notes="Reentry blackout — link indisponível" if item == "reentry" else LinkBudget().blackout_notes,
        )

    scenarios = [link_cfg("on_orbit"), link_cfg("reentry")]
    return link_cfg, scenarios


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
def _(df, link_cfg, load_state, mo, save_state, save_table):
    state = load_state()
    state.link = link_cfg("on_orbit")
    save_state(state)
    save_table("link_budget", df)
    mo.md(f"✓ Link budget → vehicle_state\n\n{state.link.blackout_notes}")
    return state


if __name__ == "__main__":
    app.run()
