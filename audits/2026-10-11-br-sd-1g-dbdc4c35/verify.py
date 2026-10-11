#!/usr/bin/env python3
"""Read-only BR-SD-1g custody verification; --seal is exclusive-create only.

Custody and accepted-byte checks are not a mathematical theorem verifier.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import runpy
from urllib.parse import unquote, urlsplit

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
BASE = (AUDIT / "BASE").read_text().strip()
REL = AUDIT.relative_to(ROOT).as_posix() + "/"
INPUT_MANIFEST_SHA = "76298c8402372e8664409849c595ef4e6939d21515c62db9f2e7034723be62bd"
OLD_MANIFEST_SHA = "1ff905853232726d72fb3a0c4551cefe894e0f56cf9a4cb89f949362da0c1d8b"
OLD_DIRS = {"audits/2026-10-11-br-sd-1a-0f181045",
            "audits/2026-10-11-br-sd-1c-fd6e1112",
            "audits/2026-10-11-br-sd-1e-337d018b"}
CLAIM = "candidate scoped exclusion; no canonical adoption"
SEAL_KEYS = {"schema", "base", "parent_status", "new_unconditional_closures",
             "claim", "payload_manifest_sha256", "payloads"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()


def run(argv):
    result = subprocess.run(argv, cwd=ROOT, capture_output=True)
    if result.returncode:
        raise ValueError(f"command failed {argv!r}: exit {result.returncode}")
    return result.stdout


def inventory(directory, excluded=()):
    records = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"unexpected symlink: {path}")
        if path.is_file():
            name = path.relative_to(directory).as_posix()
            if name in excluded:
                continue
            data = path.read_bytes()
            records.append({"path": name, "sha256": digest(data),
                            "size": len(data), "mode": path.stat().st_mode & 0o777,
                            "symlink": False})
    return records


def prerequisites(allow_pending_seal=False):
    if run(["git", "rev-parse", "HEAD"]).decode().strip() != BASE:
        raise ValueError("fresh audit HEAD drifted from fixed BASE")
    if run(["git", "rev-parse", "origin/main"]).decode().strip() != BASE:
        raise ValueError("origin/main drifted from fixed BASE")
    # This workflow authorizes no write elsewhere; initial worktree was clean.
    for record in run(["git", "status", "--porcelain=v1", "-z",
                       "--untracked-files=all"]).split(b"\0"):
        if not record:
            continue
        if record[:2] != b"??" or not record[3:].decode().startswith(REL):
            raise ValueError(f"outside write boundary or staged change: {record!r}")
    input_bytes = (AUDIT / "authority/INPUTS.json").read_bytes()
    if digest(input_bytes) != INPUT_MANIFEST_SHA:
        raise ValueError("fixed initial authority manifest drift")
    inputs = json.loads(input_bytes)
    if inputs["base"] != BASE or len(inputs["inputs"]) != 31:
        raise ValueError("authority BASE mismatch")
    for record in inputs["inputs"]:
        frozen = AUDIT / record["frozen"]
        blob = run(["git", "show", BASE + ":" + record["path"]])
        live = ROOT / record["path"]
        if (digest(blob) != record["sha256"] or len(blob) != record["size"]
                or frozen.read_bytes() != blob or live.read_bytes() != blob):
            raise ValueError(f"authority drift: {record['path']}")
    old_bytes = (AUDIT / "authority/OLD-CUSTODY.json").read_bytes()
    if digest(old_bytes) != OLD_MANIFEST_SHA:
        raise ValueError("fixed initial old-custody manifest drift")
    old = json.loads(old_bytes)
    old_dirs = sorted({"/".join(x["path"].split("/")[:2]) for x in old})
    if len(old) != 313 or set(old_dirs) != OLD_DIRS:
        raise ValueError("incomplete original three-audit custody coverage")
    observed = []
    for name in old_dirs:
        for record in inventory(ROOT / name):
            observed.append({**record, "path": name + "/" + record["path"]})
    if sorted(observed, key=lambda x: x["path"]) != sorted(old, key=lambda x: x["path"]):
        raise ValueError("old 1a/1c/1e custody inventory drift")
    acceptance = json.loads((AUDIT / "agents/paper/ACCEPTANCE.json").read_text())
    if (acceptance["base"] != BASE or acceptance["verdict"] != "accepted scoped paper exclusion"
            or acceptance["parent_status"] != "OPEN"
            or acceptance["new_unconditional_closures"] != 0):
        raise ValueError("independent acceptance scope mismatch")
    if set(acceptance["accepted_hashes"]) != {"PROOF.md", "MAPPING.md", "REPORT.md"}:
        raise ValueError("incomplete exact-byte paper acceptance")
    for path, expected in acceptance["accepted_hashes"].items():
        if digest((AUDIT / path).read_bytes()) != expected:
            raise ValueError(f"reviewed bytes drift: {path}")
    checks = json.loads((AUDIT / "logs/CHECKS.json").read_text())
    if not checks or any(x["exit_code"] != x["expected_exit_code"] for x in checks):
        raise ValueError("missing or failing recorded checks")
    for record in checks:
        for field in ("stdout", "stderr"):
            if digest((AUDIT / record[field + "_path"]).read_bytes()) != record[field + "_sha256"]:
                raise ValueError("recorded check output hash mismatch")
    helper = runpy.run_path(str(ROOT / "scripts/check_docs.py"), run_name="audit_link_helper")
    link_count = 0
    for path in sorted(AUDIT.rglob("*.md")):
        if "authority" in path.relative_to(AUDIT).parts:
            continue  # frozen documents keep historical relative-link context
        for line, destination in helper["links"](path.read_text()):
            url = urlsplit(destination)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.exists():
                if allow_pending_seal and target == AUDIT / "SEAL.json" and not url.fragment:
                    continue  # --seal creates only this planned target after prerequisites
                raise ValueError(f"missing local link {path}:{line}: {destination}")
            if url.fragment and target.suffix == ".md":
                if unquote(url.fragment) not in helper["anchors"](target.read_text()):
                    raise ValueError(f"missing local anchor {path}:{line}: {destination}")
            link_count += 1
    return len(inputs["inputs"]), len(old), len(checks), link_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--seal", action="store_true")
    group.add_argument("--check", action="store_true")
    parser.add_argument("--seal-path", type=Path,
                        help="read-only alternate manifest for corruption controls")
    args = parser.parse_args()
    if args.seal and args.seal_path:
        parser.error("--seal-path is only for --check")
    counts = prerequisites(allow_pending_seal=args.seal)
    payloads = inventory(AUDIT, excluded={"SEAL.json"})
    payload_hash = digest(canonical(payloads))
    seal_path = args.seal_path or AUDIT / "SEAL.json"
    if args.seal:
        value = {"schema": "br-sd-1g-custody-v1", "base": BASE,
                 "parent_status": "OPEN", "new_unconditional_closures": 0,
                 "claim": CLAIM,
                 "payload_manifest_sha256": payload_hash, "payloads": payloads}
        with seal_path.open("x") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
    else:
        value = json.loads(seal_path.read_text())
        if (set(value) != SEAL_KEYS or value["claim"] != CLAIM
                or value["schema"] != "br-sd-1g-custody-v1" or value["base"] != BASE
                or value["parent_status"] != "OPEN" or value["new_unconditional_closures"] != 0
                or value["payload_manifest_sha256"] != digest(canonical(value["payloads"]))
                or value["payloads"] != payloads):
            raise ValueError("seal corruption or payload inventory/hash/mode drift")
    print(json.dumps({"status": "custody verified", "mode": "seal" if args.seal else "check",
                      "base": BASE, "payloads": len(payloads), "authority_inputs": counts[0],
                      "old_custody_files": counts[1], "recorded_checks": counts[2],
                      "local_links_checked": counts[3],
                      "payload_manifest_sha256": payload_hash,
                      "source_finite_status": "not triggered", "parent_status": "OPEN",
                      "new_unconditional_closures": 0}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
