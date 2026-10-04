#!/usr/bin/env python3
"""E2: joint tight lists and named K5 controls for the 951 three-spoke branch.

The arbitrary-size Gallai leaf/path argument is a paper proof. This checker
certifies its small attachment table and four explicit nonplanar controls;
it does not enumerate disk sources or use the four-colour theorem.
"""

import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_excess_one_e2_951_three_spoke/observations.json"
CELLS = ROOT / "artifacts/c5_cells/cells.json"
U = (0, 1, 2, 3)
D = 3
B = tuple(range(5))
CYCLE = tuple(sorted(tuple(sorted((v, (v + 1) % 5))) for v in B))
Q = (0, 1, 0, 1, 2)  # singleton b4
P = (0, 1, 2, 0, 2)  # singleton b1
DELTA = (3, 1, 0, 1, 2)  # (r,b1,b2,b3,b4), outer row Q, r=D
DELTA_PRIME = (3, 1, 2, 0, 2)  # same roles and colour frame, outer P, r=D


def normalize(row):
    rename = {}
    return tuple(rename.setdefault(c, len(rename)) for c in row)


def adjacency(vertices, edges):
    result = {v: [] for v in vertices}
    for u, v in edges:
        result[u].append(v)
        result[v].append(u)
    return {v: tuple(sorted(result[v])) for v in vertices}


def colouring(vertices, edges, pinned):
    """Direct deterministic backtracking; no planarity or 4CT oracle."""
    neighbours = adjacency(vertices, edges)
    colours = dict(pinned)
    if any(u in colours and v in colours and colours[u] == colours[v]
           for u, v in edges):
        return None

    def extend():
        if len(colours) == len(vertices):
            return tuple(colours[v] for v in vertices)
        choices = []
        for v in vertices:
            if v not in colours:
                seen = {colours[w] for w in neighbours[v] if w in colours}
                allowed = tuple(c for c in U if c not in seen)
                choices.append((len(allowed), -len(neighbours[v]), v, allowed))
        _, _, v, allowed = min(choices)
        for c in allowed:
            colours[v] = c
            witness = extend()
            if witness is not None:
                return witness
        colours.pop(v, None)
        return None

    witness = extend()
    if witness is not None:
        actual = dict(zip(vertices, witness))
        assert all(actual[v] == c for v, c in pinned.items())
        assert all(actual[u] != actual[v] for u, v in edges)
    return witness


