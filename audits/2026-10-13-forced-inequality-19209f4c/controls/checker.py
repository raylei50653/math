#!/usr/bin/env python3
"""Exact finite controls for forced inequality; no Four Color Theorem oracle.

Generation uses exclusive creation. --check recomputes complete named colorings,
relations (including all empty pair cells), embeddings and source predicates.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parent.parent


def colorings(g, pins=None):
    vertices = tuple(sorted(g))
    assignment = dict(pins or {})
    if any(u in assignment and v in assignment and assignment[u] == assignment[v]
           for u, v in g.edges):
        return []
    out = []

    def visit():
        if len(assignment) == len(vertices):
            out.append(tuple(assignment[v] for v in vertices))
            return
        choices = []
        for v in vertices:
            if v not in assignment:
                allowed = tuple(c for c in range(4)
                                if all(assignment.get(w) != c for w in g[v]))
                choices.append((len(allowed), -g.degree(v), v, allowed))
        _, _, v, allowed = min(choices)
        for c in allowed:
            assignment[v] = c
            visit()
            del assignment[v]

    visit()
    return sorted(out)


def brute(g, pins=None):
    pins = pins or {}
    return [p for p in it.product(range(4), repeat=len(g))
            if all(p[v] == c for v, c in pins.items())
            and all(p[u] != p[v] for u, v in g.edges)]


def path_cube(n):
    return nx.Graph((i, j) for i in range(n) for j in range(i + 1, min(n, i + 4)))


def diamond_chain(m, leaf):
    g = nx.Graph()
    for i in range(m):
        triangle = tuple(range(m + 1 + 3 * i, m + 4 + 3 * i))
        g.add_edges_from(it.combinations(triangle, 2))
        g.add_edges_from((v, t) for v in (i, i + 1) for t in triangle)
    endpoint = m
    if leaf:
        endpoint = len(g)
        g.add_edge(m, endpoint)
    return g, (0, endpoint)


def branching(depth):
    g = nx.complete_graph(4)
    faces = [(0, 1, 3), (1, 2, 3), (0, 2, 3)]
    for _ in range(depth):
        next_faces = []
        for f in faces:
            v = len(g)
            g.add_edges_from((v, u) for u in f)
            next_faces.extend(tuple(sorted((*edge, v))) for edge in it.combinations(f, 2))
        faces = sorted(next_faces)
    return g


def wrapped(n):
    g = nx.cycle_graph(5)
    core = nx.relabel_nodes(path_cube(n), {i: i + 5 for i in range(n)})
    g.add_edges_from(core.edges)
    g.add_edge(0, 5)
    terminal_face = tuple(range(n + 2, n + 5))
    cap = tuple(range(n + 5, n + 8))
    g.add_edges_from(it.combinations(cap, 2))
    g.add_edges_from((v, w) for i, v in enumerate(cap)
                     for j, w in enumerate(terminal_face) if i != j)
    return g


def normalize(row):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in row)


REPS = sorted({normalize(p) for p in it.product(range(4), repeat=5)
               if all(p[i] != p[(i + 1) % 5] for i in range(5))})


def topology(g, boundary=None):
    planar, embedding = nx.check_planarity(g, counterexample=True)
    result = {"planar": planar}
    if planar:
        embedding.check_structure()
        result["rotation"] = [[v, list(embedding.neighbors_cw_order(v))] for v in sorted(g)]
    else:
        result["kuratowski_edges"] = sorted(sorted(e) for e in embedding.edges)
    if boundary:
        apex = g.copy()
        apex.add_edges_from((len(g), v) for v in boundary)
        result["specified_boundary_disk"] = nx.check_planarity(apex)[0]
    return result


def record(name, g, pair, boundary=None, pins=None):
    g = nx.Graph(sorted(tuple(sorted(e)) for e in g.edges))
    lifts = colorings(g, pins)
    assert lifts, name
    if len(g) <= 8:
        assert lifts == brute(g, pins), name
    u, v = pair
    fibers = [[a, b, [i for i, p in enumerate(lifts) if (p[u], p[v]) == (a, b)]]
              for a, b in it.product(range(4), repeat=2)]
    relation = [[a, b] for a, b, f in fibers if f]
    outcome = ("equality" if all(a == b for a, b in relation) else
               "inequality" if all(a != b for a, b in relation) else "free")
    return {"name": name, "n": len(g), "edges": sorted(sorted(e) for e in g.edges),
            "pair": list(pair), "boundary": boundary, "pins": pins,
            "distance": nx.shortest_path_length(g, u, v),
            "degrees": [g.degree(i) for i in range(len(g))],
            "full_lifts": lifts, "pair_fibres": fibers, "outcome": outcome,
            **topology(g, boundary)}


def compute():
    records = []
    for n in (4, 5, 6, 9, 10, 14, 26, 50, 98):
        r = record(f"stacked_path_{n}", path_cube(n), (0, n - 1))
        assert len(r["full_lifts"]) == 24
        assert r["outcome"] == ("equality" if (n - 1) % 4 == 0 else "inequality")
        assert r["distance"] == (n + 1) // 3
        assert r["planar"]
        records.append(r)
    for m in (1, 2, 3):
        for leaf in (False, True):
            g, pair = diamond_chain(m, leaf)
            r = record(f"equal_chain_{m}_leaf_{int(leaf)}", g, pair)
            assert r["outcome"] == ("inequality" if leaf else "equality")
            assert len(r["full_lifts"]) == (12 if leaf else 4) * 6 ** m
            assert r["distance"] == 2 * m + int(leaf)
            assert r["planar"]
            records.append(r)
    for depth in (1, 2, 3):
        g = branching(depth)
        r = record(f"three_face_branch_{depth}", g, (0, len(g) - 1))
        assert len(r["full_lifts"]) == 24 and r["planar"]
        records.append(r)
    for k in (1, 2, 3, 4):
        g = nx.complete_graph(3)
        g.add_edges_from((i, j) for i in range(3, 3 + k) for j in range(3))
        r = record(f"same_triangle_{k}_apices", g, (0, 3) if k == 1 else (3, 4))
        assert r["planar"] == (k <= 2)
        assert len(r["full_lifts"]) == 24
        records.append(r)
    for name, chords in (("crossed", [(0, 2), (1, 3)]),
                         ("uncrossed", [(0, 2), (2, 4)])):
        g = nx.cycle_graph(5)
        g.add_edges_from(chords)
        r = record(f"c5_{name}_chords", g, (0, 2), list(range(5)))
        assert r["planar"] and r["specified_boundary_disk"] == (name == "uncrossed")
        records.append(r)
    for n in (6, 10, 14, 26):
        g = wrapped(n)
        rows = []
        for q in REPS:
            r = record(f"wrapped_{n}_q{''.join(map(str,q))}", g, (5, n + 4),
                       list(range(5)), dict(enumerate(q)))
            assert r["planar"] and r["specified_boundary_disk"]
            assert r["outcome"] == "inequality"
            assert min(r["degrees"][5:]) >= 4
            assert sum(d - 4 for d in r["degrees"][5:]) == 2 * n - 5
            assert r["distance"] == (n + 1) // 3
            rows.append(r)
        # Deleting the bridge leaves every row accepted: one concrete failure of
        # Sigma-critical, stronger than merely failing a sufficient test.
        reduced = g.copy()
        reduced.remove_edge(0, 5)
        deletion_witnesses = []
        for q in REPS:
            lifts = colorings(reduced, dict(enumerate(q)))
            assert lifts
            deletion_witnesses.append([q, lifts[0]])
        records.append({"name": f"wrapped_{n}", "rows": rows,
                        "epsilon": 2 * n - 5, "sigma": 1023,
                        "sigma_critical": False, "deleted_edge": [0, 5],
                        "deleted_graph_witnesses": deletion_witnesses,
                        "full_source_status": "not triggered"})
    return {"schema": 1, "four_color_theorem_used": False, "records": records}


def check_frozen():
    manifest = json.loads((AUDIT / "BASE.json").read_text())
    for name, digest in manifest["inputs"].items():
        assert hashlib.sha256((AUDIT / "frozen" / name).read_bytes()).hexdigest() == digest


def summary(data):
    flat = [row for r in data["records"] for row in r.get("rows", [r])]
    return {"families_and_sizes": len(data["records"]), "complete_coloring_controls": len(flat),
            "full_lifts": sum(len(r["full_lifts"]) for r in flat),
            "max_forced_pair_graph_distance": max(r["distance"] for r in flat),
            "planar_controls": sum(r["planar"] for r in flat),
            "nonplanar_controls": sum(not r["planar"] for r in flat),
            "low_excess_critical_C5_source": "not triggered"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    if bool(args.check) == bool(args.write):
        parser.error("choose exactly one of --check or --write")
    check_frozen()
    data = compute()
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n"
    if args.write:
        with args.write.open("x") as out:
            out.write(payload)
    else:
        if args.check.read_text() != payload:
            raise SystemExit("FAIL: certificate differs from complete recomputation")
    print(json.dumps(summary(data), sort_keys=True))


if __name__ == "__main__":
    main()
