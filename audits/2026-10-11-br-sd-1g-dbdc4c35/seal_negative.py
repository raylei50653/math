#!/usr/bin/env python3
"""Replay custody negatives without writing files or changing the original seal."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
SEAL = AUDIT / "SEAL.json"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()


def run(submitted):
    # Linux anonymous in-memory file; no persistent file enters/leaves custody.
    descriptor = os.memfd_create("br-sd-1g-negative", flags=0)
    try:
        os.write(descriptor, json.dumps(submitted).encode())
        os.lseek(descriptor, 0, os.SEEK_SET)
        argv = [sys.executable, "-B", str(AUDIT / "verify.py"), "--check",
                "--seal-path", f"/proc/self/fd/{descriptor}"]
        return subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                              pass_fds=(descriptor,))
    finally:
        os.close(descriptor)


def main():
    original = SEAL.read_bytes()
    template = json.loads(original)
    cases = []
    value = copy.deepcopy(template)
    value["claim"] = "unconditional parent closure"
    cases.append(("claim drift", value))
    value = copy.deepcopy(template)
    value["extra_unreviewed_claim"] = True
    cases.append(("extra metadata key", value))
    value = copy.deepcopy(template)
    value["payloads"][0]["sha256"] = "0" * 64
    value["payload_manifest_sha256"] = hashlib.sha256(canonical(value["payloads"])).hexdigest()
    cases.append(("changed payload hash with coherent manifest digest", value))
    value = copy.deepcopy(template)
    value["payloads"].pop()
    value["payload_manifest_sha256"] = hashlib.sha256(canonical(value["payloads"])).hexdigest()
    cases.append(("omitted payload with coherent manifest digest", value))
    records = []
    for name, value in cases:
        result = run(value)
        if result.returncode != 1 or "seal corruption" not in result.stderr:
            raise ValueError(f"unexpected negative result {name}: {result.returncode} {result.stderr}")
        records.append({"control": name, "actual_exit_code": result.returncode,
                        "expected_exit_code": 1, "stderr": result.stderr.strip()})
    result = subprocess.run([sys.executable, "-B", str(AUDIT / "verify.py"), "--seal"],
                            cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 1 or "File exists" not in result.stderr:
        raise ValueError(f"exclusive-create negative failed: {result.stderr}")
    records.append({"control": "exclusive-create refuses an existing seal", "actual_exit_code": 1,
                    "expected_exit_code": 1, "stderr": result.stderr.strip()})
    if SEAL.read_bytes() != original:
        raise ValueError("negative control altered original seal")
    print(json.dumps({"status": "triggered and holds", "controls": records,
                      "seal_bytes_unchanged": True, "disk_writes": 0,
                      "actual_source_status": "not triggered"}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
