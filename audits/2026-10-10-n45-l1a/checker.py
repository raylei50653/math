#!/usr/bin/env python3
"""Read-only binding verifier. Mathematical conclusions are paper judgments."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
IDS = ["LOW1-CORE", "LOW1-COMP", "LOW1-JOIN", "LOW1-F", "LOW1-MAP", "LOW1-EXCLUSION"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(sealed):
    inputs = json.loads((HERE / "inputs.json").read_text())
    if inputs["base"] != BASE or inputs["head_at_start"] != BASE:
        raise ValueError("historical BASE binding differs")
    count = 0
    git_count = 0
    for item in inputs["inputs"]:
        frozen = HERE / item["frozen"]
        if not frozen.is_file() or sha(frozen.read_bytes()) != item["sha256"]:
            raise ValueError("frozen input digest differs: " + item["frozen"])
        if item["immutable_live"]:
            source = ROOT / item["source"]
            if not source.is_file() or sha(source.read_bytes()) != item["sha256"]:
                raise ValueError("immutable live input digest differs: " + item["source"])
        if "git_path" in item:
            raw = subprocess.check_output(["git", "show", BASE + ":" + item["git_path"]], cwd=ROOT)
            blob = subprocess.check_output(["git", "rev-parse", BASE + ":" + item["git_path"]], cwd=ROOT).decode().strip()
            if raw != frozen.read_bytes() or blob != item["git_blob"]:
                raise ValueError("BASE Git-object mismatch: " + item["git_path"])
            git_count += 1
        count += 1
    if count != 26 or git_count != 12:
        raise ValueError("required frozen input coverage differs")
    pdf = (HERE / "external/gallai-official.pdf").read_bytes()
    pdf_meta = json.loads((HERE / "external-source-check.json").read_text())
    if sha(pdf) != "50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea" or sha(pdf) != pdf_meta["sha256"]:
        raise ValueError("official PDF binding differs")
    judgment = json.loads((HERE / "independent-judgment.json").read_text())
    if [item["id"] for item in judgment["claims"]] != IDS:
        raise ValueError("required six claim IDs differ")
    if any(item["verdict"] != "holds_under_full_LOW1_contract" or item["additional_premises"] for item in judgment["claims"]):
        raise ValueError("judgment contract differs")
    if judgment["source_controls"] != [] or judgment["new_Lean"] is not False or judgment["scope"] != "N45-S-LOW1 only; original U incidence1 retained entirely":
        raise ValueError("evidence boundary differs")
    result = {"base": BASE, "frozen_inputs": count, "BASE_git_blobs": git_count, "historical_current_pins": 6,
              "claim_ids": IDS, "paper_judgment": "all six hold conditionally", "new_Lean": False,
              "source_controls": [], "mathematical_proof_by_checker": False, "integrity": "PASS"}
    if sealed:
        delivery = json.loads((HERE / "delivery.json").read_text())
        manifest = HERE / delivery["manifest_file"]
        if sha(manifest.read_bytes()) != delivery["manifest_sha256"]:
            raise ValueError("manifest receipt digest differs")
        listed = {}
        for line in manifest.read_text().splitlines():
            digest, rel = line.split("  ", 1)
            target = HERE / rel
            if Path(rel).is_absolute() or ".." in Path(rel).parts or rel in listed:
                raise ValueError("invalid manifest path: " + rel)
            if not target.is_file() or target.is_symlink() or sha(target.read_bytes()) != digest:
                raise ValueError("payload digest differs: " + rel)
            listed[rel] = digest
        excluded = set(delivery["receipt_bound_files"]) | {"MANIFEST.sha256", "delivery.json"}
        actual = {str(p.relative_to(HERE)) for p in HERE.rglob("*") if p.is_file() and not p.is_symlink()} - excluded
        if actual != set(listed) or len(listed) != delivery["payload_files"]:
            raise ValueError("exact payload inventory differs")
        if any(p.is_symlink() for p in HERE.rglob("*")):
            raise ValueError("unexpected symlink")
        for rel, digest in delivery["receipt_bound_files"].items():
            if sha((HERE / rel).read_bytes()) != digest:
                raise ValueError("receipt-bound file digest differs: " + rel)
        result["sealed_payload_files"] = len(listed)
        result["sealed_receipt_files"] = len(delivery["receipt_bound_files"])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unsealed", action="store_true", help="pre-seal input checks only")
    args = parser.parse_args()
    try:
        check(not args.unsealed)
    except (ValueError, OSError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
