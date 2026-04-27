#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "$0")/common.sh"

require_cmd ssh scp grep python3

if [ ! -f "$FLOWB_MANIFEST_PATH" ]; then
  json_out "predeploy_smoke_logtest" "fail" "$(python3 - "$FLOWB_MANIFEST_PATH" <<'PY'
import json, sys
print(json.dumps({"error": f"manifest not found: {sys.argv[1]}"}))
PY
)"
  exit 1
fi

deployable_count="$(python3 - "$FLOWB_MANIFEST_PATH" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], "r", encoding="utf-8"))
print(m.get("deployable_count", 0))
PY
)"

if [ "$deployable_count" = "0" ]; then
  json_out "predeploy_smoke_logtest" "skip" '{"notes":["no deployable XML files in manifest"]}'
  exit 0
fi

set +e
tool_check="$(ssh_cmd "/var/ossec/bin/wazuh-logtest -V >/dev/null" 2>&1)"
rc=$?
set -e

if [ $rc -ne 0 ]; then
  json_out "predeploy_smoke_logtest" "fail" "$(python3 - "$tool_check" <<'PY'
import json, sys
print(json.dumps({"error": sys.argv[1]}))
PY
)"
  exit 1
fi

corpus_file="$FLOWB_REPO_DIR/tests/smoke/predeploy.log"

if [ ! -f "$corpus_file" ]; then
  json_out "predeploy_smoke_logtest" "pass" '{"checked_lines":0,"notes":["wazuh-logtest is present; no tests/smoke/predeploy.log file was found, so only tool-availability smoke was run"]}'
  exit 0
fi

first_line_file="$FLOWB_TMP_DIR/predeploy_first_line.txt"
grep -m1 -ve '^[[:space:]]*$' "$corpus_file" > "$first_line_file" || true

if [ ! -s "$first_line_file" ]; then
  json_out "predeploy_smoke_logtest" "pass" '{"checked_lines":0,"notes":["tests/smoke/predeploy.log exists but has no non-empty lines"]}'
  exit 0
fi

scp_to "$first_line_file" "${DEPLOY_WAZUH_STAGE_DIR%/}/predeploy_first_line.txt"

set +e
stderr="$(ssh_cmd "cat '${DEPLOY_WAZUH_STAGE_DIR%/}/predeploy_first_line.txt' | /var/ossec/bin/wazuh-logtest -q >/dev/null" 2>&1)"
rc=$?
set -e

if [ $rc -ne 0 ]; then
  json_out "predeploy_smoke_logtest" "fail" "$(python3 - "$stderr" <<'PY'
import json, sys
print(json.dumps({"error": sys.argv[1]}))
PY
)"
  exit 1
fi

json_out "predeploy_smoke_logtest" "pass" '{"checked_lines":1,"notes":["single-line predeploy smoke executed with wazuh-logtest"]}'
