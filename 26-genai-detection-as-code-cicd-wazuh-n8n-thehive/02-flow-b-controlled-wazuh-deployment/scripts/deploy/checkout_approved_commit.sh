#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "$0")/common.sh"

require_cmd git python3

head_sha="${1:-}"
base_sha="${2:-}"

if [ -z "$head_sha" ]; then
  json_out "checkout_approved_commit" "fail" '{"error":"missing head_sha argument"}'
  exit 1
fi

rm -rf "$FLOWB_REPO_DIR"
mkdir -p "$FLOWB_TMP_DIR"

clone_src="$(git -C "$ROOT_DIR" config --get remote.origin.url 2>/dev/null || true)"
if [ -z "$clone_src" ]; then
  clone_src="$ROOT_DIR"
fi

set +e
stderr="$(
  {
    git clone "$clone_src" "$FLOWB_REPO_DIR" >/dev/null 2>&1
    git config --global --add safe.directory "$FLOWB_REPO_DIR" >/dev/null 2>&1 || true
    git -C "$FLOWB_REPO_DIR" fetch --all --tags >/dev/null 2>&1 || true
    git -C "$FLOWB_REPO_DIR" checkout -f "$head_sha" >/dev/null 2>&1
    if [ -z "$base_sha" ]; then
      base_sha="$(git -C "$FLOWB_REPO_DIR" rev-parse HEAD~1)"
    fi
    git -C "$FLOWB_REPO_DIR" diff --name-only "$base_sha..$head_sha" > "$FLOWB_TMP_DIR/changed_files.txt"
  } 2>&1
)"
rc=$?
set -e

if [ $rc -ne 0 ]; then
  json_out "checkout_approved_commit" "fail" "$(python3 - "$stderr" <<'PY'
import json, sys
print(json.dumps({"error": sys.argv[1]}))
PY
)"
  exit 1
fi

python3 - "$FLOWB_TMP_DIR/changed_files.txt" "$FLOWB_MANIFEST_PATH" "$base_sha" "$head_sha" <<'PY'
import json, sys
from pathlib import Path

changed_file, manifest_file, base_sha, head_sha = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
paths = [line.strip() for line in Path(changed_file).read_text(encoding="utf-8").splitlines() if line.strip()]

def xml_under(prefix):
    return lambda p: p.startswith(prefix) and p.endswith(".xml")

def yaml_under(prefix):
    return lambda p: p.startswith(prefix) and (p.endswith(".yml") or p.endswith(".yaml"))

def starts(prefix):
    return lambda p: p.startswith(prefix)

manifest = {
    "base_sha": base_sha,
    "head_sha": head_sha,
    "all_files": paths,
    "wazuh_rules": [p for p in paths if xml_under("detections/wazuh/rules/")(p)],
    "wazuh_decoders": [p for p in paths if xml_under("detections/wazuh/decoders/")(p)],
    "sigma_rules": [p for p in paths if yaml_under("detections/sigma/")(p)],
    "positive_tests": [p for p in paths if starts("tests/events/positive/")(p)],
    "negative_tests": [p for p in paths if starts("tests/events/negative/")(p)],
    "expected_outputs": [p for p in paths if starts("tests/expected/")(p)],
    "metadata_files": [p for p in paths if yaml_under("metadata/")(p)],
    "mapping_files": [p for p in paths if starts("mappings/")(p)],
    "schema_files": [p for p in paths if starts("schemas/")(p)],
}
manifest["deployable_count"] = len(manifest["wazuh_rules"]) + len(manifest["wazuh_decoders"])

Path(manifest_file).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps({
    "stage": "checkout_approved_commit",
    "status": "pass",
    "base_sha": base_sha,
    "head_sha": head_sha,
    "manifest_path": manifest_file,
    "deployable_count": manifest["deployable_count"],
    "wazuh_rules": manifest["wazuh_rules"],
    "wazuh_decoders": manifest["wazuh_decoders"]
}))
PY
