#!/usr/bin/env python3
"""Compare exact anchor enumeration and early complete-factor prefix rejection.

Each mode runs the existing frozen forty-case independent validation driver in
a fresh process. Complete outputs may differ only in the selected method and
three actual-work counters; all other fields, including every event and fibre,
must match. This finite experiment does not assert universal speed improvement.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
WORK_COUNTERS = {"checks", "candidate_checks", "relation_checks"}


def semantic_record(record):
    """Remove only method metadata and actual-work counters, nowhere else."""
    result = dict(record)
    result.pop("bucket_method", None)
    result["stats"] = {key: value for key, value in record["stats"].items()
                       if key not in WORK_COUNTERS}
    result["events"] = [dict(event, stats={
        key: value for key, value in event["stats"].items() if key not in WORK_COUNTERS
    }) for event in record["events"]]
    return result


def digest(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def compare(out_dir):
    reports = {mode: json.loads((out_dir / mode / "report.json").read_text())
               for mode in ("anchor", "prefix")}
    for mode, report in reports.items():
        if report["options"].get("bucket_method") != mode:
            raise AssertionError(f"report did not select the requested {mode} method")
    old, new = reports["anchor"], reports["prefix"]
    for field in ("inputs_sha256", "sources", "driver_sha256", "selected_cases",
                  "oracle_max_rows", "python", "networkx"):
        if old[field] != new[field]:
            raise AssertionError(f"comparison changed {field}")
    options = [{k: v for k, v in report["options"].items() if k != "bucket_method"}
               for report in reports.values()]
    if options[0] != options[1]:
        raise AssertionError("comparison changed budgets or inference options")
    cases = []
    for before, after in zip(old["cases"], new["cases"], strict=True):
        if {k: v for k, v in before.items() if k != "results"} != {
                k: v for k, v in after.items() if k != "results"}:
            raise AssertionError("original graph or independent reference changed")
        loaded, rows = {}, {}
        for mode, case in (("anchor", before), ("prefix", after)):
            row = case["results"]["combined-contexts"]
            raw = (out_dir / mode / row["full_record"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != row["compressed_record_sha256"]:
                raise AssertionError("full record differs from its source receipt")
            loaded[mode] = json.loads(gzip.decompress(raw))
            if loaded[mode].get("bucket_method") != mode:
                raise AssertionError(f"full record did not execute the requested {mode} method")
            if loaded[mode]["status"] == "limit":
                raise AssertionError("cannot claim complete equivalence from a limited run")
            if loaded[mode]["trace_truncated"]:
                raise AssertionError("complete event comparison requires untruncated traces")
            rows[mode] = dict(checks=row["stats"]["checks"],
                              candidate_checks=row["stats"]["candidate_checks"],
                              relation_checks=row["stats"]["relation_checks"],
                              record_sha256=row["compressed_record_sha256"])
        left, right = map(semantic_record, (loaded["anchor"], loaded["prefix"]))
        if left != right:
            raise AssertionError(f"complete semantic output changed: {before['name']}")
        cases.append(dict(name=before["name"], status=left["status"],
                          complete_semantic_output_equal=True,
                          semantic_sha256=digest(left), modes=rows))
    totals = {mode: report["totals"]["all"] for mode, report in reports.items()}
    return dict(schema="four-color-prefix-comparison-v1", cases=cases,
                case_count=len(cases), totals=totals,
                case_groups=dict(Counter(case["case_group"] for case in old["cases"])),
                inputs_sha256=old["inputs_sha256"], sources=old["sources"],
                options=options[0], allowed_differences=["bucket_method",
                    "stats.{checks,candidate_checks,relation_checks}",
                    "events[*].stats.{checks,candidate_checks,relation_checks}"],
                interpretation="Complete outputs compared, not just SAT/UNSAT labels. "
                    "The independent validation coverage remains per selected case: exhaustive "
                    "gap controls, exact structural projections, or frozen random "
                    "witness/UNSAT references; selected counts are in case_groups. "
                    "Prefix work counts partial extensions, "
                    "so resource-limit positions need not equal the anchor method.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--case", action="append", default=[], dest="cases")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    driver = ROOT / "scripts/four_color_flow_experiment.py"
    for mode in ("anchor", "prefix"):
        command = [sys.executable, str(driver), "--out-dir", str(args.out_dir / mode),
                   "--max-table-rows", "1000000", "--interface-cache", "on",
                   "--bucket-method", mode]
        for name in args.cases:
            command.extend(["--case", name])
        print(f"Running {mode}", flush=True)
        with (args.out_dir / f"{mode}.log").open("w") as stream:
            subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=True)
    report = compare(args.out_dir)
    (args.out_dir / "comparison.json").write_text(
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"case_count": report["case_count"],
                      "complete_semantic_outputs_equal": True,
                      "checks": {mode: total["stats"]["checks"]
                                 for mode, total in report["totals"].items()}}, indent=2))


if __name__ == "__main__":
    main()
