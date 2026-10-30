#!/usr/bin/env python3
"""Complete-fibre replay for even capped-antiprism canonical sources.

Original exterior-edge backtracking is independent of closed-rung enumeration.
All ordered boundary assignments, including empty fibres, are recorded. This
finite audit does not prove arbitrary-source no-locking or use a 4CT oracle.
"""
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

from four_color_bond_perimeter_small_cuts import (
    capped_antiprism, original_faces, short_cycle_sides,
)
from four_color_shelling_fan_verification import geometry
from four_color_shelling_verification import faces
from four_color_saturated_hub_verification import (
    canonical_contract, edge_set, enumerate_original_edges,
    exterior_stage, original_embedding_check,
)

ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))


def row_number(row):
    answer = 0
    for color in row:
        answer = 4 * answer + color
    return answer


def source_geometry(graph, n, start=0, direction=1):
    """Explicit dihedral version of the same geometric canonical ordering."""
    xs = [(start + direction * j) % n for j in range(n)]
    # The original y_i joins x_i and x_(i+1), including after reflection.
    ys = [n + (xs[j] if direction == 1 else xs[(j + 1) % n])
          for j in range(n)]
    order = xs[:2] + [2 * n] + xs[2:] + list(reversed(ys[1:])) + [2 * n + 1, ys[0]]
    _, embedding = nx.check_planarity(graph)
    outer = order[:2] + [ys[0]]
    if not any(outer == face[j:] + face[:j]
               for face in faces(embedding) for j in range(3)):
        order[:2] = list(reversed(order[:2]))
        outer = order[:2] + [ys[0]]
    geom = geometry(graph, outer=outer, order=order)
    canonical_contract(graph, geom)
    return geom


def rung_witnesses(n, left, right):
    """Closed local-state walks, with all colours and cap choices retained.

    State i is (u_i,v_i), original colors of (x_i,y_i). Node conditions
    are u_i != v_i, v_i != r, and u_i != s exactly for active a spokes.
    Transition conditions are u_i != u_(i+1), v_i != v_(i+1),
    v_i != u_(i+1). No edge-oracle input is used here.
    """
    cap_indices = set(range(n)) - set(range(left + 1, right))
    result = []
    for s, r in itertools.product(COLORS, repeat=2):
        options = [[(u, v) for u, v in itertools.product(COLORS, repeat=2)
                    if u != v and v != r and (i not in cap_indices or u != s)]
                   for i in range(n)]

        def compatible(old, new):
            return old[0] != new[0] and old[1] != new[1] and old[1] != new[0]

        def visit(word):
            if len(word) == n:
                if compatible(word[-1], word[0]):
                    result.append(tuple(u for u, _ in word) +
                                  tuple(v for _, v in word) + (s, r))
                return
            for state in options[len(word)]:
                if not word or compatible(word[-1], state):
                    visit(word + [state])

        visit([])
    assert len(result) == len(set(result))
    return sorted(result)


def support_patterns(n):
    """Ninety-six explicitly specified original geometric colour patterns."""
    answer = set()
    for palette in itertools.combinations(COLORS, 2):
        other = tuple(c for c in COLORS if c not in palette)
        for xphase, yphase in itertools.product(range(2), repeat=2):
            xs = tuple(palette[(i + xphase) % 2] for i in range(n))
            ys = tuple(other[(i + yphase) % 2] for i in range(n))
            for s, r in itertools.product(other, palette):
                answer.add(xs + ys + (s, r))
    assert len(answer) == 96
    return sorted(answer)


