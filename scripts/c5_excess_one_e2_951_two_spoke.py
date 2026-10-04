#!/usr/bin/env python3
"""E2 951 t=2: joint contact-palette tables and named nonplanar path controls.

The paper argument treats arbitrary original unary/binary pieces. The finite
checks below certify the joint tables and explicit graphs, not a source search.
"""

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_excess_one_e2_951_three_spoke as shared


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_excess_one_e2_951_two_spoke/observations.json"
CELLS = ROOT / "artifacts/c5_cells/cells.json"
U, D, B = shared.U, shared.D, shared.B
Q, P = shared.Q, shared.P


def orientation_controls():
    far_rows = ((1, P), (2, (0, 1, 2, 0, 1)))
    pair_records = []
    for singleton, far in far_rows:
        valid = [pair for pair in combinations(B, 2)
                 if len({Q[v] for v in pair}) == 2 and len({far[v] for v in pair}) == 2]
        nonadjacent = [pair for pair in valid if (pair[1] - pair[0]) % 5 in (2, 3)]
        assert nonadjacent == [(singleton, 4)]
        pair_records.append({"far_singleton_position": singleton,
                             "ordered_Q": list(Q), "ordered_far_P": list(far),
                             "joint_injective_root_spoke_pairs": [list(xs) for xs in valid],
                             "joint_injective_nonadjacent_pairs": [list(xs) for xs in nonadjacent]})
    phi = tuple((3 - v) % 5 for v in B)
    q_permutation, p_permutation = (1, 0, 2, 3), (0, 2, 1, 3)
    source_p = far_rows[1][1]
    def transport(row, permutation):
        result = [None] * 5
        for v in B:
            result[phi[v]] = permutation[row[v]]
        return tuple(result)
    assert transport(Q, q_permutation) == Q
    assert transport(source_p, p_permutation) == P
    assert sorted(phi[v] for v in (2, 4)) == [1, 4]
    assert sorted(phi[v] for v in (2, 3, 4)) == [0, 1, 4]
    assert [phi[v] for v in (4, 0, 1, 2)] == [4, 3, 2, 1]
    assert q_permutation[1] == p_permutation[0] == 0
    assert q_permutation[D] == p_permutation[D] == D
    tuple_records = []
    avoid_checks = 0
    for frame, permutation in (("whole_Q_frame", q_permutation), ("whole_P_frame", p_permutation)):
        for arity in (1, 2):
            for values in product(U, repeat=arity):
                mapped = tuple(permutation[c] for c in values)
                for colour in U:
                    assert (colour in values) == (permutation[colour] in mapped)
                    avoid_checks += 1
                tuple_records.append({"frame": frame, "ordered_original_tuple": list(values),
                                      "globally_transported_tuple": list(mapped)})
    return {"joint_root_spoke_pair_controls": pair_records,
            "source24_far2_to_target14_far1": {
                "one_common_geometric_boundary_map": list(phi),
                "source_Q": list(Q), "source_P": list(source_p),
                "whole_Q_colour_permutation": list(q_permutation),
                "whole_P_colour_permutation": list(p_permutation),
                "target_Q": list(Q), "target_P": list(P),
                "source_root_spokes": [2, 4], "target_root_spokes": [1, 4],
                "source_short_actual_support": [2, 3, 4], "target_short_actual_support": [0, 1, 4],
                "source_long_actual_boundary_arc": [4, 0, 1, 2],
                "target_long_actual_boundary_arc": [4, 3, 2, 1],
                "source_short_forbidden_Q_P": [[1], [0]],
                "target_short_forbidden_Q_P": [[0], [0]],
                "source_and_target_long_forbidden_Q_P": [[D], [D]],
                "source_long_binary_short_unary_maps_to_case": "II",
                "source_long_unary_short_binary_maps_to_case": "IV",
                "scope": "Each colour permutation acts on its whole original graph colouring and all ordered piece tuples; no independent piece normalisation."},
            "all_unary_binary_tuple_transport_controls": tuple_records,
            "tuple_colour_membership_preservation_checks": avoid_checks}


