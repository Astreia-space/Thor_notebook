# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.23.3",
# ]
# ///
"""00 — Mission CONOPS: fases, eventos, requisitos top-level → MissionSpec."""

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.constants import EI_ALTITUDE_M
    from thor.io.handoff import load_state, save_state, save_table
    from thor.models.mission_spec import MissionEvent, MissionPhase, MissionPhaseSpec, MissionSpec

    return (
        MissionEvent,
        MissionPhase,
        MissionPhaseSpec,
        MissionSpec,
        load_state,
        mo,
        pl,
        save_state,
        save_table,
    )


@app.cell
def _(mo):
    mo.md("""
    # Camada 0 — Mission CONOPS

    Fases: ascent → injection → phasing → rendezvous → docking →
    loiter → deorbit → EI → reentry → landing.
    """)
    return


@app.cell
def _(MissionPhase, MissionPhaseSpec):
    # Durações nominais [s] — ajuste aqui
    phase_data = [
        (MissionPhase.ASCENT, 600, 0, 0),
        (MissionPhase.INJECTION, 0, 9500, 0),  # ΔV herdado do lançador
        (MissionPhase.PHASING, 86400, 15, 200),
        (MissionPhase.RENDEZVOUS, 3600, 45, 150),
        (MissionPhase.DOCKING, 1800, 5, 100),
        (MissionPhase.LOITER, 604800, 2, 500),
        (MissionPhase.DEORBIT, 600, 100, 80),
        (MissionPhase.ENTRY_INTERFACE, 1, 0, 0),
        (MissionPhase.REENTRY, 900, 0, 50),
        (MissionPhase.LANDING, 600, 0, 30),
    ]
    phases = [
        MissionPhaseSpec(
            phase=p,
            duration_s=dur,
            delta_v_m_s=dv,
            power_wh=pwr,
            requirements={"EI_alt_m": 122_000} if p == MissionPhase.ENTRY_INTERFACE else {},
        )
        for p, dur, dv, pwr in phase_data
    ]
    return (phases,)


@app.cell
def _(MissionEvent, MissionPhase, MissionSpec, phases):
    events = [
        MissionEvent(name="Liftoff", phase=MissionPhase.ASCENT, t_offset_s=0, duration_s=600),
        MissionEvent(name="Orbit insertion", phase=MissionPhase.INJECTION, t_offset_s=600),
        MissionEvent(name="Deorbit burn cutoff", phase=MissionPhase.DEORBIT, t_offset_s=sum(p.duration_s for p in phases[:-3])),
        MissionEvent(name="Entry Interface", phase=MissionPhase.ENTRY_INTERFACE, t_offset_s=0, notes="~122 km"),
        MissionEvent(name="Touchdown", phase=MissionPhase.LANDING, t_offset_s=0),
    ]
    mission = MissionSpec(
        name="THOR-1",
        vehicle_class="lifting_body",
        phases=phases,
        events=events,
        top_level={
            "max_g_load": 4.0,
            "peak_heat_flux_W_cm2": 800.0,
            "downmass_kg": 500.0,
            "crossrange_km": 80.0,
            "EI_alt_m": 122_000,
        },
    )
    return (mission,)


@app.cell
def _(mission, mo, pl):
    df_phases = pl.DataFrame(
        {
            "phase": [p.phase.value for p in mission.phases],
            "duration_h": [p.duration_s / 3600 for p in mission.phases],
            "delta_v_m_s": [p.delta_v_m_s for p in mission.phases],
            "power_wh": [p.power_wh for p in mission.phases],
        }
    )
    summary = mo.vstack(
        mo.md(f"**Duração total:** {mission.total_duration_s/86400:.1f} dias"),
        mo.md(f"**ΔV missão:** {mission.total_delta_v_m_s:.0f} m/s (excl. ascent)"),
        mo.ui.table(df_phases),
    )
    summary
    return (df_phases,)


@app.cell
def _(df_phases, load_state, mission, mo, save_state, save_table):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.barh(df_phases["phase"], df_phases["duration_h"], color="#2563eb")
    ax.set_xlabel("Duração [h]")
    ax.set_title("Timeline de fases THOR")
    plt.tight_layout()
    mo.ui.pyplot(fig)

    state = load_state()
    state.mission = mission
    save_state(state)
    save_table("mission_phases", df_phases)
    mo.md("✓ `MissionSpec` → `data/vehicle_state.json` + `mission_phases.parquet`")
    return


if __name__ == "__main__":
    app.run()
