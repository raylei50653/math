#!/usr/bin/env python3
"""Finite calibration for the conditional deep degree-five wheel theorem.

This does not enumerate hypothetical outside-catalogue sources.  All writes are
exclusive; --check reconstructs and compares the entire certificate read-only.
Only the Python standard library is required.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools as it
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
COLORS = range(4)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()


def normalize(p):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in p)


def edge(a, b):
    return tuple(sorted((a, b)))


def fixture():
    # Two named pentagons, their triangulated annulus, and the deep hub 10.
    # The exterior apex 11 is used only to certify the spherical embedding.
    faces = []
    for i in range(5):
        j, h = (i + 1) % 5, (i - 1) % 5
        faces += [(i, j, 5 + i), (i, 5 + i, 5 + h),
                  (5 + i, 5 + j, 10), (j, i, 11)]
    all_edges = sorted({edge(a, b) for f in faces
                        for a, b in zip(f, f[1:] + f[:1])})
    disk_edges = [e for e in all_edges if 11 not in e]
    return faces, all_edges, disk_edges


def certify_embedding(faces, edges):
    directed = Counter((a, b) for f in faces
                       for a, b in zip(f, f[1:] + f[:1]))
    require(len(directed) == 2 * len(edges), "all directed edges present")
    require(all(directed[a, b] == directed[b, a] == 1 for a, b in edges),
            "each edge has two oppositely oriented incident triangles")
    rotations = {}
    for v in range(12):
        successor = {}
        for f in faces:
            if v in f:
                i = f.index(v)
                require(f[(i - 1) % 3] not in successor, "unique local successor")
                successor[f[(i - 1) % 3]] = f[(i + 1) % 3]
        start = min(successor)
        cycle, x = [], start
        while x not in cycle:
            cycle.append(x)
            x = successor[x]
        require(x == start and len(cycle) == len(successor), "vertex link is one circle")
        rotations[str(v)] = cycle
    require(12 - len(edges) + len(faces) == 2, "sphere Euler characteristic")
    # Explicit connectedness, together with the oriented manifold checks and
    # Euler characteristic two, certifies a sphere. Removing apex gives a disk.
    seen, todo = {0}, [0]
    while todo:
        v = todo.pop()
        for a, b in edges:
            if v in (a, b):
                w = b if v == a else a
                if w not in seen:
                    seen.add(w)
                    todo.append(w)
    require(len(seen) == 12, "connected sphere")
    return rotations


def simple_cycles(edges, bound=5):
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    found = set()
    def walk(path):
        if len(path) >= 3 and path[0] in adj[path[-1]]:
            p = tuple(path)
            found.add(min(p, (p[0],) + tuple(reversed(p[1:]))))
        if len(path) < bound:
            for w in sorted(adj[path[-1]]):
                if w > path[0] and w not in path:
                    walk(path + [w])
    for v in sorted(adj):
        walk([v])
    return sorted(found, key=lambda c: (len(c), c))


def cycle_sides(cycle, faces):
    barrier = {edge(a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1])}
    incidence = defaultdict(list)
    for i, f in enumerate(faces):
        for a, b in zip(f, f[1:] + f[:1]):
            incidence[edge(a, b)].append(i)
    dual = defaultdict(set)
    for e, (a, b) in incidence.items():
        if e not in barrier:
            dual[a].add(b)
            dual[b].add(a)
    remaining, sides = set(range(len(faces))), []
    while remaining:
        stack = [min(remaining)]
        group = set(stack)
        remaining.difference_update(group)
        while stack:
            f = stack.pop()
            for g in dual[f] & remaining:
                remaining.remove(g)
                group.add(g)
                stack.append(g)
        sides.append(sorted(set().union(*(set(faces[i]) for i in group)) - set(cycle)))
    require(len(sides) == 2, "Jordan cycle has exactly two face regions")
    return sorted(sides)


def brute_lifts(edges, boundary):
    return [list(z) for z in it.product(COLORS, repeat=6)
            if all((boundary + z)[a] != (boundary + z)[b] for a, b in edges)]


def mrv_lifts(edges, boundary, seed):
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    assignment = dict(enumerate(boundary))
    result, rng = [], random.Random(seed)
    def visit():
        pending = [v for v in range(5, 11) if v not in assignment]
        if not pending:
            result.append([assignment[v] for v in range(5, 11)])
            return
        rng.shuffle(pending)
        domains = {v: [c for c in COLORS if all(assignment.get(w) != c for w in adj[v])]
                   for v in pending}
        v = min(pending, key=lambda w: (len(domains[w]), -len(adj[w])))
        rng.shuffle(domains[v])
        for c in domains[v]:
            assignment[v] = c
            visit()
            del assignment[v]
    visit()
    return sorted(result)


def build(seed):
    manifest = json.loads((ROOT / "INPUTS.json").read_text())
    for record in manifest["inputs"]:
        require(hashlib.sha256((ROOT / record["frozen"]).read_bytes()).hexdigest()
                == record["sha256"], "frozen input drift")
    faces, sphere_edges, disk_edges = fixture()
    rotations = certify_embedding(faces, sphere_edges)
    adj = {v: set() for v in range(11)}
    for a, b in disk_edges:
        adj[a].add(b)
        adj[b].add(a)
    boundary = set(range(5))
    contacts = {str(v): sorted(adj[v] & boundary) for v in range(5, 11)}
    layer = [v for v in range(5, 11) if contacts[str(v)]]
    deep_five = [v for v in range(5, 11) if not contacts[str(v)] and len(adj[v]) == 5]
    db = sum(len(adj[b]) for b in boundary)
    excess = sum(max(len(adj[v]) - 6, 0) for v in range(5, 11))
    layer_high = [v for v in layer if len(adj[v]) >= 6]
    doubles = [v for v in layer if len(contacts[str(v)]) == 2]
    require(len(doubles) == 5 and len(layer) == db - 15, "boundary layer identity")
    require(len(deep_five) == 1 + excess + len(layer_high), "deep five exact identity")
    require(deep_five == [10], "named full-interior wheel control")
    cycle_records = []
    for c in simple_cycles(sphere_edges):
        sides = cycle_sides(c, faces)
        require(min(map(len, sides)) <= (1 if len(c) == 5 else 0),
                "sphere short-cycle property")
        cap = None
        if 11 not in c:
            cap = next(s for s in sides if 11 not in s)
            if set(c) != boundary:
                require(len(cap) <= (1 if len(c) == 5 else 0), "proper disk short-cycle cap")
        cycle_records.append({"cycle": list(c), "sides": sides, "disk_cap": cap})
    rows, mask = [], 0
    patterns = sorted({normalize(p) for p in it.product(COLORS, repeat=5)
                       if all(p[i] != p[(i + 1) % 5] for i in range(5))})
    for p in it.product(COLORS, repeat=5):
        if not all(p[i] != p[(i + 1) % 5] for i in range(5)):
            continue
        lifts = brute_lifts(disk_edges, p)
        require(lifts == mrv_lifts(disk_edges, p, seed), "independent complete fibre comparison")
        if lifts:
            mask |= 1 << patterns.index(normalize(p))
        rows.append({"boundary": list(p), "interior_order": list(range(5, 11)), "full_lifts": lifts})
    catalogue = json.loads((ROOT / "frozen/02-cells.json").read_text())
    require(patterns == list(map(tuple, catalogue["pattern_order"])), "catalogue frame order")
    cells = catalogue["cells"]
    require(str(mask) in cells, "positive control stays in catalogue")
    c4 = [{"t": t, "required_eII": 2*t-1, "simple_upper": t*(t-1)//2}
          for t in range(1, 4)]
    c5 = [{"t": t, "required_eII": 2*t-2, "outerplane_upper": 2*t-3}
          for t in range(2, 6)]
    require(all(r["required_eII"] > r["simple_upper"] for r in c4), "C4 arithmetic")
    require(all(r["required_eII"] > r["outerplane_upper"] for r in c5), "C5 arithmetic")
    return {"schema": 1, "base": manifest["base"], "frozen_inputs": manifest["inputs"],
            "arithmetic": {"C4": c4, "C5": c5},
            "control": {"name": "punctured_icosahedron", "status": "triggered and holds",
                        "outside_catalogue_status": "not triggered", "k": 6,
                        "edges": disk_edges, "sphere_faces": faces, "rotation": rotations,
                        "degree": {str(v): len(adj[v]) for v in adj}, "B_contacts": contacts,
                        "D_B": db, "layer": layer, "double_contacts": doubles,
                        "excess_ge7": excess, "layer_degree_ge6": layer_high,
                        "deep_degree5": deep_five, "sigma": mask,
                        "pattern_order": patterns, "fibres": rows, "short_cycles": cycle_records},
            "claim_scope": "Finite calibration only; the universal implication is proved in REPORT.md.",
            "lean": "not formalized"}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path)
    mode.add_argument("--check", type=Path)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    data = encode(build(args.seed))
    if args.write:
        with args.write.open("xb") as f:
            f.write(data)
    else:
        require(args.check.read_bytes() == data, "certificate differs from exact reconstruction")
    cert = json.loads(data)
    print(json.dumps({"status": "PASS", "sigma": cert["control"]["sigma"],
                      "full_boundary_fibres": len(cert["control"]["fibres"]),
                      "short_cycles": len(cert["control"]["short_cycles"]),
                      "deep_degree5": cert["control"]["deep_degree5"],
                      "sha256": hashlib.sha256(data).hexdigest()}))


if __name__ == "__main__":
    main()
