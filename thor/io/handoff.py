"""Handoff entre notebooks: VehicleState (JSON) + tabelas Polars (Parquet/DuckDB)."""

from __future__ import annotations

import json
from pathlib import Path

import polars as pl

from thor.models.vehicle_state import VehicleState

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
STATE_FILE = DATA_DIR / "vehicle_state.json"
PARQUET_DIR = DATA_DIR / "parquet"
DUCKDB_PATH = DATA_DIR / "thor.duckdb"


def state_path() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_FILE


def save_state(state: VehicleState) -> Path:
    p = state_path()
    p.write_text(state.model_dump_json(indent=2))
    return p


def load_state() -> VehicleState:
    p = state_path()
    if not p.exists():
        return VehicleState()
    return VehicleState.model_validate_json(p.read_text())


def save_table(name: str, df: pl.DataFrame) -> Path:
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)
    out = PARQUET_DIR / f"{name}.parquet"
    df.write_parquet(out)
    return out


def load_table(name: str) -> pl.DataFrame | None:
    path = PARQUET_DIR / f"{name}.parquet"
    if not path.exists():
        return None
    return pl.read_parquet(path)


def register_duckdb(name: str, df: pl.DataFrame) -> None:
    """Registra tabela no DuckDB local para queries cross-notebook."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    import duckdb

    con = duckdb.connect(str(DUCKDB_PATH))
    con.register("_tmp", df.to_arrow())
    con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM _tmp")
    con.close()