def joint_tables(root_colour):
    rows = ((root_colour, *Q[1:]), (root_colour, *P[1:]))
    records = []
    for size in range(1, 5):
        for roles in combinations(range(5), size):
            records.append({
                "actual_exterior_roles": list(roles),
                "original_root_contact": 0 in roles,
                "degree_C": 4 - size,
                "joint_tight": all(len({row[v] for v in roles}) == size for row in rows),
                "joint_residual_lists": [sorted(set(U) - {row[v] for v in roles}) for row in rows],
            })
    noncontact_pairs = [r for r in records if r["degree_C"] == 2 and
                        not r["original_root_contact"] and r["joint_tight"]]
    contact_pairs = [r for r in records if r["degree_C"] == 2 and
                     r["original_root_contact"] and r["joint_tight"]]
    signature = lambda r: tuple(tuple(xs) for xs in r["joint_residual_lists"])
    assert len({signature(r) for r in noncontact_pairs}) == 4
    assert not {signature(r) for r in noncontact_pairs} & {signature(r) for r in contact_pairs}
    noncontact_leaf = [r for r in records if r["degree_C"] == 1 and
                       not r["original_root_contact"] and r["joint_tight"]]
    contact_leaf = [r for r in records if r["degree_C"] == 1 and
                    r["original_root_contact"] and r["joint_tight"]]
    contact_singleton = [r for r in records if r["degree_C"] == 0 and
                         r["original_root_contact"] and r["joint_tight"]]
    assert not noncontact_leaf
    assert not contact_singleton
    if root_colour == 0:
        assert [r["actual_exterior_roles"] for r in contact_pairs] == [[0, 1], [0, 4]]
        assert [r["joint_residual_lists"] for r in contact_pairs] == [
            [[2, 3], [2, 3]], [[1, 3], [1, 3]]]
        assert [r["actual_exterior_roles"] for r in contact_leaf] == [[0, 1, 4]]
        assert contact_leaf[0]["joint_residual_lists"] == [[3], [3]]
    else:
        assert root_colour == D and len(contact_leaf) == 4
        assert all(all(D not in xs for xs in r["joint_residual_lists"])
                   for r in contact_pairs)
    # K4 private points have exactly one exterior neighbour; the root's joint
    # palette also differs from every single actual boundary neighbour palette.
    contact_k4 = [r for r in records if r["degree_C"] == 3 and
                  r["original_root_contact"] and r["joint_tight"]]
    noncontact_k4 = [r for r in records if r["degree_C"] == 3 and
                     not r["original_root_contact"] and r["joint_tight"]]
    assert not {signature(r) for r in contact_k4} & {signature(r) for r in noncontact_k4}
    return {"root_pinned_colour": root_colour,
            "joint_sector_rows": [list(row) for row in rows],
            "all_local_exterior_subset_tests": records,
            "noncontact_odd_cycle_private_supports": noncontact_pairs,
            "contact_odd_cycle_private_supports": contact_pairs,
            "contact_and_noncontact_joint_palettes_disjoint": True,
            "joint_tight_contact_bridge_leaves": contact_leaf,
            "joint_tight_noncontact_bridge_leaves": 0,
            "joint_tight_one_contact_singletons": 0,
            "contact_and_noncontact_K4_private_palettes_disjoint": True,
            "scope": "Exact local attachment tests; terminal-block and arbitrary-size deductions remain paper arguments."}


