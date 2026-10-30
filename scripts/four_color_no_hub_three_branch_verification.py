#!/usr/bin/env python3
"""Complete same-source three-branch capped-antiprism replay.

This file starts from an explicit original graph and canonical order. The
three-branch seed has central original triangle (a,x0,x1). Explicit templates
extend every proper seed row; the general repetition proof is in the report.
This does not assert arbitrary-source three-branch nonemptiness.
"""

import argparse
from collections import defaultdict, deque
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

from four_color_bond_perimeter_small_cuts import (
    capped_antiprism, original_faces, short_cycle_sides,
)
from four_color_no_hub_three_branch_support import (
    EIGHT_RUNG_TEMPLATES, SIX_RUNG_TEMPLATES,
    all_constructed_initial_extensions, extend_initial_local_row,
)
from four_color_shelling_fan_verification import geometry
from four_color_saturated_hub_verification import (
    canonical_contract, edge_set, enumerate_original_edges, exterior_stage,
    original_embedding_check,
)

ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))


def source_graph(n):
    assert n >= 6 and n % 2 == 0
    return capped_antiprism(n)


def initial_remaining(n):
    return frozenset((0, n - 1, 2 * n, 1, n, 2))


def source_order(n):
    """Explicit order, not canonical-order search or a coloring oracle."""
    return ([0, n - 1, 2 * n, 1, n, 2, n + 1, 2 * n + 1]
            + list(range(n + 2, 2 * n - 2))
            + list(range(3, n - 1)) + [2 * n - 2, 2 * n - 1])


def source_geometry(graph, n, order=None):
    result = geometry(graph, outer=[0, n - 1, 2 * n - 1],
                      order=source_order(n) if order is None else order)
    canonical_contract(graph, result)
    return result


def branch_labels(n):
    return {
        'central_original_triangle': [2 * n, 0, 1],
        'fixed_root_edge': [0, n - 1],
        'original_branches': [
            {'attachment_edge': [2 * n, 0], 'ear': n - 1,
             'original_face': [2 * n, 0, n - 1]},
            {'attachment_edge': [0, 1], 'ear': n,
             'original_face': [0, 1, n]},
            {'attachment_edge': [1, 2 * n], 'ear': 2,
             'original_face': [1, 2 * n, 2]},
        ],
    }


def fixed_root_state_graph(graph, n):
    """Exhaust all legal ears while retaining one literal original root edge."""
    root = frozenset((0, n - 1))
    first = initial_remaining(n)
    paths = {first: []}
    transitions = []
    queue = deque([first])
    while queue:
        old = queue.popleft()
        if len(old) == 3:
            continue
        ears = sorted(v for v in old - root
                      if graph.subgraph(old).degree(v) == 2)
        assert ears
        for vertex in ears:
            new = old - {vertex}
            transitions.append((old, new, vertex))
            if new not in paths:
                paths[new] = paths[old] + [vertex]
                queue.append(new)
    return paths, transitions


def compatible_geometry(graph, n, prior_ears, next_ear=None):
    """Same root, source, and rotation for a specified legitimate ear path."""
    remaining = set(initial_remaining(n))
    eliminated = []
    roots = {0, n - 1}
    for vertex in prior_ears + ([] if next_ear is None else [next_ear]):
        assert vertex in remaining - roots
        assert graph.subgraph(remaining).degree(vertex) == 2
        remaining.remove(vertex)
        eliminated.append(vertex)
    while len(remaining) > 3:
        vertex = next(v for v in sorted(remaining - roots)
                      if graph.subgraph(remaining).degree(v) == 2)
        remaining.remove(vertex)
        eliminated.append(vertex)
    third, = remaining - roots
    order = [0, n - 1, third] + list(reversed(eliminated)) + source_order(n)[6:]
    return source_geometry(graph, n, order=order)


def number(row):
    result = 0
    for color in row:
        result = 4 * result + color
    return result


def proper(edges, coloring):
    return all(coloring[u] != coloring[v] for u, v in edges)


def branches(boundary, n):
    """Keep the old central face until it disappears; then reanchor literally."""
    preferred = {2 * n, 0, 1}
    anchor = preferred if preferred <= set(boundary) else set(boundary)
    assert len(anchor) == 3
    central = [v for v in boundary if v in anchor]
    paths = []
    for left, right in zip(central, central[1:] + central[:1]):
        path = [left]
        j = boundary.index(left)
        while path[-1] != right:
            j = (j + 1) % len(boundary)
            path.append(boundary[j])
        paths.append(path)
    return central, paths


