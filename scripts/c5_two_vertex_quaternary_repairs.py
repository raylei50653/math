#!/usr/bin/env python3
"""Certify all minimum four-port projection repairs of the fixed mixed pullback.

Original named ports and one shared colour frame; no auxiliary variables.
Rebuild J from original edges, retain all 70 projections and all 2,415 pairs.
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
from c5_two_vertex_join import COLOUR_PERMS
from c5_two_vertex_mixed_frame import check_hashes
from c5_two_vertex_mixed_pullback import (
    FRAMES, guards, named_pullback, project, rejection, verify_lift,
)
from c5_two_vertex_private_reverse_topology import replay_colouring, source_case
from c5_two_vertex_ternary_projections import relation_record


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/ternary_projections.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/quaternary_repairs.json"
SCOPES = tuple(combinations(range(8), 4))
PAIRS = tuple(combinations(range(len(SCOPES)), 2))


def verify_catalog(records, joint, pullback, ports):
    assert tuple(tuple(r["indices"]) for r in records) == SCOPES
    difference = sorted({normalize(row) for row in pullback - joint})
    for i, record in enumerate(records):
        scope = SCOPES[i]
        assert record["scope_id"] == i
        assert tuple(record["ports"]) == tuple(ports[j] for j in scope)
        rows = {project(row, scope) for row in joint}
        assert record["relation"] == relation_record(rows)
        remaining = {row for row in pullback - joint if project(row, scope) in rows}
        ids = [j for j, row in enumerate(difference) if row in remaining]
        assert record["remaining_difference_orbit_ids"] == ids
        assert record["remaining_labelled_count"] == len(remaining)
        assert record["removed_difference_orbit_ids"] == [j for j in range(54) if j not in ids]


def verify_pairs(records, minimum_pairs, catalog, joint, pullback, difference):
    assert tuple(tuple(r["scope_ids"]) for r in records) == PAIRS
    # Independent literal-colour intersection, compared to the orbit-bitset audit.
    relations = [set(map(tuple, r["relation"]["labelled_assignments"])) for r in catalog]
    survivors = [{row for row in pullback - joint if project(row, scope) in relation}
                 for scope, relation in zip(SCOPES, relations)]
    exact = []
    for record, (a, b) in zip(records, PAIRS):
        remaining = survivors[a] & survivors[b]
        patterns = {normalize(row) for row in remaining}
        ids = [i for i, row in enumerate(difference) if row in patterns]
        assert record["remaining_difference_orbit_ids"] == ids
        assert record["remaining_labelled_count"] == len(remaining)
        assert record["equals_original_J"] == (not remaining)
        if not remaining:
            exact.append((a, b))
    assert tuple(map(tuple, minimum_pairs)) == tuple(exact)
    assert joint < pullback and all(survivors) and exact


def verify_witness(record, catalog, joint, pullback, vertices, edges):
    row = tuple(record["pattern"])
    assert normalize(row) == row and row in pullback - joint
    relations = [set(map(tuple, p["relation"]["labelled_assignments"])) for p in catalog]
    rejected = [i for i, scope in enumerate(SCOPES) if project(row, scope) not in relations[i]]
    assert record["rejecting_scope_ids"] == rejected
    lifts = record["accepted_scope_lifts"]
    assert [lift["scope_id"] for lift in lifts] == [i for i in range(70) if i not in rejected]
    for lift in lifts:
        scope = SCOPES[lift["scope_id"]]
        assert tuple(lift["ports"]) == tuple(vertices[i] for i in scope)
        assert tuple(lift["colours"]) == project(row, scope)
        verify_lift(lift["full_colouring"], row, scope, vertices, edges)
        assert tuple(lift["full_colouring"][:8]) != row


def negative_controls(catalog, pair_records, minimum_pairs, witnesses,
                      joint, pullback, difference, vertices, edges):
    def catalog_check(records):
        verify_catalog(records, joint, pullback, vertices[:8])

    def pairs_check(records, minima=minimum_pairs):
        verify_pairs(records, minima, catalog, joint, pullback, difference)

    def witness_check(record):
        verify_witness(record, catalog, joint, pullback, vertices, edges)

    wrong_ports = deepcopy(catalog)
    wrong_ports[0]["ports"] = tuple(reversed(wrong_ports[0]["ports"]))
    missing_tuple = deepcopy(catalog)
    missing_tuple[0]["relation"]["labelled_assignments"].pop()
    added_tuple = deepcopy(catalog)
    added_tuple[0]["relation"]["labelled_assignments"].append((0, 1, 2, 3))
    wrong_coverage = deepcopy(pair_records)
    ids = wrong_coverage[0]["remaining_difference_orbit_ids"]
    absent = next(i for i in range(len(difference)) if i not in ids)
    wrong_coverage[0]["remaining_difference_orbit_ids"] = sorted(ids[1:] + [absent])
    wrong_lift = deepcopy(witnesses[0])
    full = list(wrong_lift["accepted_scope_lifts"][0]["full_colouring"])
    full[vertices.index("A_inner5")] = full[vertices.index("a0")]
    wrong_lift["accepted_scope_lifts"][0]["full_colouring"] = full
    checks = (
        ("missing_one_of_70_scopes", lambda: catalog_check(catalog[:-1])),
        ("wrong_named_scope_order", lambda: catalog_check(wrong_ports)),
        ("missing_legal_projection_tuple", lambda: catalog_check(missing_tuple)),
        ("added_nonextendible_projection_tuple", lambda: catalog_check(added_tuple)),
        ("same_size_but_wrong_residual_set", lambda: pairs_check(wrong_coverage)),
        ("missing_one_of_2415_pairs", lambda: pairs_check(pair_records[:-1])),
        ("omitted_minimum_repair", lambda: pairs_check(pair_records, [])),
        ("spurious_minimum_repair", lambda: pairs_check(pair_records, minimum_pairs + [(0, 1)])),
        ("original_edge_conflict_in_scope_lift", lambda: witness_check(wrong_lift)),
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
    assert saved["identifications"] == source["identifications"]
    joint, _, original_witnesses = replay_colouring(source)
    assert saved["original_joint"] == json.loads(json.dumps(relation_record(joint)))
    frame_indices = tuple(tuple(ports.index(v) for v in frame) for frame in FRAMES)
    frame_relations = [{project(row, scope) for row in joint} for scope in frame_indices]
    pullback = named_pullback(frame_relations, ports)
    assert saved["pullback"] == json.loads(json.dumps(relation_record(pullback)))
    extra = pullback - joint
    difference = sorted({normalize(row) for row in extra})
    assert joint < pullback and (len(difference), len(extra)) == (54, 1296)
    catalog, relations, masks, cut_sets = [], [], [], []
    for i, scope in enumerate(SCOPES):
        rows = {project(row, scope) for row in joint}
        cut = {row for row in extra if project(row, scope) not in rows}
        cut_ids = [j for j, row in enumerate(difference) if row in cut]
        relations.append(rows)
        cut_sets.append(cut)
        masks.append(sum(1 << j for j in cut_ids))
        catalog.append({"scope_id": i, "indices": scope,
                        "ports": tuple(ports[j] for j in scope),
                        "relation": relation_record(rows),
                        "removed_difference_orbit_ids": cut_ids,
                        "remaining_difference_orbit_ids": [j for j in range(54) if j not in cut_ids],
                        "remaining_labelled_count": len(extra - cut)})
    verify_catalog(catalog, joint, pullback, ports)
    groups = {}
    for i, mask in enumerate(masks):
        groups.setdefault(mask, []).append(i)
    assert Counter((len(ids), mask.bit_count()) for mask, ids in groups.items()) == Counter({
        (1, 12): 2, (51, 0): 1, (1, 4): 1, (13, 38): 1,
        (1, 20): 1, (1, 48): 1, (1, 44): 1,
    })
    cut_classes = [{"class_id": i, "scope_ids": ids,
                    "removed_difference": relation_record(cut_sets[ids[0]]),
                    "removed_difference_orbit_ids": catalog[ids[0]]["removed_difference_orbit_ids"]}
                   for i, ids in enumerate(groups.values())]
    for record in cut_classes:
        assert all(cut_sets[i] == cut_sets[record["scope_ids"][0]] for i in record["scope_ids"])
    full_mask = (1 << len(difference)) - 1
    pairs, minimum_pairs = [], []
    for a, b in PAIRS:
        remainder = full_mask & ~(masks[a] | masks[b])
        ids = [i for i in range(len(difference)) if remainder & (1 << i)]
        pairs.append({"scope_ids": (a, b), "remaining_difference_orbit_ids": ids,
                      "remaining_labelled_count": 24 * len(ids),
                      "equals_original_J": not ids})
        if not ids:
            minimum_pairs.append((a, b))
    verify_pairs(pairs, minimum_pairs, catalog, joint, pullback, difference)
    assert minimum_pairs == [(0, 64)]
    assert tuple(SCOPES[i] for i in minimum_pairs[0]) == ((0, 1, 2, 3), (2, 5, 6, 7))
    # A second construction scans all literal assignments, including those outside P.
    repaired = {row for row in product(range(4), repeat=8)
                if all(project(row, s) in r for s, r in zip(frame_indices, frame_relations))
                and all(project(row, SCOPES[i]) in relations[i] for i in minimum_pairs[0])}
    assert repaired == joint

    difference_records = []
    for j, row in enumerate(difference):
        rejectors = [i for i, scope in enumerate(SCOPES) if project(row, scope) not in relations[i]]
        assert rejectors == [i for i, mask in enumerate(masks) if mask & (1 << j)]
        failures = [g for g, accepted in guards(row).items() if not accepted]
        difference_records.append({"orbit_id": j, "pattern": row,
                                   "rejecting_scope_ids": rejectors,
                                   "original_graph_rejections": [rejection(g, row, ports, edges)
                                                                  for g in failures]})
    essential = [i for i in range(70)
                 if any(r["rejecting_scope_ids"] == [i] for r in difference_records)]
    assert essential == [0]
    exclusive = [r["pattern"] for r in difference_records if r["rejecting_scope_ids"] == [0]]
    assert len(exclusive) == 4

    # Three rows prove mandatory A, the two possible partners, then reject the wrong partner.
    selected = [min(r["pattern"] for r in difference_records if r["rejecting_scope_ids"] == [0]),
                min(r["pattern"] for r in difference_records if r["rejecting_scope_ids"] == [22, 64]),
                min(r["pattern"] for r in difference_records
                    if 0 not in r["rejecting_scope_ids"] and 22 not in r["rejecting_scope_ids"])]
    assert selected == [tuple(map(int, s)) for s in ("01232112", "01212132", "01012122")]
    aligned_full = sorted({tuple(permutation[c] for c in full)
                           for full in original_witnesses.values() for permutation in COLOUR_PERMS})
    assert {full[:8] for full in aligned_full} == joint
    buckets = [{} for _ in SCOPES]
    for full in aligned_full:
        verify_lift(full, full[:8], tuple(range(8)), vertices, edges)
        for scope, bucket in zip(SCOPES, buckets):
            bucket.setdefault(project(full, scope), full)
    assert all(set(bucket) == rows for bucket, rows in zip(buckets, relations))
    witnesses = []
    for row in selected:
        rejectors = [i for i, s in enumerate(SCOPES) if project(row, s) not in relations[i]]
        lifts = [{"scope_id": i, "ports": tuple(ports[j] for j in scope),
                  "colours": project(row, scope), "full_colouring": buckets[i][project(row, scope)]}
                 for i, scope in enumerate(SCOPES) if i not in rejectors]
        record = {"pattern": row, "rejecting_scope_ids": rejectors, "accepted_scope_lifts": lifts}
        verify_witness(record, catalog, joint, pullback, vertices, edges)
        for permutation in COLOUR_PERMS:
            labelled = tuple(permutation[c] for c in row)
            assert labelled in extra
            for lift in lifts:
                full = tuple(permutation[c] for c in lift["full_colouring"])
                verify_lift(full, labelled, SCOPES[lift["scope_id"]], vertices, edges)
        witnesses.append(record)
    controls = negative_controls(catalog, pairs, minimum_pairs, witnesses,
                                 joint, pullback, difference, vertices, edges)
    paths = set(saved["source_sha256"]) | {SOURCE, str(Path(__file__).resolve().relative_to(ROOT))}
    return {
        "schema": "c5-two-vertex-quaternary-repairs-v1",
        "scope": "Fixed reverse graph; P alone plus full four-port projections of J on original U; no auxiliary variables.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)},
        "source_case": source["name"], "inputs": source["inputs"],
        "identifications": source["identifications"], "ports": ports,
        "original_boundary_maps": original_frames, "original_graph": source["graph"],
        "original_joint": relation_record(joint), "frames": FRAMES,
        "frame_indices": frame_indices, "pullback": relation_record(pullback),
        "difference": {"relation": relation_record(extra), "complete_orbit_records": difference_records},
        "all_70_four_port_projections": catalog, "exclusion_classes": cut_classes,
        "all_2415_pair_audits": pairs,
        "minimum_repairs": [{"scope_ids": pair,
                             "scopes": [catalog[i]["ports"] for i in pair],
                             "remaining_difference_orbit_ids": []} for pair in minimum_pairs],
        "compact_uniqueness_certificate": {
            "mandatory_scope_ids_in_every_four_projection_repair": essential,
            "all_exclusive_rejection_patterns_for_mandatory_scope": exclusive,
            "three_witnesses": witnesses,
            "possible_second_scope_ids_after_second_witness": [22, 64],
            "third_witness_rules_out_second_scope_id": 22,
        },
        "checks": {"original_graph_assignments_examined": 4**8,
                   "independent_full_domain_repair_queries": 4**8,
                   "four_port_scopes_checked": len(catalog), "pairs_checked": len(pairs),
                   "single_projection_exact_repairs": sum(cut == extra for cut in cut_sets),
                   "literal_pair_intersections_equal_orbit_bitsets": True,
                   "saved_scope_lifts": sum(len(w["accepted_scope_lifts"]) for w in witnesses),
                   "labelled_scope_lifts_verified": 24 * sum(len(w["accepted_scope_lifts"]) for w in witnesses),
                   "verifier_negative_controls_rejected": controls},
        "summary": {"four_port_scopes": 70, "exclusion_classes": len(groups),
                    "minimum_projection_count": 2, "minimum_combination_count": len(minimum_pairs),
                    "unique_minimum_scope_ids": minimum_pairs[0],
                    "original_J_orbits": 60, "original_J_labelled": len(joint),
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
            raise SystemExit(f"FAIL: saved quaternary repair certificate differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
