#!/usr/bin/env python3
"""Independent, finite controls for W3-TRANSPORT; Python standard library only.

The four graphs are literal annuli, not claimed minimal outside-catalogue
sources. All 10 * 1024 cells and all full lifts are retained in certificate.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = range(4)
B = list(range(5))
U = list(range(5, 10))
BETAS = [
    [0, 1, 0, 1, 2], [0, 1, 0, 2, 1], [0, 1, 0, 2, 3],
    [0, 1, 2, 0, 1], [0, 1, 2, 0, 2], [0, 1, 2, 0, 3],
    [0, 1, 2, 1, 2], [0, 1, 2, 1, 3], [0, 1, 2, 3, 1],
    [0, 1, 2, 3, 2],
]
TAUS = list(itertools.product(COLORS, repeat=5))


def norm(seq):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in seq)


def make_graph(name, diagonal_mask=None, decorated=False):
    faces = [list(reversed(B))]
    for i in range(5):
        a, b, c, d = i, (i + 1) % 5, 5 + (i + 1) % 5, 5 + i
        if diagonal_mask is None:
            if decorated and i == 0:
                faces.extend([[d, a, 10], [a, b, c, d, 10]])
            else:
                faces.append([a, b, c, d])
        elif diagonal_mask & (1 << i):
            faces.extend([[a, b, c], [a, c, d]])
        else:
            faces.extend([[a, b, d], [b, c, d]])
    faces.append(U[:])
    darts = Counter((face[i], face[(i + 1) % len(face)])
                    for face in faces for i in range(len(face)))
    assert all(n == 1 and darts[v, u] == 1 for (u, v), n in darts.items())
    edges = sorted({tuple(sorted(e)) for e in darts})
    n = 11 if decorated else 10
    assert n - len(edges) + len(faces) == 2
    # Oriented facial walks specify a spherical rotation system. Their two
    # distinguished C5 faces are the boundary components of this annulus.
    turns = {u: {} for u in range(n)}
    for face in faces:
        for i, v in enumerate(face):
            turns[v][face[i - 1]] = face[(i + 1) % len(face)]
    rotation = {}
    for v, turn in turns.items():
        start = min(turn)
        order, w = [], start
        while w not in order:
            order.append(w)
            w = turn[w]
        assert w == start and set(order) == set(turn)
        rotation[str(v)] = order
    return dict(id=name, vertices=list(range(n)), edges=[list(e) for e in edges],
                faces=faces, rotation=rotation,
                edge_ownership="all listed edges belong to this annulus; center spokes absent",
                B=B, U=U, private_vertices=list(range(10, n)))


def enumerate_graph(graph):
    n = len(graph["vertices"])
    edges = graph["edges"]
    rows = []
    for beta in BETAS:
        cells = [[] for _ in TAUS]
        wheel_lifts = []
        for tau_index, tau in enumerate(TAUS):
            for private in itertools.product(COLORS, repeat=n - 10):
                full = beta + list(tau) + list(private)
                if any(full[u] == full[v] for u, v in edges):
                    continue
                cells[tau_index].append(full)
                if len(set(tau)) == 3:
                    center = next(c for c in COLORS if c not in tau)
                    wheel_lifts.append(full + [center])
        # Independent direct DFS of the wheel graph checks the filter.
        wheel_edges = edges + [[u, n] for u in U]
        adjacency = [[] for _ in range(n + 1)]
        for u, v in wheel_edges:
            adjacency[u].append(v)
            adjacency[v].append(u)
        current = beta + [-1] * (n + 1 - 5)
        direct = []

        def visit(v):
            if v == n + 1:
                direct.append(current[:])
                return
            for c in COLORS:
                if all(current[w] != c for w in adjacency[v]):
                    current[v] = c
                    visit(v + 1)
                    current[v] = -1

        visit(5)
        assert sorted(direct) == sorted(wheel_lifts)
        rows.append(dict(beta=beta, cells=cells, wheel_lifts=sorted(wheel_lifts)))
    return graph | {"rows": rows}


def support(graph, three_only=False):
    return {(i, j) for i, row in enumerate(graph["rows"])
            for j, cell in enumerate(row["cells"])
            if cell and (not three_only or len(set(TAUS[j])) == 3)}


def sigma(graph, wheel=False):
    return sum(1 << i for i, row in enumerate(graph["rows"])
               if (bool(row["wheel_lifts"]) if wheel else any(row["cells"])))


def build():
    proper = [t for t in TAUS if all(t[i] != t[(i + 1) % 5] for i in range(5))]
    assert sorted(set(map(norm, proper))) == sorted(map(tuple, BETAS))
    assert Counter(len(set(t)) for t in proper) == {3: 120, 4: 120}
    graphs = [enumerate_graph(make_graph("prism")),
              enumerate_graph(make_graph("prism_decorated", decorated=True)),
              enumerate_graph(make_graph("triangulated_00", 0)),
              enumerate_graph(make_graph("triangulated_01", 1))]
    p, d, t, f = graphs
    assert support(p) == support(d)
    # Retraction deletes the degree-two private vertex. Every original lift
    # has exactly two extensions, proving support equality without a search.
    for row, decorated in zip(p["rows"], d["rows"]):
        for cell, larger in zip(row["cells"], decorated["cells"]):
            assert len(larger) == 2 * len(cell)
            assert {tuple(lift[:10]) for lift in larger} == set(map(tuple, cell))
    assert sigma(p, True) == sigma(t, True) == 1023
    assert support(p, True) != support(t, True)
    beta = [0, 1, 0, 1, 2]
    tau = [1, 0, 1, 0, 3]
    i, j = BETAS.index(beta), TAUS.index(tuple(tau))
    assert p["rows"][i]["cells"][j] and not t["rows"][i]["cells"][j]
    assert sigma(p) == sigma(f) == 1023
    assert sigma(f, True) == 831
    summary = {
        "status": "triggered and holds; four synthetic literal annuli only",
        "proper_three_color_tuples": 120,
        "named_three_color_cells_per_graph": 1200,
        "stored_cells": len(graphs) * len(BETAS) * len(TAUS),
        "graphs": [{"id": g["id"], "annulus_lifts": sum(len(c) for r in g["rows"] for c in r["cells"]),
                    "wheel_lifts": sum(len(r["wheel_lifts"]) for r in g["rows"]),
                    "sigma_annulus": sigma(g), "sigma_wheel": sigma(g, True),
                    "three_color_support_size": len(support(g, True))} for g in graphs],
        "same_wheel_sigma_different_named_support": {
            "graphs": [p["id"], t["id"]], "beta": beta, "tau": tau,
            "prism_full_wheel_lift": p["rows"][i]["cells"][j][0] + [2],
            "rejected_edge_in_triangulated_00": [1, 5]},
        "triangulated_00_one_full_wheel_lift_per_beta": [row["wheel_lifts"][0] for row in t["rows"]],
        "counts_are_not_part_of_transport": "prism_decorated has exactly two lifts over every prism lift",
        "minimal_933_941_sources": "not triggered",
    }
    certificate = {"schema": "w3-transport-controls-v1", "colors": list(COLORS),
                   "B": B, "U": U, "beta_domain": BETAS, "tau_domain": TAUS,
                   "cell_semantics": "Every one of the 1024 ordered tuples has a cell, including empty cells; full vectors follow vertices. Wheel center is appended.",
                   "graphs": graphs}
    return certificate, summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    certificate, summary = build()
    certificate_path, summary_path = HERE / "certificate.json.gz", HERE / "summary.json"
    packed = gzip.compress(json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode(), mtime=0)
    summary_text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.write:
        if certificate_path.exists() or summary_path.exists():
            raise SystemExit("refuse to overwrite an existing evidence file")
        certificate_path.write_bytes(packed)
        summary_path.write_text(summary_text)
    else:
        assert certificate_path.read_bytes() == packed
        assert summary_path.read_text() == summary_text
    print(summary_text, end="")


if __name__ == "__main__":
    main()