def tight_table():
    records = []
    for size in range(1, 4):
        for support in combinations(range(5), size):
            tight = (len({DELTA[v] for v in support}) == size and
                     len({DELTA_PRIME[v] for v in support}) == size)
            records.append({
                "exterior_roles": list(support),
                "root_contact": 0 in support,
                "degree_C": 4 - size,
                "joint_tight": tight,
                "lists": [sorted(set(U) - {row[v] for v in support})
                          for row in (DELTA, DELTA_PRIME)],
            })
    pairs = [r for r in records if len(r["exterior_roles"]) == 2 and
             not r["root_contact"] and r["joint_tight"]]
    assert [r["exterior_roles"] for r in pairs] == [[1, 2], [1, 4], [2, 3], [3, 4]]
    signatures = [tuple(tuple(xs) for xs in r["lists"]) for r in pairs]
    assert len(set(signatures)) == 4
    triples = [r for r in records if len(r["exterior_roles"]) == 3 and
               not r["root_contact"]]
    assert all(not r["joint_tight"] for r in triples)
    endpoints = [r for r in records if len(r["exterior_roles"]) == 3 and
                 r["root_contact"] and r["joint_tight"]]
    assert [r["exterior_roles"] for r in endpoints] == [
        [0, 1, 2], [0, 1, 4], [0, 2, 3], [0, 3, 4]]
    assert all(all(len(xs) == 1 and D not in xs for xs in r["lists"])
               for r in endpoints)
    transition_records = []
    for pair, endpoint in zip(pairs, endpoints):
        non_d = [next(c for c in xs if c != D) for xs in pair["lists"]]
        assert non_d == [xs[0] for xs in endpoint["lists"]]
        assert all(set(xs) == {D, c} for xs, c in zip(pair["lists"], non_d))
        transition_records.append({
            "actual_boundary_pair": pair["exterior_roles"],
            "endpoint_edge_palette_pair": non_d,
            "next_edge_palette_pair": [D, D],
            "internal_list_pair": pair["lists"],
        })
    endpoint_states = {tuple(xs[0] for xs in r["lists"]) for r in endpoints}
    boundary_states = {(DELTA[v], DELTA_PRIME[v]) for v in range(1, 5)}
    assert endpoint_states == {(2, 0), (0, 0), (2, 1), (0, 1)}
    assert boundary_states == {(1, 1), (0, 2), (1, 0), (2, 2)}
    assert not boundary_states & (endpoint_states | {(D, D)})
    first_cycle_entry = []
    for pair in pairs:
        valid_attachments = []
        for boundary_role in range(1, 5):
            cut_lists = [set(U) - {row[boundary_role]}
                         for row in (DELTA, DELTA_PRIME)]
            if not all(set(palette) <= cut_list
                       for palette, cut_list in zip(pair["lists"], cut_lists)):
                continue
            incoming = [sorted(cut_list - set(palette))
                        for palette, cut_list in zip(pair["lists"], cut_lists)]
            assert all(len(xs) == 1 for xs in incoming)
            state = tuple(xs[0] for xs in incoming)
            assert state in boundary_states
            assert state not in endpoint_states | {(D, D)}
            valid_attachments.append(boundary_role)
            first_cycle_entry.append({
                "private_actual_boundary_pair": pair["exterior_roles"],
                "odd_cycle_joint_block_palette": pair["lists"],
                "entry_cut_actual_boundary_neighbour": boundary_role,
                "entry_cut_residual_lists": [sorted(xs) for xs in cut_lists],
                "forced_incoming_bridge_palette_pair": list(state),
                "compatible_with_initial_bridge_chain": False,
            })
        assert valid_attachments == pair["exterior_roles"]
    # A terminal private vertex has the whole block palette as its list.
    # Uniform D membership therefore permits only all/no private contacts.
    terminal = []
    for block, minimum_private in (("bridge", 1), ("triangle", 2),
                                   ("odd_cycle_length_at_least_5", 4), ("K4", 3)):
        configurations = []
        for contact_count in range(minimum_private + 1):
            uniform = contact_count in (0, minimum_private)
            within_two_contacts = contact_count <= 2
            configurations.append({"private_contact_count": contact_count,
                                   "uniform_D_membership": uniform,
                                   "within_two_original_contacts": within_two_contacts,
                                   "allowed_by_these_two_tests": uniform and within_two_contacts})
        terminal.append({"block": block, "minimum_private_vertices": minimum_private,
                         "finite_minimum_count_tests": configurations})
    return {"exterior_subset_table": records,
            "noncontact_pair_palette_signatures_are_injective": True,
            "noncontact_bridge_leaf_triples_joint_tight": 0,
            "paired_path_transitions": transition_records,
            "initial_bridge_chain_non_D_states": [list(xs) for xs in sorted(endpoint_states)],
            "initial_bridge_chain_D_state": [D, D],
            "first_internal_odd_cycle_entry_controls": first_cycle_entry,
            "first_internal_cycle_palette_disjointness": True,
            "terminal_block_minimum_count_tests": terminal,
            "scope": "Local subsets and symbolic minimum-count controls; Gallai decomposition, leaf exclusion, and arbitrary path alternation are paper steps."}


def path_graph(name, pairs):
    r = 5
    contacts_path = tuple(range(6, 6 + 2 * len(pairs)))
    vertices = tuple(range(6 + len(contacts_path)))
    edges = set(CYCLE)
    edges.update(tuple(sorted(e)) for e in zip(contacts_path, contacts_path[1:]))
    edges.update((r, v) for v in (contacts_path[0], contacts_path[-1]))
    edges.update((b, r) for b in (0, 1, 4))
    for i, pair in enumerate(pairs):
        edges.update((b, v) for v in contacts_path[2*i:2*i+2] for b in pair)
    return {"name": name, "vertices": vertices, "edges": tuple(sorted(edges)),
            "root": r, "original_contact_order": [contacts_path[0], contacts_path[-1]],
            "original_C_path": contacts_path, "paired_actual_supports": pairs}


def connected_paths(bag, vertices, edges):
    bag = tuple(sorted(bag))
    allowed = set(bag)
    neighbours = adjacency(vertices, edges)
    root = bag[0]
    paths = {root: (root,)}
    queue = deque([root])
    while queue:
        v = queue.popleft()
        for w in neighbours[v]:
            if w in allowed and w not in paths:
                paths[w] = (*paths[v], w)
                queue.append(w)
    assert set(paths) == allowed
    return [{"vertex": v, "source_path": list(paths[v])} for v in bag]


