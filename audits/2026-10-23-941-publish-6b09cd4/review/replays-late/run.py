#!/usr/bin/env python3
"""Read-only publication replay of 13 frozen later 941 audit directories.

Run from any directory with python3 -B /path/to/this/run.py. Outputs are
confined to this receipt directory. No producer or hash-guard bypass is used.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE_PATH = HERE.parents[1] / "BASE.json"
NAMES = [
    "gamma8-empty-k-stars", "gamma8-empty-resource-stars", "gamma8-empty-seven",
    "gamma8-k-star-review", "gamma8-n-stars", "gamma8-n7-review",
    "gamma8-nonempty-k-stars", "gamma8-nonempty-resource-stars",
    "gamma8-resource-review", "types-wrong-side-round4",
    "types-wrong-side-round5", "types-wrong-side-round6", "types-wrong-side-round7",
]
PREFIX = "audits/2026-10-23-941-"
SUFFIX = "-6b09cd4"
TIMEOUT_SECONDS = 900


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def custody():
    frozen = json.loads(BASE_PATH.read_text())
    dirs = {PREFIX + name + SUFFIX for name in NAMES}
    rows = [row for row in frozen["entries"] if any(row["path"].startswith(d + "/") for d in dirs)]
    errors = []
    for row in rows:
        path = ROOT / row["path"]
        try:
            raw = path.read_bytes()
            observed = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        except OSError as exc:
            errors.append({"path": row["path"], "error": str(exc)})
            continue
        expected = {key: row[key] for key in ["bytes", "sha256"]}
        if observed != expected:
            errors.append({"path": row["path"], "expected": expected, "observed": observed})
    return {"base": frozen["base"], "directories": sorted(dirs), "files": len(rows), "errors": errors}


def plan():
    entries = []
    for name in NAMES:
        entries.append((name, "check.py", name not in {"gamma8-n7-review", "types-wrong-side-round5", "types-wrong-side-round6"}))
    entries.extend([
        ("types-wrong-side-round5", "transfer_caps.py", False),
        ("gamma8-k-star-review", "check_transfers.py", False),
    ])
    tasks = []
    for name, script, seed_cli in entries:
        for mode in ["normal", "seed17", "negative"]:
            argv = ["python3", "-B"] + (["-O"] if mode == "seed17" else [])
            argv += [PREFIX + name + SUFFIX + "/" + script]
            if mode == "seed17" and seed_cli:
                argv += ["--seed", "17"]
            if mode == "negative":
                argv += ["--negative"]
            tasks.append({"name": name, "script": script, "mode": mode, "argv": argv})
    return tasks


def execute(task):
    key = task["name"] + "--" + Path(task["script"]).stem + "--" + task["mode"]
    env = dict(os.environ)
    env.pop("PYTHONHASHSEED", None)
    if task["mode"] == "seed17":
        env["PYTHONHASHSEED"] = "17"
    # -B is also explicit in argv; the variable protects imported children.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    start = time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    timed_out = False
    try:
        completed = subprocess.run(task["argv"], cwd=ROOT, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, timeout=TIMEOUT_SECONDS)
        stdout, stderr, code = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, code = exc.stdout or b"", exc.stderr or b"", None
        timed_out = True
    elapsed = round(time.monotonic() - start, 6)
    (HERE / (key + ".stdout")).write_bytes(stdout)
    (HERE / (key + ".stderr")).write_bytes(stderr)
    payload = None
    error = None
    try:
        payload = json.loads(stdout)
    except (ValueError, UnicodeDecodeError) as exc:
        error = str(exc)
    receipt = {**task, "cwd": str(ROOT), "started_at_utc": started,
               "elapsed_seconds": elapsed, "exit_code": code, "timed_out": timed_out,
               "timeout_seconds": TIMEOUT_SECONDS,
               "environment": {"PYTHONHASHSEED": env.get("PYTHONHASHSEED"),
                               "PYTHONDONTWRITEBYTECODE": "1"},
               "environment_note": "Other environment variables are inherited; secrets are not serialized.",
               "stdout": key + ".stdout", "stderr": key + ".stderr",
               "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
               "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
               "payload": payload, "payload_parse_error": error,
               "pass": payload_pass(code, payload)}
    dump(HERE / (key + ".json"), receipt)
    print(json.dumps({"key": key, "pass": receipt["pass"], "elapsed_seconds": elapsed}), flush=True)
    return receipt


def payload_pass(code, payload):
    if code != 0 or not isinstance(payload, dict):
        return False
    status = payload.get("status", payload.get("validation", {}).get("status"))
    return status in {"PASS", "triggered and holds"}


def negative_count(payload):
    keys = {"negative_controls_rejected", "negative_rejected", "rejected",
            "negative_controls", "semantic_negatives_rejected"}
    total = 0
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in keys and isinstance(value, list):
                total += len(value)
            elif key in keys and isinstance(value, int):
                total += value
            elif isinstance(value, dict):
                total += negative_count(value)
    return total


def without_seed(value):
    if isinstance(value, dict):
        return {k: without_seed(v) for k, v in value.items() if k != "seed"}
    if isinstance(value, list):
        return [without_seed(v) for v in value]
    return value


def summarize(results, before):
    results.sort(key=lambda row: (row["name"], row["script"], row["mode"]))
    for row in results:
        row["pass"] = payload_pass(row["exit_code"], row["payload"])
        if row["mode"] == "negative":
            row["semantic_controls_rejected"] = negative_count(row["payload"])
            row["pass"] = row["pass"] and row["semantic_controls_rejected"] > 0
        key = row["name"] + "--" + Path(row["script"]).stem + "--" + row["mode"]
        dump(HERE / (key + ".json"), row)
    pairs = []
    for name, script in sorted({(r["name"], r["script"]) for r in results}):
        runs = {r["mode"]: r for r in results if r["name"] == name and r["script"] == script}
        pairs.append({"name": name, "script": script,
                      "normal_seed17_payload_equal_ignoring_seed": without_seed(runs["normal"]["payload"]) == without_seed(runs["seed17"]["payload"])})
    after = custody()
    dump(HERE / "source-after.json", after)
    failures = [{"name": r["name"], "script": r["script"], "mode": r["mode"], "exit_code": r["exit_code"]} for r in results if not r["pass"]]
    summary = {"schema": "941-publication-later-replay-v1", "directories": len(NAMES),
               "checker_entries": len(pairs), "commands": len(results),
               "pass_count": len(results) - len(failures), "failures": failures,
               "semantic_controls_rejected": sum(r.get("semantic_controls_rejected", 0) for r in results),
               "source_custody_before": before, "source_custody_after": after,
               "normal_seed17_comparisons": pairs,
               "status": "PASS" if not failures and not after["errors"] and all(p["normal_seed17_payload_equal_ignoring_seed"] for p in pairs) else "FAIL",
               "authority_boundary": {"finite_control": "triggered and holds", "actual_complete_source": "not triggered"}}
    dump(HERE / "SUMMARY.json", summary)
    print(json.dumps({k: summary[k] for k in ["status", "directories", "checker_entries", "commands", "pass_count", "failures"]}), flush=True)
    return 0 if summary["status"] == "PASS" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summarize", action="store_true", help="Re-read existing raw command receipts without rerunning commands")
    args = parser.parse_args()
    tasks = plan()
    if args.summarize:
        before = json.loads((HERE / "source-before.json").read_text())
        results = []
        for task in tasks:
            key = task["name"] + "--" + Path(task["script"]).stem + "--" + task["mode"]
            row = json.loads((HERE / (key + ".json")).read_text())
            for stream in ["stdout", "stderr"]:
                raw = (HERE / row[stream]).read_bytes()
                if hashlib.sha256(raw).hexdigest() != row[stream + "_sha256"]:
                    raise ValueError("Receipt hash mismatch: " + key + " " + stream)
            if row["payload"] != json.loads((HERE / row["stdout"]).read_bytes()):
                raise ValueError("Parsed payload mismatch: " + key)
            results.append(row)
    else:
        before = custody()
        dump(HERE / "source-before.json", before)
        if before["errors"]:
            raise SystemExit("Frozen source hash mismatch; see source-before.json")
        dump(HERE / "plan.json", tasks)
        results = []
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(execute, task) for task in tasks]
            for future in as_completed(futures):
                results.append(future.result())
    return summarize(results, before)


if __name__ == "__main__":
    sys.exit(main())
