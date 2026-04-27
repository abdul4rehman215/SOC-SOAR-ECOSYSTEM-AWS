#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "$0")/common.sh"

require_cmd ssh scp python3
require_env DEPLOY_WAZUH_STAGE_DIR

if [ ! -f "$FLOWB_MANIFEST_PATH" ]; then
  json_out "stage_new_content" "fail" "$(python3 - "$FLOWB_MANIFEST_PATH" <<'PY'
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
  json_out "stage_new_content" "skip" '{"notes":["no Wazuh XML files changed in this approved commit"]}'
  exit 0
fi

set +e
stderr="$(
  {
    ssh_cmd "rm -rf '$DEPLOY_WAZUH_STAGE_DIR' && mkdir -p '$DEPLOY_WAZUH_STAGE_DIR/rules' '$DEPLOY_WAZUH_STAGE_DIR/decoders'"

    python3 - "$FLOWB_MANIFEST_PATH" <<'PY' | while IFS=$'\t' read -r kind rel subpath; do
import json, sys
m = json.load(open(sys.argv[1], "r", encoding="utf-8"))
for rel in m.get("wazuh_rules", []):
    print("rules\t%s\t%s" % (rel, rel.split("detections/wazuh/rules/", 1)[1]))
for rel in m.get("wazuh_decoders", []):
    print("decoders\t%s\t%s" % (rel, rel.split("detections/wazuh/decoders/", 1)[1]))
PY
      local_path="$FLOWB_REPO_DIR/$rel"
      remote_path="${DEPLOY_WAZUH_STAGE_DIR%/}/$kind/$subpath"
      remote_dir="$(dirname "$remote_path")"
      ssh_cmd "mkdir -p '$remote_dir'"
      scp_to "$local_path" "$remote_path"
    done
  } 2>&1
)"
rc=$?
set -e

if [ $rc -ne 0 ]; then
  json_out "stage_new_content" "fail" "$(python3 - "$stderr" <<'PY'
import json, sys
print(json.dumps({"error": sys.argv[1]}))
PY
)"
  exit 1
fi

json_out "stage_new_content" "pass" "$(python3 - "$FLOWB_MANIFEST_PATH" "$DEPLOY_WAZUH_STAGE_DIR" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], "r", encoding="utf-8"))
print(json.dumps({
    "stage_dir": sys.argv[2],
    "staged_rules": len(m.get("wazuh_rules", [])),
    "staged_decoders": len(m.get("wazuh_decoders", []))
}))
PY
)"
