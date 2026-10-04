#!/usr/bin/env python3
"""Independent D3 C2 graph audit: no imports from production checkers."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIVE = HERE.parents[2]
Q, U = (0, 1, 0, 1, 2), set(range(4))
CONTACTS, P3 = (10, 11, 12), (7, 8, 9)
SUPPORTS = ((0, 1, 4), (1, 4), (4,))
C2 = "artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json"
C = "artifacts/c5_mixed_p3_common_endpoint/observations.json"
ALIASES = {**{i: f"b{i}" for i in range(5)}, 5: "z", 6: "w",
           **{v: f"x{i}" for i, v in enumerate(P3)},
           **{v: f"u{i}" for i, v in enumerate(CONTACTS)}}


def edge(a, b):
    return (min(a, b), max(a, b))


FRAME = {edge(i, (i + 1) % 5) for i in range(5)}
P3_INTERNAL = {(7, 8), (8, 9)}
P3_ATTACHMENTS = {edge(v, b) for v, bs in zip(P3, SUPPORTS) for b in bs}
ROOT_ORIGINAL = {(5, 6), (5, 9), (6, 9)}
CONTEXT = FRAME | P3_INTERNAL | P3_ATTACHMENTS | ROOT_ORIGINAL
TRIANGLE_INTERNAL = {edge(a, b) for a, b in combinations(CONTACTS, 2)}
TRIANGLE_ATTACHMENTS = {edge(v, a) for v in CONTACTS for a in (1, 5)}
TRIANGLE = TRIANGLE_INTERNAL | TRIANGLE_ATTACHMENTS
PROJECTION = CONTEXT | TRIANGLE


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def col_dict(raw):
    return None if raw is None else {int(v): c for v, c in raw.items()}


def enumerate_colorings(free, edges, pins):
    out = []
    for cs in product(range(4), repeat=len(free)):
        col = pins | dict(zip(free, cs))
        if all(col[a] != col[b] for a, b in edges):
            out.append(col)
    return out


def connected(group, edges):
    if not group:
        return False
    reached = {next(iter(group))}
    while True:
        grown = reached | {b for a, b in edges if a in reached and b in group}
        grown |= {a for a, b in edges if b in reached and a in group}
        if grown == reached:
            return reached == group
        reached = grown


class Audit:
    def __init__(self):
        self.checks, self.failures = 0, []

    def ck(self, name, passed, detail=None):
        self.checks += 1
        if not passed:
            self.failures.append({"check": name, "detail": detail})

    def edges(self, raw, label, expected):
        result = {tuple(e) for e in raw}
        self.ck(label + "/unique", len(result) == len(raw))
        self.ck(label + "/canonical_simple", all(a < b for a, b in result))
        self.ck(label + "/exact_original_set", result == expected,
                {"missing": sorted(expected - result), "extra": sorted(result - expected)})
        return result

    def coloring(self, raw, vertices, edges, pins, label):
        col = col_dict(raw)
        self.ck(label + "/present", col is not None)
        if col is None:
            return None
        self.ck(label + "/exact_vertex_domain", set(col) == set(vertices))
        self.ck(label + "/colors_in_U", all(c in U for c in col.values()))
        self.ck(label + "/shared_frame_and_pins", all(col.get(v) == c for v, c in pins.items()))
        self.ck(label + "/proper_every_retained_edge", all(col.get(a) != col.get(b) for a, b in edges))
        return col

    def minor(self, edges, raw_groups, witnesses, label):
        groups = [set(g) for g in raw_groups]
        self.ck(label + "/five_nonempty_sets", len(groups) == 5 and all(groups))
        self.ck(label + "/sets_disjoint", sum(map(len, groups)) == len(set().union(*groups)))
        for i, g in enumerate(groups):
            self.ck(f"{label}/connected_set_{i}", connected(g, edges))
        self.ck(label + "/ten_distinct_pairs", len(witnesses) == 10 and
                {tuple(w["pair"]) for w in witnesses} == set(combinations(range(5), 2)))
        for n, w in enumerate(witnesses):
            a, b = w["actual_edge"]
            i, j = w["pair"]
            self.ck(f"{label}/witness_{n}_original_edge", edge(a, b) in edges)
            self.ck(f"{label}/witness_{n}_named_sets",
                    (a in groups[i] and b in groups[j]) or (b in groups[i] and a in groups[j]))

    def subdivision(self, record, edges, label):
        branches = tuple(record["branch_vertices"])
        self.ck(label + "/named_branches", branches == (1, 5, 10, 11, 12))
        pairs = [tuple(r["branch_pair"]) for r in record["routes"]]
        self.ck(label + "/ten_distinct_branch_pairs", len(pairs) == 10 and
                set(pairs) == set(combinations(branches, 2)))
        interior_sets, edge_sets, paths = [], [], []
        for n, route in enumerate(record["routes"]):
            a, b = route["branch_pair"]
            path = tuple(route["original_path"])
            self.ck(f"{label}/path_{n}_endpoints", path[0] == a and path[-1] == b)
            self.ck(f"{label}/path_{n}_simple", len(path) == len(set(path)))
            inner = set(path[1:-1])
            self.ck(f"{label}/path_{n}_no_internal_branch", not inner & set(branches))
            used = {edge(x, y) for x, y in zip(path, path[1:])}
            self.ck(f"{label}/path_{n}_every_original_edge", used <= edges,
                    {"extra": sorted(used - edges)})
            interior_sets.append(inner)
            edge_sets.append(used)
            paths.append(path)
        for i, j in combinations(range(len(paths)), 2):
            self.ck(f"{label}/paths_{i}_{j}_internal_disjoint", not interior_sets[i] & interior_sets[j])
            self.ck(f"{label}/paths_{i}_{j}_edge_disjoint", not edge_sets[i] & edge_sets[j])
            self.ck(f"{label}/paths_{i}_{j}_only_shared_endpoints",
                    set(paths[i]) & set(paths[j]) == set(pairs[i]) & set(pairs[j]))
        union = set().union(*edge_sets)
        self.edges(record["subdivision_edges"], label + "/edge_union", union)
        vertices = set(branches) | set().union(*interior_sets)
        degrees = {v: sum(v in e for e in union) for v in vertices}
        self.ck(label + "/branch_and_internal_degrees",
                all(degrees[v] == (4 if v in branches else 2) for v in vertices))
        outside = tuple(record["external_path"])
        self.ck(label + "/named_external_original_path",
                outside in ((5, 9, 4, 3, 2, 1), (5, 9, 4, 0, 1)))
        expected_groups = [{10}, {11}, {12}, {5, *outside[1:-1]}, {1}]
        self.ck(label + "/exact_minor_sets", [set(g) for g in record["branch_sets"]] == expected_groups)
        self.minor(edges, record["branch_sets"], record["minor_adjacency"], label + "/minor")
        return {"external_path": list(outside),
                "external_path_names": [ALIASES[v] for v in outside],
                "path_count": len(paths), "subdivision_edges": len(union),
                "vertices": len(vertices), "internal_vertices": sorted(vertices - set(branches)),
                "edge_pair_disjointness_checks": len(edge_sets) * (len(edge_sets) - 1) // 2,
                "all_edges_with_original_provenance": sorted(union)}
