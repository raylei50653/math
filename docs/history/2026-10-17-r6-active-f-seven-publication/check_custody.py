#!/usr/bin/env python3
"""Read-only custody of the sealed active-f seven-cap research delivery."""

import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = "ffea555fc2a896d8166ce198ca28ed9262912f25"
INVENTORY_SHA = "97f1bd0a0dfaac172ba26b574c7ec3cee7637365c9af7acc419ea87043170967"
SEAL_SHA = "1db8007964989b7a31c633bac59c8f283f36c5df11168467f1dd066e42ff9659"


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
    audit = REPO / inventory["audit"]
    require(inventory["audit"] == "audits/2026-10-17-r6-active-f-seven-ffea555",
            "wrong research scope")
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
                   cwd=REPO, check=True)
    files = {item["path"]: item for item in inventory["audit_files"]}
    require(len(files) == inventory["audit_file_count"] == 77,
            "missing or duplicate research inventory entry")
    actual = {path.relative_to(REPO).as_posix()
              for path in audit.rglob("*") if path.is_file()}
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
    require(set(entries) == set(files) - {seal.relative_to(REPO).as_posix()},
            "research seal membership changed")
    require(all(files[path]["sha256"] == digest for path, digest in entries.items()),
            "publication inventory and research seal disagree")

    snapshots = {item["path"]: item for item in inventory["routing_snapshots"]}
    require(set(snapshots) == {"docs/STATUS.md", "docs/c5_kempe_guide.md"},
            "wrong routing snapshot scope")
    drift = []
    for path, item in snapshots.items():
        data = (HERE / item["snapshot"]).read_bytes()
        require(len(data) == item["bytes"] and sha(data) == item["sha256"],
                "research routing snapshot changed: " + path)
        if sha((REPO / path).read_bytes()) != item["sha256"]:
            drift.append(path)
    require(inventory["allowed_live_routing_drift"] == ["docs/STATUS.md"],
            "wrong authorized routing drift")
    require(set(drift) <= {"docs/STATUS.md"}, "unexpected live routing drift")
    print(json.dumps({"status": "PASS", "base": BASE, "audit_files": len(files),
                      "sealed_entries": len(entries), "research_bytes_unchanged": True,
                      "authorized_routing_drift": drift,
                      "separating_reference_existence": "OPEN",
                      "joint_positivity": "OPEN", "full319": "OPEN",
                      "mathematical_proof_verifier": False}, sort_keys=True))


if __name__ == "__main__":
    main()
