#!/usr/bin/env python3
"""Fresh read-only replay of the six frozen round-7 external negatives."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import run as replay

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ORIGINAL = ROOT / "audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/VERIFICATION.json"


def execute(row):
    key = "round7--" + row["name"]
    argv = row["command"]
    if "--certificate" not in argv or "negative-inputs-v2/" not in argv[-1]:
        raise ValueError("Unexpected external command: " + repr(argv))
    env = dict(os.environ)
    env.pop("PYTHONHASHSEED", None)
    env.update(row["environment"])
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    start = time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    timed_out = False
    try:
        result = subprocess.run(argv, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=900)
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        code, stdout, stderr = None, exc.stdout or b"", exc.stderr or b""
        timed_out = True
    reason = row["expected_rejection_reason"]
    reason_found = reason in (stdout + b"\n" + stderr).decode("utf-8", "replace")
    (HERE / (key + ".stdout")).write_bytes(stdout)
    (HERE / (key + ".stderr")).write_bytes(stderr)
    receipt = {"name": row["name"], "argv": argv, "cwd": str(ROOT),
               "original_verification": str(ORIGINAL.relative_to(ROOT)),
               "started_at_utc": started, "elapsed_seconds": round(time.monotonic() - start, 6),
               "exit_code": code, "expected_exit_code": 1, "timed_out": timed_out,
               "timeout_seconds": 900, "expected_rejection_reason": reason,
               "expected_rejection_reason_found": reason_found,
               "environment": {"PYTHONHASHSEED": env.get("PYTHONHASHSEED"), "PYTHONDONTWRITEBYTECODE": "1"},
               "stdout": key + ".stdout", "stderr": key + ".stderr",
               "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
               "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
               "pass": code == 1 and reason_found and not timed_out}
    replay.dump(HERE / (key + ".json"), receipt)
    print(json.dumps({"name": receipt["name"], "pass": receipt["pass"], "elapsed_seconds": receipt["elapsed_seconds"]}), flush=True)
    return receipt


def main():
    before = replay.custody()
    replay.dump(HERE / "external-source-before.json", before)
    if before["errors"]:
        raise ValueError("Source hash mismatch")
    original = json.loads(ORIGINAL.read_text())
    rows = [r for r in original["runs"] if r["name"].startswith("external-")]
    if len(rows) != 6 or any(r["expected_exit"] != 1 or not r["expected_rejection_reason"] for r in rows):
        raise ValueError("Original external-negative scope mismatch")
    replay.dump(HERE / "external-plan.json", rows)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(execute, row) for row in rows]
        results = [future.result() for future in as_completed(futures)]
    after = replay.custody()
    replay.dump(HERE / "external-source-after.json", after)
    summary = {"schema": "941-publication-round7-external-negatives-v1", "commands": len(results),
               "pass_count": sum(r["pass"] for r in results),
               "results": sorted(results, key=lambda row: row["name"]),
               "frozen_source_files": after["files"],
               "source_errors_before": before["errors"], "source_errors_after": after["errors"],
               "status": "PASS" if all(r["pass"] for r in results) and not after["errors"] else "FAIL"}
    replay.dump(HERE / "EXTERNAL-SUMMARY.json", summary)
    print(json.dumps({k: summary[k] for k in ["status", "commands", "pass_count"]}), flush=True)
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
