#!/usr/bin/env bash
set -euo pipefail

missing=0

check_command() {
  local command_name="$1"
  if command -v "$command_name" >/dev/null 2>&1; then
    printf 'ok: %s\n' "$command_name"
  else
    printf 'missing: %s\n' "$command_name"
    missing=1
  fi
}

check_link() {
  local target="$1"
  if [ -L "$target" ]; then
    printf 'ok: linked %s\n' "$target"
  else
    printf 'missing link: %s\n' "$target"
    missing=1
  fi
}

check_command git
check_command gh
check_command brew
check_command shellcheck
check_command glow

check_link "$HOME/.zshrc"
check_link "$HOME/.gitconfig"
check_link "$HOME/.gitignore_global"
check_link "$HOME/.shellcheckrc"

if [ "$missing" -ne 0 ]; then
  echo "Environment verification found missing pieces." >&2
  exit 1
fi

echo "Environment verification passed."

