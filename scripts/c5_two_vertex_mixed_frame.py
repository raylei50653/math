#!/usr/bin/env python3
"""Certify the mixed C5 boundary of the saved private_interiors_reverse graph.

Retain the original graph and complete eight-port join. Compare its named
projection with direct ten-interior extension, and with the existing R255
one-interior representative. Standard library only; no catalogue search.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from boundary_relations import Relation, normalize
from c5_two_vertex_join import expand, graph_extensions, source_graph
from c5_two_vertex_join_topology import components, cycle_edges, disk_sides, edge, trace_faces
from c5_two_vertex_private_reverse_topology import replay_colouring, source_case


ROOT = Path(__file__).resolve().parents[1]
TOPOLOGY = "artifacts/c5_two_vertex_overlap/private_reverse_topology.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/mixed_frame_relation.json"
FRAME = ("a0", "a4", "a3", "a2", "b2")
HIDDEN_PORTS = ("a1", "b0", "b4")


def check_hashes(record):
    for path, digest in record["source_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path


def check_disk(vertices, edges, rotation, frame, outer):
    assert len(frame) == len(set(frame)) == 5
    assert cycle_edges(frame) <= edges
    assert set(rotation) == set(vertices)
    assert len(components({v: set(ns) for v, ns in rotation.items()})) == 1
    faces, dart_face = trace_faces(rotation, edges)
    assert len(vertices) - len(edges) + len(faces) == 2
    assert all(len(face) == len(set(face)) for face in faces)
    assert cycle_edges(faces[outer]) == cycle_edges(frame)
    disk = disk_sides(frame, edges, faces, dart_face, outer)
    assert disk["is_whole_graph_outer_boundary"]
    assert disk["outside_faces"] == [outer]
    assert not disk["edge_locations"]["outside"]
    internal = set(vertices) - set(frame)
    inside = set(disk["edge_locations"]["inside"])
    assert all({e for e in edges if v in e} <= inside for v in internal)
    return faces, disk


def boundary_first_graph(vertices, edges, frame):
    order = frame + tuple(v for v in vertices if v not in frame)
    index = {v: i for i, v in enumerate(order)}
    remapped = sorted(edge(index[u], index[v]) for u, v in edges)
    return order, remapped


def source_projections(record, frames, pattern_order):
    """Project complete source relations, retaining their common named colours."""
    kept = {"A": FRAME[:4], "B": ("a2", "b2", "a0")}
    results, labelled = {}, {}
    for side in ("A", "B"):
        mask = record["inputs"][side]["class_id"]
        rows = [p for i, p in enumerate(pattern_order) if mask & (1 << i)]
        relation = Relation.of(frames[side], rows).project(kept[side])
        actual = expand(relation.patterns)
        expected = {
            q for q in product(range(4), repeat=len(kept[side]))
            if all(q[i] != q[i + 1] for i in range(len(q) - 1))
            and (side == "B" or len(set(q)) <= 3)
        }
        assert actual == expected
        labelled[side] = actual
        results[side] = {"source_mask": mask, "ports": kept[side],
                         "patterns": sorted(relation.patterns),
                         "labelled_assignments": len(actual)}
    # No independent normalization of the two source restrictions at this join.
    joined = {q for q in product(range(4), repeat=5)
              if q[:4] in labelled["A"] and (q[3], q[4], q[0]) in labelled["B"]}
    return results, joined


def one_interior_representative(catalogue, expected):
    cell = catalogue["cells"]["255"]
    n, edges = source_graph(cell)
    assert n == 6
    assert cell["edges"] == [[0, 5], [1, 5], [2, 5], [3, 5]]
    accepted, witnesses = graph_extensions(n, edges, 5)
    assert accepted == expected
    vertices = FRAME + ("R255_hub",)
    named_edges = {edge(vertices[u], vertices[v]) for u, v in edges}
    rotation = {FRAME[i]: (FRAME[(i + 1) % 5],)
                + ((vertices[5],) if i < 4 else ()) + (FRAME[(i - 1) % 5],)
                for i in range(5)}
    rotation[vertices[5]] = FRAME[:4]
    faces, _ = trace_faces(rotation, named_edges)
    outer, = (i for i, f in enumerate(faces) if cycle_edges(f) == cycle_edges(FRAME))
    faces, disk = check_disk(vertices, named_edges, rotation, FRAME, outer)
    return {"catalogue_id": 255, "source_cell": cell, "vertices": vertices,
            "edges": edges, "named_edges": sorted(named_edges),
            "clockwise_rotations": rotation, "faces": faces, "outer_face": outer,
            "disk": disk, "original_frame_positions_map_to": FRAME,
            "witnesses": [{"pattern": q, "colouring": witnesses[q]}
                          for q in sorted(witnesses)],
            "full_labelled_relation_equals_original_graph": True,
            "claim": "Same ordered five-port relation; not a graph minor or an eight-port replacement."}


def rejection_witness(q, edges):
    """A named forced-colour contradiction on original edges, for both zeros."""
    colours = dict(zip(FRAME, q))
    steps = []
    for vertex, neighbours in (
            ("A_inner7", ("a0", "a3", "a2")),
            ("A_inner6", ("a0", "a3", "A_inner7")),
            ("A_inner8", ("a0", "a3", "a4"))):
        assert all(edge(vertex, w) in edges for w in neighbours)
        forbidden = {colours[w] for w in neighbours}
        colour, = set(range(4)) - forbidden
        colours[vertex] = colour
        steps.append({"vertex": vertex, "original_neighbours": neighbours,
                      "forbidden_colours": sorted(forbidden), "forced_colour": colour})
    conflict = ("A_inner6", "A_inner8")
    assert edge(*conflict) in edges and colours[conflict[0]] == colours[conflict[1]]
    return {"pattern": q, "steps": steps, "monochromatic_original_edge": conflict}


def build():
    record, vertices, edges, frames, _, _, pattern_order = source_case()
    topology = json.loads((ROOT / TOPOLOGY).read_text())
    check_hashes(topology)
    assert topology["source_case"] == record["name"] == "private_interiors_reverse"
    assert topology["graph"] == record["graph"]
    assert topology["joint"] == record["joint"]
    assert topology["embedding"]["outer_boundary"] == list(FRAME)
    embedding = topology["embedding"]
    faces, disk = check_disk(vertices, edges, embedding["clockwise_rotations"],
                             FRAME, embedding["outer_face"])
    assert [list(f) for f in faces] == embedding["faces"]
    assert (len(vertices), len(edges), len(faces)) == (15, 35, 22)
    assert len(disk["edge_locations"]["inside"]) == 30
    assert set(vertices[:8]) - set(FRAME) == set(HIDDEN_PORTS)
    frame_indices = tuple(vertices.index(v) for v in FRAME)
    hidden_indices = tuple(vertices.index(v) for v in HIDDEN_PORTS)
    assert frame_indices == (0, 4, 3, 2, 6)

    joint_labelled, joint_patterns, joint_witnesses = replay_colouring(record)
    projected = {tuple(row[i] for i in frame_indices) for row in joint_labelled}
    relation = Relation.of(vertices[:8], joint_patterns).project(FRAME)
    assert expand(relation.patterns) == projected

    # An independent call exposes only five ports; a1, b0, b4 now belong to
    # the ten private vertices. The solver reads only the 35 original edges.
    direct_order, direct_edges = boundary_first_graph(vertices, edges, FRAME)
    direct, direct_witnesses = graph_extensions(len(vertices), direct_edges, 5)
    assert direct == projected
    catalogue = json.loads((ROOT / "artifacts/c5_cells/cells.json").read_text())
    assert pattern_order == catalogue["pattern_order"]
    patterns = tuple(map(tuple, pattern_order))
    universe = {q for q in product(range(4), repeat=5)
                if all(q[i] != q[(i + 1) % 5] for i in range(5))}
    assert {normalize(q) for q in universe} == set(patterns)
    formula = {q for q in universe if len(set(q[:4])) <= 3}
    assert direct == formula
    mask = sum(1 << i for i, p in enumerate(patterns) if p in relation.patterns)
    assert mask == 255 and len(direct) == 192 and len(relation.patterns) == 8
    partial_sources, source_join = source_projections(record, frames, pattern_order)
    assert source_join == direct

    # Align every saved full colouring to the new boundary BEFORE retaining
    # its hidden-port tuple. A proper C5 uses >=3 colours, so its stabilizer
    # in S4 is trivial: one joint orbit contributes one row per canonical q.
    fibres = {q: [] for q in patterns}
    for p in sorted(joint_patterns):
        full = joint_witnesses[p]
        traversal = frame_indices + tuple(i for i in range(len(vertices))
                                           if i not in frame_indices)
        relabelled = normalize(tuple(full[i] for i in traversal))
        by_vertex = dict(zip(traversal, relabelled))
        aligned = tuple(by_vertex[i] for i in range(len(vertices)))
        q = tuple(aligned[i] for i in frame_indices)
        assert q == normalize(q) and q in relation.patterns
        assert all(aligned[vertices.index(u)] != aligned[vertices.index(v)] for u, v in edges)
        assert normalize(aligned[:8]) == p
        fibres[q].append({"source_joint_pattern": p, "joint_colouring": aligned[:8],
                          "hidden_colours": tuple(aligned[i] for i in hidden_indices),
                          "full_colouring": aligned})
    rows = []
    for i, q in enumerate(patterns):
        fibre = sorted(fibres[q], key=lambda entry: entry["joint_colouring"])
        actual_fibre = {row for row in joint_labelled
                        if tuple(row[j] for j in frame_indices) == q}
        assert {entry["joint_colouring"] for entry in fibre} == actual_fibre
        assert len(fibre) == len(actual_fibre)
        direct_full = None
        if q in direct_witnesses:
            by_name = dict(zip(direct_order, direct_witnesses[q]))
            direct_full = tuple(by_name[v] for v in vertices)
            assert direct_full[:8] in actual_fibre
        rows.append({"pattern_index": i, "pattern": q, "accepted": q in direct,
                     "joint_orbits_over_pattern": len(fibre),
                     "labelled_joint_assignments_over_orbit": 24 * len(fibre),
                     "direct_full_colouring": direct_full, "complete_fibre": fibre})
    assert [len(fibres[q]) for q in patterns] == [6, 6, 6, 12, 12, 12, 3, 3, 0, 0]
    assert sum(len(f) for f in fibres.values()) == 60

    # Even ALL ten pair projections lose the four-vertex colour obstruction.
    pairs = {ij: {tuple(q[i] for i in ij) for q in direct}
             for ij in combinations(range(5), 2)}
    pair_relaxation = {q for q in product(range(4), repeat=5)
                       if all(tuple(q[i] for i in ij) in allowed
                              for ij, allowed in pairs.items())}
    assert pair_relaxation == universe and len(universe) == 240
    spurious = pair_relaxation - direct
    assert len(spurious) == 48
    rejected = sorted(set(patterns) - relation.patterns)
    assert {normalize(q) for q in spurious} == set(rejected)
    assert rejected == [(0, 1, 2, 3, 1), (0, 1, 2, 3, 2)]

    small = one_interior_representative(catalogue, direct)
    # Keep the old artifacts untouched and bind the entire imported verifier
    # chain, the original catalogue, and the exact saved topology companion.
    paths = set(topology["source_sha256"]) | {
        TOPOLOGY, "artifacts/c5_cells/cells.json",
        str(Path(__file__).resolve().relative_to(ROOT)),
    }
    return {
        "schema": "c5-two-vertex-mixed-frame-relation-v1",
        "scope": "The specified mixed outer face of one saved reverse graph; exact full five-port relation.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)},
        "source_case": record["name"], "inputs": record["inputs"],
        "identifications": record["identifications"], "original_boundary_maps": frames,
        "original_graph": record["graph"], "original_joint": record["joint"],
        "new_frame": FRAME, "frame_indices_in_original_ports": frame_indices,
        "hidden_original_ports": HIDDEN_PORTS,
        "new_internal_vertices": direct_order[5:],
        "embedding": {"clockwise_rotations": embedding["clockwise_rotations"],
                      "faces": faces, "outer_face": embedding["outer_face"], "disk": disk},
        "relation": {"ports": FRAME, "mask": mask, "catalogue_id": mask,
                     "pattern_order": patterns, "patterns": sorted(relation.patterns),
                     "rejected_proper_patterns": rejected, "global_s4_orbits": 8,
                     "labelled_assignments": sorted(direct), "labelled_assignment_count": len(direct),
                     "formula": "proper_C5(q) and len(set(q[:4])) <= 3",
                     "all_pattern_fibres": rows},
        "source_partial_relations": partial_sources,
        "rejection_witnesses": [rejection_witness(q, edges) for q in rejected],
        "pair_only_negative_control": {
            "all_ten_pairs_used": True, "labelled_assignments": len(pair_relaxation),
            "spurious_labelled_assignments": len(spurious), "spurious_patterns": rejected,
            "pairs": [{"indices": ij, "ports": [FRAME[i] for i in ij],
                       "allowed_labelled_pairs": sorted(allowed)} for ij, allowed in pairs.items()]},
        "one_interior_representative": small,
        "checks": {"original_port_assignments_examined": 4**8,
                   "new_frame_assignments_examined": 4**5,
                   "small_representative_assignments_examined": 4**5,
                   "direct_projection_source_formula_and_small_graph_agree": True,
                   "complete_joint_fibres_and_full_witnesses_verified": True,
                   "saved_sphere_embedding_replayed": True},
        "summary": {"vertices": 15, "edges": 35, "new_internal_vertices": 10,
                    "whole_graph_disk_boundary": True, "mask": mask,
                    "global_s4_orbits": 8, "labelled_assignments": 192,
                    "original_joint_orbits": 60, "catalogue_representative_internal_vertices": 1,
                    "replacement_requires_no_future_contact_with_hidden_vertices": True,
                    "replacement_scope": "Colouring contexts sharing only the named new frame.",
                    "prescribed_transition_legality": "unknown",
                    "new_lean_theorem": False},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved mixed-frame relation differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
