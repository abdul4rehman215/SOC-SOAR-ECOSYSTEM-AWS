#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {'cmd': cmd, 'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='/opt/detection-ci/wazuh-genai-ci')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    root = Path(args.repo_root)
    checks = []
    for p in [
        root / 'detections/wazuh/rules/genai_mcp_rules.xml',
        root / 'detections/wazuh/rules/genai_rag_memory_rules.xml',
        root / 'detections/wazuh/rules/genai_agentic_rules.xml',
        root / 'scripts/runtime/run_mcp_action_scenarios.py',
        root / 'scripts/runtime/run_agentic_scenarios.py',
    ]:
        checks.append({'path': str(p), 'exists': p.exists()})
    wazuh_check = {'skipped': True, 'reason': 'dry-run'} if args.dry_run else run(['sudo', '/var/ossec/bin/wazuh-analysisd', '-t'])
    status = 'pass' if all(c['exists'] for c in checks) and (args.dry_run or wazuh_check.get('returncode') == 0) else 'fail'
    print(json.dumps({'status': status, 'checks': checks, 'wazuh_check': wazuh_check}, indent=2))
    return 0 if status == 'pass' else 2
if __name__ == '__main__':
    raise SystemExit(main())
