#!/usr/bin/env python3
"""Independent direct-coloring checks; imports no primary checker helpers."""

from collections import Counter
from itertools import product
import argparse
import gzip
import json
from pathlib import Path


def edge(a, b):
    return tuple(sorted((a, b)))


def normalize(values):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in values)


def colorings(vertices, edges, fixed):
    adjacency = {x: set() for x in vertices}
    for a, b in edges:
        assert a != b
        adjacency[a].add(b)
        adjacency[b].add(a)
    assignment = dict(fixed)
    assert all(assignment[a] != assignment[b] for a, b in edges
               if a in assignment and b in assignment)
    order = sorted((x for x in vertices if x not in fixed),
                   key=lambda x: (-len(adjacency[x]), x))

    def visit(index):
        if index == len(order):
            yield tuple(assignment[x] for x in vertices)
            return
        x = order[index]
        forbidden = {assignment[y] for y in adjacency[x] if y in assignment}
        for value in range(4):
            if value not in forbidden:
                assignment[x] = value
                yield from visit(index + 1)
        assignment.pop(x, None)

    yield from visit(0)


def main():
    cycle = {edge(i, (i + 1) % 5) for i in range(5)}
    diagonals = [edge(i, (i + 2) % 5) for i in range(5)]
    tuples = list(product(range(4), repeat=5))
    proper = [t for t in tuples if all(t[a] != t[b] for a, b in cycle)]
    rims = Counter()
    for t in proper:
        count = sum(t[a] == t[b] for a, b in diagonals)
        available = tuple(c for c in range(4) if c not in t)
        assert count - 1 == len(available)
        sectors = [i for i in range(5)
                   if t[(i + 1) % 5] == t[(i + 3) % 5]
                   and t[(i + 2) % 5] == t[(i + 4) % 5]]
        assert len(sectors) == len(available)
        rims[(len(set(t)), count)] += 1

    target = {t for t in proper if len(set(t)) == 3}
    chord_masks = []
    for mask in range(32):
        added = [diagonals[i] for i in range(5) if mask & (1 << i)]
        accepted = {t for t in proper if all(t[a] != t[b] for a, b in added)}
        four_color = [t for t in accepted if len(set(t)) == 4]
        assert accepted != target
        assert not accepted or four_color
        chord_masks.append({"mask": mask, "accepted": len(accepted),
                            "forbidden_four_color": len(four_color),
                            "lost_wheel_rims": len(target - accepted)})

    # B=0..4; U=5..9; x=10 subdivides b0-u0 in the annulus.
    # Center v=11 is entirely inside the induced U pentagon.
    B, U = tuple(range(5)), tuple(range(5, 10))
    H_vertices = tuple(range(11))
    H_edges = (cycle | {edge(5 + a, 5 + b) for a, b in cycle}
               | {edge(i, 5 + i) for i in range(1, 5)}
               | {edge(0, 10), edge(5, 10)})
    G_vertices = tuple(range(12))
    G_edges = H_edges | {edge(11, u) for u in U}
    rows = sorted({normalize(t) for t in proper})
    assert len(rows) == 10
    results = []
    all_h_lifts = all_g_lifts = quotient_lifts = empty_h_cells = 0
    for beta in rows:
        fixed = dict(zip(B, beta))
        H = set(colorings(H_vertices, H_edges, fixed))
        G = set(colorings(G_vertices, G_edges, fixed))
        projected_G = {t[:-1] for t in G}
        assert len(projected_G) == len(G)
        lifted_quotients = []
        quotient_sizes = []
        for a, b in diagonals:
            source, target_vertex = sorted((5 + a, 5 + b))
            mapping = {x: source if x == target_vertex else x for x in H_vertices}
            vertices = tuple(sorted(set(mapping.values())))
            edges = {edge(mapping[a], mapping[b]) for a, b in H_edges}
            assert all(a != b for a, b in edges)
            Q = set(colorings(vertices, edges, fixed))
            indices = {x: i for i, x in enumerate(vertices)}
            pulled = {tuple(t[indices[mapping[x]]] for x in H_vertices) for t in Q}
            assert len(pulled) == len(Q)
            assert pulled == {t for t in H if t[source] == t[target_vertex]}
            lifted_quotients.append(pulled)
            quotient_sizes.append(len(Q))
        for eta in H:
            multiplicity = sum(eta in q for q in lifted_quotients)
            assert multiplicity - 1 == int(eta in projected_G)
        decoded = {eta for eta in H
                   if sum(eta in q for q in lifted_quotients) - 1 == 1}
        restored = {eta + (next(c for c in range(4) if c not in eta[5:10]),)
                    for eta in decoded}
        assert restored == G
        assert sum(quotient_sizes) - len(H) == len(G)
        # Compare entire fibres for all 4^5 cells, including impossible rim cells.
        for rim in tuples:
            h_cell = {t for t in H if t[5:10] == rim}
            g_cell = {t for t in G if t[5:10] == rim}
            restored_cell = {t for t in restored if t[5:10] == rim}
            assert g_cell == restored_cell
            if not h_cell:
                empty_h_cells += 1
        all_h_lifts += len(H)
        all_g_lifts += len(G)
        quotient_lifts += sum(quotient_sizes)
        results.append({"beta": beta, "H_lifts": len(H), "G_lifts": len(G),
                        "quotient_lifts": quotient_sizes})

    # Explicit topological obstruction: double quotient of the ordinary prism.
    # a=u1=u3, c=u2=u4, s=u0. Delete s to expose K3,3 with one edge subdivided.
    prism_edges = ({edge(i, (i + 1) % 5) for i in range(5)}
                   | {edge(5 + i, 5 + (i + 1) % 5) for i in range(5)}
                   | {edge(i, 5 + i) for i in range(5)})
    mapping = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4,
               5: 5, 6: 6, 7: 7, 8: 6, 9: 7}
    double_edges = {edge(mapping[a], mapping[b]) for a, b in prism_edges}
    left, right = (7, 1, 3), (6, 2, 4)
    paths = []
    used_internal = set()
    for a, b in product(left, right):
        path = (1, 0, 4) if (a, b) == (1, 4) else (a, b)
        assert all(edge(x, y) in double_edges for x, y in zip(path, path[1:]))
        internal = set(path[1:-1])
        assert not internal.intersection(set(left) | set(right) | used_internal)
        used_internal.update(internal)
        paths.append(path)

    return {
        "status": "PASS",
        "method": "Independent standard-library direct DFS; no primary checker imports",
        "rim_assignments": len(tuples), "proper_rim_assignments": len(proper),
        "rim_cases": [{"colors": k[0], "equal_diagonal_pairs": k[1], "count": v}
                      for k, v in sorted(rims.items())],
        "zero_new_vertex_graphs": chord_masks,
        "zero_new_vertex_nonempty_sound_relations": 0,
        "ten_pin_full_fibre_source": {
            "B": B, "U": U, "annular_extra_vertex": 10, "center": 11,
            "H_edges": sorted(H_edges), "rows": results,
            "cells_checked": len(rows) * len(tuples),
            "empty_H_cells": empty_h_cells,
            "H_lifts": all_h_lifts, "G_lifts": all_g_lifts,
            "quotient_lifts": quotient_lifts,
        },
        "double_quotient_nonplanarity": {
            "prism_edges": sorted(prism_edges), "quotient_map": mapping,
            "K33_left": left, "K33_right": right, "nine_disjoint_paths": paths,
            "certificate": "K3,3 subdivision; edge b1-b4 subdivided by b0",
        },
    }


