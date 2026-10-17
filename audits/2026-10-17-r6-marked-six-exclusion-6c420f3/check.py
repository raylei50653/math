#!/usr/bin/env python3
"""Read-only source custody and marked-switch arithmetic, not a topology proof."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys

AUDIT = Path(__file__).resolve().parent
REPO = AUDIT.parent.parent
BASE = "6c420f3ca77d60952ed76f93dff7449c522715ca"
MANIFESTS = {
    "INPUTS.json": "e9291b649f1ad317f72f693ad72cab3594c268901e311a2e62a9bb39599ea77d",
    "ADDITIONAL_INPUTS.json": "3a3d5a622cd9feca178750254ca6c22c57083bc57e227041f763d8152d7c2324",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def reconstruct():
    entries = []
    for name, digest in MANIFESTS.items():
        raw = (AUDIT / name).read_bytes()
        require(sha(raw) == digest, "changed input manifest: " + name)
        manifest = json.loads(raw)
        require(manifest["base"] == BASE, "wrong BASE")
        entries.extend(manifest["entries"])
    require(len(entries) == len({e["path"] for e in entries}) == 22,
            "missing or repeated authority input")
    for item in entries:
        require(item["frozen_path"] == "frozen/" + item["path"], "wrong frozen path")
        frozen = (AUDIT / item["frozen_path"]).read_bytes()
        original = subprocess.check_output(["git", "show", BASE + ":" + item["path"]], cwd=REPO)
        require(sha(frozen) == item["sha256"] and frozen == original,
                "frozen input is not the BASE object: " + item["path"])
        if not item["routing"]:
            require((REPO / item["path"]).read_bytes() == frozen,
                    "live mathematical input changed: " + item["path"])

    switches = []
    for start in ((1, 1, 0), (1, 0, 1), (1, 1, 1)):
        valid = []
        for flip in itertools.product((0, 1), repeat=3):
            end = tuple(a ^ b for a, b in zip(start, flip))
            in_joint = end in ((1, 1, 0), (1, 0, 1))
            required = flip[0] == 0 and ((flip[1] == flip[2]) if start != (1, 1, 1)
                                        else (flip[1] != flip[2]))
            require(in_joint == required, "wrong joint switch contract")
            if in_joint:
                valid.append({"flip": list(flip), "end": list(end)})
        switches.append({"start": list(start), "joint_switches": valid})
    return {
        "base": BASE,
        "manifest_sha256": MANIFESTS,
        "frozen_inputs_checked_against_git": len(entries),
        "frozen_input_drift": [],
        "live_mathematical_input_drift": [],
        "joint_switch_table": switches,
        "scope": "custody and XOR arithmetic only; original topology is PROOF.md",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path)
    action.add_argument("--check", type=Path, nargs="?",
                        const=AUDIT / "certificate.json")
    args = parser.parse_args()
    try:
        result = reconstruct()
        if args.write:
            with args.write.open("x") as output:
                json.dump(result, output, indent=2, sort_keys=True)
                output.write("\n")
        if args.check:
            require(json.loads(args.check.read_text()) == result, "certificate mismatch")
        print("PASS: 22 BASE inputs; zero mathematical drift; joint switch table exact")
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