def audit_stage(graph, n, left, right, patterns):
    geom = source_geometry(graph, n, left)
    k = right - left + 2
    stage = exterior_stage(graph, geom, k)
    disk, _ = original_embedding_check(stage, geom['rotation_cw'])
    assert set(stage['remaining_vertices']) == set(range(left, right + 1)) | {2 * n}
    assert not stage['unprocessed_interior_vertices']
    assert stage['exterior_vertices'] == list(range(2 * n + 2))
    inactive = {tuple(sorted((2 * n, i))) for i in range(left + 1, right)}
    assert edge_set(disk) == edge_set(graph) - inactive
    hubs = [v for v in disk if v not in stage['boundary_scope']
            and set(stage['boundary_scope']) <= set(disk[v])]
    assert not hubs
    witnesses = enumerate_original_edges(disk)
    formula = rung_witnesses(n, left, right)
    assert witnesses == formula
    witness_index = {values: j for j, values in enumerate(witnesses)}
    assert set(patterns) <= set(witnesses)
    scope = stage['boundary_scope']
    oracle = defaultdict(list)
    for j, values in enumerate(witnesses):
        oracle[tuple(values[v] for v in scope)].append(j)
    support_rows = sorted({tuple(values[v] for v in scope) for values in patterns})
    assert len(support_rows) == 24
    all_rows = list(itertools.product(COLORS, repeat=len(scope)))
    # Check the boundary-only parity definition independently of projection.
    direct_support = []
    for row in all_rows:
        c = dict(zip(scope, row))
        u, v, s = c[left], c[left + 1], c[2 * n]
        if (u != v and s not in {u, v}
                and all(c[i] == (u if (i - left) % 2 == 0 else v)
                        for i in range(left, right + 1))):
            direct_support.append(row)
    assert direct_support == support_rows
    for row in support_rows:
        matching_patterns = [p for p in patterns if tuple(p[v] for v in scope) == row]
        assert len(matching_patterns) == 4 and len(oracle[row]) >= 4
    fibre_indices = [oracle[row] for row in all_rows]
    counts = list(map(len, fibre_indices))
    boundary_edges = list(zip(scope, scope[1:] + scope[:1]))
    missing_q = next((row for row in all_rows
                      if set(row) <= {0, 1, 2} and not oracle[row]
                      and all(row[scope.index(u)] != row[scope.index(v)]
                              for u, v in boundary_edges)), None)
    accepted_four = next((row for row in all_rows
                          if len(set(row)) == 4 and oracle[row]), None)
    return stage | {
        'state_id': f'A{n}-arc-{left}-{right}', 'rim_size': n,
        'visible_x_arc': list(range(left, right + 1)),
        'active_a_spoke_indices': sorted(set(range(n)) - set(range(left + 1, right))),
        'canonical_geometry': geom,
        'common_original_hub_candidates': hubs,
        'complete_witness_scope': list(range(2 * n + 2)),
        'complete_original_edge_colorings': witnesses,
        'closed_rung_walk_set_equals_original_edge_oracle': True,
        'fibre_order': 'All lexicographic base-4 boundary assignments, including zeros.',
        'complete_boundary_fibre_counts_including_zero': counts,
        'complete_boundary_fibre_witness_indices_including_zero': fibre_indices,
        'complete_proper_boundary_relation': [row for row in all_rows if oracle[row]],
        'periodic_support_boundary_rows': support_rows,
        'periodic_support_complete_witness_indices': [witness_index[p] for p in patterns],
        'missing_proper_Q012_boundary_row': missing_q,
        'accepted_four_color_boundary_row': accepted_four,
    }


def compatible_geometry(graph, n, old, new, x):
    left, right = old['visible_x_arc'][0], old['visible_x_arc'][-1]
    geom = source_geometry(graph, n, left) if x == right else source_geometry(graph, n, right, -1)
    k = len(old['remaining_vertices'])
    assert geom['order'][k - 1] == x
    assert set(geom['order'][:k]) == set(old['remaining_vertices'])
    assert set(geom['order'][:k - 1]) == set(new['remaining_vertices'])
    step = geom['steps'][k - 4]
    assert step['vertex'] == x and step['m'] == 2
    for stage, prefix in [(old, k), (new, k - 1)]:
        actual = exterior_stage(graph, geom, prefix)
        assert set(actual['boundary_scope']) == set(stage['boundary_scope'])
        assert actual['exterior_edges'] == stage['exterior_edges']
        original_embedding_check(actual, geom['rotation_cw'])
    assert geom['rotation_cw'] == old['canonical_geometry']['rotation_cw']
    return {'canonical_geometry': geom, 'retained_root_edge': geom['order'][:2],
            'old_prefix_length': k, 'canonical_step': step}


