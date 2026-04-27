#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "$0")/common.sh"

require_cmd ssh python3
require_env DEPLOY_WAZUH_STAGE_DIR DEPLOY_WAZUH_RULES_DIR DEPLOY_WAZUH_DECODERS_DIR

if [ ! -f "$FLOWB_MANIFEST_PATH" ]; then
  json_out "activate_content" "fail" "$(python3 - "$FLOWB_MANIFEST_PATH" <<'PY'
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
  json_out "activate_content" "skip" '{"notes":["no deployable XML files in manifest"]}'
  exit 0
fi

remote_script="$(mktemp)"
cat > "$remote_script" <<'RSCRIPT'
set -euo pipefail

stage="__STAGE__"
rules_dir="__RULES__"
decoders_dir="__DECODERS__"

if [ -d "$stage/rules" ]; then
  cd "$stage/rules"
  find . -type f -name '*.xml' | while IFS= read -r f; do
    rel="${f#./}"
    install -D -o wazuh -g wazuh -m 660 "$stage/rules/$rel" "$rules_dir/$rel"
  done
fi

if [ -d "$stage/decoders" ]; then
  cd "$stage/decoders"
  find . -type f -name '*.xml' | while IFS= read -r f; do
    rel="${f#./}"
    install -D -o wazuh -g wazuh -m 660 "$stage/decoders/$rel" "$decoders_dir/$rel"
  done
fi
RSCRIPT

python3 - "$remote_script" "$DEPLOY_WAZUH_STAGE_DIR" "$DEPLOY_WAZUH_RULES_DIR" "$DEPLOY_WAZUH_DECODERS_DIR" <<'PY'
from pathlib import Path
import sys

p = Path(sys.argv[1])
text = p.read_text(encoding="utf-8")
text = text.replace("__STAGE__", sys.argv[2].rstrip("/"))
text = text.replace("__RULES__", sys.argv[3].rstrip("/"))
text = text.replace("__DECODERS__", sys.argv[4].rstrip("/"))
p.write_text(text, encoding="utf-8")
PY

set +e
stderr="$(
  ssh -i "$DEPLOY_SSH_KEY" \
      -p "${DEPLOY_WAZUH_PORT:-22}" \
      -o StrictHostKeyChecking=accept-new \
      "$DEPLOY_WAZUH_USER@$DEPLOY_WAZUH_HOST" \
      'bash -s' < "$remote_script" 2>&1
)"
rc=$?
set -e

rm -f "$remote_script"

if [ $rc -ne 0 ]; then
  json_out "activate_content" "fail" "$(python3 - "$stderr" <<'PY'
import json, sys
print(json.dumps({"error": sys.argv[1]}))
PY
)"
  exit 1
fi

json_out "activate_content" "pass" '{"notes":["staged rules and decoders copied into live Wazuh custom content directories"]}'
