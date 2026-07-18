#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

if [[ ! -x .venv/bin/hydra-mlx-demo ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -e '.[dev]'
fi

exec .venv/bin/hydra-mlx-demo
