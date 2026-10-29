#!/usr/bin/env python3
"""Compare full scan/delta propagation records under identical solver settings."""

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
MODES = ("scan", "delta")
COUNTERS = {"checks", "relation_checks", "intersection_checks", "intersection_cache_hits"}


def semantic_record(result):
    def stats(values):
        return {key: value for key, value in values.items()
                if key not in COUNTERS and not key.startswith(("interface_cache_", "propagation_"))}
    answer = dict(result)
    answer.pop("propagation_method", None)
    answer["stats"] = stats(result["stats"])
    answer["events"] = [dict(event, stats=stats(event["stats"])) for event in result["events"]]
    return answer


def compare(out):
    reports = {mode: json.loads((out/mode/"report.json").read_text()) for mode in MODES}
    baseline = reports["scan"]
    cases, totals = {}, {}
    for mode, report in reports.items():
        for key in ("inputs_sha256", "selected_cases", "sources", "driver_sha256", "oracle_max_rows"):
            if report[key] != baseline[key]:
                raise AssertionError(f"changed source or validation: {key}")
        if {k: v for k, v in report["options"].items() if k != "propagation_method"} != {
                k: v for k, v in baseline["options"].items() if k != "propagation_method"}:
            raise AssertionError("changed budgets, partition or inference")
        times = json.loads((out/mode/"timings.json").read_text())
        totals[mode] = dict(stats=report["totals"]["all"]["stats"],
                            statuses=report["totals"]["all"]["status_counts"],
                            solver_seconds=times["total_solver_seconds"])
    for old, new in zip(baseline["cases"], reports["delta"]["cases"], strict=True):
        if {k: v for k, v in old.items() if k != "results"} != {
                k: v for k, v in new.items() if k != "results"}:
            raise AssertionError("changed original graph or independent reference")
        loaded, metrics = {}, {}
        for mode, case in (("scan", old), ("delta", new)):
            row = case["results"]["combined-contexts"]
            raw = (out/mode/row["full_record"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != row["compressed_record_sha256"]:
                raise AssertionError("record checksum mismatch")
            result = json.loads(gzip.decompress(raw))
            if result["propagation_method"] != mode or result["status"] == "limit" or result["trace_truncated"]:
                raise AssertionError("comparison requires complete executions with the requested method")
            loaded[mode] = semantic_record(result)
            metrics[mode] = dict(checks=result["stats"]["checks"],
                                 intersection_checks=result["stats"]["intersection_checks"],
                                 record_sha256=row["compressed_record_sha256"],
                                 preservation=row["preservation"])
        if loaded["scan"] != loaded["delta"]:
            raise AssertionError(f"semantic record mismatch: {old['name']}")
        encoded = json.dumps(loaded["scan"], sort_keys=True, separators=(",", ":")).encode()
        cases[old["name"]] = dict(status=loaded["scan"]["status"],
                                 semantic_sha256=hashlib.sha256(encoded).hexdigest(), modes=metrics)
    counts = Counter("improved" if c["modes"]["delta"]["checks"] < c["modes"]["scan"]["checks"]
                     else "worse" if c["modes"]["delta"]["checks"] > c["modes"]["scan"]["checks"]
                     else "equal" for c in cases.values())
    return dict(schema="four-color-delta-propagation-v1", totals=totals, cases=cases,
                options=baseline["options"], inputs_sha256=baseline["inputs_sha256"],
                check_changes=dict(counts), complete_semantic_records_equal=True,
                allowed_differences=["propagation_method", "stats/events.stats: " + ", ".join(sorted(COUNTERS)),
                                     "stats/events.stats: interface_cache_* and propagation_*"],
                comparison_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--partition", choices=("none", "information", "message"), default="none")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    source = args.out_dir/"source/scripts"
    source.mkdir(parents=True)
    for path in (ROOT/"scripts").glob("four_color*.py"):
        shutil.copyfile(path, source/path.name)
    for mode in MODES:
        print(f"Running {args.partition}/{mode}", flush=True)
        command = [sys.executable, str(ROOT/"scripts/four_color_flow_experiment.py"),
                   "--out-dir", str(args.out_dir/mode), "--solver-source", str(source),
                   "--max-table-rows", "1000000", "--interface-cache", "on", "--bucket-method", "prefix",
                   "--propagation-method", mode, "--partition", args.partition, "--measure-peak-rss"]
        with (args.out_dir/f"{mode}.log").open("w") as stream:
            subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=True)
    report = compare(args.out_dir)
    shutil.copyfile(Path(__file__), args.out_dir/"comparison_driver.py")
    (args.out_dir/"comparison.json").write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(json.dumps(dict(changes=report["check_changes"], modes={mode: dict(
        checks=value["stats"]["checks"], intersection_checks=value["stats"]["intersection_checks"],
        seconds=value["solver_seconds"], statuses=value["statuses"])
        for mode, value in report["totals"].items()}), indent=2))


if __name__ == "__main__":
    main()
