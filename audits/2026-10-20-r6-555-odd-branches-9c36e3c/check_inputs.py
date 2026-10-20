#!/usr/bin/env python3
"""Read-only verification of the initial and supplemental frozen authority."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = "9c36e3c4789dfec07d60ec4e042f0bafe17451d1"
MANIFESTS = {
    "INPUTS.json": "ec81ee36dae252eda43530fc39bafff17185b6d91aac31c42ef23aac9343c9a9",
    "INPUTS-supplemental.json": "d45f657128b91326387c7db8d60eec8ae29eebcb722e4f68276d951eb9e040cf",
}
ROUTING = {"README.md", "docs/HANDOFF.md", "docs/STATUS.md",
           "docs/c5_kempe_guide.md", "docs/DOCUMENTATION.md"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(initial):
    rows = []
    for name, expected in MANIFESTS.items():
        path = initial if name == "INPUTS.json" else HERE / name
        if digest(path) != expected:
            raise ValueError(f"authority manifest changed: {name}")
        data = json.loads(path.read_text())
        if name == "INPUTS.json" and data["base"] != BASE:
            raise ValueError("Git BASE changed")
        rows.extend(data["inputs"])
    subprocess.run(["git", "cat-file", "-e", f"{BASE}^{{commit}}"],
                   cwd=REPO, check=True, capture_output=True)
    paths = [row["path"] for row in rows]
    actual = sorted(str(p.relative_to(HERE / "frozen"))
                    for p in (HERE / "frozen").rglob("*") if p.is_file())
    if len(paths) != 81 or len(set(paths)) != len(paths) or sorted(paths) != actual:
        raise ValueError("frozen authority coverage changed")
    routing_drift = []
    for row in rows:
        frozen = HERE / "frozen" / row["path"]
        live = REPO / row["path"]
        if frozen.stat().st_size != row["bytes"] or digest(frozen) != row["sha256"]:
            raise ValueError(f"frozen input changed: {row['path']}")
        if digest(live) != row["sha256"]:
            if row["path"] not in ROUTING:
                raise ValueError(f"immutable predecessor changed: {row['path']}")
            routing_drift.append(row["path"])
    return {"base": BASE, "frozen_inputs": len(rows), "immutable_drift": [],
            "permitted_routing_drift": sorted(routing_drift)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE / "INPUTS.json")
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.inputs), indent=2, sort_keys=True))
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"REJECTED: {error}")
