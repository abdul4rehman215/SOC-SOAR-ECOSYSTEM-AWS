#!/usr/bin/env python3
import base64
import json
import os
import ssl
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_API_URL = os.getenv("WAZUH_API_URL", "https://localhost:55000")
DEFAULT_API_USER = os.getenv("WAZUH_API_USERNAME", "wazuh")
DEFAULT_API_PASS = os.getenv("WAZUH_API_PASSWORD", "wazuh")
VERIFY_TLS = os.getenv("WAZUH_API_VERIFY_TLS", "false").lower() in {"1", "true", "yes"}
DEFAULT_LOG_FORMAT = os.getenv("WAZUH_LOGTEST_LOG_FORMAT", "syslog")
DEFAULT_LOCATION = os.getenv("WAZUH_LOGTEST_LOCATION", "master->/var/log/syslog")
API_TIMEOUT = int(os.getenv("WAZUH_API_TIMEOUT", "30"))


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ssl_context():
    if VERIFY_TLS:
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def http_request(method: str, url: str, headers: Dict[str, str], body: Optional[dict] = None):
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=API_TIMEOUT, context=ssl_context()) as resp:
        return resp.read().decode("utf-8")


def authenticate(api_url: str, user: str, password: str) -> str:
    creds = f"{user}:{password}".encode("utf-8")
    auth = base64.b64encode(creds).decode("ascii")
    headers = {"Authorization": f"Basic {auth}"}
    raw = http_request("POST", f"{api_url}/security/user/authenticate?raw=true", headers)
    return raw.strip().strip('"')


def put_logtest(api_url: str, token: str, body: dict):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    raw = http_request("PUT", f"{api_url}/logtest", headers, body)
    return json.loads(raw)


def delete_session(api_url: str, token: str, session_token: str):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        http_request("DELETE", f"{api_url}/logtest/sessions/{session_token}", headers)
    except Exception:
        pass


def load_event(path: Path) -> Tuple[str, str, str, Optional[int], Optional[str]]:
    suffix = path.suffix.lower()
    if suffix in {".json", ".jsonl"}:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            raw_event = data.get("event") or data.get("raw_log") or data.get("message") or json.dumps(data)
            log_format = data.get("log_format", DEFAULT_LOG_FORMAT)
            location = data.get("location", DEFAULT_LOCATION)
            repeat = int(data.get("repeat", 1))
            session_group = data.get("session_group")
            return raw_event, log_format, location, repeat, session_group
    text = path.read_text(encoding="utf-8").strip()
    return text, DEFAULT_LOG_FORMAT, DEFAULT_LOCATION, 1, None


def load_expected(event_path: Path) -> dict:
    candidates = [
        ROOT / "tests/expected" / f"{event_path.stem}.json",
        ROOT / "tests/expected" / f"{event_path.stem}.yml",
        ROOT / "tests/expected" / f"{event_path.stem}.yaml",
    ]
    for c in candidates:
        if c.exists():
            text = c.read_text(encoding="utf-8")
            if c.suffix == ".json":
                return json.loads(text)
            try:
                import yaml
            except ImportError:
                raise RuntimeError("PyYAML is required for YAML expected files")
            return yaml.safe_load(text)
    raise FileNotFoundError(f"Expected file not found for {event_path.name}")


def compare_result(is_positive: bool, expected: dict, response: dict) -> Tuple[bool, dict]:
    data = response.get("data", {})
    output = data.get("output", {})
    alert = bool(data.get("alert", False))
    rule = output.get("rule", {}) or {}
    matched_rule_id = str(rule.get("id")) if rule.get("id") is not None else None
    matched_level = rule.get("level")
    expected_rule_ids = [str(x) for x in expected.get("expected_rule_ids", [])]
    must_alert = expected.get("must_alert")
    if must_alert is None:
        must_alert = is_positive

    passed = True
    reasons = []
    if must_alert and not alert:
        passed = False
        reasons.append("Expected alert, but no alert was generated")
    if not must_alert and alert:
        passed = False
        reasons.append("Expected no alert, but alert was generated")
    if expected_rule_ids and alert and matched_rule_id not in expected_rule_ids:
        passed = False
        reasons.append(f"Expected rule id in {expected_rule_ids}, got {matched_rule_id}")
    if "min_level" in expected and alert and matched_level is not None and int(matched_level) < int(expected["min_level"]):
        passed = False
        reasons.append(f"Expected min level {expected['min_level']}, got {matched_level}")

    detail = {
        "alert": alert,
        "matched_rule_id": matched_rule_id,
        "matched_level": matched_level,
        "expected_rule_ids": expected_rule_ids,
        "passed": passed,
        "reasons": reasons,
    }
    return passed, detail


def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            "stage": "replay",
            "status": "fail",
            "error": "Usage: run_replay_harness.py <changed_files.json>"
        }))
        sys.exit(1)

    manifest = load_manifest(Path(sys.argv[1]))
    positive_files = [ROOT / p for p in manifest.get("positive_tests", [])]
    negative_files = [ROOT / p for p in manifest.get("negative_tests", [])]

    if not positive_files and not negative_files:
        print(json.dumps({
            "stage": "replay",
            "status": "skip",
            "positive_passed": 0,
            "positive_failed": 0,
            "negative_passed": 0,
            "negative_failed": 0,
            "details": [],
            "notes": ["No positive or negative test files changed"]
        }))
        return

    try:
        auth_token = authenticate(DEFAULT_API_URL, DEFAULT_API_USER, DEFAULT_API_PASS)
    except Exception as e:
        print(json.dumps({
            "stage": "replay",
            "status": "fail",
            "error": f"Unable to authenticate to Wazuh API: {e}"
        }))
        sys.exit(1)

    counters = {
        "positive_passed": 0,
        "positive_failed": 0,
        "negative_passed": 0,
        "negative_failed": 0,
    }
    details: List[dict] = []
    session_tokens: Dict[str, str] = {}

    def run_one(path: Path, is_positive: bool):
        group_name = "positive" if is_positive else "negative"
        expected = load_expected(path)
        event, log_format, location, repeat, session_group = load_event(path)
        session_key = f"{group_name}:{session_group or path.stem}"
        last_response = None
        for _ in range(max(1, repeat)):
            body = {
                "event": event,
                "log_format": log_format,
                "location": location,
            }
            if session_key in session_tokens:
                body["token"] = session_tokens[session_key]
            last_response = put_logtest(DEFAULT_API_URL, auth_token, body)
            new_token = last_response.get("data", {}).get("token")
            if new_token:
                session_tokens[session_key] = new_token
        passed, detail = compare_result(is_positive, expected, last_response or {})
        counters[f"{group_name}_{'passed' if passed else 'failed'}"] += 1
        details.append({
            "test_file": str(path.relative_to(ROOT)),
            "expected_file": f"tests/expected/{path.stem}.json|yml|yaml",
            **detail,
        })

    status = "pass"
    try:
        for p in positive_files:
            run_one(p, True)
        for p in negative_files:
            run_one(p, False)
    except Exception as e:
        status = "fail"
        details.append({"harness_error": str(e)})

    for sess in set(session_tokens.values()):
        delete_session(DEFAULT_API_URL, auth_token, sess)

    if counters["positive_failed"] or counters["negative_failed"]:
        status = "fail"

    print(json.dumps({
        "stage": "replay",
        "status": status,
        **counters,
        "details": details,
        "notes": [
            "Replay harness uses Wazuh API /logtest sessions so multi-hit rules can be tested by reusing the same session token"
        ],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
