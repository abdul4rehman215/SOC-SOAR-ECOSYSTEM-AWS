#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, json, subprocess, sys, time, os
from pathlib import Path

VALIDATORS = [
  ("wazuh_xml", "scripts/ci/validate_wazuh_xml.py"),
  ("sigma", "scripts/ci/validate_sigma.py"),
  ("metadata", "scripts/ci/validate_metadata.py"),
  ("mcp_manifest", "scripts/ci/validate_mcp_manifest.py"),
  ("mcp_policy_bundle", "scripts/ci/validate_mcp_policy_bundle.py"),
  ("tool_schema_hashes", "scripts/ci/validate_tool_schema_hashes.py"),
  ("prompt_policies", "scripts/ci/validate_prompt_policies.py"),
  ("rag_memory_policy", "scripts/ci/validate_rag_memory_policy.py"),
  ("agentic_policy", "scripts/ci/validate_agentic_policy.py"),
  ("case_template_mapping", "scripts/ci/validate_case_template_mapping.py"),
  ("rule_family_map", "scripts/ci/validate_rule_family_map.py"),
  ("datatable_schemas", "scripts/ci/validate_datatable_schemas.py"),
  ("v2_replay_harness", "scripts/ci/run_v2_replay_harness.py"),
]

CI_RELEVANT_CATEGORIES = {
  "wazuh_content", "sigma", "metadata", "schema", "mcp_policy", "rag_memory_policy",
  "agentic_policy", "mapping", "test_corpus", "datatable_schema",
}

METADATA_IMPACTING_CATEGORIES = {"metadata", "mapping", "wazuh_content", "sigma", "schema"}

def parse_changed_files(args):
    if args.changed_files_json:
        try: return json.loads(args.changed_files_json)
        except Exception: return []
    if args.changed_files_b64:
        try: return json.loads(base64.b64decode(args.changed_files_b64).decode("utf-8"))
        except Exception: return []
    return []

def classify(path):
    p = str(path or "").lower()
    if p.endswith(".xml") and "detections/wazuh" in p: return "wazuh_content", "high"
    if "detections/sigma" in p: return "sigma", "medium"
    if p.startswith("metadata/"): return "metadata", "medium"
    if p.startswith("schemas/"): return "schema", "high"
    if p.startswith("policies/mcp") or ("mcp" in p and "policies" in p): return "mcp_policy", "high"
    if p.startswith("policies/rag_memory") or ("rag_memory" in p and "policies" in p): return "rag_memory_policy", "high"
    if p.startswith("policies/agentic") or ("agentic" in p and "policies" in p): return "agentic_policy", "high"
    if p.startswith("mappings/"): return "mapping", "high"
    if p.startswith("tests/"): return "test_corpus", "medium"
    if p.startswith("data-tables/"): return "datatable_schema", "medium"
    if p.startswith("docs/"): return "documentation", "low"
    return "other", "low"

def skipped_stage(name: str, reason: str):
    return {
        "stage_name": name,
        "status": "skip",
        "passed": True,
        "duration_seconds": 0,
        "files_checked": 0,
        "findings_count": 0,
        "summary": f"{name}: skipped - {reason}",
        "details": {"skipped": True, "reason": reason},
    }

