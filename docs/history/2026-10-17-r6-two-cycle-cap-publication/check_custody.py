#!/usr/bin/env python3
"""Read-only publication custody; not a verifier of the new paper topology."""

import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = "3d325d7197aa05815c71bedc52c1b253d736c7bb"
INVENTORY_SHA = "665327d53e5e64c507f079601a1947a034c7faf09ffe327faffa6b209863f3f5"
SEAL_SHA = "6be87efb925cc994763545b42c9056c68020d72acc195a7067c18103423c4dba"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    raw = (HERE / "initial-state.json").read_bytes()
    require(sha(raw) == INVENTORY_SHA, "publication inventory changed")
    inventory = json.loads(raw)
    require(inventory["base"] == BASE, "wrong research BASE")
    require(inventory["audit"] == "audits/2026-10-17-r6-two-cycle-cap-3d325d7",
            "wrong research scope")
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
                   cwd=REPO, check=True)
    files = {item["path"]: item for item in inventory["audit_files"]}
    require(len(files) == inventory["audit_file_count"] == 78,
            "missing or duplicate research inventory entry")
    audit = REPO / inventory["audit"]
    actual = {p.relative_to(REPO).as_posix() for p in audit.rglob("*") if p.is_file()}
    require(set(files) == actual, "research audit membership changed")
    for path, item in files.items():
        data = (REPO / path).read_bytes()
        require(len(data) == item["bytes"] and sha(data) == item["sha256"],
                "research bytes changed: " + path)

    seal = audit / "OUTPUTS.sha256"
    require(inventory["research_seal_sha256"] == sha(seal.read_bytes()) == SEAL_SHA,
            "research seal changed")
    entries = {}
    for line in seal.read_text().splitlines():
        digest, path = line.split("  ", 1)
        require(path not in entries, "duplicate research seal entry")
        entries[path] = digest
    snapshots = {item["path"]: item for item in inventory["routing_snapshots"]}
    require(set(snapshots) == {"docs/STATUS.md", "docs/c5_kempe_guide.md"},
            "wrong routing snapshot scope")
    require(len(entries) == 79 and set(entries) ==
            (set(files) - {seal.relative_to(REPO).as_posix()}) | set(snapshots),
            "research seal membership changed")
    require(all(entries[path] == item["sha256"] for path, item in files.items()
                if path != seal.relative_to(REPO).as_posix()),
            "publication inventory and research seal disagree")
    drift = []
    for path, item in snapshots.items():
        data = (HERE / item["snapshot"]).read_bytes()
        require(len(data) == item["bytes"] and sha(data) == item["sha256"] == entries[path],
                "research routing snapshot changed: " + path)
        if sha((REPO / path).read_bytes()) != item["sha256"]:
            drift.append(path)
    require(inventory["allowed_live_routing_drift"] == ["docs/STATUS.md"],
            "wrong authorized routing drift")
    require(set(drift) <= {"docs/STATUS.md"}, "unexpected live routing drift")
    print(json.dumps({"status": "PASS", "base": BASE, "audit_files": len(files),
                      "sealed_entries": len(entries), "research_bytes_unchanged": True,
                      "authorized_routing_drift": drift, "source_realizability": "not triggered",
                      "two_cycle_matching_repair": "OPEN", "joint_positivity": "OPEN",
                      "full319": "OPEN", "new_Lean_theorem": False,
                      "mathematical_proof_verifier": False}, sort_keys=True))


if __name__ == "__main__":
    main()
