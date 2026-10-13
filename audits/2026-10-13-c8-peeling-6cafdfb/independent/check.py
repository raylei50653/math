#!/usr/bin/env python3
"""Independent original-graph, cap, face-walk, and complete-lift controls.

Only Python's standard library; no import from the primary implementation.
The fixtures meet local geometric premises, not the complete 933/941 source.
"""
from collections import defaultdict, deque
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import gzip
import json

ROOT = Path(__file__).resolve().parent
COLORS = range(4)
C = tuple(f"c{i}" for i in range(8))
T = tuple(f"t{i}" for i in range(8))


def compare_expected(actual, expected):
    assert actual == expected, "complete original data mismatch"


def expect_rejection(actual, expected):
    try:
        compare_expected(actual, expected)
    except AssertionError:
        return
    raise AssertionError("corruption was accepted by the normal comparator")


def edge(a, b):
    return tuple(sorted((a, b)))


def fixture(name):
    faces = [(C[i], C[(i + 1) % 8], T[i]) for i in range(8)]
    if name in ("M10-FAN3", "M10-FAN4", "M10-CHORD4"):
        faces += [(C[i], T[(i - 1) % 8], T[i]) for i in range(8)]
        vertices = C + T + ("r", "s")
        if name == "M10-CHORD4":
            for center, rim in (("r", T[:5]), ("s", T[4:] + T[:1])):
                faces += [(center, rim[i], rim[(i + 1) % 5]) for i in range(5)]
        else:
            split = 3 if name == "M10-FAN3" else 4
            faces += [("r", T[i], T[i + 1]) for i in range(split)]
            faces += [("s", T[i], T[(i + 1) % 8]) for i in range(split, 8)]
            faces += [("r", "s", T[0]), ("r", "s", T[split])]
    elif name == "M11-WIDTH":
        vertices = C + T + ("z", "r", "s")
        faces += [(C[i], T[i - 1], T[i]) for i in range(1, 8)]
        faces += [(C[0], T[7], "z"), (C[0], "z", T[0])]
        rim = ("z",) + T
        faces += [("r", rim[i], rim[i + 1]) for i in range(4)]
        faces += [("s", rim[i], rim[(i + 1) % 9]) for i in range(4, 9)]
        faces += [("r", "s", rim[0]), ("r", "s", rim[4])]
    else:
        vertices = C + T + (("x",) if name == "M11-PINCH" else ("x", "y")) + ("rL", "rR")
        faces += [(C[i], T[i - 1], T[i]) for i in (1, 2, 3, 5, 6, 7)]
        if name == "M11-PINCH":
            faces += [(C[0], T[7], "x"), (C[0], "x", T[0]),
                      (C[4], T[3], "x"), (C[4], "x", T[4])]
            rims = (("rL", ("x",) + T[:4]), ("rR", ("x",) + T[4:]))
        elif name == "M12-BRIDGE":
            faces += [(C[0], T[7], "y"), (C[0], "y", "x"), (C[0], "x", T[0]),
                      (C[4], T[3], "x"), (C[4], "x", "y"), (C[4], "y", T[4])]
            rims = (("rL", ("x",) + T[:4]), ("rR", ("y",) + T[4:]))
        else:
            raise ValueError(name)
        for center, rim in rims:
            faces += [(center, rim[i], rim[(i + 1) % 5]) for i in range(5)]
    edges = sorted({edge(a, b) for f in faces for a, b in zip(f, f[1:] + f[:1])})
    return vertices, edges, faces


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def embedding(vertices, edges, faces):
    # Orient all triangle faces by propagation, then close with the outer C8.
    by_edge = defaultdict(list)
    for i, f in enumerate(faces):
        for a, b in zip(f, f[1:] + f[:1]):
            by_edge[edge(a, b)].append(i)
    outer_edges = {edge(C[i], C[(i + 1) % 8]) for i in range(8)}
    assert all(len(indices) == (1 if e in outer_edges else 2) for e, indices in by_edge.items())
    oriented = {0: tuple(faces[0])}
    queue = deque((0,))
    while queue:
        i = queue.popleft()
        f = oriented[i]
        for a, b in zip(f, f[1:] + f[:1]):
            for j in by_edge[edge(a, b)]:
                if j == i:
                    continue
                raw = tuple(faces[j])
                candidate = raw if (b, a) in tuple(zip(raw, raw[1:] + raw[:1])) else raw[::-1]
                if j in oriented:
                    assert set(zip(oriented[j], oriented[j][1:] + oriented[j][:1])) == set(zip(candidate, candidate[1:] + candidate[:1]))
                else:
                    oriented[j] = candidate
                    queue.append(j)
    assert len(oriented) == len(faces)
    oriented_faces = [oriented[i] for i in range(len(faces))] + [C[::-1]]
    successor = {v: {} for v in vertices}
    all_halfedges = set()
    for f in oriented_faces:
        for i, v in enumerate(f):
            a, b = f[i - 1], f[(i + 1) % len(f)]
            assert a not in successor[v]
            successor[v][a] = b
            all_halfedges.add((v, b))
    assert all_halfedges == {(a, b) for e in edges for a, b in (e, e[::-1])}
    rotation = {}
    adj = adjacency(vertices, edges)
    for v in vertices:
        neighbors = successor[v]
        start = min(neighbors)
        order = [start]
        while neighbors[order[-1]] != start:
            order.append(neighbors[order[-1]])
            assert len(order) <= len(neighbors)
        assert set(order) == adj[v]
        rotation[v] = tuple(order)
    assert len(vertices) - len(edges) + len(oriented_faces) == 2
    return rotation, oriented_faces


