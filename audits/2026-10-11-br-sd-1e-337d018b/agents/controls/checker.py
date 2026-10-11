#!/usr/bin/env python3
"""Five fixed small calibration fixtures; no source or size-class search."""
import argparse
import itertools
import json
import sys

BASE = '337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f'
COLORS = ['A', 'B', 'C', 'D']
B = ['B0', 'B1', 'B2', 'B3', 'B4']
BETA = dict(zip(B, [0, 1, 0, 1, 2]))


def canonical(data):
    return json.dumps(data, sort_keys=True, indent=2) + '\n'


def normalized(edges):
    return sorted([sorted(edge) for edge in edges])


def adjacency(vertices, edges):
    result = {v: set() for v in vertices}
    for a, b in edges:
        assert a != b and a in result and b in result
        assert b not in result[a]
        result[a].add(b)
        result[b].add(a)
    return result


def components(vertices, adj):
    unseen = set(vertices)
    result = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        todo = [root]
        component = []
        while todo:
            v = todo.pop()
            component.append(v)
            for w in sorted(adj[v]):
                if w in unseen:
                    unseen.remove(w)
                    todo.append(w)
        result.append(sorted(component))
    return sorted(result)


def blocks(vertices, edges):
    """Tarjan edge-stack blocks, derived from the complete C edges."""
    adj = adjacency(vertices, edges)
    timer = 0
    discovery, low = {}, {}
    stack, result = [], []
    def visit(v, parent):
        nonlocal timer
        timer += 1
        discovery[v] = low[v] = timer
        for w in sorted(adj[v]):
            if w == parent:
                continue
            edge = sorted([v, w])
            if w not in discovery:
                stack.append(edge)
                visit(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= discovery[v]:
                    block = []
                    while True:
                        popped = stack.pop()
                        block.append(popped)
                        if popped == edge:
                            break
                    result.append(sorted(block))
            elif discovery[w] < discovery[v]:
                stack.append(edge)
                low[v] = min(low[v], discovery[w])
    for v in vertices:
        if v not in discovery:
            visit(v, None)
    return sorted(result)


def complete_tuples(vertices, edges, lists):
    adj = adjacency(vertices, edges)
    order = sorted(vertices, key=lambda v: (len(lists[v]), -len(adj[v]), v))
    current, result = {}, []
    def visit(i):
        if i == len(order):
            result.append([current[v] for v in vertices])
            return
        v = order[i]
        for color in lists[v]:
            if all(current.get(w) != color for w in adj[v]):
                current[v] = color
                visit(i + 1)
                del current[v]
    visit(0)
    return sorted(result)


def graph_record(vertices, edges, named):
    adj = adjacency(vertices, edges)
    deletion = {v: components([w for w in vertices if w != v], adj) for v in vertices}
    cutpoints = [v for v in vertices if len(deletion[v]) > 1]
    bs = blocks(vertices, edges)
    assert sorted(normalized(es) for es in named.values()) == bs
    incident = {v: sorted(label for label, es in named.items()
                           if any(v in edge for edge in es)) for v in vertices}
    return {'vertex_order': vertices, 'all_edges': edges,
            'degree': {v: len(adj[v]) for v in vertices},
            'blocks': {label: {'vertices': sorted({v for e in es for v in e}),
                               'all_edges': normalized(es)} for label, es in sorted(named.items())},
            'incident_blocks': incident, 'cutpoints': cutpoints,
            'all_vertex_deletion_components': deletion}


def triangle(a, b, c):
    return normalized([[a, b], [b, c], [c, a]])


def source_like_fixture(name, branch_at):
    named = {'J1': triangle('r', 'a1', 'w1'),
             'J2': triangle('r', 'u', 'w2'),
             'J3': triangle('v', 'a3', 'w3'),
             'uv': [['u', 'v']], 'a3t': [['a3', 't']], 'tq': [['t', 'q']],
             'Wcycle': triangle(branch_at, 'y', 'z')}
    edges = normalized([edge for es in named.values() for edge in es])
    C = sorted({v for edge in edges for v in edge})
    graph = graph_record(C, edges, named)
    contacts = ['a1', 'q']
    attachments = {}
    for v in C:
        k = 4 - graph['degree'][v] - int(v in contacts)
        assert 0 <= k <= 2
        attachments[v] = ['B4'] if v == 'a1' else B[:k]
    M_vertices = sorted(B + ['s'] + C)
    frame = [[B[i], B[(i + 1) % 5]] for i in range(5)]
    M_edges = normalized(edges + frame + [['s', v] for v in contacts]
                         + [['s', b] for b in ['B0', 'B1', 'B4']]
                         + [[v, b] for v, bs in attachments.items() for b in bs])
    M_adj = adjacency(M_vertices, M_edges)
    assert all(len(M_adj[v]) == 4 for v in C)
    assert len(M_adj['s']) == 5
    lists = {v: [c for c in range(4) if c not in {BETA[b] for b in attachments[v]}
                 and not (v in contacts and c == 3)] for v in C}
    assert all(len(lists[v]) >= graph['degree'][v] for v in C)
    tuples = complete_tuples(C, edges, lists)
    full_M = []
    for tup in tuples:
        coloring = dict(zip(C, tup)) | BETA | {'s': 3}
        assert all(coloring[a] != coloring[b] for a, b in M_edges)
        full_M.append([coloring[v] for v in M_vertices])
    G_edges = normalized(M_edges + [['r', 'B2']])
    full_G = [tup for tup in full_M if all(dict(zip(M_vertices, tup))[a]
              != dict(zip(M_vertices, tup))[b] for a, b in G_edges)]
    components_LS = components([v for v in C if v != 'r'], adjacency(C, edges))
    L = next(comp for comp in components_LS if 'a1' in comp)
    S = next(comp for comp in components_LS if 'q' in comp)
    supports = {key: sorted({b for v in piece for b in attachments[v]})
                for key, piece in [('L', L), ('S', S)]}
    assert supports['S'] == ['B0', 'B1']
    witnesses = {}
    for v, label in [('w1', 'J1'), ('w2', 'J2')]:
        witnesses[v] = {'noncutpoint': v not in graph['cutpoints'],
                        'not_s_contact': v not in contacts,
                        'only_block_is_named_cycle': graph['incident_blocks'][v] == [label],
                        'degree_C_two': graph['degree'][v] == 2,
                        'D_in_list': 3 in lists[v],
                        'all_boundary_colors_avoid_D': all(BETA[b] != 3 for b in attachments[v])}
    fibres = [{'ordered_contact_tuple': list(pair),
               'complete_C_coloring_tuples': [t for t in tuples if [t[C.index(v)] for v in contacts] == list(pair)]}
              for pair in itertools.product(range(4), repeat=2)]
    preservation = all(all(record.values()) for record in witnesses.values())
    return {'name': name, 'kind': 'synthetic fixed M/G local-degree calibration',
            'C': graph, 'ordered_frame': B, 'literal_beta': BETA, 'literal_colors': COLORS,
            'M_vertex_order': M_vertices, 'all_M_edges': M_edges, 'all_G_edges': G_edges,
            'omitted_original_edge_e': ['B2', 'r'], 'ordered_s_contacts': contacts,
            's_boundary_spokes': ['B0', 'B1', 'B4'],
            'all_boundary_attachments': attachments, 'all_LD_lists': lists,
            'degree_M': {v: len(M_adj[v]) for v in M_vertices},
            'LS_ownership': {'L': L, 'S': S}, 'actual_synthetic_supports': supports,
            'W': {'off_skeleton_vertices': ['y', 'z'], 'attachment_x': branch_at,
                  'all_incident_edges': named['Wcycle'],
                  'off_skeleton_connected': True, 'single_skeleton_contact': True},
            'rotation': None, 'rotation_status': 'not provided; no disk source is claimed',
            'private_witness_checks': witnesses,
            'private_witness_preservation_status': 'triggered and holds' if preservation else 'counterexample',
            'complete_C_LD_coloring_tuples': tuples,
            'all_ordered_contact_fibres_including_empty': fibres,
            'complete_ordered_contact_relation': [f['ordered_contact_tuple'] for f in fibres if f['complete_C_coloring_tuples']],
            'complete_M_beta_lift_tuples': sorted(full_M), 'complete_G_beta_lift_tuples': sorted(full_G),
            'M_accepts_beta': bool(full_M),
            'source_contract_status': 'not triggered',
            'missing_source_prerequisites': ['disk embedding and rotation', 'complete Sigma 933/941 or whole-graph D5 image',
                'epsilon=2', 'Sigma-critical retained-edge witnesses', 'M beta rejection and inclusion-minimality',
                'original N45 ownership provenance and complete relations/full lifts beyond this fixed beta']}


def saturated_control():
    named = {'J1': triangle('r', 'a1', 'w1'), 'J2': triangle('r', 'u', 'w2'),
             'J3': triangle('q', 'j3a', 'j3b'), 'uq': [['u', 'q']]}
    edges = normalized([e for es in named.values() for e in es])
    vertices = sorted({v for e in edges for v in e})
    graph = graph_record(vertices, edges, named)
    assert graph['degree']['q'] == 3
    return {'name': 'saturated-q-equals-a3-equals-v', 'kind': 'structural local degree negative',
            'C_before_W': graph, 'equalities': {'q': 'q', 'a3': 'q', 'v': 'q'},
            'named_s_contact': 'q', 'd_C_before_W': 3, 's_contact_indicator': 1,
            'boundary_attachment_count_before_W': 0, 'required_degree_M': 4,
            'minimum_W_incidence': 1, 'degree_M_after_nonempty_W_at_least': 5,
            'status': 'triggered and holds', 'result': 'every nonempty W at this x violates degree4',
            'lists': None, 'boundary_assignments': None, 'rotation': None,
            'source_contract_status': 'not triggered'}


def cutpoint_control():
    named = {'triangle': triangle('x', 'a', 'b'), 'bridge': [['x', 'y']]}
    edges = normalized([e for es in named.values() for e in es])
    vertices = ['a', 'b', 'x', 'y']
    graph = graph_record(vertices, edges, named)
    palettes = {'triangle': [0, 1], 'bridge': [3]}
    lists = {v: sorted({c for block in graph['incident_blocks'][v] for c in palettes[block]}) for v in vertices}
    assert all(len(lists[v]) == graph['degree'][v] for v in vertices)
    assert all(set(palettes[a]).isdisjoint(palettes[b]) for v in vertices
               for a, b in itertools.combinations(graph['incident_blocks'][v], 2))
    tuples = complete_tuples(vertices, edges, lists)
    assert not tuples
    return {'name': 'cutpoint-D-is-only-in-pendant-bridge', 'kind': 'abstract list fixture',
            'C': graph, 'literal_colors': COLORS, 'all_lists': lists, 'block_palettes': palettes,
            'complete_coloring_tuples': tuples, 'named_cutpoint': 'x',
            'D_in_cutpoint_list': 3 in lists['x'], 'D_in_cycle_palette': 3 in palettes['triangle'],
            'D_in_bridge_palette': 3 in palettes['bridge'], 'status': 'counterexample',
            'refuted_statement': 'D in a cutpoint list forces D in every incident cycle palette',
            'boundary_assignments': None, 'attachments': None, 'rotation': None,
            'source_contract_status': 'not triggered'}


def build():
    fixtures = [source_like_fixture('W-triangle-at-J3-ordinary-w3', 'w3'),
                source_like_fixture('W-triangle-at-q-endpoint', 'q'),
                source_like_fixture('W-triangle-at-q-arm-interior-t', 't'),
                source_like_fixture('forbidden-W-at-J1-unique-triangle-witness-w1', 'w1')]
    assert all(f['private_witness_preservation_status'] == 'triggered and holds' for f in fixtures[:3])
    assert fixtures[3]['private_witness_preservation_status'] == 'counterexample'
    assert all(f['M_accepts_beta'] for f in fixtures)
    return {'base': BASE, 'scope': 'six fixed minimal calibration records; no size-class/source enumeration',
            'actual_target_source_status': 'not triggered', 'actual_target_source_count': 0,
            'source_like_fixtures': fixtures, 'saturated_local_degree_control': saturated_control(),
            'unsupported_cutpoint_inference_negative': cutpoint_control()}


def check_submitted_tuples(data):
    for fixture in data['source_like_fixtures']:
        C = fixture['C']['vertex_order']
        for tup in fixture['complete_C_LD_coloring_tuples']:
            assert len(tup) == len(C), 'incomplete coloring tuple'
            assert all(type(c) is int and c in range(4) for c in tup), 'illegal complete coloring tuple'
            coloring = dict(zip(C, tup))
            assert all(coloring[v] in fixture['all_LD_lists'][v] for v in C), 'list violation'
            assert all(coloring[a] != coloring[b] for a, b in fixture['C']['all_edges']), 'edge violation'


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--write', action='store_true')
    action.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', required=True)
    args = parser.parse_args()
    if args.write:
        expected = build()
        with open(args.certificate, 'x') as output:
            output.write(canonical(expected))
    else:
        with open(args.certificate) as source:
            submitted = json.load(source)
        check_submitted_tuples(submitted)
        expected = build()
        assert canonical(submitted) == canonical(expected), 'certificate mismatch'
    print(json.dumps({'status': 'triggered and holds', 'actual_target_source_status': 'not triggered',
                      'fixture_count': 6,
                      'C_LD_tuple_counts': [len(f['complete_C_LD_coloring_tuples']) for f in expected['source_like_fixtures']],
                      'M_beta_lift_counts': [len(f['complete_M_beta_lift_tuples']) for f in expected['source_like_fixtures']],
                      'private_witness_statuses': [f['private_witness_preservation_status'] for f in expected['source_like_fixtures']]}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ValueError, KeyError, TypeError, IndexError) as error:
        print('FAIL: ' + repr(error), file=sys.stderr)
        raise SystemExit(1)
