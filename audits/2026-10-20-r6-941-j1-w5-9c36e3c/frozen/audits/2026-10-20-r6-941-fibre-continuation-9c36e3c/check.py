#!/usr/bin/env python3
"""Read-only replay of this connected conditional fibre increment."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

D = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seal", type=Path, default=D / "OUTPUTS.json")
    args = ap.parse_args()
    inputs = json.loads((D / "INPUTS.json").read_text())
    for row in inputs:
        actual = hashlib.sha256((D / "frozen" / row["path"]).read_bytes()).hexdigest()
        assert actual == row["sha256"], ("frozen input drift", row["path"])
    for row in json.loads(args.seal.read_text()):
        actual = hashlib.sha256((D / row["path"]).read_bytes()).hexdigest()
        assert actual == row["sha256"], ("sealed output drift", row["path"])
    commands = [
        "transport/check.py",
        "geometry/check.py",
        "review/check.py",
        "review/j2_transport.py",
        "review/closure.py",
        "right_cap/probe.py",
    ]
    results = []
    for relative in commands:
        run = subprocess.run([sys.executable, "-B", str(D / relative)],
                             capture_output=True, text=True)
        if run.returncode:
            raise RuntimeError(relative + "\n" + run.stdout + run.stderr)
        results.append({"checker": relative, "result": json.loads(run.stdout)})
    print(json.dumps({"status": "PASS", "frozen_inputs": len(inputs),
                      "results": results, "J1_zero_targets": 2,
                      "J2_zero_targets": 6, "last_rejection": "OPEN",
                      "source_realized": False, "new_Lean": False},
                     sort_keys=True))


if __name__ == "__main__":
    main()
