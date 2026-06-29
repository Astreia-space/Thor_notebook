"""Reentrada 3DOF, Allen-Eggers, Sutton-Graves."""

from __future__ import annotations

import math

import numpy as np

from thor.constants import G0, R_EARTH
from thor.physics.atmosphere import nrlmsise00_placeholder


def ballistic_coefficient(mass_kg: float, cd: float, area_m2: float) -> float:
    return mass_kg / (cd * area_m2)


def allen_eggers_peak_heat(
    velocity_m_s: float, rho_n: float, rn_m: float
) -> tuple[float, float]:
    """
    Sanity-check analítico Allen-Eggers.
    Retorna (q_dot_W_m2, g_peak) aproximados.
    """
    # q̇ ∝ √(ρ/Rn) V³ (Sutton-Graves form)
    q = 1.83e-4 * math.sqrt(rho_n / rn_m) * velocity_m_s**3
    g_peak = 0.002 * velocity_m_s**2 / (math.sqrt(ballistic_coefficient(1000, 0.8, 10)))
    return q, g_peak


def sutton_graves(W_cm2: bool, rho: float, rn_m: float, v_m_s: float) -> float:
    """Fluxo convectivo de estagnação [W/m² ou W/cm²]."""
    q = 1.83e-4 * math.sqrt(rho / rn_m) * v_m_s**3
    return q / 1e4 if W_cm2 else q


def integrate_entry_3dof(
    h0_m: float,
    v0_m_s: float,
    gamma0_rad: float,
    beta_kg_m2: float,
    dt: float = 0.5,
) -> dict[str, np.ndarray]:
    """
    Integrador 3DOF balístico: dh/dt = V sinγ, dV/dt = -ρV²/(2β) - g sinγ.
    """
    h, v, gamma = h0_m, v0_m_s, gamma0_rad
    t, hs, vs, gs, rhos, qs = [0.0], [h], [v], [gamma], [nrlmsise00_placeholder(h)], [0.0]
    while h > 0 and v > 0 and t[-1] < 3600:
        rho = nrlmsise00_placeholder(h)
        g = G0 * (R_EARTH / (R_EARTH + h)) ** 2
        dv = (-rho * v**2 / (2 * beta_kg_m2) - g * math.sin(gamma)) * dt
        dh = v * math.sin(gamma) * dt
        # Curvatura terrestre simplificada
        dg = (v / (R_EARTH + h) - g / v * math.cos(gamma)) * math.cos(gamma) * dt / v if v > 1 else 0
        v = max(v + dv, 0)
        h = h + dh
        gamma = gamma + dg
        t.append(t[-1] + dt)
        hs.append(h)
        vs.append(v)
        gs.append(-dv / dt / G0 if dt else 0)
        rhos.append(rho)
        qs.append(sutton_graves(True, rho, 0.5, v))
    return {
        "t_s": np.array(t),
        "h_m": np.array(hs),
        "v_m_s": np.array(vs),
        "g_load": np.array(gs),
        "rho": np.array(rhos),
        "q_W_cm2": np.array(qs),
    }
