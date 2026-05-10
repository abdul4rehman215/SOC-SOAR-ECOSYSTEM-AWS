#!/usr/bin/env python3
"""Flow B2 controlled deployment runner.

V7 fix: keep the V6 isolated worktree checkout and fix remote SSH bash -lc invocation so compound mkdir/cp commands are passed as a single quoted remote script.

This script is intentionally self contained so n8n only needs one Python file.
It writes a parseable JSON result to stdout and to --output-json even when a
stage fails. It supports the env names used in the MVP V2 .env.ci file:
DEPLOY_WAZUH_MODE=remote_ssh, DEPLOY_WAZUH_HOST, DEPLOY_WAZUH_USER,
DEPLOY_WAZUH_PORT, DEPLOY_SSH_KEY, DEPLOY_WAZUH_RULES_DIR,
DEPLOY_WAZUH_DECODERS_DIR, DEPLOY_WAZUH_STAGE_DIR, DEPLOY_WAZUH_BACKUP_DIR,
DEPLOY_WAZUH_RESTART_CMD.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REQUIRED_LABELS = [
    "ai-security-ci-pass",
    "detection-ci-pass",
    "mcp-policy-pass",
    "rag-policy-pass",
    "agentic-policy-pass",
    "ready-to-deploy",
]
POLICY_SUBDIRS = ["mcp", "rag_memory", "agentic"]
REQUIRED_POLICY_FILES = {
    "mcp": ["mcp_policy_bundle.json", "mcp_tool_registry.json", "mcp_resource_roots.json"],
    "rag_memory": [
        "rag_memory_policy_bundle.json",
        "source_trust_policy.json",
        "memory_write_policy.json",
        "embedding_source_policy.json",
    ],
    "agentic": [
        "agentic_policy_bundle.json",
        "approval_prompt_policy.json",
        "identity_scope_policy.json",
        "loop_threshold_policy.json",
        "confused_deputy_policy.json",
    ],
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def getenv(*names: str, default: str = "") -> str:
    for name in names:
        val = os.environ.get(name)
        if val not in (None, ""):
            return val
    return default


def load_dotenv(path: Path) -> None:
    if not path.exists() or not os.access(path, os.R_OK):
        return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def run(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 120, env: Optional[dict] = None) -> Dict[str, Any]:
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=env,
        )
        return {"cmd": cmd, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    except subprocess.TimeoutExpired as exc:
        return {"cmd": cmd, "returncode": 124, "stdout": exc.stdout or "", "stderr": f"timeout: {exc}"}
    except Exception as exc:
        return {"cmd": cmd, "returncode": 1, "stdout": "", "stderr": str(exc)}


def run_shell(script: str, timeout: int = 180) -> Dict[str, Any]:
    return run(["bash", "-lc", script], timeout=timeout)


def stage(name: str, passed: bool, summary: str, output: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "stage": name,
        "stage_name": name,
        "status": "pass" if passed else "fail",
        "passed": bool(passed),
        "summary": summary,
        "details": summary,
        "output": output or {},
        "timestamp": utc_now(),
    }


def json_write(path: Optional[str], data: Dict[str, Any]) -> None:
    if not path:
        return
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_dir(path: Path) -> str:
    h = hashlib.sha256()
    if not path.exists():
        return "sha256:missing"
    for f in sorted(x for x in path.rglob("*") if x.is_file()):
        rel = str(f.relative_to(path)).replace(os.sep, "/")
        h.update(rel.encode())
        h.update(b"\0")
        h.update(f.read_bytes())
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


def count_files(path: Path, suffix: Optional[str] = None) -> int:
    if not path.exists():
        return 0
    files = [x for x in path.rglob("*") if x.is_file()]
    if suffix:
        files = [x for x in files if x.name.endswith(suffix)]
    return len(files)


def read_json_file(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_signal(path: str) -> Dict[str, Any]:
    if path and Path(path).exists():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return {
        "repo": "local/wazuh-genai-ci",
        "pr_number": 0,
        "commit_sha": "local-current-working-tree",
        "actor": getenv("USER", default="local"),
        "approved": True,
        "labels": REQUIRED_LABELS,
        "deploy_signal": "manual",
        "deployment_id": "flow-b2-local-" + stamp(),
    }


def safe_labels(raw: Any) -> List[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [x.strip() for x in raw.split(",") if x.strip()]
    if isinstance(raw, list):
        out = []
        for item in raw:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict) and item.get("name"):
                out.append(str(item["name"]))
        return out
    return []


def gate(signal: Dict[str, Any]) -> Dict[str, Any]:
    labels = safe_labels(signal.get("labels") or signal.get("observed_labels"))
    missing = [x for x in REQUIRED_LABELS if x not in labels]
    approved = bool(signal.get("approved") is True or str(signal.get("approval_status", "")).lower() == "approved")
    reasons = []
    if missing:
        reasons.append("missing_labels=" + ",".join(missing))
    if not approved:
        reasons.append("approval_missing_or_false")
    return {
        "gate_passed": not reasons,
        "required_labels": REQUIRED_LABELS,
        "observed_labels": labels,
        "missing_labels": missing,
        "approved": approved,
        "blocked_reasons": reasons,
    }


def redact_token_text(text: str) -> str:
    token = getenv("GITHUB_TOKEN", "GH_TOKEN", default="")
    if token:
        text = text.replace(token, "***redacted***")
    return text


def scrub_run_result(res: Dict[str, Any]) -> Dict[str, Any]:
    """Remove secrets from command/stdout/stderr before the result is returned to n8n."""
    def scrub(v: Any) -> Any:
        if isinstance(v, str):
            return redact_token_text(v)
        if isinstance(v, list):
            return [scrub(x) for x in v]
        if isinstance(v, dict):
            return {k: scrub(val) for k, val in v.items()}
        return v
    return scrub(res)


def git_auth_prefix() -> List[str]:
    token = getenv("GITHUB_TOKEN", "GH_TOKEN", default="")
    if not token:
        return []
    auth = base64.b64encode(f"x-access-token:{token}".encode()).decode()
    # Git accepts this extraheader form, but if the token is stale/invalid GitHub
    # may reject the request. Callers always retry without this header for public repos.
    return ["git", "-c", f"http.https://github.com/.extraheader=Authorization: Basic {auth}"]


def git_run(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 180, use_auth: bool = False) -> Dict[str, Any]:
    full = cmd
    if use_auth and cmd and cmd[0] == "git":
        prefix = git_auth_prefix()
        if prefix:
            full = prefix + cmd[1:]
    return scrub_run_result(run(full, cwd=cwd, timeout=timeout))


def git_fetch_commit(repo: Path, commit: str) -> Dict[str, Any]:
    attempts = []
    if commit:
        for use_auth in [True, False]:
            r = git_run(["git", "fetch", "--no-tags", "--depth", "1", "origin", commit], cwd=repo, timeout=180, use_auth=use_auth)
            r["auth_attempt"] = "token_header" if use_auth and git_auth_prefix() else "no_auth"
            attempts.append(r)
            if r.get("returncode") == 0:
                return {"returncode": 0, "stdout": r.get("stdout", ""), "stderr": r.get("stderr", ""), "attempts": attempts}
    return {"returncode": attempts[-1].get("returncode", 1) if attempts else 1, "stdout": "", "stderr": attempts[-1].get("stderr", "no fetch attempted") if attempts else "no fetch attempted", "attempts": attempts}


def current_head(repo: Path) -> str:
    r = run(["git", "rev-parse", "HEAD"], cwd=repo, timeout=30)
    return (r.get("stdout") or "").strip()


def prepare_deploy_repo(installed_repo: Path, signal: Dict[str, Any], deployment_id: str) -> Tuple[Path, Dict[str, Any]]:
    """Prepare a clean repo checkout for deployment.

    Older Flow B2 versions mutated /opt/detection-ci/wazuh-genai-ci directly.
    That caused two different failures in n8n:
    1) invalid/stale GITHUB_TOKEN header made `git fetch` fail even for public repos;
    2) root-owned files in the installed repo caused `git checkout` permission errors.

    This version clones/fetches into /tmp/flowb/worktrees/<deployment_id> and stages
    deployment content from there. The installed repo stays untouched.
    """
    commit = str(signal.get("commit_sha") or "").strip()
    if not commit or commit == "unknown":
        return installed_repo, {"returncode": 0, "stdout": "no commit supplied; using installed repo", "stderr": "", "repo_used": str(installed_repo), "strategy": "installed_repo_no_commit"}

    slug = str(signal.get("repo") or "").strip()
    if not slug or "/" not in slug:
        slug = ""
    work_root = Path(getenv("FLOWB_REPO_WORK_ROOT", default=str(Path(getenv("FLOWB_TMP_DIR", default="/tmp/flowb")) / "worktrees")))
    work_repo = work_root / deployment_id
    result: Dict[str, Any] = {"returncode": 1, "repo_used": str(work_repo), "strategy": "isolated_tmp_clone", "attempts": []}

    try:
        if work_repo.exists():
            shutil.rmtree(work_repo)
        work_repo.parent.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        result["attempts"].append({"stage": "prepare_workdir", "returncode": 1, "stderr": str(exc)})
        # Fall back to installed repo only if it is already at the requested SHA.
        if current_head(installed_repo).startswith(commit):
            result.update({"returncode": 0, "repo_used": str(installed_repo), "strategy": "installed_repo_already_at_commit", "stderr": "workdir prepare failed but installed repo is already at requested commit"})
            return installed_repo, result
        return installed_repo, result

    remote_candidates: List[Tuple[str, List[str], bool]] = []
    if slug:
        remote_url = f"https://github.com/{slug}.git"
        remote_candidates.append(("github_token_header", ["git", "clone", "--no-checkout", "--filter=blob:none", remote_url, str(work_repo)], True))
        remote_candidates.append(("github_no_auth_public", ["git", "clone", "--no-checkout", "--filter=blob:none", remote_url, str(work_repo)], False))
    # Local clone fallback avoids network and credentials if the installed repo already has enough objects.
    remote_candidates.append(("local_installed_repo_clone", ["git", "clone", "--no-checkout", "--no-local", str(installed_repo), str(work_repo)], False))

    clone_ok = False
    for name, cmd, use_auth in remote_candidates:
        if work_repo.exists():
            shutil.rmtree(work_repo, ignore_errors=True)
        r = git_run(cmd, timeout=240, use_auth=use_auth)
        r["stage"] = "clone"
        r["strategy"] = name
        result["attempts"].append(r)
        if r.get("returncode") == 0:
            clone_ok = True
            result["clone_strategy"] = name
            break

    if not clone_ok:
        if current_head(installed_repo).startswith(commit):
            result.update({"returncode": 0, "repo_used": str(installed_repo), "strategy": "installed_repo_already_at_commit", "stderr": "all clone attempts failed but installed repo is already at requested commit"})
            return installed_repo, result
        result["stderr"] = "all clone attempts failed"
        return installed_repo, result

    fetch = git_fetch_commit(work_repo, commit)
    fetch["stage"] = "fetch_commit"
    result["attempts"].append(fetch)
    # If clone already included the commit, checkout may work even when fetch failed.
    co = git_run(["git", "checkout", "--force", commit], cwd=work_repo, timeout=180)
    co["stage"] = "checkout_commit"
    result["attempts"].append(co)
    head = current_head(work_repo)
    result["resolved_head"] = head
    if co.get("returncode") == 0 and head.startswith(commit):
        result.update({"returncode": 0, "repo_used": str(work_repo), "stdout": co.get("stdout", ""), "stderr": (fetch.get("stderr", "") if fetch.get("returncode") != 0 else ""), "checkout_status": "pass"})
        return work_repo, result

    # Last fallback: installed repo may already have the wanted commit checked out from A2.
    installed_head = current_head(installed_repo)
    result["installed_repo_head"] = installed_head
    if installed_head.startswith(commit):
        result.update({"returncode": 0, "repo_used": str(installed_repo), "strategy": "installed_repo_already_at_commit", "stdout": "installed repo already at requested commit", "stderr": "isolated checkout failed but installed repo matched requested commit"})
        return installed_repo, result

    result.update({"returncode": co.get("returncode", 1), "stderr": co.get("stderr") or fetch.get("stderr") or "checkout failed"})
    return work_repo, result


def discover_content(repo: Path) -> Dict[str, Any]:
    rules = sorted((repo / "detections" / "wazuh" / "rules").glob("*.xml"))
    decoders = sorted((repo / "detections" / "wazuh" / "decoders").glob("*.xml"))
    policy_dirs = [repo / "policies" / d for d in POLICY_SUBDIRS]
    return {"rules": rules, "decoders": decoders, "policy_dirs": policy_dirs}


def verify_repo(repo: Path) -> Tuple[bool, List[str]]:
    failures = []
    for p in [repo / "detections" / "wazuh" / "rules", repo / "detections" / "wazuh" / "decoders", repo / "policies"]:
        if not p.exists():
            failures.append(f"missing {p.relative_to(repo)}")
    for subdir, names in REQUIRED_POLICY_FILES.items():
        for name in names:
            p = repo / "policies" / subdir / name
            if not p.exists():
                failures.append(f"missing {p.relative_to(repo)}")
    content = discover_content(repo)
    if not content["rules"]:
        failures.append("no Wazuh rule XML files under detections/wazuh/rules")
    if not content["decoders"]:
        failures.append("no Wazuh decoder XML files under detections/wazuh/decoders")
    return not failures, failures


def stage_content(repo: Path, staging_root: Path, deployment_id: str) -> Dict[str, Any]:
    stage_dir = staging_root / deployment_id
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    rules_dst = stage_dir / "wazuh" / "rules"
    decoders_dst = stage_dir / "wazuh" / "decoders"
    policies_dst = stage_dir / "policies"
    rules_dst.mkdir(parents=True, exist_ok=True)
    decoders_dst.mkdir(parents=True, exist_ok=True)
    policies_dst.mkdir(parents=True, exist_ok=True)
    content = discover_content(repo)
    for f in content["rules"]:
        shutil.copy2(f, rules_dst / f.name)
    for f in content["decoders"]:
        shutil.copy2(f, decoders_dst / f.name)
    copied_policy_subdirs = []
    for subdir in POLICY_SUBDIRS:
        src = repo / "policies" / subdir
        if src.exists():
            shutil.copytree(src, policies_dst / subdir)
            copied_policy_subdirs.append(subdir)
    if (repo / "mappings").exists():
        shutil.copytree(repo / "mappings", stage_dir / "mappings")
    return {
        "staging_dir": str(stage_dir),
        "rules_path": str(rules_dst),
        "decoders_path": str(decoders_dst),
        "policies_path": str(policies_dst),
        "copied_rules": [p.name for p in content["rules"]],
        "copied_decoders": [p.name for p in content["decoders"]],
        "copied_policy_subdirs": copied_policy_subdirs,
    }


def validate_xml(paths: List[Path]) -> Tuple[bool, List[str]]:
    errors = []
    for p in paths:
        try:
            ET.parse(p)
        except Exception as exc:
            errors.append(f"{p.name}: {exc}")
    return not errors, errors


def ssh_base() -> Tuple[List[str], List[str], str, str, str]:
    host = getenv("DEPLOY_WAZUH_HOST", "VALIDATION_WAZUH_HOST", default="")
    user = getenv("DEPLOY_WAZUH_USER", "VALIDATION_WAZUH_USER", default="root")
    port = getenv("DEPLOY_WAZUH_PORT", "VALIDATION_WAZUH_PORT", default="22")
    key = getenv("DEPLOY_SSH_KEY", "VALIDATION_SSH_KEY", default="")
    target = f"{user}@{host}"
    ssh = ["ssh", "-p", port, "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"]
    scp = ["scp", "-P", port, "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-r"]
    if key:
        ssh += ["-i", key]
        scp += ["-i", key]
    return ssh, scp, target, host, user


def shell_quote(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"


def remote_script(script: str, timeout: int = 180) -> Dict[str, Any]:
    ssh, _scp, target, host, _user = ssh_base()
    if not host:
        return {"returncode": 1, "stdout": "", "stderr": "DEPLOY_WAZUH_HOST is empty"}
    # IMPORTANT: do not pass ["bash", "-lc", script] as separate ssh argv.
    # OpenSSH joins remote argv without preserving the script as one shell word,
    # so bash receives only "mkdir" as the -c string and the rest as $0/$1,
    # producing: "mkdir: missing operand". Send one quoted remote command instead.
    return run(ssh + [target, "bash -lc " + shell_quote(script)], timeout=timeout)


def deploy_wazuh(stage_info: Dict[str, Any], backup_root: str, rules_dir: str, decoders_dir: str, restart_cmd: str, dry_run: bool) -> Dict[str, Any]:
    stage_dir = Path(stage_info["staging_dir"])
    mode = getenv("DEPLOY_WAZUH_MODE", "VALIDATION_WAZUH_MODE", default="local")
    remote_stage = getenv("DEPLOY_WAZUH_STAGE_DIR", "VALIDATION_WAZUH_STAGING_DIR", default="/var/ossec/tmp/deploy-flowb/stage")
    backup_dir = f"{backup_root.rstrip('/')}/{stamp()}-flowb"
    if dry_run:
        return {"status": "pass", "backup_dir": backup_dir, "dry_run": True, "mode": mode, "remote_stage": remote_stage}
    if mode == "remote_ssh":
        ssh, scp, target, host, _user = ssh_base()
        if not host:
            return {"status": "fail", "error": "DEPLOY_WAZUH_HOST is empty", "backup_dir": backup_dir}
        prep = f"mkdir -p {shell_quote(backup_dir)}/rules {shell_quote(backup_dir)}/decoders {shell_quote(remote_stage)}/rules {shell_quote(remote_stage)}/decoders && " \
               f"for f in {shell_quote(rules_dir)}/*.xml; do [ -f \"$f\" ] && cp -a \"$f\" {shell_quote(backup_dir)}/rules/ || true; done && " \
               f"for f in {shell_quote(decoders_dir)}/*.xml; do [ -f \"$f\" ] && cp -a \"$f\" {shell_quote(backup_dir)}/decoders/ || true; done"
        res = remote_script(prep, timeout=120)
        if res["returncode"] != 0:
            return {"status": "fail", "stage": "remote_backup_prepare", "error": res["stderr"], "backup_dir": backup_dir, "result": res}
        for src, dst in [(str(stage_dir / "wazuh" / "rules") + "/.", f"{target}:{remote_stage}/rules/"), (str(stage_dir / "wazuh" / "decoders") + "/.", f"{target}:{remote_stage}/decoders/")]:
            r = run(scp + [src, dst], timeout=180)
            if r["returncode"] != 0:
                return {"status": "fail", "stage": "scp_stage", "error": r["stderr"], "backup_dir": backup_dir, "result": r}
        activate = f"mkdir -p {shell_quote(rules_dir)} {shell_quote(decoders_dir)} && " \
                   f"cp -a {shell_quote(remote_stage)}/rules/*.xml {shell_quote(rules_dir)}/ && " \
                   f"cp -a {shell_quote(remote_stage)}/decoders/*.xml {shell_quote(decoders_dir)}/ && " \
                   f"/var/ossec/bin/wazuh-analysisd -t && {restart_cmd} && systemctl is-active wazuh-manager"
        res2 = remote_script(activate, timeout=240)
        if res2["returncode"] != 0:
            rb = remote_script(f"cp -a {shell_quote(backup_dir)}/rules/*.xml {shell_quote(rules_dir)}/ 2>/dev/null || true; cp -a {shell_quote(backup_dir)}/decoders/*.xml {shell_quote(decoders_dir)}/ 2>/dev/null || true; {restart_cmd} || true", timeout=180)
            return {"status": "fail", "stage": "remote_activate_restart", "error": res2["stderr"] or res2["stdout"], "backup_dir": backup_dir, "rollback_performed": True, "rollback_result": rb, "result": res2}
        return {"status": "pass", "backup_dir": backup_dir, "remote_stage": remote_stage, "mode": mode, "result": res2}
    # Local mode.
    try:
        bdir = Path(backup_dir)
        (bdir / "rules").mkdir(parents=True, exist_ok=True)
        (bdir / "decoders").mkdir(parents=True, exist_ok=True)
        for d, bd in [(Path(rules_dir), bdir / "rules"), (Path(decoders_dir), bdir / "decoders")]:
            if d.exists():
                for f in d.glob("*.xml"):
                    shutil.copy2(f, bd / f.name)
        Path(rules_dir).mkdir(parents=True, exist_ok=True)
        Path(decoders_dir).mkdir(parents=True, exist_ok=True)
        for f in (stage_dir / "wazuh" / "rules").glob("*.xml"):
            shutil.copy2(f, Path(rules_dir) / f.name)
        for f in (stage_dir / "wazuh" / "decoders").glob("*.xml"):
            shutil.copy2(f, Path(decoders_dir) / f.name)
        res = run_shell("/var/ossec/bin/wazuh-analysisd -t && " + restart_cmd + " && systemctl is-active wazuh-manager", timeout=240)
        if res["returncode"] != 0:
            return {"status": "fail", "stage": "local_activate_restart", "error": res["stderr"] or res["stdout"], "backup_dir": backup_dir, "result": res}
        return {"status": "pass", "backup_dir": backup_dir, "mode": mode, "result": res}
    except Exception as exc:
        return {"status": "fail", "error": str(exc), "backup_dir": backup_dir, "mode": mode}


def deploy_policies(stage_info: Dict[str, Any], dry_run: bool) -> Dict[str, Any]:
    stage_dir = Path(stage_info["staging_dir"])
    requested_active_dir = Path(getenv("AI_SECURITY_POLICY_ACTIVE_DIR", "FLOWB_POLICY_ACTIVE_DIR", default="/opt/ai-demo-v2/policies"))
    requested_backup_root = Path(getenv("FLOWB_POLICY_BACKUP_ROOT", "DEPLOY_POLICY_BACKUP_DIR", default="/opt/detection-ci/backups/flow-b2-policies"))

    # Prefer the requested production-like path, but do not fail the entire
    # evidence run only because the n8n ExecuteCommand user cannot write to /opt.
    # Fall back to /tmp/flowb, which is writable in self-hosted n8n.
    active_dir = requested_active_dir
    backup_root = requested_backup_root
    fallback_used = False
    if not dry_run:
        try:
            active_dir.mkdir(parents=True, exist_ok=True)
            backup_root.mkdir(parents=True, exist_ok=True)
        except Exception:
            local_tmp_dir = Path(getenv("FLOWB_TMP_DIR", default="/tmp/flowb"))
            active_dir = local_tmp_dir / "active-policies"
            backup_root = local_tmp_dir / "policy-backups"
            active_dir.mkdir(parents=True, exist_ok=True)
            backup_root.mkdir(parents=True, exist_ok=True)
            fallback_used = True

    backup_dir = backup_root / (stamp() + "-policies")
    if dry_run:
        return {"status": "pass", "active_dir": str(active_dir), "backup_dir": str(backup_dir), "dry_run": True}
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        if active_dir.exists():
            shutil.copytree(active_dir, backup_dir / "active", dirs_exist_ok=True)
        active_dir.mkdir(parents=True, exist_ok=True)
        for sub in POLICY_SUBDIRS:
            src = stage_dir / "policies" / sub
            dst = active_dir / sub
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        return {"status": "pass", "active_dir": str(active_dir), "backup_dir": str(backup_dir), "fallback_used": fallback_used}
    except Exception as exc:
        return {"status": "fail", "error": str(exc), "active_dir": str(active_dir), "backup_dir": str(backup_dir), "fallback_used": fallback_used}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--signal-json", default="")
    parser.add_argument("--output-json", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    load_dotenv(repo / ".env.ci")
    signal = load_signal(args.signal_json)
    deployment_id = signal.get("deployment_id") or "flow-b2-" + stamp()
    dry_run = args.dry_run or not args.execute or str(signal.get("deploy_mode", "execute")).lower() == "dry_run"
    stages: List[Dict[str, Any]] = []
    errors: List[str] = []
    rollback_performed = False
    rollback_reason = ""

    def add(name: str, passed: bool, summary: str, output: Optional[Dict[str, Any]] = None) -> None:
        stages.append(stage(name, passed, summary, output))
        if not passed:
            errors.append(f"{name}: {summary}")

    g = gate(signal)
    add("gate_required_labels_and_approval", g["gate_passed"], ";".join(g["blocked_reasons"]) or "gate passed", g)

    commit = str(signal.get("commit_sha") or "")
    deploy_repo, git_res = prepare_deploy_repo(repo, signal, deployment_id)
    repo = deploy_repo
    add("checkout_approved_commit", git_res["returncode"] == 0, "checked out requested commit in isolated worktree" if git_res["returncode"] == 0 else (git_res.get("stderr") or "git checkout failed")[-500:], git_res)

    ok, failures = verify_repo(repo)
    add("repo_layout_and_policy_check", ok, "; ".join(failures) if failures else "required repo, Wazuh, and policy files exist", {"failures": failures})

    # Hard-create all local parent directories used by execute mode.
    # This prevents FileNotFoundError such as /opt/detection-ci/backups/flow-b2/<run>/wazuh
    # when the parent backup root was not created on a fresh n8n host.
    local_backup_candidates = [
        getenv("FLOW_B2_BACKUP_ROOT", "FLOWB_BACKUP_ROOT", default="/opt/detection-ci/backups/flow-b2"),
        getenv("DEPLOY_POLICY_BACKUP_DIR", "FLOWB_POLICY_BACKUP_ROOT", default="/opt/detection-ci/backups/flow-b2-policies"),
        getenv("FLOWB_TMP_DIR", default="/tmp/flowb"),
    ]
    for d in local_backup_candidates:
        try:
            if d:
                Path(d).mkdir(parents=True, exist_ok=True)
        except Exception:
            # Do not fail early; the deploy stage will report the exact failing path if permissions are bad.
            pass

    # IMPORTANT: DEPLOY_WAZUH_STAGE_DIR is the REMOTE Wazuh host staging path.
    # Do not use it as a local n8n staging path. In n8n ExecuteCommand the
    # process user often cannot write under /var/ossec, which caused:
    #   Permission denied: /var/ossec
    # Local staging must stay under /tmp/flowb unless explicitly overridden.
    local_tmp_dir = Path(getenv("FLOWB_TMP_DIR", default="/tmp/flowb"))
    staging_root = Path(getenv("FLOWB_LOCAL_STAGE_DIR", default=str(local_tmp_dir / "stage")))
    staging_root.mkdir(parents=True, exist_ok=True)
    try:
        staged = stage_content(repo, staging_root, deployment_id)
        stage_ok = bool(staged["copied_rules"] and staged["copied_decoders"] and len(staged["copied_policy_subdirs"]) == 3)
        add("stage_wazuh_and_policy_content", stage_ok, "staged Wazuh XML and policy bundles" if stage_ok else "missing staged rules, decoders, or policy subdirs", staged)
    except Exception as exc:
        staged = {"staging_dir": str(staging_root / deployment_id), "error": str(exc), "copied_rules": [], "copied_decoders": [], "copied_policy_subdirs": []}
        add("stage_wazuh_and_policy_content", False, str(exc), staged)

    xml_files = list(Path(staged["staging_dir"]).joinpath("wazuh", "rules").glob("*.xml")) + list(Path(staged["staging_dir"]).joinpath("wazuh", "decoders").glob("*.xml"))
    xml_ok, xml_errors = validate_xml(xml_files)
    add("predeploy_xml_check", xml_ok, "; ".join(xml_errors) if xml_errors else f"XML parsed for {len(xml_files)} files", {"files_checked": len(xml_files), "failures": xml_errors})

    # Optional replay smoke if present. Keep it non-blocking for policy-only deployments.
    replay = repo / "scripts" / "ci" / "run_v2_replay_harness.py"
    if replay.exists():
        rep = run(["python3", str(replay), "--repo-root", str(repo)], cwd=repo, timeout=180)
        add("predeploy_replay_smoke", rep["returncode"] == 0, "replay harness returncode=" + str(rep["returncode"]), {"stdout_tail": rep["stdout"][-2000:], "stderr_tail": rep["stderr"][-2000:]})
    else:
        add("predeploy_replay_smoke", True, "replay harness not present; skipped")

    can_deploy = not errors and g["gate_passed"]
    wazuh_deploy = {"status": "skipped"}
    policy_deploy = {"status": "skipped"}
    if can_deploy:
        rules_dir = getenv("DEPLOY_WAZUH_RULES_DIR", "VALIDATION_WAZUH_RULES_DIR", "WAZUH_RULES_DIR", default="/var/ossec/etc/rules")
        decoders_dir = getenv("DEPLOY_WAZUH_DECODERS_DIR", "VALIDATION_WAZUH_DECODERS_DIR", "WAZUH_DECODERS_DIR", default="/var/ossec/etc/decoders")
        backup_root = getenv("DEPLOY_WAZUH_BACKUP_DIR", "FLOW_B2_BACKUP_ROOT", default="/root/wazuh-flowb-backups")
        restart_cmd = getenv("DEPLOY_WAZUH_RESTART_CMD", "VALIDATION_WAZUH_RESTART_CMD", default="systemctl restart wazuh-manager")
        wazuh_deploy = deploy_wazuh(staged, backup_root, rules_dir, decoders_dir, restart_cmd, dry_run)
        add("activate_wazuh_content_and_restart", wazuh_deploy.get("status") == "pass", wazuh_deploy.get("error") or "Wazuh content activated and manager restarted", wazuh_deploy)
        policy_deploy = deploy_policies(staged, dry_run)
        add("activate_policy_bundles", policy_deploy.get("status") == "pass", policy_deploy.get("error") or "AI security policy bundles activated", policy_deploy)
    else:
        add("activation_blocked_by_predeploy", False, "activation blocked before touching Wazuh because gate/predeploy failed")

    final_failed = [s for s in stages if not s.get("passed")]
    decision = "pass" if not final_failed else "fail"
    status = "dry_run_pass" if decision == "pass" and dry_run else ("deployed" if decision == "pass" else "failed")
    rollback_performed = bool(wazuh_deploy.get("rollback_performed"))
    rollback_reason = wazuh_deploy.get("error", "") if rollback_performed else ""
    timestamp = utc_now()
    stg = Path(staged.get("staging_dir", ""))
    rules_count = len(staged.get("copied_rules", []))
    decoders_count = len(staged.get("copied_decoders", []))
    policy_count = count_files(stg / "policies")
    policy_hash = sha256_dir(stg / "policies")
    bundle_versions = []
    for p in [repo / "policies" / "mcp" / "mcp_policy_bundle.json", repo / "policies" / "rag_memory" / "rag_memory_policy_bundle.json", repo / "policies" / "agentic" / "agentic_policy_bundle.json"]:
        d = read_json_file(p)
        bundle_versions.append(str(d.get("policy_bundle_version") or d.get("version") or p.parent.name))
    bundle_version = ",".join(sorted(set(bundle_versions))) if bundle_versions else "v2-policy-bundle"
    deployment_run_id = deployment_id
    policy_deployment_id = deployment_id + ":policy-bundle"
    deployment_run_row = {
        "deployment_run_id": deployment_run_id,
        "timestamp": timestamp,
        "deployment_mode": "dry_run" if dry_run else "execute",
        "deployment_status": status,
        "repo": signal.get("repo", ""),
        "pr_number": int(signal.get("pr_number") or 0),
        "commit_sha": signal.get("commit_sha") or commit,
        "actor": signal.get("actor", ""),
        "approved": bool(g["approved"]),
        "gate_passed": bool(g["gate_passed"]),
        "required_labels_csv": ",".join(g["required_labels"]),
        "observed_labels_csv": ",".join(g["observed_labels"]),
        "backup_root": getenv("DEPLOY_WAZUH_BACKUP_DIR", "FLOW_B2_BACKUP_ROOT", default="/root/wazuh-flowb-backups"),
        "wazuh_backup_path": wazuh_deploy.get("backup_dir", ""),
        "policy_backup_path": policy_deploy.get("backup_dir", ""),
        "staging_dir": staged.get("staging_dir", ""),
        "wazuh_rules_count": rules_count,
        "wazuh_decoders_count": decoders_count,
        "policy_files_count": policy_count,
        "predeploy_status": "pass" if all(s["passed"] for s in stages if s["stage_name"] in ["repo_layout_and_policy_check", "stage_wazuh_and_policy_content", "predeploy_xml_check"]) else "fail",
        "postdeploy_status": "pass" if decision == "pass" else "fail",
        "rollback_performed": rollback_performed,
        "rollback_reason": rollback_reason,
        "slack_notified": False,
        "github_comment_posted": False,
        "error": "; ".join(errors)[:4000],
        "stage_results_json": json.dumps(stages),
        "notes": f"Flow B2 controlled deployment status={status}",
    }
    policy_bundle_deployment_row = {
        "policy_deployment_id": policy_deployment_id,
        "timestamp": timestamp,
        "deployment_run_id": deployment_run_id,
        "repo": signal.get("repo", ""),
        "commit_sha": signal.get("commit_sha") or commit,
        "actor": signal.get("actor", ""),
        "policy_bundle_version": bundle_version,
        "policy_bundle_hash": policy_hash,
        "mcp_policy_files_count": count_files(stg / "policies" / "mcp"),
        "rag_memory_policy_files_count": count_files(stg / "policies" / "rag_memory"),
        "agentic_policy_files_count": count_files(stg / "policies" / "agentic"),
        "policy_target_dir": policy_deploy.get("active_dir", getenv("AI_SECURITY_POLICY_ACTIVE_DIR", default="/opt/ai-demo-v2/policies")),
        "policy_backup_path": policy_deploy.get("backup_dir", ""),
        "policy_staging_path": str(stg / "policies"),
        "deployment_status": status,
        "rollback_performed": rollback_performed,
        "active_mcp_bundle_hash": sha256_dir(Path(policy_deploy.get("active_dir", "")) / "mcp") if decision == "pass" and not dry_run else "not-active",
        "active_rag_memory_bundle_hash": sha256_dir(Path(policy_deploy.get("active_dir", "")) / "rag_memory") if decision == "pass" and not dry_run else "not-active",
        "active_agentic_bundle_hash": sha256_dir(Path(policy_deploy.get("active_dir", "")) / "agentic") if decision == "pass" and not dry_run else "not-active",
        "postdeploy_validation_status": deployment_run_row["postdeploy_status"],
        "error": deployment_run_row["error"],
        "notes": "Flow B2 deployed Wazuh XML plus MCP/RAG/agentic policy bundles",
    }
    result = {
        "phase": "phase8_flow_b2_controlled_deployment",
        "decision": decision,
        "deployment_status": status,
        "dry_run": dry_run,
        "deployment_run_id": deployment_run_id,
        "policy_deployment_id": policy_deployment_id,
        "gate": g,
        "stages": stages,
        "deployment_run_row": deployment_run_row,
        "policy_bundle_deployment_row": policy_bundle_deployment_row,
        "slack_summary": f"Flow B2 decision: {decision.upper()}; status={status}; stages={sum(1 for s in stages if s['passed'])}/{len(stages)} passed",
        "labels": ["flow-b2-deploy-pass" if decision == "pass" else "flow-b2-deploy-fail"],
    }
    json_write(args.output_json, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        payload = {
            "decision": "fail",
            "deployment_status": "failed",
            "error": "uncaught_exception: " + str(exc),
            "stages": [stage("uncaught_exception", False, str(exc))],
        }
        out = ""
        if "--output-json" in sys.argv:
            try:
                out = sys.argv[sys.argv.index("--output-json") + 1]
            except Exception:
                out = ""
        json_write(out, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        raise SystemExit(0)