def components(vertices, adj):
    remaining = set(vertices)
    answer = []
    while remaining:
        start = min(remaining)
        found = {start}
        queue = [start]
        while queue:
            v = queue.pop()
            for w in adj[v] & remaining - found:
                found.add(w)
                queue.append(w)
        answer.append(found)
        remaining -= found
    return answer


def face_walks(vertices, rotation, adj):
    vertices = set(vertices)
    walks = []
    for comp in components(vertices, adj):
        if len(comp) == 1:
            walks.append([min(comp)])
            continue
        rot = {v: tuple(w for w in rotation[v] if w in comp) for v in comp}
        unseen = {(v, w) for v in comp for w in adj[v] & comp}
        local = []
        while unseen:
            start = min(unseen)
            current = start
            walk = []
            while True:
                assert current in unseen
                unseen.remove(current)
                a, b = current
                walk.append(a)
                order = rot[b]
                current = (b, order[(order.index(a) + 1) % len(order)])
                if current == start:
                    break
            local.append(walk)
        outer = max(local, key=len)
        assert all(len(w) == 3 for w in local if w is not outer)
        walks.append(outer)
    return walks


def small_cycles(vertices, adj, limit=5):
    answer = set()
    for start in vertices:
        def visit(path):
            for w in adj[path[-1]]:
                if w == start and len(path) >= 3:
                    cycle = tuple(path)
                    answer.add(min(cycle, (cycle[0],) + cycle[:0:-1]))
                elif w not in path and w > start and len(path) < limit:
                    visit(path + [w])
        visit([start])
    return sorted(answer)


def verify_caps(vertices, adj, oriented_faces):
    by_edge = defaultdict(list)
    for i, f in enumerate(oriented_faces):
        for a, b in zip(f, f[1:] + f[:1]):
            by_edge[edge(a, b)].append(i)
    counts = defaultdict(int)
    outer = len(oriented_faces) - 1
    for cycle in small_cycles(vertices, adj):
        barriers = {edge(a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1])}
        dual = defaultdict(set)
        for e, (a, b) in by_edge.items():
            if e not in barriers:
                dual[a].add(b)
                dual[b].add(a)
        found = {outer}
        queue = [outer]
        while queue:
            for j in dual[queue.pop()] - found:
                found.add(j)
                queue.append(j)
        inner_faces = set(range(len(oriented_faces))) - found
        assert inner_faces
        interior = set().union(*(set(oriented_faces[i]) for i in inner_faces)) - set(cycle)
        size = len(cycle)
        if size in (3, 4):
            assert not interior, (cycle, interior)
        else:
            assert len(interior) <= 1, (cycle, interior)
            if interior:
                center = next(iter(interior))
                assert adj[center] == set(cycle), (cycle, center, adj[center])
        counts[f"C{size}-{'empty' if not interior else 'W5'}"] += 1
    return dict(sorted(counts.items()))


def colorings(vertices, adj, pins):
    vertices = tuple(vertices)
    assign = dict(pins)
    if any(assign[a] == assign[b] for a in assign for b in adj[a] & assign.keys()):
        return []
    result = []
    def search():
        if len(assign) == len(vertices):
            result.append(tuple(assign[v] for v in vertices))
            return
        domains = {}
        for v in vertices:
            if v not in assign:
                forbidden = {assign[w] for w in adj[v] if w in assign}
                domains[v] = tuple(c for c in COLORS if c not in forbidden)
        v = min(domains, key=lambda x: (len(domains[x]), -len(adj[x]), x))
        for c in domains[v]:
            assign[v] = c
            search()
        assign.pop(v, None)
    search()
    return sorted(result)