def run_validator(repo_root: Path, name: str, script: str):
    start = time.time()
    path = repo_root / script
    if not path.exists():
        return {"stage_name": name, "status": "fail", "passed": False, "duration_seconds": 0, "files_checked": 0, "findings_count": 1, "summary": f"Missing validator {script}", "details": {"missing": script}}
    try:
        proc = subprocess.run([sys.executable, str(path), "--repo-root", str(repo_root)], cwd=str(repo_root), capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired as e:
        duration = round(time.time() - start, 3)
        return {"stage_name": name, "status": "fail", "passed": False, "duration_seconds": duration, "files_checked": 0, "findings_count": 1, "summary": f"{name}: validator timed out after 30 seconds", "details": {"timeout": True, "stdout": (e.stdout or "")[-2000:] if isinstance(e.stdout, str) else "", "stderr": (e.stderr or "")[-2000:] if isinstance(e.stderr, str) else ""}}
    duration = round(time.time() - start, 3)
    details = {"stdout": proc.stdout[-10000:], "stderr": proc.stderr[-4000:], "returncode": proc.returncode}
    parsed = None
    try:
        parsed = json.loads(proc.stdout[proc.stdout.find("{"):]) if "{" in proc.stdout else None
    except Exception:
        parsed = None
    if isinstance(parsed, dict): details["parsed"] = parsed
    failures = parsed.get("failures", []) if isinstance(parsed, dict) else []
    warnings = parsed.get("warnings", []) if isinstance(parsed, dict) else []
    files_checked = parsed.get("files_checked", parsed.get("manifests_checked", len(parsed.get("files_present", [])) if isinstance(parsed, dict) else 0)) if isinstance(parsed, dict) else 0
    status = "pass" if proc.returncode == 0 else "fail"
    return {"stage_name": name, "status": status, "passed": proc.returncode == 0, "duration_seconds": duration, "files_checked": files_checked or 0, "findings_count": len(failures), "warning_count": len(warnings), "summary": f"{name}: {status}", "details": details}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--changed-files-json", default="")
    ap.add_argument("--changed-files-b64", default="")
    ap.add_argument("--output-json", default="")
    ap.add_argument("--pr-number", default="0")
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "local/wazuh-genai-ci"))
    ap.add_argument("--head-sha", default=os.environ.get("GITHUB_SHA", "local"))
    ap.add_argument("--actor", default=os.environ.get("GITHUB_ACTOR", "local"))
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    started = time.time()
    changed = parse_changed_files(args)
    changed_rows = []
    for idx, f in enumerate(changed):
        path = f.get("filename") if isinstance(f, dict) else str(f)
        status = f.get("status", "modified") if isinstance(f, dict) else "modified"
        category, risk = classify(path)
        changed_rows.append({"change_id": f"a2-change-{idx+1}", "file_path": path, "change_status": status, "category": category, "risk_category": risk, "validator_group": category, "requires_review": risk in {"high", "critical"}, "notes": "classified by Flow A2"})

    relevant_categories = {r["category"] for r in changed_rows if r["category"] in CI_RELEVANT_CATEGORIES}
    # If GitHub sends docs-only or non-security-only changes, A2 should skip instead of running full CI.
    if changed_rows and not relevant_categories:
        completed = time.time()
        result = {
            "ci_run_id": f"a2-skip-{int(started)}-{args.pr_number}",
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(completed)),
            "duration_seconds": round(completed-started, 3),
            "repo": args.repo,
            "pr_number": int(args.pr_number or 0),
            "head_sha": args.head_sha,
            "actor": args.actor,
            "changed_files": changed_rows,
            "relevant_change_count": 0,
            "stage_results": [],
            "decision": "skip",
            "status": "skipped",
            "labels": ["ai-security-ci-skip"],
            "summary": "Flow A2 skipped: docs/non-security-only PR change",
        }
        if args.output_json: Path(args.output_json).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
        raise SystemExit(0)

    stages = []
    for name, script in VALIDATORS:
        if name == "metadata" and changed_rows and not (relevant_categories & METADATA_IMPACTING_CATEGORIES):
            stages.append(skipped_stage("metadata", "no metadata/mapping/rule/schema files changed"))
        else:
            stages.append(run_validator(repo_root, name, script))

    failed = [s for s in stages if not s["passed"]]
    labels = []
    labels += ["ai-security-ci-pass" if not failed else "ai-security-ci-fail"]
    labels += ["detection-ci-pass" if all(s["passed"] for s in stages if s["stage_name"] in {"wazuh_xml", "sigma", "metadata", "v2_replay_harness"}) else "detection-ci-fail"]
    labels += ["mcp-policy-pass" if all(s["passed"] for s in stages if s["stage_name"] in {"mcp_manifest", "mcp_policy_bundle", "tool_schema_hashes"}) else "mcp-policy-fail"]
    labels += ["rag-policy-pass" if next((s for s in stages if s["stage_name"] == "rag_memory_policy"), {"passed": False})["passed"] else "rag-policy-fail"]
    labels += ["agentic-policy-pass" if next((s for s in stages if s["stage_name"] == "agentic_policy"), {"passed": False})["passed"] else "agentic-policy-fail"]
    if not failed: labels.append("ready-to-deploy")
    if failed or any(r.get("requires_review") for r in changed_rows): labels.append("needs-review")
    completed = time.time()
    ci_run_id = f"a2-{int(started)}-{args.pr_number}"
    result = {
      "ci_run_id": ci_run_id,
      "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
      "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(completed)),
      "duration_seconds": round(completed-started, 3),
      "repo": args.repo,
      "pr_number": int(args.pr_number or 0),
      "head_sha": args.head_sha,
      "actor": args.actor,
      "changed_files": changed_rows,
      "relevant_change_count": sum(1 for r in changed_rows if r["category"] in CI_RELEVANT_CATEGORIES),
      "stage_results": stages,
      "decision": "pass" if not failed else "fail",
      "status": "passed" if not failed else "failed",
      "labels": labels,
      "summary": f"Flow A2 decision: {'PASS' if not failed else 'FAIL'}; stages={len(stages)} failed={len(failed)}",
    }
    if args.output_json:
        Path(args.output_json).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if failed else 0)
if __name__ == "__main__": main()
