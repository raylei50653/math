#!/usr/bin/env python3
"""Read-only BASE and frozen-input custody, not a mathematical proof checker."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=HERE / "INPUTS.json")
    args = parser.parse_args()
    seal = json.loads(args.manifest.read_text())
    assert seal["base"] == "3953c85e334b96533e44652df065640f5463715a"
    assert len(seal["entries"]) == 23
    assert len({row["path"] for row in seal["entries"]}) == 23
    for row in seal["entries"]:
        frozen = (ROOT / row["frozen_path"]).read_bytes()
        assert hashlib.sha256(frozen).hexdigest() == row["sha256"], row["path"]
        assert len(frozen) == row["bytes"], row["path"]
        original = subprocess.check_output(
            ["git", "show", seal["base"] + ":" + row["path"]], cwd=ROOT)
        assert frozen == original, row["path"]
        if not row["path"].startswith("docs/"):
            assert (ROOT / row["path"]).read_bytes() == original, row["path"]
    print("PASS: 23 frozen inputs equal exact BASE; all immutable live inputs unchanged")


if __name__ == "__main__":
    main()