def audit_closure(graph, n, old, new, x, patterns):
    compatible = compatible_geometry(graph, n, old, new, x)
    added = set(map(tuple, new['exterior_edges'])) - set(map(tuple, old['exterior_edges']))
    assert len(added) == 1
    p, q = next(iter(added))
    assert 2 * n in {p, q}
    scope, old_scope = new['boundary_scope'], old['boundary_scope']
    assert set(scope) == set(old_scope) - {x}
    old_witnesses = old['complete_original_edge_colorings']
    new_witnesses = new['complete_original_edge_colorings']
    survivors = [values for values in old_witnesses if values[p] != values[q]]
    assert survivors == new_witnesses
    old_rows = set(old['complete_proper_boundary_relation'])
    oracle_masks = defaultdict(int)
    survivors_by_old_row = defaultdict(set)
    new_index = {values: j for j, values in enumerate(new_witnesses)}
    for values in new_witnesses:
        oracle_masks[tuple(values[v] for v in scope)] |= 1 << values[x]
        survivors_by_old_row[tuple(values[v] for v in old_scope)].add(values)
    masks, transfer_fibres = [], []
    for row in itertools.product(COLORS, repeat=len(scope)):
        c = dict(zip(scope, row))
        mask, branches = 0, []
        if c[p] != c[q]:
            for t in COLORS:
                old_row = tuple((c | {x: t})[v] for v in old_scope)
                if old_row in old_rows:
                    mask |= 1 << t
                    indices = old['complete_boundary_fibre_witness_indices_including_zero'][row_number(old_row)]
                    branches.append({'eliminated_color': t, 'old_boundary_row': old_row,
                                     'old_witness_indices': indices})
        assert mask == oracle_masks[row]
        assert bool(mask) == bool(new['complete_boundary_fibre_counts_including_zero'][row_number(row)])
        # Each complete branch carries unchanged original vertex colours.
        glued = {old_witnesses[j] for branch in branches for j in branch['old_witness_indices']}
        expected = {new_witnesses[j] for j in new['complete_boundary_fibre_witness_indices_including_zero'][row_number(row)]}
        assert glued == expected
        masks.append(mask)
        transfer_fibres.append(branches)
    for row, indices in zip(itertools.product(COLORS, repeat=len(old_scope)),
                            old['complete_boundary_fibre_witness_indices_including_zero']):
        c = dict(zip(old_scope, row))
        expected = {old_witnesses[j] for j in indices} if c[p] != c[q] else set()
        assert survivors_by_old_row[row] == expected
    support_lifts = []
    for row in new['periodic_support_boundary_rows']:
        values = next(values for values in patterns if tuple(values[v] for v in scope) == row)
        assert values[p] != values[q]
        old_row = tuple(values[v] for v in old_scope)
        assert old_row in old['periodic_support_boundary_rows']
        support_lifts.append({'new_boundary_row': row, 'old_boundary_row': old_row,
                              'same_complete_original_witness': values,
                              'new_witness_index': new_index[values]})
    return {'old_state_id': old['state_id'], 'new_state_id': new['state_id'],
            'compatible_same_root_canonical_transition': compatible,
            'm': 2, 'eliminated_boundary_vertex': x, 'added_original_edge': [p, q],
            'new_boundary_scope': scope,
            'complete_transition_masks_including_zero': masks,
            'complete_transfer_fibre_branches_including_empty': transfer_fibres,
            'same_old_row_all_witness_filter_checked': True,
            'periodic_support_same_witness_old_row_lifts': support_lifts}


def opening_audit(graph, n, first):
    geom = first['canonical_geometry']
    result = []
    first_k = len(first['remaining_vertices'])
    for k in range(len(graph) - 1, first_k, -1):
        stage = exterior_stage(graph, geom, k)
        disk, _ = original_embedding_check(stage, geom['rotation_cw'])
        witnesses = enumerate_original_edges(disk)
        assert witnesses
        result.append(stage | {'complete_original_edge_colorings': witnesses})
    assert result[-1]['unprocessed_interior_vertices'] == [2 * n]
    step = geom['steps'][first_k - 3]
    assert step['vertex'] == n - 1 and step['m'] == 3
    assert step['lower_neighbors'][1:-1] == [2 * n]
    assert all(stage['unprocessed_interior_vertices'] for stage in result)
    return {'actual_pre_saturation_stages': result,
            'last_m3_step_exposing_a': step,
            'first_saturated_state_id': first['state_id']}



