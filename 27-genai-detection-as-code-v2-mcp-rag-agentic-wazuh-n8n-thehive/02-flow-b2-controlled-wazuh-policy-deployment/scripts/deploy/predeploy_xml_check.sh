#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-/tmp/flow-b2-staging/manual/wazuh}"
python3 - <<'PY' "$TARGET"
import sys, pathlib, xml.etree.ElementTree as ET
base = pathlib.Path(sys.argv[1])
files = list(base.rglob('*.xml'))
if not files:
    print('no XML files found', file=sys.stderr)
    raise SystemExit(2)
for f in files:
    ET.parse(f)
    print(f'OK XML {f}')
PY