def full_joint_interfaces(graph, stage, n, witnesses):
    """Build three complete tables on ONE common exterior-coloring index.

    Independent enumeration uses only G[X]. Each branch then checks all its
    actual X attachments and path edges. The diagonal intersection, rather
    than nonempty marginals, must equal the original D-edge oracle.
    """
    boundary = stage['boundary_scope']
    central, paths = branches(boundary, n)
    exterior = sorted(set(graph) - set(boundary))
    omegas = enumerate_original_edges(graph.subgraph(exterior))
    omega_lookup = {values: j for j, values in enumerate(omegas)}
    domains = []
    for values in omegas:
        c = dict(zip(exterior, values))
        domains.append({v: sum(1 << color for color in COLORS
                               if all(color != c[w] for w in graph[v] if w in c))
                        for v in boundary})
    tables, table_sets = [], []
    for path in paths:
        all_rows = list(itertools.product(COLORS, repeat=len(path)))
        table = []
        for row in all_rows:
            ids = []
            if all(row[j] != row[j + 1] for j in range(len(row) - 1)):
                ids = [j for j, allowed in enumerate(domains)
                       if all(allowed[v] & (1 << color) for v, color in zip(path, row))]
            table.append(ids)
        tables.append({'ordered_path_scope': path,
                       'all_path_fibres_common_omega_indices_including_empty': table})
        table_sets.append([set(ids) for ids in table])
    oracle = defaultdict(set)
    for values in witnesses:
        row = tuple(values[v] for v in boundary)
        oracle[row].add(omega_lookup[tuple(values[v] for v in exterior)])
    joined = []
    marginal_false_positives = []
    for row in itertools.product(COLORS, repeat=len(boundary)):
        c = dict(zip(boundary, row))
        branch_sets = [table[number(tuple(c[v] for v in path))]
                       for path, table in zip(paths, table_sets)]
        ids = set.intersection(*branch_sets)
        assert ids == oracle[row]
        joined.append(sorted(ids))
        if all(branch_sets) and not ids:
            marginal_false_positives.append(row)
    # Joining from the tables reconstructs every named original coloring.
    reconstructed = set()
    for row, indices in zip(itertools.product(COLORS, repeat=len(boundary)), joined):
        for j in indices:
            c = dict(zip(boundary, row)) | dict(zip(exterior, omegas[j]))
            reconstructed.add(tuple(c[v] for v in sorted(graph)))
    assert reconstructed == set(witnesses)
    return {'central_original_triangle': central, 'ordered_branch_paths': paths,
            'common_exterior_scope': exterior,
            'all_proper_common_exterior_colorings': omegas,
            'branch_complete_interfaces': tables,
            'complete_joint_omega_fibres_including_empty': joined,
            'marginal_nonempty_but_joint_empty_rows': marginal_false_positives}


def local_support(graph, active, boundary):
    return [row for row in itertools.product(COLORS, repeat=len(boundary))
            if proper(graph.subgraph(active).edges(), dict(zip(boundary, row)))]


def original_faces_and_dual(graph, geom, active):
    fs = [sorted(f) for f in original_faces_from_rotation(graph, geom)
          if set(f) <= set(active)]
    dual = nx.Graph()
    dual.add_nodes_from(range(len(fs)))
    dual.add_edges_from((i, j) for i in range(len(fs)) for j in range(i)
                        if len(set(fs[i]) & set(fs[j])) == 2)
    assert len(fs) == len(active) - 2 and nx.is_tree(dual)
    return {'remaining_original_triangle_faces': fs,
            'weak_dual_edges': sorted(map(sorted, dual.edges())),
            'weak_dual_degrees': [dual.degree(i) for i in range(len(fs))]}


def original_faces_from_rotation(graph, geom):
    embedding = nx.PlanarEmbedding()
    embedding.set_data(geom['rotation_cw'])
    embedding.check_structure()
    return original_faces(embedding)


