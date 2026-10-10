#!/usr/bin/env python3
"""Read-only verification of the named dispatch inputs, not mathematical claims."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    index = json.loads((ROOT / "inputs.json").read_text())
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
    ).strip()
    if head != index["BASE"]:
        raise ValueError("BASE/HEAD drift")
    rows = []
    for row in index["inputs"]:
        frozen = ROOT / row["frozen"]
        if digest(frozen.read_bytes()) != row["sha256"]:
            raise ValueError("frozen input drift: " + row["path"])
        if row["layer"] == "base":
            data = subprocess.check_output(
                ["git", "show", index["BASE"] + ":" + row["path"]], cwd=REPO
            )
        elif row["layer"] == "current":
            data = (REPO / row["path"]).read_bytes()
        else:
            raise ValueError("unknown input layer")
        if digest(data) != row["sha256"]:
            raise ValueError("named input drift: " + row["path"])
        rows.append({"path": row["path"], "layer": row["layer"], "sha256": row["sha256"]})
    print(json.dumps({"BASE": head, "named_inputs": rows, "scope": "dispatch input integrity only"}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
