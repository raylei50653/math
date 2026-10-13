#!/usr/bin/env python3
"""Verify frozen authority; record live routing drift without editing inputs."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ROUTING = {"docs/tasks/c5_no4ct_handoff.md"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    inputs = json.loads((HERE / "INPUTS.json").read_text())
    rows = []
    for entry in inputs["files"]:
        path = entry["path"]
        frozen = digest(HERE / "frozen" / path)
        live = digest(ROOT / path)
        assert frozen == entry["sha256"], "frozen authority drift: " + path
        assert (HERE / "frozen" / path).stat().st_size == entry["bytes"]
        routing = path in ROUTING
        if not routing:
            assert live == frozen, "live mathematical input drift: " + path
        rows.append({"path": path, "role": "mutable routing snapshot" if routing else "mathematical authority",
                     "frozen_sha256": frozen, "live_sha256": live,
                     "frozen_drift": False, "live_drift": live != frozen})
    return {"base": inputs["base"], "frozen_inputs": len(rows), "frozen_drift": 0,
            "live_mathematical_drift": 0,
            "live_routing_drift": sum(r["live_drift"] for r in rows if r["role"] == "mutable routing snapshot"),
            "policy": "All proofs and controls use frozen bytes. Live handoff is a concurrently maintained routing document; its changes are recorded, not adopted or overwritten.",
            "files": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = calculate()
    if args.write:
        with (HERE / "INPUT_DRIFT.json").open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
