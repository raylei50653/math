#!/usr/bin/env python3
"""Fixed BR-SD-1g calibrations. No search for, or assertion of, actual sources."""
import argparse
import hashlib
import itertools
import json
import random
import sys

BASE = 'dbdc4c35f785519c8e3cb0260807f0d2feb82469'
B = ['B0', 'B1', 'B2', 'B3', 'B4']
BETA = dict(zip(B, [0, 1, 0, 1, 2]))
COL = [0, 1, 2, 3]
SEED = None


def canonical(value):
    return json.dumps(value, sort_keys=True, indent=2) + '\n'


def norm(edges):
    result = sorted([sorted(e) for e in edges])
    assert len(result) == len({tuple(e) for e in result})
    return result


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        assert a != b and a in adj and b in adj and b not in adj[a]
        adj[a].add(b)
        adj[b].add(a)
    return adj


def components(vertices, adj):
    unseen = set(vertices)
    found = []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
        todo, current = [first], []
        while todo:
            v = todo.pop()
            current.append(v)
            for w in sorted(adj[v]):
                if w in unseen:
                    unseen.remove(w)
                    todo.append(w)
        found.append(sorted(current))
    return sorted(found)


def tarjan_blocks(vertices, edges):
    adj = adjacency(vertices, edges)
    seen, low, stack, answer = {}, {}, [], []
    def visit(v, parent):
        seen[v] = low[v] = len(seen)
        for w in sorted(adj[v]):
            e = sorted([v, w])
            if w == parent:
                continue
            if w not in seen:
                stack.append(e)
                visit(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= seen[v]:
                    block = []
                    while True:
                        last = stack.pop()
                        block.append(last)
                        if last == e:
                            break
                    answer.append(norm(block))
            elif seen[w] < seen[v]:
                stack.append(e)
                low[v] = min(low[v], seen[w])
    for v in vertices:
        if v not in seen:
            visit(v, None)
    return sorted(answer)


def full_tuples(vertices, edges, lists):
    adj = adjacency(vertices, edges)
    rng = random.Random(SEED)
    shuffled = list(vertices)
    rng.shuffle(shuffled)
    tie = {v: i for i, v in enumerate(shuffled)}
    order = sorted(vertices, key=lambda v: (len(lists[v]), -len(adj[v]), tie[v]))
    assignment, answer = {}, []
    def visit(i):
        if i == len(order):
            answer.append([assignment[v] for v in vertices])
            return
        v = order[i]
        colors = list(lists[v])
        rng.shuffle(colors)
        for c in colors:
            if all(assignment.get(w) != c for w in adj[v]):
                assignment[v] = c
                visit(i + 1)
                del assignment[v]
    visit(0)
    return sorted(answer)


def graph_record(vertices, edges, named):
    adj = adjacency(vertices, edges)
    assert sorted(norm(es) for es in named.values()) == tarjan_blocks(vertices, edges)
    incident = {v: sorted(k for k, es in named.items() if any(v in e for e in es)) for v in vertices}
    deletion = {v: components([w for w in vertices if w != v], adj) for v in vertices}
    return {'vertex_order': vertices, 'all_edges': edges,
            'degree': {v: len(adj[v]) for v in vertices},
            'all_vertex_deletion_components': deletion,
            'cutpoints': [v for v in vertices if len(deletion[v]) > 1],
            'incident_blocks': incident,
            'blocks': {k: {'vertices': sorted({v for e in es for v in e}), 'all_edges': norm(es)}
                       for k, es in sorted(named.items())}}


def triangle(a, b, c):
    return norm([[a, b], [b, c], [c, a]])


def beta_lifts(vertices, edges):
    adj = adjacency(vertices, edges)
    internal = [v for v in vertices if v not in B]
    lists = {v: [c for c in COL if c not in {BETA[b] for b in adj[v] if b in B}]
             for v in internal}
    internal_edges = [e for e in edges if all(v in internal for v in e)]
    tuples = full_tuples(internal, internal_edges, lists)
    answer = []
    for tup in tuples:
        assignment = BETA | dict(zip(internal, tup))
        assert all(assignment[a] != assignment[b] for a, b in edges)
        answer.append([assignment[v] for v in vertices])
    return sorted(answer)


def palette_assignments(graph, lists):
    incident = graph['incident_blocks']
    bs = graph['blocks']
    choices = {}
    for label, block in bs.items():
        vertices = block['vertices']
        size = 1 if len(block['all_edges']) == 1 else 2
        intersection = set(COL).intersection(*(set(lists[v]) for v in vertices))
        choices[label] = [list(p) for p in itertools.combinations(sorted(intersection), size)]
    order = sorted(bs, key=lambda k: (len(choices[k]), k))
    current, found = {}, []
    def visit(i):
        if i == len(order):
            if all(set(lists[v]) == {c for k in incident[v] for c in current[k]} for v in lists):
                found.append(dict(current))
            return
        k = order[i]
        for p in choices[k]:
            if all(set(p).isdisjoint(current[j]) for v in bs[k]['vertices']
                   for j in incident[v] if j in current):
                current[k] = p
                visit(i + 1)
                del current[k]
    visit(0)
    return {'all_block_palette_candidates': choices, 'complete_compatible_palette_assignments': found,
            'status': 'triggered and holds',
            'claim': 'finite fixed-graph palette search only; no arbitrary-size theorem'}


def fixture(name, p_length, q_length, W2_at, W2_shape):
    named = {'J1': triangle('r', 'a1', 'x1'), 'J2': triangle('r', 'u', 'w2'),
             'J3': triangle('v', 'a3', 'w3'), 'uv': [['u', 'v']],
             'W1cycle': triangle('x1', 'Y1', 'Z1')}
    p_arm = ['a1'] + (['p'] if p_length == 1 else [])
    q_arm = ['a3'] + ([f't{i}' for i in range(1, q_length)] + ['q'] if q_length else [])
    p, q = p_arm[-1], q_arm[-1]
    for prefix, arm in [('p', p_arm), ('q', q_arm)]:
        for i, (a, b) in enumerate(zip(arm, arm[1:])):
            named[f'{prefix}arm{i}'] = [[a, b]]
    x = {'ordinary-J3': 'w3', 'v': 'v', 'a3': 'a3', 'q': q, 'arm-interior': 't1'}[W2_at]
    if W2_shape == 'triangle':
        named['W2cycle'] = triangle(x, 'Y2', 'Z2')
        W2 = ['Y2', 'Z2']
    else:
        named['W2stem'] = [[x, 'Y2']]
        named['W2cycle'] = triangle('Y2', 'Z2', 'T2')
        W2 = ['T2', 'Y2', 'Z2']
    edges = norm([e for es in named.values() for e in es])
    C = sorted({v for e in edges for v in e})
    graph = graph_record(C, edges, named)
    cadj = adjacency(C, edges)
    LS = components([v for v in C if v != 'r'], cadj)
    L = next(comp for comp in LS if p in comp)
    S = next(comp for comp in LS if q in comp)
    assert len(LS) == 2 and all(y in L for y in ['Y1', 'Z1']) and all(y in S for y in W2)
    attachments = {}
    for v in C:
        k = 4 - len(cadj[v]) - int(v in [p, q])
        assert 0 <= k <= 2, (name, v, k)
        attachments[v] = (['B4'] if k == 1 and v == 'a1' else B[:k])
    lists = {v: [c for c in COL if c not in {BETA[b] for b in attachments[v]}
                 and not (v in [p, q] and c == 3)] for v in C}
    assert all(len(lists[v]) >= len(cadj[v]) for v in C)
    assert all({2, 3}.issubset(lists[v]) for v in S if v != q)
    assert 2 in lists[q] and 3 not in lists[q]
    frame = norm([[B[i], B[(i + 1) % 5]] for i in range(5)])
    vertices = sorted(B + ['s'] + C)
    M_edges = norm(edges + frame + [['s', p], ['s', q]]
                   + [['s', b] for b in ['B0', 'B1', 'B4']]
                   + [[v, b] for v, bs in attachments.items() for b in bs])
    G_edges = norm(M_edges + [['r', 'B2']])
    madj, gadj = adjacency(vertices, M_edges), adjacency(vertices, G_edges)
    assert all(len(madj[v]) == 4 for v in C) and len(madj['s']) == 5
    assert sum(len(gadj[v]) - 4 for v in C + ['s']) == 2
    tuples = full_tuples(C, edges, lists)
    full_M, full_G = beta_lifts(vertices, M_edges), beta_lifts(vertices, G_edges)
    expected_M = sorted([[((BETA | {'s': 3} | dict(zip(C, tup)))[v]) for v in vertices] for tup in tuples])
    assert full_M == expected_M
    fibres = [{'ordered_pq_tuple': list(pin),
               'complete_C_tuples': [t for t in tuples if [t[C.index(p)], t[C.index(q)]] == list(pin)],
               'complete_M_tuples': [t for t in full_M if [t[vertices.index(p)], t[vertices.index(q)]] == list(pin)],
               'complete_G_tuples': [t for t in full_G if [t[vertices.index(p)], t[vertices.index(q)]] == list(pin)]}
              for pin in itertools.product(COL, repeat=2)]
    # These fixtures accept beta, so they fail the original rejection/minimality
    # premise immediately. Do not pretend their edge witnesses certify a source.
    minimal = False
    palette = palette_assignments(graph, lists)
    assert graph['incident_blocks']['x1'] == ['J1', 'W1cycle']
    assert 'x1' in graph['cutpoints'] and graph['incident_blocks']['w2'] == ['J2']
    supports = {key: sorted({b for v in piece for b in attachments[v]}) for key, piece in [('L', L), ('S', S)]}
    assert supports['S'] == ['B0', 'B1']
    degrees = {v: {'d_C': len(cadj[v]), 'B_attachments': attachments[v],
                  's_contact_indicator': int(v in [p, q]), 'complete_degree_M': len(madj[v]),
                  'ownership': 'root' if v == 'r' else 'L' if v in L else 'S'} for v in C}
    return {'name': name, 'kind': 'synthetic complete finite G/M graph calibration',
            'construction_rule': 'build C including both branches first, then specify all original attachments once; no old full-degree source is edited',
            'C': graph, 'ordered_frame': B, 'literal_beta': BETA, 'literal_colors': ['A', 'B', 'T', 'D'],
            'M_G_vertex_order': vertices, 'all_M_edges': M_edges, 'all_G_edges': G_edges,
            'original_deleted_spoke_e': ['B2', 'r'], 'p_arm': p_arm, 'q_arm': q_arm,
            'ordered_s_contacts': [p, q], 's_boundary_spokes': ['B0', 'B1', 'B4'],
            'all_degree_attachment_ownership_rows': degrees, 'all_boundary_attachments': attachments,
            'LS_ownership': {'L': L, 'S': S}, 'actual_synthetic_supports': supports,
            'W1': {'vertices': ['Y1', 'Z1'], 'single_attachment_x': 'x1', 'all_edges': named['W1cycle'], 'ownership': 'L'},
            'W2': {'vertices': W2, 'single_attachment_x': x,
                   'all_edges': norm(named['W2cycle'] + named.get('W2stem', [])), 'ownership': 'S'},
            'unique_J1_original_private_witness': 'x1', 'J1_witness_preservation': 'counterexample',
            'J2_unchanged_private_witness': 'w2', 'J2_witness_preservation': 'triggered and holds',
            'all_LD_lists': lists, 'complete_C_LD_coloring_tuples': tuples,
            'complete_M_beta_lift_tuples': full_M, 'complete_G_beta_lift_tuples': full_G,
            'all_16_ordered_pq_fibres_including_empty': fibres,
            'complete_ordered_pq_relation': [f['ordered_pq_tuple'] for f in fibres if f['complete_M_tuples']],
            'full_extension_equivalence': 'triggered and holds', 'finite_palette_search': palette,
            'exclusive_T_D_route_premises': {
                'status': 'triggered and holds', 'same_literal_T': 2, 'same_literal_D': 3,
                'all_S_non_q_lists_contain_T_and_D': all({2, 3}.issubset(lists[v]) for v in S if v != q),
                'q_list_contains_T_and_omits_D': 2 in lists[q] and 3 not in lists[q],
                'untouched_J2_private_witness': 'w2', 'w2_list_equals_T_D': lists['w2'] == [2, 3],
                'J2_palette_candidates': palette['all_block_palette_candidates']['J2'],
                'only_L_S_exit_vertex': 'r', 'J2_incident_at_r': 'J2' in graph['incident_blocks']['r'],
                'first_q_incident_palette_candidates': {
                    k: palette['all_block_palette_candidates'][k] for k in graph['incident_blocks'][q]},
                'finite_complete_palette_assignment_count': len(palette['complete_compatible_palette_assignments']),
                'unbounded_alternating_incidence_tree_theorem_status': 'not triggered by finite controls'},
            'M_rejects_literal_beta': not full_M, 'M_beta_inclusion_minimal': minimal,
            'retained_edge_source_witness_status': 'not triggered: no original source and M already accepts beta',
            'local_degrees_pair_support_ownership': 'triggered and holds',
            'numeric_epsilon_G': 2, 'rotation': None, 'disk_embedding': None,
            'source_contract_status': 'not triggered',
            'missing_source_prerequisites': ['actual original disk/rotation provenance', 'complete Sigma 933/941 or common whole-graph D5 image',
                                            'original G per-nonframe-edge Sigma-critical witnesses',
                                            'original N45 piece/attachment provenance', 'M beta rejection and inclusion minimality',
                                            'all ordered boundary relations and fibres beyond the one fixed literal beta']}


def abstract_palette_control(name, named, palettes, contacts, refuted):
    edges = norm([e for es in named.values() for e in es])
    vertices = sorted({v for e in edges for v in e})
    graph = graph_record(vertices, edges, named)
    lists = {v: sorted({c for k in graph['incident_blocks'][v] for c in palettes[k]}) for v in vertices}
    assert all(len(lists[v]) == graph['degree'][v] for v in vertices)
    assert all(set(palettes[k]).isdisjoint(palettes[j]) for v in vertices
               for k, j in itertools.combinations(graph['incident_blocks'][v], 2))
    tuples = full_tuples(vertices, edges, lists)
    assert not tuples
    return {'name': name, 'kind': 'abstract fixed list/palette inference negative', 'C': graph,
            'all_lists': lists, 'all_block_palettes': palettes, 'declared_s_contacts': contacts,
            'complete_C_list_coloring_tuples': tuples, 'status': 'counterexample',
            'refuted_statement': refuted, 'boundary_attachments': None, 'rotation': None,
            'source_contract_status': 'not triggered'}


def negatives(f):
    branch = abstract_palette_control('W1-can-carry-D-without-J1-carrying-D',
        {'J1': triangle('r', 'a1', 'x1'), 'J2': triangle('r', 'u', 'w2'),
         'W1': triangle('x1', 'y', 'z')},
        {'J1': [0, 1], 'J2': [2, 3], 'W1': [2, 3]}, ['a1'],
        'D in the occupied J1 cutpoint list forces D in J1 palette')
    branch['D_in_x1_list'] = True
    branch['D_in_J1_palette'] = False
    branch['D_in_W1_palette'] = True
    first = abstract_palette_control('first-branch-block-may-omit-D',
        {'firstbridge': [['x', 'y']], 'leafcycle': triangle('y', 'z', 'w')},
        {'firstbridge': [0], 'leafcycle': [2, 3]}, [],
        'a finite pair-supported branch with no s-contact must put D in its first block')
    first['qualifier'] = 'root x also has unseen skeleton blocks; only branch-side incident lists are displayed at x'
    first['local_original_attachments_on_W'] = {'y': ['B1'], 'z': ['B0', 'B1'], 'w': ['B0', 'B1']}
    first['W_complete_degree_rows'] = {'y': {'d_C': 3, 'k': 1, 't': 0, 'sum': 4},
                                      'z': {'d_C': 2, 'k': 2, 't': 0, 'sum': 4},
                                      'w': {'d_C': 2, 'k': 2, 't': 0, 'sum': 4}}
    saturated = {'name': 'saturated-old-witness-cannot-gain-a-branch',
        'before': {'d_C': 2, 'original_B_attachments': ['B0', 'B1'], 't': 0, 'degree_M': 4},
        'minimum_new_C_edge_count': 1, 'after_complete_degree_at_least': 5,
        'status': 'triggered and holds', 'source_contract_status': 'not triggered'}
    fraud = {'name': 'deleting-original-attachment-to-fake-capacity',
        'before': saturated['before'], 'claimed_after': {'d_C': 3, 'B_attachments': ['B0'], 't': 0, 'sum': 4},
        'lost_original_edge': ['B1', 'old-witness'], 'same_original_attachments_preserved': False,
        'first_failure': 'original attachment identity is deleted before degree is repaired',
        'status': 'triggered and holds', 'source_contract_status': 'not triggered'}
    supports = {'name': 'wrong-actual-support-despite-degree-legality', 'required_actual_pair': ['B0', 'B1'],
        'original_vertex': 'w2', 'original_attachments': ['B0', 'B1'],
        'invalid_replacement_attachments': ['B0', 'B4'], 'degree_count_before_and_after': 2,
        'computed_invalid_S_support': ['B0', 'B1', 'B4'], 'status': 'triggered and holds',
        'first_failure': 'actual S boundary-neighbor set is not the prescribed two original frame endpoints',
        'source_contract_status': 'not triggered'}
    marginal = {'name': 'marginals-discard-complete-lift-correlations',
        'vertex_order': ['a', 'b'], 'all_edges': [['a', 'b']], 'all_lists': {'a': [0, 1], 'b': [0, 1]},
        'complete_coloring_tuples': [[0, 1], [1, 0]], 'both_coordinate_marginals': [[0, 1], [0, 1]],
        'false_marginally_admitted_tuple': [0, 0], 'status': 'counterexample',
        'refuted_statement': 'independent nonempty marginals are a complete edge-compatible lift',
        'source_contract_status': 'not triggered'}
    K5 = [f'K{i}' for i in range(5)]
    mv = sorted(B + K5 + ['a', 'b'])
    me = norm([[B[i], B[(i + 1) % 5]] for i in range(5)]
              + [list(e) for e in itertools.combinations(K5, 2)] + [['a', 'b']]
              + [[v, boundary] for v in ['a', 'b'] for boundary in ['B0', 'B1', 'B4']])
    missing_edge = ['K0', 'K1']
    maj = adjacency(mv, me)
    before = beta_lifts(mv, me)
    after = beta_lifts(mv, [e for e in me if e != missing_edge])
    assert not before and not after and all(len(maj[v]) == 4 for v in K5 + ['a', 'b'])
    minimal = {'name': 'beta-rejection-and-local-degree-do-not-imply-M-minimality',
        'kind': 'independent synthetic implication negative outside the 1g skeleton',
        'M_vertex_order': mv, 'all_M_edges': me, 'literal_beta': BETA,
        'all_internal_degrees': {v: len(maj[v]) for v in K5 + ['a', 'b']},
        'complete_M_beta_lift_tuples': before, 'deleted_original_edge': missing_edge,
        'complete_deleted_edge_beta_lift_tuples': after,
        'M_rejects_literal_beta': True, 'M_beta_inclusion_minimal': False,
        'status': 'counterexample', 'source_contract_status': 'not triggered',
        'missing_source_prerequisites': ['sole connected C', '1g skeleton', 'r/s roots', 'disk embedding', 'Sigma criticality'],
        'refuted_statement': 'beta rejection plus numeric degrees automatically supplies all retained-edge beta witnesses'}
    capacity = []
    for label, d0, t in [('q=a3=v, q-arm-zero', 3, 1), ('a3=v, q-arm-positive', 4, 0)]:
        capacity.append({'name': label, 'd_C_skeleton': d0, 's_contact_indicator': t,
                         'minimum_W2_incidence': 1, 'minimum_degree_without_any_B_attachment': d0 + t + 1,
                         'status': 'triggered and holds', 'source_contract_status': 'not triggered'})
    return {'cutpoint_and_W1_D_routing': branch, 'first_branch_D_overstatement': first,
            'saturated_illegal_addition': saturated, 'removed_original_attachment_fraud': fraud,
            'actual_pair_support_failure': supports, 'marginal_full_lift_negative': marginal,
            'M_minimality_omission': minimal, 'forbidden_named_overlap_capacity': capacity}


def build():
    specs = [('all-triangles-p0-q0-W2-at-J3-witness', 0, 0, 'ordinary-J3', 'triangle'),
             ('all-triangles-p1-q0-W2-at-v', 1, 0, 'v', 'stem-triangle'),
             ('all-triangles-p0-q1-W2-at-a3', 0, 1, 'a3', 'stem-triangle'),
             ('all-triangles-p1-q2-W2-at-arm-interior', 1, 2, 'arm-interior', 'triangle'),
             ('all-triangles-p0-q1-W2-at-q-direct-cycle', 0, 1, 'q', 'triangle'),
             ('all-triangles-p1-q2-W2-at-q-stem-cycle', 1, 2, 'q', 'stem-triangle')]
    fixtures = [fixture(*spec) for spec in specs]
    assert all(not f['M_rejects_literal_beta'] for f in fixtures)
    assert all(not f['finite_palette_search']['complete_compatible_palette_assignments'] for f in fixtures)
    return {'base': BASE, 'format': 'BR-SD-1g-controls-v1', 'traversal_seed': SEED,
            'scope': 'six fixed named finite graph fixtures and explicit inference negatives; no source enumeration',
            'actual_target_source_count': 0, 'actual_target_source_status': 'not triggered',
            'source_like_fixtures': fixtures, 'negative_controls': negatives(fixtures[0]),
            'new_unconditional_parent_identity_closure_count': 0}


def main():
    global SEED
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', required=True)
    args = parser.parse_args()
    SEED = args.seed
    expected = build()
    if args.write:
        with open(args.certificate, 'x') as output:
            output.write(canonical(expected))
    else:
        with open(args.certificate) as source:
            submitted = json.load(source)
        assert canonical(submitted) == canonical(expected), 'certificate disagrees with complete recomputation'
    print(json.dumps({'status': 'triggered and holds', 'actual_target_source_status': 'not triggered',
                      'fixed_fixture_count': len(expected['source_like_fixtures']),
                      'C_tuple_counts': [len(f['complete_C_LD_coloring_tuples']) for f in expected['source_like_fixtures']],
                      'M_beta_minimality': [f['M_beta_inclusion_minimal'] for f in expected['source_like_fixtures']],
                      'sha256': hashlib.sha256(canonical(expected).encode()).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ValueError, KeyError, TypeError, IndexError) as error:
        print('FAIL: ' + repr(error), file=sys.stderr)
        raise SystemExit(1)
