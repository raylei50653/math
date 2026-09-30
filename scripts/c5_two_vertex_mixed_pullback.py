#!/usr/bin/env python3
"""Compare the two saved mixed-frame relations with their original eight-port J.

Keep named colours, complete differences, separate original-graph lifts, and
original-edge rejection proofs. Fixed saved graph only; standard library only.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from boundary_relations import normalize
from c5_two_vertex_join import COLOUR_PERMS, expand
from c5_two_vertex_join_topology import cycle_edges, edge
from c5_two_vertex_mixed_frame import check_hashes
from c5_two_vertex_private_reverse_topology import replay_colouring, source_case


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "artifacts/c5_two_vertex_overlap/mixed_frame_relation.json",
    "artifacts/c5_two_vertex_overlap/second_mixed_frame_relation.json",
)
OUT = ROOT / "artifacts/c5_two_vertex_overlap/mixed_frame_pullback.json"
FRAMES = (("a0", "a4", "a3", "a2", "b2"),
          ("a0", "b4", "b0", "a2", "a1"))
GUARDS = {
    "E": {"ports": ("b2", "b4"), "formula": "b2 != b4"},
    "A": {"ports": ("a0", "a1", "a2", "a3"),
          "formula": "len({a0,a1,a2,a3}) <= 3"},
    "B": {"ports": ("a2", "b4", "b0", "b2"),
          "formula": "a2 != b4 or b0 == b2"},
}


def project(row, indices):
    return tuple(row[i] for i in indices)


def guards(row):
    # U = (a0,a1,a2,a3,a4,b0,b2,b4).
    return {"E": row[6] != row[7], "A": len(set(row[:4])) <= 3,
            "B": row[2] != row[7] or row[5] == row[6]}


def named_pullback(relations, ports):
    """Natural join on literal named colours, without independent renaming."""
    common = tuple(v for v in ports if all(v in frame for frame in FRAMES))
    assert common == ("a0", "a2")
    common_indices = [tuple(frame.index(v) for v in common) for frame in FRAMES]
    buckets = {}
    for q in sorted(relations[1]):
        buckets.setdefault(project(q, common_indices[1]), []).append(q)
    result = set()
    for q in sorted(relations[0]):
        for r in buckets.get(project(q, common_indices[0]), ()):
            colours = dict(zip(FRAMES[0], q))
            for v, c in zip(FRAMES[1], r):
                assert v not in colours or colours[v] == c
                colours[v] = c
            result.add(tuple(colours[v] for v in ports))
    return result


def verify_lift(full, row, indices, vertices, edges):
    assert len(full) == len(vertices) and all(c in range(4) for c in full)
    assert project(full, indices) == project(row, indices)
    colours = dict(zip(vertices, full))
    assert all(colours[u] != colours[v] for u, v in edges)


def verify_rejection(proof, row, ports, edges):
    """Verify local contradictions using only fixed ports and original edges."""
    colours = dict(zip(ports, row))
    for step in proof["forced_steps"]:
        v, ns = step["vertex"], step["original_neighbours"]
        assert v not in colours and len(ns) == len(set(ns))
        assert all(w in colours and edge(v, w) in edges for w in ns)
        available = set(range(4)) - {colours[w] for w in ns}
        assert available == {step["forced_colour"]}
        colours[v] = step["forced_colour"]
    u, v = proof["monochromatic_original_edge"]
    assert edge(u, v) in edges and u in colours and v in colours
    assert colours[u] == colours[v]


def rejection(guard, row, ports, edges):
    if guard == "E":
        recipe, conflict = (), ("b2", "b4")
    elif guard == "A":
        recipe = (("A_inner9", ("a0", "a1", "a2")),
                  ("A_inner5", ("a0", "a2", "A_inner9")),
                  ("A_inner7", ("a0", "a2", "a3")))
        conflict = ("A_inner5", "A_inner7")
    else:
        assert guard == "B"
        recipe = (("B_inner5", ("b0", "b4", "b2")),
                  ("B_inner6", ("b0", "a2", "b2")))
        conflict = ("B_inner5", "B_inner6")
    colours, steps = dict(zip(ports, row)), []
    for v, ns in recipe:
        forced, = set(range(4)) - {colours[w] for w in ns}
        colours[v] = forced
        steps.append({"vertex": v, "original_neighbours": ns, "forced_colour": forced})
    proof = {"failed_guard": guard, "forced_steps": steps,
             "monochromatic_original_edge": conflict}
    verify_rejection(proof, row, ports, edges)
    return proof


def source_formula_a(q):
    proper = all(q[i] != q[(i + 1) % 5] for i in range(5))
    return proper and len(set(q[:4])) <= 3 and len({q[i] for i in (0, 4, 3, 2)}) <= 3


def source_formula_b(q):
    proper = all(q[i] != q[(i + 1) % 5] for i in range(5))
    return proper and q[2] != q[4] and (q[1] != q[4] or q[0] == q[2])


def negative_controls(difference, indices, vertices, edges):
    edge_case = next(d for d in difference if d["failed_guards"] == ["E"])
    a_case = next(d for d in difference if d["failed_guards"] == ["A"])
    b_case = next(d for d in difference if d["failed_guards"] == ["B"])
    bad_force = deepcopy(a_case["original_graph_rejections"][0])
    bad_force["forced_steps"][0]["forced_colour"] = (
        bad_force["forced_steps"][0]["forced_colour"] + 1) % 4
    bad_lift = list(edge_case["separate_frame_lifts"][0]["full_colouring"])
    bad_lift[0] = (bad_lift[0] + 1) % 4
    checks = (
        ("missing_cross_frame_edge_invalidates_edge_rejection",
         lambda: verify_rejection(edge_case["original_graph_rejections"][0],
                                  edge_case["pattern"], vertices[:8],
                                  edges - {edge("b2", "b4")})),
        ("incorrect_forced_colour_is_rejected",
         lambda: verify_rejection(bad_force, a_case["pattern"], vertices[:8], edges)),
        ("missing_B_conflict_edge_invalidates_rejection",
         lambda: verify_rejection(b_case["original_graph_rejections"][0],
                                  b_case["pattern"], vertices[:8],
                                  edges - {edge("B_inner5", "B_inner6")})),
        ("independently_recoloured_shared_port_is_rejected",
         lambda: verify_lift(bad_lift, edge_case["pattern"], indices[0], vertices, edges)),
        ("a_single_frame_lift_is_not_a_joint_lift",
         lambda: verify_lift(edge_case["separate_frame_lifts"][0]["full_colouring"],
                             edge_case["pattern"], tuple(range(8)), vertices, edges)),
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
    record, vertices, edges, original_frames, _, _, pattern_order = source_case()
    ports = vertices[:8]
    assert ports == ("a0", "a1", "a2", "a3", "a4", "b0", "b2", "b4")
    saved = [json.loads((ROOT / p).read_text()) for p in SOURCES]
    relations, indices = [], []
    for data, frame, mask in zip(saved, FRAMES, (255, 1022)):
        check_hashes(data)
        assert data["source_case"] == record["name"]
        assert data["original_graph"] == record["graph"]
        assert data["original_joint"] == record["joint"]
        assert data["identifications"] == record["identifications"]
        assert tuple(data["new_frame"]) == frame
        ix = tuple(ports.index(v) for v in frame)
        assert tuple(data["frame_indices_in_original_ports"]) == ix
        relation = set(map(tuple, data["relation"]["labelled_assignments"]))
        assert data["relation"]["mask"] == mask
        assert relation == expand(data["relation"]["patterns"])
        relations.append(relation)
        indices.append(ix)
    assert set(FRAMES[0]) | set(FRAMES[1]) == set(ports)

    joint, joint_patterns, joint_witnesses = replay_colouring(record)
    assert all({project(row, ix) for row in joint} == relation
               for ix, relation in zip(indices, relations))
    pullback = named_pullback(relations, ports)
    exhaustive = {row for row in product(range(4), repeat=8)
                  if all(project(row, ix) in relation
                         for ix, relation in zip(indices, relations))}
    assert pullback == exhaustive and joint < pullback
    pb_patterns = {normalize(row) for row in pullback}
    extra = pullback - joint
    extra_patterns = {normalize(row) for row in extra}
    assert pullback == expand(pb_patterns) and extra == expand(extra_patterns)
    assert (len(pullback), len(pb_patterns), len(extra), len(extra_patterns)) == (2736, 114, 1296, 54)
    assert joint - pullback == set()
    assert all(len(expand([p])) == 24 for p in pb_patterns)

    covered_edges = cycle_edges(FRAMES[0]) | cycle_edges(FRAMES[1])
    port_edges = {e for e in edges if set(e) <= set(ports)}
    assert covered_edges <= port_edges and port_edges - covered_edges == {edge("b2", "b4")}
    assert all(all(row[ports.index(u)] != row[ports.index(v)] for u, v in covered_edges)
               for row in pullback)

    source_formulas = []
    for side, formula in (("A", source_formula_a), ("B", source_formula_b)):
        mask = record["inputs"][side]["class_id"]
        source_rows = [p for i, p in enumerate(pattern_order) if mask & (1 << i)]
        formula_rows = {q for q in product(range(4), repeat=5) if formula(q)}
        assert formula_rows == expand(source_rows)
        source_formulas.append({"side": side, "ports": original_frames[side], "mask": mask,
                                "patterns": sorted({normalize(q) for q in formula_rows}),
                                "labelled_assignment_count": len(formula_rows)})

    # Use original full graph witnesses, with one common S4 action on all 15 points.
    lifts = [{}, {}]
    for full in sorted(joint_witnesses.values()):
        for permutation in COLOUR_PERMS:
            aligned = tuple(permutation[c] for c in full)
            for bucket, ix in zip(lifts, indices):
                q = project(aligned, ix)
                if q not in bucket or aligned < bucket[q]:
                    bucket[q] = aligned
    assert all(set(bucket) == relation for bucket, relation in zip(lifts, relations))
    difference = []
    for row in sorted(extra_patterns):
        failed = [name for name, passes in guards(row).items() if not passes]
        assert failed
        separate = []
        for frame, ix, bucket in zip(FRAMES, indices, lifts):
            q = project(row, ix)
            full = bucket[q]
            verify_lift(full, row, ix, vertices, edges)
            assert full[:8] in joint and full[:8] != row
            separate.append({"frame": frame, "frame_colours": q, "full_colouring": full,
                             "joint_colouring": full[:8],
                             "changed_original_ports": [v for i, v in enumerate(ports)
                                                        if full[i] != row[i]]})
        rejected_by = [side for side, formula in (("A", source_formula_a), ("B", source_formula_b))
                       if not formula(tuple(row[ports.index(v)] for v in original_frames[side]))]
        assert rejected_by == (["A"] if "A" in failed else []) + (
            ["B"] if "E" in failed or "B" in failed else [])
        difference.append({"pattern": row, "failed_guards": failed,
                           "rejected_by_original_sources": rejected_by,
                           "separate_frame_lifts": separate,
                           "original_graph_rejections": [rejection(g, row, ports, edges) for g in failed]})

    signatures = Counter(tuple(d["failed_guards"]) for d in difference)
    assert signatures == {("E",): 34, ("A",): 6, ("B",): 8, ("E", "A"): 4, ("A", "B"): 2}
    refinements = []
    expected_counts = {(): 114, ("E",): 76, ("A",): 102, ("B",): 104,
                       ("E", "A"): 68, ("E", "B"): 66, ("A", "B"): 94,
                       ("E", "A", "B"): 60}
    for size in range(4):
        for kept in combinations(GUARDS, size):
            refined = {row for row in pullback if all(guards(row)[name] for name in kept)}
            assert joint <= refined and len(refined) == 24 * expected_counts[kept]
            if size == 3:
                assert refined == joint
            spurious = sorted({normalize(row) for row in refined - joint})
            refinements.append({"guards_kept": kept, "global_s4_orbits": len(refined) // 24,
                                "labelled_assignment_count": len(refined), "equals_original_J": refined == joint,
                                "complete_spurious_patterns": spurious})
    irredundancy = []
    for guard in GUARDS:
        example = next(d for d in difference if d["failed_guards"] == [guard])
        irredundancy.append({"omitted_guard": guard, "pattern": example["pattern"],
                             "all_other_guards_pass": True})
    controls = negative_controls(difference, indices, vertices, edges)
    paths = set(SOURCES) | {str(Path(__file__).resolve().relative_to(ROOT))}
    for data in saved:
        paths.update(data["source_sha256"])
    return {
        "schema": "c5-two-vertex-mixed-frame-pullback-v1",
        "scope": "Two full named projections of one saved reverse graph; not a general state theorem.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)},
        "source_case": record["name"], "inputs": record["inputs"],
        "identifications": record["identifications"], "original_boundary_maps": original_frames,
        "original_graph": record["graph"], "original_joint": record["joint"],
        "ports": ports, "frames": FRAMES, "frame_indices": indices,
        "shared_ports": ("a0", "a2"), "covered_original_port_edges": sorted(covered_edges),
        "missing_original_port_edges": sorted(port_edges - covered_edges),
        "pullback": {"formula": "R255(U[0,4,3,2,6]) and R1022(U[0,7,5,2,1])",
                     "patterns": sorted(pb_patterns), "labelled_assignments": sorted(pullback),
                     "global_s4_orbits": len(pb_patterns), "labelled_assignment_count": len(pullback)},
        "difference": {"original_J_minus_pullback": [],
                       "pullback_minus_J_labelled": sorted(extra),
                       "complete_orbit_records": difference,
                       "failure_signature_counts": [{"failed_guards": sig, "global_s4_orbits": count,
                                                     "labelled_assignment_count": 24 * count}
                                                    for sig, count in sorted(signatures.items())]},
        "exact_repair": {"formula": "J(U) iff pullback(U) and E(U) and A(U) and B(U)",
                         "guards": GUARDS, "source_formula_checks": source_formulas,
                         "all_guard_subsets": refinements, "irredundancy_witnesses": irredundancy,
                         "minimal_among_all_possible_summaries": "not claimed"},
        "checks": {"original_graph_assignments_examined": 4**8,
                   "pullback_assignments_examined": 4**8,
                   "source_formula_assignments_examined_each": 4**5,
                   "separate_original_graph_lifts_per_difference_orbit": 2,
                   "all_original_edge_rejection_proofs_verified": True,
                   "verifier_negative_controls_rejected": controls},
        "summary": {"pullback_orbits": 114, "pullback_labelled": 2736,
                    "original_J_orbits": 60, "original_J_labelled": 1440,
                    "spurious_orbits": 54, "spurious_labelled": 1296,
                    "spurious_orbits_after_restoring_original_port_edge": 16,
                    "three_guards_restore_exact_J": True, "new_lean_theorem": False,
                    "general_multistep_sufficiency": "not proved"},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved mixed-frame pullback differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
