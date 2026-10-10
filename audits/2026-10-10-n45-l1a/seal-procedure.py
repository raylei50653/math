#!/usr/bin/env python3
"""One-time local seal builder. Replays use checker.py, never this writer."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
if (HERE / "delivery.json").exists():
    raise SystemExit("refusing to overwrite a completed delivery")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def jwrite(p, data):
    (HERE / p).write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def run(seed, unsealed):
    env = dict(os.environ)
    if seed is None:
        env.pop("PYTHONHASHSEED", None)
    else:
        env["PYTHONHASHSEED"] = str(seed)
    argv = [sys.executable, "-B", str(HERE / "checker.py")]
    if unsealed:
        argv.append("--unsealed")
    result = subprocess.run(argv, capture_output=True, env=env)
    return result, {"argv": argv, "PYTHONHASHSEED": seed, "actual_exit": result.returncode,
                    "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr)}


(HERE / "preseal").mkdir()
pre_records = []
pre_results = []
for label, seed in [("normal", None), ("seed17", 17)]:
    result, record = run(seed, True)
    for channel in ["stdout", "stderr"]:
        (HERE / "preseal" / (label + "." + channel + ".log")).write_bytes(getattr(result, channel))
    record["stdout"] = "preseal/" + label + ".stdout.log"
    record["stderr"] = "preseal/" + label + ".stderr.log"
    pre_records.append(record)
    pre_results.append(result)
    if result.returncode != 0:
        raise SystemExit("pre-seal replay failed: " + label)
if pre_results[0].stdout != pre_results[1].stdout:
    raise SystemExit("pre-seal normal/seed17 output differs")
jwrite("checks.json", {"preseal_replays": pre_records, "preseal_normal_seed17_byte_equal": True,
                       "final_sealed_replays": "seal/commands.json",
                       "lake_build": "not run: no Lean change; no claimed new Lean proof",
                       "whole_DocGraph_and_historical_check_docs": "not rerun; existing FAIL preserved",
                       "source_control_evaluation": "not performed; no trigger count"})

receipts = ["seal/normal.stdout.log", "seal/normal.stderr.log", "seal/seed17.stdout.log",
            "seal/seed17.stderr.log", "seal/commands.json"]
(HERE / "seal").mkdir()
for rel in receipts:
    (HERE / rel).write_bytes(b"")
excluded = set(receipts) | {"MANIFEST.sha256", "delivery.json"}
files = sorted(str(p.relative_to(HERE)) for p in HERE.rglob("*") if p.is_file() and not p.is_symlink())
payload = [rel for rel in files if rel not in excluded]
if any(p.is_symlink() for p in HERE.rglob("*")):
    raise SystemExit("unexpected symlink")
manifest = "".join(sha((HERE / rel).read_bytes()) + "  " + rel + "\n" for rel in payload).encode()
(HERE / "MANIFEST.sha256").write_bytes(manifest)

# Bootstrap deterministic expected transcripts, then replace them with actual
# captured transcripts only after exact equality and actual exit checks. The
# completed delivery contains only actual execution metadata and captures.
expected = json.loads(pre_results[0].stdout)
expected["sealed_payload_files"] = len(payload)
expected["sealed_receipt_files"] = len(receipts)
expected_bytes = (json.dumps(expected, ensure_ascii=False, sort_keys=True) + "\n").encode()
for label in ["normal", "seed17"]:
    (HERE / "seal" / (label + ".stdout.log")).write_bytes(expected_bytes)
jwrite("seal/commands.json", {"phase": "bootstrap expected transcripts; not yet actual execution metadata"})
delivery = {"task": "N45-L1A", "base": "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744",
            "manifest_file": "MANIFEST.sha256", "manifest_sha256": sha(manifest),
            "payload_files": len(payload), "symlinks": 0,
            "manifest_scope": "Every regular payload file recursively; exactly the manifest, delivery and five named receipt-bound seal files are excluded.",
            "receipt_bound_files": {rel: sha((HERE / rel).read_bytes()) for rel in receipts},
            "mathematical_verdict": "Six claims hold under the full LOW1 contract only; arbitrary-size conditional paper, not proved by this checker.",
            "writes": "Only this dedicated audit directory; no shared edits, commit, push, PR or child delegation."}
jwrite("delivery.json", delivery)
records = []
for label, seed in [("normal", None), ("seed17", 17)]:
    result, record = run(seed, False)
    if result.returncode != 0 or result.stdout != expected_bytes or result.stderr != b"":
        raise SystemExit("sealed replay failed or differs from deterministic expectation: " + label + "\n" + result.stderr.decode())
    for channel in ["stdout", "stderr"]:
        (HERE / "seal" / (label + "." + channel + ".log")).write_bytes(getattr(result, channel))
    record["stdout"] = "seal/" + label + ".stdout.log"
    record["stderr"] = "seal/" + label + ".stderr.log"
    records.append(record)
jwrite("seal/commands.json", {"phase": "actual sealed checker execution", "commands": records,
                            "normal_seed17_byte_equal": True,
                            "bootstrap_transcripts_replaced_by_actual_capture_after_exit_and_byte_checks": True})
delivery["receipt_bound_files"] = {rel: sha((HERE / rel).read_bytes()) for rel in receipts}
delivery["sealed_replays"] = {"normal_actual_exit": 0, "seed17_actual_exit": 0, "byte_equal": True}
jwrite("delivery.json", delivery)

# Final validation after actual receipt binding. No output file is rewritten.
for label, seed in [("normal", None), ("seed17", 17)]:
    result, record = run(seed, False)
    if result.returncode != 0 or result.stdout != (HERE / "seal" / (label + ".stdout.log")).read_bytes() or result.stderr != b"":
        raise SystemExit("finalized receipt replay failed: " + label + "\n" + result.stderr.decode())
print(json.dumps({"manifest_sha256": delivery["manifest_sha256"], "payload_files": len(payload),
                  "receipt_bound_files": len(receipts), "normal_actual_exit": 0, "seed17_actual_exit": 0,
                  "byte_equal": True, "final_receipt_bound_replays_validated": True}, sort_keys=True))
