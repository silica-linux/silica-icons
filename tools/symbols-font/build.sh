#!/bin/sh
# One command: create the venv if needed, build the fonts, then verify them.
#   tools/symbols-font/build.sh            build fonts/ (and the variable font when possible)
#   tools/symbols-font/build.sh --verify OUTDIR   also render the comparison against the SVGs
set -eu
here=$(cd "$(dirname "$0")" && pwd)
if [ ! -x "$here/.venv/bin/python" ]; then
  python3.12 -m venv "$here/.venv" 2>/dev/null || python3 -m venv "$here/.venv"
  "$here/.venv/bin/pip" install -q -r "$here/requirements.txt"
fi
"$here/.venv/bin/python" "$here/build.py"
if [ "${1:-}" = "--verify" ]; then
  "$here/.venv/bin/python" "$here/verify.py" "${2:?output directory}"
fi
