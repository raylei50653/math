#!/usr/bin/env python3
"""Independent read-only custody review; stdout only, no target imports or writes."""

import hashlib
import json
from pathlib import Path
import stat
import subprocess


REPO = Path(__file__).resolve().parents[2]
TARGET = REPO / "audits/2026-10-11-n45-s-long-s-t2-q0-restore"
DISPATCH = REPO / "audits/2026-10-11-n45-s-long-s-rfibre-dispatch"
BASE = "f2692089ad4259808e27d9b7e882ac09505b180a"
TASK = "N45-S-LONG-S-T2-Q0-RESTORE"
DELIVERY_SHA = "920a7161ac5c758dea78c45b9360eb00f81bc6f91ea0c39b45e09723e026b349"
MISSING = [
    "artifacts/c5_no_spoke_exterior/observations.json",
    "artifacts/c5_single_spoke_residual_locality/observations.json",
]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    return json.loads(path.read_text())


def digest(path):
    require(stat.S_ISREG(path.lstat().st_mode), f"not a regular file: {path}")
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def declared_digest(record):
    return {key: record[key] for key in ("bytes", "sha256")}


def safe_relative(value):
    path = Path(value)
    require(not path.is_absolute(), f"absolute relative path: {value}")
    require(value == path.as_posix(), f"noncanonical relative path: {value}")
    require(".." not in path.parts and bool(path.parts), f"unsafe relative path: {value}")
    return path


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True)


def tree_inventory():
    require(stat.S_ISDIR(TARGET.lstat().st_mode), "target is not a directory")
    files = {}
    directories = []
    pending = [TARGET]
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            mode = path.lstat().st_mode
            rel = path.relative_to(TARGET).as_posix()
            if stat.S_ISDIR(mode):
                directories.append(rel)
                pending.append(path)
            elif stat.S_ISREG(mode):
                files[rel] = digest(path)
            else:
                raise AssertionError(f"symlink or special target entry: {rel}")
    return {"files": dict(sorted(files.items())), "directories": sorted(directories)}


