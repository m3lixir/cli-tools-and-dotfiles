#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is not installed. Install it from https://brew.sh, then rerun this script." >&2
  exit 1
fi

brew bundle --file "$ROOT_DIR/Brewfile"

mkdir -p "$HOME/src" "$HOME/.local/bin"

echo "Bootstrap complete. Run ./scripts/link_dotfiles.sh next."

