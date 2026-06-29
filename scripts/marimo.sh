#!/usr/bin/env bash
# Run marimo with the project venv (polars, thor, etc.)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -U pip
  .venv/bin/pip install -U -r requirements.txt
  .venv/bin/pip install -e .
fi

NB="${1:-notebooks/00_mission_conops.py}"
exec .venv/bin/marimo edit "$NB"