def audit_stage(graph, n, active, prior_ears):
    geom = compatible_geometry(graph, n, prior_ears)
    stage = exterior_stage(graph, geom, len(active))
    assert set(stage['remaining_vertices']) == set(active)
    assert not stage['unprocessed_interior_vertices']
    assert stage['exterior_vertices'] == sorted(graph)
    disk, _ = original_embedding_check(stage, geom['rotation_cw'])
    hubs = sorted(v for v in disk if v not in active and set(active) <= set(disk[v]))
    assert not hubs
    witnesses = enumerate_original_edges(disk)
    witness_index = {values: j for j, values in enumerate(witnesses)}
    boundary = stage['boundary_scope']
    oracle = defaultdict(list)
    for j, values in enumerate(witnesses):
        oracle[tuple(values[v] for v in boundary)].append(j)
    fibres = [oracle[row] for row in itertools.product(COLORS, repeat=len(boundary))]
    support = local_support(graph, active, boundary)
    assert len(support) == 24 * 2 ** (len(active) - 3)
    lifts = []
    for row in support:
        # Fill only removed LOCAL ears, without reading any whole-graph witness.
        initial_local = dict(zip(boundary, row))
        local_fill = []
        for vertex in reversed(prior_ears):
            forbidden = {initial_local[v] for v in graph[vertex] if v in initial_local}
            choices = sorted(set(COLORS) - forbidden)
            assert len(choices) == 2
            initial_local[vertex] = choices[0]
            local_fill.append({'vertex': vertex, 'two_local_color_choices': choices,
                               'chosen_local_color': choices[0]})
        assert set(initial_local) == initial_remaining(n)
        assert proper(graph.subgraph(initial_remaining(n)).edges(), initial_local)
        values = extend_initial_local_row(n, initial_local)
        assert values in witness_index
        lifts.append({'supported_boundary_row': row,
                      'completed_initial_local_row': initial_local,
                      'local_ear_fill_before_template_construction': local_fill,
                      'constructed_original_witness': values,
                      'original_edge_oracle_witness_index': witness_index[values]})
    dual = original_faces_and_dual(graph, geom, active)
    return stage | dual | {
        'state_id': 'U-' + '-'.join(map(str, sorted(active))),
        'same_root_canonical_geometry': geom,
        'common_original_hubs': hubs,
        'complete_original_edge_colorings': witnesses,
        'all_boundary_fibre_witness_indices_including_empty': fibres,
        'all_boundary_fibre_counts_including_zero': list(map(len, fibres)),
        'all_proper_remaining_graph_support_rows': support,
        'constructive_support_lifts': lifts,
        'three_branch_complete_common_witness_interfaces': full_joint_interfaces(
            graph, stage, n, witnesses),
    }


