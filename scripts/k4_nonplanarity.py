#!/usr/bin/env python3
"""Certify a K5 minor from a literal K4 and one exterior component.

The detector and certificate checker use only the standard library. A miss
means only that this sufficient condition did not trigger, never planarity.
Input JSON: {"vertices": [integer IDs], "edges": [[u, v], ...]}.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path


def normalize(graph):
    """Validate integer IDs, reject loops, and collapse duplicate undirected edges."""
    vertices = list(graph["vertices"])
    if any(type(v) is not int for v in vertices) or len(set(vertices)) != len(vertices):
        raise ValueError("vertices must be distinct integer IDs")
    vertices = sorted(vertices)
    allowed = set(vertices)
    edges = set()
    for pair in graph["edges"]:
        if len(pair) != 2:
            raise ValueError("each edge must have two endpoints")
        u, v = pair
        if type(u) is not int or type(v) is not int or u not in allowed or v not in allowed:
            raise ValueError("edge endpoints must be declared integer vertices")
        if u == v:
            raise ValueError("simple graphs must not have loops")
        edges.add(tuple(sorted((u, v))))
    return {"vertices": vertices, "edges": [list(e) for e in sorted(edges)]}


def adjacency(graph):
    adj = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def four_cliques(adj):
    """Enumerate each actual K4 once, in lexicographic vertex order."""
    for a in sorted(adj):
        for b in sorted(v for v in adj[a] if v > a):
            common = adj[a] & adj[b]
            for c in sorted(v for v in common if v > b):
                for d in sorted(v for v in common & adj[c] if v > c):
                    yield (a, b, c, d)


def components_outside(adj, removed):
    remaining = set(adj) - removed
    while remaining:
        start = min(remaining)
        remaining.remove(start)
        component, stack, tree = {start}, [start], []
        while stack:
            u = stack.pop()
            for v in sorted(adj[u] & remaining):
                remaining.remove(v)
                component.add(v)
                stack.append(v)
                tree.append([u, v])
        yield component, tree


def detect(graph):
    graph = normalize(graph)
    adj = adjacency(graph)
    scanned, component_checks, maximum = 0, 0, 0
    for clique in four_cliques(adj):
        scanned += 1
        removed = set(clique)
        for component, tree in components_outside(adj, removed):
            component_checks += 1
            touching = [v for v in clique if adj[v] & component]
            maximum = max(maximum, len(touching))
            if len(touching) != 4:
                continue
            links = [{"branches": [i, j], "edge": [clique[i], clique[j]]}
                     for i, j in combinations(range(4), 2)]
            links.extend({"branches": [i, 4],
                          "edge": [v, min(adj[v] & component)]}
                         for i, v in enumerate(clique))
            certificate = {
                "model": "K5", "k4": list(clique),
                "branch_sets": [[v] for v in clique] + [sorted(component)],
                "branch_trees": [[], [], [], [], tree], "links": links,
            }
            verify_certificate(graph, certificate)
            return {"status": "triggered and holds", "detected": True,
                    "certificate": certificate,
                    "scan": {"k4s_scanned": scanned,
                             "exterior_components_checked": component_checks,
                             "max_attachment_count": maximum,
                             "stopped_at_first_certificate": True}}
    return {"status": "not triggered", "detected": False, "certificate": None,
            "scan": {"k4s_scanned": scanned,
                     "exterior_components_checked": component_checks,
                     "max_attachment_count": maximum,
                     "stopped_at_first_certificate": False}}


def verify_certificate(graph, certificate):
    """Independently check a K5 model against original edges; no planarity oracle."""
    graph = normalize(graph)
    edges = {tuple(e) for e in graph["edges"]}
    vertices = set(graph["vertices"])
    if certificate.get("model") != "K5":
        raise ValueError("certificate must be a K5 model")
    branches = certificate.get("branch_sets", [])
    trees = certificate.get("branch_trees", [])
    if len(branches) != 5 or len(trees) != 5:
        raise ValueError("five branch sets and trees are required")
    used = set()
    sets = []
    for branch, tree in zip(branches, trees):
        if not branch or any(type(v) is not int for v in branch) or len(set(branch)) != len(branch):
            raise ValueError("branch sets must be nonempty with no duplicate vertices")
        current = set(branch)
        if not current <= vertices or current & used:
            raise ValueError("branch sets must be declared and pairwise disjoint")
        used.update(current)
        sets.append(current)
        if len(tree) != len(current) - 1:
            raise ValueError("a branch tree must have |branch|-1 edges")
        local = {v: set() for v in current}
        for u, v in tree:
            if type(u) is not int or type(v) is not int or u not in current or v not in current or tuple(sorted((u, v))) not in edges:
                raise ValueError("branch tree edges must be actual internal source edges")
            local[u].add(v)
            local[v].add(u)
        reached, stack = {branch[0]}, [branch[0]]
        while stack:
            for v in local[stack.pop()] - reached:
                reached.add(v)
                stack.append(v)
        if reached != current:
            raise ValueError("each branch set must be connected")
    k4 = certificate.get("k4", [])
    if any(type(v) is not int for v in k4) or k4 != [branch[0] for branch in branches[:4]] or any(
            len(branch) != 1 for branch in branches[:4]):
        raise ValueError("the four K4 branches must be the named singleton vertices")
    pairs = set()
    for link in certificate.get("links", []):
        pair = tuple(link["branches"])
        if any(type(i) is not int for i in pair) or pair not in set(combinations(range(5), 2)) or pair in pairs:
            raise ValueError("each distinct K5 branch pair must appear once")
        pairs.add(pair)
        u, v = link["edge"]
        if type(u) is not int or type(v) is not int or u not in sets[pair[0]] or v not in sets[pair[1]]:
            raise ValueError("link endpoints must belong to their named branches")
        if tuple(sorted((u, v))) not in edges:
            raise ValueError("every branch link must be an actual source edge")
    if pairs != set(combinations(range(5), 2)):
        raise ValueError("all ten K5 branch links are required")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path, help="JSON graph, or a saved detector result")
    parser.add_argument("--check", action="store_true", help="check saved positive certificate only")
    parser.add_argument("--output", type=Path, help="exclusively create a result JSON")
    args = parser.parse_args()
    data = json.loads(args.graph.read_text())
    if args.check:
        if not data.get("detected") or not data.get("certificate"):
            parser.error("--check needs a saved positive certificate; a miss does not prove planarity")
        verify_certificate(data["graph"], data["certificate"])
        print("K5 minor certificate PASS (original edges, no planarity oracle)")
        return
    graph = normalize(data.get("graph", data))
    result = {"schema": 1, "graph": graph, **detect(graph)}
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(encoded)
        print(f"{result['status']}: {args.output}")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
