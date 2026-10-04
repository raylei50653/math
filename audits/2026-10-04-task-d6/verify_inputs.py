#!/usr/bin/env python3
"""Check D6 source preservation against all before manifests; read-only inputs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def metadata(path):
    raw = path.read_bytes()
    return {"sha256": sha256(raw).hexdigest(), "bytes": len(raw)}


def verify():
    expected = json.loads((HERE / "sha256_before.json").read_text())
    originals = dict(expected)
    for entry in json.loads((HERE / "scope_history/dependency_manifest_start.json").read_text()):
        recorded = {"sha256": entry["sha256"], "bytes": entry["bytes"]}
        if entry["path"] in originals:
            assert originals[entry["path"]] == recorded
        originals[entry["path"]] = recorded
    current = {rel: metadata(ROOT / rel) for rel in originals}
    drift = [rel for rel in originals if originals[rel] != current[rel]]
    frozen_drift = [rel for rel, m in expected.items()
                    if metadata(HERE / "snapshot" / rel) != m]
    for entry in json.loads((HERE / "scope_history/dependency_manifest_start.json").read_text()):
        rel = entry["path"]
        if metadata(HERE / "scope_history/snapshot" / rel) != originals[rel]:
            frozen_drift.append("scope_history/" + rel)
    status = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True)
    (HERE / "workspace_after.txt").write_text(status)
    before_status = (HERE / "workspace_before.txt").read_text()
    def protected_status(s):
        return [line for line in s.splitlines() if "audits/2026-10-04-task-d6" not in line]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    bad_links, whitespace = [], []
    checked_markdown = 0
    for path in HERE.rglob("*"):
        if not path.is_file() or ".snapshot" in path.relative_to(HERE).parts:
            continue
        if path.suffix in (".md", ".py"):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if line.rstrip() != line:
                    whitespace.append(f"{path.relative_to(HERE)}:{number}")
        if path.suffix != ".md":
            continue
        checked_markdown += 1
        for destination in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in destination or destination.startswith("#"):
                continue
            target = destination.split("#", 1)[0]
            if not (path.parent / target).exists():
                bad_links.append({"file": str(path.relative_to(HERE)), "target": target})
    result = {"unique_original_files_checked": len(originals), "live_input_drift": drift,
              "frozen_input_drift": frozen_drift,
              "protected_git_status_unchanged": protected_status(status) == protected_status(before_status),
              "outside_task_git_status_added": sorted(set(protected_status(status)) - set(protected_status(before_status))),
              "outside_task_git_status_removed": sorted(set(protected_status(before_status)) - set(protected_status(status))),
              "head": head, "branch": branch, "audit_markdown_files_checked": checked_markdown,
              "audit_local_missing_links": bad_links, "audit_whitespace_errors": whitespace,
              "after": current}
    result["passed"] = (not drift and not frozen_drift and not bad_links and not whitespace
                        and head == "ca3870f9b79684c2100480d0dc04523899666928"
                        and branch == "shield-budget-hub-principle")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "sha256_after.json")
    args = parser.parse_args()
    args.output.touch(exist_ok=True)
    result = verify()
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "after"}, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
