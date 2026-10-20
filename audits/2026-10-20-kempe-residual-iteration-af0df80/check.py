#!/usr/bin/env python3
"""Read-only replay of exact residual iteration and safe phase controls."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def main():
    inputs = json.loads((HERE / "INPUTS.json").read_text())
    for item in inputs:
        if sha256((HERE / item["frozen"]).read_bytes()).hexdigest() != item["sha256"]:
            raise SystemExit("FAIL: frozen input drift: " + item["frozen"])
    commands = [
        ["experiment/check.py", "--check"],
        ["experiment/check.py", "--negative-controls"],
        ["review/check_residual.py", "--check"],
        ["review/compare_residual_phase.py", "--check"],
        ["phase.py", "--check"],
        ["probe.py", "--check"],
        ["review/check_probe.py", "--check", "--compare-root"],
    ]
    for relative, *args in commands:
        p = subprocess.run([sys.executable, "-B", str(HERE / relative), *args],
                           cwd=HERE, text=True, capture_output=True)
        if p.returncode:
            print(p.stdout)
            print(p.stderr, file=sys.stderr)
            raise SystemExit(f"FAIL: {relative}: {p.returncode}")
        print("PASS:", relative, " ".join(args))
    print(f"PASS: {len(inputs)} frozen inputs; fixed cell95 only; J1 not triggered.")


if __name__ == "__main__":
    main()
