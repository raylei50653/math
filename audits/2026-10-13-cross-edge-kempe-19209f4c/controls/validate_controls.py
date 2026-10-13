#!/usr/bin/env python3
"""Replay normal, seed17, exclusive-write and malformed-certificate controls.

Default/--check compares the saved validation.json without changing artifacts.
--write exclusively creates validation.json. Temporary corrupt certificates
are confined to this controls directory and removed on exit.
"""
import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("check_cross_edge.py", "certificate.json.gz", "summary.json")}


def run(args, expected):
    result = subprocess.run([sys.executable, str(ROOT / "check_cross_edge.py"), *args],
                            text=True, capture_output=True,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    if result.returncode != expected:
        raise ValueError(f"unexpected exit {result.returncode}: {result.stdout} {result.stderr}")
    return {"exit_code": result.returncode, "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()}


def mutate(cert, kind):
    if kind == "drop_empty_J_cell":
        row = next(r for g in cert["graphs"] for e in g["edge_fibres"] for r in e["rows"]
                   if any(not cell for cell in r["cells"]))
        row["cells"].pop(next(i for i, cell in enumerate(row["cells"]) if not cell))
    elif kind == "change_named_color_in_full_J_lift":
        full = next(cell[0] for g in cert["graphs"] for e in g["edge_fibres"]
                    for r in e["rows"] for cell in r["cells"] if cell)
        full[0] = (full[0] + 1) % 4
    elif kind == "wrong_shared_edge_multiplicity":
        record = next(e for g in cert["graphs"] for e in g["edge_fibres"] if e["m5"] == 2)
        record["m5"] = 1
    elif kind == "missing_rejected_H_lift":
        row = next(r for g in cert["graphs"] for r in g["rows"] if r["rejected_by_G"] and r["h_lifts"])
        row["h_lifts"].pop()
    elif kind == "broken_Kempe_component_partition":
        component = cert["graphs"][0]["rows"][0]["pointwise_h_records"][0]["Kempe"]["color_pair_records"][0]["components"][0]
        component.pop()
    else:
        raise ValueError(f"unknown mutation {kind}")


def build():
    before = hashes()
    records = {"normal": run(["--check"], 0), "default_readonly": run([], 0),
               "seed17": run(["--check", "--seed", "17"], 0),
               "exclusive_write_refusal": run(["--write"], 1)}
    with gzip.open(ROOT / "certificate.json.gz", "rt") as stream:
        original = json.load(stream)
    with tempfile.TemporaryDirectory(prefix=".malformed-", dir=ROOT) as tmp:
        path = Path(tmp) / "certificate.json.gz"
        for kind in ("drop_empty_J_cell", "change_named_color_in_full_J_lift",
                     "wrong_shared_edge_multiplicity", "missing_rejected_H_lift",
                     "broken_Kempe_component_partition"):
            broken = copy.deepcopy(original)
            mutate(broken, kind)
            path.write_bytes(gzip.compress(json.dumps(broken).encode(), mtime=0))
            records[kind] = run(["--check", "--certificate", str(path)], 1)
    after = hashes()
    if before != after:
        raise ValueError("read-only replay or failed write changed original artifacts")
    return {"result": "PASS", "tests": records, "artifact_sha256_before": before,
            "artifact_sha256_after": after, "read_only_artifacts_unchanged": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "validation.json"
    if args.write and path.exists():
        raise ValueError("refusing to overwrite validation.json")
    result = build()
    if args.write:
        with path.open("x") as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write("\n")
    else:
        with path.open() as stream:
            if json.load(stream) != result:
                raise ValueError("validation.json differs from fresh replay")
    print(json.dumps({"result": "PASS", "test_count": len(result["tests"]),
                      "read_only_artifacts_unchanged": True}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"FAIL: {error}")
