# THOR — Actical Hypersonic Orbital Reentry

Lean sizing pipeline for a hypersonic orbital reentry vehicle. Marimo notebooks share state via Pydantic (`data/vehicle_state.json`) and Polars tables (`data/parquet/`). Notebooks cover mission budgets, astrodynamics, reentry, aero, propulsion, GNC, structures, thermal, geometry, and MDAO trades.

## Setup

```bash
cd thor_notebook
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U -r requirements.txt
pip install -e .
```

**Edit all sizing numbers in one spreadsheet:** `data/inputs/thor_inputs.csv`  
Sections: `mission`, `phase`, `mass`, `delta_v`, `link`, `orbit`, `entry`, `aero`, `geometry`, `propulsion`, `tps`, `docking`, `nav`, `loads`, `thermal`, `power`, `mdao`, `trade`, …  
Preview: `00_inputs.py` · validate: `./scripts/validate_pipeline.py`

## Run

**Browser** (always use the project venv — do not use system `marimo`)

```bash
source .venv/bin/activate
.venv/bin/marimo edit notebooks/00_mission_conops.py
# or:
./scripts/marimo.sh notebooks/00_mission_conops.py
```

**Cursor / VS Code**

1. Install the [marimo extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) (`marimo-team.vscode-marimo`)
2. Open a notebook → marimo icon (top-right), or `Cmd+Shift+P` → `marimo: Open as marimo notebook`
3. Select interpreter: **`thor_notebook/.venv/bin/python`**

## Suggested order

`00_inputs` → `00`–`04` → `10`, `12`–`14` → `20`–`24` → `30`–`33` → `40`–`42` → `50`–`53` → `60`–`62` → `70`–`71` → `80`–`81` → `90`–`91`
