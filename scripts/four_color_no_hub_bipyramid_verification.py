#!/usr/bin/env python3
"""Replay complete fibres for saturated bipyramid exteriors without a hub.

Finite evidence only.  Original-edge enumeration is independent of the
two-pole path formula and of the closure recurrence.  All labelled boundary
assignments, including empty fibres, and all exterior witnesses are retained.
"""

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx

from four_color_shelling_fan_verification import geometry
from four_color_shelling_verification import bipyramid, faces
from four_color_saturated_hub_verification import (
    canonical_contract,
    edge_set,
    enumerate_original_edges,
    exterior_stage,
    original_embedding_check,
)


ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))


def path_count(q, length, equal):
    """Labelled K_q walk count for prescribed endpoints, q in {2, 3}."""
    correction = (q - 1) if equal else -1
    return ((q - 1) ** length + correction * (-1) ** length) // q


def row_number(row):
    number = 0
    for color in row:
        number = 4 * number + color
    return number


def stage_geometry(graph, rim_size, left, right):
    """An actual canonical ordering reaching this contiguous-rim prefix."""
    boundary_pole, processed_pole = rim_size, rim_size + 1
    rim_order = [(left + j) % rim_size for j in range(rim_size)]
    order = rim_order[:2] + [boundary_pole] + rim_order[2:] + [processed_pole]
    _, embedding = nx.check_planarity(graph)
    outer = [rim_order[0], rim_order[1], processed_pole]
    assert any(outer == face[j:] + face[:j]
               for face in faces(embedding) for j in range(3))
    geom = geometry(graph, outer=outer, order=order)
    canonical_contract(graph, geom)
    k = right - left + 2
    assert set(order[:k]) == set(range(left, right + 1)) | {boundary_pole}
    return geom, exterior_stage(graph, geom, k)


