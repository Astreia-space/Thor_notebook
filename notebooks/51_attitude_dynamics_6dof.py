# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.9.0",
#     "polars",
#     "matplotlib",
#     "numpy",
#     "pydantic>=2",
#     "duckdb",
#     "thor-notebook",
# ]
#
# [tool.uv.sources]
# thor-notebook = { path = "..", editable = true }
# ///
"""51 — Attitude dynamics 6DOF (quaternions)."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _(mo):
    mo.md("# Camada 5 — Attitude Dynamics 6DOF")
    return


@app.cell
def _(mo, np):
    # Quaternion kinematics: q̇ = 0.5 Ω(ω) q
    def omega_matrix(w):
        wx, wy, wz = w
        return 0.5 * np.array(
            [
                [0, -wx, -wy, -wz],
                [wx, 0, wz, -wy],
                [wy, -wz, 0, wx],
                [wz, wy, -wx, 0],
            ]
        )

    q = np.array([1.0, 0, 0, 0])
    w = np.array([0.01, 0.02, -0.005])  # rad/s
    dt = 1.0
    q_new = q + omega_matrix(w) @ q * dt
    q_new /= np.linalg.norm(q_new)
    mo.md(f"Quaternion após 1 s: `{q_new.round(4)}`")
    return dt, omega_matrix, q, q_new, w


if __name__ == "__main__":
    app.run()