def identification_reduction(graph, n):
    """All colourings of the smaller quotient lift with the same Y witness."""
    a, b, h = 2 * n, 2 * n + 1, n
    even_y = [n + i for i in range(0, n, 2)]
    retained = list(range(n, 2 * n)) + [b]
    mapping = {v: (h if v in even_y else v) for v in retained}
    quotient_edges = {tuple(sorted((mapping[u], mapping[v])))
                      for u, v in graph.subgraph(retained).edges()}
    assert all(u != v for u, v in quotient_edges)
    smaller = nx.Graph()
    smaller.add_nodes_from(sorted(set(mapping.values())))
    smaller.add_edges_from(sorted(quotient_edges))
    assert len(smaller) == n // 2 + 2 < len(graph)
    planar, embedding = nx.check_planarity(smaller)
    assert planar
    odd_y = [n + i for i in range(1, n, 2)]
    assert edge_set(smaller) == ({tuple(sorted((b, h)))} |
                                 {tuple(sorted((v, w))) for v in odd_y for w in [b, h]})
    lifts = []
    for values in enumerate_original_edges(smaller):
        c = dict(zip(sorted(smaller), values))
        free = set(COLORS) - {c[b], c[h]}
        assert len(free) == 2
        full = {v: c[mapping[v]] for v in retained} | {a: c[h]}
        for i in range(n):
            full[i] = c[b] if i % 2 == 0 else next(iter(free - {full[n + i]}))
        assert all(full[u] != full[v] for u, v in graph.edges())
        assert all(full[v] == c[mapping[v]] for v in retained)
        lifts.append({'smaller_coloring': values,
                      'same_Y_witness_after_splitting': [full[v] for v in retained],
                      'complete_original_lift': [full[v] for v in sorted(graph)]})
    assert len(lifts) == 12 * 2 ** (n // 2)
    return {'deleted_original_vertices': list(range(n)) + [a],
            'identified_even_Y_vertices': even_y,
            'original_Y_to_quotient_vertex': mapping,
            'smaller_vertices': sorted(smaller), 'smaller_edges': sorted(edge_set(smaller)),
            'smaller_rotation_cw': {v: list(embedding.neighbors_cw_order(v)) for v in smaller},
            'simple_planar_strictly_smaller_checked': True,
            'complete_smaller_colorings_and_same_Y_lifts': lifts}


def triangle_reduction(graph, n):
    """Every original root-triangle colouring has four specified full lifts."""
    a, b = 2 * n, 2 * n + 1
    triangle = graph.subgraph([a, 0, 1]).copy()
    assert edge_set(triangle) == {(0, 1), (0, a), (1, a)}
    planar, _ = nx.check_planarity(triangle)
    assert planar and len(triangle) == 3 < len(graph)
    lifts = []
    for values in enumerate_original_edges(triangle):
        c = dict(zip(sorted(triangle), values))
        palette = (c[0], c[1])
        other = tuple(color for color in COLORS if color not in palette)
        extensions = []
        for phase, bcolor in itertools.product(range(2), palette):
            full = {i: palette[i % 2] for i in range(n)}
            full |= {n + i: other[(i + phase) % 2] for i in range(n)}
            full |= {a: c[a], b: bcolor}
            assert all(full[u] != full[v] for u, v in graph.edges())
            assert all(full[v] == c[v] for v in triangle)
            extensions.append(tuple(full[v] for v in sorted(graph)))
        assert len(set(extensions)) == 4
        lifts.append({'same_original_triangle_coloring': values,
                      'complete_original_lifts': extensions})
    assert len(lifts) == 24
    return {'retained_original_triangle_scope': sorted(triangle),
            'smaller_edges': sorted(edge_set(triangle)),
            'simple_planar_strictly_smaller_checked': True,
            'complete_smaller_colorings_and_lifts': lifts}


def case_audit(n):
    graph = capped_antiprism(n)
    assert n >= 6 and n % 2 == 0 and min(dict(graph.degree()).values()) == 5
    _, embedding = nx.check_planarity(graph)
    fs = original_faces(embedding)
    cycles = short_cycle_sides(graph, fs)
    patterns = support_patterns(n)
    assert all(all(p[u] != p[v] for u, v in graph.edges()) for p in patterns)
    states = {(left, right): audit_stage(graph, n, left, right, patterns)
              for left in range(n - 2) for right in range(left + 1, n - 1)}
    closures = []
    for (left, right), stage in states.items():
        if right - left == 1:
            continue
        remaining = graph.subgraph(stage['remaining_vertices'])
        ears = sorted(v for v in remaining if remaining.degree(v) == 2)
        assert ears == [left, right]
        closures.append(audit_closure(graph, n, stage, states[left + 1, right], left, patterns))
        closures.append(audit_closure(graph, n, stage, states[left, right - 1], right, patterns))
    terminal = enumerate_original_edges(graph)
    for stage in states.values():
        if len(stage['visible_x_arc']) == 2:
            assert set(map(tuple, stage['exterior_edges'])) == edge_set(graph)
            assert stage['complete_original_edge_colorings'] == terminal
    return {'name': f'even-capped-antiprism-{n}', 'rim_size': n,
            'original_vertices': sorted(graph), 'original_edges': sorted(edge_set(graph)),
            'original_faces': fs, 'original_degrees': dict(graph.degree()),
            'all_short_cycle_original_side_checks': cycles,
            'uniform_canonical_order': source_geometry(graph, n)['order'],
            'periodic_complete_original_patterns': patterns,
            'opening_to_first_saturation': opening_audit(graph, n, states[0, n - 2]),
            'all_branching_states': list(states.values()),
            'all_left_and_right_ear_closures': closures,
            'terminal_full_original_graph_coloring_count': len(terminal),
            'identification_style_C_reduction': identification_reduction(graph, n),
            'original_triangle_C_reduction': triangle_reduction(graph, n)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    cases = [case_audit(n) for n in [6, 8]]
    states = [s for case in cases for s in case['all_branching_states']]
    closures = [t for case in cases for t in case['all_left_and_right_ear_closures']]
    totals = {
        'original_graphs': len(cases), 'rim_sizes': [6, 8],
        'original_short_cycles_checked': sum(len(c['all_short_cycle_original_side_checks']) for c in cases),
        'actual_canonical_saturated_states': len(states),
        'states_without_common_original_hub': len(states),
        'all_left_and_right_ear_closures': len(closures),
        'complete_original_edge_colorings': sum(len(s['complete_original_edge_colorings']) for s in states),
        'complete_boundary_fibre_entries_including_zero': sum(len(s['complete_boundary_fibre_counts_including_zero']) for s in states),
        'zero_boundary_fibres': sum(s['complete_boundary_fibre_counts_including_zero'].count(0) for s in states),
        'complete_transition_masks_including_zero': sum(len(t['complete_transition_masks_including_zero']) for t in closures),
        'zero_transition_masks': sum(t['complete_transition_masks_including_zero'].count(0) for t in closures),
        'periodic_same_witness_old_row_lifts': sum(len(t['periodic_support_same_witness_old_row_lifts']) for t in closures),
        'periodic_complete_original_patterns_per_graph': 96,
        'states_rejecting_some_proper_Q012_row': sum(s['missing_proper_Q012_boundary_row'] is not None for s in states),
        'states_accepting_some_four_color_row': sum(s['accepted_four_color_boundary_row'] is not None for s in states),
        'first_saturation_m3_openings': len(cases),
        'identification_reduction_smaller_colorings_lifted': sum(len(c['identification_style_C_reduction']['complete_smaller_colorings_and_same_Y_lifts']) for c in cases),
        'triangle_reduction_smaller_colorings_lifted': sum(len(c['original_triangle_C_reduction']['complete_smaller_colorings_and_lifts']) for c in cases),
        'triangle_reduction_complete_original_lifts': 96 * len(cases),
    }
    imports = [Path(__file__), ROOT / 'scripts/four_color_bond_perimeter_small_cuts.py',
               ROOT / 'scripts/four_color_shelling_fan_verification.py',
               ROOT / 'scripts/four_color_shelling_verification.py',
               ROOT / 'scripts/four_color_saturated_hub_verification.py']
    report = {
        'schema': 'four-color-no-hub-min5-verification-v1',
        'scope': 'Finite even capped antiprisms n=6,8. General source coverage and 4CT remain OPEN.',
        'oracle': 'Original exterior-edge backtracking, independent of local closed-rung walks and boundary transition recurrence.',
        'networkx_version': nx.__version__,
        'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in imports},
        'totals': totals, 'cases': cases,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(totals, sort_keys=True))


if __name__ == '__main__':
    main()
