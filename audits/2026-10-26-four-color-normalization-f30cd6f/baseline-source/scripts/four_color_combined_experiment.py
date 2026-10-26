#!/usr/bin/env python3
"""Compare intersections and original-cycle propagation on 36 frozen graphs.

The same original graph and literal fixed colors feed all three modes.  The
objective is conflict detection and candidate reduction before elimination;
there are no timing criteria.  Structured cases have exact global projection
oracles, while random SAT cases check one frozen independent witness only.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

from four_color_conflict_priority import pre_elimination_metrics
from four_color_constraints import solve_constraints
from four_color_lab import graph_fingerprint, verify_coloring
from four_color_larger_cases import create_oracle
from four_color_larger_experiment import (
    validate_random_binding,
    validate_trace,
    verify_projections,
    verify_reference_witness,
)


ROOT = Path(__file__).resolve().parents[1]
FROZEN_INPUT = ROOT / "artifacts/four_color_larger_structures/inputs.json"
FROZEN_INPUT_SHA256 = "60b37010d4cec3cf6c079f9f2f46a255defe5d3092a561fe3669316efe68bf81"
MODES = {
    "base": {"use_intersections": False, "use_cycles": False},
    "intersections": {"use_intersections": True, "use_cycles": False},
    "combined": {"use_intersections": True, "use_cycles": True},
}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def source_hashes():
    """Bind solver, oracle, validation, scanner and regression-test sources."""
    paths = ["scripts/" + name for name in (
        "four_color_combined_experiment.py", "four_color_larger_experiment.py",
        "four_color_larger_cases.py", "four_color_larger_random.py",
        "four_color_conflict_priority.py", "four_color_intersection_experiment.py",
        "four_color_intersections.py", "four_color_constraints.py",
        "four_color_serialization.py", "four_color_joint_consistency.py",
        "four_color_lab.py", "four_color_examples.py", "four_color_c5.py",
        "four_color_cycle_structure.py", "four_color_conflicts.py",
        "four_color_local_information.py", "four_color_cycle_propagation.py",
    )]
    paths.append("tools/four_color_lab_viewer.html")
    paths.extend(str(path.relative_to(ROOT)) for path in sorted(
        (ROOT / "tools/tests").glob("test_four_color_*.py")))
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in sorted(set(paths))}


def frozen_cases(path):
    """Accept only an exact byte copy of the original 36-case experiment."""
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != FROZEN_INPUT_SHA256:
        raise ValueError("inputs must be the unchanged frozen 36-case source")
    cases = json.loads(raw)
    if len(cases) != 36 or len({case["name"] for case in cases}) != 36:
        raise ValueError("this frozen experiment requires 36 distinct named contexts")
    if Counter(case["case_group"] for case in cases) != {"structured": 24, "random": 12}:
        raise ValueError("unexpected structured/random source split")
    return cases, raw


def cycle_summary(result):
    """Keep cycle provenance available beside the complete compressed trace."""
    return dict(
        stats={key: value for key, value in result["stats"].items()
               if key.startswith("cycle")},
        scan=result.get("cycle_scan"),
        substructures={key: value for key, value in result.get("substructures", {}).items()
                       if key.startswith("cycle")},
        recorded_events=dict(Counter(event["kind"] for event in result["events"]
                                     if event["kind"].startswith("cycle"))),
    )


def comparison(results):
    """Report earlier contradiction detection without treating UNSAT as a fault."""
    old = results["intersections"]["metrics"]
    new = results["combined"]["metrics"]
    before = old["eliminations_before_first_conflict"] if old else None
    after = new["eliminations_before_first_conflict"] if new else None
    return dict(
        statuses_agree=len({result["status"] for result in results.values()}) == 1,
        combined_conflict_earlier_than_intersections=(
            after < before if after is not None and before is not None else None),
        eliminations_before_conflict_intersections=before,
        eliminations_before_conflict_combined=after,
        extra_candidate_prunes_before_first_elimination=(
            old["candidate_count_before_first_elimination"]
            - new["candidate_count_before_first_elimination"]
            if old is not None and new is not None else None),
    )


def experiment(out_dir, *, inputs=FROZEN_INPUT, max_checks=5_000_000,
               oracle_max_rows=100_000, cycle_max_cycles=128,
               cycle_max_scan_steps=200_000):
    import networkx as nx

    if any(type(value) is not int or value < 0 for value in (
            max_checks, oracle_max_rows, cycle_max_cycles, cycle_max_scan_steps)):
        raise ValueError("experiment limits must be nonnegative integers")
    cases, input_bytes = frozen_cases(inputs)
    sources = source_hashes()
    options = dict(
        max_checks=max_checks, oracle_max_rows=oracle_max_rows,
        use_substructures=True, use_conflicts=False, use_c5=False,
        record_relations=True, trace_limit=5000,
        cycle_max_cycles=cycle_max_cycles, cycle_max_scan_steps=cycle_max_scan_steps,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "runs").mkdir(exist_ok=True)
    (out_dir / "inputs.json").write_bytes(input_bytes)
    records = []
    for index, case in enumerate(cases):
        graph = case["graph"]
        nx_graph = nx.Graph()
        nx_graph.add_nodes_from(graph["vertices"])
        nx_graph.add_edges_from(graph["edges"])
        if not nx.check_planarity(nx_graph)[0]:
            raise AssertionError("original graph failed independent planarity check")
        oracle = create_oracle(case) if case["case_group"] == "structured" else None
        if oracle is not None:
            expected = "colored" if oracle.solution_count else "unsatisfiable"
        else:
            validate_random_binding(case)
            expected = case["reference"]["status"]
            if expected == "colored" and not verify_coloring(graph, case["reference"]["colors"]):
                raise AssertionError("frozen random reference witness is invalid")
        results = {}
        for mode, mode_options in MODES.items():
            result = solve_constraints(
                graph, **mode_options, use_substructures=options["use_substructures"],
                use_conflicts=False, use_c5=False, record_relations=True,
                trace_limit=options["trace_limit"], max_checks=max_checks,
                cycle_max_cycles=cycle_max_cycles,
                cycle_max_scan_steps=cycle_max_scan_steps,
            )
            if result["graph_sha256"] != graph_fingerprint(graph):
                raise AssertionError("main solver changed the source graph")
            if expected != "limit" and result["status"] not in (expected, "limit"):
                raise AssertionError("solver disagrees with independent source reference")
            validate_trace(graph, result)
            if oracle is not None:
                preservation = verify_projections(oracle, result, oracle_max_rows)
            elif expected == "colored":
                preservation = verify_reference_witness(graph, result, case["reference"]["colors"])
            else:
                preservation = dict(
                    coverage=("independent_exhaustive_unsat_reference"
                              if expected == "unsatisfiable" else "reference_unknown"),
                    all_solutions_preserved=None,
                    complete_solver_run=result["status"] != "limit",
                    trace_complete=not result["trace_truncated"],
                )
            metrics = pre_elimination_metrics(result) if not result["trace_truncated"] else None
            relative = f"runs/{case['name']}-{mode}.json.gz"
            compressed = gzip.compress(encoded(result), mtime=0)
            (out_dir / relative).write_bytes(compressed)
            results[mode] = dict(
                status=result["status"], colors=result["colors"], stats=result["stats"],
                metrics=metrics, preservation=preservation,
                cycles=cycle_summary(result),
                trace_truncated=result["trace_truncated"], event_count=result["event_count"],
                stop_detail=result["events"][-1]["detail"] if result["events"] else None,
                full_record=relative,
                compressed_record_sha256=hashlib.sha256(compressed).hexdigest(),
            )
        records.append(dict(
            name=case["name"], case_group=case["case_group"],
            vertices=len(graph["vertices"]), edges=len(graph["edges"]),
            graph_sha256=graph_fingerprint(graph), planar_verified=True,
            reference_status=expected,
            exact_solution_count=oracle.solution_count if oracle is not None else None,
            reference_coverage=("exact_structural_projection" if oracle is not None
                                else case["reference"]["coverage"]),
            results=results, comparison=comparison(results),
        ))
        print(f"{index + 1}/36 {case['name']}: " + ", ".join(
            f"{mode}={row['status']}" for mode, row in results.items()), flush=True)
    totals = {}
    for group in ("structured", "random", "all"):
        rows = [record for record in records if group == "all" or record["case_group"] == group]
        totals[group] = {}
        for mode in MODES:
            data = [record["results"][mode] for record in rows]
            metrics = [row["metrics"] for row in data if row["metrics"] is not None]
            totals[group][mode] = dict(
                cases=len(data), status_counts=dict(Counter(row["status"] for row in data)),
                early_conflicts=sum(row["early_conflict"] for row in metrics),
                initial_color_prunes=sum(row["color_prunes_before_first_elimination"]
                                         for row in metrics),
                candidates_before_first_elimination=sum(
                    row["candidate_count_before_first_elimination"] for row in metrics),
                row_prunes_before_first_elimination=sum(
                    row["row_prunes_before_first_elimination"] for row in metrics),
                eliminations_before_conflict=sum(
                    row["eliminations_before_first_conflict"] for row in metrics
                    if row["eliminations_before_first_conflict"] is not None),
                projection_limits=sum(bool(row["preservation"].get("projection_limits")) for row in data),
                truncated_traces=sum(row["trace_truncated"] for row in data),
                preservation_coverage=dict(Counter(row["preservation"]["coverage"] for row in data)),
            )
    if source_hashes() != sources:
        raise AssertionError("experiment source files changed during the run; replay after edits finish")
    report = dict(
        schema="four-color-combined-cycles-conflict-priority-v1",
        cases=records, totals=totals, input_file="inputs.json",
        frozen_source_input="artifacts/four_color_larger_structures/inputs.json",
        inputs_sha256=hashlib.sha256(input_bytes).hexdigest(),
        options=options, modes=MODES, sources=sources,
        python=sys.version.split()[0], networkx=nx.__version__,
        interpretation=(
            "Finite cases, not general planar-graph coverage. Limit remains inconclusive. "
            "Structured projections compare every available saved scope against all global "
            "solutions; explicit projection limits and truncated traces reduce that coverage. "
            "Random SAT cases preserve one independently supplied source witness only; "
            "random UNSAT statuses use frozen exhaustive-search references. "
            "Cycle supports are exact for each selected original cycle under its current "
            "literal domains. Discovery selects fundamental cycles of the original graph "
            "and domain-induced subgraphs; a completed prescribed scan never means all "
            "original cycles were enumerated. Caps may omit further optional propagators. "
            "Intersections and cycles repeat within reduction before exact elimination and "
            "final writeback. No uniqueness requirement and no timing criterion."
        ),
    )
    (out_dir / "report.json").write_bytes(encoded(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("artifacts/four_color_combined_cycles"))
    parser.add_argument("--inputs", type=Path, default=FROZEN_INPUT,
                        help="unchanged frozen 36-case inputs, or an exact byte copy")
    parser.add_argument("--max-checks", type=int, default=5_000_000)
    parser.add_argument("--oracle-max-rows", type=int, default=100_000)
    parser.add_argument("--cycle-max-cycles", type=int, default=128)
    parser.add_argument("--cycle-max-scan-steps", type=int, default=200_000)
    args = parser.parse_args()
    report = experiment(
        args.out_dir, inputs=args.inputs, max_checks=args.max_checks,
        oracle_max_rows=args.oracle_max_rows,
        cycle_max_cycles=args.cycle_max_cycles,
        cycle_max_scan_steps=args.cycle_max_scan_steps,
    )
    print(json.dumps(report["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
