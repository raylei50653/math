#!/usr/bin/env python3
"""Read-only audit delivery, frozen-authority and current Git check; stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

AUDIT = Path(__file__).resolve().parent
REPO = AUDIT.parent.parent
BASE = "4dd11f422c6fa49265a412085116b088786d0344"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    manifest = AUDIT / "MANIFEST.sha256"
    checked = 0
    for line in manifest.read_text().splitlines():
        digest, name = line.split("  ", 1)
        path = (AUDIT / name).resolve()
        assert path.is_relative_to(AUDIT), "manifest path escapes audit"
        assert sha(path) == digest, f"delivery bytes changed: {name}"
        checked += 1
    inputs = json.loads((AUDIT / "authority/input-hashes.json").read_text())
    for item in inputs:
        path = AUDIT / "authority/base" / item["path"]
        expected = subprocess.check_output(["git", "show", f"{BASE}:{item['path']}"], cwd=REPO)
        assert hashlib.sha256(expected).hexdigest() == item["sha256"]
        assert sha(path) == item["sha256"], f"frozen input changed: {item['path']}"
    initial = json.loads((AUDIT / "initial-receipt.json").read_text())
    drift = [item["path"] for item in initial["tracked_worktree_inputs"]
             if not (REPO / item["path"]).is_file()
             or sha(REPO / item["path"]) != item["sha256"]]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    status = subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=REPO, text=True)
    assert not drift, f"initial tracked worktree drift: {drift}"
    assert head == BASE, "HEAD changed"
    print(json.dumps({"status": "triggered and holds", "claim": "delivery hashes and frozen BASE inputs match; current initial tracked bytes unchanged",
                      "manifest_files_checked": checked, "base_documents_checked": len(inputs),
                      "tracked_input_count": len(initial["tracked_worktree_inputs"]),
                      "tracked_byte_drift": drift, "head": head, "current_git_status": status},
                     ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
