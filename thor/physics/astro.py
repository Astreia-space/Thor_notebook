"""Astrodinâmica enxuta (substituível por Orekit/poliastro)."""

from __future__ import annotations

import math

import numpy as np

from thor.constants import G0, MU_EARTH, R_EARTH


def circular_velocity(altitude_m: float) -> float:
    r = R_EARTH + altitude_m
    return math.sqrt(MU_EARTH / r)


def hohmann_delta_v(alt1_m: float, alt2_m: float) -> tuple[float, float]:
    """ΔV1 (perigee burn) e ΔV2 (apogee burn) para transferência Hohmann."""
    r1 = R_EARTH + alt1_m
    r2 = R_EARTH + alt2_m
    a = (r1 + r2) / 2
    v1 = math.sqrt(MU_EARTH / r1)
    v_t1 = math.sqrt(MU_EARTH * (2 / r1 - 1 / a))
    v_t2 = math.sqrt(MU_EARTH * (2 / r2 - 1 / a))
    v2 = math.sqrt(MU_EARTH / r2)
    return v_t1 - v1, v2 - v_t2


def hill_clohessy_wiltshire(
    n: float, dt: float, x0: np.ndarray
) -> np.ndarray:
    """
    Estado relativo CW: x = [x, y, z, dx, dy, dz].
    n = mean motion [rad/s], dt [s].
    """
    c, s = math.cos(n * dt), math.sin(n * dt)
    phi = np.array(
        [
            [4 - 3 * c, 0, 0, s / n, 2 * (1 - c) / n, 0],
            [6 * (s - n * dt), 1, 0, -2 * (1 - c) / n, (4 * s - 3 * n * dt) / n, 0],
            [0, 0, c, 0, 0, s / n],
            [3 * n * s, 0, 0, c, 2 * s, 0],
            [-6 * n * (1 - c), 0, 0, -2 * s, 4 * c - 3, 0],
            [0, 0, -n * s, 0, 0, c],
        ]
    )
    return phi @ x0


def mean_motion(altitude_m: float) -> float:
    r = R_EARTH + altitude_m
    return math.sqrt(MU_EARTH / r**3)
