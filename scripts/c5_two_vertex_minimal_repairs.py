#!/usr/bin/env python3
"""All inclusion-minimal four-port projection repairs of the fixed reverse graph.

Keep P alone as the base, original U, literal colours and complete exclusions.
Reduce by the saved x/y witnesses, enumerate exclusion classes, then expand
every named scope. Independently query all 4^8 assignments for every repair.
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
from c5_two_vertex_mixed_frame import check_hashes
from c5_two_vertex_mixed_pullback import (
    FRAMES, named_pullback, project, verify_rejection,
)
from c5_two_vertex_private_reverse_topology import replay_colouring, source_case
from c5_two_vertex_quaternary_repairs import SCOPES, verify_catalog, verify_witness
from c5_two_vertex_ternary_projections import relation_record


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/quaternary_repairs.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/minimal_repairs.json"
A, T, B = 0, 22, 64


def subsets(items):
    return (s for k in range(len(items) + 1) for s in combinations(items, k))


def union(sets):
    return set().union(*sets)


def relation_hash(rows):
    payload = json.dumps(sorted(rows), separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def verify_classes(classes, cuts):
    groups = {}
    for i, cut in enumerate(cuts):
        groups.setdefault(frozenset(cut), []).append(i)
    expected = [{"class_id": k, "scope_ids": ids,
                 "removed_difference_orbit_ids": sorted(cut)}
                for k, (cut, ids) in enumerate(groups.items())]
    assert classes == expected


def literal_class_minima(classes, universe):
    """Second enumeration: all 256 subsets, without forced A/T or bitmasks."""
    cuts = [set(c["removed_difference_orbit_ids"]) for c in classes]
    result = []
    for chosen in subsets(tuple(range(len(classes)))):
        if union(cuts[i] for i in chosen) == universe and all(
                union(cuts[i] for i in chosen if i != omitted) != universe
                for omitted in chosen):
            result.append(chosen)
    return result


def expand_classes(class_minima, classes):
    # Two scopes with identical full exclusions cannot both be indispensable.
    return sorted((tuple(sorted(ids)) for choice in class_minima
                   for ids in product(*(classes[i]["scope_ids"] for i in choice))),
                  key=lambda ids: (len(ids), ids))


def verify_combinations(records, expected):
    assert [tuple(r["scope_ids"]) for r in records] == expected


def verify_exact_relation(rows, joint):
    assert rows == joint


def verify_deletion(record, scope_ids, joint, pullback, relations, difference):
    omitted = record["omitted_scope_id"]
    assert omitted in scope_ids
    others = tuple(i for i in scope_ids if i != omitted)
    remaining = {row for row in pullback if all(
        project(row, SCOPES[i]) in relations[i] for i in others)}
    assert joint < remaining
    extra = remaining - joint
    ids = [i for i, row in enumerate(difference) if row in extra]
    assert record["remaining_difference_orbit_ids"] == ids
    assert record["remaining_difference_labelled_count"] == len(extra)
    assert record["remaining_relation_labelled_count"] == len(remaining)
    row = tuple(record["witness_pattern"])
    assert row in extra and project(row, SCOPES[omitted]) not in relations[omitted]
    assert record["accepted_remaining_scope_ids"] == list(others)
    assert record["rejecting_scope_ids_within_repair"] == [omitted]


def negative_controls(classes, cuts, repairs, expected, relations, joint,
                      pullback, difference):
    wrong_classes = deepcopy(classes)
    # A and the class of scope 28 each exclude 12 orbits, but different sets.
    wrong_classes[0]["removed_difference_orbit_ids"] = classes[5]["removed_difference_orbit_ids"]
    wrong_scope_order = deepcopy(repairs)
    wrong_scope_order[0]["scope_ids"] = tuple(reversed(wrong_scope_order[0]["scope_ids"]))
    wrong_residual = deepcopy(repairs[0]["deletion_witnesses"][0])
    ids = wrong_residual["remaining_difference_orbit_ids"]
    absent = next(i for i in range(54) if i not in ids)
    wrong_residual["remaining_difference_orbit_ids"] = sorted(ids[1:] + [absent])
    wrong_witness = deepcopy(repairs[0]["deletion_witnesses"][0])
    wrong_witness["witness_pattern"] = tuple(map(int, "01212132"))
    wrong_relation = (joint - {min(joint)}) | {min(pullback - joint)}
    assert len(wrong_relation) == len(joint)
    checks = (
        ("missing_exclusion_class", lambda: verify_classes(classes[:-1], cuts)),
        ("same_size_different_exclusion_set", lambda: verify_classes(wrong_classes, cuts)),
        ("missing_named_scope_expansion", lambda: verify_combinations(repairs[:-1], expected)),
        ("duplicate_named_repair", lambda: verify_combinations(repairs + repairs[:1], expected)),
        ("wrong_scope_order", lambda: verify_combinations(wrong_scope_order, expected)),
        ("nonminimal_superset", lambda: verify_combinations(
            repairs + [{"scope_ids": (0, 22, 64)}], expected)),
        ("same_size_wrong_deletion_residual", lambda: verify_deletion(
            wrong_residual, repairs[0]["scope_ids"], joint, pullback, relations, difference)),
        ("witness_fails_another_retained_scope", lambda: verify_deletion(
            wrong_witness, repairs[0]["scope_ids"], joint, pullback, relations, difference)),
        ("same_size_wrong_repaired_relation", lambda: verify_exact_relation(wrong_relation, joint)),
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
    source, vertices, edges, original_frames, *_ = source_case()
    ports = vertices[:8]
    assert saved["source_case"] == source["name"]
    assert saved["original_graph"] == source["graph"]
    assert saved["identifications"] == source["identifications"]
    assert tuple(saved["ports"]) == ports
    joint, _, _ = replay_colouring(source)
    assert saved["original_joint"] == json.loads(json.dumps(relation_record(joint)))
    frame_indices = tuple(tuple(ports.index(v) for v in frame) for frame in FRAMES)
    frame_relations = [{project(row, scope) for row in joint} for scope in frame_indices]
    pullback = named_pullback(frame_relations, ports)
    assert saved["pullback"] == json.loads(json.dumps(relation_record(pullback)))
    difference = sorted({normalize(row) for row in pullback - joint})
    universe = set(range(len(difference)))
    assert (len(joint), len(pullback), len(difference)) == (1440, 2736, 54)
    catalog = deepcopy(saved["all_70_four_port_projections"])
    # The upstream in-memory verifier uses tuple rows; JSON reload uses lists.
    for record in catalog:
        for key in ("patterns", "labelled_assignments"):
            record["relation"][key] = list(map(tuple, record["relation"][key]))
    verify_catalog(catalog, joint, pullback, ports)
    relations = [{project(row, scope) for row in joint} for scope in SCOPES]
    cuts = [{j for j, row in enumerate(difference) if project(row, scope) not in relation}
            for scope, relation in zip(SCOPES, relations)]
    labelled_cuts = [{row for row in pullback - joint if project(row, scope) not in relation}
                     for scope, relation in zip(SCOPES, relations)]
    classes = [{key: deepcopy(c[key]) for key in (
        "class_id", "scope_ids", "removed_difference_orbit_ids")}
        for c in saved["exclusion_classes"]]
    verify_classes(classes, cuts)
    # Compare complete named exclusion sets, not only orbit counts or representatives.
    assert all((cuts[i] == cuts[j]) == (labelled_cuts[i] == labelled_cuts[j])
               for i in range(70) for j in range(70))
    assert all(len(labelled) == 24 * len(cut) for labelled, cut in zip(labelled_cuts, cuts))
    scope_class = {s: c["class_id"] for c in classes for s in c["scope_ids"]}
    class_cuts = [set(c["removed_difference_orbit_ids"]) for c in classes]
    masks = [sum(1 << j for j in cut) for cut in class_cuts]
    full_mask = (1 << len(difference)) - 1

    witnesses = deepcopy(saved["compact_uniqueness_certificate"]["three_witnesses"])
    for record, label in zip(witnesses, ("x", "y", "z")):
        verify_witness(record, catalog, joint, pullback, vertices, edges)
        record["label"] = label
        old = next(r for r in saved["difference"]["complete_orbit_records"]
                   if r["pattern"] == record["pattern"])
        record["original_graph_rejections"] = deepcopy(old["original_graph_rejections"])
        assert record["original_graph_rejections"]
        for proof in record["original_graph_rejections"]:
            verify_rejection(proof, record["pattern"], ports, edges)
    assert witnesses[0]["rejecting_scope_ids"] == [A]
    assert witnesses[1]["rejecting_scope_ids"] == [T, B]
    edge_scopes = [i for i, scope in enumerate(SCOPES) if {6, 7} <= set(scope)]
    assert witnesses[2]["rejecting_scope_ids"] == edge_scopes
    assert cuts[A] | cuts[B] == universe
    # x forces A. If B occurs, {A,B} already repairs, so minimality forbids extras.
    # Without B, y forces T. Empty exclusions never contribute.
    fixed = tuple(sorted((scope_class[A], scope_class[T])))
    optional = tuple(c["class_id"] for c in classes if c["removed_difference_orbit_ids"]
                     and c["class_id"] not in (*fixed, scope_class[B]))
    assert len(optional) == 4
    reduced_audit, reduced_minima = [], []
    for choice in subsets(optional):
        selected = tuple(sorted((*fixed, *choice)))
        covered = 0
        for i in selected:
            covered |= masks[i]
        missing = full_mask & ~covered
        private = {i: masks[i] & ~sum_mask(masks[j] for j in selected if j != i)
                   for i in selected}
        minimal = missing == 0 and all(private.values())
        reduced_audit.append({"class_ids": selected,
                              "remaining_difference_orbit_ids": bit_ids(missing, len(difference)),
                              "private_difference_orbit_ids_by_class": {
                                  str(i): bit_ids(private[i], len(difference)) for i in selected},
                              "is_exact_repair": missing == 0, "is_inclusion_minimal": minimal})
        if minimal:
            reduced_minima.append(selected)
    class_minima = [tuple(sorted((scope_class[A], scope_class[B])))] + reduced_minima
    exhaustive = literal_class_minima(classes, universe)
    assert sorted(class_minima) == sorted(exhaustive)
    expected = expand_classes(exhaustive, classes)
    assert expected == sorted([(A, B)] + [tuple(sorted((A, T, e))) for e in edge_scopes if e != B],
                              key=lambda ids: (len(ids), ids))

    # No exclusion IDs, orbit masks, or precomputed P-membership in this scan.
    # Every repair is queried on the entire literal domain, then compared as sets.
    domain = tuple(product(range(4), repeat=8))
    assert {row for row in domain if all(project(row, s) in r
            for s, r in zip(frame_indices, frame_relations))} == pullback
    repairs = []
    for ids in expected:
        repaired = {row for row in domain
                    if all(project(row, s) in r for s, r in zip(frame_indices, frame_relations))
                    and all(project(row, SCOPES[i]) in relations[i] for i in ids)}
        verify_exact_relation(repaired, joint)
        deletions = []
        for omitted in ids:
            remaining = {row for row in pullback if all(
                project(row, SCOPES[i]) in relations[i] for i in ids if i != omitted)}
            residual_ids = [j for j, row in enumerate(difference) if row in remaining - joint]
            witness = witnesses[0 if omitted == A else 1 if omitted in (T, B) else 2]
            deletion = {"omitted_scope_id": omitted,
                        "remaining_difference_orbit_ids": residual_ids,
                        "remaining_difference_labelled_count": len(remaining - joint),
                        "remaining_relation_labelled_count": len(remaining),
                        "witness_label": witness["label"], "witness_pattern": witness["pattern"],
                        "accepted_remaining_scope_ids": [i for i in ids if i != omitted],
                        "rejecting_scope_ids_within_repair": [omitted]}
            verify_deletion(deletion, ids, joint, pullback, relations, difference)
            # Every saved residual is also checked by the independent class-mask route.
            assert set(residual_ids) == universe - union(cuts[i] for i in ids if i != omitted)
            deletions.append(deletion)
        repairs.append({"repair_id": len(repairs), "scope_ids": ids,
                        "scopes": [catalog[i]["ports"] for i in ids],
                        "class_ids": sorted(scope_class[i] for i in ids),
                        "projection_count": len(ids), "equals_original_J": True,
                        "repaired_relation_sha256": relation_hash(repaired),
                        "repaired_relation_labelled_count": len(repaired),
                        "deletion_witnesses": deletions})
    verify_combinations(repairs, expected)
    controls = negative_controls(classes, cuts, repairs, expected, relations,
                                 joint, pullback, difference)
    paths = set(saved["source_sha256"]) | {SOURCE, str(Path(__file__).resolve().relative_to(ROOT))}
    distribution = dict(sorted(Counter(len(ids) for ids in expected).items()))
    assert distribution == {2: 1, 3: 14}
    return {
        "schema": "c5-two-vertex-inclusion-minimal-repairs-v1",
        "scope": "Fixed reverse graph; P alone; original U; full four-port projections; named unordered scope sets.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)},
        "source_case": source["name"], "inputs": source["inputs"],
        "identifications": source["identifications"], "ports": ports,
        "original_boundary_maps": original_frames, "original_graph": source["graph"],
        "original_joint": relation_record(joint), "frames": FRAMES,
        "frame_indices": frame_indices, "pullback_labelled_count": len(pullback),
        "pullback_relation_sha256": relation_hash(pullback),
        "relation_hash_encoding": "SHA-256 of json.dumps(sorted(literal tuples), separators=(',', ':')).encode()",
        "difference_orbit_patterns": difference,
        "named_scope_catalog": [{"scope_id": i, "indices": scope,
                                 "ports": catalog[i]["ports"], "class_id": scope_class[i]}
                                for i, scope in enumerate(SCOPES)],
        "complete_exclusion_classes": classes,
        "forced_reduction": {"mandatory_scope_id": A, "if_contains_B": [A, B],
                             "if_omits_B_fixed_scope_ids": [A, T],
                             "optional_nonempty_class_ids": optional},
        "all_16_reduced_class_audits": reduced_audit,
        "all_inclusion_minimal_class_combinations": exhaustive,
        "all_named_inclusion_minimal_repairs": repairs,
        "shared_indispensability_witnesses": witnesses,
        "checks": {"original_graph_assignments_examined": 4**8,
                   "full_domain_base_queries": len(domain),
                   "full_domain_repair_queries": len(domain) * len(repairs),
                   "unrestricted_class_subsets_checked": 2**len(classes),
                   "forced_class_subsets_checked": len(reduced_audit),
                   "complete_named_scope_count": len(SCOPES),
                   "deletion_witnesses_checked": sum(len(r["deletion_witnesses"]) for r in repairs),
                   "original_graph_scope_lifts_rechecked": sum(len(w["accepted_scope_lifts"]) for w in witnesses),
                   "literal_relations_equal_J_for_every_repair": True,
                   "verifier_negative_controls_rejected": controls},
        "summary": {"inclusion_minimal_repairs": len(repairs),
                    "projection_count_distribution": distribution,
                    "full_exclusion_classes": len(classes),
                    "inclusion_minimal_class_combinations": len(exhaustive),
                    "original_J_orbits": 60, "original_J_labelled": len(joint),
                    "new_lean_theorem": False, "general_multistep_sufficiency": "not proved"},
    }


def sum_mask(masks):
    result = 0
    for mask in masks:
        result |= mask
    return result


def bit_ids(mask, n):
    return [i for i in range(n) if mask & (1 << i)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved inclusion-minimal repair certificate differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
