#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$(cd "$REPO_ROOT/.." && pwd)/.venv"

if [ -d "$VENV_DIR" ]; then
  . "$VENV_DIR/bin/activate"
fi

cd "$REPO_ROOT"
python -m pytest -q sirius_tests/test_light_bugs.py