def audit_stage(graph, rim_size, left, right):
    boundary_pole, processed_pole = rim_size, rim_size + 1
    geom, stage = stage_geometry(graph, rim_size, left, right)
    disk, _ = original_embedding_check(stage, geom["rotation_cw"])
    assert not stage["unprocessed_interior_vertices"]
    assert stage["exterior_vertices"] == sorted(graph)
    visible = list(range(left, right + 1))
    hidden = list(range(right + 1, rim_size)) + list(range(left))
    assert hidden
    path = [right] + hidden + [left]
    length = len(path) - 1
    scope = stage["boundary_scope"]
    assert set(scope) == set(visible) | {boundary_pole}
    common_hubs = sorted(v for v in set(disk) - set(scope)
                         if set(scope) <= set(disk[v]))
    assert not common_hubs
    expected_edges = {
        tuple(sorted((j, (j + 1) % rim_size))) for j in range(rim_size)
    } | {tuple(sorted((processed_pole, j))) for j in range(rim_size)} | {
        tuple(sorted((boundary_pole, j))) for j in hidden + [left, right]
    }
    assert edge_set(disk) == expected_edges
    witnesses = enumerate_original_edges(disk)
    assert witnesses
    witness_set = set(witnesses)
    witness_index = {values: j for j, values in enumerate(witnesses)}
    vertices = sorted(disk)
    oracle = defaultdict(list)
    equal_pole_oracle = set()
    for j, values in enumerate(witnesses):
        coloring = dict(zip(vertices, values))
        row = tuple(coloring[v] for v in scope)
        oracle[row].append(j)
        if coloring[processed_pole] == coloring[boundary_pole]:
            equal_pole_oracle.add(values)

    fibre_counts, fibre_indices, branch_counts = [], [], []
    rows = []
    equal_pole_rows = []
    glued_all = set()
    missing_q, accepted_four = None, None
    boundary_edges = list(zip(scope, scope[1:] + scope[:1]))
    for row in itertools.product(COLORS, repeat=len(scope)):
        coloring = dict(zip(scope, row))
        proper = all(coloring[u] != coloring[v] for u, v in boundary_edges)
        s = coloring[boundary_pole]
        rim_colors = {coloring[v] for v in visible}
        endpoints_equal = coloring[left] == coloring[right]
        equal_count = (path_count(3, length, endpoints_equal)
                       if proper and s not in rim_colors else 0)
        unequal_count = (len(set(COLORS) - rim_colors - {s})
                         * path_count(2, length, endpoints_equal) if proper else 0)
        formula_count = equal_count + unequal_count
        glued, branches = set(), []
        for r in COLORS:
            expected = 0
            if proper and r not in rim_colors:
                palette = sorted(set(COLORS) - {r, s})
                expected = path_count(len(palette), length, endpoints_equal)
                actual = 0
                for values in itertools.product(palette, repeat=len(hidden)):
                    full = coloring | {processed_pole: r} | dict(zip(hidden, values))
                    if all(full[u] != full[v] for u, v in zip(path, path[1:])):
                        glued.add(tuple(full[v] for v in vertices))
                        actual += 1
                assert actual == expected
            branches.append(expected)
        oracle_values = {witnesses[j] for j in oracle[row]}
        assert glued == oracle_values
        assert len(glued) == formula_count == sum(branches)
        assert equal_count == sum(values in equal_pole_oracle for values in glued)
        glued_all |= glued
        fibre_counts.append(len(glued))
        fibre_indices.append(oracle[row])
        branch_counts.append(branches)
        if glued:
            rows.append(row)
        if equal_count:
            equal_pole_rows.append(row)
            assert equal_count > 0 and s not in rim_colors
        if (missing_q is None and proper and set(row) <= {0, 1, 2}
                and not glued):
            missing_q = row
        if accepted_four is None and glued and len(set(row)) == 4:
            accepted_four = row
    assert glued_all == witness_set
    assert equal_pole_oracle
    for values in equal_pole_oracle:
        coloring = dict(zip(vertices, values))
        assert coloring[boundary_pole] not in {coloring[v] for v in visible}
    result = dict(stage) | {
        "state_id": f"C{rim_size}-arc-{left}-{right}",
        "canonical_geometry": geom,
        "rim_size": rim_size,
        "visible_rim_arc": visible,
        "hidden_rim_arc": hidden,
        "hidden_path_vertex_scope": path,
        "hidden_path_length": length,
        "boundary_pole_b": boundary_pole,
        "processed_pole_a": processed_pole,
        "common_original_hub_candidates": common_hubs,
        "complete_witness_scope": vertices,
        "complete_original_edge_colorings": witnesses,
        "complete_proper_boundary_relation": rows,
        "fibre_order": "all base-4 boundary rows lexicographically, zeros included",
        "complete_boundary_fibre_counts_including_zero": fibre_counts,
        "complete_boundary_fibre_witness_indices_including_zero": fibre_indices,
        "complete_path_branch_counts_by_processed_pole_color": branch_counts,
        "equal_pole_supported_boundary_rows": equal_pole_rows,
        "equal_pole_complete_witness_indices": sorted(
            witness_index[values] for values in equal_pole_oracle),
        "missing_proper_Q012_boundary_row": missing_q,
        "accepted_four_color_boundary_row": accepted_four,
    }
    return result


def compatible_closure_geometry(graph, old, new, x):
    """One canonical order and one retained root edge for this actual step."""
    rim_size = old["rim_size"]
    boundary_pole, processed_pole = old["boundary_pole_b"], old["processed_pole_a"]
    left, right = old["visible_rim_arc"][0], old["visible_rim_arc"][-1]
    if x == right:
        geom = old["canonical_geometry"]
    else:
        assert x == left
        # Retain a root edge at the opposite end and build the old visible arc
        # by adding its left endpoints.  The root dart keeps its original
        # orientation even though subsequent rim insertions run backwards.
        rim_order = [right - 1, right] + [
            (right - 2 - j) % rim_size for j in range(rim_size - 2)
        ]
        order = rim_order[:2] + [boundary_pole] + rim_order[2:] + [processed_pole]
        geom = geometry(graph, outer=rim_order[:2] + [processed_pole], order=order)
        canonical_contract(graph, geom)
    k = len(old["remaining_vertices"])
    assert geom["order"][k - 1] == x
    assert set(geom["order"][:k]) == set(old["remaining_vertices"])
    assert set(geom["order"][:k - 1]) == set(new["remaining_vertices"])
    step = geom["steps"][k - 4]
    assert step["vertex"] == x and step["m"] == 2
    actual_old, actual_new = exterior_stage(graph, geom, k), exterior_stage(graph, geom, k - 1)
    for original, actual in ((old, actual_old), (new, actual_new)):
        assert set(original["boundary_scope"]) == set(actual["boundary_scope"])
        assert original["exterior_vertices"] == actual["exterior_vertices"]
        assert original["exterior_edges"] == actual["exterior_edges"]
        original_embedding_check(actual, geom["rotation_cw"])
    assert geom["rotation_cw"] == old["canonical_geometry"]["rotation_cw"]
    return {
        "canonical_geometry": geom,
        "same_retained_root_edge": geom["order"][:2],
        "old_remaining_prefix_length": k,
        "old_boundary_scope_in_this_order": actual_old["boundary_scope"],
        "new_boundary_scope_in_this_order": actual_new["boundary_scope"],
        "canonical_step": step,
        "same_original_exterior_edges_and_rotation_checked": True,
    }


