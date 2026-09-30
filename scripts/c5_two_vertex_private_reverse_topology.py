#!/usr/bin/env python3
"""Certify the saved private_interiors_reverse graph with its original names.

Standard library only. Replay a sphere rotation, disjoint source disks, two
alternating-path obstructions, and the full join; retain its difference from
the forward join. No classification of other rotations or representatives.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from c5_two_vertex_join import expand, graph_extensions, source_graph
from c5_two_vertex_join_topology import (
    canonical_colours, components, cycle_edges, disk_sides, edge, trace_faces,
)
from c5_two_vertex_private_topology import (
    check_obstruction, source_case as forward_source_case,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/eight_point_joins.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/private_reverse_topology.json"

# Constructed by reattaching the B source at the reversed ordered pair.
# These are candidates only: every original dart and face is verified below.
ROTATION = {
    "a0": ("a1", "A_inner9", "A_inner5", "A_inner7", "A_inner6", "A_inner8",
           "a4", "b2", "b4"),
    "a1": ("a0", "a2", "A_inner9"),
    "a2": ("a1", "b0", "B_inner6", "b2", "a3", "A_inner7", "A_inner5", "A_inner9"),
    "a3": ("a2", "a4", "A_inner8", "A_inner6", "A_inner7"),
    "a4": ("a3", "a0", "A_inner8"),
    "b0": ("b4", "B_inner5", "B_inner6", "a2"),
    "b2": ("a0", "a2", "B_inner6", "B_inner5", "b4"),
    "b4": ("b2", "B_inner5", "b0", "a0"),
    "A_inner5": ("A_inner7", "a0", "A_inner9", "a2"),
    "A_inner6": ("A_inner8", "a0", "A_inner7", "a3"),
    "A_inner7": ("A_inner6", "a0", "A_inner5", "a2", "a3"),
    "A_inner8": ("a4", "a0", "A_inner6", "a3"),
    "A_inner9": ("A_inner5", "a0", "a1", "a2"),
    "B_inner5": ("b0", "b4", "b2", "B_inner6"),
    "B_inner6": ("B_inner5", "b2", "a2", "b0"),
}
OUTER_BOUNDARY = ("a0", "a4", "a3", "a2", "b2")
OBSTRUCTION_PATHS = {
    "A": (("a0", "b2", "a2"),
          ("a1", "A_inner9", "A_inner5", "A_inner7", "a3")),
    "B": (("a0", "a1", "a2"), ("b0", "B_inner6", "b2")),
}


def source_case():
    saved = json.loads((ROOT / SOURCE).read_text())
    for path, digest in saved["source_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    record, = (r for r in saved["cases"] if r["name"] == "private_interiors_reverse")
    assert record["inputs"] == {
        "A": {"class_id": 127, "source_cell_key": "127", "pair": [0, 2]},
        "B": {"class_id": 167, "source_cell_key": "167", "pair": [3, 1]},
    }
    assert record["identifications"] == [["a0", "b3"], ["a2", "b1"]]
    graph = record["graph"]
    vertices = tuple(graph["vertices"])
    assert len(vertices) == len(set(vertices)) == 15
    assert list(vertices[:8]) == record["joint"]["ports"]
    edges = {edge(vertices[u], vertices[v]) for u, v in graph["edges"]}
    assert len(edges) == len(graph["edges"]) == 35
    frames = {s: tuple(record["boundary_maps"][s]) for s in ("A", "B")}
    assert frames == {"A": ("a0", "a1", "a2", "a3", "a4"),
                      "B": ("b0", "a2", "b2", "a0", "b4")}
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


def replay_colouring(record):
    graph = record["graph"]
    accepted, witnesses = graph_extensions(len(graph["vertices"]), graph["edges"], 8)
    patterns = {canonical_colours(row) for row in accepted}
    assert patterns == {tuple(row) for row in record["joint"]["patterns"]}
    assert accepted == expand(patterns)
    assert len(accepted) == record["joint"]["labelled_assignments"] == 1440
    assert len(patterns) == record["joint"]["global_s4_orbits"] == 60
    assert witnesses == {tuple(w["pattern"]): tuple(w["colouring"])
                         for w in graph["witnesses"]}
    return accepted, patterns, witnesses


def compare_forward(record, accepted, patterns, witnesses):
    forward, *_ = forward_source_case()
    f_accepted, f_patterns, f_witnesses = replay_colouring(forward)
    assert forward["joint"]["ports"] == record["joint"]["ports"]
    assert forward["graph"]["vertices"] == record["graph"]["vertices"]
    common = f_patterns & patterns
    f_only, r_only = f_patterns - patterns, patterns - f_patterns
    assert len(common) == 44 and len(f_only) == len(r_only) == 16
    assert len(f_accepted & accepted) == 1056
    assert len(f_accepted - accepted) == len(accepted - f_accepted) == 384
    controls = []
    for owner, other, rows, full in ((forward, record, f_only, f_witnesses),
                                    (record, forward, r_only, witnesses)):
        row = min(rows)
        other_graph = other["graph"]
        conflicts = [(u, v) for u, v in other_graph["edges"]
                     if v < 8 and row[u] == row[v]]
        assert conflicts  # Concrete original-edge rejection, not just absence.
        controls.append({
            "accepted_by": owner["name"], "rejected_by": other["name"],
            "pattern": row, "full_colouring_in_accepted_graph": full[row],
            "monochromatic_original_edges_in_other_graph": [
                (other_graph["vertices"][u], other_graph["vertices"][v])
                for u, v in conflicts],
        })
    return {"ports": record["joint"]["ports"], "common_patterns": sorted(common),
            "forward_only_patterns": sorted(f_only), "reverse_only_patterns": sorted(r_only),
            "common_labelled_assignments": 1056, "each_only_labelled_assignments": 384,
            "both_graphs_replayed_from_original_edges": True,
            "distinguishing_colourings": controls}


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
    assert Counter(map(len, faces)) == {3: 20, 5: 2}
    outer, = (i for i, f in enumerate(faces) if f == OUTER_BOUNDARY)
    disks = {s: disk_sides(frame, edges, faces, dart_face, outer)
             for s, frame in frames.items()}
    for side, disk in disks.items():
        locations = disk["edge_locations"]
        inside, boundary = set(locations["inside"]), set(locations["boundary"])
        own = source_edges[side]
        other = source_edges["B" if side == "A" else "A"]
        assert own - boundary <= inside
        assert other <= set(locations["outside"])
        assert not disk["is_whole_graph_outer_boundary"]
        # Every incident edge of each original private vertex is strictly inside.
        assert all({e for e in edges if v in e} <= inside for v in private[side])
        assert all(any(v in e for e in inside) for v in private[side])
        disk["source_private_vertices_inside"] = private[side]
        disk["entire_source_graph_in_own_disk"] = True
        disk["other_source_edges_outside"] = True
    assert set(disks["A"]["inside_faces"]).isdisjoint(disks["B"]["inside_faces"])

    obstructions = {s: check_obstruction(frames[s], OBSTRUCTION_PATHS[s], edges, source_edges)
                    for s in ("A", "B")}
    accepted, patterns, witnesses = replay_colouring(record)
    for s, frame in frames.items():
        indices = [vertices.index(v) for v in frame]
        projected = {canonical_colours(tuple(row[i] for i in indices)) for row in accepted}
        assert projected == {tuple(p) for p in record["projections"][s]["patterns"]}
        mask = sum(1 << i for i, p in enumerate(pattern_order) if tuple(p) in projected)
        assert mask == record["projections"][s]["mask"] == {"A": 127, "B": 167}[s]
    comparison = compare_forward(record, accepted, patterns, witnesses)

    source_paths = (SOURCE, "scripts/c5_two_vertex_join.py", "scripts/boundary_relations.py",
                    "scripts/c5_two_vertex_join_topology.py",
                    "scripts/c5_two_vertex_private_topology.py",
                    str(Path(__file__).resolve().relative_to(ROOT)))
    return {
        "schema": "c5-two-vertex-private-reverse-topology-v1",
        "scope": "One saved private_interiors_reverse graph; one sphere rotation and two universal frame obstructions.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
        "source_case": record["name"], "inputs": record["inputs"],
        "identifications": record["identifications"], "boundary_maps": frames,
        "graph": record["graph"], "named_edges": sorted(edges),
        "source_named_edges": {s: sorted(es) for s, es in source_edges.items()},
        "joint": record["joint"], "projections": record["projections"],
        "colouring_check": {"port_assignments_examined_per_graph": 4**8, "graphs_replayed": 2,
                            "private_vertices_per_graph": 7,
                            "edge_backtracking_matches_full_join": True,
                            "both_full_projections_match": True},
        "embedding": {"clockwise_rotations": rotation, "faces": faces,
                      "euler_characteristic": euler, "outer_face": outer,
                      "outer_boundary": faces[outer], "disks": disks,
                      "region_type": "disjoint_interiors",
                      "meets_disjoint_disk_policy": True},
        "frame_obstructions": obstructions, "forward_comparison": comparison,
        "summary": {"abstract_planar": True, "vertices": len(vertices), "edges": len(edges),
                    "faces_in_witness": len(faces),
                    "A_frame_can_be_whole_graph_disk_boundary": False,
                    "B_frame_can_be_whole_graph_disk_boundary": False,
                    "disjoint_source_disks_witness": True,
                    "full_join_equals_forward_in_same_port_order": False,
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
            raise SystemExit(f"FAIL: saved private reverse topology differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
