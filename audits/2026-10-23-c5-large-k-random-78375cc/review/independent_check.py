#!/usr/bin/env python3
"""Independently verify sampled C5 triangulated disks and their exact Sigma.

No imports from the sampler, SAT library, or NetworkX are used.  A combinatorial
2-manifold disk check validates the supplied oriented triangular faces.  A
finite-domain backtracker independently decides all ten fixed boundary rows.
Node limits produce UNRESOLVED, never an UNSAT claim.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
import time


PATTERNS = ("01012", "01021", "01023", "01201", "01202", "01203",
            "01212", "01213", "01231", "01232")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value):
    return type(value) is int


def edge(u, v):
    return (min(u, v), max(u, v))


def connected(vertices, adjacency):
    if not vertices:
        return False
    found = {next(iter(vertices))}
    stack = list(found)
    while stack:
        for v in adjacency[stack.pop()]:
            if v not in found:
                found.add(v)
                stack.append(v)
    return found == set(vertices)


def check_disk(sample):
    n = sample["n"]
    require(integer(n) and n >= 5, "n must be an integer at least five")
    require(integer(sample["k"]) and sample["k"] == n - 5, "k != n - 5")
    vertices = set(range(n))
    boundary = sample["boundary"]
    require(isinstance(boundary, list) and len(boundary) == 5
            and all(integer(v) for v in boundary)
            and len(set(boundary)) == 5 and set(boundary) <= vertices,
            "boundary must have five distinct vertex IDs in range(n)")
    rim = {edge(boundary[i], boundary[(i + 1) % 5]) for i in range(5)}
    raw_edges = sample["edges"]
    require(isinstance(raw_edges, list), "edges must be a list")
    edges = set()
    adjacent = [set() for _ in range(n)]
    for pair in raw_edges:
        require(isinstance(pair, list) and len(pair) == 2
                and all(integer(v) and v in vertices for v in pair)
                and pair[0] != pair[1], "invalid edge")
        u, v = pair
        e = edge(u, v)
        require(e not in edges, "duplicate undirected edge")
        edges.add(e)
        adjacent[u].add(v)
        adjacent[v].add(u)
    require(rim <= edges, "missing boundary edge")
    require(connected(vertices, adjacent), "graph is disconnected")
    require(len(edges) == 3 * n - 8, "wrong edge count for C5 near triangulation")
    faces = sample["faces"]
    require(isinstance(faces, list), "faces must be a list")
    require(len(faces) == 2 * n - 7, "wrong number of triangular disk faces")
    directed = Counter()
    seen_faces = set()
    links = [defaultdict(set) for _ in range(n)]
    link_edges = [set() for _ in range(n)]
    for face in faces:
        require(isinstance(face, list) and len(face) == 3
                and all(integer(v) and v in vertices for v in face)
                and len(set(face)) == 3, "invalid triangular face")
        canonical = tuple(sorted(face))
        require(canonical not in seen_faces, "duplicate triangular face")
        seen_faces.add(canonical)
        for i in range(3):
            u, v, w = face[i], face[(i + 1) % 3], face[(i + 2) % 3]
            directed[u, v] += 1
            require(edge(v, w) not in link_edges[u], "repeated edge in vertex link")
            link_edges[u].add(edge(v, w))
            links[u][v].add(w)
            links[u][w].add(v)
    require({edge(u, v) for u, v in directed} == edges,
            "declared edges differ from face edges")
    for u, v in edges:
        if (u, v) in rim:
            require(directed[u, v] + directed[v, u] == 1,
                    "boundary edge must meet exactly one triangular face")
        else:
            require(directed[u, v] == directed[v, u] == 1,
                    "internal edge must meet two oppositely oriented faces")
    orientations = [directed[boundary[i], boundary[(i + 1) % 5]] for i in range(5)]
    require(len(set(orientations)) == 1, "inconsistent boundary orientation")
    require(n - len(edges) + len(faces) == 1, "disk Euler characteristic failed")
    boundary_position = {v: i for i, v in enumerate(boundary)}
    for v in range(n):
        link = links[v]
        require(set(link) == adjacent[v] and connected(adjacent[v], link),
                f"vertex {v} has disconnected/incomplete link")
        if v in boundary_position:
            pos = boundary_position[v]
            endpoints = {boundary[(pos - 1) % 5], boundary[(pos + 1) % 5]}
            require(all(len(link[w]) == (1 if w in endpoints else 2) for w in link),
                    f"boundary vertex {v} link is not the required path")
        else:
            require(all(len(link[w]) == 2 for w in link),
                    f"interior vertex {v} link is not a cycle")
    return adjacent


class NodeLimit(Exception):
    pass


def solve_row(adjacent, boundary, word, max_nodes=None):
    """Decide one pinned row by singleton propagation and MRV search.

    A domain is a four-bit color set; trail restores every changed domain.
    Each failed search branch exhausts every remaining color, so returning None
    means exact non-extension.  The separate NodeLimit exception is inconclusive.
    """
    n = len(adjacent)
    domains = [15] * n
    trail = []
    nodes = 0

    def set_domain(v, mask):
        if domains[v] != mask:
            trail.append((v, domains[v]))
            domains[v] = mask

    def restore(mark):
        while len(trail) > mark:
            v, mask = trail.pop()
            domains[v] = mask

    def propagate(queue):
        while queue:
            v = queue.pop()
            singleton = domains[v]
            for w in adjacent[v]:
                if domains[w] & singleton:
                    reduced = domains[w] & ~singleton
                    if not reduced:
                        return False
                    set_domain(w, reduced)
                    if reduced & (reduced - 1) == 0:
                        queue.append(w)
        return True

    for v, color in zip(boundary, map(int, word)):
        set_domain(v, 1 << color)
    if not propagate(list(boundary)):
        return None, nodes

    def search():
        nonlocal nodes
        nodes += 1
        if max_nodes is not None and nodes > max_nodes:
            raise NodeLimit()
        choices = [v for v in range(n) if domains[v] & (domains[v] - 1)]
        if not choices:
            return [mask.bit_length() - 1 for mask in domains]
        v = min(choices, key=lambda w: (domains[w].bit_count(),
                -sum(bool(domains[z] & (domains[z] - 1)) for z in adjacent[w]),
                -len(adjacent[w]), w))
        mask = domains[v]
        colors = [1 << c for c in range(4) if mask & (1 << c)]
        colors.sort(key=lambda bit: (sum(bool(domains[w] & bit)
                                        for w in adjacent[v]), bit))
        for bit in colors:
            mark = len(trail)
            set_domain(v, bit)
            if propagate([v]):
                result = search()
                if result is not None:
                    return result
            restore(mark)
        return None

    try:
        result = search()
    except NodeLimit:
        return "UNRESOLVED", nodes
    return result, nodes


def check_witness(colors, n, boundary, word, edges):
    require(isinstance(colors, list) and len(colors) == n
            and all(integer(c) and 0 <= c < 4 for c in colors),
            "witness must give a color 0..3 at every vertex")
    require("".join(str(colors[v]) for v in boundary) == word,
            "witness does not use the literal pinned boundary colors")
    require(all(colors[u] != colors[v] for u, v in edges),
            "witness has a monochromatic edge")


def check_sample(sample, keys, max_nodes=None):
    adjacent = check_disk(sample)
    require(integer(sample["sigma"]) and 0 <= sample["sigma"] < 1024,
            "invalid sigma integer")
    require(sample["rows"] == list(PATTERNS), "rows must preserve all ten fixed patterns")
    witnesses = sample["witnesses"]
    require(isinstance(witnesses, list) and len(witnesses) == 10,
            "witnesses must have exactly ten entries")
    exact_mask = 0
    unresolved = []
    nodes = []
    for i, word in enumerate(PATTERNS):
        accepted = bool(sample["sigma"] & (1 << i))
        if accepted:
            check_witness(witnesses[i], sample["n"], sample["boundary"], word, sample["edges"])
        else:
            require(witnesses[i] is None, "rejected row has a supplied witness")
        result, count = solve_row(adjacent, sample["boundary"], word, max_nodes)
        nodes.append(count)
        if result == "UNRESOLVED":
            unresolved.append(word)
            continue
        if result is not None:
            check_witness(result, sample["n"], sample["boundary"], word, sample["edges"])
            exact_mask |= 1 << i
        require((result is not None) == accepted,
                f"independent exact solver disagrees on row {word}")
    return {"status": "UNRESOLVED" if unresolved else "VERIFIED",
            "k": sample["k"], "sigma": sample["sigma"],
            "catalogue_member": sample["sigma"] in keys,
            "exact_sigma": exact_mask if not unresolved else None,
            "unresolved_rows": unresolved, "nodes_by_row": nodes}


def root_directory():
    # This review directory is audit_root/review beneath the repository.
    return Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples", type=Path)
    parser.add_argument("--catalogue", type=Path,
                        default=root_directory() / "artifacts/c5_cells/cells.json")
    parser.add_argument("--max-nodes", type=int, default=None,
                        help="optional per-row cap; exceeded rows remain UNRESOLVED")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--stride", type=int, default=1)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    require(args.max_nodes is None or args.max_nodes > 0, "max-nodes must be positive")
    require(args.stride > 0 and 0 <= args.offset < args.stride, "invalid stride/offset")
    catalogue_bytes = args.catalogue.read_bytes()
    catalogue = json.loads(catalogue_bytes)
    require(catalogue["pattern_order"] == [list(map(int, p)) for p in PATTERNS],
            "catalogue has a different fixed row order")
    keys = {int(key) for key in catalogue["cells"]}
    require(len(keys) == 132, "catalogue does not contain 132 keys")
    sample_bytes = args.samples.read_bytes()
    start = time.monotonic()
    results = []
    for line_index, line in enumerate(sample_bytes.splitlines()):
        if not line.strip() or line_index % args.stride != args.offset:
            continue
        if args.limit is not None and len(results) >= args.limit:
            break
        try:
            sample = json.loads(line)
            result = check_sample(sample, keys, args.max_nodes)
        except (ValueError, KeyError, TypeError, IndexError) as exc:
            result = {"status": "FAILED", "error": str(exc)}
        result["line"] = line_index + 1
        results.append(result)
    counts = Counter(r["status"] for r in results)
    report = {"schema": "c5-large-k-independent-review-v1",
              "samples_sha256": sha256(sample_bytes).hexdigest(),
              "catalogue_sha256": sha256(catalogue_bytes).hexdigest(),
              "review_source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "sample_count": len(results), "status_counts": dict(sorted(counts.items())),
              "catalogue_outside_verified": [r["line"] for r in results
                    if r["status"] == "VERIFIED" and not r["catalogue_member"]],
              "seconds": round(time.monotonic() - start, 6),
              "selection": {"stride": args.stride, "offset": args.offset, "limit": args.limit},
              "max_nodes_per_row": args.max_nodes, "results": results}
    if args.output:
        with args.output.open("x") as handle:
            json.dump(report, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, sort_keys=True))
    return 1 if counts["FAILED"] else (2 if counts["UNRESOLVED"] else 0)


if __name__ == "__main__":
    sys.exit(main())
