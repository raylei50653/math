#!/usr/bin/env python3
"""Compare storage capacities or RAM indexes in fresh processes per frozen graph.

Every child uses the complete flow driver's original-source validation. The
comparison varies storage capacity or cache use; other budgets remain fixed. Peak
RSS and wall time are observations stored separately from deterministic proof
records. Workers execute sequentially, including when only probes are selected.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
from time import perf_counter

import four_color_flow_experiment as flow


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "artifacts/four_color_memory_optimization"
DRIVER = ROOT / "scripts/four_color_flow_experiment.py"
RSS_FIELDS = ("peak_rss_before_solve_bytes", "peak_rss_after_solve_bytes",
              "peak_rss_after_serialization_bytes")


def experiment(out_dir, *, solver_source, inputs, row_limits, names=None,
               check_planarity=True, cache_modes=None, interface_cache_max_rows=1_000_000):
    if (not row_limits or len(set(row_limits)) != len(row_limits)
            or any(type(value) is not int or value < 0 for value in row_limits)):
        raise ValueError("row limits must be distinct nonnegative integers")
    if type(interface_cache_max_rows) is not int or interface_cache_max_rows < 0:
        raise ValueError("interface_cache_max_rows must be a nonnegative integer")
    if cache_modes is not None:
        if (len(row_limits) != 1 or not cache_modes or len(set(cache_modes)) != len(cache_modes)
                or any(mode not in ("off", "on") for mode in cache_modes)):
            raise ValueError("cache comparison requires distinct off/on modes and exactly one row limit")
        configurations = [(mode, row_limits[0], mode == "on", f"cache-{mode}") for mode in cache_modes]
    else:
        configurations = [(str(cap), cap, None, f"rows-{cap}") for cap in row_limits]
    solver_source = solver_source.resolve()
    raw, manifest_raw = inputs.read_bytes(), (EVIDENCE / "baseline-manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    if flow.sha256(raw) != flow.FROZEN_INPUT_SHA256 or manifest["inputs_sha256"] != flow.sha256(raw):
        raise ValueError("inputs must be the unchanged frozen forty-case source")
    prior_path = ROOT / manifest["prior_report"]
    prior_raw = prior_path.read_bytes()
    if flow.sha256(prior_raw) != manifest["prior_report_sha256"]:
        raise AssertionError("prior optimized reference report changed")
    cases = json.loads(raw)
    if (len(cases) != 40 or len({case["name"] for case in cases}) != 40
            or Counter(case["case_group"] for case in cases)
            != {"gap": 4, "structured": 24, "random": 12}):
        raise ValueError("unexpected frozen source cases")
    if names:
        unknown = set(names) - {case["name"] for case in cases}
        if unknown:
            raise ValueError(f"unknown frozen case names: {sorted(unknown)}")
        cases = [case for case in cases if case["name"] in set(names)]
    sources = flow.source_hashes(solver_source)
    if (solver_source == (EVIDENCE / "baseline-source/scripts").resolve()
            and sources != manifest["sources"]):
        raise AssertionError("memory baseline source no longer matches its frozen manifest")
    driver_hash, supervisor_hash = flow.sha256(DRIVER.read_bytes()), flow.sha256(Path(__file__).read_bytes())
    out_dir.mkdir(parents=True, exist_ok=True)
    flow.write_frozen(out_dir / "inputs.json", raw)
    flow.write_frozen(out_dir / "baseline-manifest.json", manifest_raw)
    budget_records = {key: [] for key, _, _, _ in configurations}
    records, timings, common_binding = [], [], None
    for position, case in enumerate(cases, 1):
        capacity_rows, capacity_times, original_reference = {}, {}, None
        for key, cap, cache_enabled, directory in configurations:
            relative = Path(directory) / case["name"]
            worker_dir = out_dir / relative
            worker_dir.mkdir(parents=True, exist_ok=True)
            command = [sys.executable, str(DRIVER), "--out-dir", str(worker_dir),
                       "--solver-source", str(solver_source), "--inputs", str(inputs.resolve()),
                       "--case", case["name"], "--max-table-rows", str(cap), "--measure-peak-rss"]
            expected_options = dict(flow.OPTIONS, max_table_rows=cap)
            if cache_enabled is not None:
                command.extend(["--interface-cache", key, "--interface-cache-max-rows", str(interface_cache_max_rows)])
                expected_options.update(use_interface_cache=cache_enabled,
                                        interface_cache_max_rows=interface_cache_max_rows)
            if not check_planarity:
                command.append("--skip-planarity")
            label = f"cache={key},rows={cap}" if cache_enabled is not None else f"rows={cap}"
            print(f"{position}/{len(cases)} {label} {case['name']}: starting fresh worker", flush=True)
            started = perf_counter()
            with (worker_dir / "worker.log").open("w") as log:
                completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
            worker_seconds = perf_counter() - started
            if completed.returncode:
                raise RuntimeError(f"worker failed ({completed.returncode}); inspect {worker_dir / 'worker.log'}")
            report_raw = (worker_dir / "report.json").read_bytes()
            report = json.loads(report_raw)
            child_times = json.loads((worker_dir / "timings.json").read_bytes())
            if (report["case_count"] != 1 or report["selected_cases"] != [case["name"]]
                    or len(report["cases"]) != 1 or len(child_times["cases"]) != 1
                    or child_times["memory_measurement"]["process_cases"] != 1):
                raise AssertionError("a fresh worker must process exactly its selected original case")
            if (report["inputs_sha256"] != flow.sha256(raw) or report["sources"] != sources
                    or report["driver_sha256"] != driver_hash
                    or report["options"] != expected_options):
                raise AssertionError("worker source/input/options differ from the fixed comparison")
            binding = {key: report[key] for key in (
                "sources", "driver_sha256", "inputs_sha256", "oracle_max_rows", "python", "networkx",
                "baseline_manifest_sha256", "baseline_commit", "prior_report_sha256")}
            if common_binding is None:
                common_binding = binding
            elif binding != common_binding:
                raise AssertionError("workers changed sources, input, reference, or validation options")
            child_case = report["cases"][0]
            reference = {key: value for key, value in child_case.items() if key != "results"}
            if original_reference is None:
                original_reference = reference
            elif reference != original_reference:
                raise AssertionError("capacities do not share the same original-source reference")
            row = dict(child_case["results"][flow.MODE])
            record_path = worker_dir / row["full_record"]
            if flow.sha256(record_path.read_bytes()) != row["compressed_record_sha256"]:
                raise AssertionError("complete worker record does not match its receipt")
            row.update(full_record=str(relative / row["full_record"]),
                       worker_report=str(relative / "report.json"),
                       worker_report_sha256=flow.sha256(report_raw))
            capacity_rows[key] = row
            budget_records[key].append(child_case)
            timing = dict(child_times["cases"][0], worker_seconds=worker_seconds)
            if not (0 < timing[RSS_FIELDS[0]] <= timing[RSS_FIELDS[1]] <= timing[RSS_FIELDS[2]]):
                raise AssertionError("process high-water marks must be positive and nondecreasing")
            capacity_times[key] = timing
            print(f"{position}/{len(cases)} {label} {case['name']}: {row['status']}, "
                  f"checks={row['stats']['checks']}, peak_rss={timing[RSS_FIELDS[-1]]} bytes", flush=True)
        records.append(dict(original_reference, results=capacity_rows))
        timings.append(dict(name=case["name"], results=capacity_times))
    if (flow.source_hashes(solver_source) != sources or flow.sha256(DRIVER.read_bytes()) != driver_hash
            or flow.sha256(Path(__file__).read_bytes()) != supervisor_hash or inputs.read_bytes() != raw
            or (EVIDENCE / "baseline-manifest.json").read_bytes() != manifest_raw
            or prior_path.read_bytes() != prior_raw):
        raise AssertionError("sources or frozen references changed during the isolated comparison")
    report = dict(
        schema="four-color-ram-indexes-v1" if cache_modes is not None else "four-color-memory-optimization-v1",
        case_count=len(cases),
        selected_cases=[case["name"] for case in cases], row_limits=row_limits,
        cases=records, totals={cap: flow.totals_for(rows) for cap, rows in budget_records.items()},
        options=flow.OPTIONS, oracle_max_rows=flow.ORACLE_MAX_ROWS,
        sources=sources, driver_sha256=driver_hash, supervisor_sha256=supervisor_hash,
        worker_binding=common_binding, input_file="inputs.json", inputs_sha256=flow.sha256(raw),
        baseline_manifest_file="baseline-manifest.json", baseline_manifest_sha256=flow.sha256(manifest_raw),
        prior_report=manifest["prior_report"], prior_report_sha256=flow.sha256(prior_raw),
        interpretation=(
            ("Fresh sequential exec processes per original graph and interface-cache mode. Only "
             "the acceleration-cache mode varies; complete-record storage is fixed. "
             if cache_modes is not None else
             "Fresh sequential exec processes per original graph and storage capacity. Only the "
             "explicit storage cap varies. ") + "Work/discovery/oracle budgets and full recording remain "
            "fixed. All original-source validation layers run inside every worker. Finite original "
            "solution/projection/one-witness boundaries are recorded per case; limits remain "
            "inconclusive. RSS and timings are separate process-lifetime observations, not "
            "deterministic certificates or general performance guarantees."
        ),
    )
    if cache_modes is not None:
        report.update(cache_modes=cache_modes, interface_cache_max_rows=interface_cache_max_rows,
                      modes={key: dict(max_table_rows=cap, use_interface_cache=enabled,
                                       interface_cache_max_rows=interface_cache_max_rows)
                             for key, cap, enabled, _ in configurations})
    timing_totals = {}
    for key, _, _, _ in configurations:
        rows = [case["results"][key] for case in timings]
        timing_totals[key] = dict(
            total_solver_seconds=sum(row["solver_seconds"] for row in rows),
            total_case_seconds=sum(row["case_seconds"] for row in rows),
            total_worker_seconds=sum(row["worker_seconds"] for row in rows),
            maximum_case_peak_rss_bytes=max((row[RSS_FIELDS[-1]] for row in rows), default=0),
        )
        if cache_modes is not None:
            timing_totals[key]["maximum_case_peak_rss_after_solve_bytes"] = max(
                (row[RSS_FIELDS[1]] for row in rows), default=0)
    (out_dir / "report.json").write_bytes(flow.encoded(report))
    (out_dir / "timings.json").write_bytes(flow.encoded(dict(
        schema="four-color-ram-index-timings-v1" if cache_modes is not None else "four-color-memory-timings-v1",
        cases=timings, totals=timing_totals,
        metric="resource.getrusage(RUSAGE_SELF).ru_maxrss", units="bytes", platform=sys.platform,
        interpretation="Each child handles one case; RSS includes imports, validation, and serialization. "
                       "High-water marks are not additive allocations. Wall time/RSS are excluded from replay equality.",
    )))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--solver-source", type=Path, default=ROOT / "scripts")
    parser.add_argument("--inputs", type=Path, default=EVIDENCE / "inputs.json")
    parser.add_argument("--row-limits", type=int, nargs="+", default=[100_000, 1_000_000])
    parser.add_argument("--cache-modes", nargs="+", choices=("off", "on"),
                        help="compare cache modes at exactly one explicit --row-limits value")
    parser.add_argument("--interface-cache-max-rows", type=int, default=1_000_000)
    parser.add_argument("--case", action="append", nargs="+", dest="cases")
    parser.add_argument("--skip-planarity", action="store_true")
    args = parser.parse_args()
    report = experiment(args.out_dir, solver_source=args.solver_source, inputs=args.inputs,
                        row_limits=args.row_limits,
                        names=[name for group in (args.cases or []) for name in group],
                        check_planarity=not args.skip_planarity, cache_modes=args.cache_modes,
                        interface_cache_max_rows=args.interface_cache_max_rows)
    print(json.dumps({cap: groups["all"]["status_counts"] for cap, groups in report["totals"].items()},
                     sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
