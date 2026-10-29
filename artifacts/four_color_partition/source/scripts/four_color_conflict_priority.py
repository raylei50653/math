#!/usr/bin/env python3
"""Finite conflict-priority audit of exact shared-interface propagation.

Compare the same seven original graphs without timing.  Every complete literal
original-edge solution is independently enumerated and checked against all
recorded domains, input relations and saved reconstruction choices.  A genuine
unsatisfiable context remains unsatisfiable: early detection is the objective,
not a reduction in the number of genuine contradictions.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

from four_color_constraints import solve_constraints
from four_color_intersection_experiment import MODES, named_controls
from four_color_lab import graph_fingerprint, normalize_graph


ROOT = Path(__file__).resolve().parents[1]
MAX_CHECKS = 1_000_000
TRACE_LIMIT = 5000


def conflict_controls():
    """Reuse four existing controls and add three fixed original contexts."""
    edges = list(combinations(range(3), 2))
    edges += [(v, hub) for v in range(3) for hub in (3, 4)]
    edges += [(3, 5), (3, 6), (4, 7), (4, 8)]
    return named_controls() + [
        dict(name="bipyramid_identical_hub_domains", expected_status="colored",
             graph=dict(vertices=list(range(9)), edges=[list(e) for e in edges],
                        fixed=[[5, 2], [6, 3], [7, 2], [8, 3]]),
             explanation=("Both hubs see the same original triangle and both have "
                          "domain {0,1}. Twelve complete literal solutions remain; "
                          "shared-interface propagation need not prune anything.")),
        dict(name="bipyramid_overlapping_hub_domains", expected_status="colored",
             graph=dict(vertices=list(range(9)), edges=[list(e) for e in edges],
                        fixed=[[5, 2], [6, 3], [7, 0], [8, 3]]),
             explanation=("Original fixed leaves restrict the equal hubs to {0,1} "
                          "and {1,2}. Their common color is forced to 1 before "
                          "elimination, while six complete solutions remain.")),
        dict(name="odd_bipyramid_distinct_fixed_hubs", expected_status="unsatisfiable",
             graph=dict(vertices=list(range(7)),
                        edges=[[v, (v + 1) % 5] for v in range(5)]
                        + [[v, hub] for v in range(5) for hub in (5, 6)],
                        fixed=[[5, 2], [6, 3]]),
             explanation=("The two fixed hubs leave only colors 0 and 1 on an "
                          "odd five-cycle. Pairwise support is insufficient; "
                          "full elimination still detects the contradiction.")),
    ]


def original_solutions(graph):
    """Enumerate literal complete assignments using only original edges/fixes."""
    fixed = dict(graph["fixed"])
    free = [vertex for vertex in graph["vertices"] if vertex not in fixed]
    for choices in product(range(4), repeat=len(free)):
        assignment = dict(fixed)
        assignment.update(zip(free, choices))
        if all(assignment[a] != assignment[b] for a, b in graph["edges"]):
            yield [assignment[vertex] for vertex in graph["vertices"]]


def pre_elimination_metrics(result):
    """Read the phase strictly before the first eliminate event.

    An eliminate event already includes that elimination's work and increments
    its depth, so it must not contribute to these propagation-only measures.
    For a context rejected without elimination, use its complete reduction trace.
    """
    before = []
    for event in result["events"]:
        if event["kind"] == "eliminate":
            break
        if event["phase"] == "reduce":
            before.append(event)
    if not before:
        raise AssertionError("complete trace lacks initial reduction event")
    domains = before[-1]["domains"]
    conflict = next((event for event in result["events"]
                     if event["kind"] == "conflict"), None)
    if result["status"] == "unsatisfiable" and conflict is None:
        raise AssertionError("unsatisfiable result lacks a recorded conflict")
    eliminations_before_conflict = (conflict["stats"]["eliminations"]
                                   if conflict is not None else None)
    return dict(
        row_prunes_before_first_elimination=max(
            event["stats"]["row_prunes"] for event in before),
        intersection_row_prunes_before_first_elimination=sum(
            event["left_removed"] + event["right_removed"] for event in before
            if event["kind"] == "intersection" and event["depth"] == 0),
        color_prunes_before_first_elimination=max(
            event["stats"]["prunes"] for event in before),
        domain_candidates_before_first_elimination=[
            dict(vertex=vertex, colors=colors)
            for vertex, colors in zip(result["graph"]["vertices"], domains)],
        candidate_count_before_first_elimination=sum(map(len, domains)),
        eliminations_before_first_conflict=eliminations_before_conflict,
        early_conflict=(result["status"] == "unsatisfiable"
                        and eliminations_before_conflict == 0),
    )


def verify_preservation(graph, solutions, result):
    """Check every original solution against every retained reduction record."""
    if result["trace_truncated"] or result["event_count"] != len(result["events"]):
        raise AssertionError("audit requires the complete trace")
    if not result["record_relations"]:
        raise AssertionError("audit requires complete relation records")
    expected = "colored" if solutions else "unsatisfiable"
    if result["status"] != expected:
        raise AssertionError("solver disagrees with independent original-edge enumeration")
    fixed = dict(graph["fixed"])
    positions = {vertex: offset for offset, vertex in enumerate(graph["vertices"])}
    for event in result["events"]:
        if event["phase"] == "reduce":
            for vertex, color in zip(graph["vertices"], event["colors"]):
                if color != fixed.get(vertex, -1):
                    raise AssertionError("unfixed color written during reduction")
        if event["kind"] == "writeback" and event["depth"] != len(graph["vertices"]):
            raise AssertionError("writeback started before complete elimination")
    if solutions:
        # Membership in the independent exhaustive list also checks every
        # original edge and literal fixed color of the selected final witness.
        if result["colors"] not in solutions:
            raise AssertionError("final witness is not an original complete solution")

    prepared = []
    for record in result["elimination_records"]:
        prepared.append((record,
                         {tuple(row["boundary"]): set(row["colors"])
                          for row in record["rows"]},
                         [(relation["scope"], {tuple(row) for row in relation["rows"]})
                          for relation in record["input_relations"]]))
    counts = dict(original_solutions=len(solutions), source_domain_memberships=0,
                  input_relation_memberships=0, saved_choice_memberships=0,
                  reduction_domain_memberships=0)
    for colors in solutions:
        assignment = {vertex: colors[offset] for vertex, offset in positions.items()}
        for event in result["events"]:
            if event["phase"] != "reduce":
                continue
            for offset, color in enumerate(colors):
                if color not in event["domains"][offset]:
                    raise AssertionError("an original solution lost a reduction-domain color")
                counts["reduction_domain_memberships"] += 1
        for record, saved, inputs in prepared:
            for domain in record["source_domains"]:
                if assignment[domain["vertex"]] not in domain["colors"]:
                    raise AssertionError("an original solution lost a source-domain color")
                counts["source_domain_memberships"] += 1
            for scope, rows in inputs:
                if tuple(assignment[vertex] for vertex in scope) not in rows:
                    raise AssertionError("an original solution lost an input-relation row")
                counts["input_relation_memberships"] += 1
            boundary = tuple(assignment[vertex] for vertex in record["scope"])
            if (boundary not in saved
                    or assignment[record["vertex"]] not in saved[boundary]):
                raise AssertionError("an original solution lost its saved boundary choice")
            counts["saved_choice_memberships"] += 1
    return dict(all_solutions_preserved=True, no_early_writeback_verified=True,
                witness_verified=bool(solutions), checks=counts)


def experiment():
    controls = []
    for control in conflict_controls():
        graph = normalize_graph(dict(control["graph"], name=control["name"]))
        solutions = list(original_solutions(graph))
        expected = "colored" if solutions else "unsatisfiable"
        if expected != control["expected_status"]:
            raise AssertionError("control status disagrees with original-edge enumeration")
        results = {}
        for mode in MODES:
            result = solve_constraints(
                graph, use_intersections=mode == "intersections", use_c5=False,
                use_conflicts=False, record_relations=True, trace_limit=TRACE_LIMIT,
                max_checks=MAX_CHECKS)
            if result["graph_sha256"] != graph_fingerprint(graph):
                raise AssertionError("solver changed the original graph")
            verification = verify_preservation(graph, solutions, result)
            results[mode] = dict(status=result["status"], solution_count=len(solutions),
                                 metrics=pre_elimination_metrics(result),
                                 recorded_result=result, **verification)
        controls.append(dict(name=control["name"], graph=graph,
                             graph_sha256=graph_fingerprint(graph),
                             explanation=control["explanation"], expected_status=expected,
                             solution_count=len(solutions), original_solutions=solutions,
                             results=results))

    totals = {}
    for mode in MODES:
        rows = [control["results"][mode] for control in controls]
        totals[mode] = dict(
            colored=sum(row["status"] == "colored" for row in rows),
            unsatisfiable=sum(row["status"] == "unsatisfiable" for row in rows),
            early_conflicts=sum(row["metrics"]["early_conflict"] for row in rows),
            row_prunes_before_first_elimination=sum(
                row["metrics"]["row_prunes_before_first_elimination"] for row in rows),
            intersection_row_prunes_before_first_elimination=sum(
                row["metrics"]["intersection_row_prunes_before_first_elimination"]
                for row in rows),
            color_prunes_before_first_elimination=sum(
                row["metrics"]["color_prunes_before_first_elimination"] for row in rows),
            all_solutions_preserved=all(row["all_solutions_preserved"] for row in rows),
            no_early_writeback_verified=all(row["no_early_writeback_verified"] for row in rows))
    ranking = sorted(MODES, key=lambda mode: (
        -totals[mode]["early_conflicts"],
        -totals[mode]["color_prunes_before_first_elimination"],
        -totals[mode]["row_prunes_before_first_elimination"], mode))
    sources = ["scripts/" + name for name in (
        "four_color_conflict_priority.py", "four_color_intersections.py",
        "four_color_constraints.py", "four_color_examples.py", "four_color_lab.py",
        "four_color_serialization.py", "four_color_joint_consistency.py", "four_color_triangle_equalities.py", "four_color_partition.py",
        "four_color_c5.py", "four_color_conflicts.py",
        "four_color_intersection_experiment.py")]
    sources.append("tools/tests/test_four_color_conflict_priority.py")
    return dict(
        schema="four-color-conflict-priority-v1", controls=controls, totals=totals,
        control_count=len(controls), preferred_mode_order=ranking,
        priority_order=["earlier confirmed contradictions", "more unsupported colors removed",
                        "more unsupported complete rows removed"],
        options=dict(use_substructures=True, use_c5=False, use_conflicts=False,
                     record_relations=True, trace_limit=TRACE_LIMIT, max_checks=MAX_CHECKS),
        reference_method="exhaustive literal complete assignments against original edges and fixed colors",
        unsatisfiable_preservation="No original solutions exist; preservation checks are vacuous for these contexts.",
        interpretation=("Finite controls only. Actual satisfiable/unsatisfiable contexts must agree; "
                        "raw conflict counts are not minimized. The solver makes no speculative "
                        "decisions or backtracks. Pairwise support is not a completeness proof."),
        metric_definitions=dict(
            row_prunes="all factor-row deletions before the first eliminate event",
            intersection_row_prunes="sum of both tables' deletions in depth-zero intersection events",
            color_prunes="maximum cumulative stats.prunes before the first eliminate event",
            conflict_eliminations="successful eliminations before the first conflict; null for satisfiable cases",
            domain_candidates="last reduction-domain snapshot before the first eliminate event"),
        sources={path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                 for path in sources})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=Path("artifacts/four_color_intersections/conflict-priority.json"))
    args = parser.parse_args(argv)
    report = experiment()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(out=str(args.out), totals=report["totals"],
                          preferred_mode_order=report["preferred_mode_order"]),
                     ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
