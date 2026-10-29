#!/usr/bin/env python3
"""Independent original-edge and residual-projection audit; no 4CT oracle.

Construction costs are explicit prototype units, never main-engine checks.
Deterministic evidence excludes timing and uses exclusive-create output.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_bounded_projection import (  # noqa: E402
    METHODS, build_representation, compile_representation, reconstruct_one,
)
from structure import run as structural_audit  # noqa: E402


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def original_accepts(graph, row):
    assignment = dict(zip(graph["vertices"], row))
    return (all(assignment[u] != assignment[v] for u, v in graph["edges"])
            and all(assignment[v] == c for v, c in graph.get("fixed", [])))


def factor_accepts(factor, assignment):
    """Direct JSON evaluation independent of the prototype's predicate compiler."""
    scope = factor["scope"]
    if factor["kind"] == "domain":
        return assignment[scope[0]] in factor["colors"]
    if factor["kind"] == "neq":
        return assignment[scope[0]] != assignment[scope[1]]
    if factor["kind"] == "table":
        return tuple(assignment[v] for v in scope) in factor["_rows"]
    raise AssertionError(factor)


def check(graph, rep, oracle, totals):
    rep = json.loads(canonical(rep))
    accepted = compile_representation(rep)
    vertices, active = graph["vertices"], rep["active_vertices"]
    positions = {v: i for i, v in enumerate(vertices)}
    expected_projection = {tuple(row[positions[v]] for v in active)
                           for row, valid in oracle if valid}
    for row, valid in oracle:
        assert accepted(row) == valid, (graph, rep["projection_method"], row)
        totals["full_assignment_checks"] += 1
    # Membership alone is insufficient: old history constraints can mask an
    # overapproximate residual. Check the residual EXISTS projection itself.
    factors = deepcopy(rep["factors"])
    for factor in factors.values():
        if factor["kind"] == "table":
            factor["_rows"] = frozenset(map(tuple, factor["rows"]))
    for row in product(range(4), repeat=len(active)):
        assignment = dict(zip(active, row))
        actual = all(factor_accepts(factors[k], assignment) for k in rep["active_factor_ids"])
        assert actual == (row in expected_projection), ("residual", graph, row, rep)
        totals["residual_assignment_checks"] += 1
    witness = reconstruct_one(rep)
    assert (witness is not None) == bool(expected_projection)
    if witness is not None:
        assert original_accepts(graph, witness)
        totals["original_edge_witness_checks"] += 1
    if rep["decision"] != "undetermined":
        assert (rep["decision"] == "satisfiable") == bool(expected_projection)
    totals["representations"] += 1


def cases():
    for n in range(5):
        edges = list(combinations(range(n), 2))
        for bits in range(1 << len(edges)):
            graph = dict(vertices=list(range(n)), edges=[list(e) for i, e in enumerate(edges)
                                                        if bits & (1 << i)], fixed=[])
            yield "all_graphs_n0_n4", graph
            if n <= 3:
                for colors in product(range(-1, 4), repeat=n):
                    if any(c >= 0 for c in colors):
                        yield "all_partial_fixed_n1_n3", dict(
                            graph, fixed=[[v, c] for v, c in enumerate(colors) if c >= 0])
    named = [
        dict(vertices=list(range(5)), edges=list(map(list, combinations(range(5), 2)))),
        dict(vertices=list(range(5)), edges=[[i, (i + 1) % 5] for i in range(5)]),
        dict(vertices=list(range(6)), edges=[[i, (i + 1) % 5] for i in range(5)]
             + [[5, i] for i in range(5)]),
        dict(vertices=list(range(5)), edges=[[0, i] for i in range(1, 5)],
             fixed=[[i, i - 1] for i in range(1, 5)]),
        dict(vertices=[40, -3, 900, 17, 0], edges=[[40, -3], [900, 17]], fixed=[[900, 3]]),
        dict(vertices=[30, -7, 800], edges=[[30, -7]], fixed=[[30, 2], [-7, 2]]),
    ]
    for graph in named:
        yield "named_two_orders", graph
    rng = random.Random(20261029)
    for i in range(16):
        vertices = [40, -3, 900, 17, 0, 81][:5 + i % 2]
        rng.shuffle(vertices)
        yield "seeded_n5_n6", dict(vertices=vertices,
            edges=[list(e) for e in combinations(vertices, 2) if rng.random() < (i % 5 + 1) / 6],
            fixed=[[v, rng.randrange(4)] for v in vertices[:i % 4]])


def tiny_audit():
    totals, groups, statuses = Counter(), {}, Counter()
    for kind, graph in cases():
        totals["inputs"] += 1
        groups.setdefault(kind, Counter())["inputs"] += 1
        oracle = [(row, original_accepts(graph, row))
                  for row in product(range(4), repeat=len(graph["vertices"]))]
        orders = [graph["vertices"]]
        if kind == "named_two_orders":
            orders.append(list(reversed(graph["vertices"])))
        for order in orders:
            for cut in range(len(order) + 1):
                for method in METHODS:
                    rep = build_representation(graph, order=order, stop_after=cut, method=method)
                    check(graph, rep, oracle, totals)
                    statuses[rep["decision"]] += 1
                    groups[kind]["representations"] += 1
    return dict(totals=dict(totals), groups={k: dict(v) for k, v in groups.items()},
                representation_decisions=dict(statuses))


