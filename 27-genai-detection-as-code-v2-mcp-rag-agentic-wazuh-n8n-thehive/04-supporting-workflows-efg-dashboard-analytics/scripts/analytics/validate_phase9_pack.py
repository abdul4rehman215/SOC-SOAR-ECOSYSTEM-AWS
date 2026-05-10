#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, py_compile, subprocess
from pathlib import Path
from phase9_common import write_json

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--repo-root', default='.'); ap.add_argument('--output-json', default='')
    args = ap.parse_args(); repo = Path(args.repo_root).resolve()
    failures=[]; checked=[]
    required = [
      'scripts/analytics/run_phase9_mcp_policy_monitor_local.py','scripts/analytics/run_phase9_regression_harness.py','scripts/analytics/run_phase9_false_positive_analytics.py','scripts/analytics/run_phase9_dashboard_rollups.py',
      'n8n-workflows/Flow_E_MCP_Runtime_Policy_Monitor_IMPORT_SAFE.json','n8n-workflows/Flow_F_RedTeam_Replay_Regression_IMPORT_SAFE.json','n8n-workflows/Flow_G_False_Positive_Analytics_IMPORT_SAFE.json','n8n-workflows/Flow_SOC_Dashboard_V2_Metrics_Rollup_IMPORT_SAFE.json'
    ]
    for rel in required:
        p=repo/rel; checked.append(rel)
        if not p.exists(): failures.append(f'missing {rel}')
    for p in (repo/'scripts/analytics').glob('*.py'):
        try: py_compile.compile(str(p), doraise=True); checked.append(str(p.relative_to(repo)))
        except Exception as e: failures.append(f'python compile failed {p}: {e}')
    for p in (repo/'n8n-workflows').glob('Flow_*IMPORT_SAFE.json'):
        try: json.loads(p.read_text(encoding='utf-8')); checked.append(str(p.relative_to(repo)))
        except Exception as e: failures.append(f'n8n json invalid {p}: {e}')
    outdir = repo/'validation/phase9'
    outdir.mkdir(parents=True, exist_ok=True)
    smoke_cmds = [
      ['python3', str(repo/'scripts/analytics/run_phase9_mcp_policy_monitor_local.py'), '--repo-root', str(repo), '--event-json', str(repo/'tests/fixtures/flow-e-mcp-policy-event-violation.json'), '--output-json', str(outdir/'flowe_violation_result.json')],
      ['python3', str(repo/'scripts/analytics/run_phase9_regression_harness.py'), '--repo-root', str(repo), '--output-json', str(outdir/'flowf_regression_result.json')],
      ['python3', str(repo/'scripts/analytics/run_phase9_false_positive_analytics.py'), '--repo-root', str(repo), '--output-json', str(outdir/'flowg_fp_result.json')],
      ['python3', str(repo/'scripts/analytics/run_phase9_dashboard_rollups.py'), '--repo-root', str(repo), '--regression-json', str(outdir/'flowf_regression_result.json'), '--fp-json', str(outdir/'flowg_fp_result.json'), '--output-json', str(outdir/'dashboard_rollup_result.json')]
    ]
    for cmd in smoke_cmds:
        cp = subprocess.run(cmd, capture_output=True, text=True)
        if cp.returncode != 0: failures.append(f'smoke command failed {cmd}: {cp.stderr[-1000:]}')
    result={'stage':'validate_phase9_pack','status':'fail' if failures else 'pass','checked_count':len(checked),'failures':failures}
    if args.output_json: write_json(Path(args.output_json), result)
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if failures else 0)
if __name__ == '__main__': main()
