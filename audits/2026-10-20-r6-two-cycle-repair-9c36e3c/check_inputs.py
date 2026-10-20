#!/usr/bin/env python3
"""Read-only custody check; this does not certify a mathematical source."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
BASE = "9c36e3c4789dfec07d60ec4e042f0bafe17451d1"
REQUIRED = {
    "docs/DOCUMENTATION.md",
    "docs/HANDOFF.md",
    "docs/STATUS.md",
    "docs/c5_kempe_guide.md",
    "audits/2026-10-17-r6-two-cycle-cap-3d325d7/PROOF.md",
    "audits/2026-10-17-r6-two-cycle-cap-3d325d7/A/PROOF.md",
    "audits/2026-10-17-r6-two-cycle-cap-3d325d7/B/PROOF.md",
    "audits/2026-10-17-r6-two-cycle-cap-3d325d7/C/PROOF.md",
    "audits/2026-10-17-r6-seven-five-repair-5b9a7b3/A/PROOF.md",
    "audits/2026-10-17-r6-active-f-seven-ffea555/PROOF.md",
    "audits/2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md",
    "audits/2026-10-17-r6-active-f-seven-ffea555/C/PROOF.md",
    "audits/2026-10-18-abstraction-bottleneck-9f1fe84/REPORT.md",
}
EXTRA = (
    "audits/2026-10-17-r6-active-f-seven-ffea555/frozen/"
    "audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(row, source, copy):
    data = copy.read_bytes()
    require(len(data) == row["bytes"], f"byte count: {source}")
    require(hashlib.sha256(data).hexdigest() == row["sha256"],
            f"sha256: {source}")
    original = subprocess.check_output(
        ["git", "show", f"{BASE}:{source}"], cwd=REPO
    )
    require(data == original, f"BASE mismatch: {source}")
    if not source.startswith("docs/"):
        require((REPO / source).read_bytes() == original,
                f"immutable live authority drift: {source}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=ROOT / "INPUTS.json")
    args = parser.parse_args()
    manifest = json.loads(args.inputs.read_text())
    require(manifest["base"] == BASE, "wrong BASE")
    rows = manifest["inputs"]
    require(len(rows) == len(REQUIRED), "missing or repeated authority")
    require({row["path"] for row in rows} == REQUIRED,
            "authority paths differ")
    for row in rows:
        require(row["routing"] == row["path"].startswith("docs/"),
                "incorrect routing classification")
        verify(row, row["path"], ROOT / "frozen" / row["path"])
    extra = json.loads((ROOT / "B/INPUTS.json").read_text())
    require(extra["base"] == BASE, "extra input BASE")
    require(len(extra["additional_inputs"]) == 1, "extra authority count")
    row = extra["additional_inputs"][0]
    require(row["source"] == EXTRA, "extra authority path")
    require(row["copy"] == "frozen/j-source-geometry.md", "extra copy path")
    verify(row, EXTRA, ROOT / "B" / row["copy"])
    print(json.dumps({
        "base": BASE,
        "frozen_inputs": len(REQUIRED) + 1,
        "immutable_drift": [],
        "routing_scope": "frozen BASE bytes checked; live documentation may change",
        "source_realizability": "not triggered",
        "authority": "custody only",
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"REJECTED: {error}")