def verify_primary(path):
    """Re-enumerate the primary literal graphs without importing their checker."""
    with gzip.open(path, "rt") as handle:
        certificate = json.load(handle)
    B, U = tuple(range(5)), tuple(range(5, 10))
    center = 10
    rims = list(product(range(4), repeat=5))
    rows = sorted({normalize(t) for t in rims
                   if all(t[i] != t[(i + 1) % 5] for i in range(5))})
    assert certificate["B"] == list(B) and certificate["U"] == list(U)
    assert certificate["v"] == center
    assert certificate["beta_domain"] == [list(t) for t in rows]
    assert certificate["tau_domain"] == [list(t) for t in rims]
    statistics = Counter()
    for graph in certificate["graphs"]:
        hv = tuple(graph["h_vertices"])
        he = {tuple(e) for e in graph["h_edges"]}
        assert he == {edge(*e) for e in he}
        assert center not in hv and set(B + U) <= set(hv)
        expected_rim = {edge(U[i], U[(i + 1) % 5]) for i in range(5)}
        assert {e for e in he if set(e) <= set(U)} == expected_rim
        gv = tuple(sorted(hv + (center,)))
        ge = he | {edge(center, u) for u in U}
        assert graph["g_vertices"] == list(gv)
        assert graph["g_edges"] == [list(e) for e in sorted(ge)]
        assert len(graph["rows"]) == 10 and len(graph["quotients"]) == 5
        for row_index, beta in enumerate(rows):
            fixed = dict(zip(B, beta))
            H = set(colorings(hv, he, fixed))
            G = set(colorings(gv, ge, fixed))
            record = graph["rows"][row_index]
            assert record["beta"] == list(beta) and len(record["cells"]) == 1024
            cells = {rim: [] for rim in rims}
            indices = [hv.index(u) for u in U]
            for eta in H:
                cells[tuple(eta[i] for i in indices)].append(eta)
            for rim, cell in zip(rims, record["cells"]):
                assert cell == [list(t) for t in sorted(cells[rim])]
            assert record["g_lifts"] == [list(t) for t in sorted(G)]
            assert record["h_count"] == len(H) and record["g_count"] == len(G)
            qcounts = []
            for j, quotient in enumerate(graph["quotients"]):
                a, b = U[j], U[(j + 2) % 5]
                pi = {x: min(a, b) if x in (a, b) else x for x in hv}
                qv = tuple(sorted(set(pi.values())))
                qe = {edge(pi[a], pi[b]) for a, b in he}
                assert quotient["j"] == j and quotient["pair"] == [a, b]
                assert quotient["map"] == [[x, pi[x]] for x in hv]
                assert quotient["vertices"] == list(qv)
                assert quotient["edges"] == [list(e) for e in sorted(qe)]
                Q = set(colorings(qv, qe, fixed))
                qrow = quotient["rows"][row_index]
                assert qrow["beta"] == list(beta)
                assert qrow["lifts"] == [list(t) for t in sorted(Q)]
                qcounts.append(len(Q))
            assert record["quotient_counts"] == qcounts
            assert sum(qcounts) - len(H) == len(G)
            statistics.update({"rows": 1, "cells": 1024, "H_lifts": len(H),
                               "G_lifts": len(G), "quotient_lifts": sum(qcounts)})
        statistics["graphs"] += 1
    return dict(statistics)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, help="write a new certificate exclusively")
    action.add_argument("--check", type=Path, help="recompute and compare without writing")
    parser.add_argument("--primary", type=Path,
                        help="also independently re-enumerate a primary gzip certificate")
    arguments = parser.parse_args()
    result = main()
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    destination = arguments.write or arguments.check or Path(__file__).with_name("independent_results.json")
    if arguments.write:
        with destination.open("x") as handle:
            handle.write(serialized)
    elif destination.read_text() != serialized:
        raise SystemExit("FAIL: independent certificate differs from direct recomputation")
    output = {"status": result["status"],
                      "rim_assignments": result["rim_assignments"],
                      "cells_checked": result["ten_pin_full_fibre_source"]["cells_checked"],
                      "H_lifts": result["ten_pin_full_fibre_source"]["H_lifts"],
                      "G_lifts": result["ten_pin_full_fibre_source"]["G_lifts"],
                      "action": "write" if arguments.write else "read-only check",
                      "certificate": str(destination)}
    if arguments.primary:
        output["primary_independent_comparison"] = verify_primary(arguments.primary)
    print(json.dumps(output, sort_keys=True))