def layer_transfer(vertices, adj, rotation, pins):
    """Set-valued recurrence; every returned tuple uses original vertex names."""
    vertices = tuple(vertices)
    exposed = set().union(*(set(w) for w in face_walks(vertices, rotation, adj))) if vertices else set()
    assert set(pins) == exposed
    if any(pins[a] == pins[b] for a in pins for b in adj[a] & pins.keys()):
        return []
    remaining = tuple(v for v in vertices if v not in exposed)
    if not remaining:
        return [tuple(pins[v] for v in vertices)]
    next_boundary = set().union(*(set(w) for w in face_walks(remaining, rotation, adj)))
    assert all((adj[v] & set(remaining)) <= next_boundary for v in exposed)
    # Cross-edge endpoint colors are imposed in the same literal frame.
    next_order = tuple(v for v in remaining if v in next_boundary)
    shell_order = tuple(v for v in vertices if v in exposed or v in next_boundary)
    shell = {v: adj[v] & set(shell_order) for v in shell_order}
    result = []
    for shell_tuple in colorings(shell_order, shell, pins):
        shell_assignment = dict(zip(shell_order, shell_tuple))
        beta = {v: shell_assignment[v] for v in next_order}
        for tail in layer_transfer(remaining, adj, rotation, beta):
            assignment = dict(pins)
            assignment.update(zip(remaining, tail))
            result.append(tuple(assignment[v] for v in vertices))
    assert len(result) == len(set(result))
    return sorted(result)


def canonical_words(n):
    answer = []
    def rec(word):
        if len(word) == n:
            if word[-1] != word[0]:
                answer.append(tuple(word))
            return
        for c in range(min(3, max(word) + 1) + 1):
            if c != word[-1]:
                rec(word + [c])
    rec([0])
    return answer


def block_negative():
    left = ("x", "a1", "a2", "a3")
    right = ("x", "b0", "b2", "b3")
    edges = [edge(a, b) for block in (left, right) for a, b in combinations(block, 2)]
    vertices = left + right[1:]
    adj = adjacency(vertices, edges)
    pins = {"a1": 1, "a2": 2, "a3": 3, "b0": 0, "b2": 2, "b3": 3}
    left_lifts = colorings(left, {v: adj[v] & set(left) for v in left}, {v: c for v, c in pins.items() if v in left})
    right_lifts = colorings(right, {v: adj[v] & set(right) for v in right}, {v: c for v, c in pins.items() if v in right})
    joint = colorings(vertices, adj, pins)
    assert len(left_lifts) == len(right_lifts) == 1 and not joint
    assert left_lifts[0][0] == 0 and right_lifts[0][0] == 1
    return {"name": "OB-SIBLING-MARGINAL", "left_full_lifts": left_lifts,
            "right_full_lifts": right_lifts, "original_joint_count": len(joint),
            "incorrect_independent_nonempty_product": 1,
            "status": "synthetic counterexample to a weakened join"}


def repeated_negative():
    left = ("x",) + T[:4] + ("rL",)
    right = ("x",) + T[4:] + ("rR",)
    vertices, edges, _ = fixture("M11-PINCH")
    adj = adjacency(vertices, edges)
    left_pins = dict(zip(left[:-1], (0, 1, 2, 1, 2)))
    right_pins = dict(zip(right[:-1], (1, 0, 2, 0, 2)))
    lifts_left = colorings(left, {v: adj[v] & set(left) for v in left}, left_pins)
    lifts_right = colorings(right, {v: adj[v] & set(right) for v in right}, right_pins)
    assert len(lifts_left) == len(lifts_right) == 1
    assert left_pins["x"] != right_pins["x"]
    return {"name": "OB-REPEATED-VERTEX-COLOR", "left_pins": left_pins,
            "right_pins": right_pins, "left_full_lifts": lifts_left,
            "right_full_lifts": lifts_right, "original_joint_count": 0,
            "incorrect_occurrence_copy_product": 1,
            "status": "counterexample to treating face-walk occurrences as different vertices"}