def path_control(name, internal_pairs):
    root, quartet = 5, 6
    path = tuple(range(7, 9 + 2 * len(internal_pairs)))
    vertices = tuple(range(9 + 2 * len(internal_pairs)))
    edges = set(shared.CYCLE)
    edges.update((b, root) for b in (1, 4))
    edges.add((root, quartet))
    edges.update((b, quartet) for b in (0, 1, 4))
    edges.update(zip(path, path[1:]))
    edges.update((root, v) for v in (path[0], path[-1]))
    for v in (path[0], path[-1]):
        edges.update((b, v) for b in (1, 4))
    for i, pair in enumerate(internal_pairs):
        edges.update((b, v) for v in path[1+2*i:3+2*i] for b in pair)
    return {"name": name, "vertices": vertices,
            "edges": tuple(sorted(tuple(sorted(e)) for e in edges)),
            "root": root, "quartet_piece": quartet,
            "original_long_path": path, "original_contact_order": [path[0], path[-1]],
            "internal_paired_actual_supports": internal_pairs}


def k5_control(graph, pair_index):
    vertices, edges = graph["vertices"], graph["edges"]
    pair = graph["internal_paired_actual_supports"][pair_index]
    a, b = pair
    u, v = graph["original_long_path"][1+2*pair_index:3+2*pair_index]
    H_rest = sorted(set(vertices) - set(B) - {u, v})
    if pair == (1, 4):
        bags = [[u], [v], [0, 1], [4], sorted(set(H_rest) | {2, 3})]
        method = "pair14: full support places b2,b3 on the remaining long piece"
    else:
        assert b == a + 1
        bags = [[u], [v], [a], [b], sorted(set(H_rest) | (set(B) - {a, b}))]
        method = "adjacent pair: actual root-quartet-b0 path connects the complementary frame arc"
    assert all(not set(xs) & set(ys) for xs, ys in combinations(bags, 2))
    branch_sets = [{"name": f"X{i}", "vertices": sorted(bag),
                    "all_source_connecting_paths": shared.connected_paths(bag, vertices, edges)}
                   for i, bag in enumerate(bags)]
    links = []
    for i, j in combinations(range(5), 2):
        xs, ys = set(bags[i]), set(bags[j])
        source = next((list(e) for e in edges if
                       (e[0] in xs and e[1] in ys) or (e[0] in ys and e[1] in xs)), None)
        assert source is not None
        links.append({"target_edge": [f"X{i}", f"X{j}"], "actual_source_edge": source})
    assert (5, 6) in edges and (0, 6) in edges
    return {"graph_name": graph["name"], "selected_pair_index": pair_index,
            "selected_private_vertices": [u, v], "actual_boundary_pair": list(pair),
            "actual_root_to_b0_path_through_original_quartet": [5, 6, 0],
            "remaining_original_H_connecting_paths": shared.connected_paths(H_rest, vertices, edges),
            "method": method, "five_K5_branch_sets": branch_sets,
            "ten_K5_edges_with_actual_source_witnesses": links}


