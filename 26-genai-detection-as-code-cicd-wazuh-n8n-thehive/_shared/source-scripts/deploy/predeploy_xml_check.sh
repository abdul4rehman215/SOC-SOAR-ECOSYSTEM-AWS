#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "$0")/common.sh"

require_cmd xmllint python3

if [ ! -f "$FLOWB_MANIFEST_PATH" ]; then
  json_out "predeploy_xml_check" "fail" "$(python3 - "$FLOWB_MANIFEST_PATH" <<'PY'
import json, sys
print(json.dumps({"error": f"manifest not found: {sys.argv[1]}"}))
PY
)"
  exit 1
fi

mapfile -t xml_files < <(python3 - "$FLOWB_MANIFEST_PATH" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], "r", encoding="utf-8"))
for rel in m.get("wazuh_rules", []):
    print(rel)
for rel in m.get("wazuh_decoders", []):
    print(rel)
PY
)

if [ "${#xml_files[@]}" -eq 0 ]; then
  json_out "predeploy_xml_check" "skip" '{"notes":["no deployable XML files in manifest"]}'
  exit 0
fi

err_file="$FLOWB_TMP_DIR/predeploy_xml_check.err"
: > "$err_file"
failed_files=()
passed_files=()

for rel in "${xml_files[@]}"; do
  full_path="$FLOWB_REPO_DIR/$rel"
  if xmllint --noout "$full_path" 2>>"$err_file"; then
    passed_files+=("$rel")
  else
    failed_files+=("$rel")
  fi
done

if [ "${#failed_files[@]}" -gt 0 ]; then
  json_out "predeploy_xml_check" "fail" "$(python3 - "$err_file" "${failed_files[@]}" <<'PY'
import json, sys
err = open(sys.argv[1], "r", encoding="utf-8").read()
failed = sys.argv[2:]
print(json.dumps({
    "checked": len(failed),
    "failed_files": failed,
    "error": err
}))
PY
)"
  exit 1
fi

json_out "predeploy_xml_check" "pass" "$(python3 - "${passed_files[@]}" <<'PY'
import json, sys
passed = sys.argv[1:]
print(json.dumps({
    "checked": len(passed),
    "passed_files": passed,
    "engine": "xmllint"
}))
PY
)"
