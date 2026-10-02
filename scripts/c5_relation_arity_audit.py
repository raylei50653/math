#!/usr/bin/env python3
"""Projection arity of saved C5 relations and six existing named joins.

No new graph/class-pair search. Literal colours share one global S4 frame.
The 20 five-ary catalogue counterexamples are replayed against original edges;
the six joins retain their saved, independently checked disk-frame proofs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from boundary_relations import normalize
from c5_two_vertex_join import expand, graph_extensions, source_graph
from c5_two_vertex_repair_transport import reconstruct, verify_frame_proofs

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = "artifacts/c5_cells/cells.json"
JOINS = "artifacts/c5_two_vertex_overlap/eight_point_joins.json"
TRANSPORT = "artifacts/c5_two_vertex_overlap/repair_transport.json"
OUT = ROOT / "artifacts/c5_relation_arity/observations.json"
COLOURS = range(4)
PERMS = tuple(permutations(COLOURS))


def project(row, scope):
    return tuple(row[i] for i in scope)


def words(rows):
    return sorted({"".join(map(str, normalize(row))) for row in rows})


def digest(rows):
    return sha256(json.dumps(sorted(rows), separators=(",", ":")).encode()).hexdigest()


def closure(relation, domain, n, arity):
    scopes = tuple(combinations(range(n), arity))
    views = [{project(row, scope) for row in relation} for scope in scopes]
    return {row for row in domain if all(
        project(row, scope) in view for scope, view in zip(scopes, views))}


def build():
    catalogue = json.loads((ROOT / CATALOGUE).read_text())
    patterns = tuple(map(tuple, catalogue["pattern_order"]))
    pattern_index = {row: i for i, row in enumerate(patterns)}
    domain5 = set(product(COLOURS, repeat=5))
    proper5 = {row for row in domain5 if all(row[i] != row[(i + 1) % 5] for i in range(5))}
    assert len(proper5) == 240 and expand(patterns) == proper5
    t4 = sum(1 << i for i, row in enumerate(patterns) if len(set(row)) == 4)
    assert t4 == 932

    def relation(mask):
        return expand(row for i, row in enumerate(patterns) if mask & (1 << i))

    def d5_orbit(mask):
        return sorted({sum(1 << pattern_index[normalize(tuple(row[(a + s*i) % 5]
                         for i in range(5)))]
                         for j, row in enumerate(patterns) if mask & (1 << j))
                       for a in range(5) for s in (-1, 1)})

    # All Boolean masks are a relation-algebra control, not graph realizations.
    failures, t4_controls = [], []
    for mask in range(1024):
        rel = relation(mask)
        residue = closure(rel, domain5, 5, 4) - rel
        if residue:
            failures.append(mask)
        if mask & t4 == t4:
            assert not residue
            t4_controls.append(mask)

    records, arities = [], {}
    scopes4 = tuple(combinations(range(5), 4))
    for mask in sorted(map(int, catalogue["cells"])):
        rel = relation(mask)
        current = domain5
        ladder, before_exact = [], None
        for arity in range(1, 6):
            previous = current
            current = closure(rel, current, 5, arity)
            assert rel <= current <= previous
            ladder.append(len(current - rel))
            if current == rel and mask not in arities:
                arities[mask] = arity
                before_exact = previous - rel
        record = {"class_id": mask, "k_eff": catalogue["cells"][str(mask)]["k_eff"],
                  "minimum_arity": arities[mask],
                  "residual_labelled_counts_arity_1_to_5": ladder,
                  "relation_sha256": digest(rel),
                  "lower_arity_counterexample": min(before_exact)}
        if arities[mask] == 5:
            n, edges = source_graph(catalogue["cells"][str(mask)])
            actual, lifts = graph_extensions(n, edges, 5)
            assert actual == rel  # original edges, independent of mask evaluator
            literal_lifts = {}
            for full in sorted(lifts.values()):
                for perm in PERMS:
                    lifted = tuple(perm[c] for c in full)
                    literal_lifts.setdefault(lifted[:5], lifted)
            assert set(literal_lifts) == rel
            rejected = min(before_exact)
            assert rejected not in actual
            witnesses = []
            for scope in scopes4:
                extension = min(row for row in rel if project(row, scope) == project(rejected, scope))
                full = literal_lifts[extension]
                assert all(full[u] != full[v] for u, v in edges)
                assert project(full, scope) == project(rejected, scope)
                witnesses.append({"scope": scope, "full_graph_colouring": full})
            record["five_ary_graph_counterexample"] = {
                "vertices": list(range(n)), "edges_with_frame": edges,
                "rejected_boundary": rejected,
                "all_four_scope_graph_lifts": witnesses,
                "four_closure_extra_orbits": words(before_exact),
                "disk_status": "inherited from catalogue; no new planarity check"}
        records.append(record)

    assert Counter(arities.values()) == {2: 11, 4: 101, 5: 20}
    five = sorted(mask for mask, arity in arities.items() if arity == 5)
    orbit_reps = sorted({min(d5_orbit(mask)) for mask in five})
    assert orbit_reps == [223, 383, 509, 511]
    assert all(set(d5_orbit(mask)) <= set(five) for mask in five)

    saved_joins = json.loads((ROOT / JOINS).read_text())
    saved_transport = json.loads((ROOT / TRANSPORT).read_text())
    by_name = {case["name"]: case for case in saved_transport["cases"]}
    domain8 = set(product(COLOURS, repeat=8))
    joined_records = []
    for case in saved_joins["cases"]:
        saved = by_name[case["name"]]
        joint, _, _ = reconstruct(case, catalogue, patterns)
        assert joint == expand(tuple(map(int, word)) for word in saved["J"]["patterns"])
        verify_frame_proofs(saved["frame_proofs"], case["graph"])
        frames = [tuple(record["cycle"]) for record in saved["frame_proofs"] if record["available"]]
        views = [{project(row, frame) for row in joint} for frame in frames]
        pullback = {row for row in domain8 if all(project(row, frame) in view
                    for frame, view in zip(frames, views))}
        assert joint <= pullback and digest(pullback) == saved["P"]["labelled_sha256"]
        ports = case["joint"]["ports"]
        source_scopes = [tuple(ports.index(v) for v in case["boundary_maps"][side])
                         for side in ("A", "B")]
        source_views = [{project(row, scope) for row in joint} for scope in source_scopes]
        rebuilt = {row for row in domain8 if all(project(row, scope) in view
                   for scope, view in zip(source_scopes, source_views))}
        assert rebuilt == joint
        bound = max(arities[case["inputs"][side]["class_id"]] for side in ("A", "B"))
        current = pullback
        ladder = [len(words(current - joint))]
        for arity in range(1, 6):
            current = closure(joint, current, 8, arity)
            ladder.append(len(words(current - joint)))
        r_star = next(i for i, residual in enumerate(ladder) if residual == 0)
        assert r_star <= bound <= 5
        assert ladder == [row["remaining_difference_orbits"] for row in saved["arity_ladder"][:6]]
        joined_records.append({"name": case["name"], "ports": ports,
                               "source_scopes": source_scopes,
                               "source_class_ids": [case["inputs"][side]["class_id"] for side in ("A", "B")],
                               "available_frames": frames, "J_sha256": digest(joint),
                               "P_sha256": digest(pullback), "source_arity_upper_bound": bound,
                               "residual_orbits_arity_0_to_5": ladder, "r_star": r_star})

    paths = [CATALOGUE, JOINS, TRANSPORT, "scripts/c5_relation_arity_audit.py",
             "scripts/boundary_relations.py", "scripts/c5_two_vertex_join.py",
             "scripts/c5_two_vertex_repair_transport.py", "scripts/c5_two_vertex_join_topology.py"]
    return {"schema": "c5-relation-arity-v1",
            "scope": "132 saved source relations, 1024 abstract masks, 20 original-graph counterexamples, six existing named joins; no new class pairs or disk realizability theorem",
            "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "definition": "d(S) is the least r such that all r-coordinate projections reconstruct S in the full literal 4^5 domain; repair r* is relative to the certified frame pullback P",
            "catalogue": records, "five_ary_classes": five,
            "five_ary_d5_orbits": [{"representative": m, "members": d5_orbit(m)} for m in orbit_reps],
            "abstract_four_arity_failures": failures,
            "T4_containing_masks_checked": t4_controls,
            "nonrealizability_controls": {str(mask): {"four_decomposable": mask not in failures,
                "meaning": "relation algebra does not exclude this unknown disk candidate"} for mask in (933, 941)},
            "existing_joins": joined_records,
            "summary": {"catalogue_classes": len(records), "source_arity_distribution": dict(sorted(Counter(arities.values()).items())),
                        "five_ary_d5_orbits": len(orbit_reps), "original_graph_counterexamples": len(five),
                        "four_scope_full_graph_lifts": 5 * len(five), "abstract_masks": 1024,
                        "abstract_four_arity_failures": len(failures), "T4_masks_checked": len(t4_controls),
                        "existing_joins": len(joined_records), "new_class_pairs": 0,
                        "new_lean_theorems": 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved arity audit differs or is missing: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
