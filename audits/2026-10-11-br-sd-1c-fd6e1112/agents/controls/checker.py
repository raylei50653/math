#!/usr/bin/env python3
"""Tiny BR-SD-1c literal-edge controls. No imported repository solver/source."""
import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

COLORS = ['A', 'B', 'C', 'D']
D = 3
BASE = 'fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69'
ROOT = Path(__file__).resolve().parents[4]


def e(a, b):
    assert a != b
    return tuple(sorted((a, b)))


def neighbors(vertices, edges):
    adj = {v: set() for v in vertices}
    assert len(adj) == len(vertices)
    for a, b in edges:
        assert a in adj and b in adj and a != b
        adj[a].add(b)
        adj[b].add(a)
    return adj


def components(vertices, edges):
    adj = neighbors(vertices, edges)
    unseen = set(vertices)
    out = []
    while unseen:
        todo = [min(unseen)]
        unseen.remove(todo[0])
        found = []
        while todo:
            v = todo.pop()
            found.append(v)
            for w in sorted(adj[v]):
                if w in unseen:
                    unseen.remove(w)
                    todo.append(w)
        out.append(sorted(found))
    return sorted(out)


def edge_blocks(vertices, edges):
    """Fresh Tarjan decomposition reads only original graph edges."""
    adj = neighbors(vertices, edges)
    discovery, low = {}, {}
    stack, blocks = [], []
    def dfs(v, parent):
        discovery[v] = low[v] = len(discovery)
        for w in sorted(adj[v]):
            if w == parent:
                continue
            if w not in discovery:
                stack.append(e(v, w))
                dfs(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= discovery[v]:
                    block = []
                    while True:
                        item = stack.pop()
                        block.append(item)
                        if item == e(v, w):
                            break
                    blocks.append(sorted(block))
            elif discovery[w] < discovery[v]:
                stack.append(e(v, w))
                low[v] = min(low[v], discovery[w])
    for v in vertices:
        if v not in discovery:
            dfs(v, None)
    assert not stack
    return sorted(blocks)


def all_colorings(vertices, edges, lists):
    """Complete tuples from original edge inequalities; no block solvers."""
    adj = neighbors(vertices, edges)
    order = list(vertices)
    where = {v: i for i, v in enumerate(order)}
    adjacent_indices = [[where[w] for w in sorted(adj[v])] for v in order]
    allowed = [list(lists[v]) for v in order]
    current = [-1] * len(order)
    result, count = [], 0
    def visit():
        nonlocal count
        count += 1
        unassigned = [i for i, color in enumerate(current) if color < 0]
        if not unassigned:
            result.append(current.copy())
            return
        candidates = []
        for i in unassigned:
            forbidden = {current[j] for j in adjacent_indices[i] if current[j] >= 0}
            options = [c for c in allowed[i] if c not in forbidden]
            if not options:
                return
            candidates.append((len(options), -len(adj[order[i]]), i, options))
        _, _, i, options = min(candidates)
        for c in options:
            current[i] = c
            visit()
            current[i] = -1
    visit()
    return sorted(result), count


def check_tuple(vertices, edges, lists, tup):
    assert len(tup) == len(vertices)
    asg = dict(zip(vertices, tup))
    assert all(c in lists[v] for v, c in asg.items()), 'illegal complete coloring tuple'
    assert all(asg[a] != asg[b] for a, b in edges), 'original-edge conflict'


def make_C(branch_anchor):
    cycles = {'J1': ['r', 'a', 'x'], 'J2': ['r', 'u', 'w'], 'J3': ['v', 'z', 't']}
    blocks = {k: sorted(e(c[i], c[(i + 1) % 3]) for i in range(3)) for k, c in cycles.items()}
    blocks['uv'] = [e('u', 'v')]
    blocks['tq'] = [e('t', 'q')]
    blocks['branch'] = [e(branch_anchor, 'y')]
    edges = sorted({item for block in blocks.values() for item in block})
    vertices = sorted({v for edge in edges for v in edge})
    adj = neighbors(vertices, edges)
    assert len(components(vertices, edges)) == 1
    reconstructed = edge_blocks(vertices, edges)
    assert reconstructed == sorted(blocks.values())
    deleted = {v: components([w for w in vertices if w != v], [item for item in edges if v not in item]) for v in vertices}
    cutpoints = [v for v in vertices if len(deleted[v]) > 1]
    incident = {v: sorted(k for k, items in blocks.items() if any(v in item for item in items)) for v in vertices}
    private = {k: [v for v in c if v not in cutpoints and v not in ['a', 'q']] for k, c in cycles.items()}
    LS = components([v for v in vertices if v != 'r'], [item for item in edges if 'r' not in item])
    assert len(LS) == 2
    L = next(c for c in LS if 'a' in c)
    S = next(c for c in LS if 'q' in c)
    assert sorted(v for v in adj['r'] if v in L) == ['a', 'x']
    assert sorted(v for v in adj['r'] if v in S) == ['u', 'w']
    return {'vertex_order': vertices, 'all_original_C_edges': edges, 'named_cycles': cycles,
            'original_named_blocks': blocks, 'blocks_reconstructed_from_original_edges': reconstructed,
            'all_original_C_neighbors': {v: sorted(adj[v]) for v in vertices},
            'degree_C': {v: len(adj[v]) for v in vertices}, 'all_vertex_deletion_components': deleted,
            'cut_vertices_reconstructed_from_original_edges': cutpoints,
            'incident_blocks': incident, 'private_noncontact_vertices': private,
            's_contact_order': ['a', 'q'], 'p_arm_path': ['a'], 'q_arm_path': ['t', 'q'],
            'branch_path': [branch_anchor, 'y'], 'r_contact_split': [2, 2], 'L_component': L, 'S_component': S}


def make_fixture(name, branch_anchor, mode):
    graph = make_C(branch_anchor)
    C = graph['vertex_order']
    B = ['B0', 'B1', 'B2', 'B3', 'B4']
    beta = dict(zip(B, [0, 1, 0, 1, 2]))
    frame = [e(B[i], B[(i + 1) % 5]) for i in range(5)]
    contacts = ['a', 'q']
    attachments = {
        'r': [], 'a': ['B4'], 'x': ['B4'], 'u': ['B1'], 'w': ['B0', 'B1'],
        'v': ['B4'], 'z': ['B0', 'B4'], 't': ['B4'], 'q': ['B1', 'B4'],
        'y': ['B0', 'B1', 'B4'],
    }
    if mode != 'negative':
        attachments.update({'v': ['B0'], 'z': ['B0', 'B1'], 't': ['B0'], 'q': ['B0', 'B1']})
    if branch_anchor == 'a':
        attachments['a'] = []
        attachments['x'] = ['B0', 'B1']
    elif branch_anchor == 'w':
        attachments['x'] = ['B0', 'B1']
        attachments['w'] = ['B0']
    sb = ['B0', 'B1', 'B4']
    edges = sorted(set(tuple(item) for item in graph['all_original_C_edges']) | set(frame) |
                   {e(v, b) for v in C for b in attachments[v]} |
                   {e('s', v) for v in contacts} | {e('s', b) for b in sb})
    vertices = sorted(B + C + ['s'])
    madj = neighbors(vertices, edges)
    assert len(madj['s']) == 5
    assert all(len(madj[v]) == 4 for v in C)
    assert set(madj['r']).isdisjoint(B + ['s'])
    assert all(beta[a] != beta[b] for a, b in frame)
    queries = []
    for sc in range(4):
        lists = {}
        for v in C:
            banned = {beta[b] for b in attachments[v]}
            if v in contacts:
                banned.add(sc)
            lists[v] = [c for c in range(4) if c not in banned]
        tuples, nodes = all_colorings(C, graph['all_original_C_edges'], lists)
        for tup in tuples:
            check_tuple(C, graph['all_original_C_edges'], lists, tup)
        fibres = []
        for pair in itertools.product(range(4), repeat=2):
            selected = [tup for tup in tuples if [tup[C.index(v)] for v in contacts] == list(pair)]
            fibres.append({'contact_color_tuple': list(pair), 'complete_C_coloring_fibre': selected})
        relation = [rec['contact_color_tuple'] for rec in fibres if rec['complete_C_coloring_fibre']]
        assert sorted(tup for rec in fibres for tup in rec['complete_C_coloring_fibre']) == tuples
        queries.append({'s_color': sc, 's_B_spokes_imposed': False, 'all_original_derived_lists': lists,
                        'complete_C_coloring_fibre': tuples, 'complete_contact_relation': relation,
                        'all_contact_fibres_including_empties': fibres, 'backtracking_nodes': nodes})
    dquery = queries[D]
    lists = dquery['all_original_derived_lists']
    assert all(len(lists[v]) >= graph['degree_C'][v] for v in C)
    assert all((D not in lists[v]) if v in contacts else (D in lists[v]) for v in C)
    full_M = []
    for query in queries:
        sc = query['s_color']
        if any(sc == beta[b] for b in sb):
            continue
        for tup in query['complete_C_coloring_fibre']:
            asg = dict(zip(C, tup)) | beta | {'s': sc}
            full = [asg[v] for v in vertices]
            singleton_lists = {v: [asg[v]] for v in vertices}
            check_tuple(vertices, edges, singleton_lists, full)
            full_M.append(full)
    full_M.sort()
    G_edges = sorted(edges + [e('r', 'B2')])
    full_G = [tup for tup in full_M if tup[vertices.index('r')] != beta['B2']]
    source_supports = {k: sorted({b for v in graph[k + '_component'] for b in attachments[v]}) for k in ['L', 'S']}
    true_edge_pair = len(source_supports['S']) == 2 and e(*source_supports['S']) in frame
    point_data = {v: {'all_original_M_neighbors': sorted(madj[v]), 'degree_M': len(madj[v]),
        'degree_C': graph['degree_C'][v], 'boundary_attachments': attachments[v],
        'boundary_attachment_beta_colors': [beta[b] for b in attachments[v]],
        'original_s_edge_present': v in contacts, 'L_D': lists[v], 'L_D_size': len(lists[v]),
        'D_present': D in lists[v]} for v in C}
    datum = {'name': name, 'finite_control_status': 'triggered and holds', 'actual_target_source_status': 'not triggered',
      'scope': 'synthetic named original-edge degree/list calibration; no disk or Sigma/source certification',
      'original_C': graph, 'ordered_frame': B, 'proper_literal_beta': beta, 'D': D,
      'M_vertex_order': vertices, 'all_original_M_edges': edges, 'all_original_G_edges': G_edges,
      'removed_original_r_spoke': e('r', 'B2'), 's_boundary_spokes': sb, 's_ordered_contacts': contacts,
      'all_original_M_degrees': {v: len(madj[v]) for v in vertices},
      'all_original_G_degrees': {v: len(neighbors(vertices, G_edges)[v]) for v in vertices},
      'all_original_attachments': attachments, 'all_C_point_list_derivations': point_data,
      'actual_component_boundary_supports': source_supports, 'S_true_original_edge_pair_support': true_edge_pair,
      'complete_four_s_queries': queries, 'full_M_beta_lift_fibre': full_M, 'full_G_beta_lift_fibre': full_G,
      'beta_refusal_on_M': not bool(full_M), 'M_beta_minimality': 'not supplied or asserted',
      'disk_embedding': 'not supplied or asserted', 'rotation_ownership_complete_Sigma': 'not supplied or asserted'}
    if mode == 'negative':
        assert branch_anchor == 'x' and not true_edge_pair and not full_M
        palettes = {'J1': [0, 1], 'J2': [2, 3], 'J3': [1, 3], 'uv': [0], 'tq': [0], 'branch': [3]}
        for v in C:
            incident = graph['incident_blocks'][v]
            assert all(set(palettes[a]).isdisjoint(palettes[b]) for a, b in itertools.combinations(incident, 2))
            union = sorted({color for block in incident for color in palettes[block]})
            assert union == lists[v] and len(union) == graph['degree_C'][v]
        assert D in lists['x'] and D not in palettes['J1'] and D in palettes['branch']
        datum['unsupported_D_propagation_counterexample'] = {
            'status': 'counterexample',
            'claim_refuted': 'D in a cut-vertex list forces D in every incident block palette',
            'block_palettes_in_one_literal_frame': palettes,
            'named_cut_vertex': 'x', 'L_D_x': lists['x'],
            'D_routed_to': 'branch', 'D_absent_from': 'J1',
            'failed_actual_source_premise': 'S boundary support is B0/B1/B4, not one true original frame edge pair',
            'actual_disk_source_status': 'not triggered', 'complete_D_coloring_fibre': []}
    else:
        assert full_M
        if branch_anchor in ['a', 'x']:
            assert true_edge_pair
        if branch_anchor == 'a':
            assert graph['private_noncontact_vertices']['J1'] == ['x']
            assert graph['private_noncontact_vertices']['J2'] == ['w']
        if branch_anchor == 'w':
            assert graph['private_noncontact_vertices']['J2'] == []
            datum['routing_obstruction_under_hypothetical_bad_palettes'] = {
              'status': 'triggered and holds',
              'named_chain': ['J1', 'r', 'J2', 'u', 'uv', 'v', 'J3'],
              'premise': 'Assume this C has an uncolorable degree-list assignment with D at all noncontacts',
              'forced_D_blocks': ['J1', 'uv', 'J3'], 'forced_no_D_blocks': ['J2'],
              'contradiction': 'uv and J3 share v but both would contain D',
              'proof_scope': 'necessary palette route verified from the named incidence data; not an enumeration theorem'}
    datum['summary'] = {'C_vertex_count': len(C), 'C_edge_count': len(graph['all_original_C_edges']),
         'four_C_fibre_counts': [len(q['complete_C_coloring_fibre']) for q in queries],
         'full_M_beta_lift_count': len(full_M), 'full_G_beta_lift_count': len(full_G),
         'S_true_edge_pair_support': true_edge_pair,
         'private_witness_counts_J1_J2': [len(graph['private_noncontact_vertices'][k]) for k in ['J1', 'J2']]}
    return datum


def certificate():
    fixtures = [make_fixture('two-private-witnesses-J1-branch-at-a', 'a', 'normal'),
                make_fixture('support-preserved-J1-triangle-branch-at-x', 'x', 'normal'),
                make_fixture('J2-triangle-private-witness-consumed', 'w', 'normal'),
                make_fixture('negative-J1-D-routed-into-pendant-bridge', 'x', 'negative')]
    paths = ['audits/2026-10-11-br-sd-1a-0f181045/agents/controls/checker.py',
             'audits/2026-10-11-br-sd-1a-0f181045/PROOF.md',
             'audits/2026-10-11-br-sd-1a-0f181045/agents/mapping/MAPPING.md',
             'docs/history/2026-10-11-br-sd-1b-adoption.md',
             'docs/c5_degree5_interfaces.md']
    inputs = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths}
    return {'schema': 'BR-SD-1c-tiny-controls-v1', 'BASE': BASE, 'colors_in_literal_order': COLORS,
            'independence': 'Python stdlib only; original-edge tuple backtracking and Tarjan blocks; no source or solver imports',
            'authority_input_sha256': inputs,
            'claim_boundary': 'Four fixed list/edge fixtures; no list-domain or source enumeration; no actual target disk, minimality, Sigma, ownership or rotation',
            'actual_target_source_status': 'not triggered', 'fixtures': fixtures,
            'summary': {'fixed_fixtures': len(fixtures), 'actual_target_sources': 0,
                        'abstract_propagation_counterexamples': 1,
                        'normal_full_M_beta_lifts': [len(x['full_M_beta_lift_fibre']) for x in fixtures[:-1]]}}


