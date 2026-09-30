#!/usr/bin/env python3
"""Replay all ternary projections of the saved reverse eight-port relation J.

Fixed original graph, literal named colours, complete residual differences and
one original-graph lift for every residual orbit and every three-port scope.
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
from c5_two_vertex_join_topology import edge
from c5_two_vertex_mixed_frame import check_hashes
from c5_two_vertex_mixed_pullback import (
    FRAMES, guards, named_pullback, project, rejection, verify_lift,
    verify_rejection,
)
from c5_two_vertex_private_reverse_topology import replay_colouring, source_case


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/mixed_frame_pullback.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/ternary_projections.json"
TRIPLES = tuple(combinations(range(8), 3))
FOUR_SCOPES = ((0, 1, 2, 3), (2, 5, 6, 7))


def relation_record(rows):
    patterns = {normalize(row) for row in rows}
    assert expand(patterns) == rows
    return {"patterns": sorted(patterns), "labelled_assignments": sorted(rows),
            "global_s4_orbits": len(patterns), "labelled_assignment_count": len(rows)}


def local_edge_relation(scope, ports, edges):
    indices = {ports[i]: j for j, i in enumerate(scope)}
    local_edges = [(indices[u], indices[v]) for u, v in edges
                   if u in indices and v in indices]
    return {q for q in product(range(4), repeat=len(scope))
            if all(q[u] != q[v] for u, v in local_edges)}


def verify_projection(rows, scope, joint):
    assert rows == {project(row, scope) for row in joint}


def verify_residual(record, vertices, edges):
    row = tuple(record["pattern"])
    assert normalize(row) == row
    lifts = record["separate_triple_lifts"]
    assert tuple(tuple(lift["indices"]) for lift in lifts) == TRIPLES
    for lift in lifts:
        scope, full = tuple(lift["indices"]), tuple(lift["full_colouring"])
        assert tuple(lift["ports"]) == tuple(vertices[i] for i in scope)
        assert tuple(lift["colours"]) == project(row, scope)
        verify_lift(full, row, scope, vertices, edges)
        assert full[:8] != row
    assert len(record["separate_frame_lifts"]) == 2
    for lift, frame in zip(record["separate_frame_lifts"], FRAMES):
        scope = tuple(vertices.index(v) for v in frame)
        assert tuple(lift["frame"]) == frame
        verify_lift(lift["full_colouring"], row, scope, vertices, edges)
    failed = [g for g, accepted in guards(row).items() if not accepted]
    assert failed and "E" not in failed and record["failed_guards"] == failed
    assert [p["failed_guard"] for p in record["original_graph_rejections"]] == failed
    for proof in record["original_graph_rejections"]:
        verify_rejection(proof, row, vertices[:8], edges)


def negative_controls(records, triple_relations, joint, vertices, edges):
    example = records[0]
    missing_scope = deepcopy(example)
    missing_scope["separate_triple_lifts"].pop()
    wrong_colour = deepcopy(example)
    lift = wrong_colour["separate_triple_lifts"][0]
    i = lift["indices"][0]
    lift["full_colouring"] = list(lift["full_colouring"])
    lift["full_colouring"][i] = (lift["full_colouring"][i] + 1) % 4
    wrong_edge = deepcopy(example)
    full = list(wrong_edge["separate_triple_lifts"][0]["full_colouring"])
    full[vertices.index("A_inner5")] = full[vertices.index("a0")]
    wrong_edge["separate_triple_lifts"][0]["full_colouring"] = full
    scope = (0, 6, 7)
    incomplete = triple_relations[scope] - {min(triple_relations[scope])}
    spurious = triple_relations[scope] | {(0, 1, 1)}
    checks = (
        ("missing_one_of_56_scopes_is_rejected",
         lambda: verify_residual(missing_scope, vertices, edges)),
        ("changed_named_triple_colour_is_rejected",
         lambda: verify_residual(wrong_colour, vertices, edges)),
        ("monochromatic_original_edge_in_lift_is_rejected",
         lambda: verify_residual(wrong_edge, vertices, edges)),
        ("a_triple_lift_is_not_a_joint_lift",
         lambda: verify_lift(example["separate_triple_lifts"][0]["full_colouring"],
                             example["pattern"], tuple(range(8)), vertices, edges)),
        ("incomplete_projection_is_rejected",
         lambda: verify_projection(incomplete, scope, joint)),
        ("added_nonextendible_projection_tuple_is_rejected",
         lambda: verify_projection(spurious, scope, joint)),
    )
    rejected = []
    for name, check in checks:
        try:
            check()
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(f"negative control was accepted: {name}")
    return rejected


def build():
    saved = json.loads((ROOT / SOURCE).read_text())
    check_hashes(saved)
    source, vertices, edges, original_frames, _, _, _ = source_case()
    ports = vertices[:8]
    assert tuple(saved["ports"]) == ports
    assert saved["source_case"] == source["name"]
    assert saved["original_graph"] == source["graph"]
    assert saved["original_joint"] == source["joint"]
    assert saved["identifications"] == source["identifications"]
    joint, joint_patterns, witnesses = replay_colouring(source)
    frame_indices = tuple(tuple(ports.index(v) for v in frame) for frame in FRAMES)
    assert tuple(map(tuple, saved["frame_indices"])) == frame_indices
    frame_relations = [{project(row, scope) for row in joint} for scope in frame_indices]
    pullback = named_pullback(frame_relations, ports)
    assert pullback == set(map(tuple, saved["pullback"]["labelled_assignments"]))
    assert pullback == expand(saved["pullback"]["patterns"])

    # Compute from the original graph's J, never from guard formulas or P.
    triple_relations, projections = {}, []
    for scope in TRIPLES:
        rows = {project(row, scope) for row in joint}
        local = local_edge_relation(scope, ports, edges)
        assert rows == local
        triple_relations[scope] = rows
        cut = {row for row in pullback if project(row, scope) not in rows}
        scope_ports = tuple(ports[i] for i in scope)
        induced_edges = sorted(e for e in edges if set(e) <= set(scope_ports))
        projections.append({"indices": scope, "ports": scope_ports,
                            "relation": relation_record(rows),
                            "induced_original_edges": induced_edges,
                            "equals_induced_edge_relation": True,
                            "pullback_rows_removed": relation_record(cut)})
    assert len(projections) == 56
    refined = {row for row in pullback
               if all(project(row, s) in r for s, r in triple_relations.items())}
    exhaustive = {row for row in product(range(4), repeat=8)
                  if all(project(row, s) in r for s, r in zip(frame_indices, frame_relations))
                  and all(project(row, s) in r for s, r in triple_relations.items())}
    assert refined == exhaustive
    port_edges = {e for e in edges if set(e) <= set(ports)}
    edge_refined = {row for row in pullback
                    if all(row[ports.index(u)] != row[ports.index(v)] for u, v in port_edges)}
    assert refined == edge_refined == {row for row in pullback if guards(row)["E"]}
    pairs = tuple(combinations(range(8), 2))
    pair_relations = {s: {project(row, s) for row in joint} for s in pairs}
    pair_refined = {row for row in pullback
                    if all(project(row, s) in r for s, r in pair_relations.items())}
    assert refined == pair_refined and joint < refined
    extra = refined - joint
    extra_patterns = {normalize(row) for row in extra}
    assert refined == expand({normalize(row) for row in refined})
    assert extra == expand(extra_patterns) and joint - refined == set()
    assert (len(refined), len(extra), len(extra_patterns)) == (1824, 384, 16)
    assert all(len(expand([row])) == 24 for row in pullback)
    cut_counts = Counter(len(p["pullback_rows_removed"]["patterns"]) for p in projections)
    assert cut_counts == {0: 50, 38: 6}
    for p in projections:
        expected = pullback - refined if {6, 7} <= set(p["indices"]) else set()
        assert set(map(tuple, p["pullback_rows_removed"]["labelled_assignments"])) == expected

    # Apply one shared S4 action to all fifteen vertices, then index literal triples.
    full_by_joint = {}
    for full in sorted(witnesses.values()):
        for permutation in COLOUR_PERMS:
            aligned = tuple(permutation[c] for c in full)
            if aligned[:8] not in full_by_joint or aligned < full_by_joint[aligned[:8]]:
                full_by_joint[aligned[:8]] = aligned
    assert set(full_by_joint) == joint
    buckets = {s: {} for s in TRIPLES}
    for full in sorted(full_by_joint.values()):
        verify_lift(full, full[:8], tuple(range(8)), vertices, edges)
        for scope, bucket in buckets.items():
            bucket.setdefault(project(full, scope), full)
    assert all(set(buckets[s]) == r for s, r in triple_relations.items())
    previous = {tuple(d["pattern"]): d for d in saved["difference"]["complete_orbit_records"]}
    residuals = []
    for row in sorted(extra_patterns):
        lifts = [{"indices": s, "ports": tuple(ports[i] for i in s),
                  "colours": project(row, s), "full_colouring": buckets[s][project(row, s)]}
                 for s in TRIPLES]
        failed = [g for g, accepted in guards(row).items() if not accepted]
        record = {"pattern": row, "failed_guards": failed,
                  "separate_triple_lifts": lifts,
                  "separate_frame_lifts": previous[row]["separate_frame_lifts"],
                  "original_graph_rejections": [rejection(g, row, ports, edges) for g in failed]}
        verify_residual(record, vertices, edges)
        # Check every labelled residual as well as its canonical orbit witness.
        for permutation in COLOUR_PERMS:
            labelled = tuple(permutation[c] for c in row)
            assert labelled in extra
            for lift in lifts:
                aligned = tuple(permutation[c] for c in lift["full_colouring"])
                verify_lift(aligned, labelled, lift["indices"], vertices, edges)
        residuals.append(record)
    failures = Counter(tuple(r["failed_guards"]) for r in residuals)
    assert failures == {("A",): 6, ("B",): 8, ("A", "B"): 2}

    # The second four-port projection also restores the missing original edge.
    four_relations, four_projections = {}, []
    for scope in FOUR_SCOPES:
        rows = {project(row, scope) for row in joint}
        four_relations[scope] = rows
        four_projections.append({"indices": scope, "ports": tuple(ports[i] for i in scope),
                                 "relation": relation_record(rows)})
    repaired = {row for row in refined
                if all(project(row, s) in r for s, r in four_relations.items())}
    direct_repair = {row for row in pullback
                     if all(project(row, s) in r for s, r in four_relations.items())}
    assert repaired == direct_repair == joint
    omissions = []
    for omitted in FOUR_SCOPES:
        kept = {s: r for s, r in four_relations.items() if s != omitted}
        remaining = {row for row in refined
                     if all(project(row, s) in r for s, r in kept.items())}
        assert joint < remaining
        omissions.append({"omitted_scope": omitted,
                          "remaining_spurious": relation_record(remaining - joint)})
    controls = negative_controls(residuals, triple_relations, joint, vertices, edges)
    paths = set(saved["source_sha256"]) | {SOURCE, str(Path(__file__).resolve().relative_to(ROOT))}
    return {
        "schema": "c5-two-vertex-ternary-projections-v1",
        "scope": "One fixed reverse graph; conjunctions of constraints on original named U ports, no auxiliary variables.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)},
        "source_case": source["name"], "inputs": source["inputs"],
        "identifications": source["identifications"], "ports": ports,
        "original_boundary_maps": original_frames,
        "original_graph": source["graph"], "original_joint": relation_record(joint),
        "frames": FRAMES, "frame_indices": frame_indices,
        "pullback": relation_record(pullback), "all_56_triple_projections": projections,
        "ternary_refinement": relation_record(refined),
        "difference": {"original_J_minus_refinement": [],
                       "refinement_minus_J": relation_record(extra),
                       "complete_orbit_records": residuals,
                       "failure_signature_counts": [
                           {"failed_guards": sig, "global_s4_orbits": n,
                            "labelled_assignment_count": 24 * n}
                           for sig, n in sorted(failures.items())]},
        "exact_four_ary_repair": {"base": "P alone; no extra ternary projection needed",
                                  "projections": four_projections,
                                  "equals_original_J": True,
                                  "omission_control_base": "P and all 56 ternary projections of J",
                                  "omission_controls": omissions},
        "checks": {"original_graph_assignments_examined": 4**8,
                   "independent_full_domain_refinement_queries": 4**8,
                   "every_triple_equals_its_induced_original_edge_relation": True,
                   "triple_scopes_redundant_on_P": 50,
                   "triple_scopes_exactly_restoring_b2_b4": 6,
                   "all_pair_refinement_equals_all_triple_refinement": True,
                   "all_original_port_edges_refinement_equals_all_triple_refinement": True,
                   "saved_triple_lifts": len(residuals) * len(TRIPLES),
                   "labelled_triple_lifts_verified": len(extra) * len(TRIPLES),
                   "verifier_negative_controls_rejected": controls},
        "summary": {"original_J_orbits": len(joint_patterns), "original_J_labelled": len(joint),
                    "ternary_refinement_orbits": 76, "ternary_refinement_labelled": len(refined),
                    "spurious_orbits": len(extra_patterns), "spurious_labelled": len(extra),
                    "all_ternary_projections_suffice": False,
                    "minimum_added_constraint_arity_on_original_ports": 4,
                    "new_lean_theorem": False, "general_multistep_sufficiency": "not proved"},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved ternary projection certificate differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
