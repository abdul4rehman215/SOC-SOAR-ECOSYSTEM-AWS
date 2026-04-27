#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "$0")/common.sh"

require_cmd ssh python3
require_env DEPLOY_WAZUH_RESTART_CMD

if [ ! -f "$FLOWB_BACKUP_FILE" ]; then
  json_out "rollback_from_backup" "fail" "$(python3 - "$FLOWB_BACKUP_FILE" <<'PY'
import json, sys
print(json.dumps({"error": f"backup file not found: {sys.argv[1]}"}))
PY
)"
  exit 1
fi

backup_path="$(cat "$FLOWB_BACKUP_FILE")"

if [ -z "$backup_path" ]; then
  json_out "rollback_from_backup" "fail" '{"error":"backup path file is empty"}'
  exit 1
fi

set +e
stderr="$(ssh_cmd "tar -C /var/ossec -xzf '$backup_path' && $DEPLOY_WAZUH_RESTART_CMD >/dev/null 2>&1 && systemctl is-active wazuh-manager" 2>&1)"
rc=$?
set -e

if [ $rc -ne 0 ]; then
  json_out "rollback_from_backup" "fail" "$(python3 - "$stderr" "$backup_path" <<'PY'
import json, sys
print(json.dumps({"backup_path": sys.argv[2], "error": sys.argv[1]}))
PY
)"
  exit 1
fi

json_out "rollback_from_backup" "pass" "$(python3 - "$backup_path" "$stderr" <<'PY'
import json, sys
print(json.dumps({"backup_path": sys.argv[1], "service_status": sys.argv[2].strip()}))
PY
)"
