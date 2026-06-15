#!/usr/bin/env bash
set -euo pipefail

# Python / Node bootstrap
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
npm install -g pnpm

BASHRC="${HOME}/.bashrc"

after_line() {
  local line="$1"
  grep -qxF "$line" "$BASHRC" || echo "$line" >> "$BASHRC"
}

# Persistent command history for Dev Containers.
# Some Codespaces sessions mount /commandhistory as a root-owned volume.
# If it is not writable, fall back to a user-owned history file.
HISTORY_FILE="/commandhistory/.bash_history"
if mkdir -p /commandhistory 2>/dev/null && touch "$HISTORY_FILE" 2>/dev/null; then
  :
else
  HISTORY_FILE="${HOME}/.w3_bash_history"
  touch "$HISTORY_FILE"
fi

after_line "export HISTFILE=${HISTORY_FILE}"
after_line 'export HISTSIZE=10000'
after_line 'export HISTFILESIZE=20000'
after_line 'export PROMPT_COMMAND="history -a; history -c; history -r; ${PROMPT_COMMAND:-}"'

# W3 helper aliases.
after_line 'alias w3api="python tools/w3api.py"'
after_line 'alias w3server="uvicorn w3_api.main:app --host 127.0.0.1 --port 8000"'
after_line 'alias w3test-api="python -m pytest tests/test_w3_api_gateway.py tests/test_w3_api_cross_plan.py -q"'
after_line 'alias w3test-croll="python -m unittest discover -s croll -p \"test_*.py\" -v"'

cat <<EOF

W3 devcontainer ready.

History file:
  ${HISTORY_FILE}

Useful commands after terminal reload:
  w3server
  w3api health
  w3api review W3 system
  w3test-api
  w3test-croll

EOF
