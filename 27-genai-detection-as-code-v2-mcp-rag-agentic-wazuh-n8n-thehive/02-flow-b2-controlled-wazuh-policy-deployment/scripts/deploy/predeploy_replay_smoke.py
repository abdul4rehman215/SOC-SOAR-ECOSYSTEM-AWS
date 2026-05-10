#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {'cmd': cmd, 'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='/opt/detection-ci/wazuh-genai-ci')
    args = ap.parse_args()
    root = Path(args.repo_root)
    replay = root / 'scripts' / 'ci' / 'run_v2_replay_harness.py'
    if not replay.exists():
        print(json.dumps({'status': 'fail', 'error': f'missing {replay}'}, indent=2))
        return 2
    r = run(['python3', str(replay), '--repo-root', str(root)], root)
    print(json.dumps({'status': 'pass' if r['returncode'] == 0 else 'fail', 'result': r}, indent=2))
    return r['returncode']
if __name__ == '__main__':
    raise SystemExit(main())
