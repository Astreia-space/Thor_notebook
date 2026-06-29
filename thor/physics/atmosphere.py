"""Modelos atmosféricos enxutos."""

from __future__ import annotations

import math

from thor.constants import US76_RHO0


def us76_density(h_m: float) -> float:
    """US Standard 1976 — aproximação exponencial por faixa."""
    h_m = max(h_m, 0.0)
    scale_heights = [
        (0, 8500, US76_RHO0),
        (25_000, 6000, 3.9e-2),
        (50_000, 8000, 1.0e-3),
    ]
    if h_m >= 80_000:
        return 1.8e-5 * math.exp(-(h_m - 80_000) / 7000)
    rho = US76_RHO0
    h_ref = 0.0
    for h_base, H, rho_base in scale_heights:
        if h_m >= h_base:
            h_ref, rho, H_use = h_base, rho_base, H
        else:
            break
    return rho * math.exp(-(h_m - h_ref) / H_use)


def nrlmsise00_placeholder(h_m: float) -> float:
    """Placeholder NRLMSISE-00 — substituir por biblioteca real."""
    return us76_density(h_m)
