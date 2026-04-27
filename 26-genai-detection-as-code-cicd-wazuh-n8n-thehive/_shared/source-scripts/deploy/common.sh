#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env.ci"

if [ -f "$ENV_FILE" ]; then
  set -a
  . "$ENV_FILE"
  set +a
fi

FLOWB_TMP_DIR="${FLOWB_TMP_DIR:-/tmp/flowb}"
FLOWB_REPO_DIR="${FLOWB_REPO_DIR:-$FLOWB_TMP_DIR/repo}"
FLOWB_MANIFEST_PATH="${FLOWB_MANIFEST_PATH:-$FLOWB_TMP_DIR/deploy_manifest.json}"
FLOWB_BACKUP_FILE="${FLOWB_BACKUP_FILE:-$FLOWB_TMP_DIR/last_backup_path.txt}"

mkdir -p "$FLOWB_TMP_DIR"

require_cmd() {
  local cmd
  for cmd in "$@"; do
    command -v "$cmd" >/dev/null 2>&1 || {
      echo "missing command: $cmd" >&2
      exit 1
    }
  done
}

require_env() {
  local var
  for var in "$@"; do
    [ -n "${!var:-}" ] || {
      echo "missing env: $var" >&2
      exit 1
    }
  done
}

ssh_cmd() {
  require_env DEPLOY_WAZUH_HOST DEPLOY_WAZUH_USER DEPLOY_SSH_KEY
  ssh -i "$DEPLOY_SSH_KEY" \
      -p "${DEPLOY_WAZUH_PORT:-22}" \
      -o StrictHostKeyChecking=accept-new \
      "$DEPLOY_WAZUH_USER@$DEPLOY_WAZUH_HOST" \
      "$@"
}

scp_to() {
  local src="$1"
  local dst="$2"
  require_env DEPLOY_WAZUH_HOST DEPLOY_WAZUH_USER DEPLOY_SSH_KEY
  scp -i "$DEPLOY_SSH_KEY" \
      -P "${DEPLOY_WAZUH_PORT:-22}" \
      -o StrictHostKeyChecking=accept-new \
      "$src" \
      "$DEPLOY_WAZUH_USER@$DEPLOY_WAZUH_HOST:$dst"
}

json_out() {
  local stage="$1"
  local status="$2"
  local payload="${3:-}"

  python3 - "$stage" "$status" "$payload" <<'PY'
import json, sys
stage, status, payload = sys.argv[1], sys.argv[2], sys.argv[3]
data = {"stage": stage, "status": status}
payload = (payload or "").strip()
if payload:
    try:
        extra = json.loads(payload)
        if isinstance(extra, dict):
            data.update(extra)
        else:
            data["payload"] = extra
    except Exception:
        data["detail"] = payload
print(json.dumps(data))
PY
}
