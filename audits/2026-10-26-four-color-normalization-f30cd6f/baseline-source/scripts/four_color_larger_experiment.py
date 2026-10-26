#!/usr/bin/env python3
"""Finite, conflict-first comparison on larger original graphs.

Structured cases have graph-bound exact projection oracles.  Random cases have
an independent literal-edge search reference, with only one-witness coverage
for SAT.  Both preserve their explicit UNKNOWN/limit boundaries.  No timing.
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
from four_color_larger_cases import ProjectionLimit, create_oracle, generate_cases
from four_color_larger_random import generate_random_cases


ROOT = Path(__file__).resolve().parents[1]
MODES = ("base", "intersections")


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def validate_random_binding(case):
    """Bind a frozen reference to its exact original graph and fixed frame.

    This detects accidental source drift; an UNSAT reference remains a saved
    independent-search result, rather than a new proof inferred from a hash.
    """
    graph = case["graph"]
    if case.get("graph_sha256") != graph_fingerprint(graph):
        raise ValueError("frozen random reference does not match its original graph/fixed colors")
    if case.get("source_graph_sha256") != graph_fingerprint(dict(graph, fixed=[])):
        raise ValueError("frozen random context does not match its unfixed source graph")


def validate_trace(graph, result):
    fixed = dict(graph["fixed"])
    for event in result["events"]:
        if event["phase"] == "reduce":
            if event["colors"] != [fixed.get(v, -1) for v in graph["vertices"]]:
                raise AssertionError("unfixed color written before full elimination")
        if event["kind"] == "writeback" and event["depth"] != len(graph["vertices"]):
            raise AssertionError("writeback before all original variables eliminated")
    if result["status"] == "colored" and not verify_coloring(graph, result["colors"]):
        raise AssertionError("returned witness violates original edges or fixed colors")


def verify_projections(oracle, result, max_rows):
    """Compare every saved relation against its exact GLOBAL source projection."""
    cache, omitted = {}, {}
    checks = Counter()

    def projection(scope):
        key = tuple(scope)
        if key not in cache and key not in omitted:
            try:
                cache[key] = oracle.project(key, max_rows=max_rows)
            except ProjectionLimit as limit:
                omitted[key] = dict(scope=list(key), rows=limit.row_count,
                                    limit=limit.max_rows)
        return cache.get(key)

    supports = [projection((vertex,)) for vertex in oracle.graph["vertices"]]
    for event in result["events"]:
        if event["phase"] != "reduce":
            continue
        for allowed, domain in zip(supports, event["domains"]):
            if allowed is not None and not {row[0] for row in allowed} <= set(domain):
                raise AssertionError("an original global solution lost a reduction-domain value")
            checks["reduction_domains"] += 1
    for record in result["elimination_records"]:
        for domain in record["source_domains"]:
            allowed = projection((domain["vertex"],))
            if allowed is not None and not {row[0] for row in allowed} <= set(domain["colors"]):
                raise AssertionError("an original global solution lost a saved source-domain value")
            checks["source_domains"] += 1
        for relation in record["input_relations"]:
            allowed = projection(relation["scope"])
            if allowed is not None and not allowed <= {tuple(row) for row in relation["rows"]}:
                raise AssertionError("an original global solution lost a complete input row")
            checks["input_relations"] += 1
        saved = {tuple(row["boundary"]): set(row["colors"]) for row in record["rows"]}
        allowed = projection([record["vertex"], *record["scope"]])
        if allowed is not None:
            for row in allowed:
                if row[1:] not in saved or row[0] not in saved[row[1:]]:
                    raise AssertionError("an original global solution lost a reconstruction choice")
                checks["saved_choices"] += 1
    return dict(
        coverage="all_global_solutions_in_saved_records" if not omitted else "projection_limit_partial",
        complete_projections_checked=not omitted,
        complete_solver_run=result["status"] != "limit",
        trace_complete=not result["trace_truncated"],
        exact_global_solution_count=oracle.solution_count,
        unsat_preservation_vacuous=oracle.solution_count == 0,
        checks=dict(checks), distinct_scopes=len(cache),
        projection_rows=sum(map(len, cache.values())),
        projection_limits=list(omitted.values()),
    )


def verify_reference_witness(graph, result, colors):
    """Retain the independently supplied witness; no all-solutions claim."""
    if not verify_coloring(graph, colors):
        raise AssertionError("invalid independent source witness")
    assignment = dict(zip(graph["vertices"], colors))
    for event in result["events"]:
        if event["phase"] == "reduce" and any(
                color not in domain for color, domain in zip(colors, event["domains"])):
            raise AssertionError("independent witness lost a reduction-domain value")
    for record in result["elimination_records"]:
        if any(assignment[entry["vertex"]] not in entry["colors"]
               for entry in record["source_domains"]):
            raise AssertionError("independent witness lost a source-domain value")
        for relation in record["input_relations"]:
            if tuple(assignment[v] for v in relation["scope"]) not in {
                    tuple(row) for row in relation["rows"]}:
                raise AssertionError("independent witness lost an input row")
        saved = {tuple(row["boundary"]): row["colors"] for row in record["rows"]}
        boundary = tuple(assignment[v] for v in record["scope"])
        if assignment[record["vertex"]] not in saved.get(boundary, []):
            raise AssertionError("independent witness lost a reconstruction choice")
    return dict(coverage="one_reference_witness_in_saved_records", witness_preserved=True,
                complete_solver_run=result["status"] != "limit",
                trace_complete=not result["trace_truncated"], all_solutions_preserved=None)


def build_inputs():
    return [dict(case, case_group="structured") for case in generate_cases()] + [
        dict(case, case_group="random") for case in generate_random_cases()]


def experiment(out_dir, *, inputs=None, max_checks=5_000_000, oracle_max_rows=100_000):
    import networkx as nx

    cases = build_inputs() if inputs is None else inputs
    if len(cases) != 36 or len({case["name"] for case in cases}) != 36:
        raise ValueError("this frozen experiment requires its 36 distinct named contexts")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "runs").mkdir(exist_ok=True)
    input_bytes = encoded(cases)
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
        for mode in MODES:
            result = solve_constraints(graph, use_intersections=mode == "intersections",
                                       use_conflicts=False, use_c5=False,
                                       record_relations=True, trace_limit=5000,
                                       max_checks=max_checks)
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
                preservation = dict(coverage="independent_exhaustive_unsat_reference" if expected == "unsatisfiable"
                                    else "reference_unknown", all_solutions_preserved=None)
            metrics = pre_elimination_metrics(result) if not result["trace_truncated"] else None
            relative = f"runs/{case['name']}-{mode}.json.gz"
            compressed = gzip.compress(encoded(result), mtime=0)
            (out_dir / relative).write_bytes(compressed)
            results[mode] = dict(status=result["status"], colors=result["colors"],
                                 stats=result["stats"], metrics=metrics,
                                 preservation=preservation,
                                 trace_truncated=result["trace_truncated"],
                                 event_count=result["event_count"],
                                 stop_detail=result["events"][-1]["detail"] if result["events"] else None,
                                 full_record=relative,
                                 compressed_record_sha256=hashlib.sha256(compressed).hexdigest())
        record = dict(name=case["name"], case_group=case["case_group"],
                      vertices=len(graph["vertices"]), edges=len(graph["edges"]),
                      graph_sha256=graph_fingerprint(graph), planar_verified=True,
                      reference_status=expected,
                      exact_solution_count=oracle.solution_count if oracle is not None else None,
                      reference_coverage="exact_structural_projection" if oracle is not None else case["reference"]["coverage"],
                      results=results)
        records.append(record)
        print(f"{index + 1}/36 {case['name']}: " + ", ".join(
            f"{mode}={row['status']}" for mode, row in results.items()), flush=True)
    totals = {}
    for group in ("structured", "random", "all"):
        rows = [record for record in records if group == "all" or record["case_group"] == group]
        totals[group] = {}
        for mode in MODES:
            data = [record["results"][mode] for record in rows]
            totals[group][mode] = dict(
                cases=len(data), status_counts=dict(Counter(row["status"] for row in data)),
                early_conflicts=sum(bool(row["metrics"] and row["metrics"]["early_conflict"]) for row in data),
                initial_color_prunes=sum(row["metrics"]["color_prunes_before_first_elimination"]
                                         for row in data if row["metrics"]),
                projection_limits=sum(bool(row["preservation"].get("projection_limits")) for row in data),
                truncated_traces=sum(row["trace_truncated"] for row in data))
    sources = ["scripts/" + name for name in (
        "four_color_larger_experiment.py", "four_color_larger_cases.py", "four_color_larger_random.py",
        "four_color_conflict_priority.py", "four_color_intersection_experiment.py",
        "four_color_intersections.py", "four_color_constraints.py", "four_color_lab.py",
        "four_color_serialization.py", "four_color_joint_consistency.py",
        "four_color_examples.py", "four_color_c5.py", "four_color_conflicts.py")]
    sources.append("tools/tests/test_four_color_larger_cases.py")
    report = dict(schema="four-color-larger-conflict-priority-v1", cases=records, totals=totals,
                  input_file="inputs.json", inputs_sha256=hashlib.sha256(input_bytes).hexdigest(),
                  options=dict(max_checks=max_checks, oracle_max_rows=oracle_max_rows,
                               use_conflicts=False, use_c5=False, record_relations=True, trace_limit=5000),
                  sources={name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources},
                  python=sys.version.split()[0], networkx=nx.__version__,
                  interpretation="Finite cases, not general planar-graph coverage. Limit remains inconclusive. Structured scope projections are exact; random SAT checks preserve one independently supplied witness only. No timing criterion.")
    (out_dir / "report.json").write_bytes(encoded(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("artifacts/four_color_larger_structures"))
    parser.add_argument("--inputs", type=Path, help="replay frozen original graphs and references")
    parser.add_argument("--max-checks", type=int, default=5_000_000)
    parser.add_argument("--oracle-max-rows", type=int, default=100_000)
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_text()) if args.inputs else None
    report = experiment(args.out_dir, inputs=inputs, max_checks=args.max_checks,
                        oracle_max_rows=args.oracle_max_rows)
    print(json.dumps(report["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
