#!/usr/bin/env python3
"""Freeze and audit local-consistency gaps without changing the solver.

Complete original-edge assignments supply independent SAT/UNSAT references.
For the two propagation gaps, independently enumerated original simple cycles
are checked by literal cycle assignment enumeration, then compared with the
existing cycle DP.  This is a finite audit, not a general completeness theorem.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

from four_color_combined_experiment import encoded, source_hashes as combined_sources
from four_color_conflict_priority import pre_elimination_metrics, verify_preservation
from four_color_constraints import solve_constraints
from four_color_lab import graph_fingerprint, normalize_graph
from four_color_larger_experiment import validate_trace
from four_color_local_information import derive_cycle


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_SHA256 = "194cc742b9130f0d4d49c73e598aabcc15ce888028a872edb1266b342f892f62"
SECONDARY_SHA256 = "10eb7febb228531089f53d33ab7a9351c4acbdcb17ea502f5271804b178b5cd7"
MODES = {
    "combined": {"use_c5": False},
    "combined-c5-structure": {"use_c5": True},
}
OPTIONS = dict(
    use_substructures=True, use_conflicts=True, use_intersections=True,
    use_cycles=True, c5_method="structure", max_checks=5_000_000,
    cycle_max_cycles=128, cycle_max_scan_steps=200_000,
    record_relations=True, trace_limit=5000,
)


def source_hashes():
    sources = combined_sources()
    relative = "scripts/four_color_guarantee_audit.py"
    sources[relative] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    return dict(sorted(sources.items()))


def wheel(rim, *, free_center_leaf=False):
    """One private leaf per core vertex, in the same literal color frame."""
    return normalize_graph(dict(
        vertices=list(range(2 * (rim + 1))),
        edges=[[v, 1 + v % rim] for v in range(1, rim + 1)]
              + [[0, v] for v in range(1, rim + 1)]
              + [[v, rim + 1 + v] for v in range(rim + 1)],
        fixed=[[rim + 1 + v, 3] for v in range(rim + 1)
               if not (free_center_leaf and v == 0)],
    ))


def build_inputs():
    cases = [
        dict(name="odd-wheel-private-fixed-leaves", role="primary-gap",
             graph=wheel(5), expected_solution_count=0),
        dict(name="even-wheel-private-fixed-leaves", role="even-control",
             graph=wheel(6), expected_solution_count=6),
        dict(name="odd-wheel-free-center-leaf", role="relaxed-control",
             graph=wheel(5, free_center_leaf=True), expected_solution_count=90),
        dict(name="reduced-planar-fixed-gap", role="secondary-gap",
             graph=normalize_graph(dict(
                 vertices=[0, 1, 2, 4, 5, 6, 7, 8, 9],
                 edges=[[0, 1], [0, 2], [0, 5], [0, 8], [1, 2], [1, 4],
                        [1, 5], [1, 6], [2, 4], [2, 8], [2, 9], [4, 6],
                        [4, 7], [4, 9], [5, 6], [5, 7], [5, 8], [6, 7],
                        [7, 8], [7, 9], [8, 9]],
                 fixed=[[0, 0], [6, 3]],
             )), expected_solution_count=0),
    ]
    for case in cases:
        case["graph"]["name"] = case["name"]
        case["graph_sha256"] = graph_fingerprint(case["graph"])
        case["source_graph_sha256"] = graph_fingerprint(dict(case["graph"], fixed=[]))
    if cases[0]["graph_sha256"] != PRIMARY_SHA256:
        raise AssertionError("primary literal graph drifted")
    if cases[3]["graph_sha256"] != SECONDARY_SHA256:
        raise AssertionError("secondary literal graph drifted")
    return cases


def original_solutions(graph):
    """Exhaust all free literal colors; inspect original edges and fixes only."""
    fixed = dict(graph["fixed"])
    free = [v for v in graph["vertices"] if v not in fixed]
    solutions, checked = [], 0
    for choices in product(range(4), repeat=len(free)):
        checked += 1
        assignment = dict(fixed)
        assignment.update(zip(free, choices))
        if all(assignment[a] != assignment[b] for a, b in graph["edges"]):
            solutions.append([assignment[v] for v in graph["vertices"]])
    return solutions, checked


def original_cycles(graph):
    """Enumerate every undirected simple cycle exactly once by canonical DFS.

    Each cycle starts at its least original vertex ID, and is kept only in the
    orientation whose second ID is less than its final ID.  Chords are allowed.
    """
    adjacency = {v: set() for v in graph["vertices"]}
    for a, b in graph["edges"]:
        adjacency[a].add(b)
        adjacency[b].add(a)
    cycles = []
    for start in sorted(graph["vertices"]):
        def visit(path, used):
            for following in sorted(adjacency[path[-1]]):
                if following == start:
                    if len(path) >= 3 and path[1] < path[-1]:
                        cycles.append(tuple(path))
                elif following > start and following not in used:
                    visit(path + [following], used | {following})
        visit([start], {start})
    if len(cycles) != len(set(cycles)):
        raise AssertionError("independent cycle enumerator duplicated a cycle")
    return sorted(cycles)


def brute_cycle(domains):
    """Full local cycle assignments, using inequalities and no DP or factors."""
    supports = [set() for _ in domains]
    row_count = checked = 0
    for row in product(*domains):
        checked += 1
        if all(row[i] != row[(i + 1) % len(row)] for i in range(len(row))):
            row_count += 1
            for support, color in zip(supports, row):
                support.add(color)
    return dict(row_count=row_count, candidate_rows_checked=checked,
                supports=[sorted(support) for support in supports])


def all_cycle_audit(graph, domains):
    allowed = dict(zip(graph["vertices"], domains))
    summaries = []
    for cycle in original_cycles(graph):
        local_domains = [allowed[v] for v in cycle]
        brute = brute_cycle(local_domains)
        dp = derive_cycle([sum(1 << c for c in domain) for domain in local_domains])
        dp_supports = [[c for c in range(4) if mask & (1 << c)]
                       for mask in dp["supports"]]
        if brute["row_count"] != dp["row_count"] or brute["supports"] != dp_supports:
            raise AssertionError("cycle DP disagrees with literal independent enumeration")
        if not brute["row_count"] or brute["supports"] != local_domains:
            raise AssertionError("a claimed full-cycle propagation gap has a pruning cycle")
        summaries.append(dict(cycle=list(cycle), **brute,
                              nonempty=True, full_unary_supports=True, dp_matches=True))
    return dict(
        method=("canonical DFS over original edges, then itertools.product of literal "
                "cycle domains and every consecutive/closing inequality; compare DP"),
        graph_sha256=graph_fingerprint(graph),
        initial_domains=domains, cycles=len(summaries),
        length_histogram=dict(sorted(Counter(len(row["cycle"]) for row in summaries).items())),
        candidate_cycle_rows_checked=sum(row["candidate_rows_checked"] for row in summaries),
        valid_cycle_rows_total=sum(row["row_count"] for row in summaries),
        all_nonempty=True, all_unary_supports_preserved=True,
        all_dp_counts_and_supports_match=True, summaries=summaries,
    )


def initial_snapshot(result):
    before = []
    for event in result["events"]:
        if event["kind"] == "eliminate":
            break
        if event["phase"] == "reduce":
            before.append(event)
    if not before:
        raise AssertionError("missing reduction snapshot")
    snapshot = before[-1]
    return dict(
        domains=snapshot["domains"], stats=snapshot["stats"],
        event_count=len(before), conflict_events=sum(e["kind"] == "conflict" for e in before),
        cycle_queries=sum(e["kind"] == "cycle_query" for e in before),
        intersection_events=sum(e["kind"] == "intersection" for e in before),
    )


def conditioned_hub_audit(graph, domains):
    """Diagnostic full wheel query; no color is committed and solver is unchanged."""
    allowed = dict(zip(graph["vertices"], domains))
    rim = [1, 2, 3, 4, 5]
    edges = {frozenset(edge) for edge in graph["edges"]}
    if not all(frozenset((0, v)) in edges for v in rim):
        raise AssertionError("diagnostic requires every original hub spoke")
    cases = []
    for color in allowed[0]:
        conditioned = [[c for c in allowed[v] if c != color] for v in rim]
        brute = brute_cycle(conditioned)
        if brute["row_count"] != 0:
            raise AssertionError("primary odd-wheel hub color unexpectedly extends")
        cases.append(dict(hub_color=color, rim_domains=conditioned, **brute))
    return dict(hub=0, ordered_rim=rim, hub_cases=cases, feasible_hub_colors=[],
                all_cases_empty=True, diagnostic_only=True, solver_modified=False,
                contract="For a fixed common hub color, check all original spokes and the same original rim cycle.")


def experiment(out_dir):
    import networkx as nx

    sources = source_hashes()
    cases = build_inputs()
    inputs_bytes = encoded(cases)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "runs").mkdir(exist_ok=True)
    inputs_path = out_dir / "inputs.json"
    if inputs_path.exists() and inputs_path.read_bytes() != inputs_bytes:
        raise AssertionError("refusing to replace a different frozen input")
    inputs_path.write_bytes(inputs_bytes)
    records, cycle_audits, cycle_cache = [], {}, {}
    for case in cases:
        graph = case["graph"]
        nx_graph = nx.Graph()
        nx_graph.add_nodes_from(graph["vertices"])
        nx_graph.add_edges_from(graph["edges"])
        planar, embedding = nx.check_planarity(nx_graph)
        if not planar:
            raise AssertionError("original source graph is not planar")
        embedding.check_structure()
        solutions, assignments_checked = original_solutions(graph)
        if len(solutions) != case["expected_solution_count"]:
            raise AssertionError("independent full solution count changed")
        expected = "colored" if solutions else "unsatisfiable"
        results = {}
        for mode, mode_options in MODES.items():
            result = solve_constraints(graph, **OPTIONS, **mode_options)
            if result["status"] != expected or result["trace_truncated"]:
                raise AssertionError("complete solver disagrees with exhaustive source oracle")
            if result["graph_sha256"] != case["graph_sha256"]:
                raise AssertionError("solver source graph drifted")
            validate_trace(graph, result)
            preservation = verify_preservation(graph, solutions, result)
            initial = initial_snapshot(result)
            metrics = pre_elimination_metrics(result)
            required_gap = case["role"] == "primary-gap" or (
                case["role"] == "secondary-gap" and mode == "combined")
            audit_key = None
            if required_gap:
                if initial["conflict_events"] or initial["stats"]["conflicts"]:
                    raise AssertionError("required gap was detected during initial propagation")
                if metrics["eliminations_before_first_conflict"] <= 0:
                    raise AssertionError("gap did not survive until elimination")
                if case["role"] == "primary-gap" and result["stats"]["eliminations"] != 8:
                    raise AssertionError("primary frozen run no longer has eight eliminations")
                signature = (case["graph_sha256"], tuple(map(tuple, initial["domains"])))
                if signature not in cycle_cache:
                    audit_key = f"{case['name']}-initial-{len(cycle_audits) + 1}"
                    cycle_cache[signature] = audit_key
                    cycle_audits[audit_key] = all_cycle_audit(graph, initial["domains"])
                audit_key = cycle_cache[signature]
            relative = f"runs/{case['name']}-{mode}.json.gz"
            compressed = gzip.compress(encoded(result), mtime=0)
            (out_dir / relative).write_bytes(compressed)
            results[mode] = dict(
                status=result["status"], stats=result["stats"], metrics=metrics,
                initial_snapshot=initial, initial_gap_required=required_gap,
                preservation=preservation, full_cycle_audit=audit_key,
                trace_truncated=result["trace_truncated"], event_count=result["event_count"],
                cycle_scan=result["cycle_scan"], full_record=relative,
                compressed_record_sha256=hashlib.sha256(compressed).hexdigest(),
            )
        record = dict(
            name=case["name"], role=case["role"],
            graph_sha256=case["graph_sha256"], source_graph_sha256=case["source_graph_sha256"],
            vertices=len(graph["vertices"]), edges=len(graph["edges"]),
            reference_status=expected, exact_solution_count=len(solutions),
            independent_reference=dict(method="exhaust every literal assignment to free original vertices; inspect only original edges and fixed colors", assignments_checked=assignments_checked, original_solutions=solutions),
            planarity=dict(method="networkx.check_planarity plus embedding.check_structure", networkx=nx.__version__, planar=True, embedding_cw_neighbors={str(v): list(embedding.neighbors_cw_order(v)) for v in graph["vertices"]}),
            results=results,
        )
        if case["role"] == "primary-gap":
            record["conditioned_hub_diagnostic"] = conditioned_hub_audit(
                graph, results["combined"]["initial_snapshot"]["domains"])
        if case["role"] == "secondary-gap":
            unfixed_graph = dict(graph, fixed=[])
            unfixed_solutions, unfixed_checked = original_solutions(unfixed_graph)
            positions = {v: i for i, v in enumerate(graph["vertices"])}
            if unfixed_checked != 4 ** 9 or len(unfixed_solutions) != 48:
                raise AssertionError("secondary unfixed source enumeration changed")
            if not all(colors[positions[0]] == colors[positions[6]]
                       for colors in unfixed_solutions):
                raise AssertionError("secondary source no longer forces c0=c6")
            record["unfixed_source_reference"] = dict(
                graph=unfixed_graph, graph_sha256=graph_fingerprint(unfixed_graph),
                method="exhaust all 4^9 literal original-vertex assignments and inspect original edges only",
                assignments_checked=unfixed_checked, exact_solution_count=48,
                original_solutions=unfixed_solutions, equal_vertices=[0, 6],
                equality_holds_in_every_original_solution=True,
                fixed_context_contradicts_equality=graph["fixed"] == [[0, 0], [6, 3]],
            )
        records.append(record)
        print(case["name"] + ": " + ", ".join(
            f"{mode}={row['status']},eliminations={row['stats']['eliminations']}"
            for mode, row in results.items()), flush=True)
    if source_hashes() != sources:
        raise AssertionError("audit sources changed during run; repeat after edits finish")
    totals = dict(
        cases=len(records), modes=len(MODES), runs=len(records) * len(MODES),
        unique_control_solutions=sum(row["exact_solution_count"] for row in records),
        status_counts=dict(Counter(row["status"] for case in records for row in case["results"].values())),
        limit_results=0, truncated_traces=0, full_cycle_snapshots=len(cycle_audits),
        independently_enumerated_cycles=sum(row["cycles"] for row in cycle_audits.values()),
        all_original_solutions_preserved=True,
    )
    if totals["unique_control_solutions"] != 96:
        raise AssertionError("control solution coverage changed")
    report = dict(
        schema="four-color-local-consistency-guarantee-gap-v1", cases=records,
        all_cycle_audits=cycle_audits, totals=totals, modes=MODES, options=OPTIONS,
        input_file="inputs.json", inputs_sha256=hashlib.sha256(inputs_bytes).hexdigest(),
        sources=sources, python=sys.version.split()[0], networkx=nx.__version__,
        interpretation=("Frozen planar fixed-color counterexamples to inferring global SAT "
                        "from nonempty local propagation. All original simple cycles are "
                        "independently enumerated at the required gap snapshots; every "
                        "cycle retains all unary supports. Complete elimination remains "
                        "responsible for exact final verdicts. Complete original-edge "
                        "solution preservation is checked for both SAT controls, with "
                        "vacuous preservation on UNSAT contexts. No universal graph "
                        "coverage or newly implemented wheel propagator is claimed."),
    )
    (out_dir / "report.json").write_bytes(encoded(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path,
                        default=ROOT / "artifacts/four_color_guarantee_gap")
    args = parser.parse_args()
    report = experiment(args.out_dir.resolve())
    print(json.dumps(report["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
