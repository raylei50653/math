#!/usr/bin/env python3
"""Audit every rotation of the saved eight-vertex reference join.

Standard library only. A separate companion certificate leaves the original
colouring artifact intact. --check recomputes and compares without writing.
The 36 rotations belong to one actual graph, not to all realizations of its Sigma.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/eight_point_joins.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/reference_topology.json"
PATHS = (
    ("a0", "a1", "a2"),
    ("a0", "a4", "a3", "a2"),
    ("a0", "a2"),
    ("a0", "b4", "b3", "b2", "a2"),
)


def edge(u, v):
    return tuple(sorted((u, v)))


def path_edges(path):
    return {edge(u, v) for u, v in zip(path, path[1:])}


def cycle_edges(cycle):
    return path_edges(tuple(cycle) + (cycle[0],))


def canonical_colours(row):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in row)


def reference():
    saved = json.loads((ROOT / SOURCE).read_text())
    for path, digest in saved["source_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    record, = (r for r in saved["cases"] if r["name"] == "reference")
    assert record["inputs"] == {
        "A": {"class_id": 1023, "source_cell_key": "1023", "pair": [0, 2]},
        "B": {"class_id": 1023, "source_cell_key": "1023", "pair": [0, 1]},
    }
    graph = record["graph"]
    vertices = tuple(graph["vertices"])
    assert vertices == tuple(record["joint"]["ports"])
    edges = {edge(vertices[u], vertices[v]) for u, v in graph["edges"]}
    assert len(vertices) == 8 and len(edges) == 10
    frames = {s: tuple(record["boundary_maps"][s]) for s in ("A", "B")}
    assert set(frames["A"]) & set(frames["B"]) == {"a0", "a2"}
    assert not cycle_edges(frames["A"]) & cycle_edges(frames["B"])
    assert edges == cycle_edges(frames["A"]) | cycle_edges(frames["B"])
    assert not graph["shared_edges"]
    for side in ("A", "B"):
        mapping = graph["source_vertex_maps"][side]
        assert mapping == list(frames[side])  # These representatives have no private vertices.
        actual = {edge(mapping[u], mapping[v])
                  for u, v in graph["source_edges_with_frames"][side]}
        assert actual == cycle_edges(frames[side])

    # An independent 4^8 edge-only replay binds the topology to the entire J.
    accepted = [row for row in product(range(4), repeat=8)
                if all(row[u] != row[v] for u, v in graph["edges"])]
    assert {canonical_colours(row) for row in accepted} == {
        tuple(row) for row in record["joint"]["patterns"]}
    assert len(accepted) == record["joint"]["labelled_assignments"] == 3360
    assert record["joint"]["global_s4_orbits"] == 140
    for side, frame in frames.items():
        indices = [vertices.index(v) for v in frame]
        projection = {canonical_colours(tuple(row[i] for i in indices)) for row in accepted}
        assert projection == {tuple(row) for row in record["projections"][side]["patterns"]}
    return record, vertices, edges, frames


def rotations(order_x, order_y):
    result = {"a0": tuple(PATHS[i][1] for i in order_x),
              "a2": tuple(PATHS[i][-2] for i in order_y)}
    for path in PATHS:
        for i in range(1, len(path) - 1):
            result[path[i]] = (path[i - 1], path[i + 1])
    return dict(sorted(result.items()))


def trace_faces(rotation, edges):
    """Face permutation: reverse a dart, then take its clockwise predecessor."""
    darts = {(u, v) for a, b in edges for u, v in ((a, b), (b, a))}
    assert {(u, v) for u, neighbours in rotation.items() for v in neighbours} == darts
    assert all(len(ns) == len(set(ns)) for ns in rotation.values())
    remaining, faces, dart_face = set(darts), [], {}
    while remaining:
        start = min(remaining)
        current, face = start, []
        while current in remaining:
            remaining.remove(current)
            dart_face[current] = len(faces)
            u, v = current
            face.append(u)
            neighbours = rotation[v]
            current = (v, neighbours[(neighbours.index(u) - 1) % len(neighbours)])
        assert current == start
        faces.append(tuple(face))
    assert len(dart_face) == 2 * len(edges)
    return faces, dart_face


def components(adjacency):
    remaining, result = set(adjacency), []
    while remaining:
        reached, todo = set(), [min(remaining)]
        while todo:
            v = todo.pop()
            if v not in reached:
                reached.add(v)
                todo.extend(adjacency[v] - reached)
        remaining -= reached
        result.append(reached)
    return result


def disk_sides(frame, edges, faces, dart_face, outer):
    """Cut the dual along the actual original cycle; infinity picks the outside."""
    boundary = cycle_edges(frame)
    dual = {i: set() for i in range(len(faces))}
    for u, v in edges - boundary:
        a, b = dart_face[u, v], dart_face[v, u]
        dual[a].add(b)
        dual[b].add(a)
    parts = components(dual)
    assert len(parts) == 2
    inside, = (part for part in parts if outer not in part)
    outside = set(range(len(faces))) - inside
    locations = {"inside": [], "outside": [], "boundary": sorted(boundary)}
    for u, v in sorted(edges - boundary):
        a, b = dart_face[u, v], dart_face[v, u]
        assert (a in inside) == (b in inside)
        locations["inside" if a in inside else "outside"].append((u, v))
    for u, v in boundary:
        assert (dart_face[u, v] in inside) != (dart_face[v, u] in inside)
    directed = zip(frame, frame[1:] + frame[:1])
    right_is_inside = {dart_face[u, v] in inside for u, v in directed}
    assert len(right_is_inside) == 1
    whole_graph_in_disk = not locations["outside"]
    assert whole_graph_in_disk == (cycle_edges(faces[outer]) == boundary)
    return {"inside_faces": sorted(inside), "outside_faces": sorted(outside),
            "bounded_side_of_directed_frame": "right" if right_is_inside == {True} else "left",
            "edge_locations": locations,
            "is_whole_graph_outer_boundary": whole_graph_in_disk}


def build():
    record, vertices, edges, frames = reference()
    sets = [path_edges(p) for p in PATHS]
    assert set().union(*sets) == edges and sum(map(len, sets)) == len(edges)
    assert all(set(p[1:-1]).isdisjoint(q[1:-1]) for p, q in combinations(PATHS, 2))
    assert sets[0] | sets[1] == cycle_edges(frames["A"])
    assert sets[2] | sets[3] == cycle_edges(frames["B"])
    orders = [(0,) + p for p in permutations((1, 2, 3))]
    records, histogram, type_counts = [], Counter(), Counter()
    outer_counts = Counter({"A": 0, "B": 0, "both": 0})
    witnesses = {}
    for order_x, order_y in product(orders, repeat=2):
        rotation = rotations(order_x, order_y)
        faces, dart_face = trace_faces(rotation, edges)
        euler = len(vertices) - len(edges) + len(faces)
        histogram[len(faces)] += 1
        planar = euler == 2
        # The paper construction realizes precisely opposite path orders.
        assert planar == (order_y == (order_x[0],) + tuple(reversed(order_x[1:])))
        row = {"id": len(records), "path_order_at_a0": order_x,
               "path_order_at_a2": order_y, "clockwise_rotations": rotation,
               "faces": faces, "euler_characteristic": euler,
               "sphere_rotation": planar, "plane_embeddings": []}
        if planar:
            assert len(faces) == 4 and all(len(f) == len(set(f)) for f in faces)
            face_path_pairs = []
            for face in faces:
                pairs = [pair for pair in combinations(range(4), 2)
                         if sets[pair[0]] | sets[pair[1]] == cycle_edges(face)]
                pair, = pairs
                face_path_pairs.append(pair)
            row["face_path_pairs"] = face_path_pairs
            alternating = all((order_x[i] < 2) != (order_x[(i + 1) % 4] < 2)
                              for i in range(4))
            row["original_cycles_alternate_at_shared_vertices"] = alternating
            for outer in range(4):
                disks = {side: disk_sides(frame, edges, faces, dart_face, outer)
                         for side, frame in frames.items()}
                a, b = (set(disks[s]["inside_faces"]) for s in ("A", "B"))
                if not a & b:
                    kind = "disjoint_interiors"
                elif b < a:
                    kind = "B_in_A"
                elif a < b:
                    kind = "A_in_B"
                else:
                    assert a & b and a - b and b - a
                    kind = "proper_overlap"
                assert (kind == "proper_overlap") == alternating
                whole = {s: disks[s]["is_whole_graph_outer_boundary"] for s in disks}
                assert not (whole["A"] and whole["B"])
                assert whole["A"] == (kind == "B_in_A")
                assert whole["B"] == (kind == "A_in_B")
                type_counts[kind] += 1
                outer_counts.update({**whole, "both": whole["A"] and whole["B"]})
                embedding_id = f"r{row['id']}-f{outer}"
                witnesses.setdefault(kind, embedding_id)
                row["plane_embeddings"].append({
                    "id": embedding_id, "outer_face": outer,
                    "outer_boundary": faces[outer], "disks": disks,
                    "region_type": kind, "common_interior_faces": sorted(a & b),
                    "A_only_faces": sorted(a - b), "B_only_faces": sorted(b - a),
                    "outside_both_faces": sorted(set(range(4)) - (a | b)),
                    "meets_disjoint_disk_policy": kind == "disjoint_interiors",
                    "prescribed_transition_legality": "unknown",
                })
        records.append(row)

    assert histogram == {2: 30, 4: 6}
    assert type_counts == {"disjoint_interiors": 8, "B_in_A": 4,
                           "A_in_B": 4, "proper_overlap": 8}
    assert outer_counts == {"A": 4, "B": 4, "both": 0}
    # Every simple cycle uses exactly two complete paths (all other vertices
    # have degree two). No eight-port simple boundary exists in this graph.
    cycles = [{"paths": (i, j), "vertices": PATHS[i] + tuple(reversed(PATHS[j][1:-1]))}
              for i, j in combinations(range(4), 2)]
    assert sorted(len(c["vertices"]) for c in cycles) == [3, 4, 5, 5, 6, 7]
    source_paths = (SOURCE, str(Path(__file__).resolve().relative_to(ROOT)))
    return {
        "schema": "c5-two-vertex-reference-topology-v1",
        "scope": "All rotations of the single saved reference graph; no other representatives or transition policy.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
        "source_case": record["name"], "inputs": record["inputs"],
        "identifications": record["identifications"], "boundary_maps": frames,
        "graph": {"vertices": vertices, "edges": sorted(edges), "paths": PATHS},
        "joint": record["joint"], "projections": record["projections"],
        "colouring_check": {"assignments_examined": 4**8, "edge_only_replay_matches": True},
        "summary": {"abstract_planar": True, "rotations_examined": len(records),
                    "face_count_histogram": dict(sorted(histogram.items())),
                    "sphere_rotations": 6, "plane_embeddings_with_outer_face": 24,
                    "region_type_counts": dict(sorted(type_counts.items())),
                    "whole_graph_outer_boundary_counts": dict(sorted(outer_counts.items())),
                    "all_eight_ports_on_one_simple_boundary": False,
                    "prescribed_transition_legality": "unknown"},
        "region_type_witnesses": dict(sorted(witnesses.items())),
        "simple_cycles": cycles, "rotations": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved topology differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
