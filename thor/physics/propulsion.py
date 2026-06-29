"""Propulsão enxuta (substituível por Cantera/RocketCEA)."""

from __future__ import annotations

import math

from thor.constants import G0


def tsiolkovsky_delta_v(isp_s: float, m0_kg: float, mf_kg: float) -> float:
    return isp_s * G0 * math.log(m0_kg / mf_kg)


def mass_ratio(isp_s: float, delta_v_m_s: float) -> float:
    return math.exp(delta_v_m_s / (isp_s * G0))


def propellant_mass(m0_kg: float, isp_s: float, delta_v_m_s: float) -> float:
    mr = mass_ratio(isp_s, delta_v_m_s)
    return m0_kg * (1 - 1 / mr)
