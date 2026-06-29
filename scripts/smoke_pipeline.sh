#!/usr/bin/env bash
# Validate inputs + core pipeline (no Marimo server)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec "${ROOT}/.venv/bin/python" "${ROOT}/scripts/validate_pipeline.py"
