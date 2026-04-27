#!/usr/bin/env python3
import base64
import json
import os
import shlex
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

stage = "postdeploy_test"

manifest_path = Path(os.environ.get("FLOWB_MANIFEST_PATH", "/tmp/flowb/deploy_manifest.json"))
if not manifest_path.exists():
    print(json.dumps({"stage": stage, "status": "fail", "error": f"manifest not found: {manifest_path}"}))
    sys.exit(1)

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
deployable = list(manifest.get("wazuh_rules", [])) + list(manifest.get("wazuh_decoders", []))

if not deployable:
    print(json.dumps({"stage": stage, "status": "skip", "notes": ["no deployable Wazuh XML files in manifest"]}))
    sys.exit(0)

api_url = os.environ["DEPLOY_API_URL"].rstrip("/")
api_user = os.environ["DEPLOY_API_USERNAME"]
api_password = os.environ["DEPLOY_API_PASSWORD"]
verify_tls = os.environ.get("DEPLOY_API_VERIFY_TLS", "false").lower() == "true"

ctx = None if verify_tls else ssl._create_unverified_context()

def open_url(req):
    if ctx is None:
        return urllib.request.urlopen(req, timeout=30)
    return urllib.request.urlopen(req, context=ctx, timeout=30)

try:
    basic = base64.b64encode(f"{api_user}:{api_password}".encode()).decode()
    auth_req = urllib.request.Request(
        f"{api_url}/security/user/authenticate?raw=true",
        method="POST",
        headers={"Authorization": f"Basic {basic}"}
    )
    with open_url(auth_req) as resp:
        token = resp.read().decode().strip()

    root_req = urllib.request.Request(
        f"{api_url}/",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    )
    with open_url(root_req) as resp:
        root_data = json.loads(resp.read().decode())

    remote_host = os.environ["DEPLOY_WAZUH_HOST"]
    remote_user = os.environ["DEPLOY_WAZUH_USER"]
    ssh_key = os.environ["DEPLOY_SSH_KEY"]
    remote_port = str(os.environ.get("DEPLOY_WAZUH_PORT", "22"))
    rules_dir = os.environ["DEPLOY_WAZUH_RULES_DIR"].rstrip("/")
    decoders_dir = os.environ["DEPLOY_WAZUH_DECODERS_DIR"].rstrip("/")

    expected_targets = []
    for rel in manifest.get("wazuh_rules", []):
        sub = rel.split("detections/wazuh/rules/", 1)[1]
        expected_targets.append(f"{rules_dir}/{sub}")
    for rel in manifest.get("wazuh_decoders", []):
        sub = rel.split("detections/wazuh/decoders/", 1)[1]
        expected_targets.append(f"{decoders_dir}/{sub}")

    missing = []
    for target in expected_targets:
        cmd = [
            "ssh",
            "-i", ssh_key,
            "-p", remote_port,
            "-o", "StrictHostKeyChecking=accept-new",
            f"{remote_user}@{remote_host}",
            f"test -f {shlex.quote(target)}"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            missing.append(target)

    if missing:
        print(json.dumps({
            "stage": stage,
            "status": "fail",
            "api_title": root_data.get("data", {}).get("title", ""),
            "api_version": root_data.get("data", {}).get("api_version", ""),
            "verified_files": len(expected_targets) - len(missing),
            "missing_files": missing
        }))
        sys.exit(1)

    print(json.dumps({
        "stage": stage,
        "status": "pass",
        "api_title": root_data.get("data", {}).get("title", ""),
        "api_version": root_data.get("data", {}).get("api_version", ""),
        "verified_files": len(expected_targets),
        "missing_files": []
    }))
except urllib.error.HTTPError as e:
    print(json.dumps({
        "stage": stage,
        "status": "fail",
        "error": f"HTTP {e.code}",
        "detail": e.read().decode(errors="replace")
    }))
    sys.exit(1)
except Exception as e:
    print(json.dumps({
        "stage": stage,
        "status": "fail",
        "error": str(e)
    }))
    sys.exit(1)
