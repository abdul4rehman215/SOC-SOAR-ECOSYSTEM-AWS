#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="${1:-/opt/detection-ci/wazuh-genai-ci}"
STAGING_DIR="${2:-/tmp/flow-b2-staging/manual}/policies"
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"
for d in mcp rag_memory agentic; do
  cp -a "$REPO_ROOT/policies/$d" "$STAGING_DIR/$d"
done
if [ -d "$REPO_ROOT/mappings" ]; then
  mkdir -p "$(dirname "$STAGING_DIR")/mappings"
  cp -a "$REPO_ROOT/mappings/." "$(dirname "$STAGING_DIR")/mappings/"
fi
echo "$STAGING_DIR"