def audit_closure(graph, old, new, x):
    compatible = compatible_closure_geometry(graph, old, new, x)
    old_scope, scope = old["boundary_scope"], new["boundary_scope"]
    assert set(scope) == set(old_scope) - {x}
    assert new["hidden_path_length"] == old["hidden_path_length"] + 1
    assert set(new["hidden_rim_arc"]) == set(old["hidden_rim_arc"]) | {x}
    assert old["boundary_pole_b"] == new["boundary_pole_b"]
    assert old["processed_pole_a"] == new["processed_pole_a"]
    old_edges, new_edges = set(map(tuple, old["exterior_edges"])), set(map(tuple, new["exterior_edges"]))
    added = sorted(new_edges - old_edges)
    assert len(added) == 1 and new_edges == old_edges | set(added)
    p, q = added[0]
    assert {p, q} == {old_scope[(old_scope.index(x) - 1) % len(old_scope)],
                      old_scope[(old_scope.index(x) + 1) % len(old_scope)]}
    assert old["boundary_pole_b"] in {p, q}
    vertices = old["complete_witness_scope"]
    assert vertices == new["complete_witness_scope"]
    old_witnesses = list(map(tuple, old["complete_original_edge_colorings"]))
    new_witnesses = list(map(tuple, new["complete_original_edge_colorings"]))
    survivors = [values for values in old_witnesses
                 if values[vertices.index(p)] != values[vertices.index(q)]]
    assert survivors == new_witnesses
    old_rows = set(map(tuple, old["complete_proper_boundary_relation"]))
    oracle = defaultdict(int)
    lifted_by_row = defaultdict(set)
    survivors_by_old_row = defaultdict(set)
    equal_pole_witness_by_new_row = {}
    for values in new_witnesses:
        coloring = dict(zip(vertices, values))
        row = tuple(coloring[v] for v in scope)
        old_row = tuple(coloring[v] for v in old_scope)
        oracle[row] |= 1 << coloring[x]
        lifted_by_row[row].add(old_row)
        survivors_by_old_row[old_row].add(values)
        if coloring[old["boundary_pole_b"]] == coloring[old["processed_pole_a"]]:
            equal_pole_witness_by_new_row.setdefault(row, values)
    masks, new_rows = [], set()
    for row in itertools.product(COLORS, repeat=len(scope)):
        coloring = dict(zip(scope, row))
        mask, lifts = 0, set()
        if coloring[p] != coloring[q]:
            for color in COLORS:
                lifted = tuple((coloring | {x: color})[v] for v in old_scope)
                if lifted in old_rows:
                    mask |= 1 << color
                    lifts.add(lifted)
        assert mask == oracle[row]
        assert lifts == lifted_by_row[row]
        assert bool(mask) == bool(new["complete_boundary_fibre_counts_including_zero"][row_number(row)])
        masks.append(mask)
        if mask:
            new_rows.add(row)
    assert new_rows == set(map(tuple, new["complete_proper_boundary_relation"]))
    # Each new equal-pole boundary row has a complete old-row lift with p != q.
    support_lifts = []
    for row in new["equal_pole_supported_boundary_rows"]:
        values = equal_pole_witness_by_new_row[row]
        witness = dict(zip(vertices, values))
        old_row = tuple(witness[v] for v in old_scope)
        assert old_row in old_rows and witness[p] != witness[q]
        support_lifts.append({"new_boundary_row": row, "old_boundary_row": old_row,
                              "old_complete_witness": values})
    assert support_lifts
    # Check all witness sets of every single old row, with no marginal splicing.
    for row, indices in zip(itertools.product(COLORS, repeat=len(old_scope)),
                            old["complete_boundary_fibre_witness_indices_including_zero"]):
        coloring = dict(zip(old_scope, row))
        expected = {old_witnesses[j] for j in indices} if coloring[p] != coloring[q] else set()
        observed = survivors_by_old_row[row]
        assert observed == expected
    return {
        "old_state_id": old["state_id"], "new_state_id": new["state_id"],
        "compatible_same_root_canonical_transition": compatible,
        "eliminated_boundary_vertex": x, "m": 2,
        "added_original_edge": added[0], "new_boundary_scope": scope,
        "complete_transition_masks_including_zero": masks,
        "transition_fibre_order": "all base-4 new boundary rows lexicographically; color t has bit 1<<t",
        "same_old_row_all_witness_filter_checked": True,
        "equal_pole_support_complete_old_row_lifts": support_lifts,
    }


