#!/usr/bin/env python3
"""Cross-case local projection repair audit of exactly six saved C5 joins.

All whole-graph disk C5 frames on original U, certified by rotations or
alternating crosscuts. Full literal relations, all arities, complete exclusion
sets, exhaustive minimal covers, and original-graph witness lifts. No oracle,
new class-pair search, auxiliary variable, or Lean claim.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from boundary_relations import normalize
from c5_two_vertex_join import (
    CASES, COLOUR_PERMS, expand, graph_extensions, join_relations, source_graph,
)
from c5_two_vertex_join_topology import components, trace_faces

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/eight_point_joins.json"
FRAMES = "artifacts/c5_two_vertex_overlap/repair_transport_frames.json"
PREVIOUS = "artifacts/c5_two_vertex_overlap/minimal_repairs.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/repair_transport.json"
DOMAIN = tuple(product(range(4), repeat=8))


def project(row, scope):
    return tuple(row[i] for i in scope)


def word(row):
    return "".join(map(str, row))


def patterns(rows):
    return sorted({normalize(row) for row in rows})


def relation_hash(rows):
    return sha256(json.dumps(sorted(rows), separators=(",", ":")).encode()).hexdigest()


def relation(rows):
    canonical = patterns(rows)
    assert expand(canonical) == rows
    return {"patterns": list(map(word, canonical)), "global_s4_orbits": len(canonical),
            "labelled_assignment_count": len(rows), "labelled_sha256": relation_hash(rows)}


def check_hashes(saved):
    for path, digest in saved["source_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path


def cycle_edges(cycle):
    return {tuple(sorted(e)) for e in zip(cycle, cycle[1:] + cycle[:1])}


def cycles_on_ports(edges):
    return [p for p in permutations(range(8), 5)
            if p[0] == min(p) and p[1] < p[-1] and cycle_edges(p) <= edges]


def verify_frame_proofs(records, graph):
    n, edges = len(graph["vertices"]), {tuple(e) for e in graph["edges"]}
    adjacency = {i: set() for i in range(n)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert len(components(adjacency)) == 1
    assert [tuple(r["cycle"]) for r in records] == cycles_on_ports(edges)
    for record in records:
        cycle = tuple(record["cycle"])
        if record["available"]:
            rotation = dict(enumerate(tuple(map(tuple, record["rotation"]))))
            assert set(rotation) == set(range(n))
            faces, _ = trace_faces(rotation, edges)
            assert n - len(edges) + len(faces) == 2
            assert any(len(f) == 5 and cycle_edges(f) == cycle_edges(cycle) for f in faces)
        else:
            p, q = map(tuple, record["alternating_paths"])
            assert set(p).isdisjoint(q)
            for path in (p, q):
                assert len(path) >= 2 and len(set(path)) == len(path)
                assert {path[0], path[-1]} <= set(cycle)
                assert set(path[1:-1]).isdisjoint(cycle)
                assert all(tuple(sorted(e)) in edges for e in zip(path, path[1:]))
            endpoints = {p[0], p[-1], q[0], q[-1]}
            labels = [v in (p[0], p[-1]) for v in cycle if v in endpoints]
            assert len(labels) == 4 and all(labels[i] != labels[(i + 1) % 4] for i in range(4))


def reconstruct(case, catalogue, pattern_order):
    """Rebuild the same graph from source representatives, then exhaust colours."""
    graph = case["graph"]
    vertices, ports = graph["vertices"], case["joint"]["ports"]
    assert vertices[:8] == ports and len(set(vertices)) == len(vertices)
    source_edges, rows = {}, {}
    for side in ("A", "B"):
        data = case["inputs"][side]
        n, edges = source_graph(catalogue["cells"][data["source_cell_key"]])
        mapping = graph["source_vertex_maps"][side]
        assert len(mapping) == len(set(mapping)) == n
        assert mapping[:5] == case["boundary_maps"][side]
        assert edges == tuple(map(tuple, graph["source_edges_with_frames"][side]))
        source_edges[side] = {tuple(sorted((vertices.index(mapping[u]), vertices.index(mapping[v]))))
                              for u, v in edges}
        rows[side] = [p for i, p in enumerate(pattern_order) if data["class_id"] & (1 << i)]
    assert set(graph["source_vertex_maps"]["A"]) & set(graph["source_vertex_maps"]["B"]) == {
        a for a, _ in case["identifications"]}
    edges = source_edges["A"] | source_edges["B"]
    assert edges == set(map(tuple, graph["edges"]))
    assert source_edges["A"] & source_edges["B"] == set(map(tuple, graph["shared_edges"]))
    joint, graph_lifts = graph_extensions(len(vertices), sorted(edges), 8)
    assert joint == expand(case["joint"]["patterns"])
    _, joined, map_a, map_b = join_relations(rows["A"], rows["B"],
                                           case["inputs"]["A"]["pair"], case["inputs"]["B"]["pair"])
    assert joint == joined
    assert list(map_a) == case["boundary_maps"]["A"] and list(map_b) == case["boundary_maps"]["B"]
    assert graph_lifts == {tuple(r["pattern"]): tuple(r["colouring"]) for r in graph["witnesses"]}
    # Every literal J tuple has one aligned full colouring; never rename sides separately.
    literal_lifts = {}
    for full in graph_lifts.values():
        for perm in COLOUR_PERMS:
            lifted = tuple(perm[c] for c in full)
            assert all(lifted[u] != lifted[v] for u, v in edges)
            literal_lifts[lifted[:8]] = lifted
    assert set(literal_lifts) == joint
    return joint, graph_lifts, literal_lifts


def minimal_covers(cuts, universe):
    """Exhaust every class subset, not only covers of minimum cardinality."""
    answer = []
    for k in range(len(cuts) + 1):
        for chosen in combinations(range(len(cuts)), k):
            if set().union(*(cuts[i] for i in chosen)) == universe and all(
                    set().union(*(cuts[j] for j in chosen if j != i)) != universe for i in chosen):
                answer.append(chosen)
    return answer


def classify(cuts, difference):
    # Group by the entire literal exclusion set, not its size or a marginal.
    groups = {}
    for i, cut in enumerate(cuts):
        groups.setdefault(frozenset(cut), []).append(i)
    result = []
    for cut, ids in groups.items():
        orbit_ids = [j for j, row in enumerate(difference) if row in cut]
        assert expand(difference[j] for j in orbit_ids) == cut
        result.append({"class_id": len(result), "scope_ids": ids,
                       "removed_difference_orbit_ids": orbit_ids,
                       "removed_labelled_count": len(cut)})
    return result


def verify_classes(classes, cuts, difference):
    assert classes == classify(cuts, difference)


def verify_family(records, expected):
    assert [tuple(r["scope_ids"]) for r in records] == expected


def verify_exact_relation(actual, expected):
    assert actual == expected


def verify_deletion(record, chosen, pullback, joint, scopes, local, difference):
    omitted = record["omitted_scope_id"]
    assert omitted in chosen
    others = tuple(i for i in chosen if i != omitted)
    remaining = {q for q in pullback if all(project(q, scopes[i]) in local[i] for i in others)}
    assert joint < remaining
    extra = remaining - joint
    ids = [i for i, q in enumerate(difference) if q in extra]
    assert record["remaining_difference_orbit_ids"] == ids
    assert record["remaining_labelled_count"] == len(extra)
    row = tuple(map(int, record["witness_pattern"]))
    assert row in extra and project(row, scopes[omitted]) not in local[omitted]


def detect_structure(repairs, scopes, ports, classes):
    sets = [set(r["scope_ids"]) for r in repairs]
    core = set.intersection(*sets)
    if sets == [set()]:
        return {"type": "frame_exact", "forced_scope_ids": []}
    minimum = min(map(len, sets))
    smallest = [s for s in sets if len(s) == minimum]
    if len(core) != 1 or len(smallest) != 1 or minimum != 2:
        return {"type": "other", "forced_scope_ids": sorted(core)}
    a, = core
    b, = smallest[0] - core
    alternatives = [s for s in sets if s != smallest[0]]
    if not alternatives or any(len(s) != 3 for s in alternatives):
        return {"type": "other", "forced_scope_ids": sorted(core)}
    shared = set.intersection(*alternatives)
    if len(shared) != 2 or not core < shared:
        return {"type": "other", "forced_scope_ids": sorted(core)}
    t, = shared - core
    es = sorted(next(iter(s - shared)) for s in alternatives)
    pair = set.intersection(*(set(scopes[i]) for i in es))
    expected_es = [i for i, s in enumerate(scopes) if pair <= set(s) and i != b]
    assert len(pair) == 2 and es == expected_es
    assert sets == [set(r) for r in sorted([(a, b)] + [tuple(sorted((a, t, e))) for e in es],
                                         key=lambda r: (len(r), r))]
    return {"type": "forced_core_alternative_family", "forced_scope_ids": [a],
            "A": a, "B": b, "T": t, "E_scope_ids": es,
            "E_common_pair": [ports[i] for i in sorted(pair)],
            "E_exclusion_class_ids": [c["class_id"] for c in classes if set(c["scope_ids"]) & set(es)]}


def audit_case(case, frame_proofs, catalogue, pattern_order):
    verify_frame_proofs(frame_proofs, case["graph"])
    joint, graph_lifts, lifts = reconstruct(case, catalogue, pattern_order)
    ports = case["joint"]["ports"]
    frame_scopes = [tuple(r["cycle"]) for r in frame_proofs if r["available"]]
    frame_relations = [{project(q, s) for q in joint} for s in frame_scopes]
    pullback = {q for q in DOMAIN if all(project(q, s) in r for s, r in zip(frame_scopes, frame_relations))}
    assert joint <= pullback
    delta = pullback - joint
    difference = patterns(delta)
    all_scopes, all_relations, ladder = {}, {}, []
    for arity in range(9):
        all_scopes[arity] = list(combinations(range(8), arity))
        all_relations[arity] = [{project(q, s) for q in joint} for s in all_scopes[arity]]
        left = {q for q in pullback if all(project(q, s) in r for s, r in
                                         zip(all_scopes[arity], all_relations[arity]))}
        assert joint <= left
        if arity:
            assert left <= previous
        previous = left
        residual_ids = [i for i, q in enumerate(difference) if q in left - joint]
        assert expand(difference[i] for i in residual_ids) == left - joint
        ladder.append({"arity": arity, "scope_count": len(all_scopes[arity]),
                       "remaining_relation_orbits": len(patterns(left)),
                       "remaining_relation_labelled": len(left),
                       "remaining_difference_orbit_ids": residual_ids,
                       "remaining_difference_orbits": len(residual_ids),
                       "remaining_difference_labelled": len(left - joint)})
    rstar = next(r["arity"] for r in ladder if not r["remaining_difference_orbit_ids"])
    scopes, local = all_scopes[rstar], all_relations[rstar]
    cuts = [{q for q in delta if project(q, s) not in r} for s, r in zip(scopes, local)]
    classes = classify(cuts, difference)
    verify_classes(classes, cuts, difference)
    class_cuts = [set(c["removed_difference_orbit_ids"]) for c in classes]
    class_minima = minimal_covers(class_cuts, set(range(len(difference))))
    # Independent literal-set path verifies the entire class enumeration.
    assert class_minima == minimal_covers([cuts[c["scope_ids"][0]] for c in classes], delta)
    expected = sorted((tuple(sorted(ids)) for chosen in class_minima
                       for ids in product(*(classes[i]["scope_ids"] for i in chosen))),
                      key=lambda ids: (len(ids), ids))
    assert len(expected) == len(set(expected))

    lift_cache = {}

    def lift(row, scope):
        if scope not in lift_cache:
            index = {}
            for full in sorted(lifts.values()):
                index.setdefault(project(full, scope), full)
            lift_cache[scope] = index
        full = lift_cache[scope][project(row, scope)]
        assert full[:8] in joint and project(full, scope) == project(row, scope)
        return word(full)

    witness_pool = {}

    def witness(row):
        assert row in delta and normalize(row) == row
        key = word(row)
        if key not in witness_pool:
            rejected = [i for i, s in enumerate(scopes) if project(row, s) not in local[i]]
            witness_pool[key] = {
                "pattern": key, "difference_orbit_id": difference.index(row),
                "rejected_scope_ids": rejected,
                "accepted_scope_lifts": [{"scope_id": i, "full_colouring": lift(row, s)}
                                         for i, s in enumerate(scopes) if i not in rejected],
                "separate_frame_lifts": [lift(row, s) for s in frame_scopes],
                "original_graph_extension_exists": False,
            }
        return key

    lower_witnesses = []
    for row in ladder[:rstar]:
        q = difference[row["remaining_difference_orbit_ids"][0]]
        a = row["arity"]
        lower_witnesses.append({"arity": a, "pattern": witness(q),
                                "all_scope_lifts": [{"indices": s, "full_colouring": lift(q, s)}
                                                    for s in all_scopes[a]]})

    repairs = []
    for ids in expected:
        # Scan the whole literal domain, independent of exclusion classes and P membership.
        repaired = {q for q in DOMAIN
                    if all(project(q, s) in r for s, r in zip(frame_scopes, frame_relations))
                    and all(project(q, scopes[i]) in local[i] for i in ids)}
        verify_exact_relation(repaired, joint)
        deletion = []
        for omitted in ids:
            remaining = {q for q in pullback if all(project(q, scopes[i]) in local[i]
                                                   for i in ids if i != omitted)}
            extra = remaining - joint
            residual_ids = [i for i, q in enumerate(difference) if q in extra]
            record = {"omitted_scope_id": omitted, "remaining_difference_orbit_ids": residual_ids,
                      "remaining_labelled_count": len(extra),
                      "witness_pattern": witness(difference[residual_ids[0]])}
            verify_deletion(record, ids, pullback, joint, scopes, local, difference)
            deletion.append(record)
        repairs.append({"repair_id": len(repairs), "scope_ids": ids,
                        "repaired_relation_equals_J": True, "deletion_witnesses": deletion})
    verify_family(repairs, expected)
    forced = set.intersection(*(set(r) for r in expected))
    forced_records = []
    for i in range(len(scopes)):
        private = cuts[i] - set().union(*(c for j, c in enumerate(cuts) if j != i))
        assert bool(private) == (i in forced)
        if private:
            ids = [j for j, q in enumerate(difference) if q in private]
            q = difference[ids[0]]
            assert [j for j, cut in enumerate(cuts) if q in cut] == [i]
            forced_records.append({"scope_id": i, "all_other_scopes_residual_ids": ids,
                                   "witness_pattern": witness(q)})

    structure = detect_structure(repairs, scopes, ports, classes)
    structural_witnesses = []
    if structure["type"] == "forced_core_alternative_family":
        a, b, t = (structure[k] for k in ("A", "B", "T"))
        edge_scopes = sorted([b] + structure["E_scope_ids"])
        for label, rejectors in (("forced_A", [a]), ("B_or_T", sorted((b, t))),
                                 ("edge_family", edge_scopes)):
            q = next(q for q in difference if [i for i, cut in enumerate(cuts) if q in cut] == rejectors)
            structural_witnesses.append({"role": label, "witness_pattern": witness(q),
                                         "all_rejecting_scope_ids": rejectors})

    controls = negative_controls(frame_proofs, case["graph"], classes, cuts, repairs, expected,
                                 pullback, joint, scopes, local, difference)
    scope_class = {i: c["class_id"] for c in classes for i in c["scope_ids"]}
    minimum = min(map(len, expected))
    result = {
        "name": case["name"], "inputs": case["inputs"], "identifications": case["identifications"],
        "ports": ports, "boundary_maps": case["boundary_maps"],
        "original_graph": {k: v for k, v in case["graph"].items() if k != "witnesses"},
        "original_graph_J_lifts": [{"pattern": word(q), "full_colouring": word(full)}
                                   for q, full in sorted(graph_lifts.items())],
        "frame_proofs": frame_proofs,
        "available_frames": [{"frame_id": i, "indices": s, "ports": [ports[j] for j in s],
                              "relation": relation(r)} for i, (s, r) in enumerate(zip(frame_scopes, frame_relations))],
        "J": relation(joint), "P": relation(pullback), "difference": relation(delta),
        "difference_separate_frame_lifts": [{"pattern": word(q), "full_colourings": [lift(q, s) for s in frame_scopes]}
                                             for q in difference],
        "arity_ladder": ladder, "minimum_sufficient_arity": rstar,
        "lower_arity_witnesses": lower_witnesses,
        "scope_catalog": [{"scope_id": i, "indices": s, "ports": [ports[j] for j in s],
                           "class_id": scope_class[i], "relation": relation(local[i])}
                          for i, s in enumerate(scopes)],
        "complete_exclusion_classes": classes, "inclusion_minimal_class_combinations": class_minima,
        "all_inclusion_minimal_repairs": repairs, "minimum_projection_count": minimum,
        "minimum_repair_ids": [r["repair_id"] for r in repairs if len(r["scope_ids"]) == minimum],
        "repair_size_distribution": dict(sorted(Counter(map(len, expected)).items())),
        "forced_scope_witnesses": forced_records, "witness_pool": list(witness_pool.values()),
        "structure": structure, "structural_witnesses": structural_witnesses,
        "checks": {"graph_assignments": len(DOMAIN), "repair_full_domain_queries": len(DOMAIN) * len(repairs),
                   "class_subsets_per_enumeration": 2**len(classes), "class_enumerations": 2,
                   "deletion_witnesses": sum(len(r["deletion_witnesses"]) for r in repairs),
                   "negative_controls_rejected": controls},
    }
    return result


def negative_controls(frames, graph, classes, cuts, repairs, expected, pullback, joint,
                      scopes, local, difference):
    checks = [("missing_cycle", lambda: verify_frame_proofs(frames[:-1], graph)),
              ("missing_class", lambda: verify_classes(classes[:-1], cuts, difference)),
              ("missing_repair", lambda: verify_family(repairs[:-1], expected)),
              ("duplicate_repair", lambda: verify_family(repairs + repairs[:1], expected))]
    wrong = deepcopy(frames)
    positive = next(r for r in wrong if r["available"])
    positive["rotation"][0].pop()
    checks.append(("missing_rotation_dart", lambda: verify_frame_proofs(wrong, graph)))
    if difference:
        bad_classes = deepcopy(classes)
        i, j = next((i, j) for i, a in enumerate(classes) for j, b in enumerate(classes)
                    if i < j and a["removed_labelled_count"] == b["removed_labelled_count"]
                    and a["removed_difference_orbit_ids"] != b["removed_difference_orbit_ids"])
        bad_classes[i]["removed_difference_orbit_ids"] = classes[j]["removed_difference_orbit_ids"]
        checks.append(("same_size_wrong_exclusions", lambda: verify_classes(bad_classes, cuts, difference)))
        bad_deletion = deepcopy(repairs[0]["deletion_witnesses"][0])
        bad_deletion["witness_pattern"] = word(min(joint))
        checks.append(("J_row_as_indispensability_witness", lambda: verify_deletion(
            bad_deletion, repairs[0]["scope_ids"], pullback, joint, scopes, local, difference)))
        wrong_relation = (joint - {min(joint)}) | {min(pullback - joint)}
        checks.append(("same_size_wrong_repaired_relation", lambda: verify_exact_relation(wrong_relation, joint)))
        wrong_residual = deepcopy(repairs[0]["deletion_witnesses"][0])
        residual = wrong_residual["remaining_difference_orbit_ids"]
        replacement = next(i for i in range(len(difference)) if i not in residual)
        wrong_residual["remaining_difference_orbit_ids"] = sorted(residual[1:] + [replacement])
        checks.append(("same_size_wrong_deletion_residual", lambda: verify_deletion(
            wrong_residual, repairs[0]["scope_ids"], pullback, joint, scopes, local, difference)))
        false_block = deepcopy(frames)
        blocked = next(r for r in false_block if not r["available"])
        blocked["alternating_paths"][1] = blocked["alternating_paths"][0]
        checks.append(("intersecting_crosscuts", lambda: verify_frame_proofs(false_block, graph)))
    rejected = []
    for name, check in checks:
        try:
            check()
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(f"negative control accepted: {name}")
    return rejected


def compare_private(forward, reverse):
    """Distinguish an isomorphic repair family from transport of full relations."""
    def family(case):
        scopes = [frozenset(s["indices"]) for s in case["scope_catalog"]]
        return {frozenset(scopes[i] for i in r["scope_ids"]) for r in case["all_inclusion_minimal_repairs"]}

    f, r = family(forward), family(reverse)
    maps = []
    fj = expand(tuple(map(int, p)) for p in forward["J"]["patterns"])
    rj = expand(tuple(map(int, p)) for p in reverse["J"]["patterns"])
    fp = expand(tuple(map(int, p)) for p in forward["P"]["patterns"])
    rp = expand(tuple(map(int, p)) for p in reverse["P"]["patterns"])
    for perm in permutations(range(8)):
        renamed = {frozenset(frozenset(perm[v] for v in scope) for scope in repair) for repair in f}
        if renamed != r:
            continue

        def move(row):
            out = [0] * 8
            for v, w in enumerate(perm):
                out[w] = row[v]
            return tuple(out)

        moved_j, moved_p = {move(q) for q in fj}, {move(q) for q in fp}
        assert moved_j != rj and moved_p != rp
        q = min(q for q in fj if move(q) not in rj)
        fs = forward["scope_catalog"]
        rs = {frozenset(s["indices"]): s for s in reverse["scope_catalog"]}
        mismatch = next((s, rs[frozenset(perm[v] for v in s["indices"])]) for s in fs
                        if forward["complete_exclusion_classes"][s["class_id"]]["removed_labelled_count"]
                        != reverse["complete_exclusion_classes"][rs[frozenset(perm[v] for v in s["indices"])]["class_id"]]["removed_labelled_count"])
        maps.append({"port_index_map": perm, "repair_family_matches": True,
                     "full_J_matches": False, "full_P_matches": False,
                     "J_transport_failure": {"forward_pattern": word(q), "image_not_in_reverse_J": word(move(q))},
                     "exclusion_transport_failure_scope_ids": [mismatch[0]["scope_id"], mismatch[1]["scope_id"]]})
    assert maps
    return {"same_named_repairs": len(f & r), "forward_only_repairs": len(f - r),
            "reverse_only_repairs": len(r - f), "port_bijections_examined": 40320,
            "all_repair_family_bijections": maps,
            "full_named_exclusion_audits_isomorphic_under_port_bijection": False,
            "shared_formula": "{A,B} and {A,T,E}, with E all r*-scopes containing the saved pair except B",
            "next_step": "conditional common repair lemma for the two nontrivial cases; retain frame-exact as a separate degenerate branch"}


def build():
    saved = json.loads((ROOT / SOURCE).read_text())
    topology = json.loads((ROOT / FRAMES).read_text())
    check_hashes(saved)
    check_hashes(topology)
    assert [c["name"] for c in saved["cases"]] == [spec[0] for spec in CASES]
    assert set(topology["cases"]) == {spec[0] for spec in CASES}
    catalogue = json.loads((ROOT / "artifacts/c5_cells/cells.json").read_text())
    order = tuple(map(tuple, saved["pattern_order"]))
    cases = [audit_case(c, topology["cases"][c["name"]], catalogue, order) for c in saved["cases"]]
    previous = json.loads((ROOT / PREVIOUS).read_text())
    check_hashes(previous)
    reverse = cases[-1]
    assert reverse["J"]["patterns"] == [word(q) for q in previous["original_joint"]["patterns"]]
    assert reverse["P"]["labelled_sha256"] == previous["pullback_relation_sha256"]
    assert reverse["difference"]["patterns"] == [word(q) for q in previous["difference_orbit_patterns"]]
    assert [r["scope_ids"] for r in reverse["all_inclusion_minimal_repairs"]] == [
        tuple(r["scope_ids"]) for r in previous["all_named_inclusion_minimal_repairs"]]
    assert reverse["complete_exclusion_classes"] == [
        {"class_id": c["class_id"], "scope_ids": c["scope_ids"],
         "removed_difference_orbit_ids": c["removed_difference_orbit_ids"],
         "removed_labelled_count": 24 * len(c["removed_difference_orbit_ids"])}
        for c in previous["complete_exclusion_classes"]]
    comparison = compare_private(cases[-2], reverse)
    paths = [SOURCE, FRAMES, PREVIOUS, "scripts/c5_two_vertex_repair_transport.py",
             "scripts/c5_two_vertex_join.py", "scripts/c5_two_vertex_join_topology.py", "scripts/boundary_relations.py"]
    return {"schema": "c5-cross-case-repair-transport-v1",
            "scope": "Exactly six existing graphs; every simple C5 on original U certified available iff whole graph has a disk embedding with it as boundary. P alone; all full r*-projections; no auxiliary vertices.",
            "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "relation_encoding": "Digit strings denote complete global S4 orbits. Expand by all 24 permutations of 0,1,2,3. Counts and hashes use deduplicated literal tuples; never independent local renaming.",
            "hash_encoding": "SHA-256 of json.dumps(sorted(literal tuples), separators=(',', ':')).encode()",
            "zero_arity_convention": "r*=0 iff P=J. The sole empty scope has relation {()} and empty exclusion; the unique minimal repair is the empty set.",
            "cases": cases, "private_case_comparison": comparison,
            "cross_case_matrix": [{"name": c["name"], "candidate_frames": len(c["frame_proofs"]),
                                   "available_frames": len(c["available_frames"]),
                                   "J_orbits": c["J"]["global_s4_orbits"], "P_orbits": c["P"]["global_s4_orbits"],
                                   "difference_orbits": c["difference"]["global_s4_orbits"],
                                   "arity_ladder_residual_orbits": [r["remaining_difference_orbits"] for r in c["arity_ladder"]],
                                   "r_star": c["minimum_sufficient_arity"], "exclusion_classes": len(c["complete_exclusion_classes"]),
                                   "minimum_projection_count": c["minimum_projection_count"],
                                   "minimum_repairs": len(c["minimum_repair_ids"]),
                                   "all_inclusion_minimal_repairs": len(c["all_inclusion_minimal_repairs"]),
                                   "repair_size_distribution": c["repair_size_distribution"],
                                   "forced_scopes": [c["scope_catalog"][r["scope_id"]]["ports"] for r in c["forced_scope_witnesses"]],
                                   "structure": c["structure"]["type"]} for c in cases],
            "summary": {"cases": len(cases), "candidate_frames": sum(len(c["frame_proofs"]) for c in cases),
                        "available_frames": sum(len(c["available_frames"]) for c in cases),
                        "deletion_witnesses": sum(c["checks"]["deletion_witnesses"] for c in cases),
                        "new_class_pairs": 0, "new_lean_theorem": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: saved cross-case audit differs or is missing: {OUT}")
    else:
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
