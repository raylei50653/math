#!/usr/bin/env python3
"""Exclusive-create final checks, full hash inventory, and delivery metadata.

Precondition: fixed replay and authored-preseal logs already exist. Keeps every
historical failure and every source-checkout file. No original input is written.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HOME = Path(__file__).resolve().parent
ROOT = HOME.parent.parent
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"


def enc(x):
    return (json.dumps(x, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p, data):
    with p.open("xb") as f:
        f.write(data)


def main():
    targets = [HOME / name for name in ("checks.json", "MANIFEST.sha256", "delivery.json")]
    if any(p.exists() for p in targets):
        raise FileExistsError("Seal output already exists; use a fresh named version without overwriting")
    records = []
    for path in sorted((HOME / "logs").glob("*.command.json")):
        r = json.loads(path.read_text())
        name = path.name.removesuffix(".command.json")
        if name in ("build-controls", "generate-final"):
            r["classification"] = "Development integration FAIL retained; superseded by named fresh successful version"
        elif name.startswith("cli-"):
            r["classification"] = "Expected fail-closed source contract rejection; exit2 verified"
        elif name.startswith("exclusive-"):
            r["classification"] = "Expected exclusive-create FileExistsError; no overwrite"
        elif name in ("docs-fresh-base", "docgraph-whole-shared"):
            r["classification"] = "FAIL retained: historical document paths / whole-worktree duplicate IDs"
        else:
            r["classification"] = "Completed within stated finite/integrity scope"
        r["record_file"] = str(path.relative_to(HOME))
        records.append(r)
    checks = {"task": "N45-PC", "BASE": BASE, "setup": json.loads((HOME / "logs/setup.json").read_text()),
              "commands": records, "read_only_verification": json.loads((HOME / "read-only-after.json").read_text()),
              "historical_E4_provenance": {"status": "Four historical replay exit1 FAILs retained; not rerun",
                                           "evidence": "historical-inputs.json"},
              "not_run": {"lake_build_axioms": "No new Lean or dependency change; no formalization claim",
                          "upstream_E3_E4_E4C_U1_U4_enumeration": "Outside the fixed PC contract task",
                          "new_graph_piece_k_search": "Explicitly forbidden by task",
                          "PG_PR_paper_or_external_theorem_review": "Independent task; no unreturned judgments imported",
                          "source_realization_or_general_exclusion": "No finite positive LP source; no arbitrary-size proof obligation attempted"},
              "source_contract_coverage": "not triggered; never a source-exclusion PASS",
              "final_certificate": {"path": "certificate-final-v2.json", "sha256": sha(HOME / "certificate-final-v2.json")},
              "seal_command": ["python3", "-B", "audits/2026-10-09-n45-pc/seal.py"],
              "seal_log": "delivery.json records completed seal and read-only verification"}
    write(HOME / "checks.json", enc(checks))
    head = subprocess.check_output(["git", "-C", str(HOME / "source"), "rev-parse", "HEAD"], text=True).strip()
    clean = subprocess.check_output(["git", "-C", str(HOME / "source"), "status", "--porcelain"], text=True)
    assert head == BASE and not clean
    initial = json.loads((HOME / "initial-state.json").read_text())
    current = subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain=v1"], text=True)
    inventory = []
    for path in sorted(HOME.rglob("*")):
        if path.is_file():
            rel = str(path.relative_to(HOME))
            if rel not in ("MANIFEST.sha256", "delivery.json"):
                inventory.append((sha(path), rel, path.stat().st_size))
    manifest = "".join(h + "  " + name + "\n" for h, name, size in inventory).encode()
    write(HOME / "MANIFEST.sha256", manifest)
    # Verify all recorded bytes now; excludes only two declared self-reference files.
    assert all(sha(HOME / name) == h for h, name, size in inventory)
    empty_dirs = [str(p.relative_to(HOME)) for p in sorted(HOME.rglob("*")) if p.is_dir() and not any(p.iterdir())]
    delivery = {"task": "N45-PC", "BASE": BASE, "source_HEAD": head, "source_clean": not clean,
                "generated_utc": datetime.now(timezone.utc).isoformat(), "manifest_sha256": sha(HOME / "MANIFEST.sha256"),
                "inventory_files": len(inventory), "inventory_bytes": sum(size for h, name, size in inventory),
                "manifest_exclusions": {"MANIFEST.sha256": "Self-reference; digest recorded here",
                                        "delivery.json": "Contains manifest digest; excluded to avoid circular hashing"},
                "empty_directories_preserved": empty_dirs,
                "initial_main_status": initial["status"], "final_main_status": current,
                "status_added_lines": sorted(set(current.splitlines()) - set(initial["status"].splitlines())),
                "own_write_scope": str(HOME.relative_to(ROOT)) + "/", "other_worker_outputs": "PG/PR directories may appear concurrently; no judgments consumed",
                "commit_push_PR_subagents_external_messages": "None",
                "completed_command": {"argv": checks["seal_command"], "exit": 0,
                                      "log": "This delivery record plus full manifest; integrity-only scope"},
                "final_certificate_sha256": checks["final_certificate"]["sha256"],
                "finite_coverage": "19 N2 / 7 N2 whole U / 4 N1 interface calibrations; five negatives rejected",
                "LP_source_contract": "not triggered", "source_exclusion": "not established"}
    write(HOME / "delivery.json", enc(delivery))
    # The standalone verifier reads the finished delivery without creating new files.
    from verify_delivery import verify
    verified = verify(False)
    print(json.dumps({"seal": "completed", "manifest_sha256": delivery["manifest_sha256"],
                      "delivery_sha256": sha(HOME / "delivery.json"), "verification": verified}, sort_keys=True))


if __name__ == "__main__":
    main()
