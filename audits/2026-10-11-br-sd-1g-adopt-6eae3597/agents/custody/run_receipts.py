#!/usr/bin/env python3
"""Replay read-only custody entries and preserve stdout/stderr separately."""
from pathlib import Path
import hashlib
import json
import subprocess
import time
import argparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
COMMANDS = [
    ("publication-normal", ["python3", "-B", "audits/2026-10-11-br-sd-1g-publication/verify.py", "--check", "--require-tracked"], 1),
    ("publication-hashseed17", ["env", "PYTHONHASHSEED=17", "python3", "-B", "audits/2026-10-11-br-sd-1g-publication/verify.py", "--check", "--require-tracked"], 1),
    ("original-fresh-check", ["python3", "-B", "audits/2026-10-11-br-sd-1g-dbdc4c35/verify.py", "--check"], 1),
    ("independent-immutable-check", ["python3", "-B", str(HERE / "independent_immutable_check.py")], 0),
    ("independent-immutable-hashseed17", ["env", "PYTHONHASHSEED=17", "python3", "-B", str(HERE / "independent_immutable_check.py")], 0),
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    if not args.label.replace("-", "").isalnum():
        raise ValueError("label must contain letters, numbers, or hyphens")
    records = []
    for name, argv, expected in COMMANDS:
        started = time.time()
        result = subprocess.run(argv, cwd=ROOT, capture_output=True)
        row = {"id": name, "argv": argv, "cwd": str(ROOT), "expected_exit_code": expected,
               "exit_code": result.returncode, "started_unix": started,
               "wall_seconds": time.time() - started}
        for field in ("stdout", "stderr"):
            data = getattr(result, field)
            path = HERE / (args.label + "-" + name + "." + field + ".log")
            with path.open("xb") as stream:
                stream.write(data)
            row[field + "_path"] = path.relative_to(HERE).as_posix()
            row[field + "_sha256"] = hashlib.sha256(data).hexdigest()
            row[field + "_bytes"] = len(data)
        records.append(row)
        print(json.dumps({"id": name, "exit_code": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr.decode()}, ensure_ascii=False))
    with (HERE / (args.label + "-COMMAND_RECEIPTS.json")).open("x") as stream:
        json.dump(records, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
    if any(row["exit_code"] != row["expected_exit_code"] for row in records):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