def serialize(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def validate_supplied(data):
    assert data['schema'] == 'BR-SD-1c-tiny-controls-v1'
    assert data['BASE'] == BASE
    for fixture in data['fixtures']:
        graph = fixture['original_C']
        C = graph['vertex_order']
        for query in fixture['complete_four_s_queries']:
            for tup in query['complete_C_coloring_fibre']:
                check_tuple(C, graph['all_original_C_edges'], query['all_original_derived_lists'], tup)
        vertices = fixture['M_vertex_order']
        for tup in fixture['full_M_beta_lift_fibre']:
            check_tuple(vertices, fixture['all_original_M_edges'], {v: list(range(4)) for v in vertices}, tup)
            assert all(tup[vertices.index(v)] == c for v, c in fixture['proper_literal_beta'].items())


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', required=True, type=Path)
    args = parser.parse_args()
    if args.check:
        supplied = args.certificate.read_bytes()
        validate_supplied(json.loads(supplied))
    expected = certificate()
    raw = serialize(expected)
    if args.write:
        with args.certificate.open('xb') as file:
            file.write(raw)
    else:
        assert supplied == raw, 'certificate differs from complete original-edge recomputation'
    print(json.dumps({'mode': 'write' if args.write else 'check', 'certificate': str(args.certificate),
        'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), **expected['summary']}, sort_keys=True))
    for fixture in expected['fixtures']:
        print(json.dumps({'fixture': fixture['name'], **fixture['summary']}, sort_keys=True))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (AssertionError, ValueError, KeyError, TypeError, IndexError) as error:
        print('FAIL: ' + repr(error), file=sys.stderr)
        raise SystemExit(1)
