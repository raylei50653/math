#!/usr/bin/env python3
"""Replay seven current configurations on the frozen forty original contexts."""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CONFIGS = {
    "anchor_scan": ("anchor", "scan", "none", "on"),
    "prefix_scan_uncached": ("prefix", "scan", "none", "off"),
    "prefix_scan": ("prefix", "scan", "none", "on"),
    "prefix_delta": ("prefix", "delta", "none", "on"),
    "prefix_support": ("prefix", "support", "none", "on"),
    "information_delta": ("prefix", "delta", "information", "on"),
    "message_delta": ("prefix", "delta", "message", "on"),
}
PAIRS = (
    ("anchor_scan", "prefix_scan", "bucket"),
    ("prefix_scan_uncached", "prefix_scan", "cache"),
    ("prefix_scan", "prefix_delta", "propagation"),
    ("prefix_delta", "prefix_support", "propagation"),
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def normalized(record, kind):
    record = dict(record)
    counters = {"checks", "relation_checks"}
    prefixes = ()
    if kind == "bucket":
        record.pop("bucket_method")
        counters.add("candidate_checks")
    elif kind == "cache":
        record.pop("use_interface_cache")
        counters.update(("intersection_checks", "intersection_cache_hits", "cycle_context_checks"))
        prefixes = ("interface_cache_", "interface_cover_index_")
    else:
        record.pop("propagation_method")
        counters.update(("intersection_checks", "intersection_cache_hits"))
        prefixes = ("interface_cache_", "propagation_")
    def stats(values):
        return {k: v for k, v in values.items()
                if k not in counters and not k.startswith(prefixes)}
    record["stats"] = stats(record["stats"])
    record["events"] = [dict(e, stats=stats(e["stats"])) for e in record["events"]]
    return record


def summarize(out):
    reports = {name: json.loads((out/name/"report.json").read_text()) for name in CONFIGS}
    base = reports["prefix_scan"]
    totals, cases = {}, {}
    for name, report in reports.items():
        for field in ("inputs_sha256", "sources", "driver_sha256", "selected_cases",
                      "oracle_max_rows", "python", "networkx"):
            assert report[field] == base[field], (name, field)
        assert report["case_count"] == 40
        expected = dict(base["options"], bucket_method=CONFIGS[name][0],
                        propagation_method=CONFIGS[name][1], partition_strategy=CONFIGS[name][2],
                        use_interface_cache=CONFIGS[name][3] == "on")
        assert report["options"] == expected, name
        timing = json.loads((out/name/"timings.json").read_text())
        times = {c["name"]: c for c in timing["cases"]}
        coverage = Counter()
        for original, case in zip(base["cases"], report["cases"], strict=True):
            assert {k: v for k, v in case.items() if k != "results"} == {
                k: v for k, v in original.items() if k != "results"}
            row = case["results"]["combined-contexts"]
            raw = (out/name/row["full_record"]).read_bytes()
            assert digest(raw) == row["compressed_record_sha256"]
            record = json.loads(gzip.decompress(raw))
            assert record["bucket_method"] == CONFIGS[name][0]
            assert record["propagation_method"] == CONFIGS[name][1]
            assert record["partition_plan"]["strategy"] == CONFIGS[name][2]
            assert record["use_interface_cache"] == (CONFIGS[name][3] == "on")
            assert record["graph_sha256"] == case["graph_sha256"]
            assert record["status"] == case["reference_status"]
            assert not record["trace_truncated"]
            assert row["preservation"]["complete_solver_run"]
            assert row["preservation"]["trace_complete"]
            assert not row["preservation"].get("projection_limits")
            coverage[row["preservation"]["coverage"]] += 1
            cases.setdefault(case["name"], {})[name] = dict(
                status=record["status"], checks=record["stats"]["checks"],
                intersection_checks=record["stats"]["intersection_checks"],
                table_rows=record["stats"]["table_rows"],
                certificate_rows=record["stats"]["certificate_rows"],
                peak_frontier=record["stats"]["peak_frontier"],
                solver_seconds=times[case["name"]]["solver_seconds"],
                record_sha256=digest(raw), preservation=row["preservation"])
        totals[name] = dict(
            options=report["options"], statuses=report["totals"]["all"]["status_counts"],
            checks=report["totals"]["all"]["stats"]["checks"],
            intersection_checks=report["totals"]["all"]["stats"]["intersection_checks"],
            table_rows=report["totals"]["all"]["stats"]["table_rows"],
            certificate_rows=report["totals"]["all"]["stats"]["certificate_rows"],
            peak_frontier=max(c[name]["peak_frontier"] for c in cases.values()),
            solver_seconds=timing["total_solver_seconds"],
            process_peak_after_solve_bytes=max(c["peak_rss_after_solve_bytes"] for c in timing["cases"]),
            preservation_coverage=dict(coverage))
    comparisons = []
    for before, after, kind in PAIRS:
        for old, new in zip(reports[before]["cases"], reports[after]["cases"], strict=True):
            def load(name, case):
                return json.loads(gzip.decompress((out/name/case["results"]["combined-contexts"]["full_record"]).read_bytes()))
            assert normalized(load(before, old), kind) == normalized(load(after, new), kind), (before, after, old["name"])
        changes = Counter("improved" if c[after]["checks"] < c[before]["checks"] else
                          "worse" if c[after]["checks"] > c[before]["checks"] else "equal"
                          for c in cases.values())
        comparisons.append(dict(before=before, after=after, kind=kind,
                                complete_semantic_records_equal=True, check_changes=dict(changes),
                                allowed_differences={
                                    "bucket": ["bucket_method", "stats/events.stats: checks, relation_checks, candidate_checks"],
                                    "cache": ["use_interface_cache", "stats/events.stats: checks, relation_checks, intersection_checks, intersection_cache_hits, cycle_context_checks", "stats/events.stats: interface_cache_*, interface_cover_index_*"],
                                    "propagation": ["propagation_method", "stats/events.stats: checks, relation_checks, intersection_checks, intersection_cache_hits", "stats/events.stats: interface_cache_*, propagation_*"],
                                }[kind]))
    for name in ("information_delta", "message_delta"):
        totals[name]["check_changes_vs_none_delta"] = dict(Counter(
            "improved" if c[name]["checks"] < c["prefix_delta"]["checks"] else
            "worse" if c[name]["checks"] > c["prefix_delta"]["checks"] else "equal"
            for c in cases.values()))
    result = dict(schema="four-color-current-method-comparison-v1", totals=totals,
                  cases=cases, comparisons=comparisons, inputs_sha256=base["inputs_sha256"],
                  sources=base["sources"], driver_sha256=base["driver_sha256"],
                  comparison_driver_sha256=digest(Path(__file__).read_bytes()), python=base["python"],
                  interpretation="One sequential timing per configuration, including planning but excluding independent validation and serialization. Process RSS is a lifetime high-water mark, not solver-only allocation. Different partition orders are independently checked against original-graph references; their intermediate records need not be equal. Finite sample only; limit is inconclusive.")
    (out/"comparison.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(dict(totals=totals, comparisons=comparisons), indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summarize-only", action="store_true")
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if not args.summarize_only:
        out.mkdir(parents=True, exist_ok=False)
        source = out/"source/scripts"
        source.mkdir(parents=True)
        for path in (ROOT/"scripts").glob("four_color*.py"):
            shutil.copyfile(path, source/path.name)
        for name, (bucket, propagation, partition, cache) in CONFIGS.items():
            print(f"Running {name}", flush=True)
            command = [sys.executable, str(ROOT/"scripts/four_color_flow_experiment.py"),
                       "--out-dir", str(out/name), "--solver-source", str(source),
                       "--max-table-rows", "1000000", "--measure-peak-rss",
                       "--interface-cache", cache, "--bucket-method", bucket,
                       "--propagation-method", propagation, "--partition", partition]
            with (out/f"{name}.log").open("w") as stream:
                subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=True)
        shutil.copyfile(Path(__file__), out/"comparison_driver.py")
    summarize(out)


if __name__ == "__main__":
    main()
