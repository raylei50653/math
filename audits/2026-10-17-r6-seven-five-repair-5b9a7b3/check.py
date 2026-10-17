#!/usr/bin/env python3
"""Check BASE custody and reference-batch mark arithmetic, not paper topology."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
BASE = "5b9a7b3190c84bc10ff99608e372a9b4be57a0f6"
INPUT_SHA = "b302612d7f288ee1ef64b66238801bf8b301b89b4dfd77fbae49f64cc4a9e853"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reconstruct():
    raw = (HERE / "INPUTS.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INPUT_SHA, "input manifest changed")
    manifest = json.loads(raw)
    require(manifest["base"] == BASE, "wrong BASE")
    entries = manifest["entries"]
    require(len(entries) == len({item["path"] for item in entries}) == 11,
            "missing or duplicate authority input")
    for item in entries:
        require(item["frozen_path"] == "frozen/" + item["path"], "wrong frozen path")
        frozen = (HERE / item["frozen_path"]).read_bytes()
        require(hashlib.sha256(frozen).hexdigest() == item["sha256"],
                "changed frozen bytes: " + item["path"])
        original = subprocess.check_output(["git", "show", BASE + ":" + item["path"]],
                                           cwd=REPO)
        require(frozen == original, "input differs from BASE: " + item["path"])
        if not item["routing"]:
            require((REPO / item["path"]).read_bytes() == frozen,
                    "live mathematical authority changed: " + item["path"])

    general, reference = [], []
    joint = {(1, 1, 0), (1, 0, 1)}
    for start in sorted(joint):
        for flip in itertools.product((0, 1), repeat=3):
            end = tuple(a ^ b for a, b in zip(start, flip))
            expected = flip[0] == 0 and flip[1] == flip[2]
            require((end in joint) == expected, "wrong general union criterion")
            general.append({"start": start, "flip": flip, "end": end,
                            "union_preserved": expected})
        # The chosen even111 reference differs in exactly the omitted mark.
        omitted = next(i for i, value in enumerate(start) if value == 0)
        for choose_h in (False, True):
            end = tuple(value ^ int(choose_h and i == omitted)
                        for i, value in enumerate(start))
            require((end in joint) == (not choose_h), "wrong H obstruction")
            require(end == ((1, 1, 1) if choose_h else start),
                    "reference batch changed common marks")
            reference.append({"start": start, "choose_H": choose_h, "end": end})
    # Normalize complete certificate types before deterministic comparison.
    return json.loads(json.dumps({
        "base": BASE,
        "input_manifest_sha256": INPUT_SHA,
        "frozen_inputs_checked_against_git": len(entries),
        "frozen_drift": [],
        "live_mathematical_drift": [],
        "general_union_switches": general,
        "reference_batch_switches": reference,
        "source_realizability": "not triggered",
        "evidence_scope": "custody and Boolean arithmetic; paper claims in PROOF.md",
    }, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", type=Path)
    group.add_argument("--check", type=Path, nargs="?", const=HERE / "certificate.json")
    args = parser.parse_args()
    try:
        result = reconstruct()
        if args.write:
            with args.write.open("x") as output:
                json.dump(result, output, indent=2, sort_keys=True)
                output.write("\n")
        if args.check:
            require(json.loads(args.check.read_text()) == result, "certificate mismatch")
        print("PASS: 11 BASE inputs; zero mathematical drift; general and reference marks exact")
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