def budget_audit():
    totals, statuses = Counter(), Counter()
    graphs = [dict(vertices=[0, 1, 2, 3], edges=[[0, 1], [1, 2], [2, 3], [3, 0]]),
              dict(vertices=[9, -3, 20, 0, 2], edges=[[9, v] for v in [-3, 20, 0, 2]],
                   fixed=[[-3, 0], [20, 1], [0, 2], [2, 3]])]
    for graph in graphs:
        oracle = [(row, original_accepts(graph, row))
                  for row in product(range(4), repeat=len(graph["vertices"]))]
        for method in METHODS:
            complete = build_representation(graph, method=method)
            cost = complete["metrics"]["candidate_checks"]
            for budget in range(cost + 2):
                rep = build_representation(graph, method=method, max_checks=budget)
                check(graph, rep, oracle, totals)
                prefix = build_representation(graph, method=method, stop_after=len(rep["history"]))
                for key in ("history", "active_vertices", "active_factor_ids", "factors"):
                    assert rep[key] == prefix[key], ("atomicity", method, budget, key)
                assert rep["metrics"]["candidate_checks"] <= budget
                assert rep["metrics"]["candidate_checks"] == (
                    rep["metrics"]["color_trials"] + rep["metrics"]["cap_scan_rows"])
                statuses[rep["stop_reason"]] += 1
    return dict(totals=dict(totals), stop_reasons=dict(statuses))


def benchmarks():
    records = []
    # Same center-first ordering, domain, graph and recipe policy for every mode.
    for degree in (4, 5, 6, 7, 8, 9, 10):
        graph = dict(vertices=list(range(degree + 1)), edges=[[0, i] for i in range(1, degree + 1)])
        for method in METHODS:
            rep = build_representation(graph, method=method, stop_after=1)
            step = rep["metrics"]["steps"][0]
            expected_rows = (4 * 3**degree - 6 * 2**degree + 4)
            if method == "full":
                assert step["projected_rows"] == expected_rows
            expected_factors = (1 if method == "full" else
                                comb(degree - (method == "anchored"),
                                     3 if method == "anchored" else 4))
            assert step["projected_factors"] == expected_factors
            if method != "full":
                assert step["projected_rows"] == 232 * expected_factors
            residual_tables = [rep["factors"][key] for key in rep["active_factor_ids"]
                               if rep["factors"][key]["kind"] == "table"]
            records.append(dict(family="star_one_step", degree=degree, method=method,
                                complete_projected_rows_formula=expected_rows,
                                projected_tuple_cells=sum(len(f["scope"]) * len(f["rows"])
                                                          for f in residual_tables),
                                representation_json_bytes=len(canonical(rep)),
                                **{k: v for k, v in step.items() if k != "vertex"}))
    # Positive single-step results must face complete multi-step costs. Do not
    # call reconstruction on an interrupted wide residual just to obtain SAT.
    for degree in (5, 6, 8):
        graph = dict(vertices=list(range(degree + 1)), edges=[[0, i] for i in range(1, degree + 1)])
        for order_name, order in (("center_first", graph["vertices"]),
                                  ("leaves_first", graph["vertices"][1:] + [0])):
            for method in METHODS:
                rep = build_representation(graph, method=method, order=order, max_checks=200000)
                if rep["decision"] == "satisfiable":
                    assert original_accepts(graph, reconstruct_one(rep))
                records.append(dict(family="star_complete_budget", degree=degree, order=order_name,
                                    method=method, stop_reason=rep["stop_reason"], decision=rep["decision"],
                                    representation_json_bytes=len(canonical(rep)), metrics=rep["metrics"]))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    output = dict(schema="four-color-bounded-projection-audit-v1")
    output["structure"] = structural_audit()
    print("PASS independent finite-mask and star structural controls", flush=True)
    output["tiny_original_and_residual"] = tiny_audit()
    print("PASS all tiny original and residual assignment checks", flush=True)
    output["budget_interruptions"] = budget_audit()
    print("PASS every tested budget and atomic prefix", flush=True)
    output["benchmarks"] = benchmarks()
    sources = [Path(__file__), Path(__file__).with_name("structure.py"),
               ROOT / "scripts/four_color_bounded_projection.py",
               ROOT / "scripts/four_color_partial_history.py", ROOT / "scripts/four_color_lab.py",
               ROOT / "scripts/four_color_serialization.py", ROOT / "Math/ColoringBoundedProjection.lean",
               ROOT / "Math/ColoringElimination.lean", ROOT / "Math.lean",
               Path(__file__).with_name("axioms.lean"),
               ROOT / "tools/tests/test_four_color_bounded_projection.py"]
    output["source_sha256"] = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sources}
    output["limitations"] = [
        "A standalone prototype, not a modification or benchmark of the production engine.",
        "All subfamilies share one literal remaining assignment; complete historical fibres remain recipes.",
        "Counters are construction trials/cap-row visits, not main-engine checks, total CPU or RSS.",
        "No general fixed arity, polynomial bound, universal speedup or Four Color Theorem result.",
        "Residual search and witness reconstruction are outside the construction budget.",
        "Single-step and center-first star controls are not an optimized elimination-order comparison.",
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x") as stream:
        json.dump(output, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps({k: output[k]["totals"] for k in
                      ("tiny_original_and_residual", "budget_interruptions")}, sort_keys=True))


if __name__ == "__main__":
    main()
