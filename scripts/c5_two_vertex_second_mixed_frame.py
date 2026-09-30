#!/usr/bin/env python3
"""Certify face 21 of the saved private_interiors_reverse graph.

Keep the full original join and its fibres. Compare its second mixed C5
projection with direct ten-interior extension and the existing R1022 disk.
Standard library only; no new source graphs or rotations are enumerated.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from boundary_relations import Relation, normalize
from c5_two_vertex_join import expand, graph_extensions, source_graph
from c5_two_vertex_join_topology import cycle_edges, edge, trace_faces
from c5_two_vertex_mixed_frame import boundary_first_graph, check_disk, check_hashes
from c5_two_vertex_private_reverse_topology import replay_colouring, source_case


ROOT = Path(__file__).resolve().parents[1]
TOPOLOGY = "artifacts/c5_two_vertex_overlap/private_reverse_topology.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/second_mixed_frame_relation.json"
FRAME = ("a0", "b4", "b0", "a2", "a1")
HIDDEN_PORTS = ("a3", "a4", "b2")
OUTER_FACE = 21


def source_projections(record, frames, pattern_order):
    """Existentially hide disjoint source ports, in one named colour frame."""
    kept = {"A": ("a2", "a1", "a0"), "B": FRAME[:4]}
    results, labelled = {}, {}
    for side in ("A", "B"):
        mask = record["inputs"][side]["class_id"]
        rows = [p for i, p in enumerate(pattern_order) if mask & (1 << i)]
        relation = Relation.of(frames[side], rows).project(kept[side])
        actual = expand(relation.patterns)
        expected = {
            q for q in product(range(4), repeat=len(kept[side]))
            if all(q[i] != q[i + 1] for i in range(len(q) - 1))
            and (side == "A" or len(set(q)) >= 3)
        }
        assert actual == expected
        labelled[side] = actual
        results[side] = {"source_mask": mask, "ports": kept[side],
                         "patterns": sorted(relation.patterns),
                         "labelled_assignments": len(actual)}
    joined = {q for q in product(range(4), repeat=5)
              if (q[3], q[4], q[0]) in labelled["A"] and q[:4] in labelled["B"]}
    return results, joined


def rejection_witness(q, edges):
    """The original B triangle has only two available colours at each point."""
    colours = dict(zip(FRAME, q))
    triangle = ("b2", "B_inner5", "B_inner6")
    attachments = {"b2": ("a0", "a2"),
                   "B_inner5": ("b0", "b4"),
                   "B_inner6": ("b0", "a2")}
    assert all(edge(u, v) in edges for u, v in combinations(triangle, 2))
    domains = {}
    for v, neighbours in attachments.items():
        assert all(edge(v, w) in edges for w in neighbours)
        domains[v] = set(range(4)) - {colours[w] for w in neighbours}
    palette = domains["b2"]
    assert len(palette) == 2 and all(d == palette for d in domains.values())
    branches = []
    for colour in sorted(palette):
        branch = {**colours, "b2": colour}
        steps = []
        for v in triangle[1:]:
            neighbours = attachments[v] + ("b2",)
            forbidden = {branch[w] for w in neighbours}
            forced, = set(range(4)) - forbidden
            branch[v] = forced
            steps.append({"vertex": v, "original_neighbours": neighbours,
                          "forbidden_colours": sorted(forbidden), "forced_colour": forced})
        assert branch["B_inner5"] == branch["B_inner6"]
        branches.append({"b2_colour": colour, "steps": steps,
                         "monochromatic_original_edge": ("B_inner5", "B_inner6")})
    return {"pattern": q, "original_triangle": triangle,
            "original_boundary_attachments": attachments,
            "common_available_colours": sorted(palette), "exhaustive_branches": branches}


def two_interior_representative(catalogue, expected):
    cell = catalogue["cells"]["1022"]
    n, edges = source_graph(cell)
    assert n == 7
    assert cell["edges"] == [[2, 5], [3, 5], [4, 5], [0, 6], [1, 6], [4, 6], [5, 6]]
    accepted, witnesses = graph_extensions(n, edges, 5)
    assert accepted == expected
    vertices = FRAME + ("R1022_inner5", "R1022_inner6")
    named_edges = {edge(vertices[u], vertices[v]) for u, v in edges}
    candidate = {0: (1, 6, 4), 1: (2, 6, 0), 2: (3, 5, 1), 3: (4, 5, 2),
                 4: (0, 6, 5, 3), 5: (2, 3, 4, 6), 6: (0, 1, 5, 4)}
    # Reflect only the embedding so the bounded side agrees with the original.
    rotation = {vertices[v]: tuple(vertices[w] for w in reversed(ns))
                for v, ns in candidate.items()}
    faces, _ = trace_faces(rotation, named_edges)
    outer, = (i for i, f in enumerate(faces) if cycle_edges(f) == cycle_edges(FRAME))
    faces, disk = check_disk(vertices, named_edges, rotation, FRAME, outer)
    assert (len(vertices), len(edges), len(faces)) == (7, 12, 7)
    assert disk["bounded_side_of_directed_frame"] == "left"
    return {"catalogue_id": 1022, "source_cell": cell, "vertices": vertices,
            "edges": edges, "named_edges": sorted(named_edges),
            "clockwise_rotations": rotation, "faces": faces, "outer_face": outer,
            "disk": disk, "original_frame_positions_map_to": FRAME,
            "witnesses": [{"pattern": q, "colouring": witnesses[q]}
                          for q in sorted(witnesses)],
            "full_labelled_relation_equals_original_graph": True,
            "claim": "Same ordered five-port relation; not a minor or an eight-port replacement."}


def dihedral_relabellings(patterns, accepted, catalogue):
    records = []
    for sign in (1, -1):
        for shift in range(5):
            permutation = tuple((shift + sign * i) % 5 for i in range(5))
            rows = {normalize(tuple(q[j] for j in permutation)) for q in accepted}
            mask = sum(1 << i for i, q in enumerate(patterns) if q in rows)
            assert str(mask) in catalogue["cells"]
            records.append({"new_position_reads_old_position": permutation, "mask": mask})
    assert {r["mask"] for r in records} == {959, 1007, 1015, 1021, 1022}
    assert sum(r["mask"] == 1022 for r in records) == 2
    return {"convention": "new_q[i] = old_q[permutation[i]], then common colour normalization",
            "ordered_match": 1022, "orbit_masks": sorted({r["mask"] for r in records}),
            "stabilizer_size": 2, "all_ten_actions": records,
            "first_mixed_R255_is_not_dihedrally_equivalent": True}


def negative_controls(vertices, edges, rotation):
    checks = (
        ("other_pentagonal_face_is_not_this_boundary",
         lambda: check_disk(vertices, edges, rotation, FRAME, 19)),
        ("accepted_pattern_is_not_a_two_colour_triangle_obstruction",
         lambda: rejection_witness((0, 1, 0, 2, 1), edges)),
        ("missing_original_triangle_edge_invalidates_rejection",
         lambda: rejection_witness((0, 1, 0, 1, 2),
                                   edges - {edge("B_inner5", "B_inner6")})),
    )
    passed = []
    for name, check in checks:
        try:
            check()
        except AssertionError:
            passed.append(name)
        else:
            raise AssertionError(f"negative control was accepted: {name}")
    return passed


def build():
    record, vertices, edges, frames, _, _, pattern_order = source_case()
    topology = json.loads((ROOT / TOPOLOGY).read_text())
    check_hashes(topology)
    assert topology["source_case"] == record["name"] == "private_interiors_reverse"
    assert topology["graph"] == record["graph"] and topology["joint"] == record["joint"]
    embedding = topology["embedding"]
    assert embedding["outer_face"] == 19
    faces, disk = check_disk(vertices, edges, embedding["clockwise_rotations"], FRAME, OUTER_FACE)
    assert [list(f) for f in faces] == embedding["faces"]
    assert tuple(faces[OUTER_FACE]) == FRAME
    assert (len(vertices), len(edges), len(faces)) == (15, 35, 22)
    assert sorted(len(f) for f in faces) == [3] * 20 + [5] * 2
    assert len(disk["edge_locations"]["inside"]) == 30
    assert disk["bounded_side_of_directed_frame"] == "left"
    assert set(vertices[:8]) - set(FRAME) == set(HIDDEN_PORTS)
    frame_indices = tuple(vertices.index(v) for v in FRAME)
    hidden_indices = tuple(vertices.index(v) for v in HIDDEN_PORTS)
    assert frame_indices == (0, 7, 5, 2, 1)

    joint_labelled, joint_patterns, joint_witnesses = replay_colouring(record)
    projected = {tuple(row[i] for i in frame_indices) for row in joint_labelled}
    relation = Relation.of(vertices[:8], joint_patterns).project(FRAME)
    assert expand(relation.patterns) == projected
    direct_order, direct_edges = boundary_first_graph(vertices, edges, FRAME)
    direct, direct_witnesses = graph_extensions(len(vertices), direct_edges, 5)
    assert direct == projected
    catalogue = json.loads((ROOT / "artifacts/c5_cells/cells.json").read_text())
    assert pattern_order == catalogue["pattern_order"]
    patterns = tuple(map(tuple, pattern_order))
    universe = {q for q in product(range(4), repeat=5)
                if all(q[i] != q[(i + 1) % 5] for i in range(5))}
    assert {normalize(q) for q in universe} == set(patterns)
    formula = {q for q in universe if len(set(q[:4])) >= 3}
    assert formula == {q for q in universe if q[0] != q[2] or q[1] != q[3]}
    assert direct == formula
    mask = sum(1 << i for i, p in enumerate(patterns) if p in relation.patterns)
    assert mask == 1022 and len(direct) == 216 and len(relation.patterns) == 9
    partial_sources, source_join = source_projections(record, frames, pattern_order)
    assert source_join == direct

    # Normalize the new frame FIRST, applying the same colour map everywhere.
    # A proper C5 has trivial S4 stabilizer, even when it uses only three colours.
    fibres = {q: [] for q in patterns}
    for p in sorted(joint_patterns):
        full = joint_witnesses[p]
        traversal = frame_indices + tuple(i for i in range(len(vertices)) if i not in frame_indices)
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
        actual_fibre = {row for row in joint_labelled if tuple(row[j] for j in frame_indices) == q}
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
    assert [len(fibres[q]) for q in patterns] == [0, 4, 4, 12, 12, 12, 4, 4, 4, 4]
    assert sum(len(f) for f in fibres.values()) == 60

    pairs = {ij: {tuple(q[i] for i in ij) for q in direct} for ij in combinations(range(5), 2)}
    pair_relaxation = {q for q in product(range(4), repeat=5)
                       if all(tuple(q[i] for i in ij) in allowed for ij, allowed in pairs.items())}
    assert pair_relaxation == universe and len(universe) == 240
    spurious = pair_relaxation - direct
    rejected = sorted(set(patterns) - relation.patterns)
    assert len(spurious) == 24 and {normalize(q) for q in spurious} == set(rejected)
    assert rejected == [(0, 1, 0, 1, 2)]
    small = two_interior_representative(catalogue, direct)
    dihedral = dihedral_relabellings(patterns, relation.patterns, catalogue)
    assert len(relation.patterns) != (255).bit_count()  # D5 preserves orbit count.
    controls = negative_controls(vertices, edges, embedding["clockwise_rotations"])
    paths = set(topology["source_sha256"]) | {
        TOPOLOGY, "artifacts/c5_cells/cells.json", "scripts/c5_two_vertex_mixed_frame.py",
        str(Path(__file__).resolve().relative_to(ROOT)),
    }
    return {
        "schema": "c5-two-vertex-second-mixed-frame-relation-v1",
        "scope": "Face 21 of one saved reverse graph; exact full ordered five-port relation.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)},
        "source_case": record["name"], "inputs": record["inputs"],
        "identifications": record["identifications"], "original_boundary_maps": frames,
        "original_graph": record["graph"], "original_joint": record["joint"],
        "new_frame": FRAME, "frame_indices_in_original_ports": frame_indices,
        "hidden_original_ports": HIDDEN_PORTS, "new_internal_vertices": direct_order[5:],
        "embedding": {"clockwise_rotations": embedding["clockwise_rotations"],
                      "faces": faces, "previous_outer_face": 19,
                      "outer_face": OUTER_FACE, "disk": disk},
        "relation": {"ports": FRAME, "mask": mask, "catalogue_id": mask,
                     "pattern_order": patterns, "patterns": sorted(relation.patterns),
                     "rejected_proper_patterns": rejected, "global_s4_orbits": 9,
                     "labelled_assignments": sorted(direct), "labelled_assignment_count": len(direct),
                     "formula": "proper_C5(q) and (q[0] != q[2] or q[1] != q[3])",
                     "equivalent_formula": "proper_C5(q) and len(set(q[:4])) >= 3",
                     "all_pattern_fibres": rows},
        "source_partial_relations": partial_sources,
        "rejection_witnesses": [rejection_witness(q, edges) for q in rejected],
        "pair_only_negative_control": {
            "all_ten_pairs_used": True, "labelled_assignments": len(pair_relaxation),
            "spurious_labelled_assignments": len(spurious), "spurious_patterns": rejected,
            "pairs": [{"indices": ij, "ports": [FRAME[i] for i in ij],
                       "allowed_labelled_pairs": sorted(allowed)} for ij, allowed in pairs.items()]},
        "two_interior_representative": small, "dihedral_relabellings": dihedral,
        "checks": {"original_port_assignments_examined": 4**8,
                   "new_frame_assignments_examined": 4**5,
                   "small_representative_assignments_examined": 4**5,
                   "direct_projection_source_formula_and_small_graph_agree": True,
                   "complete_joint_fibres_and_full_witnesses_verified": True,
                   "same_sphere_rotation_with_changed_outer_face_verified": True,
                   "verifier_negative_controls_rejected": controls},
        "summary": {"vertices": 15, "edges": 35, "new_internal_vertices": 10,
                    "whole_graph_disk_boundary": True, "mask": mask,
                    "global_s4_orbits": 9, "labelled_assignments": 216,
                    "original_joint_orbits": 60, "catalogue_representative_internal_vertices": 2,
                    "replacement_requires_no_future_contact_with_hidden_vertices": True,
                    "replacement_scope": "Colouring contexts sharing only the named new frame.",
                    "prescribed_transition_legality": "unknown", "new_lean_theorem": False},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved second mixed-frame relation differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
