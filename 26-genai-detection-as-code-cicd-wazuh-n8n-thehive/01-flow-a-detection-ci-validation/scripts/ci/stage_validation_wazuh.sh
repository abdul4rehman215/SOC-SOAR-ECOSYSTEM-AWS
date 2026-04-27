#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo '{"stage":"stage_validation_content","status":"fail","error":"Usage: stage_validation_wazuh.sh <changed_files.json>"}'
  exit 1
fi

MANIFEST="$1"
REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
MODE="${VALIDATION_WAZUH_MODE:-remote_ssh}"
RULES_DIR="${VALIDATION_WAZUH_RULES_DIR:-/var/ossec/etc/rules}"
DECODERS_DIR="${VALIDATION_WAZUH_DECODERS_DIR:-/var/ossec/etc/decoders}"
STAGING_DIR="${VALIDATION_WAZUH_STAGING_DIR:-/var/ossec/tmp/detection-ci}"
RESTART_CMD="${VALIDATION_WAZUH_RESTART_CMD:-systemctl restart wazuh-manager}"
SSH_USER="${VALIDATION_WAZUH_USER:-root}"
SSH_HOST="${VALIDATION_WAZUH_HOST:-}"
SSH_PORT="${VALIDATION_WAZUH_PORT:-22}"
SSH_KEY="${VALIDATION_SSH_KEY:-}"

if [[ ! -f "$MANIFEST" ]]; then
  echo '{"stage":"stage_validation_content","status":"fail","error":"Manifest file not found"}'
  exit 1
fi

mapfile -t FILES < <(python3 - <<'PY' "$MANIFEST"
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
for key in ('wazuh_rules', 'wazuh_decoders'):
    for item in data.get(key, []):
        print(item)
PY
)

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo '{"stage":"stage_validation_content","status":"skip","checked":0,"notes":["No Wazuh rules or decoders changed"]}'
  exit 0
fi

if [[ "$MODE" == "remote_ssh" && -z "$SSH_HOST" ]]; then
  echo '{"stage":"stage_validation_content","status":"fail","error":"VALIDATION_WAZUH_HOST is required for remote_ssh mode"}'
  exit 1
fi

SSH_ARGS=(-p "$SSH_PORT" -o StrictHostKeyChecking=no)
SCP_ARGS=(-P "$SSH_PORT" -o StrictHostKeyChecking=no)
if [[ -n "$SSH_KEY" ]]; then
  SSH_ARGS+=(-i "$SSH_KEY")
  SCP_ARGS+=(-i "$SSH_KEY")
fi

copied=()
backups=()

stage_remote() {
  ssh "${SSH_ARGS[@]}" "${SSH_USER}@${SSH_HOST}" "mkdir -p '$STAGING_DIR/rules' '$STAGING_DIR/decoders' '$STAGING_DIR/backup/rules' '$STAGING_DIR/backup/decoders'"

  for rel in "${FILES[@]}"; do
    src="$REPO_ROOT/$rel"
    if [[ ! -f "$src" ]]; then
      echo "{\"stage\":\"stage_validation_content\",\"status\":\"fail\",\"error\":\"File not found: $rel\"}"
      exit 1
    fi
    base="$(basename "$rel")"
    if [[ "$rel" == detections/wazuh/rules/* ]]; then
      remote_stage="$STAGING_DIR/rules/$base"
      remote_live="$RULES_DIR/$base"
      remote_backup="$STAGING_DIR/backup/rules/$base"
    else
      remote_stage="$STAGING_DIR/decoders/$base"
      remote_live="$DECODERS_DIR/$base"
      remote_backup="$STAGING_DIR/backup/decoders/$base"
    fi
    scp "${SCP_ARGS[@]}" "$src" "${SSH_USER}@${SSH_HOST}:$remote_stage"
    ssh "${SSH_ARGS[@]}" "${SSH_USER}@${SSH_HOST}" "if [[ -f '$remote_live' ]]; then cp '$remote_live' '$remote_backup'; fi; cp '$remote_stage' '$remote_live'"
    copied+=("$rel")
    backups+=("$remote_backup")
  done

  ssh "${SSH_ARGS[@]}" "${SSH_USER}@${SSH_HOST}" "$RESTART_CMD"
}

stage_local() {
  mkdir -p "$STAGING_DIR/rules" "$STAGING_DIR/decoders" "$STAGING_DIR/backup/rules" "$STAGING_DIR/backup/decoders"
  for rel in "${FILES[@]}"; do
    src="$REPO_ROOT/$rel"
    if [[ ! -f "$src" ]]; then
      echo "{\"stage\":\"stage_validation_content\",\"status\":\"fail\",\"error\":\"File not found: $rel\"}"
      exit 1
    fi
    base="$(basename "$rel")"
    if [[ "$rel" == detections/wazuh/rules/* ]]; then
      live="$RULES_DIR/$base"
      backup="$STAGING_DIR/backup/rules/$base"
      cp "$src" "$STAGING_DIR/rules/$base"
    else
      live="$DECODERS_DIR/$base"
      backup="$STAGING_DIR/backup/decoders/$base"
      cp "$src" "$STAGING_DIR/decoders/$base"
    fi
    [[ -f "$live" ]] && cp "$live" "$backup" || true
    cp "$src" "$live"
    copied+=("$rel")
    backups+=("$backup")
  done
  eval "$RESTART_CMD"
}

if [[ "$MODE" == "local" ]]; then
  stage_local
else
  stage_remote
fi

python3 - <<'PY' "${#FILES[@]}" "$MODE" "${copied[*]}"
import json, sys
checked = int(sys.argv[1])
mode = sys.argv[2]
copied = [x for x in sys.argv[3].split() if x]
print(json.dumps({
    "stage": "stage_validation_content",
    "status": "pass",
    "mode": mode,
    "checked": checked,
    "copied_files": copied,
    "notes": ["Validation Wazuh content staged and manager restart command executed"]
}))
PY
