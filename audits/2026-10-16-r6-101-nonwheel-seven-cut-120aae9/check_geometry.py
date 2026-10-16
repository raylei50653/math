#!/usr/bin/env python3
"""Finite synthetic heptagonal-disk calibration; no source-realization claim."""
import argparse
from collections import defaultdict
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random


BOUNDARY = ("u", "d1", "d2", "v", "c1", "b2", "b1")
INTERIOR = ("A", "B", "C", "D")
FACES = (
    ("A", "B", "C"), ("A", "C", "v"), ("A", "v", "D"),
    ("A", "D", "u"), ("A", "u", "B"), ("D", "u", "d1"),
    ("D", "d1", "d2"), ("D", "d2", "v"), ("B", "u", "b1"),
    ("B", "b1", "b2"), ("B", "b2", "C"), ("C", "b2", "c1"),
    ("C", "c1", "v"),
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def connected(vertices, adjacency):
    if not vertices:
        return True
    seen = {min(vertices)}
    todo = list(seen)
    while todo:
        new = adjacency[todo.pop()] & set(vertices) - seen
        seen |= new
        todo.extend(new)
    return seen == set(vertices)


def oriented_direction(face, a, b):
    return any(face[i] == a and face[(i + 1) % 3] == b for i in range(3))


def build(seed=None):
    rng = random.Random(seed)
    vertices = sorted(set(BOUNDARY) | set(INTERIOR))
    incidence = defaultdict(list)
    for i, face in enumerate(FACES):
        require(len(set(face)) == 3, "degenerate input face")
        for a, b in combinations(face, 2):
            incidence[edge(a, b)].append(i)
    edges = set(incidence)
    boundary_edges = {edge(BOUNDARY[i], BOUNDARY[(i + 1) % 7]) for i in range(7)}
    require({e for e, fs in incidence.items() if len(fs) == 1} == boundary_edges,
            "wrong literal heptagonal boundary")
    require(all(len(fs) == (1 if e in boundary_edges else 2)
                for e, fs in incidence.items()), "nonmanifold edge incidence")
    require(len(vertices) - len(edges) + len(FACES) == 1, "disk Euler identity")
    adj = {v: set() for v in vertices}
    dual_adj = {i: set() for i in range(len(FACES))}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for fs in incidence.values():
        if len(fs) == 2:
            a, b = fs
            dual_adj[a].add(b)
            dual_adj[b].add(a)
    require(connected(set(vertices), adj), "disconnected patch")
    require(connected(set(dual_adj), dual_adj), "disconnected face disk")

    # Check an orientation of every face, not only Euler's equation.
    oriented = {0: FACES[0]}
    todo = [0]
    while todo:
        i = todo.pop()
        face = oriented[i]
        for a, b in combinations(face, 2):
            for j in incidence[edge(a, b)]:
                if j == i:
                    continue
                proposed = FACES[j]
                if oriented_direction(proposed, a, b) == oriented_direction(face, a, b):
                    proposed = tuple(reversed(proposed))
                if j in oriented:
                    require(oriented_direction(oriented[j], a, b)
                            != oriented_direction(face, a, b), "orientation conflict")
                else:
                    oriented[j] = proposed
                    todo.append(j)
    require(len(oriented) == len(FACES), "incomplete orientation")

    links = {}
    for v in vertices:
        link_edges = sorted(edge(*[u for u in f if u != v]) for f in FACES if v in f)
        link_adj = {u: set() for u in adj[v]}
        for a, b in link_edges:
            link_adj[a].add(b)
            link_adj[b].add(a)
        require(connected(adj[v], link_adj), "disconnected vertex link")
        degrees = sorted(map(len, link_adj.values()))
        expected = [2] * len(adj[v]) if v in INTERIOR else [1, 1] + [2] * (len(adj[v]) - 2)
        require(degrees == sorted(expected), "vertex link is not a cycle/path")
        links[v] = dict(neighbours=sorted(adj[v]), link_edges=link_edges,
                        link_type="cycle" if v in INTERIOR else "path")
    require(all(len(adj[v]) == 5 for v in INTERIOR), "interior degree drift")
    require({e for e in edges if set(e) <= set(BOUNDARY)} == boundary_edges,
            "interior boundary chord")
    triangles = {frozenset(t) for t in combinations(vertices, 3)
                 if all(edge(a, b) in edges for a, b in combinations(t, 2))}
    require(triangles == set(map(frozenset, FACES)), "nonfacial triangle")

    def induced_cycles(length):
        found = set()
        def visit(path):
            if len(path) == length:
                if path[0] in adj[path[-1]]:
                    cycle_edges = {edge(path[i], path[(i + 1) % length]) for i in range(length)}
                    if {e for e in edges if set(e) <= set(path)} == cycle_edges:
                        found.add(min(tuple(path), tuple([path[0]] + path[:0:-1])))
                return
            candidates = sorted(adj[path[-1]])
            rng.shuffle(candidates)
            for u in candidates:
                if u > path[0] and u not in path:
                    visit(path + [u])
        starts = list(vertices)
        rng.shuffle(starts)
        for v in starts:
            visit([v])
        return sorted(found)

    c4 = induced_cycles(4)
    require(not c4, "unexpected induced C4")
    c5 = induced_cycles(5)
    caps = []
    for cycle in c5:
        centres = [v for v in INTERIOR if adj[v] == set(cycle)]
        require(len(centres) == 1, "induced C5 lacks one complete interior W5")
        centre = centres[0]
        face_ids = [i for i, f in enumerate(FACES) if centre in f]
        cap_boundary = {e for e, fs in incidence.items()
                        if sum(i in face_ids for i in fs) == 1}
        require(cap_boundary == {edge(cycle[i], cycle[(i + 1) % 5]) for i in range(5)},
                "wheel cap boundary mismatch")
        caps.append(dict(cycle=cycle, complete_degree_five_centre=centre, faces=face_ids))
    require(len(caps) == 4, "induced pentagon count drift")

    @lru_cache(None)
    def matchings(free):
        if not free:
            return ((),)
        u = min(free)
        candidates = sorted(dual_adj[u] & free)
        rng.shuffle(candidates)
        out = []
        for v in candidates:
            for sub in matchings(free - {u, v}):
                out.append(tuple(sorted((edge(u, v),) + sub)))
        return tuple(sorted(out))

    deletions = {}
    for u in sorted(dual_adj):
        full = matchings(frozenset(set(dual_adj) - {u}))
        require(full, "dual is not factor-critical")
        require(len(full) == len(set(full)), "duplicate matching lift")
        for matching in full:
            flat = [v for e in matching for v in e]
            require(sorted(flat) == sorted(set(dual_adj) - {u}), "bad full matching lift")
        deletions[str(u)] = list(full)
    ports = [dict(boundary_edge=edge(BOUNDARY[i], BOUNDARY[(i + 1) % 7]),
                  inside_dual_vertex=incidence[edge(BOUNDARY[i], BOUNDARY[(i + 1) % 7])][0])
             for i in range(7)]
    require(len({p["inside_dual_vertex"] for p in ports}) == 7, "port collision")
    require(sorted(map(len, dual_adj.values())) == [2] * 7 + [3] * 6, "dual degree drift")
    inward = [len(adj[v] & set(INTERIOR)) for v in BOUNDARY]
    require(inward == [3, 1, 1, 3, 1, 2, 1], "inward degree drift")
    internal_edges = sorted(e for e in edges if set(e) <= set(INTERIOR))
    require(len(internal_edges) == 4, "interior graph edge drift")
    literal_input = dict(boundary=BOUNDARY, interior=INTERIOR, faces=FACES)
    return dict(
        schema=1,
        domain=dict(kind="one explicit synthetic local disk", original_source_realization=False,
                    original_source_tests="not triggered", arbitrary_size_proof="paper only",
                    six_pin_or_source_completion_claim=False),
        input_sha256=hashlib.sha256(canonical_bytes(literal_input)).hexdigest(),
        input=literal_input,
        primal=dict(vertices=vertices, edges=sorted(edges), links=links,
                    orientable_disk=True, euler_characteristic=1,
                    all_triangles_facial=True, interior_edges=internal_edges,
                    inward_degree_boundary_order=inward, induced_C4=c4,
                    induced_C5_complete_caps=caps),
        dual=dict(vertices=sorted(dual_adj), edges=sorted(edge(i, j) for i in dual_adj
                                                        for j in dual_adj[i] if i < j),
                  ports_boundary_order=ports, factor_critical=True,
                  every_deletion_full_matching_fibre=deletions),
        curvature_calibration=dict(Iodd=4, Bodd=6, epsilon=0,
                                   weighted_Q_formal=12, excess_formal=0,
                                   source_realization_inferred=False),
    )


def strict_load(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            require(k not in out, "duplicate JSON key")
            out[k] = v
        return out
    def constant(value):
        raise ValueError("non-finite JSON number: " + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", type=Path)
    group.add_argument("--check", type=Path)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    expected = build(args.seed)
    raw = canonical_bytes(expected)
    if args.write:
        with args.write.open("xb") as target:
            target.write(raw)
    if args.check:
        supplied = args.check.read_bytes()
        strict_load(supplied)
        require(supplied == raw, "certificate mismatch (including source-domain promotion)")
    print(json.dumps(dict(status="PASS", source_realization="not triggered",
                          certificate_sha256=hashlib.sha256(raw).hexdigest(),
                          primal_vertices=11, disk_faces=13, ports=7,
                          induced_C4=0, induced_C5=4,
                          full_deletion_matching_lifts=sum(len(v) for v in expected["dual"]
                                                          ["every_deletion_full_matching_fibre"].values())),
                     sort_keys=True))


if __name__ == "__main__":
    main()
