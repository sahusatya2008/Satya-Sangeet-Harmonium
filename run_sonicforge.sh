#!/bin/zsh
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if [[ -x "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3" ]]; then
  PYTHON_BIN="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
elif [[ -x "/opt/homebrew/bin/python3.14" ]]; then
  PYTHON_BIN="/opt/homebrew/bin/python3.14"
elif [[ -x "/usr/local/bin/python3" ]]; then
  PYTHON_BIN="/usr/local/bin/python3"
else
  PYTHON_BIN="$(command -v python3)"
fi

if [[ "$#" -eq 0 ]]; then
  exec "$PYTHON_BIN" "$SCRIPT_DIR/run_sonicforge.py" --mode web
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/run_sonicforge.py" "$@"
