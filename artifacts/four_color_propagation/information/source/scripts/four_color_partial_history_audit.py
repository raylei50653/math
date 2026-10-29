#!/usr/bin/env python3
"""Compare partial-history representations with every original coloring.

This bounded experiment uses a separate original-edge oracle. It checks all
assignments (including ones violating fixed colors), not merely solution counts.
No production solver modes or previously saved evidence are changed.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys

from four_color_partial_history import (
    build_representation, compile_representation, reconstruct_one,
)


ROOT = Path(__file__).resolve().parents[1]
MODES = ("table", "recipe", "mixed")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def original_accepts(graph, colors):
    """Literal oracle independent of factors, elimination and reconstruction."""
    assignment = dict(zip(graph["vertices"], colors))
    return (all(assignment[u] != assignment[v] for u, v in graph["edges"])
            and all(assignment[v] == c for v, c in graph.get("fixed", [])))


def cases():
    for n in range(5):
        pairs = list(combinations(range(n), 2))
        for bits in range(1 << len(pairs)):
            graph = dict(vertices=list(range(n)),
                         edges=[list(edge) for i, edge in enumerate(pairs) if bits & (1 << i)],
                         fixed=[])
            yield "all_graphs_n0_to_n4", f"n{n}_edges{bits}", graph
            if n <= 3:
                for fixed in product(range(-1, 4), repeat=n):
                    if any(c >= 0 for c in fixed):
                        conditioned = dict(graph, fixed=[[v, c] for v, c in enumerate(fixed) if c >= 0])
                        yield "all_nonempty_partial_fixed_n1_to_n3", digest(conditioned), conditioned

    named = {
        "K5": dict(vertices=list(range(5)), edges=list(map(list, combinations(range(5), 2))), fixed=[]),
        "C5": dict(vertices=list(range(5)), edges=[[i, (i + 1) % 5] for i in range(5)], fixed=[]),
        "odd_wheel": dict(vertices=list(range(6)),
                          edges=[[i, (i + 1) % 5] for i in range(5)] + [[5, i] for i in range(5)], fixed=[]),
        "star_blocked": dict(vertices=list(range(5)), edges=[[0, i] for i in range(1, 5)],
                             fixed=[[i, i - 1] for i in range(1, 5)]),
        "star_same_leaves": dict(vertices=list(range(5)), edges=[[0, i] for i in range(1, 5)],
                                 fixed=[[i, 3] for i in range(1, 5)]),
        "triangle_external_fixed": dict(vertices=[40, -3, 900, 17],
                                        edges=[[40, -3], [-3, 900], [900, 40], [900, 17]], fixed=[[17, 2]]),
        "disconnected_literal_ids": dict(vertices=[40, -3, 900, 17, 0],
                                         edges=[[40, -3], [900, 17]], fixed=[[900, 3]]),
        "fixed_edge_conflict": dict(vertices=[30, -7, 800], edges=[[30, -7]], fixed=[[30, 2], [-7, 2]]),
    }
    for name, graph in named.items():
        yield "named_controls_two_orders", name, graph

    rng = random.Random(20261027)
    for i in range(16):
        vertices = [40, -3, 900, 17, 0, 81][:5 + i % 2]
        rng.shuffle(vertices)
        graph = dict(vertices=vertices,
                     edges=[list(edge) for edge in combinations(vertices, 2) if rng.random() < (i % 5 + 1) / 6],
                     fixed=[[v, rng.randrange(4)] for v in vertices[:i % 4]])
        yield "seeded_n5_n6_literal_frames", f"seed20261027_{i}", graph


def check_representation(graph, rep, oracle):
    # Persisted JSON must carry the semantics without Python object identities.
    rep = json.loads(canonical(rep))
    accepts = compile_representation(rep)
    for colors, expected in oracle:
        actual = accepts(colors)
        if actual != expected:
            raise AssertionError(dict(kind="membership_mismatch", graph=graph, colors=colors,
                                      expected=expected, actual=actual, representation=rep))
    witness = reconstruct_one(rep)
    has_solution = any(expected for _, expected in oracle)
    if ((witness is not None) != has_solution
            or witness is not None and (len(witness) != len(graph["vertices"])
                                       or any(type(c) is not int or c not in range(4) for c in witness)
                                       or not original_accepts(graph, witness))):
        raise AssertionError(dict(kind="writeback_mismatch", graph=graph, witness=witness))
    if rep["decision"] == "satisfiable" and not has_solution:
        raise AssertionError("false satisfiable declaration")
    if rep["decision"] == "unsatisfiable" and has_solution:
        raise AssertionError("false unsatisfiable declaration")
    return witness


def negative_controls():
    controls = []

    # Without the recorded fibre, the projected single vertex forgets its edge.
    graph = dict(vertices=[0, 1], edges=[[0, 1]], fixed=[])
    rep = build_representation(graph, stop_after=1, history_mode="table")
    broken = deepcopy(rep)
    broken["history"][0]["rows"] = [dict(boundary=[b], colors=list(range(4))) for b in range(4)]
    colors = [0, 0]
    assert not original_accepts(graph, colors) and compile_representation(broken)(colors)
    controls.append(dict(kind="forget_fibre_constraint", graph=graph, colors=colors,
                         original_accepts=False, broken_accepts=True))

    # The prefix alone says nothing about a separate residual edge.
    graph = dict(vertices=[0, 1, 2], edges=[[1, 2]], fixed=[])
    rep = build_representation(graph, stop_after=1, history_mode="table")
    broken = deepcopy(rep)
    broken["active_factor_ids"] = []
    colors = [0, 0, 0]
    assert not original_accepts(graph, colors) and compile_representation(broken)(colors)
    controls.append(dict(kind="drop_residual_constraints", graph=graph, colors=colors,
                         original_accepts=False, broken_accepts=True))

    # One selected support still yields one solution, but loses other originals.
    graph = dict(vertices=[0, 1], edges=[[0, 1]], fixed=[])
    rep = build_representation(graph, stop_after=1, history_mode="table")
    broken = deepcopy(rep)
    row = next(row for row in broken["history"][0]["rows"] if row["boundary"] == [0])
    row["colors"] = [1]
    colors = [2, 0]
    assert original_accepts(graph, colors) and not compile_representation(broken)(colors)
    controls.append(dict(kind="keep_only_one_support", graph=graph, colors=colors,
                         original_accepts=True, broken_accepts=False))
    return controls


def encoding_statistics(rep):
    return dict(json_bytes=len(canonical(rep)),
                completed_steps=len(rep["history"]),
                active_vertices=len(rep["active_vertices"]),
                stored_fibre_rows=sum(len(row.get("rows", [])) for row in rep["history"]),
                recipe_steps=sum(row["kind"] == "recipe" for row in rep["history"]),
                retained_factor_table_rows=sum(len(factor.get("rows", [])) for factor in rep["factors"].values()))


def size_examples():
    examples = []
    for name, graph, cut in (
        ("leaf", dict(vertices=[0, 1], edges=[[0, 1]], fixed=[]), 1),
        ("star_center", dict(vertices=list(range(5)), edges=[[0, i] for i in range(1, 5)], fixed=[]), 1),
        ("K4_complete", dict(vertices=list(range(4)), edges=list(map(list, combinations(range(4), 2))), fixed=[]), 4),
    ):
        examples.append(dict(name=name, graph=graph, stop_after=cut,
                             representations={mode: encoding_statistics(build_representation(
                                 graph, stop_after=cut, history_mode=mode)) for mode in MODES}))
    return examples


def run_audit():
    paths = [ROOT / "scripts" / name for name in (
        "four_color_partial_history.py", "four_color_partial_history_audit.py",
        "four_color_lab.py", "four_color_serialization.py")]
    sources = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    grouped, evidence_digests = {}, []
    totals = Counter()
    decisions = Counter()
    for group, name, graph in cases():
        counts = grouped.setdefault(group, Counter())
        counts["inputs"] += 1
        oracle = [(colors, original_accepts(graph, colors))
                  for colors in product(range(4), repeat=len(graph["vertices"]))]
        solution_count = sum(expected for _, expected in oracle)
        counts["satisfiable_inputs" if solution_count else "unsatisfiable_inputs"] += 1
        orders = [graph["vertices"]]
        if group == "named_controls_two_orders":
            orders.append(list(reversed(graph["vertices"])))
        for order in orders:
            for cut in range(len(graph["vertices"]) + 1):
                for mode in MODES:
                    rep = build_representation(graph, stop_after=cut, history_mode=mode, order=order)
                    witness = check_representation(graph, rep, oracle)
                    counts["representations"] += 1
                    counts["assignment_checks"] += len(oracle)
                    counts["valid_writebacks"] += witness is not None
                    counts["partial_representations"] += bool(rep["history"] and rep["active_vertices"])
                    decisions[rep["decision"]] += 1
                    evidence_digests.append(digest(dict(graph=graph, order=order, cut=cut, mode=mode,
                                                      representation=rep, solutions=solution_count, witness=witness)))
        if counts["inputs"] % 200 == 0:
            print(f"checked {group}: {counts['inputs']} inputs", file=sys.stderr, flush=True)

    # Every budget may interrupt a different join position. Prior exact states
    # must remain usable; an unfinished relation must never be published.
    budget_graph = dict(vertices=[0, 1, 2, 3], edges=[[0, 1], [1, 2], [2, 0], [2, 3]], fixed=[[3, 1]])
    oracle = [(colors, original_accepts(budget_graph, colors)) for colors in product(range(4), repeat=4)]
    budgets = Counter()
    for mode in MODES:
        for budget in (0, 1, 4, 15, 16, 17, 63, 64, 65, 100, 200, 1000):
            rep = build_representation(budget_graph, history_mode=mode, max_checks=budget)
            witness = check_representation(budget_graph, rep, oracle)
            budgets["representations"] += 1
            budgets["assignment_checks"] += len(oracle)
            budgets["valid_writebacks"] += witness is not None
            budgets[rep["stop_reason"]] += 1
            evidence_digests.append(digest(dict(budget=budget, mode=mode, representation=rep, witness=witness)))
    for counts in grouped.values():
        totals.update(counts)
    if sources != {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}:
        raise AssertionError("source files changed during audit")
    return dict(schema="four-color-partial-history-audit-v1", python=sys.version.split()[0],
                sources_sha256=sources, groups=grouped, totals=totals, decisions=decisions,
                budget_checks=budgets, case_evidence_sha256=digest(evidence_digests),
                negative_controls=negative_controls(), encoding_examples=size_examples(),
                scope="Finite exact-membership and deferred-writeback audit of an independent prototype. "
                      "Table, recipe and mixed modes are tested at every requested prefix. "
                      "No general speed, memory, production integration or planar-colorability claim. "
                      "JSON byte counts measure the complete serialized prototype state, not process RSS. "
                      "Recipe mode omits historical fibre rows but may retain projected factor tables.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error("use a new output file to preserve saved evidence")
    report = run_audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("totals", "budget_checks", "encoding_examples")}, indent=2))


if __name__ == "__main__":
    main()