def main():
    inventory = tree_inventory()
    require(len(inventory["files"]) == 77, "target regular file count mismatch")
    require(len(inventory["directories"]) == 5, "target directory count mismatch")
    delivery = read(TARGET / "delivery.json")
    require(delivery["base"] == BASE and delivery["task_id"] == TASK, "delivery identity mismatch")
    require(delivery["status"] == "待獨立驗收" and delivery["adopted"] is False, "original adoption changed")
    require(digest(TARGET / "delivery.json")["sha256"] == DELIVERY_SHA, "bound delivery SHA mismatch")
    require(delivery["metadata_exclusions"] == ["delivery.json"], "metadata exclusions changed")
    payload = delivery["payload"]
    paths = [record["path"] for record in payload]
    require(len(paths) == len(set(paths)) == 76, "payload duplicate or count mismatch")
    require(set(paths) | {"delivery.json"} == set(inventory["files"]), "payload inventory mismatch")
    require(delivery["payload_files"] == 76, "declared payload count mismatch")
    require(delivery["payload_bytes"] == sum(record["bytes"] for record in payload) == 1665969,
            "declared payload size mismatch")
    for record in payload:
        safe_relative(record["path"])
        require(inventory["files"][record["path"]] == declared_digest(record),
                f"payload digest mismatch: {record['path']}")

    inputs = read(TARGET / "inputs.json")
    pins = read(DISPATCH / "input-pins.json")
    require(inputs["base"] == pins["base"] == BASE, "input BASE mismatch")
    groups = [("BASE_blobs", "BASE Git blob", 12),
              ("sealed_audit_SHA256", "sealed audit physical SHA256", 11)]
    all_input_records = []
    for key, authority, count in groups:
        records = inputs[key]
        require(len(records) == count, f"input group count mismatch: {key}")
        for record in records:
            original = {name: value for name, value in record.items() if name != "dispatch_frozen_path"}
            matched = [p for p in pins["inputs"] if p["path"] == record["path"]]
            require(len(matched) == 1 and matched[0] == original, f"dispatch record mismatch: {record['path']}")
            require(record["authority"] == authority, f"input authority mismatch: {record['path']}")
            expected_frozen = (DISPATCH / safe_relative(record["frozen_path"])).relative_to(REPO).as_posix()
            require(record["dispatch_frozen_path"] == expected_frozen, f"frozen path mismatch: {record['path']}")
            expected = declared_digest(record)
            for name in ("path", "dispatch_frozen_path"):
                require(digest(REPO / safe_relative(record[name])) == expected,
                        f"live/frozen input mismatch: {record[name]}")
            if key == "BASE_blobs":
                data = git("show", BASE + ":" + record["path"])
                blob = git("rev-parse", BASE + ":" + record["path"])
                require(data.returncode == blob.returncode == 0, f"missing admitted BASE blob: {record['path']}")
                observed = {"bytes": len(data.stdout), "sha256": hashlib.sha256(data.stdout).hexdigest()}
                require(observed == expected and blob.stdout.decode().strip() == record["git_blob"],
                        f"BASE content/blob mismatch: {record['path']}")
            else:
                require(record["git_blob"] is None and record["included_in_BASE_claimed"] is False,
                        f"sealed input falsely promoted to BASE: {record['path']}")
            all_input_records.append({"path": record["path"], "authority": authority, **expected})
    require(len(pins["inputs"]) == 23, "dispatch total authority count mismatch")
    require(len({record["path"] for record in all_input_records}) == 23, "duplicate authority input")
    metadata = inputs["dispatch_metadata_SHA256"]
    expected_metadata = {str((DISPATCH / name).relative_to(REPO))
                         for name in ("input-pins.json", "delivery.json", "TASK_B_T2_Q0.md")}
    require(len(metadata) == 3 and {record["path"] for record in metadata} == expected_metadata,
            "dispatch metadata set mismatch")
    for record in metadata:
        require(digest(REPO / safe_relative(record["path"])) == declared_digest(record),
                f"dispatch metadata digest mismatch: {record['path']}")

    before = read(TARGET / "custody-before.json")
    after = read(TARGET / "custody-after.json")
    require(before["base"] == after["base"] == BASE, "custody BASE mismatch")
    require(before["files"] == after["files"] and len(before["files"]) == 60,
            "recorded before/after custody mismatch")
    for path, expected in before["files"].items():
        require(digest(REPO / safe_relative(path)) == expected, f"recorded input/old certificate drift: {path}")
    head = git("rev-parse", "HEAD")
    diff = git("diff", "--binary", "HEAD")
    require(head.returncode == diff.returncode == 0 and head.stdout.decode().strip() == BASE,
            "HEAD identity mismatch")
    require(diff.stdout == b"", "tracked changes detected")
    require(after["same_as_before"] is True and after["zero_input_old_certificate_drift"] is True
            and after["HEAD_and_tracked_diff_unchanged"] is True, "custody attestation field mismatch")

    findings = read(TARGET / "findings.json")
    require(inputs["missing_BASE_blobs"] == findings["findings"], "input/finding list mismatch")
    require(len(findings["findings"]) == 2 and {record["path"] for record in findings["findings"]} == set(MISSING),
            "missing BASE finding set mismatch")
    missing_results = []
    for record in findings["findings"]:
        require(record["BASE_blob_available"] is False and record["exit"] == 128
                and record["physical_or_quarantine_admitted"] is False
                and record["dependent_finite_replay_executed"] is False,
                f"missing BASE trust boundary mismatch: {record['path']}")
        result = git("show", BASE + ":" + record["path"])
        require(result.returncode == 128 and result.stdout == b"", f"missing BASE finding no longer holds: {record['path']}")
        require(b"not in" in result.stderr, f"unexpected missing BASE failure: {record['path']}")
        missing_results.append({"path": record["path"], "exit": result.returncode,
                                "stdout_bytes": 0, "stderr": result.stderr.decode().strip()})

    history = sorted(path for path in inventory["files"] if path.startswith("metadata-initial/"))
    require(len(history) == 16, "retained metadata history count mismatch")
    corrections = read(TARGET / "metadata-corrections.json")
    required_history = {"metadata-initial/claims.json", "metadata-initial/coverage.json",
                        "metadata-initial/checks.json", "metadata-initial/negative-controls/missing-diagonal.json"}
    require(set(corrections["retained_initial_files"]) == required_history, "retained initial metadata list mismatch")
    require(required_history <= set(history), "retained initial metadata missing")
    external = inputs["external_theorem_pins"]
    require(len(external) == 1 and external[0]["git_blob"] is None
            and external[0]["origin_refetched"] is False
            and external[0]["direct_external_theorem_revalidation_executed"] is False,
            "external dependency trust boundary changed")
    require(tree_inventory() == inventory, "target tree changed during read-only custody review")
    print(json.dumps({
        "status": "independent custody checks passed",
        "task_id": TASK, "base": BASE,
        "target_delivery": digest(TARGET / "delivery.json"),
        "payload_files": 76, "payload_bytes": 1665969,
        "metadata_exclusions": ["delivery.json"],
        "target_regular_files": 77, "target_directories": inventory["directories"],
        "target_inventory": inventory["files"],
        "symlink_or_special_entries": [], "missing_or_extra_payload_entries": [],
        "authority_inputs": all_input_records, "dispatch_metadata": metadata,
        "recorded_custody_files": 60, "recorded_input_old_certificate_drift": [],
        "old_certificates": {path: value for path, value in before["files"].items() if "certificate" in path},
        "HEAD": head.stdout.decode().strip(), "tracked_diff_bytes": 0,
        "expected_missing_BASE_blobs": missing_results,
        "retained_historical_metadata_and_logs": history,
        "external_dependency": {"pin": external[0], "fresh_primary_theorem_validation_executed": False},
        "target_checker_executed": False,
        "source_realizability_or_paper_adoption_claimed": False,
        "writes": [],
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
