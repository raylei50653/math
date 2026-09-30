#!/usr/bin/env python3
"""Certify planarity and both original-frame obstructions of private_interiors.

Standard library only: verify a fixed rotation by its face permutation, and
verify alternating, internally disjoint original paths for each frame. No
planarity oracle, rotation enumeration, or claim about other representatives.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from c5_two_vertex_join import expand, graph_extensions, source_graph
from c5_two_vertex_join_topology import (
    canonical_colours, components, cycle_edges, disk_sides, edge, path_edges,
    trace_faces,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/eight_point_joins.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/private_topology.json"

# Discovery used NetworkX 3.6.1 on the saved graph. Replay checks every dart,
# every original edge, connectedness and Euler=2 without importing NetworkX.
ROTATION = {
    "a0": ("a1", "A_inner9", "A_inner5", "A_inner7", "A_inner6", "A_inner8",
           "a4", "b0", "B_inner6", "b2"),
    "a1": ("a0", "a2", "A_inner9"),
    "a2": ("a1", "b2", "b4", "a3", "A_inner7", "A_inner5", "A_inner9"),
    "a3": ("a2", "a4", "A_inner8", "A_inner6", "A_inner7"),
    "a4": ("a3", "a0", "A_inner8"),
    "b0": ("b4", "B_inner5", "B_inner6", "a0"),
    "b2": ("a2", "a0", "B_inner6", "B_inner5", "b4"),
    "b4": ("b2", "B_inner5", "b0", "a2"),
    "A_inner5": ("A_inner7", "a0", "A_inner9", "a2"),
    "A_inner6": ("A_inner8", "a0", "A_inner7", "a3"),
    "A_inner7": ("A_inner6", "a0", "A_inner5", "a2", "a3"),
    "A_inner8": ("a4", "a0", "A_inner6", "a3"),
    "A_inner9": ("A_inner5", "a0", "a1", "a2"),
    "B_inner5": ("b0", "b4", "b2", "B_inner6"),
    "B_inner6": ("B_inner5", "b2", "a0", "b0"),
}
OUTER_BOUNDARY = ("a0", "a4", "a3", "a2", "b4", "b0")
OBSTRUCTION_PATHS = {
    "A": (("a0", "b2", "a2"),
          ("a1", "A_inner9", "A_inner5", "A_inner7", "a3")),
    "B": (("a0", "a1", "a2"), ("b0", "B_inner6", "b2")),
}


def source_case():
    saved = json.loads((ROOT / SOURCE).read_text())
    for path, digest in saved["source_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    record, = (r for r in saved["cases"] if r["name"] == "private_interiors")
    assert record["inputs"] == {
        "A": {"class_id": 127, "source_cell_key": "127", "pair": [0, 2]},
        "B": {"class_id": 167, "source_cell_key": "167", "pair": [1, 3]},
    }
    assert record["identifications"] == [["a0", "b1"], ["a2", "b3"]]
    graph = record["graph"]
    vertices = tuple(graph["vertices"])
    assert len(vertices) == len(set(vertices)) == 15
    assert list(vertices[:8]) == record["joint"]["ports"]
    edges = {edge(vertices[u], vertices[v]) for u, v in graph["edges"]}
    assert len(edges) == len(graph["edges"]) == 35
    frames = {s: tuple(record["boundary_maps"][s]) for s in ("A", "B")}
    assert frames == {"A": ("a0", "a1", "a2", "a3", "a4"),
                      "B": ("b0", "a0", "b2", "a2", "b4")}
    catalogue = json.loads((ROOT / "artifacts/c5_cells/cells.json").read_text())
    source_edges, private = {}, {}
    for side in ("A", "B"):
        cell = catalogue["cells"][record["inputs"][side]["source_cell_key"]]
        n, original_edges = source_graph(cell)
        mapping = graph["source_vertex_maps"][side]
        assert n == len(mapping) == len(set(mapping))
        assert tuple(mapping[:5]) == frames[side]
        assert original_edges == tuple(map(tuple, graph["source_edges_with_frames"][side]))
        source_edges[side] = {edge(mapping[u], mapping[v]) for u, v in original_edges}
        private[side] = mapping[5:]
        assert cycle_edges(frames[side]) <= source_edges[side]
    maps = graph["source_vertex_maps"]
    assert set(maps["A"]) & set(maps["B"]) == {"a0", "a2"}
    assert set(maps["A"]) | set(maps["B"]) == set(vertices)
    assert len(private["A"]) == 5 and len(private["B"]) == 2
    assert source_edges["A"] | source_edges["B"] == edges
    assert not source_edges["A"] & source_edges["B"] and not graph["shared_edges"]
    return record, vertices, edges, frames, source_edges, private, saved["pattern_order"]


def check_obstruction(frame, paths, edges, source_edges):
    """Check the hypotheses of the disk alternating-crosscuts obstruction."""
    assert len(frame) == len(set(frame)) == 5
    assert cycle_edges(frame) <= edges
    endpoints, rows = [], []
    for path in paths:
        assert len(path) >= 3 and len(path) == len(set(path))
        assert path[0] in frame and path[-1] in frame
        assert set(path[1:-1]).isdisjoint(frame)
        actual = path_edges(path)
        assert actual <= edges
        owners = [s for s in ("A", "B") if actual <= source_edges[s]]
        owner, = owners
        endpoints.extend((path[0], path[-1]))
        rows.append({"vertices": path, "edges": sorted(actual), "source": owner})
    assert len(set(endpoints)) == 4
    assert set(paths[0]).isdisjoint(paths[1])
    order = [v for v in frame if v in endpoints]
    labels = [0 if v in (paths[0][0], paths[0][-1]) else 1 for v in order]
    assert all(labels[i] != labels[(i + 1) % 4] for i in range(4))
    return {"frame": frame, "paths": rows, "cyclic_endpoint_order": order,
            "path_indices_in_cyclic_order": labels,
            "original_edges_only": True, "internally_disjoint_from_frame": True,
            "vertex_disjoint_paths": True, "alternating_endpoints": True,
            "whole_graph_disk_with_this_frame_possible": False,
            "inference": "Jordan disk crosscuts with alternating endpoints must meet"}


def build():
    record, vertices, edges, frames, source_edges, private, pattern_order = source_case()
    rotation = dict(sorted(ROTATION.items()))
    assert set(rotation) == set(vertices)
    assert len(components({v: set(ns) for v, ns in rotation.items()})) == 1
    faces, dart_face = trace_faces(rotation, edges)
    euler = len(vertices) - len(edges) + len(faces)
    assert euler == 2 and len(faces) == 22
    assert all(len(f) == len(set(f)) for f in faces)
    assert sum(map(len, faces)) == 2 * len(edges) == 70
    assert Counter(map(len, faces)) == {3: 20, 4: 1, 6: 1}
    outer, = (i for i, f in enumerate(faces) if f == OUTER_BOUNDARY)
    disks = {s: disk_sides(frame, edges, faces, dart_face, outer)
             for s, frame in frames.items()}
    for side, disk in disks.items():
        locations = disk["edge_locations"]
        inside = set(locations["inside"])
        boundary = set(locations["boundary"])
        own = source_edges[side]
        other = source_edges["B" if side == "A" else "A"]
        assert own - boundary <= inside
        assert other <= set(locations["outside"])
        assert not disk["is_whole_graph_outer_boundary"]
        # Every private vertex has an incident original edge strictly inside.
        assert all(any(v in e for e in own & inside) for v in private[side])
        disk["source_private_vertices_inside"] = private[side]
        disk["entire_source_graph_in_own_disk"] = True
        disk["other_source_edges_outside"] = True
    assert set(disks["A"]["inside_faces"]).isdisjoint(disks["B"]["inside_faces"])

    obstructions = {s: check_obstruction(frames[s], OBSTRUCTION_PATHS[s], edges, source_edges)
                    for s in ("A", "B")}
    # Full same-graph replay: all 4^8 port assignments, with the seven original
    # private vertices solved from edges. Compare actual sets, not only counts.
    graph_edges = record["graph"]["edges"]
    accepted, witnesses = graph_extensions(len(vertices), graph_edges, 8)
    patterns = {canonical_colours(row) for row in accepted}
    assert patterns == {tuple(row) for row in record["joint"]["patterns"]}
    assert accepted == expand(patterns)
    assert len(accepted) == record["joint"]["labelled_assignments"] == 1440
    assert len(patterns) == record["joint"]["global_s4_orbits"] == 60
    assert witnesses == {tuple(w["pattern"]): tuple(w["colouring"])
                         for w in record["graph"]["witnesses"]}
    assert all(all(full[u] != full[v] for u, v in graph_edges) for full in witnesses.values())
    for s, frame in frames.items():
        indices = [vertices.index(v) for v in frame]
        projected = {canonical_colours(tuple(row[i] for i in indices)) for row in accepted}
        assert projected == {tuple(p) for p in record["projections"][s]["patterns"]}
        mask = sum(1 << i for i, p in enumerate(pattern_order) if tuple(p) in projected)
        assert mask == record["projections"][s]["mask"] == {"A": 127, "B": 167}[s]

    source_paths = (SOURCE, "scripts/c5_two_vertex_join.py", "scripts/boundary_relations.py",
                    "scripts/c5_two_vertex_join_topology.py",
                    str(Path(__file__).resolve().relative_to(ROOT)))
    return {
        "schema": "c5-two-vertex-private-topology-v1",
        "scope": "One saved private_interiors graph; one sphere rotation and two universal frame obstructions.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
        "source_case": record["name"], "inputs": record["inputs"],
        "identifications": record["identifications"], "boundary_maps": frames,
        "graph": record["graph"], "named_edges": sorted(edges),
        "source_named_edges": {s: sorted(es) for s, es in source_edges.items()},
        "joint": record["joint"], "projections": record["projections"],
        "colouring_check": {"port_assignments_examined": 4**8, "private_vertices": 7,
                            "edge_backtracking_matches_full_join": True,
                            "both_full_projections_match": True},
        "embedding": {"clockwise_rotations": rotation, "faces": faces,
                      "euler_characteristic": euler, "outer_face": outer,
                      "outer_boundary": faces[outer], "disks": disks,
                      "region_type": "disjoint_interiors",
                      "meets_disjoint_disk_policy": True},
        "frame_obstructions": obstructions,
        "summary": {"abstract_planar": True, "vertices": len(vertices), "edges": len(edges),
                    "faces_in_witness": len(faces),
                    "A_frame_can_be_whole_graph_disk_boundary": False,
                    "B_frame_can_be_whole_graph_disk_boundary": False,
                    "disjoint_source_disks_witness": True,
                    "all_embeddings_classified": False,
                    "prescribed_transition_legality": "unknown"},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved private topology differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
