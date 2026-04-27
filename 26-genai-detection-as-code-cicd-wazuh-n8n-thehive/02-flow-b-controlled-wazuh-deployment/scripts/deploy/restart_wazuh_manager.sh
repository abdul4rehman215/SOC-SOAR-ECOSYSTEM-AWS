#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "$0")/common.sh"

require_cmd ssh python3
require_env DEPLOY_WAZUH_RESTART_CMD

set +e
status_out="$(ssh_cmd "$DEPLOY_WAZUH_RESTART_CMD >/dev/null 2>&1 && systemctl is-active wazuh-manager" 2>&1)"
rc=$?
set -e

if [ $rc -ne 0 ]; then
  json_out "restart_manager" "fail" "$(python3 - "$status_out" <<'PY'
import json, sys
print(json.dumps({"error": sys.argv[1]}))
PY
)"
  exit 1
fi

json_out "restart_manager" "pass" "$(python3 - "$status_out" <<'PY'
import json, sys
print(json.dumps({"service_status": sys.argv[1].strip()}))
PY
)"
