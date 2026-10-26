#!/usr/bin/env python3
"""Bounded, matched-input comparison of separator relation propagation.

The named controls retain complete relation traces.  Sample runs retain the
original normalized graphs, literal witnesses, deterministic work counters and
all elapsed times, with repeated median times reported separately from work.
This is a finite nonuniform sample, not a universal performance claim.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
from statistics import median
import sys
from time import perf_counter

from four_color_examples import random_triangulation
from four_color_lab import graph_fingerprint, normalize_graph, verify_coloring


MODES = ("base", "intersections")


def named_controls():
    """Small original graphs with independently enumerable literal solutions."""
    triangle = list(combinations(range(3), 2))
    bipyramid = triangle + [(v, hub) for v in range(3) for hub in (3, 4)]
    restricted = bipyramid + [(3, 5), (3, 6)]
    return [
        dict(name="k4_free", expected_status="colored", graph=dict(
            vertices=list(range(4)), edges=[list(e) for e in combinations(range(4), 2)],
            fixed=[]), explanation="Four pairwise adjacent vertices use all four colors."),
        dict(name="bipyramid_restricted_hub", expected_status="colored", graph=dict(
            vertices=list(range(7)), edges=[list(e) for e in restricted],
            fixed=[[5, 2], [6, 3]]), explanation=(
                "ABC is a triangle; both hubs x=3 and y=4 see ABC, so x=y. "
                "Two fixed leaves exclude colors 2 and 3 from x, hence also from y.")),
        dict(name="bipyramid_incompatible_hubs", expected_status="unsatisfiable", graph=dict(
            vertices=list(range(9)),
            edges=[list(e) for e in restricted + [(4, 7), (4, 8)]],
            fixed=[[5, 2], [6, 3], [7, 0], [8, 1]]), explanation=(
                "The common ABC triangle forces x=y, but original fixed leaves "
                "restrict x to {0,1} and y to {2,3}; no extension exists.")),
        dict(name="odd_five_wheel", expected_status="colored", graph=dict(
            vertices=list(range(6)),
            edges=[[v, (v + 1) % 5] for v in range(5)] + [[v, 5] for v in range(5)],
            fixed=[]), explanation="An odd five-cycle and its common hub require four colors."),
    ]


def _control_solution_count(graph):
    """Independent exhaustive count on the small original graph, without factors."""
    fixed = dict(graph["fixed"])
    free = [v for v in graph["vertices"] if v not in fixed]
    total = 0
    for colors in product(range(4), repeat=len(free)):
        assignment = dict(fixed)
        assignment.update(zip(free, colors))
        if all(assignment[a] != assignment[b] for a, b in graph["edges"]):
            total += 1
    return total


def _compare(graph, *, repeats, max_checks, order_offset, full, expected_status):
    from four_color_constraints import solve_constraints

    runs = {mode: [] for mode in MODES}
    first = {}
    orders = []
    for repeat in range(repeats):
        order = MODES if (order_offset + repeat) % 2 == 0 else tuple(reversed(MODES))
        orders.append(list(order))
        for mode in order:
            start = perf_counter()
            result = solve_constraints(
                graph, use_intersections=mode == "intersections", use_c5=False,
                use_conflicts=False, max_checks=max_checks,
                trace_limit=5000 if full else 0, record_relations=full)
            elapsed = perf_counter() - start
            if result["graph_sha256"] != graph_fingerprint(graph):
                raise AssertionError("solver graph fingerprint differs from the supplied graph")
            if result["status"] not in (expected_status, "limit"):
                raise AssertionError(
                    f"unexpected {result['status']} in {mode}; expected {expected_status} or limit")
            verified = result["status"] == "colored" and verify_coloring(graph, result["colors"])
            if result["status"] == "colored" and not verified:
                raise AssertionError("invalid witness against original edges and fixed colors")
            if mode in first:
                if (result["status"] != first[mode]["status"]
                        or result["stats"] != first[mode]["stats"]):
                    raise AssertionError(f"status or counters changed across repeats in {mode}")
                if result["colors"] != first[mode]["colors"]:
                    raise AssertionError(f"literal witness changed across repeats in {mode}")
            else:
                first[mode] = result
            runs[mode].append(elapsed)
    results = {}
    for mode in MODES:
        result = first[mode]
        compact = dict(
            status=result["status"], seconds=median(runs[mode]),
            seconds_runs=runs[mode], stats=result["stats"],
            colors=result["colors"] if result["status"] == "colored" else None,
            witness_verified=(verify_coloring(graph, result["colors"])
                              if result["status"] == "colored" else None),
            status_and_counters_stable=True,
            substructures={key: value for key, value in result["substructures"].items()
                           if isinstance(value, (str, int, float, bool))})
        if full:
            compact["recorded_result"] = result
        results[mode] = compact
    if all(results[mode]["status"] != "limit" for mode in MODES):
        if results["base"]["status"] != results["intersections"]["status"]:
            raise AssertionError("completed modes disagree")
    return dict(graph=graph, graph_sha256=graph_fingerprint(graph),
                run_orders=orders, results=results)


def _aggregate(rows):
    keys = sorted({key for row in rows for key in row["stats"]})
    statuses = Counter(row["status"] for row in rows)
    return dict(
        graphs=len(rows), status_counts=dict(sorted(statuses.items())),
        colored=statuses["colored"], limit=statuses["limit"],
        unsatisfiable=statuses["unsatisfiable"],
        verified_witnesses=sum(row["witness_verified"] is True for row in rows),
        seconds=sum(row["seconds"] for row in rows),
        stats={key: max((row["stats"].get(key, 0) for row in rows), default=0)
            if key.startswith(("peak_", "max_")) else
            sum(row["stats"].get(key, 0) for row in rows) for key in keys})


def experiment(count=30, size=30, seed=0, max_checks=1000000, repeats=3):
    import networkx as nx

    if type(count) is not int or count < 0:
        raise ValueError("count must be a nonnegative integer")
    if type(size) is not int or size < 3:
        raise ValueError("vertices must be an integer at least 3")
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    if type(max_checks) is not int or max_checks < 0:
        raise ValueError("max_checks must be a nonnegative integer")
    if type(repeats) is not int or repeats < 1:
        raise ValueError("repeats must be a positive integer")

    controls = []
    for offset, control in enumerate(named_controls()):
        graph = normalize_graph(dict(control["graph"], name=control["name"]))
        reference_count = _control_solution_count(graph)
        if (reference_count > 0) != (control["expected_status"] == "colored"):
            raise AssertionError("named control disagrees with independent exhaustive count")
        record = _compare(graph, repeats=repeats, max_checks=max_checks,
                          order_offset=offset, full=True,
                          expected_status=control["expected_status"])
        record.update(name=control["name"], expected_status=control["expected_status"],
                      explanation=control["explanation"], reference_solutions=reference_count,
                      reference_method="exhaustive original-edge assignments with literal fixed colors")
        controls.append(record)

    records = []
    for offset in range(count):
        graph = normalize_graph(random_triangulation(size, seed + offset))
        nx_graph = nx.Graph()
        nx_graph.add_nodes_from(graph["vertices"])
        nx_graph.add_edges_from(graph["edges"])
        if not nx.check_planarity(nx_graph)[0]:
            raise AssertionError("sample failed independent NetworkX planarity check")
        record = _compare(graph, repeats=repeats, max_checks=max_checks,
                          order_offset=offset + len(controls), full=False,
                          expected_status="colored")
        record.update(seed=seed + offset, planar_verified=True)
        records.append(record)

    totals = {mode: _aggregate([record["results"][mode] for record in records]) for mode in MODES}
    paired = [record for record in records
              if all(record["results"][mode]["status"] == "colored" for mode in MODES)]
    paired_totals = {mode: _aggregate([record["results"][mode] for record in paired]) for mode in MODES}
    base_seconds = paired_totals["base"]["seconds"]
    intersection_seconds = paired_totals["intersections"]["seconds"]
    source_names = (
        "four_color_intersection_experiment.py", "four_color_intersections.py",
        "four_color_constraints.py", "four_color_examples.py", "four_color_lab.py",
        "four_color_serialization.py", "four_color_joint_consistency.py",
        "four_color_c5.py", "four_color_conflicts.py")
    source_dir = Path(__file__).resolve().parent
    return dict(
        schema="four-color-intersections-comparison-v1", count=count, vertices=size,
        seed=seed, max_checks=max_checks, repeats=repeats,
        options=dict(use_substructures=True, use_c5=False, use_conflicts=False,
                     controls_trace_limit=5000, controls_record_relations=True,
                     samples_trace_limit=0, samples_record_relations=False),
        sampling="deterministic face insertion and convex flips with relabeling; nonuniform free planar triangulations",
        timing="in-process elapsed solve time per repetition; alternate mode order per graph and repetition; seconds is each graph's median; totals sum those medians",
        timing_scope="includes graph normalization, relation construction, propagation, elimination, writeback and solver verification; excludes generation and external verification",
        interpretation="finite matched-input results; limit is inconclusive; no universal speed or propagation-completeness claim",
        stats_aggregation="sum work counters; maximum peak_* and max_* fields; repeated runs do not multiply counters",
        control_solution_counts_independently_checked=True,
        repeats_status_and_counters_stable=True,
        both_modes_completed=len(paired), paired_totals=paired_totals,
        paired_median_time_ratio_base_over_intersections=(
            base_seconds / intersection_seconds if intersection_seconds > 0 else None),
        totals=totals, controls=controls, records=records,
        sources={name: hashlib.sha256((source_dir / name).read_bytes()).hexdigest()
                 for name in source_names},
        python=sys.version.split()[0], networkx=nx.__version__)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--vertices", type=int, default=30)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-checks", type=int, default=1000000)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--out", type=Path,
                        default=Path("artifacts/four_color_intersections/report.json"))
    args = parser.parse_args(argv)
    report = experiment(args.count, args.vertices, args.seed, args.max_checks, args.repeats)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(dict(out=str(args.out), totals=report["totals"],
                          both_modes_completed=report["both_modes_completed"],
                          paired_totals=report["paired_totals"]), ensure_ascii=False))


if __name__ == "__main__":
    main()
