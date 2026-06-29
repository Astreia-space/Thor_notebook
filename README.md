# THOR — Actical Hypersonic Orbital Reentry

Lean sizing pipeline for a hypersonic orbital reentry vehicle. Marimo notebooks share state via Pydantic (`data/vehicle_state.json`) and Polars tables (`data/parquet/`). Notebooks cover mission budgets, astrodynamics, reentry, aero, propulsion, GNC, structures, thermal, geometry, and MDAO trades.

## Setup

```bash
cd thor_notebook
pip install -e .
```

## Run

**Browser**

```bash
marimo edit notebooks/00_mission_conops.py
```

**Cursor / VS Code**

1. Install the [marimo extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) (`marimo-team.vscode-marimo`)
2. Open a notebook → marimo icon (top-right), or `Cmd+Shift+P` → `marimo: Open as marimo notebook`
3. Select the Python interpreter for this project

## Suggested order

`00`–`04` → `10`, `12`–`14` → `20`–`24` → `30`–`33` → `40`–`42` → `50`–`53` → `60`–`62` → `70`–`71` → `80`–`81` → `90`–`91`
