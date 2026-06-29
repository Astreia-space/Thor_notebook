"""53 — Navigation filters: IMU, EKF/UKF."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell
def _(mo):
    mo.md("# Camada 5 — Navigation (sistema inercial)")
    return


@app.cell
def _(mo, pl):
    # Erros típicos IMU + sensores
    df = pl.DataFrame(
        {
            "sensor": ["IMU gyro", "IMU accel", "Star tracker", "GNSS"],
            "error": ["0.01 °/s", "100 μg", "10 arcsec", "5 m"],
            "phase": ["all", "all", "on-orbit", "ascent/landing"],
        }
    )
    mo.vstack(
        mo.md("EKF/UKF: fusão IMU + ST + GNSS (implementar com filterpy/etc.)"),
        mo.ui.table(df),
    )
    return df


if __name__ == "__main__":
    app.run()
