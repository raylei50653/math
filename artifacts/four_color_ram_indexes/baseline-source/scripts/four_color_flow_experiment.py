#!/usr/bin/env python3
"""Replay one exact colouring workflow on forty frozen original contexts.

Run this driver in a fresh process for each solver source.  ``--solver-source``
selects both the solver and its validation helpers before any four_color module
is imported.  Deterministic records/report are separate from wall-clock timings.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import importlib
import inspect
import json
from pathlib import Path
import sys
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "artifacts/four_color_flow_optimization"
FROZEN_INPUT = EVIDENCE / "prior-inputs.json"
FROZEN_INPUT_SHA256 = "48f416783a9e8c73a0c4156a756eff2eda7b24778cd46a96ad9dca9d0d50abab"
MODE = "combined-contexts"
OPTIONS = dict(
    use_substructures=True, use_intersections=True, use_cycles=True,
    use_cycle_contexts=True, cycle_context_search="partial",
    use_conflicts=False, use_c5=False, use_joint_constraints=False,
    max_checks=5_000_000, trace_limit=5000, record_relations=True,
    cycle_max_cycles=128, cycle_max_scan_steps=200_000,
    cycle_context_max_contexts=128, cycle_context_max_scan_steps=200_000,
)
ORACLE_MAX_ROWS = 100_000


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def peak_rss_bytes():
    """Process-lifetime high-water mark, including imports and validation."""
    import resource

    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(raw if sys.platform == "darwin" else raw * 1024)


def write_frozen(path, data):
    if path.exists() and path.read_bytes() != data:
        raise ValueError(f"refusing to replace different frozen input: {path}")
    path.write_bytes(data)


def source_hashes(solver_source):
    """Hash the selected source tree without calling snapshot-relative helpers."""
    paths = sorted(solver_source.glob("four_color*.py"))
    paths += sorted((solver_source.parent / "tools/tests").glob("test_four_color*.py"))
    viewer = solver_source.parent / "tools/four_color_lab_viewer.html"
    if viewer.is_file():
        paths.append(viewer)
    return {
        str(path.relative_to(solver_source.parent)): sha256(path.read_bytes())
        for path in paths if path.resolve() != Path(__file__).resolve()
    }


def load_helpers(solver_source):
    """Prevent accidental mixtures of workspace modules and snapshot modules."""
    if any(name.startswith("four_color") for name in sys.modules):
        raise RuntimeError("select the solver source in a fresh process before importing helpers")
    if not (solver_source / "four_color_constraints.py").is_file():
        raise ValueError("--solver-source must contain four_color_constraints.py")
    sys.path.insert(0, str(solver_source))
    names = (
        "four_color_constraints", "four_color_lab", "four_color_guarantee_audit",
        "four_color_cycle_context_experiment", "four_color_larger_cases",
        "four_color_larger_experiment", "four_color_conflict_priority",
        "four_color_combined_experiment",
    )
    helpers = {name: importlib.import_module(name) for name in names}
    verify_module_sources(solver_source)
    return helpers


def verify_module_sources(solver_source):
    for name, module in list(sys.modules.items()):
        if name.startswith("four_color") and getattr(module, "__file__", None):
            if Path(module.__file__).resolve().parent != solver_source:
                raise AssertionError(f"mixed solver source for module {name}")


def frozen_cases(inputs, graph_fingerprint):
    raw = inputs.read_bytes()
    if sha256(raw) != FROZEN_INPUT_SHA256:
        raise ValueError("inputs must be the unchanged frozen forty-case source")
    cases = json.loads(raw)
    if (len(cases) != 40 or len({case["name"] for case in cases}) != 40
            or Counter(case["case_group"] for case in cases)
            != {"gap": 4, "structured": 24, "random": 12}):
        raise ValueError("unexpected frozen source cases")
    for case in cases:
        graph = case["graph"]
        if case.get("graph_sha256", graph_fingerprint(graph)) != graph_fingerprint(graph):
            raise AssertionError("frozen reference changed its original graph/fixed colors")
        if (case.get("source_graph_sha256", graph_fingerprint(dict(graph, fixed=[])))
                != graph_fingerprint(dict(graph, fixed=[]))):
            raise AssertionError("frozen reference changed its unfixed source graph")
    return cases, raw


def totals_for(records):
    totals = {}
    for group in ("gap", "structured", "random", "all"):
        rows = [record for record in records
                if group == "all" or record["case_group"] == group]
        data = [record["results"][MODE] for record in rows]
        keys = sorted({key for row in data for key in row["stats"]})
        totals[group] = dict(
            cases=len(rows), status_counts=dict(Counter(row["status"] for row in data)),
            stats={key: sum(row["stats"].get(key, 0) for row in data) for key in keys},
            truncated_traces=sum(row["trace_truncated"] for row in data),
            projection_limits=sum(bool(row["preservation"].get("projection_limits"))
                                  for row in data),
            preservation_coverage=dict(Counter(row["preservation"]["coverage"] for row in data)),
        )
    return totals


def experiment(out_dir, *, solver_source, inputs=FROZEN_INPUT, names=None,
               check_planarity=True, max_table_rows=None, measure_peak_rss=False):
    if max_table_rows is not None and (type(max_table_rows) is not int or max_table_rows < 0):
        raise ValueError("max_table_rows must be a nonnegative integer or None")
    solver_source = solver_source.resolve()
    helpers = load_helpers(solver_source)
    options = dict(OPTIONS)
    solver_options = dict(options)
    if max_table_rows is not None:
        options["max_table_rows"] = max_table_rows
        if "max_table_rows" in inspect.signature(helpers["four_color_constraints"].solve_constraints).parameters:
            solver_options["max_table_rows"] = max_table_rows
        elif max_table_rows != 100_000:
            raise ValueError("selected solver does not support a configurable storage cap")
    expected_table_rows = 100_000 if max_table_rows is None else max_table_rows
    lab = helpers["four_color_lab"]
    larger = helpers["four_color_larger_experiment"]
    contexts = helpers["four_color_cycle_context_experiment"]
    sources = source_hashes(solver_source)
    driver_hash = sha256(Path(__file__).read_bytes())
    manifest_raw = (EVIDENCE / "baseline-manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    prior_report_raw = (EVIDENCE / "prior-report.json").read_bytes()
    if (manifest["frozen_input_sha256"] != FROZEN_INPUT_SHA256
            or sha256(prior_report_raw) != manifest["prior_report_sha256"]):
        raise AssertionError("frozen baseline manifest or prior report changed")
    baseline_source = (EVIDENCE / "baseline-source/scripts").resolve()
    if solver_source == baseline_source and sources != manifest["source_sha256"]:
        raise AssertionError("baseline source no longer matches its frozen manifest")
    cases, input_bytes = frozen_cases(inputs, lab.graph_fingerprint)
    prior_cases = {case["name"]: case for case in json.loads(prior_report_raw)["cases"]}
    for case in cases:
        if prior_cases[case["name"]]["graph_sha256"] != lab.graph_fingerprint(case["graph"]):
            raise AssertionError("frozen input graph differs from its prior report")
    if names:
        requested = set(names)
        unknown = requested - {case["name"] for case in cases}
        if unknown:
            raise ValueError(f"unknown frozen case names: {sorted(unknown)}")
        cases = [case for case in cases if case["name"] in requested]
    nx = importlib.import_module("networkx") if check_planarity else None
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "runs").mkdir(exist_ok=True)
    write_frozen(out_dir / "inputs.json", input_bytes)
    write_frozen(out_dir / "baseline-manifest.json", manifest_raw)
    records, timings = [], []
    for position, case in enumerate(cases, 1):
        case_started = perf_counter()
        graph = case["graph"]
        graph_sha256 = lab.graph_fingerprint(graph)
        original_graph_bytes = encoded(graph)
        planar = None
        if nx is not None:
            nx_graph = nx.Graph()
            nx_graph.add_nodes_from(graph["vertices"])
            nx_graph.add_edges_from(graph["edges"])
            planar, embedding = nx.check_planarity(nx_graph)
            if not planar:
                raise AssertionError("original graph failed independent planarity check")
            embedding.check_structure()
        oracle, solutions, reference = None, None, {}
        if case["case_group"] == "gap":
            solutions, checked = helpers["four_color_guarantee_audit"].original_solutions(graph)
            if len(solutions) != case["expected_solution_count"]:
                raise AssertionError("frozen gap/control full solution count changed")
            expected = "colored" if solutions else "unsatisfiable"
            coverage, exact_count = "exhaustive_original_edge_solutions", len(solutions)
            reference = dict(
                method="exhaust original-edge/fixed-color literal assignments",
                assignments_checked=checked, original_solutions=solutions,
            )
        elif case["case_group"] == "structured":
            oracle = helpers["four_color_larger_cases"].create_oracle(case)
            expected = "colored" if oracle.solution_count else "unsatisfiable"
            coverage, exact_count = "exact_structural_projection", oracle.solution_count
        else:
            larger.validate_random_binding(case)
            expected = case["reference"]["status"]
            coverage, exact_count = case["reference"]["coverage"], None
            reference = case["reference"]
            if expected == "colored" and not lab.verify_coloring(graph, reference["colors"]):
                raise AssertionError("frozen independent random witness is invalid")
        rss = dict(peak_rss_before_solve_bytes=peak_rss_bytes()) if measure_peak_rss else {}
        solve_started = perf_counter()
        result = helpers["four_color_constraints"].solve_constraints(graph, **solver_options)
        solve_seconds = perf_counter() - solve_started
        if measure_peak_rss:
            rss["peak_rss_after_solve_bytes"] = peak_rss_bytes()
        if (encoded(graph) != original_graph_bytes or encoded(result["graph"]) != original_graph_bytes
                or result["graph_sha256"] != graph_sha256):
            raise AssertionError("solver changed the literal original graph or fixed colors")
        if (result["max_checks"] != options["max_checks"]
                or result["max_table_rows"] != expected_table_rows):
            raise AssertionError("solver changed the frozen work/storage limits")
        if result["status"] not in (expected, "limit"):
            raise AssertionError("solver disagrees with independent original-source reference")
        larger.validate_trace(graph, result)
        if solutions is not None:
            preservation = contexts.verify_exhaustive_solutions(graph, solutions, result)
        elif oracle is not None:
            preservation = larger.verify_projections(oracle, result, ORACLE_MAX_ROWS)
        elif expected == "colored":
            preservation = larger.verify_reference_witness(graph, result, reference["colors"])
        else:
            preservation = dict(
                coverage="independent_exhaustive_unsat_reference",
                all_solutions_preserved=None, unsat_preservation_vacuous=True,
                complete_solver_run=result["status"] != "limit",
                trace_complete=not result["trace_truncated"],
            )
        metrics = (helpers["four_color_conflict_priority"].pre_elimination_metrics(result)
                   if not result["trace_truncated"] else None)
        relative = f"runs/{case['name']}-{MODE}.json.gz"
        compressed = gzip.compress(encoded(result), mtime=0)
        (out_dir / relative).write_bytes(compressed)
        row = dict(
            status=result["status"], colors=result["colors"], stats=result["stats"],
            metrics=metrics, preservation=preservation,
            cycles=helpers["four_color_combined_experiment"].cycle_summary(result),
            contexts=contexts.context_summary(result),
            trace_truncated=result["trace_truncated"], event_count=result["event_count"],
            stop_detail=result["events"][-1]["detail"] if result["events"] else None,
            full_record=relative, compressed_record_sha256=sha256(compressed),
        )
        records.append(dict(
            name=case["name"], case_group=case["case_group"], role=case.get("role"),
            vertices=len(graph["vertices"]), edges=len(graph["edges"]),
            graph_sha256=graph_sha256,
            source_graph_sha256=lab.graph_fingerprint(dict(graph, fixed=[])),
            planar_verified=planar, reference_status=expected,
            reference_coverage=coverage, exact_solution_count=exact_count,
            independent_reference=reference, results={MODE: row},
        ))
        if measure_peak_rss:
            rss["peak_rss_after_serialization_bytes"] = peak_rss_bytes()
        timings.append(dict(name=case["name"], solver_seconds=solve_seconds,
                            case_seconds=perf_counter() - case_started, **rss))
        print(f"{position}/{len(cases)} {case['name']}: {result['status']}, "
              f"checks={result['stats']['checks']}, "
              f"eliminations={result['stats']['eliminations']}", flush=True)
    verify_module_sources(solver_source)
    if (source_hashes(solver_source) != sources
            or sha256(Path(__file__).read_bytes()) != driver_hash
            or inputs.read_bytes() != input_bytes
            or (EVIDENCE / "baseline-manifest.json").read_bytes() != manifest_raw
            or (EVIDENCE / "prior-report.json").read_bytes() != prior_report_raw):
        raise AssertionError("experiment sources or frozen references changed during run")
    report = dict(
        schema="four-color-flow-optimization-v1", case_count=len(cases),
        cases=records, totals=totals_for(records), selected_cases=[case["name"] for case in cases],
        input_file="inputs.json", inputs_sha256=sha256(input_bytes),
        frozen_source_input="artifacts/four_color_flow_optimization/prior-inputs.json",
        baseline_manifest_file="baseline-manifest.json", baseline_manifest_sha256=sha256(manifest_raw),
        baseline_commit=manifest["base_commit"], prior_report_sha256=sha256(prior_report_raw),
        solver_source_kind="frozen-baseline" if solver_source == baseline_source else "selected-source",
        sources=sources, driver_sha256=driver_hash, options=options,
        oracle_max_rows=ORACLE_MAX_ROWS, modes={MODE: options},
        python=sys.version.split()[0], networkx=nx.__version__ if nx else None,
        interpretation=(
            "Forty frozen finite original graph/fixed-color contexts; no general graph coverage. "
            "Same work/storage and discovery budgets for each selected solver source. "
            "Four gap controls retain all independently enumerated original-edge solutions; "
            "24 structured cases check exact global projections subject to explicit row limits. "
            "Twelve random cases retain one frozen independent SAT witness or a frozen exhaustive "
            "UNSAT reference, never all-SAT-solution coverage. Complete saved input relations, "
            "domains and reconstruction fibres are checked. Limits remain inconclusive; trace "
            "or projection limits reduce recorded coverage. Timings are separate and do not "
            "determine correctness or reproducibility. No early speculative coloring."
        ),
    )
    (out_dir / "report.json").write_bytes(encoded(report))
    timing_report = dict(
        schema="four-color-flow-timings-v1", cases=timings,
        total_solver_seconds=sum(row["solver_seconds"] for row in timings),
        total_case_seconds=sum(row["case_seconds"] for row in timings),
        interpretation="Wall-clock observations only; excluded from deterministic evidence comparison.",
    )
    if measure_peak_rss:
        timing_report["memory_measurement"] = dict(
            metric="resource.getrusage(RUSAGE_SELF).ru_maxrss", units="bytes",
            platform=sys.platform, process_cases=len(cases),
            interpretation="Process-lifetime high-water marks; not incremental or solver-only allocation.",
        )
    (out_dir / "timings.json").write_bytes(encoded(timing_report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--solver-source", type=Path, default=ROOT / "scripts")
    parser.add_argument("--inputs", type=Path, default=FROZEN_INPUT)
    parser.add_argument("--case", action="append", nargs="+", dest="cases",
                        help="select frozen case names; repeat this option or list several names")
    parser.add_argument("--skip-planarity", action="store_true",
                        help="retain frozen input identity but omit the independent planarity replay")
    parser.add_argument("--max-table-rows", type=int,
                        help="explicit storage cap; omitted preserves historical solver default")
    parser.add_argument("--measure-peak-rss", action="store_true",
                        help="record process peak RSS in timings.json only")
    args = parser.parse_args()
    names = [name for group in (args.cases or []) for name in group]
    report = experiment(args.out_dir, solver_source=args.solver_source,
                        inputs=args.inputs, names=names,
                        check_planarity=not args.skip_planarity,
                        max_table_rows=args.max_table_rows, measure_peak_rss=args.measure_peak_rss)
    print(json.dumps(report["totals"], ensure_ascii=False, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
