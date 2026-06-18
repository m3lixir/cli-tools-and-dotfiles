#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Point this clone at the tracked hook directory so bootstrap can install the
# same pre-commit behavior on a new machine.
git -C "$ROOT_DIR" config core.hooksPath .githooks

echo "Configured Git hooks from .githooks."
