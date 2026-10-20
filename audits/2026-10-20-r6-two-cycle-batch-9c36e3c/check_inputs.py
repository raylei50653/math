#!/usr/bin/env python3
"""Read-only custody check of the exact pre-existing worktree evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = "9c36e3c4789dfec07d60ec4e042f0bafe17451d1"
MANIFEST_SHA256 = "313a65d9beb500a9f45171f5f83a568089dbea0a6a682f766d691d76002d1dcd"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(manifest):
    if sha(manifest) != MANIFEST_SHA256:
        raise ValueError("authority manifest differs from frozen initial worktree")
    data = json.loads(manifest.read_text())
    if data["base"] != BASE:
        raise ValueError("incorrect Git BASE")
    subprocess.run(
        ["git", "cat-file", "-e", f"{BASE}^{{commit}}"],
        cwd=REPO, check=True, capture_output=True,
    )
    rows = data["inputs"]
    paths = [row["path"] for row in rows]
    actual = sorted(str(p.relative_to(HERE / "frozen"))
                    for p in (HERE / "frozen").rglob("*") if p.is_file())
    if len(rows) != 104 or len(paths) != len(set(paths)) or sorted(paths) != actual:
        raise ValueError("incomplete or additional frozen authority inputs")
    routing_drift = []
    for row in rows:
        frozen, live = HERE / "frozen" / row["path"], REPO / row["path"]
        if frozen.stat().st_size != row["bytes"] or sha(frozen) != row["sha256"]:
            raise ValueError(f"frozen input drift: {row['path']}")
        if sha(live) != row["sha256"]:
            if row["routing"]:
                routing_drift.append(row["path"])
            else:
                raise ValueError(f"immutable live input drift: {row['path']}")
    return {
        "base": BASE,
        "authority_origin": "initial worktree, including uncommitted prior audit",
        "frozen_inputs": len(rows),
        "immutable_drift": [],
        "permitted_routing_drift": sorted(routing_drift),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE / "INPUTS.json")
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.inputs), indent=2, sort_keys=True))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"REJECTED: {error}")
