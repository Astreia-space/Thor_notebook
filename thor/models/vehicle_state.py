"""VehicleState — handoff central entre notebooks (Pydantic v2)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from thor.models.mission_spec import MissionSpec


class MassItem(BaseModel):
    name: str
    dry_kg: float = 0.0
    growth_kg: float = 0.0

    @property
    def total_kg(self) -> float:
        return self.dry_kg + self.growth_kg


class MassBudget(BaseModel):
    items: list[MassItem] = Field(default_factory=list)
    growth_allowance: float = 0.30
    propellant_kg: float = 0.0

    @property
    def dry_mass_kg(self) -> float:
        return sum(i.total_kg for i in self.items)

    @property
    def wet_mass_kg(self) -> float:
        return self.dry_mass_kg + self.propellant_kg

    @property
    def total_with_margin_kg(self) -> float:
        return self.wet_mass_kg * (1.0 + self.growth_allowance)


class DeltaVItem(BaseModel):
    phase: str
    delta_v_m_s: float
    margin_frac: float = 0.10


class DeltaVBudget(BaseModel):
    items: list[DeltaVItem] = Field(default_factory=list)

    @property
    def total_m_s(self) -> float:
        return sum(i.delta_v_m_s * (1.0 + i.margin_frac) for i in self.items)


class PowerItem(BaseModel):
    phase: str
    average_power_W: float
    duration_s: float

    @property
    def energy_wh(self) -> float:
        return self.average_power_W * self.duration_s / 3600.0


class PowerBudget(BaseModel):
    items: list[PowerItem] = Field(default_factory=list)

    @property
    def total_wh(self) -> float:
        return sum(i.energy_wh for i in self.items)


class LinkBudget(BaseModel):
    frequency_hz: float = 2.2e9
    tx_power_W: float = 10.0
    tx_gain_dBi: float = 0.0
    rx_gain_dBi: float = 30.0
    path_loss_dB: float = 180.0
    required_snr_dB: float = 10.0
    margin_dB: float = 3.0
    blackout_notes: str = (
        "Deorbit/reentry: plasma blackout ~40–80 km; "
        "telemetria via relay ou armazenamento a bordo."
    )

    @property
    def received_power_dBm(self) -> float:
        tx_dbm = 10 * __import__("math").log10(self.tx_power_W * 1000)
        return tx_dbm + self.tx_gain_dBi + self.rx_gain_dBi - self.path_loss_dB

    @property
    def link_ok(self) -> bool:
        return self.received_power_dBm > (-174 + 10 * __import__("math").log10(self.frequency_hz) + self.required_snr_dB + self.margin_dB)


class OrbitState(BaseModel):
    altitude_km: float = 400.0
    inclination_deg: float = 51.6
    eccentricity: float = 0.0
    raan_deg: float = 0.0
    arg_perigee_deg: float = 0.0
    true_anomaly_deg: float = 0.0


class EntryState(BaseModel):
    altitude_m: float = 122_000.0
    velocity_m_s: float = 7800.0
    flight_path_angle_deg: float = -1.0
    heading_deg: float = 90.0
    ballistic_coefficient_kg_m2: float = 200.0


class AeroBudget(BaseModel):
    cd: float = 0.8
    cl: float = 0.3
    reference_area_m2: float = 10.0
    nose_radius_m: float = 0.5

    @property
    def ld(self) -> float:
        return self.cl / self.cd if self.cd else 0.0


class VehicleState(BaseModel):
    mission: MissionSpec | None = None
    mass: MassBudget = Field(default_factory=MassBudget)
    delta_v: DeltaVBudget = Field(default_factory=DeltaVBudget)
    power: PowerBudget = Field(default_factory=PowerBudget)
    link: LinkBudget = Field(default_factory=LinkBudget)
    orbit: OrbitState = Field(default_factory=OrbitState)
    entry: EntryState = Field(default_factory=EntryState)
    aero: AeroBudget = Field(default_factory=AeroBudget)
    notes: dict[str, str] = Field(default_factory=dict)
