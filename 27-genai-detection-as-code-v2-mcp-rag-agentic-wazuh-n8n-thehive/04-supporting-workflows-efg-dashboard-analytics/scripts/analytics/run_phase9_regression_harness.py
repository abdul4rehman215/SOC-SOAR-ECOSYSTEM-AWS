#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from phase9_common import utcnow, stable_id, write_json, parse_expected_rule_from_event, load_simple_yml_mapping, family_for_rule

def count_alerts(alerts_path: Path) -> int:
    if not alerts_path.exists(): return 0
    try:
        return sum(1 for _ in alerts_path.open(encoding='utf-8', errors='ignore'))
    except Exception:
        return 0

def collect_tests(repo: Path):
    roots = [repo/'tests/events/mcp', repo/'tests/events/rag_memory', repo/'tests/events/agentic']
    files = []
    for root in roots:
        if root.exists():
            files.extend(sorted(root.rglob('*.json')))
    return files

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--trigger-type', default='manual')
    ap.add_argument('--alerts-json', default='/var/ossec/logs/alerts/alerts.json')
    ap.add_argument('--output-json', required=True)
    ap.add_argument('--execute-existing-harness', action='store_true', help='Also call scripts/ci/run_v2_replay_harness.py if present')
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    started = utcnow()
    before = count_alerts(Path(args.alerts_json))
    expected_maps = {}
    for p in [repo/'tests/expected/mcp_expected_rules.yml', repo/'tests/expected/rag_memory_expected_rules.yml', repo/'tests/expected/agentic_expected_rules.yml', repo/'tests/expected/v2_expected_rules.yml']:
        expected_maps.update(load_simple_yml_mapping(p))
    test_files = collect_tests(repo)
    results = []
    misses = 0
    unexpected = 0
    for f in test_files:
        rid = parse_expected_rule_from_event(f)
        expected_from_map = None
        stem = f.stem
        for key, val in expected_maps.items():
            if key == stem or key == f.name or key in str(f): expected_from_map = val; break
        ok = True
        notes = []
        if rid is None:
            ok = False; misses += 1; notes.append('missing expected_wazuh_rule_id in event')
        if expected_from_map is not None and rid is not None and expected_from_map != rid:
            ok = False; misses += 1; notes.append(f'expected map mismatch: map={expected_from_map} event={rid}')
        results.append({'test_file': str(f.relative_to(repo)), 'expected_rule_id': rid or 0, 'expected_map_rule_id': expected_from_map or 0, 'family': family_for_rule(rid or 0), 'passed': ok, 'notes': '; '.join(notes)})
    harness_result = None
    if args.execute_existing_harness and (repo/'scripts/ci/run_v2_replay_harness.py').exists():
        try:
            cp = subprocess.run(['python3', str(repo/'scripts/ci/run_v2_replay_harness.py'), '--repo-root', str(repo)], capture_output=True, text=True, timeout=120)
            harness_result = {'returncode': cp.returncode, 'stdout': cp.stdout[-4000:], 'stderr': cp.stderr[-4000:]}
            if cp.returncode != 0: unexpected += 1
        except Exception as e:
            harness_result = {'error': str(e)}; unexpected += 1
    after = count_alerts(Path(args.alerts_json))
    completed = utcnow()
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    failed = total - passed
    status = 'pass' if failed == 0 and unexpected == 0 and total > 0 else 'fail'
    commit = ''
    try:
        commit = subprocess.check_output(['git','-C',str(repo),'rev-parse','--short','HEAD'], text=True).strip()
    except Exception:
        commit = 'unknown'
    run_id = stable_id('regression', commit, started)
    run_row = {'regression_run_id': run_id, 'started_at': started, 'completed_at': completed, 'trigger_type': args.trigger_type, 'repo': str(repo), 'commit_sha': commit, 'corpus_version': 'v2-phase9-regression-v1', 'total_tests': total, 'passed_tests': passed, 'failed_tests': failed, 'expected_rule_misses': misses, 'unexpected_alerts': unexpected, 'alert_volume_before': before, 'alert_volume_after': after, 'regression_status': status, 'github_issue_url': '', 'slack_notified': False, 'notes': f'{passed}/{total} tests passed', 'raw_result_json': ''}
    result = {'flow': 'Flow F - Red-Team Replay and Regression Harness', 'decision': status, 'regression_run_row': run_row, 'test_results': results, 'harness_result': harness_result, 'slack_text': f'Flow F regression {status.upper()}: {passed}/{total} passed, misses={misses}, unexpected={unexpected}, alert_volume_before={before}, after={after}', 'github_issue_needed': status != 'pass'}
    run_row['raw_result_json'] = json.dumps({k:v for k,v in result.items() if k != 'regression_run_row'}, sort_keys=True)[:9000]
    write_json(Path(args.output_json), result)
    print(json.dumps(result, indent=2))
if __name__ == '__main__': main()
