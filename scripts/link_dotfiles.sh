#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$HOME/.dotfiles-backup/$(date +%Y%m%d-%H%M%S)"

link_file() {
  local source="$1"
  local target="$2"

  mkdir -p "$(dirname "$target")"

  if [ -L "$target" ] && [ "$(readlink "$target")" = "$source" ]; then
    echo "Already linked: $target"
    return
  fi

  if [ -e "$target" ] || [ -L "$target" ]; then
    mkdir -p "$BACKUP_DIR"
    mv "$target" "$BACKUP_DIR/"
    echo "Backed up existing $target to $BACKUP_DIR"
  fi

  ln -s "$source" "$target"
  echo "Linked $target -> $source"
}

link_file "$ROOT_DIR/dotfiles/zshrc" "$HOME/.zshrc"
link_file "$ROOT_DIR/dotfiles/gitconfig" "$HOME/.gitconfig"
link_file "$ROOT_DIR/dotfiles/gitignore_global" "$HOME/.gitignore_global"
link_file "$ROOT_DIR/dotfiles/shellcheckrc" "$HOME/.shellcheckrc"

echo "Dotfile linking complete."

