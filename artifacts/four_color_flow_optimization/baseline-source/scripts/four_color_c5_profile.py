#!/usr/bin/env python3
"""Replay the frozen C5-finder timing experiment on its original graph cohort.

The stored finder-profile.json was measured with byte-identical frozen modules
in /tmp. This script repeats that recipe using baseline-source, without copying
the modules or the prior experiment. Wall-clock timings vary between runs.
The solver's internal final coloring check is timed; graph preparation and
external comparisons of the two modes are outside the measurement.
"""
from __future__ import annotations

import argparse
import cProfile
import hashlib
import importlib
import json
from pathlib import Path
import pstats
import statistics
import sys
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts/four_color_c5"
FROZEN = ARTIFACTS / "baseline-source"
SOURCE_SHA256 = {
    "four_color_c5.py": "643e0e27281a4e9677358cbf3488029de0ca1d411424625acd88e8f725a9b46c",
    "four_color_constraints.py": "423f09d5ede3031eadb22bc01321f237230f3f98ea01972c160672b6aef417e4",
    "four_color_lab.py": "822577e9d29f7a74e6c6c12d06ae85dddd88145beb417ba3760843f911ee9753",
    "four_color_examples.py": "cfa9f761475072e2e0e57e0b3afc3b527141e1e8b4b9b65e20f239228eafa953",
}
NOTE = (
    "All stages measured on frozen prior source bytes; cached mode reuses the same "
    "once-per-graph scan result. Query wrapper overhead included in both modes; "
    "graph generation and external result comparisons excluded; solver final coloring check included. "
    "Timings can vary under concurrent work."
)


def load_baseline():
    """Reject changed source bytes before importing any solver code."""
    prior = json.loads((FROZEN.parent / "experiment.json").read_text())
    for name, expected in SOURCE_SHA256.items():
        actual = hashlib.sha256((FROZEN / name).read_bytes()).hexdigest()
        if actual != expected or prior["sources"].get(name) != expected:
            raise ValueError(f"frozen source or prior experiment SHA-256 mismatch: {name}")
        module = sys.modules.get(Path(name).stem)
        if module is not None and Path(module.__file__).resolve() != (FROZEN / name).resolve():
            raise ValueError(f"current-tree module already imported: {name}")
    sys.path.insert(0, str(FROZEN))
    modules = {Path(name).stem: importlib.import_module(Path(name).stem)
               for name in SOURCE_SHA256}
    return prior, modules


def summarize(rows, repetitions):
    summary = {}
    keys = ("seconds", "finder_seconds", "query_seconds", "rest_seconds",
            "finder_calls", "query_calls")
    for cohort in ("free", "fixed"):
        summary[cohort] = {}
        for mode in ("finder", "precomputed"):
            selected = [row for row in rows if row["cohort"] == cohort and row["mode"] == mode]
            totals = []
            for repeat in range(repetitions):
                part = [row for row in selected if row["repeat"] == repeat]
                totals.append({key: sum(row[key] for row in part) for key in keys})
            summary[cohort][mode] = dict(
                repetition_totals=totals,
                mean_totals={key: statistics.mean(total[key] for total in totals) for key in keys})
        finder = summary[cohort]["finder"]["mean_totals"]
        precomputed = summary[cohort]["precomputed"]["mean_totals"]
        summary[cohort]["finder_fraction"] = finder["finder_seconds"] / finder["seconds"]
        summary[cohort]["ideal_speedup_ceiling"] = (
            finder["seconds"] / (finder["seconds"] - finder["finder_seconds"]))
        summary[cohort]["measured_precomputed_speedup"] = finder["seconds"] / precomputed["seconds"]
        fractions = [row["finder_seconds"] / row["seconds"] for row in rows
                     if row["cohort"] == cohort and row["mode"] == "finder"]
        summary[cohort]["per_graph_finder_fraction_median"] = statistics.median(fractions)
        summary[cohort]["per_graph_finder_fraction_max"] = max(fractions)
    return summary


