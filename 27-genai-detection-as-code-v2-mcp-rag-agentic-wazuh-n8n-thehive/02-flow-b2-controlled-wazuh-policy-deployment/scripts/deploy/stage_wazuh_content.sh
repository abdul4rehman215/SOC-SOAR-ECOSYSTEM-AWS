#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="${1:-/opt/detection-ci/wazuh-genai-ci}"
STAGING_DIR="${2:-/tmp/flow-b2-staging/manual}/wazuh"
mkdir -p "$STAGING_DIR/rules" "$STAGING_DIR/decoders"
for f in genai_mcp_rules.xml genai_rag_memory_rules.xml genai_agentic_rules.xml; do
  cp -a "$REPO_ROOT/detections/wazuh/rules/$f" "$STAGING_DIR/rules/$f"
done
for f in genai_mcp_decoder.xml genai_rag_memory_decoder.xml genai_agentic_decoder.xml; do
  cp -a "$REPO_ROOT/detections/wazuh/decoders/$f" "$STAGING_DIR/decoders/$f"
done
echo "$STAGING_DIR"