def minor_control(graph, pair_index):
    vertices, edges = graph["vertices"], graph["edges"]
    r = graph["root"]
    a, b = graph["paired_actual_supports"][pair_index]
    u, v = graph["original_C_path"][2*pair_index:2*pair_index+2]
    remaining_H = sorted((set(graph["original_C_path"]) | {r}) - {u, v})
    if (a, b) == (1, 4):
        bags = [[u], [v], [1, 0], [4], sorted(set(remaining_H) | {2, 3})]
        reason = "pair14; B-touch connects b2,b3 to remaining_H"
    else:
        assert b == a + 1
        bags = [[u], [v], [a], [b], sorted(set(remaining_H) | (set(B) - {a, b}))]
        reason = "adjacent pair; rb0 connects remaining_H to complementary frame path"
    assert all(not set(xs) & set(ys) for xs, ys in combinations(bags, 2))
    bag_records = [{"name": f"X{i}", "vertices": sorted(xs),
                    "source_connecting_paths": connected_paths(xs, vertices, edges)}
                   for i, xs in enumerate(bags)]
    target_edges = []
    for i, j in combinations(range(5), 2):
        xs, ys = set(bags[i]), set(bags[j])
        witnesses = [list(e) for e in edges if
                     (e[0] in xs and e[1] in ys) or (e[1] in xs and e[0] in ys)]
        assert witnesses
        target_edges.append({"target_edge": [f"X{i}", f"X{j}"],
                             "source_edge": witnesses[0]})
    return {"actual_pair": [a, b], "selected_private_vertices": [u, v],
            "remaining_H_connecting_paths": connected_paths(remaining_H, vertices, edges),
            "reason": reason, "K5_branch_sets": bag_records,
            "ten_target_edges_with_actual_source_edges": target_edges}


def graph_relation(graph, reps, full_rows):
    vertices, edges = graph["vertices"], graph["edges"]
    rows = []
    mask = 0
    for i, row in enumerate(reps):
        witness = colouring(vertices, edges, dict(enumerate(row)))
        if witness is not None:
            mask |= 1 << i
        rows.append({"pattern_index": i, "ordered_boundary_row": list(row),
                     "complete_colouring": None if witness is None else list(witness)})
    accepted = []
    for row in full_rows:
        witness = colouring(vertices, edges, dict(enumerate(row)))
        expected = bool(mask & (1 << reps.index(normalize(row))))
        assert (witness is not None) == expected
        if expected:
            accepted.append("".join(map(str, row)))
    assert mask == 942
    neighbours = adjacency(vertices, edges)
    interior_degrees = [[v, len(neighbours[v])] for v in vertices if v >= 5]
    assert interior_degrees[0] == [5, 5]
    assert all(degree == 4 for _, degree in interior_degrees[1:])
    assert set(B) == {b for b in B if any(v >= 5 for v in neighbours[b])}
    deletions = []
    for edge in edges:
        if edge in CYCLE:
            continue
        child = tuple(e for e in edges if e != edge)
        child_mask = 0
        additions = []
        for i, row in enumerate(reps):
            witness = colouring(vertices, child, dict(enumerate(row)))
            if witness is not None:
                child_mask |= 1 << i
                if not mask & (1 << i):
                    additions.append({"pattern_index": i, "ordered_boundary_row": list(row),
                                      "complete_colouring": list(witness)})
        assert child_mask | mask == child_mask and child_mask != mask
        assert all(child_mask & (1 << reps.index(row)) for row in (Q, P))
        deletions.append({"original_edge": list(edge), "child_complete_sigma": child_mask,
                          "all_added_row_witnesses": additions})
    # The two binary contacts and complete, ordered tuples share the same frame.
    contacts = graph["original_contact_order"]
    C_vertices = graph["original_C_path"]
    C_edges = tuple(e for e in edges if 5 not in e)
    tuples = []
    for row in (Q, P):
        relation = []
        for x, y in product(U, repeat=2):
            pinned = dict(enumerate(row))
            pinned.update(zip(contacts, (x, y)))
            witness = colouring((*B, *C_vertices), C_edges, pinned)
            if witness is not None:
                relation.append({"ordered_contact_tuple": [x, y],
                                 "complete_C_witness": list(witness)})
        bans = sorted(set.intersection(*(set(t["ordered_contact_tuple"]) for t in relation)))
        assert bans == [D]
        tuples.append({"ordered_boundary_row": list(row), "ordered_contacts": contacts,
                       "complete_ordered_contact_relation_with_witnesses": relation,
                       "forbidden_root_colours": bans})
    return {"name": graph["name"], "vertices": list(vertices), "edges": [list(e) for e in edges],
            "ordered_boundary": list(B), "root": 5, "root_spokes": [0, 1, 4],
            "original_C_path": list(C_vertices), "original_contact_order": contacts,
            "paired_actual_supports": [list(xs) for xs in graph["paired_actual_supports"]],
            "interior_full_degrees": interior_degrees, "epsilon": 1,
            "complete_sigma": mask, "canonical_row_witnesses": rows,
            "all_240_ordered_rows_checked": len(full_rows),
            "complete_accepted_ordered_rows": accepted,
            "all_nonframe_edge_deletion_certificates": deletions,
            "Q_and_P_binary_relations": tuples,
            "scope": "A named nonplanar control, certified by its stored K5 minor; not a disk counterexample."}


