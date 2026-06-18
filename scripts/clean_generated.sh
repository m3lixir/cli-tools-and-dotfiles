#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Remove generated Python caches anywhere in the repo. These files are useful
# locally but should never become part of the portable environment history.
find "$ROOT_DIR" \
  \( -type d -name __pycache__ -prune -exec rm -rf {} + \) -o \
  \( -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*$py.class' \) -delete \)

echo "Generated Python cache cleanup complete."