def run_profile():
    prior, modules = load_baseline()
    c5 = modules["four_color_c5"]
    solve_constraints = modules["four_color_constraints"].solve_constraints
    graph_fingerprint = modules["four_color_lab"].graph_fingerprint
    random_triangulation = modules["four_color_examples"].random_triangulation
    original_find, original_query = c5.find_induced_c5, c5.query_c5
    samples = []
    for record in prior["records"]:
        base = random_triangulation(prior["vertices"], record["seed"])
        scan = original_find(base)
        for cohort, graph in (("free", base), ("fixed", dict(base, fixed=record["fixed"]))):
            if graph_fingerprint(graph) != record["cohorts"][cohort]["graph_sha256"]:
                raise ValueError(f"graph fingerprint mismatch: seed={record['seed']}, cohort={cohort}")
            samples.append((record["seed"], cohort, graph, scan))
    print(f"Prepared and fingerprint-verified {len(samples)} cohort graphs.", flush=True)

    rows, repetitions = [], 2
    try:
        for repeat in range(repetitions):
            for seed, cohort, graph, scan in samples:
                outputs = {}
                modes = (("finder", "precomputed") if (seed + repeat) % 2 == 0
                         else ("precomputed", "finder"))
                for mode in modes:
                    stage = dict(finder_seconds=0.0, finder_calls=0, query_seconds=0.0, query_calls=0)

                    def find_wrapper(*args, **kwargs):
                        stage["finder_calls"] += 1
                        if mode == "precomputed":
                            return scan
                        started = perf_counter()
                        result = original_find(*args, **kwargs)
                        stage["finder_seconds"] += perf_counter() - started
                        return result

                    def query_wrapper(*args, **kwargs):
                        stage["query_calls"] += 1
                        started = perf_counter()
                        result = original_query(*args, **kwargs)
                        stage["query_seconds"] += perf_counter() - started
                        return result

                    c5.find_induced_c5, c5.query_c5 = find_wrapper, query_wrapper
                    started = perf_counter()
                    result = solve_constraints(graph, use_c5=True, max_checks=prior["max_checks"],
                                               trace_limit=0, record_relations=False,
                                               use_conflicts=False, c5_method="table")
                    elapsed = perf_counter() - started
                    outputs[mode] = result
                    rows.append(dict(
                        repeat=repeat, seed=seed, cohort=cohort, mode=mode, seconds=elapsed,
                        rest_seconds=elapsed - stage["finder_seconds"] - stage["query_seconds"],
                        status=result["status"], cycles=result["substructures"]["c5"],
                        scan_steps=result["substructures"]["c5_scan_steps"], **stage))
                    if stage["finder_calls"] != 1:
                        raise AssertionError("expected exactly one finder invocation per solve")
                for field in ("status", "colors", "stats"):
                    if outputs["finder"][field] != outputs["precomputed"][field]:
                        raise AssertionError(f"precomputed finder changed {field}")
            print(f"Finished repetition {repeat + 1}.", flush=True)
    finally:
        c5.find_induced_c5, c5.query_c5 = original_find, original_query

    # Instrumented stage profiling is separate from the wall-clock measurements.
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        for _seed, _cohort, graph, _scan in samples:
            solve_constraints(graph, use_c5=True, max_checks=prior["max_checks"],
                              trace_limit=0, record_relations=False,
                              use_conflicts=False, c5_method="table")
    finally:
        profiler.disable()
    stages = []
    for (filename, line, name), (_primitive, calls, self_time, cumulative, _callers) in pstats.Stats(profiler).stats.items():
        if filename.endswith(("four_color_constraints.py", "four_color_c5.py")):
            stages.append(dict(file=Path(filename).name, line=line, name=name, calls=calls,
                               self_seconds=self_time, cumulative_seconds=cumulative))
    stages.sort(key=lambda stage: stage["cumulative_seconds"], reverse=True)
    return dict(source_sha256=SOURCE_SHA256, matched_graphs=len(samples), repetitions=repetitions,
                max_checks=prior["max_checks"], summary=summarize(rows, repetitions), rows=rows,
                profile_stages=stages, note=NOTE, python=sys.version.split()[0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ARTIFACTS / "finder-profile.json",
                        help="output receipt path; repeats the full timing/profile experiment")
    args = parser.parse_args()
    result = run_profile()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
    print(f"Profile receipt: {args.out}")


if __name__ == "__main__":
    main()