def build():
    cells = json.loads(CELLS.read_text())
    reps = [tuple(row) for row in cells["pattern_order"]]
    assert cells["singleton_of_three_colour"] == {"0": 4, "1": 3, "3": 2, "4": 1, "6": 0}
    assert {i for i, row in enumerate(reps) if len(set(row)) == 4} == {2, 5, 7, 8, 9}
    full_rows = tuple(row for row in product(U, repeat=5)
                      if all(row[i] != row[(i + 1) % 5] for i in B))
    assert len(full_rows) == 240
    graphs = [path_graph("C4_pairs12_34", ((1, 2), (3, 4))),
              path_graph("C4_pairs14_23", ((1, 4), (2, 3))),
              path_graph("C6_pairs12_14_34", ((1, 2), (1, 4), (3, 4))),
              path_graph("C6_pairs14_12_23", ((1, 4), (1, 2), (2, 3)))]
    minors = [dict(graph_name=graphs[0]["name"], **minor_control(graphs[0], 0)),
              dict(graph_name=graphs[1]["name"], **minor_control(graphs[1], 1)),
              dict(graph_name=graphs[0]["name"], **minor_control(graphs[0], 1)),
              dict(graph_name=graphs[1]["name"], **minor_control(graphs[1], 0)),
              dict(graph_name=graphs[2]["name"], **minor_control(graphs[2], 0)),
              dict(graph_name=graphs[3]["name"], **minor_control(graphs[3], 0))]
    controls = [graph_relation(graph, reps, full_rows) for graph in graphs]
    return {"schema": 1,
            "scope": "E2 951 t=3 all-G-minimal branch: finite joint-list table and named K5/path controls. Arbitrary-size exclusion is the separate paper proof; no source enumeration or new Lean proof.",
            "sha256": {str(Path(__file__).resolve().relative_to(ROOT)): sha256(Path(__file__).read_bytes()).hexdigest(),
                       str(CELLS.relative_to(ROOT)): sha256(CELLS.read_bytes()).hexdigest()},
            "provenance": {"ordered_original_boundary": list(B), "root": "r",
                           "root_spokes": ["b0", "b1", "b4"],
                           "original_C_attachments_allowed_only_at": ["r", "b1", "b2", "b3", "b4"],
                           "two_distinct_original_contacts": ["a", "b"],
                           "sector_role_order": ["r", "b1", "b2", "b3", "b4"],
                           "Q_singleton_b4": list(Q), "P_singleton_b1": list(P),
                           "joint_sector_rows": [list(DELTA), list(DELTA_PRIME)],
                           "root_pinned_colour": D,
                           "other_nonadjacent_row_singleton_b2_has_duplicate_spoke_colours": [0, 1, 1]},
            "pattern_order": [list(row) for row in reps], "tight_attachment_controls": tight_table(),
            "K5_controls": minors, "complete_graph_controls": controls,
            "summary": {"tight_noncontact_boundary_pairs": 4, "tight_noncontact_bridge_leaf_triples": 0,
                        "first_internal_cycle_entry_checks": 8,
                        "named_K5_minors": len(minors), "named_complete_graph_controls": len(controls),
                        "full_ordered_boundary_row_checks": len(controls) * len(full_rows),
                        "control_masks": [g["complete_sigma"] for g in controls],
                        "control_C_orders": [len(g["original_C_path"]) for g in controls],
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