def opening_audit(graph, rim_size, first):
    geom = first["canonical_geometry"]
    previous = exterior_stage(graph, geom, rim_size + 1)
    disk, _ = original_embedding_check(previous, geom["rotation_cw"])
    witnesses = enumerate_original_edges(disk)
    x = rim_size - 1
    boundary_pole = rim_size
    assert previous["unprocessed_interior_vertices"] == [boundary_pole]
    step = geom["steps"][rim_size - 3]
    assert step["vertex"] == x and step["m"] == 3
    old_scope = previous["boundary_scope"]
    new_scope = first["boundary_scope"]
    path = step["lower_neighbors"]
    assert set(path[1:-1]) == {boundary_pole}
    old_rows = {tuple(dict(zip(previous["exterior_vertices"], values))[v] for v in old_scope)
                for values in witnesses}
    masks = []
    for row in itertools.product(COLORS, repeat=len(new_scope)):
        coloring = dict(zip(new_scope, row))
        mask = 0
        for color in COLORS:
            lifted = coloring | {x: color}
            if (tuple(lifted[v] for v in old_scope) in old_rows
                    and all(color != coloring[v] for v in path)
                    and all(coloring[u] != coloring[v]
                            for u, v in zip(new_scope, new_scope[1:] + new_scope[:1]))):
                mask |= 1 << color
        masks.append(mask)
    oracle = defaultdict(int)
    for values in first["complete_original_edge_colorings"]:
        coloring = dict(zip(first["complete_witness_scope"], values))
        oracle[tuple(coloring[v] for v in new_scope)] |= 1 << coloring[x]
    assert masks == [oracle[row] for row in itertools.product(COLORS, repeat=len(new_scope))]
    return dict(previous) | {
        "complete_original_edge_colorings": witnesses,
        "complete_proper_boundary_relation": sorted(old_rows),
        "m3_transition": {"eliminated": x, "neighbor_path": path,
                           "new_boundary_scope": new_scope,
                           "complete_transition_masks_including_zero": masks},
        "first_saturated_state_id": first["state_id"],
    }