def run(full=True, write=False, negative=False):
    words = canonical_words(8)
    assert len(words) == 274
    records = []
    archive = {}
    for name in ("M10-FAN3", "M10-FAN4", "M10-CHORD4", "M11-PINCH", "M12-BRIDGE", "M11-WIDTH"):
        vertices, edges, raw_faces = fixture(name)
        adj = adjacency(vertices, edges)
        rotation, faces = embedding(vertices, edges, raw_faces)
        assert all(len(adj[v]) >= 4 for v in C)
        assert all(len(adj[v]) >= 5 for v in vertices if v not in C)
        assert {edge(a, b) for a in C for b in adj[a] & set(C)} == {edge(C[i], C[(i+1)%8]) for i in range(8)}
        assert all(len(adj[v] & set(C)) <= 2 for v in vertices if v not in C)
        cap_counts = verify_caps(vertices, adj, faces)
        inner = tuple(v for v in vertices if v not in C)
        walks = face_walks(inner, rotation, adj)
        exposed = set().union(*(set(w) for w in walks))
        assert exposed == {v for v in inner if adj[v] & set(C)}
        cuts = [v for v in inner if len(components(set(inner) - {v}, adj)) > 1]
        antipodal = [v for v in inner if len(adj[v] & set(C)) == 2 and all(edge(v, c) in edges for c in (C[0], C[4]))]
        assert set(cuts) == set(antipodal)
        second_contacts = {v: len(adj[v] & exposed) for v in inner if v not in exposed}
        fibers = []
        all_lifts = []
        for word in words if full else words[:10]:
            pins = dict(zip(C, word))
            direct = colorings(vertices, adj, pins)
            transferred = layer_transfer(vertices, adj, rotation, pins)
            assert direct == transferred, (name, word)
            compact = [list(lift[8:]) for lift in direct]
            digest = sha256(json.dumps(compact, separators=(",", ":")).encode()).hexdigest()
            fibers.append({"C_word": list(word), "count": len(direct), "full_lift_sha256": digest})
            all_lifts.append({"C_word": list(word), "interior_full_lifts": compact})
        archive[name] = {"interior_vertex_order": list(inner), "complete_fibres": all_lifts}
        records.append({"name": name, "vertices": list(vertices), "edges": [list(e) for e in edges],
                        "inner_faces": [list(f) for f in faces[:-1]], "rotations": rotation,
                        "degrees": {v: len(adj[v]) for v in vertices}, "cap_cycle_counts": cap_counts,
                        "Q_outer_walks": walks, "Q_cutvertices": cuts, "second_layer_contact_counts": second_contacts,
                        "complete_fibre_receipts": fibers,
                        "source_status": "local geometric control; complete 933/941 minimal source not triggered"})
    certificate = {"fixtures": records, "negative_controls": [repeated_negative(), block_negative()],
                   "method": "independent face rotation, dual cap separation, MRV direct search versus recursive original-vertex natural joins",
                   "literal_colors": [0, 1, 2, 3], "complete_C8_fibres_per_fixture": len(words) if full else 10}
    if write:
        ROOT.joinpath("certificate.json").write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
        with gzip.open(ROOT / "full_lifts.json.gz", "wt", encoding="utf-8") as out:
            json.dump(archive, out, separators=(",", ":"), sort_keys=True)
    elif full:
        saved = json.loads(ROOT.joinpath("certificate.json").read_text())
        # JSON turns tuples into arrays; compare through canonical JSON.
        compare_expected(json.loads(json.dumps(certificate)), saved)
        saved_lifts = json.load(gzip.open(ROOT / "full_lifts.json.gz", "rt"))
        compare_expected(archive, saved_lifts)
        if negative:
            damaged = json.loads(json.dumps(saved_lifts))
            first = next(f for f in damaged["M10-FAN3"]["complete_fibres"] if f["interior_full_lifts"])
            first["interior_full_lifts"].pop()
            expect_rejection(damaged, archive)
            damaged = json.loads(json.dumps(saved))
            pinch = next(f for f in damaged["fixtures"] if f["name"] == "M11-PINCH")
            walk = pinch["Q_outer_walks"][0]
            assert walk.count("x") == 2
            walk[walk.index("x")] = "x-copy"
            expect_rejection(damaged, json.loads(json.dumps(certificate)))
    print(json.dumps({"fixtures": len(records), "C8_fibres": sum(len(r["complete_fibre_receipts"]) for r in records),
                      "full_lifts": sum(sum(f["count"] for f in r["complete_fibre_receipts"]) for r in records),
                      "negative_controls": 2, "negative_corruptions_rejected": 2 if negative else 0,
                      "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    run(full=not args.quick, write=args.write, negative=args.negative)
