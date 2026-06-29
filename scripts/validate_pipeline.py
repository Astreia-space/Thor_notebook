#!/usr/bin/env python3
"""Validate thor_inputs.csv and pipeline state without Marimo UI."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from thor.io.handoff import load_state, save_state
from thor.io.inputs import float_list, item_table, load_inputs, num, phase_rows, txt
from thor.models.mission_spec import MissionPhase, MissionPhaseSpec, MissionSpec
from thor.models.vehicle_state import (
    DeltaVBudget,
    DeltaVItem,
    EntryState,
    LinkBudget,
    MassBudget,
    MassItem,
    OrbitState,
    PowerBudget,
    PowerItem,
)
from thor.physics.entry import integrate_entry_3dof
from thor.physics.propulsion import propellant_mass


def main() -> None:
    df = load_inputs()
    print(f"inputs: {len(df)} rows")

    phases = [
        MissionPhaseSpec(
            phase=MissionPhase(r["item"]),
            duration_s=float(r["duration_s"]),
            delta_v_m_s=float(r["delta_v_m_s"]),
            power_wh=float(r["power_wh"]),
        )
        for r in phase_rows()
    ]
    mission = MissionSpec(
        name=txt("mission", "name"),
        vehicle_class=txt("mission", "vehicle_class"),
        phases=phases,
    )

    growth = num("mass", "growth_allowance", "_config")
    mass = MassBudget(
        items=[MassItem(name=r["item"], dry_kg=float(r["dry_kg"]), growth_kg=float(r["dry_kg"]) * growth) for r in __import__("thor.io.inputs", fromlist=["items_with_params"]).items_with_params("mass", "dry_kg")],
        growth_allowance=growth,
        propellant_kg=num("mass", "propellant_kg", "_config"),
    )

    state = load_state()
    state.mission = mission
    state.mass = mass
    state.orbit = OrbitState(altitude_km=num("orbit", "altitude_km"), inclination_deg=num("orbit", "inclination_deg"))
    state.entry = EntryState(
        altitude_m=num("entry", "altitude_m"),
        velocity_m_s=7800.0,
        flight_path_angle_deg=num("entry", "flight_path_angle_deg"),
        ballistic_coefficient_kg_m2=num("entry", "ballistic_coefficient_kg_m2"),
    )
    state.aero.cd = num("aero", "cd")
    state.aero.reference_area_m2 = num("geometry", "length_m") * num("geometry", "width_m") * num("geometry", "s_ref_factor")
    save_state(state)

    traj = integrate_entry_3dof(
        state.entry.altitude_m,
        state.entry.velocity_m_s,
        math.radians(state.entry.flight_path_angle_deg),
        state.entry.ballistic_coefficient_kg_m2,
        dt=2.0,
    )
    g_peak = float(traj["g_load"].max())
    assert len(phases) == 10
    assert len(float_list("aero_db", "mach_list")) >= 3
    assert len(item_table("docking")) == 4
    assert len(item_table("nav")) == 4
    print(f"pipeline OK — g_peak={g_peak:.2f} g, dry_mass={mass.dry_mass_kg:.0f} kg")


if __name__ == "__main__":
    main()
