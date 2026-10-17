#!/usr/bin/env python3
"""Read-only custody of the sealed seven-defect research delivery."""

import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
AUDIT = REPO / "audits/2026-10-17-r6-seven-five-repair-5b9a7b3"
BASE = "5b9a7b3190c84bc10ff99608e372a9b4be57a0f6"
INITIAL_SHA = "a430c443a82905d416e8f89e54e5dc47ca919594b909ad8fd677cf8024a5467b"
SEAL = "cd2b9911fc4b4383abc5c15453b161423d5fb40d4a6f5932bfd144f095d0eb0a"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    raw = (HERE / "initial-state-v2.json").read_bytes()
    require(sha(raw) == INITIAL_SHA, "publication inventory changed")
    initial = json.loads(raw)
    require(initial["base"] == BASE, "wrong research BASE")
    require(initial["research_seal_sha256"] == SEAL, "wrong research seal")
    require(sha((AUDIT / "SHA256SUMS").read_bytes()) == SEAL, "research seal changed")
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
                   cwd=REPO, check=True)

    inventory = {item["path"]: item for item in initial["audit_files"]}
    require(len(inventory) == initial["audit_file_count"] == 77,
            "research inventory missing or repeated entries")
    actual = {str(path.relative_to(REPO)) for path in AUDIT.rglob("*") if path.is_file()}
    require(set(inventory) == actual, "research audit membership changed")
    for path, item in inventory.items():
        data = (REPO / path).read_bytes()
        require(len(data) == item["bytes"] and sha(data) == item["sha256"],
                "research bytes changed: " + path)

    entries = {}
    for line in (AUDIT / "SHA256SUMS").read_text().splitlines():
        digest, path = line.split("  ", 1)
        require(path not in entries, "duplicate research seal entry")
        entries[path] = digest
    seal_path = str((AUDIT / "SHA256SUMS").relative_to(REPO))
    require(set(entries) == set(inventory) - {seal_path}, "research seal membership changed")
    require(all(inventory[path]["sha256"] == digest for path, digest in entries.items()),
            "inventory and research seal disagree")

    snapshots = {row["path"]: row for row in initial["routing_snapshots"]}
    require(set(snapshots) == {"docs/STATUS.md", "docs/c5_kempe_guide.md"},
            "wrong routing snapshot scope")
    drift = []
    for path, row in snapshots.items():
        require(sha((HERE / row["snapshot"]).read_bytes()) == row["sha256"],
                "research routing snapshot changed")
        if sha((REPO / path).read_bytes()) != row["sha256"]:
            drift.append(path)
    require(initial["allowed_live_routing_drift"] == ["docs/STATUS.md"],
            "wrong authorized routing drift")
    require(set(drift) <= {"docs/STATUS.md"}, "unexpected routing drift")

    policy = json.loads((REPO / "tools/generated_artifact_exceptions.json").read_text())
    large = [item for item in inventory.values()
             if item["bytes"] >= 1_000_000 and Path(item["path"]).suffix == ".json"]
    require(len(large) == 3, "wrong large sealed evidence set")
    for item in large:
        exception = policy["files"][item["path"]]
        require(exception["kind"] == "frozen" and exception["bytes"] == item["bytes"]
                and exception["sha256"] == item["sha256"],
                "large evidence exception changed: " + item["path"])
    print(json.dumps({"status": "PASS", "base": BASE, "audit_files": len(inventory),
                      "sealed_entries": len(entries), "research_bytes_unchanged": True,
                      "authorized_routing_drift": drift, "large_frozen_exceptions": len(large),
                      "three_spoke_case": "PARTIAL", "joint_positivity": "OPEN",
                      "mathematical_proof_verifier": False}, sort_keys=True))


if __name__ == "__main__":
    main()
