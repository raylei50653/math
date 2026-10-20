#!/usr/bin/env python3
"""Read-only replay of the joint Kempe state audit and its independent review."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="default; always read-only")
    parser.parse_args()
    inputs = json.loads((HERE / "INPUTS.json").read_text())
    for row in inputs:
        frozen = HERE / "frozen" / row["path"]
        assert frozen.stat().st_size == row["bytes"], row["path"]
        assert digest(frozen) == row["sha256"], row["path"]
        if not row["routing"]:
            assert digest(ROOT / row["path"]) == row["sha256"], row["path"]
    outputs = [
        HERE / "experiment/certificate.json", HERE / "refinement.json",
        HERE / "review/collision_certificate.json", HERE / "review/cross_certificate.json",
    ]
    before = {str(path.relative_to(HERE)): digest(path) for path in outputs}
    checks = [
        ("experiment/check.py", "--check"),
        ("refine.py", "--check"),
        ("review/check_collision.py", "check"),
        ("review/check_cross.py", "check"),
    ]
    for script, mode in checks:
        result = subprocess.run(
            [sys.executable, "-B", str(HERE / script), mode],
            cwd=ROOT, text=True, capture_output=True,
        )
        if result.returncode:
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)
            raise SystemExit(result.returncode)
        print(json.dumps({
            "check": script, "status": "PASS",
            "stdout_sha256": sha256(result.stdout.encode()).hexdigest(),
        }, sort_keys=True))
    after = {str(path.relative_to(HERE)): digest(path) for path in outputs}
    assert before == after, "replay changed evidence"
    print(json.dumps({
        "status": "PASS", "frozen_inputs": len(inputs), "input_drift": 0,
        "read_only_evidence": after, "j1_source_status": "not triggered",
        "scope": "fixed catalogue and fixed cell95; joint summary generally insufficient",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