def case_audit(rim_size):
    graph = bipyramid(rim_size)
    states = {}
    for left in range(rim_size - 2):
        for right in range(left + 1, rim_size - 1):
            states[left, right] = audit_stage(graph, rim_size, left, right)
    transitions = []
    for (left, right), old in states.items():
        if right - left == 1:
            continue
        # These are all ears of the remaining induced fan.  Either endpoint
        # can be canonical after choosing an appropriate retained base edge.
        remaining = graph.subgraph(old["remaining_vertices"])
        ears = sorted(v for v in remaining if remaining.degree(v) == 2)
        assert ears == [left, right]
        transitions.append(audit_closure(graph, old, states[left + 1, right], left))
        transitions.append(audit_closure(graph, old, states[left, right - 1], right))
    first = states[0, rim_size - 2]
    opening = opening_audit(graph, rim_size, first)
    suffix = [states[0, right]["state_id"] for right in range(rim_size - 2, 0, -1)]
    terminal_count = (4 * (2 ** rim_size + 2 * (-1) ** rim_size)
                      + 12 * (1 + (-1) ** rim_size))
    terminal_sets = []
    for (left, right), stage in states.items():
        if right - left == 1:
            assert set(map(tuple, stage["exterior_edges"])) == edge_set(graph)
            assert len(stage["complete_original_edge_colorings"]) == terminal_count
            terminal_sets.append(set(map(tuple, stage["complete_original_edge_colorings"])))
    assert terminal_sets and all(values == terminal_sets[0] for values in terminal_sets)
    if rim_size == 4:
        counts = first["complete_boundary_fibre_counts_including_zero"]
        assert first["boundary_scope"] == [0, 1, 2, 4]
        assert counts[row_number((0, 1, 2, 1))] == 0
        assert counts[row_number((0, 1, 2, 3))] == 1
        assert counts[row_number((0, 1, 0, 1))] == 2
    return {"name": f"bipyramid-C{rim_size}",
            "original_vertices": sorted(graph), "original_edges": sorted(edge_set(graph)),
            "pole_roles": {"processed_pole_a": rim_size + 1, "boundary_pole_b": rim_size},
            "rim_cyclic_order": list(range(rim_size)),
            "opening_wheel_and_m3": opening,
            "terminal_full_original_graph_coloring_count": terminal_count,
            "terminal_count_closed_formula": "4*(2**ell+2*(-1)**ell)+12*(1+(-1)**ell)",
            "standard_right_ear_canonical_suffix": suffix,
            "all_branching_states": list(states.values()),
            "all_left_and_right_ear_closures": transitions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    cases = [case_audit(size) for size in range(4, 8)]
    states = [stage for case in cases for stage in case["all_branching_states"]]
    closures = [step for case in cases for step in case["all_left_and_right_ear_closures"]]
    imports = [Path(__file__),
               ROOT / "scripts/four_color_shelling_fan_verification.py",
               ROOT / "scripts/four_color_shelling_verification.py",
               ROOT / "scripts/four_color_saturated_hub_verification.py"]
    totals = {
        "original_graphs": len(cases), "rim_sizes": list(range(4, 8)),
        "actual_canonical_saturated_states": len(states),
        "states_without_common_original_hub": len(states),
        "all_left_and_right_ear_closures": len(closures),
        "complete_original_edge_colorings": sum(len(s["complete_original_edge_colorings"]) for s in states),
        "complete_boundary_fibre_entries_including_zero": sum(len(s["complete_boundary_fibre_counts_including_zero"]) for s in states),
        "zero_boundary_fibres": sum(s["complete_boundary_fibre_counts_including_zero"].count(0) for s in states),
        "complete_transition_masks_including_zero": sum(len(c["complete_transition_masks_including_zero"]) for c in closures),
        "zero_transition_masks": sum(c["complete_transition_masks_including_zero"].count(0) for c in closures),
        "states_rejecting_some_proper_Q012_row": sum(s["missing_proper_Q012_boundary_row"] is not None for s in states),
        "states_accepting_some_four_color_row": sum(s["accepted_four_color_boundary_row"] is not None for s in states),
        "equal_pole_complete_witnesses": sum(len(s["equal_pole_complete_witness_indices"]) for s in states),
        "equal_pole_supported_boundary_rows": sum(len(s["equal_pole_supported_boundary_rows"]) for s in states),
        "equal_pole_same_witness_old_row_lifts": sum(len(c["equal_pole_support_complete_old_row_lifts"]) for c in closures),
        "initial_wheel_to_first_saturation_m3_transitions": len(cases),
    }
    report = {
        "schema": "four-color-no-hub-bipyramid-verification-v1",
        "scope": "Finite C4-C7 bipyramid canonical sources; general no-hub sources and 4CT remain OPEN.",
        "oracle": "All labelled proper colorings of original exterior edges by backtracking, independent of path formula and recurrence.",
        "networkx_version": nx.__version__,
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in imports},
        "totals": totals, "cases": cases,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(totals, sort_keys=True))


if __name__ == "__main__":
    main()
