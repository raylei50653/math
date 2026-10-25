#!/usr/bin/env python3
"""Reproducible fixed-context cases on six larger planar triangulations.

Each original graph supplies two contexts on the same independent fixed
vertices. One context comes from a directly verified original-edge witness;
the other changes those literal fixed colors without imposing a fixed-edge
conflict. The independent search reference determines the trial's status.
Only ``main`` writes an artifact, after independently checking planarity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

from four_color_examples import random_triangulation
from four_color_lab import graph_fingerprint, normalize_graph, solve, verify_coloring


SIZES = (30, 60, 100)
SOURCE_SEEDS = (0, 1)
REFERENCE_MAX_STEPS = 1_000_000
FIXED_VERTEX_TARGET = 4


def _independent_fixed_vertices(graph):
    """Choose up to four vertices in ascending original-degree/label order."""
    adjacent = {vertex: set() for vertex in graph["vertices"]}
    for left, right in graph["edges"]:
        adjacent[left].add(right)
        adjacent[right].add(left)
    order = sorted(graph["vertices"], key=lambda vertex: (len(adjacent[vertex]), vertex))
    selected = []
    for vertex in order:
        if all(previous not in adjacent[vertex] for previous in selected):
            selected.append(vertex)
            if len(selected) == FIXED_VERTEX_TARGET:
                break
    if len(selected) < 3:
        raise RuntimeError("deterministic fixed-vertex selection found fewer than three vertices")
    return selected, [dict(vertex=vertex, degree=len(adjacent[vertex]))
                      for vertex in selected]


def _reference(graph):
    """Return only evidence justified by the independent literal-edge search."""
    result = solve(graph, strategy="dsatur", propagation=True, backtracking=True,
                   max_steps=REFERENCE_MAX_STEPS, trace_limit=0)
    status = result["status"]
    if result["graph_sha256"] != graph_fingerprint(graph):
        raise AssertionError("reference search changed the original graph or fixed colors")
    reference = dict(
        method="independent-original-edge-dsatur",
        status=status,
        classification={"colored": "SAT", "unsatisfiable": "UNSAT", "limit": "UNKNOWN"}.get(status),
        colors=None,
        stats=result["stats"],
        max_steps=REFERENCE_MAX_STEPS,
        witness_verified=False,
        all_solutions_preserved=None,
    )
    if status == "colored":
        if not verify_coloring(graph, result["colors"]):
            raise AssertionError("reference witness violates an original edge or literal fixed color")
        reference.update(colors=result["colors"], coverage="onewitness",
                         witness_verified=True,
                         evidence="One full witness checked directly against original edges and fixed colors.")
    elif status == "unsatisfiable":
        reference.update(coverage="exhaustive_search",
                         evidence="All original-edge search branches exhausted under these literal fixed colors.")
    elif status == "limit":
        reference.update(coverage="unknown_limit",
                         evidence="Assignment limit reached; no satisfiability or preservation conclusion.")
    else:
        raise AssertionError(f"unexpected independent-reference status: {status!r}")
    return reference


def generate_random_cases():
    """Return twelve deterministic cases without writing files or timing data.