def audit_transition(graph, n, old, new, prior_ears, vertex):
    geom = compatible_geometry(graph, n, prior_ears, vertex)
    k = len(old['remaining_vertices'])
    assert geom['order'][k - 1] == vertex
    assert geom['steps'][k - 4]['m'] == 2
    assert geom['order'][:2] == [0, n - 1]
    for stage, prefix in ((old, k), (new, k - 1)):
        actual = exterior_stage(graph, geom, prefix)
        assert actual['boundary_scope'] == stage['boundary_scope']
        assert actual['exterior_edges'] == stage['exterior_edges']
    added = set(map(tuple, new['exterior_edges'])) - set(map(tuple, old['exterior_edges']))
    assert len(added) == 1
    p, q = next(iter(added))
    assert graph.has_edge(p, q)
    before, after = old['complete_original_edge_colorings'], new['complete_original_edge_colorings']
    assert [w for w in before if w[p] != w[q]] == after
    scope, old_scope = new['boundary_scope'], old['boundary_scope']
    after_index = {w: j for j, w in enumerate(after)}
    masks, complete_branches = [], []
    for row in itertools.product(COLORS, repeat=len(scope)):
        c = dict(zip(scope, row))
        branches_for_row, union = [], set()
        mask = 0
        for color in COLORS:
            old_row = tuple((c | {vertex: color})[v] for v in old_scope)
            ids = old['all_boundary_fibre_witness_indices_including_empty'][number(old_row)]
            allowed = c[p] != c[q]
            if allowed:
                if ids:
                    mask |= 1 << color
                union.update(before[j] for j in ids)
            # Include all four branches, even if the new-edge gate rejects them.
            branches_for_row.append({'eliminated_color': color, 'old_boundary_row': old_row,
                                     'new_edge_allows_branch': allowed,
                                     'all_old_original_witness_indices': ids})
        expected = {after[j] for j in new['all_boundary_fibre_witness_indices_including_empty'][number(row)]}
        assert union == expected
        assert bool(mask) == bool(expected)
        masks.append(mask)
        complete_branches.append(branches_for_row)
    new_support = set(map(tuple, new['all_proper_remaining_graph_support_rows']))
    old_support = set(map(tuple, old['all_proper_remaining_graph_support_rows']))
    lift_by_old = {tuple(l['supported_boundary_row']): l for l in old['constructive_support_lifts']}
    support_lifts = []
    for row in sorted(new_support):
        c = dict(zip(scope, row))
        assert c[p] != c[q]
        choices = []
        for color in COLORS:
            old_row = tuple((c | {vertex: color})[v] for v in old_scope)
            if old_row in old_support:
                w = tuple(lift_by_old[old_row]['constructed_original_witness'])
                assert w[p] != w[q] and w in after_index
                choices.append({'old_boundary_row': old_row,
                                'same_complete_original_witness': w,
                                'new_original_witness_index': after_index[w]})
        assert len(choices) == 2
        support_lifts.append({'new_boundary_row': row, 'two_supported_old_rows_and_witnesses': choices})
    for row in old_support:
        c = dict(zip(old_scope, row))
        assert c[p] != c[q]
        assert tuple(c[v] for v in scope) in new_support
        ids = old['all_boundary_fibre_witness_indices_including_empty'][number(row)]
        assert all(before[j] in after_index for j in ids)
    return {'old_state_id': old['state_id'], 'new_state_id': new['state_id'],
            'eliminated_vertex': vertex, 'added_original_edge': [p, q], 'm': 2,
            'same_fixed_root_canonical_geometry': geom,
            'all_transition_masks_including_zero': masks,
            'complete_old_fibre_branches_including_empty': complete_branches,
            'all_support_same_witness_old_row_lifts': support_lifts,
            'all_old_support_fibres_survive_new_edge': True}


def template_audit():
    rows = []
    for n, templates in ((6, SIX_RUNG_TEMPLATES), (8, EIGHT_RUNG_TEMPLATES)):
        graph = source_graph(n)
        constructed = all_constructed_initial_extensions(n)
        assert all(proper(graph.edges(), dict(enumerate(w))) for w in constructed)
        for key, (xs, ys, b) in templates.items():
            xs, ys = tuple(map(int, xs)), tuple(map(int, ys))
            assert (xs[-1], xs[2], ys[0]) == key
            checks = [xs[i] != 0 and ys[i] != b and xs[i] != ys[i]
                      and xs[i] != xs[(i + 1) % n]
                      and ys[i] != ys[(i + 1) % n]
                      and ys[i] != xs[(i + 1) % n] for i in range(n)]
            assert all(checks)
            reversible = n == 8 and xs[4] != xs[3] and ys[4] != ys[3] and ys[4] != xs[3]
            assert n == 6 or reversible
            rows.append({'n': n, 'normalized_ear_choices': key, 'X': xs, 'Y': ys, 'b': b,
                         'all_local_and_closing_edge_checks': checks,
                         'rungs_3_4_reversible': reversible})
    # Additional lengths test code implementing the symbolic repetition proof.
    for n in (10, 12, 20, 100):
        graph = source_graph(n)
        for w in all_constructed_initial_extensions(n):
            assert proper(graph.edges(), dict(enumerate(w)))
    return rows


