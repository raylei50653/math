#!/usr/bin/env python3
"""Independent replay for two adjacent eliminations from original edge factors.

Run with the repository requirements; this does not import the projection engine.
All four colors are literal. Counts are complete rows, not normalized patterns.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path

import networkx as nx


COLORS = frozenset(range(4))


def available(values):
    return COLORS.difference(values)


def edge_transfer(support):
    return frozenset(b for b in COLORS if any(a != b for a in support))


def capacity_audit():
    cases = 0
    for mask in range(1, 16):
        a = frozenset(c for c in COLORS if mask & (1 << c))
        expected = COLORS if len(a) >= 2 else COLORS - a
        assert edge_transfer(a) == expected
        for supmask in range(16):
            s = frozenset(c for c in COLORS if supmask & (1 << c))
            if a <= s:
                # Each partial first-step projection has support containing A.
                assert edge_transfer(a) <= edge_transfer(s)
                assert len(COLORS - edge_transfer(s)) <= 1
                if len(a) == 1:
                    assert COLORS - edge_transfer(s) <= a
                cases += 1
    # Without Group A, four differently colored x-neighbors leave no color
    # for x. Their anchored triples forbid four *different* y colors.
    empty_a_b_forbidden = [sorted(COLORS - edge_transfer(available(triple)))
                           for triple in combinations(range(4), 3)]
    assert sorted(c for group in empty_a_b_forbidden for c in group) == list(range(4))
    return {"nonempty_full_supports": 15, "support_superset_pairs": cases,
            "empty_support_countercontrol": list(sorted(edge_transfer(frozenset()))),
            "without_Group_A_different_B_forbidden_colors": empty_a_b_forbidden,
            "hypothesis": "the same residual assignment satisfies Group A"}


def triangle_audit():
    result = []
    for degree in range(3, 9):
        groups = list(combinations(range(2, degree), min(2, degree - 2)))
        count = 0
        for row in product(range(4), repeat=degree):
            direct = row[0] != row[1] and bool(available(row))
            compressed = all(row[0] != row[1] and bool(available(
                (row[0], row[1], *(row[i] for i in pair)))) for pair in groups)
            assert direct == compressed
            count += 1
        result.append({"degree": degree, "tables": len(groups),
                       "candidate_tables_formula": comb(degree - 2, min(2, degree - 2)),
                       "complete_boundary_rows_checked": count})
    return result


def two_step_audit(graph, x, y, name):
    """Only the pair's original incident edges; no residual edge conditioning."""
    assert graph.has_edge(x, y)
    s = set(graph[x]) - {y}
    t = set(graph[y]) - {x}
    scope = sorted(s | t)
    st = list(combinations(sorted(s), 3))
    tt = list(combinations(sorted(t), 3))
    cross_scopes = {frozenset(a) | frozenset(b) for a in st for b in tt}
    checked = rejected = cross_rejected = 0
    for row in product(range(4), repeat=len(scope)):
        assignment = dict(zip(scope, row))
        ax = available(assignment[v] for v in s)
        ay = available(assignment[v] for v in t)
        direct = any(a != b for a in ax for b in ay)
        separate = bool(ax) and bool(ay)
        cross = not any(
            len({assignment[v] for v in a}) == 3
            and {assignment[v] for v in a} == {assignment[v] for v in b}
            for a in st for b in tt)
        assert direct == (separate and cross)
        checked += 1
        rejected += not direct
        cross_rejected += separate and not cross
    return {"name": name, "vertices": len(graph), "edges": graph.number_of_edges(),
            "source_graph": {"vertices": sorted(graph),
                             "edges": sorted(sorted(edge) for edge in graph.edges())},
            "eliminated_pair": [x, y],
            "planar": nx.check_planarity(graph)[0], "degrees": [graph.degree(x), graph.degree(y)],
            "common_neighbors": len(s & t), "interface_size": len(scope),
            "cross_candidate_pairs": len(st) * len(tt),
            "distinct_cross_source_scopes": len(cross_scopes),
            "minimum_cross_source_scope": min(map(len, cross_scopes), default=None),
            "complete_boundary_rows_checked": checked, "rejected_rows": rejected,
            "rejected_after_nonempty_separate_supports": cross_rejected}


