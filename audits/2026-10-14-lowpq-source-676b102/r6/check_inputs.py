#!/usr/bin/env python3
"""Verify custody only; this does not verify the source-geometry proof."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = "676b1024715f24a0d969fba90baab21b756406e2"
PARENT = "audits/2026-10-14-lowpq-source-676b102/INPUTS.json"
SOURCES = (
    PARENT,
    "audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md",
    "audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md",
    "audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md",
    "audits/2026-10-14-c4-return-branches-a11d4bb/r_high/PROOF.md",
    "audits/2026-10-14-cofacial-fibres-676b102/r6/PROOF.md",
    "audits/2026-10-14-cofacial-fibres-676b102/pq/PROOF.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=HERE / "SOURCE_SEAL.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    seal = json.loads(args.certificate.read_text())
    assert set(seal) == {"base", "scope", "inputs"}, "malformed seal"
    assert seal["base"] == BASE, "BASE mismatch"
    assert seal["scope"] == "Input custody only; no finite mathematical proof claimed"
    assert set(seal["inputs"]) == set(SOURCES), "missing or unexpected direct input"
    for path in SOURCES:
        assert digest(ROOT / path) == seal["inputs"][path], f"input drift: {path}"
    parent = json.loads((ROOT / PARENT).read_text())
    assert parent["base"] == BASE
    for entry in parent["inputs"]:
        if "frozen_path" in entry:
            file = (ROOT / PARENT).parent / entry["frozen_path"]
        else:
            file = ROOT / entry["path"]
        assert digest(file) == entry["sha256"], f"parent input drift: {entry['path']}"
    print(json.dumps({"status": "PASS", "scope": seal["scope"],
                      "direct_inputs": len(SOURCES),
                      "parent_inputs": len(parent["inputs"])}, sort_keys=True))


if __name__ == "__main__":
    main()
