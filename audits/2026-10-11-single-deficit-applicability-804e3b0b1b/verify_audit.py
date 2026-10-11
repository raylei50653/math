#!/usr/bin/env python3
"""Exclusive audit seal; replay verifies frozen inputs and every retained output."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "4dd11f422c6fa49265a412085116b088786d0344"
SEAL = HERE / "SEAL.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload():
    rows = []
    for path in sorted(HERE.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"unexpected symlink: {path}")
        if path.is_file() and path != SEAL:
            rows.append({"path": str(path.relative_to(HERE)),
                         "bytes": path.stat().st_size, "sha256": digest(path)})
    return rows


def verify_inputs():
    rows = []
    for name in ("INPUTS.json", "EXTRA-INPUTS-01.json", "EXTRA-INPUTS-02.json"):
        manifest = json.loads((HERE / name).read_text())
        assert manifest["base"] == BASE
        for item in manifest["files"]:
            frozen = HERE / "frozen" / item["path"]
            assert digest(frozen) == item["sha256"], item["path"]
            assert frozen.stat().st_size == item["bytes"], item["path"]
            if item.get("authority_kind", "BASE-tracked") == "BASE-tracked":
                original = subprocess.check_output(
                    ["git", "show", f"{BASE}:{item['path']}"], cwd=ROOT)
                assert hashlib.sha256(original).hexdigest() == item["sha256"], item["path"]
            rows.append(item)
    return rows


def verify_links(expect_new_seal=False):
    paths = ["REPORT.md", "APPLICABILITY.md", "BRIDGES.md", "NEXT-TASK.md",
             "VERIFICATION.md", "theorem_contract/theorem-contract.md",
             "identity_inventory/inventory.md", "literal_controls/controls-report.md"]
    count = 0
    for name in paths:
        path = HERE / name
        for _, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("http:", "https:", "#")):
                continue
            resolved = path.parent / target.split("#")[0]
            if not (expect_new_seal and resolved == SEAL):
                assert resolved.exists(), (name, target)
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--seal", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--seed17", action="store_true")
    args = parser.parse_args()
    inputs = verify_inputs()
    links = verify_links(args.seal)
    inventory = json.loads((HERE / "identity_inventory/inventory.json").read_text())
    assert inventory["base"] == BASE
    assert inventory["no_actual_source_supplied"] is True
    assert inventory["new_unconditional_source_exclusions"] == 0
    assert len(inventory["rows"]) == 17
    for row in inventory["rows"]:
        assert row["actual_source"] == "unknown"
        assert row["finite_control"] == "not triggered"
    command = [sys.executable, "-B", str(HERE / "literal_controls/check_literal_controls.py"), "--check"]
    if args.seed17:
        command += ["--seed", "17"]
    control = subprocess.run(command, capture_output=True, text=True, check=True)
    actual = payload()
    if args.seal:
        record = {"schema": "single-deficit-applicability-seal-v1", "base": BASE,
                  "scope": "All regular payload including frozen and retired generations; only this exact SEAL.json excluded.",
                  "source_exclusions_unconditional": 0, "A_status": "conditional",
                  "inputs": len(inputs), "payload": actual}
        with SEAL.open("x") as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    else:
        expected = json.loads(SEAL.read_text())
        assert expected["base"] == BASE
        assert actual == expected["payload"], "payload differs from exclusive seal"
    print(json.dumps({"status": "PASS", "input_files": len(inputs),
                      "payload_files": len(actual), "local_links": links,
                      "identity_rows": 17, "A": "conditional",
                      "literal_controls": json.loads(control.stdout)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
