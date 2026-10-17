#!/usr/bin/env python3
"""Verify frozen authority custody; this does not check the paper topology."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
BASE = "ffea555fc2a896d8166ce198ca28ed9262912f25"
INPUT_SHA = "19329167af4721afcc277b5c4bf278e30901e0a29e42606a0613920079aa3db9"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(manifest_path):
    raw = manifest_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INPUT_SHA, "input manifest changed")
    manifest = json.loads(raw)
    require(manifest["base"] == BASE, "wrong BASE")
    entries = manifest["inputs"]
    require(len(entries) == len({item["path"] for item in entries}) == 17,
            "missing or duplicate input")
    for item in entries:
        path = item["path"]
        frozen = (HERE / "frozen" / path).read_bytes()
        require(len(frozen) == item["bytes"], "frozen length changed: " + path)
        require(hashlib.sha256(frozen).hexdigest() == item["sha256"],
                "frozen bytes changed: " + path)
        original = subprocess.check_output(["git", "show", BASE + ":" + path],
                                           cwd=REPO)
        require(frozen == original, "input differs from BASE: " + path)
        if not item["routing"]:
            require((REPO / path).read_bytes() == frozen,
                    "live mathematical authority changed: " + path)
    return {"base": BASE, "frozen_inputs_checked": len(entries),
            "frozen_drift": [], "live_mathematical_drift": [],
            "source_realizability": "not triggered",
            "evidence_scope": "custody only; arbitrary-size claims are paper proofs"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE / "INPUTS.json")
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.inputs), sort_keys=True))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
