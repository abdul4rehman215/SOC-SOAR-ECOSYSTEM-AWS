#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "$0")/common.sh"

require_cmd ssh tar python3
require_env DEPLOY_WAZUH_BACKUP_DIR DEPLOY_WAZUH_RULES_DIR DEPLOY_WAZUH_DECODERS_DIR

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_path="${DEPLOY_WAZUH_BACKUP_DIR%/}/flowb_${timestamp}.tgz"
rules_rel="${DEPLOY_WAZUH_RULES_DIR#/var/ossec/}"
decoders_rel="${DEPLOY_WAZUH_DECODERS_DIR#/var/ossec/}"

set +e
stderr="$(ssh_cmd "mkdir -p '$DEPLOY_WAZUH_BACKUP_DIR' && tar -C /var/ossec -czf '$backup_path' '$rules_rel' '$decoders_rel'" 2>&1)"
rc=$?
set -e

if [ $rc -ne 0 ]; then
  python3 - "$stderr" <<'PY'
import json, sys
print(json.dumps({
    "stage": "backup_current_content",
    "status": "fail",
    "error": sys.argv[1]
}))
PY
  exit 1
fi

printf '%s\n' "$backup_path" > "$FLOWB_BACKUP_FILE"

python3 - "$backup_path" <<'PY'
import json, sys
print(json.dumps({
    "stage": "backup_current_content",
    "status": "pass",
    "backup_path": sys.argv[1]
}))
PY
