#!/usr/bin/env python3
"""Read-only replay of frozen inputs and the fixed three-observer experiment."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def main():
    inputs = json.loads((HERE / "INPUTS.json").read_text())
    for item in inputs:
        actual = sha256((HERE / item["frozen"]).read_bytes()).hexdigest()
        if actual != item["sha256"]:
            raise SystemExit("FAIL: frozen input drift: " + item["frozen"])
    commands = [
        ["experiment/check.py", "--check"],
        ["experiment/check.py", "--negative-controls"],
        ["review/check_independent.py", "--check"],
        ["review/compare_certificates.py", "--check"],
        ["theory/check.py"],
        ["coupling.py", "--check"],
        ["frozen/audits/2026-10-20-joint-kempe-state-1148ce0/review/check_collision.py", "check"],
    ]
    for relative, *args in commands:
        completed = subprocess.run(
            [sys.executable, "-B", str(HERE / relative), *args],
            cwd=HERE, capture_output=True, text=True,
        )
        if completed.returncode:
            print(completed.stdout)
            print(completed.stderr, file=sys.stderr)
            raise SystemExit(f"FAIL: {relative}: {completed.returncode}")
        print("PASS:", relative, " ".join(args))
    print(f"PASS: {len(inputs)} frozen inputs; fixed graph only; J1 not triggered.")


if __name__ == "__main__":
    main()