def case_audit(n):
    graph = source_graph(n)
    geom = source_geometry(graph, n)
    fs = original_faces_from_rotation(graph, geom)
    cycles = short_cycle_sides(graph, fs)
    assert min(dict(graph.degree()).values()) == 5
    opening = []
    for k in range(len(graph) - 1, 6, -1):
        stage = exterior_stage(graph, geom, k)
        assert 1 in stage['unprocessed_interior_vertices']
        disk, _ = original_embedding_check(stage, geom['rotation_cw'])
        # Supply an explicit already-constructed shared witness at every opening.
        witness = all_constructed_initial_extensions(n)[0]
        assert proper(disk.edges(), dict(enumerate(witness)))
        opening.append(stage | {'same_explicit_original_witness': witness})
    assert geom['steps'][3]['vertex'] == n + 1 and geom['steps'][3]['m'] == 3
    constructed = all_constructed_initial_extensions(n)
    initial = sorted(initial_remaining(n))
    local = {tuple(w[v] for v in initial) for w in constructed}
    assert local == set(map(tuple, local_support(graph, initial, initial))) and len(local) == 192
    paths, transitions = fixed_root_state_graph(graph, n)
    states = {active: audit_stage(graph, n, active, path)
              for active, path in paths.items()}
    first = states[initial_remaining(n)]
    assert sorted(first['weak_dual_degrees']) == [1, 1, 1, 3]
    transfers = [audit_transition(graph, n, states[old], states[new], paths[old], v)
                 for old, new, v in transitions]
    return {'rim_size': n, 'original_vertices': sorted(graph),
            'original_edges': sorted(edge_set(graph)), 'original_faces': fs,
            'original_degrees': dict(graph.degree()), 'source_labels': branch_labels(n),
            'initial_canonical_geometry': geom,
            'short_cycle_original_sides': cycles,
            'actual_pre_saturation_stages': opening,
            'first_saturation_m3_step': geom['steps'][3],
            'constructed_initial_local_extensions': constructed,
            'all_fixed_root_saturated_states': list(states.values()),
            'all_fixed_root_legal_ear_transitions': transfers}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    templates = template_audit()
    cases = [case_audit(n) for n in (6, 8)]
    states = [s for c in cases for s in c['all_fixed_root_saturated_states']]
    transfers = [t for c in cases for t in c['all_fixed_root_legal_ear_transitions']]
    totals = {
        'original_graphs': len(cases), 'short_cycles_checked': sum(len(c['short_cycle_original_sides']) for c in cases),
        'fixed_root_states': len(states), 'fixed_root_ear_transitions': len(transfers),
        'complete_original_witnesses': sum(len(s['complete_original_edge_colorings']) for s in states),
        'all_boundary_fibres': sum(len(s['all_boundary_fibre_counts_including_zero']) for s in states),
        'empty_boundary_fibres': sum(s['all_boundary_fibre_counts_including_zero'].count(0) for s in states),
        'all_transition_masks': sum(len(t['all_transition_masks_including_zero']) for t in transfers),
        'zero_transition_masks': sum(t['all_transition_masks_including_zero'].count(0) for t in transfers),
        'supported_boundary_rows': sum(len(s['all_proper_remaining_graph_support_rows']) for s in states),
        'new_support_rows_lifted': sum(len(t['all_support_same_witness_old_row_lifts']) for t in transfers),
        'same_witness_old_support_row_lifts': 2 * sum(len(t['all_support_same_witness_old_row_lifts']) for t in transfers),
        'marginal_nonempty_joint_empty_rows': sum(len(s['three_branch_complete_common_witness_interfaces']['marginal_nonempty_but_joint_empty_rows']) for s in states),
        'complete_branch_interface_rows': sum(sum(len(t['all_path_fibres_common_omega_indices_including_empty']) for t in s['three_branch_complete_common_witness_interfaces']['branch_complete_interfaces']) for s in states),
        'empty_branch_interface_rows': sum(sum(sum(not ids for ids in t['all_path_fibres_common_omega_indices_including_empty']) for t in s['three_branch_complete_common_witness_interfaces']['branch_complete_interfaces']) for s in states),
        'common_exterior_assignments': sum(len(s['three_branch_complete_common_witness_interfaces']['all_proper_common_exterior_colorings']) for s in states),
        'explicit_normalized_templates': len(templates),
    }
    imported = [Path(__file__)] + [ROOT / 'scripts' / (name + '.py') for name in (
        'four_color_no_hub_three_branch_support', 'four_color_bond_perimeter_small_cuts',
        'four_color_shelling_fan_verification', 'four_color_shelling_verification',
        'four_color_saturated_hub_verification')]
    result = {'schema': 'four-color-no-hub-three-branch-v1',
              'scope': 'Specified A_n three-branch source; all local proper-four-color rows extend. No arbitrary-source nonemptiness theorem.',
              'networkx_version': nx.__version__,
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in imported},
              'normalized_template_checks': templates, 'totals': totals, 'cases': cases}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps(totals, sort_keys=True))


if __name__ == '__main__':
    main()
