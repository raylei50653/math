#!/usr/bin/env python3
"""Finite original-edge checks of the full historical-fibre conjunction.

The production solver supplies complete elimination records. An independent
literal-color Cartesian enumeration compares their conjunction with every
original edge and fixed color. Incomplete, failed, or limited executions are
explicitly excluded from the conjunction theorem. This is finite implementation
evidence, not a Python refinement proof or a Four Color Theorem proof.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from four_color_constraints import solve_constraints


PALETTE = tuple(range(4))
BASE = "8d28acc"


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def cases():
    diamond_edges = [[10, 20], [10, 30], [20, 30], [20, 40], [30, 40]]
    return [
        ("empty", dict(vertices=[], edges=[], fixed=[])),
        ("isolated_vertex", dict(vertices=[-7], edges=[], fixed=[])),
        ("fixed_edge", dict(vertices=[8, 3], edges=[[8, 3]], fixed=[[8, 2]])),
        ("C5", dict(vertices=list(range(5)),
                    edges=[[v, (v + 1) % 5] for v in range(5)], fixed=[])),
        ("diamond", dict(vertices=[10, 20, 30, 40], edges=diamond_edges, fixed=[])),
        ("diamond_fixed_exterior", dict(vertices=[10, 20, 30, 40, 50, 60],
            edges=diamond_edges + [[10, 50], [40, 50], [50, 60], [20, 60]],
            fixed=[[50, 0], [60, 1]])),
        ("disconnected_edge_and_isolate", dict(vertices=[9, -2, 100],
            edges=[[9, -2]], fixed=[])),
    ]


def original_legal(graph, assignment):
    """No production normalizer, verifier, table, or propagation is used here."""
    return (all(assignment[a] != assignment[b] for a, b in graph["edges"])
            and all(assignment[v] == color for v, color in graph.get("fixed", [])))


def compile_complete_records(graph, result):
    """Fail closed: a partial record list is not a complete solution encoding."""
    vertices = graph["vertices"]
    records = result["elimination_records"]
    if (result["status"] != "colored"
            or result["stats"]["eliminations"] != len(vertices)
            or len(records) != len(vertices)):
        return None
    order = [record["vertex"] for record in records]
    assert len(set(order)) == len(vertices) and set(order) == set(vertices)
    compiled = []
    for i, record in enumerate(records):
        assert record["complete"] is True
        scope = record["scope"]
        assert len(scope) == len(set(scope)) and set(scope) <= set(order[i + 1:])
        rows = record["rows"]
        assert record["relation_rows"] == len(rows)
        table = {}
        for row in rows:
            boundary = tuple(row["boundary"])
            colors = tuple(row["colors"])
            assert len(boundary) == len(scope) and all(c in PALETTE for c in boundary)
            assert colors and len(colors) == len(set(colors))
            assert all(c in PALETTE for c in colors)
            assert boundary not in table
            table[boundary] = frozenset(colors)
        compiled.append((record["vertex"], tuple(scope), table))
    return compiled


def conjunction_holds(assignment, compiled):
    return all(assignment[vertex] in table.get(
        tuple(assignment[v] for v in scope), ()) for vertex, scope, table in compiled)


def check_complete_case(name, graph, bucket_method, use_substructures):
    result = solve_constraints(graph, bucket_method=bucket_method,
        use_substructures=use_substructures, record_relations=True,
        max_checks=1_000_000, max_table_rows=1_000_000, trace_limit=0)
    compiled = compile_complete_records(graph, result)
    assert compiled is not None, (name, result["status"])
    legal_rows = []
    encoded_rows = []
    checked = 0
    for colors in product(PALETTE, repeat=len(graph["vertices"])):
        assignment = dict(zip(graph["vertices"], colors))
        legal = original_legal(graph, assignment)
        encoded = conjunction_holds(assignment, compiled)
        assert legal == encoded, (name, colors, legal, encoded)
        checked += 1
        if legal:
            legal_rows.append(colors)
        if encoded:
            encoded_rows.append(colors)
    assert legal_rows == encoded_rows
    assert original_legal(graph, dict(zip(result["graph"]["vertices"], result["colors"])))
    return dict(name=name, graph=graph, bucket_method=bucket_method,
        use_substructures=use_substructures, status=result["status"],
        tau=True, complete_history=True, elimination_order=[entry[0] for entry in compiled],
        elimination_count=len(compiled), checked_full_assignments=checked,
        original_legal_count=len(legal_rows), historical_fibre_conjunction_count=len(encoded_rows),
        mismatches=0, legal_assignments_sha256=digest(legal_rows),
        source_domain_restrictions=sum(
            len(domain["colors"]) < 4 for record in result["elimination_records"]
            for domain in record["source_domains"]))


def incomplete_controls():
    c5 = dict(vertices=list(range(5)), edges=[[v, (v + 1) % 5] for v in range(5)], fixed=[])
    unsat = dict(vertices=[0, 1], edges=[[0, 1]], fixed=[[0, 0], [1, 0]])
    checks = []
    for name, graph, budget, expected in [
        ("fixed_equal_edge_unsatisfiable", unsat, 1_000_000, "unsatisfiable"),
        ("C5_zero_budget", c5, 0, "limit"),
        ("C5_partial_history", c5, 200, "limit"),
    ]:
        result = solve_constraints(graph, record_relations=True, max_checks=budget,
                                   max_table_rows=1_000_000, trace_limit=0)
        assert result["status"] == expected
        assert compile_complete_records(graph, result) is None
        if name == "C5_partial_history":
            assert 0 < result["stats"]["eliminations"] < len(graph["vertices"])
        count = sum(original_legal(graph, dict(zip(graph["vertices"], colors)))
                    for colors in product(PALETTE, repeat=len(graph["vertices"])))
        checks.append(dict(name=name, graph=graph, max_checks=budget,
            status=result["status"], completed_eliminations=result["stats"]["eliminations"],
            original_legal_count=count, complete_history=False,
            historical_conjunction_applied=False))
    return checks


def counting_control():
    """Force the mathematical x,y,z order independently of production min-fill."""
    graph = dict(vertices=[0, 1, 2], edges=[[0, 1], [0, 2]], fixed=[])
    # Exact symbolic elimination: first the center x, then the leaves y,z.
    wx = {(y, z): frozenset(PALETTE) - {y, z} for y, z in product(PALETTE, repeat=2)}
    wy = {(z,): frozenset(PALETTE) for z in PALETTE}
    wz = {(): frozenset(PALETTE)}
    compiled = [(0, (1, 2), wx), (1, (2,), wy), (2, (), wz)]
    legal_count = 0
    for row in product(PALETTE, repeat=3):
        assignment = dict(zip(graph["vertices"], row))
        legal = original_legal(graph, assignment)
        assert legal == conjunction_holds(assignment, compiled)
        legal_count += legal
    same = sum(len(colors) for (y, z), colors in wx.items() if y == z)
    different = sum(len(colors) for (y, z), colors in wx.items() if y != z)
    assert legal_count == same + different == 36
    assert len(wx[(0, 0)]) * len(wy[(0,)]) * len(wz[()]) == 48
    assert len(wx[(0, 1)]) * len(wy[(1,)]) * len(wz[()]) == 32
    return dict(graph=graph, mathematical_order=[0, 1, 2],
        order_is_forced_in_production_solver=False,
        checked_full_assignments=64, original_legal_count=legal_count,
        same_leaf_boundary_rows=4, same_leaf_fibre_size=3, same_leaf_contribution=same,
        different_leaf_boundary_rows=12, different_leaf_fibre_size=2,
        different_leaf_contribution=different,
        one_same_leaf_branch_product=48, one_different_leaf_branch_product=32,
        branch_products_are_not_total_counts=True)


def source_hashes():
    paths = {Path(__file__).resolve()}
    for name, module in tuple(sys.modules.items()):
        if name.startswith("four_color_") and getattr(module, "__file__", None):
            path = Path(module.__file__).resolve()
            if path.is_relative_to(ROOT / "scripts"):
                paths.add(path)
    return {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in sorted(paths)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True,
                        help="Explicit output path; saved reports are never overwritten implicitly.")
    args = parser.parse_args()
    results = [check_complete_case(name, graph, method, grouping)
               for name, graph in cases()
               for method in ("anchor", "prefix") for grouping in (False, True)]
    controls = incomplete_controls()
    count = counting_control()
    report = dict(schema="four-color-complete-history-v1", baseline=BASE,
        evidence="finite independent original-edge/fixed-color exhaustive comparison",
        claims_python_refinement_proof=False, claims_four_color_theorem=False,
        palette=list(PALETTE), cases=results, incomplete_history_controls=controls,
        counting_counterexample=count,
        totals=dict(named_successful_graphs=len(cases()), successful_runs=len(results),
            checked_full_assignments=sum(row["checked_full_assignments"] for row in results),
            original_legal_assignments=sum(row["original_legal_count"] for row in results),
            incomplete_history_controls=len(controls), mismatches=0),
        source_sha256=source_hashes())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