def complete_control(graph, reps, full_rows):
    vertices, edges = graph["vertices"], graph["edges"]
    adjacency = shared.adjacency(vertices, edges)
    degrees = [[v, len(adjacency[v])] for v in vertices if v >= 5]
    assert degrees[0] == [5, 5] and all(degree == 4 for _, degree in degrees[1:])
    assert all(any(v >= 5 for v in adjacency[b]) for b in B)
    canonical = []
    mask = 0
    for i, row in enumerate(reps):
        witness = shared.colouring(vertices, edges, dict(enumerate(row)))
        if witness is not None:
            mask |= 1 << i
        canonical.append({"pattern_index": i, "ordered_boundary_row": list(row),
                          "complete_colouring": None if witness is None else list(witness)})
    assert mask == 942
    accepted = []
    for row in full_rows:
        actual = shared.colouring(vertices, edges, dict(enumerate(row))) is not None
        assert actual == bool(mask & (1 << reps.index(shared.normalize(row))))
        if actual:
            accepted.append("".join(map(str, row)))
    deletions = []
    for edge in edges:
        if edge in shared.CYCLE:
            continue
        child = tuple(e for e in edges if e != edge)
        child_mask = 0
        additions = []
        for i, row in enumerate(reps):
            witness = shared.colouring(vertices, child, dict(enumerate(row)))
            if witness is not None:
                child_mask |= 1 << i
                if not mask & (1 << i):
                    additions.append({"pattern_index": i, "ordered_boundary_row": list(row),
                                      "complete_colouring": list(witness)})
        assert mask | child_mask == child_mask and child_mask != mask
        assert all(child_mask & (1 << reps.index(row)) for row in (Q, P))
        deletions.append({"original_edge": list(edge), "child_complete_sigma": child_mask,
                          "all_added_boundary_row_witnesses": additions})
    long_path = graph["original_long_path"]
    contacts = graph["original_contact_order"]
    piece_relations = []
    for row in (Q, P):
        # Remove both root-spokes and all quartet incidences before querying the
        # long piece's literal ordered contacts. The root is not normalised.
        long_edges = tuple(e for e in edges if 5 not in e and 6 not in e)
        tuples = []
        for x, y in product(U, repeat=2):
            pins = dict(enumerate(row))
            pins.update(zip(contacts, (x, y)))
            witness = shared.colouring((*B, *long_path), long_edges, pins)
            if witness is not None:
                tuples.append({"ordered_original_contact_tuple": [x, y],
                               "complete_long_piece_colouring": list(witness)})
        forbidden = sorted(set.intersection(*(set(t["ordered_original_contact_tuple"]) for t in tuples)))
        assert forbidden == [0]
        quartet_tuples = []
        quartet_edges = tuple(e for e in edges if e in shared.CYCLE or 6 in e and 5 not in e)
        for colour in U:
            pins = dict(enumerate(row))
            pins[6] = colour
            witness = shared.colouring((*B, 6), quartet_edges, pins)
            if witness is not None:
                quartet_tuples.append({"ordered_original_contact_tuple": [colour],
                                       "complete_quartet_piece_colouring": list(witness)})
        assert [t["ordered_original_contact_tuple"] for t in quartet_tuples] == [[D]]
        piece_relations.append({"ordered_boundary_row": list(row),
                                "long_original_contact_order": contacts,
                                "long_complete_ordered_contact_relation": tuples,
                                "long_forbidden_root_colours": forbidden,
                                "quartet_original_contact_order": [6],
                                "quartet_complete_ordered_contact_relation": quartet_tuples,
                                "quartet_forbidden_root_colours": [D]})
    return {"name": graph["name"], "vertices": list(vertices), "edges": [list(e) for e in edges],
            "ordered_boundary": list(B), "root": 5, "root_spokes": [1, 4],
            "original_quartet_vertices": [6], "quartet_actual_support": [0, 1, 4],
            "actual_root_to_b0_path_through_quartet": [5, 6, 0],
            "original_long_path": list(long_path), "long_original_contact_order": contacts,
            "paired_noncontact_supports": [list(pair) for pair in graph["internal_paired_actual_supports"]],
            "interior_full_degrees": degrees, "epsilon": 1,
            "complete_sigma": mask, "canonical_row_colouring_witnesses": canonical,
            "all_240_ordered_boundary_rows_checked": len(full_rows),
            "complete_accepted_ordered_boundary_rows": accepted,
            "all_nonframe_edge_deletion_certificates": deletions,
            "original_piece_relations_at_Q_and_P": piece_relations,
            "scope": "Named case-I algebraic controls. Stored K5 minors show nonplanarity, so these are not disk counterexamples or a source enumeration."}