For each size/seed pair, both contexts retain the same original vertices,
edges, positions and generator descriptor. Their fixed vertices are pairwise
nonadjacent, so the trial cannot fail merely on an edge joining fixed points.
The search limit remains UNKNOWN; planarity is never used as a coloring oracle.
"""
    cases = []
    for size in SIZES:
        for source_seed in SOURCE_SEEDS:
            original = normalize_graph(random_triangulation(size, source_seed))
            original_sha = graph_fingerprint(original)
            source_reference = _reference(original)
            if source_reference["status"] != "colored":
                raise RuntimeError(
                    f"cannot construct a verified compatible context for n={size}, "
                    f"seed={source_seed}: source reference is {source_reference['classification']}")
            witness = dict(zip(original["vertices"], source_reference["colors"]))
            fixed_vertices, fixed_degrees = _independent_fixed_vertices(original)
            compatible_colors = [witness[vertex] for vertex in fixed_vertices]
            trial_seed = 10_000_000 + size * 100 + source_seed
            rng = random.Random(trial_seed)
            trial_colors = [rng.randrange(4) for _ in fixed_vertices]
            if trial_colors == compatible_colors:
                trial_colors[0] = (compatible_colors[0] + 1) % 4
            for context, colors in (("compatible", compatible_colors),
                                    ("trial", trial_colors)):
                name = f"random_triangulation_n{size}_seed{source_seed}_{context}"
                fixed = [[vertex, color] for vertex, color in zip(fixed_vertices, colors)]
                graph = normalize_graph(dict(
                    original, name=name, fixed=fixed,
                    description=(original.get("description", "")
                                 + f" Fixed context: {context}; {len(fixed_vertices)} independent original vertices.")))
                fixed_assignment = dict(fixed)
                if any(left in fixed_assignment and right in fixed_assignment
                       for left, right in original["edges"]):
                    raise AssertionError("selected fixed vertices are not independent in the original graph")
                if context == "compatible" and not verify_coloring(graph, source_reference["colors"]):
                    raise AssertionError("source witness does not extend the compatible context")
                reference = _reference(graph)
                if context == "compatible" and reference["status"] == "unsatisfiable":
                    raise AssertionError("independent search rejected a directly verified compatible witness")
                cases.append(dict(
                    name=name,
                    case_kind=f"random_triangulation_{context}_context",
                    source_seed=source_seed,
                    n=size,
                    graph=graph,
                    graph_sha256=graph_fingerprint(graph),
                    source_graph_sha256=original_sha,
                    fixed_metadata=dict(
                        context=context,
                        selection="greedy ascending original degree, then integer vertex label",
                        target_count=FIXED_VERTEX_TARGET,
                        vertices=fixed_vertices,
                        original_degrees=fixed_degrees,
                        pairwise_nonadjacent=True,
                        original_fixed_edge_conflict=False,
                        compatible_fixed=[[vertex, color] for vertex, color
                                          in zip(fixed_vertices, compatible_colors)],
                        differs_from_compatible=(colors != compatible_colors),
                        trial_rng_seed=trial_seed,
                        compatible_source_witness_verified=True,
                        compatible_source_reference=source_reference,
                    ),
                    reference=reference,
                    label_scope=("Status comes from the independent fixed-context search; "
                                 "a SAT reference preserves one verified witness only. "
                                 "The trial context is not preclassified."),
                ))
    if len(cases) != 12:
        raise AssertionError("expected exactly twelve larger random cases")
    return cases


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=Path("artifacts/four_color_intersections/larger-random.json"))
    args = parser.parse_args(argv)
    import networkx as nx

    cases = generate_random_cases()
    checked = {}
    for case in cases:
        original_sha = case["source_graph_sha256"]
        if original_sha not in checked:
            graph = nx.Graph()
            graph.add_nodes_from(case["graph"]["vertices"])
            graph.add_edges_from(case["graph"]["edges"])
            planar, _ = nx.check_planarity(graph)
            if not planar:
                raise AssertionError("generated original graph failed independent planarity check")
            checked[original_sha] = dict(planar=True, vertices=graph.number_of_nodes(),
                                         edges=graph.number_of_edges(), method="networkx.check_planarity")
        case["planarity"] = checked[original_sha]
    report = dict(schema="four-color-larger-random-v1", cases=cases,
                  case_count=len(cases), original_graph_count=len(checked),
                  sizes=list(SIZES), source_seeds=list(SOURCE_SEEDS),
                  reference_max_steps=REFERENCE_MAX_STEPS,
                  interpretation="Finite, nonuniform sample. SAT coverage is one witness; limit is UNKNOWN.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(dict(out=str(args.out), case_count=len(cases),
                          statuses={status: sum(case["reference"]["status"] == status for case in cases)
                                    for status in ("colored", "unsatisfiable", "limit")}),
                     ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
