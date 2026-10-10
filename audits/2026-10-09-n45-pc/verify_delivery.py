#!/usr/bin/env python3
"""Read-only output links, authored whitespace, inputs and sealed inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

HOME = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify(preseal=False):
    problems = []
    for p in sorted(HOME.glob("*.py")) + [HOME / "REPORT.md", HOME / "SOURCE_SCHEMA.md"]:
        for i, line in enumerate(p.read_text().splitlines(), 1):
            if line.rstrip() != line:
                problems.append(f"{p.name}:{i}: trailing whitespace")
    links, pending = 0, []
    planned = {"checks.json", "MANIFEST.sha256", "delivery.json"} if preseal else set()
    for p in (HOME / "REPORT.md", HOME / "SOURCE_SCHEMA.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", p.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            links += 1
            if not (p.parent / target).exists():
                if target in planned:
                    pending.append(target)
                else:
                    problems.append(f"{p.name}: missing local link {target}")
    before = json.loads((HOME / "read-only-before.json").read_text())
    for item in before:
        p = Path(item["path"])
        if sha(p) != item["sha256"] or p.stat().st_mtime_ns != item["mtime_ns"]:
            problems.append("read-only fingerprint drift: " + item["path"])
    history = json.loads((HOME / "historical-inputs.json").read_text())
    for item in history["files"]:
        p = HOME / item["copy"]
        original = HOME.parent.parent / item["path"]
        if sha(p) != item["sha256"] or sha(original) != item["sha256"] or original.stat().st_mtime_ns != item["mtime_ns"]:
            problems.append("historical input drift: " + item["path"])
    clean = subprocess.check_output(["git", "-C", str(HOME / "source"), "status", "--porcelain"], text=True)
    if clean:
        problems.append("BASE source checkout is dirty")
    c = json.loads((HOME / "certificate-final-v2.json").read_text())
    if c["checker_sha256"] != sha(HOME / "checker.py") or c["validator_sha256"] != sha(HOME / "validator.py"):
        problems.append("final certificate program hash drift")
    required_exits = {"replay-normal": 0, "replay-seed17": 0, "docs-fresh-base": 1,
                      "docgraph-fresh-formal": 0, "docgraph-whole-shared": 1, "diff-check": 0,
                      "exclusive-certificate-guard": 1, "cli-fixed-missing-LP": 2}
    for name in ("missing-complete-tuple", "wrong-shared-ownership", "stale-source-hash", "wrong-whole-unit-X", "wrong-declared-unit"):
        required_exits["cli-" + name] = 2
    for name, expected in required_exits.items():
        record = json.loads((HOME / "logs" / (name + ".command.json")).read_text())
        if record["exit"] != expected:
            problems.append("unexpected command exit: " + name)
    files = 0
    if not preseal:
        manifest = HOME / "MANIFEST.sha256"
        delivery = json.loads((HOME / "delivery.json").read_text())
        if sha(manifest) != delivery["manifest_sha256"]:
            problems.append("manifest digest differs from delivery")
        inventory = {}
        for line in manifest.read_text().splitlines():
            h, name = line.split("  ", 1)
            if name in inventory:
                problems.append("duplicate inventory path: " + name)
            inventory[name] = h
            p = HOME / name
            if not p.is_file() or sha(p) != h:
                problems.append("sealed inventory drift: " + name)
        actual = {str(p.relative_to(HOME)) for p in HOME.rglob("*") if p.is_file()
                  and str(p.relative_to(HOME)) not in ("MANIFEST.sha256", "delivery.json")}
        if actual != set(inventory):
            problems.append("sealed inventory missing/extra files: " + str(sorted(actual ^ set(inventory))))
        files = len(inventory)
    if problems:
        raise ValueError("\n".join(problems))
    return {"authored_text_and_links": "holds", "local_links": links, "preseal_pending_links": pending,
            "read_only_files_zero_drift": len(before), "historical_input_files": len(history["files"]),
            "source_checkout": "clean BASE", "sealed_files_verified": files,
            "scope": "Delivery integrity only; LP source contract remains not triggered."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preseal", action="store_true")
    args = ap.parse_args()
    print(json.dumps(verify(args.preseal), ensure_ascii=False, sort_keys=True))
