#!/usr/bin/env python3
"""Exact four-color enumeration and planarity controls; no coloring theorem oracle."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent


def enumerate_colorings(graph, pins):
    nodes = list(graph)
    colors = dict(pins)
    assert set(pins) <= set(nodes)
    assert all(colors[u] != colors[v] for u, v in graph.edges if u in colors and v in colors)
    free = sorted((v for v in nodes if v not in pins), key=lambda v: (-graph.degree(v), v))
    answers = []

    def visit(i):
        if i == len(free):
            answers.append([colors[v] for v in nodes])
            return
        v = free[i]
        forbidden = {colors[u] for u in graph[v] if u in colors}
        for c in range(4):
            if c not in forbidden:
                colors[v] = c
                visit(i + 1)
                del colors[v]

    visit(0)
    return nodes, answers


def certificate(graph):
    planar, proof = nx.check_planarity(graph, counterexample=True)
    if planar:
        proof.check_structure()
        return {"planar": True, "rotation": {v: list(proof.neighbors_cw_order(v)) for v in graph}}
    return {"planar": False, "kuratowski_nodes": list(proof), "kuratowski_edges": [list(e) for e in proof.edges]}


def record(name, graph, pins, terminals, expected_count, expected_planar):
    nodes, colorings = enumerate_colorings(graph, pins)
    assert len(colorings) == expected_count, (name, len(colorings), expected_count)
    cert = certificate(graph)
    assert cert["planar"] == expected_planar, name
    indices = [nodes.index(v) for v in terminals]
    relation = sorted({tuple(row[i] for i in indices) for row in colorings})
    fibres = [[a, b, [i for i, row in enumerate(colorings)
                      if tuple(row[j] for j in indices) == (a, b)]]
              for a, b in itertools.product(range(4), repeat=2)]
    witnesses = {}
    for row in colorings:
        kind = "equal" if row[indices[0]] == row[indices[1]] else "different"
        witnesses.setdefault(kind, row)
    return {
        "name": name,
        "nodes": nodes,
        "edges": [list(e) for e in graph.edges],
        "pins": pins,
        "terminals": list(terminals),
        "terminal_graph_distance": nx.shortest_path_length(graph, *terminals),
        "coloring_count": len(colorings),
        "terminal_relation": [list(r) for r in relation],
        "terminal_fibres": fibres,
        "witnesses": witnesses,
        "colorings": colorings,
        **cert,
    }


def two_hubs(tree, adjacent=True):
    g = tree.copy()
    g.add_nodes_from(["a", "b"])
    if adjacent:
        g.add_edge("a", "b")
    g.add_edges_from((hub, v) for hub in ("a", "b") for v in tree)
    return g


def named_path(n):
    return nx.path_graph([f"v{i}" for i in range(n)])


def shared_clique_book(size, pages):
    shared = [f"s{i}" for i in range(size)]
    g = nx.complete_graph(shared)
    for i in range(pages):
        private = [f"p{i}_{j}" for j in range(4-size)]
        g.add_edges_from(itertools.combinations(shared + private, 2))
    return g


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    if bool(args.write) == bool(args.check):
        parser.error("choose exactly one of --write or --check")
    rows = []
    for n in range(2, 9):
        t = named_path(n)
        rows.append(record(f"ordinary_path_n{n}", t, {"v0": 2}, ("v0", f"v{n-1}"), 3**(n-1), True))
        rows.append(record(f"two_adjacent_hubs_path_n{n}", two_hubs(t), {"a": 0, "b": 1, "v0": 2}, ("v0", f"v{n-1}"), 1, True))
        rows.append(record(f"two_unlinked_distinct_pinned_hubs_path_n{n}", two_hubs(t, False), {"a": 0, "b": 1, "v0": 2}, ("v0", f"v{n-1}"), 1, True))
        rows.append(record(f"two_unlinked_same_pinned_hubs_path_n{n}", two_hubs(t, False), {"a": 0, "b": 0, "v0": 2}, ("v0", f"v{n-1}"), 2**(n-1), True))

    for leaves in range(1, 6):
        t = nx.star_graph(["v0"] + [f"v{i}" for i in range(1, leaves+1)])
        terminals = ("v0", "v1") if leaves == 1 else ("v1", "v2")
        for adjacent in (True, False):
            row = record(f"two_hubs_star_leaves{leaves}_adjacent{adjacent}", two_hubs(t, adjacent), {"a": 0, "b": 1, "v0": 2}, terminals, 1, leaves <= 2)
            if leaves >= 3:
                left, right = ["a", "b", "v0"], ["v1", "v2", "v3"]
                assert all(row_edge(row, u, v) for u in left for v in right)
                row["literal_K33_parts"] = [left, right]
            rows.append(row)

        private = t.copy()
        pins = {"v0": 2}
        for v in t:
            for j in range(2):
                support = f"support_{v}_{j}"
                private.add_edge(v, support)
                pins[support] = j
        rows.append(record(f"private_external_pinned_supports_star_leaves{leaves}", private, pins, terminals, 1, True))
        rows.append(record(f"private_unpinned_supports_star_leaves{leaves}", private, {"v0": 2}, terminals, 3**(private.number_of_nodes()-1), True) if leaves <= 2 else {
            "name": f"private_unpinned_supports_star_leaves{leaves}",
            "status": "formula_only_not_enumerated",
            "nodes": list(private), "edges": [list(e) for e in private.edges],
            "pins": {"v0": 2}, "coloring_count_formula": f"3^{private.number_of_nodes()-1}",
            "proof": "The literal graph is a tree, so every nonroot vertex has three choices after its parent.",
        })

    for n in range(3, 9):
        cycle = nx.cycle_graph([f"v{i}" for i in range(n)])
        rows.append(record(f"two_adjacent_hubs_cycle_n{n}", two_hubs(cycle), {"a": 0, "b": 1, "v0": 2}, ("a", "b"), 1 if n % 2 == 0 else 0, False))
        rows.append(record(f"two_unlinked_distinct_pinned_hubs_cycle_n{n}", two_hubs(cycle, False), {"a": 0, "b": 1, "v0": 2}, ("a", "b"), 1 if n % 2 == 0 else 0, True))
        rows.append(record(f"two_unlinked_same_pinned_hubs_cycle_n{n}", two_hubs(cycle, False), {"a": 0, "b": 0, "v0": 2}, ("a", "b"), (2**n + 2*(-1)**n)//3, True))
        # Only a=0 is fixed: enumerate all completions and retain the full hub relation.
        free_b_count = 2**n + 2*(-1)**n + (6 if n % 2 == 0 else 0)
        rows.append(record(f"two_unlinked_hubs_free_b_cycle_n{n}", two_hubs(cycle, False), {"a": 0}, ("a", "b"), free_b_count, True))

    for size in (1, 2, 3):
        for pages in range(2, 6):
            g = shared_clique_book(size, pages)
            pins = {f"s{j}": j for j in range(size)}
            pins.update({f"p0_{j}": size+j for j in range(4-size)})
            factorial = {1: 6, 2: 2, 3: 1}[size]
            rows.append(record(f"K4_book_shared_clique{size}_pages{pages}", g, pins, ("p0_0", "p1_0"), factorial**(pages-1), size < 3 or pages <= 2))

    result = {
        "scope": "Exact literal graphs, one global color frame, colors 0,1,2,3; each listed row contains every coloring extending its pins unless explicitly formula_only_not_enumerated.",
        "networkx_version": nx.__version__,
        "case_count": len(rows),
        "enumerated_case_count": sum("colorings" in row for row in rows),
        "rows": rows,
    }
    payload = json.dumps(result, indent=2) + "\n"
    out = args.write or args.check
    if args.write:
        with out.open("x") as handle:
            handle.write(payload)
    elif out.read_text() != payload:
        raise SystemExit("FAIL: certificate differs from complete recomputation")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({"mode": "write" if args.write else "check", "cases": len(rows), "enumerated_cases": result["enumerated_case_count"], "total_colorings": sum(row.get("coloring_count", 0) for row in rows), "sha256": digest, "output": str(out)}, indent=2))


def row_edge(row, u, v):
    return [u, v] in row["edges"] or [v, u] in row["edges"]


if __name__ == "__main__":
    main()
