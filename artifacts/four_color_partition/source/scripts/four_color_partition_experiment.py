#!/usr/bin/env python3
"""Compare partition schedules on the same forty frozen, independently checked cases."""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = ("none", "components", "articulation", "bfs")


def compare(out):
    reports = {mode: json.loads((out / mode / "report.json").read_text()) for mode in STRATEGIES}
    baseline = reports["none"]
    cases, totals = {}, {}
    for mode, report in reports.items():
        for key in ("inputs_sha256", "selected_cases", "sources", "driver_sha256"):
            if report[key] != baseline[key]:
                raise AssertionError(f"changed comparison source: {key}")
        if {k: v for k, v in report["options"].items() if k != "partition_strategy"} != {
                k: v for k, v in baseline["options"].items() if k != "partition_strategy"}:
            raise AssertionError("changed comparison budgets or inference")
        timing = json.loads((out / mode / "timings.json").read_text())
        totals[mode] = dict(statuses=dict(Counter()), checks=0, table_rows=0,
                            peak_frontier=0, solver_seconds=timing["total_solver_seconds"],
                            smaller_checks=0, equal_checks=0, larger_checks=0)
        statuses = Counter()
        for case in report["cases"]:
            row = case["results"]["combined-contexts"]
            raw = (out / mode / row["full_record"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != row["compressed_record_sha256"]:
                raise AssertionError("record checksum changed")
            result = json.loads(gzip.decompress(raw))
            if result["partition_plan"]["strategy"] != mode:
                raise AssertionError("wrong strategy executed")
            if result["status"] not in (case["reference_status"], "limit"):
                raise AssertionError("incorrect verdict")
            width = max((len(r["scope"]) for r in result["elimination_records"]), default=0)
            entry = dict(status=result["status"], checks=result["stats"]["checks"],
                         table_rows=result["stats"]["table_rows"],
                         peak_rows=result["stats"]["peak_rows"], peak_frontier=width,
                         groups=len(result["partition_plan"]["groups"]),
                         splits=len(result["partition_plan"]["splits"]),
                         preservation=row["preservation"],
                         record_sha256=row["compressed_record_sha256"])
            common = cases.setdefault(case["name"], dict(graph_sha256=case["graph_sha256"],
                        reference_status=case["reference_status"], strategies={}))
            if common["graph_sha256"] != case["graph_sha256"]:
                raise AssertionError("graph identity changed")
            common["strategies"][mode] = entry
            statuses[result["status"]] += 1
            for metric in ("checks", "table_rows"):
                totals[mode][metric] += entry[metric]
            totals[mode]["peak_frontier"] = max(totals[mode]["peak_frontier"], width)
            delta = entry["checks"] - common["strategies"]["none"]["checks"]
            totals[mode]["smaller_checks" if delta < 0 else "larger_checks" if delta > 0 else "equal_checks"] += 1
        totals[mode]["statuses"] = dict(statuses)
    return dict(schema="four-color-partition-comparison-v1", totals=totals, cases=cases,
                options=baseline["options"], inputs_sha256=baseline["inputs_sha256"],
                interpretation="Different schedules need not have identical intermediate fibres or final witnesses. "
                "Each run uses the original driver to check complete bucket joins, provenance, traces and "
                "independent original-graph references with the per-case coverage in preservation. "
                "Peak frontier is over completed records only. Limits are inconclusive. "
                "Planning is included in solver time but excluded from relation checks. No universal speed claim.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--block-size", type=int, default=12)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    source = args.out_dir / "source" / "scripts"
    source.mkdir(parents=True)
    for path in (ROOT / "scripts").glob("four_color*.py"):
        shutil.copyfile(path, source / path.name)
    driver = ROOT / "scripts/four_color_flow_experiment.py"
    for mode in STRATEGIES:
        print(f"Running {mode}", flush=True)
        command = [sys.executable, str(driver), "--out-dir", str(args.out_dir / mode),
                   "--solver-source", str(source), "--max-table-rows", "1000000",
                   "--interface-cache", "on", "--bucket-method", "prefix", "--partition", mode,
                   "--partition-block-size", str(args.block_size), "--measure-peak-rss"]
        with (args.out_dir / f"{mode}.log").open("w") as stream:
            subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=True)
    report = compare(args.out_dir)
    (args.out_dir / "comparison.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["totals"], indent=2))


if __name__ == "__main__":
    main()