def build():
    cells = json.loads(CELLS.read_text())
    reps = [tuple(row) for row in cells["pattern_order"]]
    assert cells["singleton_of_three_colour"] == {"0": 4, "1": 3, "3": 2, "4": 1, "6": 0}
    full_rows = tuple(row for row in product(U, repeat=5)
                      if all(row[v] != row[(v + 1) % 5] for v in B))
    assert len(full_rows) == 240
    graphs = [path_control("L4_inner_pair23_quartet_unary_D", ((2, 3),)),
              path_control("L6_inner_pairs12_34_quartet_unary_D", ((1, 2), (3, 4))),
              path_control("L6_inner_pairs23_14_quartet_unary_D", ((2, 3), (1, 4)))]
    minors = [k5_control(graphs[0], 0), k5_control(graphs[1], 0),
              k5_control(graphs[1], 1), k5_control(graphs[2], 1)]
    controls = [complete_control(graph, reps, full_rows) for graph in graphs]
    shared_table = shared.tight_table()
    own = Path(__file__).resolve()
    dependency = ROOT / "scripts/c5_excess_one_e2_951_three_spoke.py"
    return {"schema": 1,
            "scope": "E2 951 t=2 root-spokes14: two joint pinned-root tables, symbolic contact/noncontact palette separation, first-cycle entries, and three named nonplanar binary-long-piece controls. Arbitrary-size unary/binary exclusion remains the accompanying paper proof; no new Lean theorem or disk-source enumeration.",
            "sha256": {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
                       for path in (own, dependency, CELLS)},
            "provenance": {"ordered_original_boundary": list(B), "root_spokes": ["b1", "b4"],
                           "original_Q_singleton_b4": list(Q), "original_P_singleton_b1": list(P),
                           "joint_long_sector_role_order": ["r", "b1", "b2", "b3", "b4"],
                           "quartet_actual_support": ["b0", "b1", "b4"],
                           "quartet_Q_restriction": [0, 1, 2], "quartet_P_restriction": [0, 1, 2],
                           "same_original_quartet_relation_at_Q_and_P": True,
                           "four_paper_cases": [
                               {"case": "I", "long_original_contacts": 2, "long_forbidden_root_colour": 0,
                                "quartet_original_contacts": 1, "quartet_forbidden_root_colour": D},
                               {"case": "II", "long_original_contacts": 2, "long_forbidden_root_colour": D,
                                "quartet_original_contacts": 1, "quartet_forbidden_root_colour": 0},
                               {"case": "III", "long_original_contacts": 1, "long_forbidden_root_colour": 0,
                                "quartet_original_contacts": 2, "quartet_forbidden_root_colour": D},
                               {"case": "IV", "long_original_contacts": 1, "long_forbidden_root_colour": D,
                                "quartet_original_contacts": 2, "quartet_forbidden_root_colour": 0}]},
            "pattern_order": [list(row) for row in reps],
            "named_orientation_and_whole_graph_colour_transport_controls": orientation_controls(),
            "joint_pinned_root_attachment_tables": [joint_tables(0), joint_tables(D)],
            "noncontact_initial_bridge_chain_A": shared_table["initial_bridge_chain_non_D_states"],
            "initial_bridge_D_state": [D, D],
            "first_internal_odd_cycle_entry_controls": shared_table["first_internal_odd_cycle_entry_controls"],
            "K5_controls_with_actual_quartet_paths": minors,
            "complete_graph_controls": controls,
            "summary": {"joint_root_pin_tables": 2, "root0_contact_odd_cycle_palette_types": 2,
                        "far_row_nonadjacent_spoke_orientation_controls": 2,
                        "whole_graph_tuple_transport_colour_checks": 160,
                        "root0_contact_bridge_leaf_types": 1, "joint_tight_noncontact_bridge_leaf_types": 0,
                        "joint_tight_one_contact_singletons": 0, "first_internal_cycle_entry_checks": 8,
                        "named_K5_minors": len(minors), "named_complete_graph_controls": len(controls),
                        "full_ordered_boundary_row_checks": len(controls) * len(full_rows),
                        "control_masks": [g["complete_sigma"] for g in controls],
                        "control_long_orders": [len(g["original_long_path"]) for g in controls],
                        "nonframe_edge_deletion_checks": sum(len(g["all_nonframe_edge_deletion_certificates"]) for g in controls)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        assert OUT.read_text() == data, "certificate differs; rebuild only this new certificate explicitly"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
