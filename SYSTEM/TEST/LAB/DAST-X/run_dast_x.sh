#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

if [ -z "${DASTX_REPO_ROOT:-}" ]; then
  if git rev-parse --show-toplevel >/dev/null 2>&1; then
    export DASTX_REPO_ROOT="$(git rev-parse --show-toplevel)"
  else
    export DASTX_REPO_ROOT="$HOME/W3_HB_team_BXCGICOG"
  fi
fi

export DASTX_HOST="${DASTX_HOST:-127.0.0.1}"
export DASTX_PORT="${DASTX_PORT:-8181}"
export DASTX_DATA_DIR="${DASTX_DATA_DIR:-$APP_DIR/data}"

mkdir -p "$DASTX_DATA_DIR"

printf '\nDAST-X starting...\n'
printf 'APP_DIR        : %s\n' "$APP_DIR"
printf 'DASTX_REPO_ROOT: %s\n' "$DASTX_REPO_ROOT"
printf 'DASTX_DATA_DIR : %s\n' "$DASTX_DATA_DIR"
printf 'URL            : http://%s:%s/\n\n' "$DASTX_HOST" "$DASTX_PORT"

python dast_x_app.py