def four_variable_kernel():
    rejected = []
    for a, b, p, q in product(range(4), repeat=4):
        ax, ay = available((a, b, p)), available((a, b, q))
        bad = not any(x != y for x in ax for y in ay)
        formula = a != b and p == q and p not in {a, b}
        assert bad == formula
        if bad:
            rejected.append([a, b, p, q])
    assert len(rejected) == 24
    return {"rows": 256, "rejected": len(rejected), "accepted": 256 - len(rejected),
            "rejected_rows": rejected}


def color_search(graph, count):
    """Complete DSATUR search with first-use color symmetry; no search cap."""
    assignment = {}
    nodes = 0

    def visit():
        nonlocal nodes
        nodes += 1
        if len(assignment) == len(graph):
            return dict(assignment)
        vertex = max((v for v in graph if v not in assignment), key=lambda v: (
            len({assignment[w] for w in graph[v] if w in assignment}), graph.degree(v), -v))
        blocked = {assignment[w] for w in graph[vertex] if w in assignment}
        # Every color is symmetric before its first use. Introduce at most
        # the next unused color; this retains one representative of every orbit.
        next_color = min(count - 1, max(assignment.values(), default=-1) + 1)
        for color in range(next_color + 1):
            if color in blocked:
                continue
            assignment[vertex] = color
            found = visit()
            if found is not None:
                return found
            del assignment[vertex]
        return None

    witness = visit()
    if witness is not None:
        assert all(witness[a] != witness[b] for a, b in graph.edges())
    return witness, nodes


def run():
    icosahedron = nx.icosahedral_graph()
    x, y = next(iter(icosahedron.edges()))
    mycielski = nx.mycielskian(nx.mycielskian(nx.cycle_graph(5)))
    assert not any(nx.triangles(mycielski).values())
    bad4, nodes4 = color_search(mycielski, 4)
    good5, nodes5 = color_search(mycielski, 5)
    assert bad4 is None and good5 is not None
    k212 = nx.complete_bipartite_graph(2, 12)
    first = comb(11, 3)
    assert nx.check_planarity(k212)[0] and comb(first, 3) == 735130
    return {
        "schema": "independent-original-edge-two-step-v1",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "networkx_version": nx.__version__,
        "capacity": capacity_audit(),
        "triangle_anchor": triangle_audit(),
        "two_step": [two_step_audit(nx.complete_graph(5), 0, 1, "K5"),
                     two_step_audit(icosahedron, x, y, "icosahedron_adjacent_degree_five"),
                     two_step_audit(nx.complete_bipartite_graph(2, 6), 0, 2, "K2_6_hub_then_leaf")],
        "four_variable_kernel": four_variable_kernel(),
        "K2_12": {"first_anchor_candidates": first, "old_second_candidates": comb(first, 3),
                   "extra_Group_A_candidates": comb(11, 4),
                   "second_new_constraints_under_Group_A": 0,
                   "reason": "one original edge and one coherent predecessor bundle each forbid at most one color"},
        "Mycielski_squared_C5": {"vertices": len(mycielski), "edges": mycielski.number_of_edges(),
                                  "planar": nx.check_planarity(mycielski)[0],
                                  "maximum_common_neighbors_on_an_edge": max(
                                      len(set(mycielski[a]) & set(mycielski[b])) for a, b in mycielski.edges()),
                                  "minimum_cross_source_scope": 6,
                                  "four_coloring": False, "four_color_search_nodes": nodes4,
                                  "five_color_search_nodes": nodes5,
                                  "five_color_witness": good5},
        "limits": ["no claim about later arbitrary factors, fixed domains, or semijoin simplification",
                   "no Lean theorem added; no general runtime or 4CT conclusion",
                   "the current anchored representation already is exact without explicit Group A"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        with args.out.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
