"""Aerodinâmica hipersônica enxuta."""

from __future__ import annotations

import math


def modified_newton_cp(cp_max: float, theta_rad: float) -> float:
    """Cp = Cp_max · sin²θ (Newtoniano modificado)."""
    return cp_max * math.sin(theta_rad) ** 2


def hypersonic_cd_cl(cp_max: float, alpha_rad: float, s_ref_ratio: float = 0.3) -> tuple[float, float]:
    """Estimativa Cl/Cd a partir de Cp_max e α."""
    cd = cp_max * math.sin(alpha_rad) ** 2 * s_ref_ratio + 0.1
    cl = cp_max * math.sin(2 * alpha_rad) * s_ref_ratio
    return cd, cl
