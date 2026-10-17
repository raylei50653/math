#!/usr/bin/env python3
"""Verify sealed research bytes after the authorized publication routing update."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
AUDIT = REPO / "audits/2026-10-17-r6-marked-six-exclusion-6c420f3"
BASE = "6c420f3ca77d60952ed76f93dff7449c522715ca"
SEAL = "948d3f87c9587accb03c279b57cb4abe6e9050674587f3c774b636bcb318904b"
ROUTES = {"docs/STATUS.md", "docs/c5_kempe_guide.md", "docs/c5_c4_triangle_core.md"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    initial = json.loads((HERE / "initial-state.json").read_text())
    require(initial["base"] == BASE, "wrong research BASE")
    require(initial["allowed_live_routing_drift"] == ["docs/STATUS.md"], "wrong routing scope")
    require(digest((AUDIT / "SHA256SUMS").read_bytes()) == SEAL, "research seal changed")
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=REPO, check=True)
    files = initial["audit_files"]
    require(len(files) == len({r["path"] for r in files}) == 81, "wrong audit inventory")
    require({str(p.relative_to(REPO)) for p in AUDIT.rglob("*") if p.is_file()}
            == {r["path"] for r in files}, "audit membership changed")
    for row in files:
        raw = (REPO / row["path"]).read_bytes()
        require(len(raw) == row["bytes"] and digest(raw) == row["sha256"],
                "audit identity changed: " + row["path"])

    snapshots = {r["path"]: r for r in initial["routing_snapshots"]}
    require(set(snapshots) == ROUTES, "wrong research-delivery routing snapshot set")
    drift = []
    for path, row in snapshots.items():
        require(digest((HERE / row["snapshot"]).read_bytes()) == row["sha256"],
                "research-delivery snapshot changed: " + path)
        if digest((REPO / path).read_bytes()) != row["sha256"]:
            drift.append(path)
    require(set(drift) <= {"docs/STATUS.md"}, "unauthorized live routing drift")

    lines = (AUDIT / "SHA256SUMS").read_text().splitlines()
    require(len(lines) == 83, "wrong research seal membership")
    for line in lines:
        expected, path = line.split("  ", 1)
        source = HERE / snapshots[path]["snapshot"] if path in snapshots else REPO / path
        require(digest(source.read_bytes()) == expected, "sealed bytes changed: " + path)
    subprocess.run(["python3", "-B", str(AUDIT / "check.py"), "--check"],
                   cwd=REPO, check=True, stdout=subprocess.PIPE)
    print(json.dumps({"status": "PASS", "research_base": BASE, "audit_files": 81,
                      "sealed_entries": 83, "authority_inputs": 22,
                      "research_bytes_unchanged": True, "authorized_live_routing_drift": drift,
                      "source_positivity": "OPEN", "mathematical_proof_verifier": False}, sort_keys=True))


if __name__ == "__main__":
    main()
