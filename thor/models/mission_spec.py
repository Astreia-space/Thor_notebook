"""MissionSpec — fases, eventos, durações e requisitos top-level."""

from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class MissionPhase(str, Enum):
    ASCENT = "ascent"
    INJECTION = "injection"
    PHASING = "phasing"
    RENDEZVOUS = "rendezvous"
    DOCKING = "docking"
    LOITER = "loiter"
    DEORBIT = "deorbit"
    ENTRY_INTERFACE = "entry_interface"
    REENTRY = "reentry"
    LANDING = "landing"


class MissionEvent(BaseModel):
    name: str
    phase: MissionPhase
    t_offset_s: float = Field(description="Tempo desde T0 [s]")
    duration_s: float = 0.0
    notes: str = ""


class MissionPhaseSpec(BaseModel):
    phase: MissionPhase
    duration_s: float
    delta_v_m_s: float = 0.0
    power_wh: float = 0.0
    requirements: dict[str, float | str] = Field(default_factory=dict)


class MissionSpec(BaseModel):
    name: str = "THOR-1"
    vehicle_class: str = "lifting_body"
    phases: list[MissionPhaseSpec]
    events: list[MissionEvent] = Field(default_factory=list)
    top_level: dict[str, float] = Field(
        default_factory=lambda: {
            "max_g_load": 4.0,
            "peak_heat_flux_W_cm2": 500.0,
            "downmass_kg": 500.0,
            "crossrange_km": 50.0,
        }
    )

    @property
    def total_duration_s(self) -> float:
        return sum(p.duration_s for p in self.phases)

    @property
    def total_delta_v_m_s(self) -> float:
        return sum(p.delta_v_m_s for p in self.phases)
