#!/usr/bin/env python3
"""Compare common-context cycle propagation on forty frozen original graphs.

Both modes already use complete shared-interface intersections and ordinary
original-cycle closure.  Only conditional common-context propagation differs.
The four gap/control graphs have independently enumerated full solutions;
twenty-four structured graphs have exact global projection oracles; twelve
random graphs retain their frozen one-witness/exhaustive-reference boundary.
There is no timing criterion and no uniqueness requirement.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

from four_color_combined_experiment import (
    FROZEN_INPUT as LARGER_INPUT,
    FROZEN_INPUT_SHA256 as LARGER_INPUT_SHA256,
    cycle_summary,
    encoded,
    frozen_cases as frozen_larger_cases,
    source_hashes as combined_sources,
)
from four_color_conflict_priority import pre_elimination_metrics, verify_preservation
from four_color_constraints import solve_constraints
from four_color_guarantee_audit import original_solutions
from four_color_lab import graph_fingerprint, verify_coloring
from four_color_larger_cases import create_oracle
from four_color_larger_experiment import (
    validate_random_binding,
    validate_trace,
    verify_projections,
    verify_reference_witness,
)


ROOT = Path(__file__).resolve().parents[1]
GAP_INPUT = ROOT / "artifacts/four_color_guarantee_gap/inputs.json"
GAP_INPUT_SHA256 = "624fa536d4d2fe060cb024252cfae18c66f928ac2931d8a301b12ccc0104e090"
MODES = {
    "combined": {"use_cycle_contexts": False},
    "combined-contexts": {"use_cycle_contexts": True},
}


def source_hashes():
    """Bind the solver, complete oracle/trace dependencies and current tests."""
    sources = combined_sources()
    names = [
        "scripts/four_color_guarantee_audit.py",
        "scripts/four_color_cycle_context_experiment.py",
    ]
    # Include every context helper, while preserving the explicit imported
    # dependency list supplied by combined_sources().  Tests are included there.
    names.extend(str(path.relative_to(ROOT)) for path in sorted(
        (ROOT / "scripts").glob("four_color_cycle_context*.py")))
    for name in names:
        sources[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return dict(sorted(sources.items()))


def frozen_inputs(gap_path, larger_path):
    """Accept only exact byte copies of both earlier frozen input sources."""
    gap_raw = gap_path.read_bytes()
    if hashlib.sha256(gap_raw).hexdigest() != GAP_INPUT_SHA256:
        raise ValueError("gap inputs must be the unchanged frozen four-case source")
    gap_cases = json.loads(gap_raw)
    if (len(gap_cases) != 4 or
            [case["expected_solution_count"] for case in gap_cases] != [0, 6, 90, 0]):
        raise ValueError("unexpected frozen gap/control references")
    for case in gap_cases:
        graph = case["graph"]
        if case["graph_sha256"] != graph_fingerprint(graph):
            raise ValueError("gap reference does not match its original graph/fixed colors")
        if case["source_graph_sha256"] != graph_fingerprint(dict(graph, fixed=[])):
            raise ValueError("gap reference does not match its unfixed original source")
    larger_cases, larger_raw = frozen_larger_cases(larger_path)
    cases = [dict(case, case_group="gap") for case in gap_cases] + larger_cases
    if len({case["name"] for case in cases}) != 40:
        raise ValueError("forty distinct original contexts are required")
    return cases, gap_raw, larger_raw


def context_summary(result):
    """Keep context-query provenance beside the complete compressed trace."""
    return dict(
        stats={key: value for key, value in result["stats"].items()
               if key.startswith("cycle_context")},
        metadata={key: value for key, value in result.items()
                  if key.startswith("cycle_context")},
        recorded_events=dict(Counter(event["kind"] for event in result["events"]
                                     if "context" in event["kind"])),
    )


def verify_exhaustive_solutions(graph, solutions, result):
    """Check every independently enumerated original solution, including limits."""
    if result["status"] != "limit":
        answer = verify_preservation(graph, solutions, result)
    else:
        # Limits do not prove a decision.  They still permit checking every
        # recorded domain and complete saved row against all original solutions.
        for colors in solutions:
            verify_reference_witness(graph, result, colors)
        answer = dict(all_solutions_preserved=True, witness_verified=False,
                      no_early_writeback_verified=True)
    answer.update(
        coverage="all_original_solutions_in_saved_records",
        exact_global_solution_count=len(solutions),
        unsat_preservation_vacuous=not solutions,
        complete_solver_run=result["status"] != "limit",
        trace_complete=not result["trace_truncated"],
    )
    return answer


def comparison(results):
    old = results["combined"]["metrics"]
    new = results["combined-contexts"]["metrics"]
    before = old["eliminations_before_first_conflict"] if old else None
    after = new["eliminations_before_first_conflict"] if new else None
    return dict(
        statuses_agree=len({row["status"] for row in results.values()}) == 1,
        conflict_earlier_with_contexts=(
            after < before if after is not None and before is not None else None),
        eliminations_before_conflict_combined=before,
        eliminations_before_conflict_combined_contexts=after,
        extra_candidate_prunes_before_first_elimination=(
            old["candidate_count_before_first_elimination"]
            - new["candidate_count_before_first_elimination"]
            if old is not None and new is not None else None),
    )


def totals_for(records):
    totals = {}
    for group in ("gap", "structured", "random", "all"):
        rows = [record for record in records
                if group == "all" or record["case_group"] == group]
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
                projection_limits=sum(bool(row["preservation"].get("projection_limits"))
                                      for row in data),
                truncated_traces=sum(row["trace_truncated"] for row in data),
                preservation_coverage=dict(Counter(
                    row["preservation"]["coverage"] for row in data)),
            )
    return totals


def experiment(out_dir, *, gap_inputs=GAP_INPUT, larger_inputs=LARGER_INPUT,
               max_checks=5_000_000, oracle_max_rows=100_000,
               cycle_max_cycles=128, cycle_max_scan_steps=200_000,
               cycle_context_max_contexts=128,
               cycle_context_max_scan_steps=200_000,
               cycle_context_search="neighbours"):
    import networkx as nx

    if any(type(value) is not int or value < 0 for value in (
            max_checks, oracle_max_rows, cycle_max_cycles, cycle_max_scan_steps,
            cycle_context_max_contexts, cycle_context_max_scan_steps)):
        raise ValueError("experiment limits must be nonnegative integers")
    if cycle_context_search not in ("neighbours", "partial"):
        raise ValueError("cycle_context_search must be neighbours or partial")
    cases, gap_raw, larger_raw = frozen_inputs(gap_inputs, larger_inputs)
    sources = source_hashes()
    options = dict(
        max_checks=max_checks, oracle_max_rows=oracle_max_rows,
        use_substructures=True, use_intersections=True, use_cycles=True,
        use_conflicts=False, use_c5=False, record_relations=True, trace_limit=5000,
        cycle_max_cycles=cycle_max_cycles, cycle_max_scan_steps=cycle_max_scan_steps,
        cycle_context_max_contexts=cycle_context_max_contexts,
        cycle_context_max_scan_steps=cycle_context_max_scan_steps,
        cycle_context_search=cycle_context_search,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "runs").mkdir(exist_ok=True)
    input_bytes = encoded(cases)
    frozen_files = {"inputs.json": input_bytes, "gap-inputs.json": gap_raw,
                    "larger-inputs.json": larger_raw}
    for name, data in frozen_files.items():
        path = out_dir / name
        if path.exists() and path.read_bytes() != data:
            raise AssertionError(f"refusing to replace different frozen input: {name}")
        path.write_bytes(data)

    records = []
    for index, case in enumerate(cases):
        graph = case["graph"]
        nx_graph = nx.Graph()
        nx_graph.add_nodes_from(graph["vertices"])
        nx_graph.add_edges_from(graph["edges"])
        planar, embedding = nx.check_planarity(nx_graph)
        if not planar:
            raise AssertionError("original graph failed independent planarity check")
        embedding.check_structure()
        oracle = create_oracle(case) if case["case_group"] == "structured" else None
        solutions = None
        reference = {}
        if case["case_group"] == "gap":
            solutions, checked = original_solutions(graph)
            if len(solutions) != case["expected_solution_count"]:
                raise AssertionError("frozen gap/control full solution count changed")
            expected = "colored" if solutions else "unsatisfiable"
            coverage = "exhaustive_original_edge_solutions"
            exact_count = len(solutions)
            reference = dict(
                method="exhaust literal original-vertex assignments; inspect original edges and fixed colors only",
                assignments_checked=checked, original_solutions=solutions,
            )
        elif oracle is not None:
            expected = "colored" if oracle.solution_count else "unsatisfiable"
            coverage = "exact_structural_projection"
            exact_count = oracle.solution_count
        else:
            validate_random_binding(case)
            expected = case["reference"]["status"]
            coverage = case["reference"]["coverage"]
            exact_count = None
            if expected == "colored" and not verify_coloring(graph, case["reference"]["colors"]):
                raise AssertionError("frozen random source witness is invalid")
        results = {}
        for mode, mode_options in MODES.items():
            result = solve_constraints(
                graph, **mode_options, use_substructures=True, use_intersections=True,
                use_cycles=True, use_conflicts=False, use_c5=False,
                record_relations=True, trace_limit=options["trace_limit"],
                max_checks=max_checks, cycle_max_cycles=cycle_max_cycles,
                cycle_max_scan_steps=cycle_max_scan_steps,
                cycle_context_max_contexts=cycle_context_max_contexts,
                cycle_context_max_scan_steps=cycle_context_max_scan_steps,
                cycle_context_search=(cycle_context_search
                                      if mode_options["use_cycle_contexts"] else "neighbours"),
            )
            if result["graph_sha256"] != graph_fingerprint(graph):
                raise AssertionError("main solver changed the original graph")
            if expected != "limit" and result["status"] not in (expected, "limit"):
                raise AssertionError("solver disagrees with independent original-source reference")
            validate_trace(graph, result)
            if solutions is not None:
                preservation = verify_exhaustive_solutions(graph, solutions, result)
            elif oracle is not None:
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
                cycles=cycle_summary(result), contexts=context_summary(result),
                trace_truncated=result["trace_truncated"], event_count=result["event_count"],
                stop_detail=result["events"][-1]["detail"] if result["events"] else None,
                full_record=relative,
                compressed_record_sha256=hashlib.sha256(compressed).hexdigest(),
            )
        records.append(dict(
            name=case["name"], case_group=case["case_group"],
            role=case.get("role"), vertices=len(graph["vertices"]), edges=len(graph["edges"]),
            graph_sha256=graph_fingerprint(graph), planar_verified=True,
            reference_status=expected, exact_solution_count=exact_count,
            reference_coverage=coverage, independent_reference=reference,
            results=results, comparison=comparison(results),
        ))
        print(f"{index + 1}/40 {case['name']}: " + ", ".join(
            f"{mode}={row['status']},eliminations={row['stats']['eliminations']}"
            for mode, row in results.items()), flush=True)

    if source_hashes() != sources:
        raise AssertionError("experiment sources changed during run; replay after edits finish")
    report = dict(
        schema="four-color-cycle-contexts-conflict-priority-v1",
        cases=records, totals=totals_for(records), input_file="inputs.json",
        inputs_sha256=hashlib.sha256(input_bytes).hexdigest(),
        frozen_source_inputs={
            "gap": dict(source="artifacts/four_color_guarantee_gap/inputs.json",
                        copy="gap-inputs.json", sha256=GAP_INPUT_SHA256),
            "larger": dict(source="artifacts/four_color_larger_structures/inputs.json",
                           copy="larger-inputs.json", sha256=LARGER_INPUT_SHA256),
        },
        options=options, modes=MODES, sources=sources,
        python=sys.version.split()[0], networkx=nx.__version__,
        interpretation=(
            "Finite frozen cases, not general planar-graph coverage. Both modes use "
            "intersections and original-cycle closure; only common-context cycle "
            "propagation differs. Gap/control solutions are independently exhausted "
            "against original edges and fixed colors. Structured projections compare "
            "every saved scope with all global solutions, subject to explicit projection "
            "limits. Random SAT cases preserve one frozen independent witness only; "
            "random UNSAT statuses use frozen exhaustive-search references. Domains, "
            "original input relations and saved complete reconstruction choices are "
            "checked without requiring a unique solution. Discovery and relation caps "
            "may omit optional propagators; a finished prescribed cycle scan is not an "
            "all-cycles claim. Limits remain inconclusive; truncated traces reduce "
            "recorded coverage. No timing criterion or speculative writeback."
        ),
    )
    (out_dir / "report.json").write_bytes(encoded(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path,
                        default=Path("artifacts/four_color_cycle_contexts"))
    parser.add_argument("--gap-inputs", type=Path, default=GAP_INPUT)
    parser.add_argument("--larger-inputs", type=Path, default=LARGER_INPUT)
    parser.add_argument("--max-checks", type=int, default=5_000_000)
    parser.add_argument("--oracle-max-rows", type=int, default=100_000)
    parser.add_argument("--cycle-max-cycles", type=int, default=128)
    parser.add_argument("--cycle-max-scan-steps", type=int, default=200_000)
    parser.add_argument("--cycle-context-max-contexts", type=int, default=128)
    parser.add_argument("--cycle-context-max-scan-steps", type=int, default=200_000)
    parser.add_argument("--cycle-context-search", choices=("neighbours", "partial"),
                        default="neighbours")
    args = parser.parse_args()
    report = experiment(
        args.out_dir, gap_inputs=args.gap_inputs, larger_inputs=args.larger_inputs,
        max_checks=args.max_checks, oracle_max_rows=args.oracle_max_rows,
        cycle_max_cycles=args.cycle_max_cycles,
        cycle_max_scan_steps=args.cycle_max_scan_steps,
        cycle_context_max_contexts=args.cycle_context_max_contexts,
        cycle_context_max_scan_steps=args.cycle_context_max_scan_steps,
        cycle_context_search=args.cycle_context_search,
    )
    print(json.dumps(report["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
