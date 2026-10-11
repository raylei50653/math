#!/usr/bin/env python3
"""Independent reader: original M edges, fixed alphabetical DFS, deletion cuts.

No imports from the producer. Supplied block edge partition is checked by its
block-vertex incidence tree and each block's direct edge shape.
"""
import argparse
import itertools
import json
import sys


def adjacency(vertices, edges):
    result = {v: [] for v in vertices}
    assert edges == sorted(edges)
    for a, b in edges:
        assert a < b and a in result and b in result
        result[a].append(b)
        result[b].append(a)
    assert all(len(ws) == len(set(ws)) for ws in result.values())
    return {v: sorted(ws) for v, ws in result.items()}


def components(vertices, adj):
    pending = set(vertices)
    parts = []
    while pending:
        start = min(pending)
        pending.remove(start)
        queue, part = [start], []
        while queue:
            v = queue.pop(0)
            part.append(v)
            for w in adj[v]:
                if w in pending:
                    pending.remove(w)
                    queue.append(w)
        parts.append(sorted(part))
    return sorted(parts)


def verify_graph(graph):
    vertices, edges = graph['vertex_order'], graph['all_edges']
    adj = adjacency(vertices, edges)
    assert vertices == sorted(vertices)
    assert len(components(vertices, adj)) == 1
    assert graph['degree'] == {v: len(ws) for v, ws in adj.items()}
    deletion = {v: components([w for w in vertices if w != v], adj) for v in vertices}
    cuts = [v for v in vertices if len(deletion[v]) > 1]
    assert graph['all_vertex_deletion_components'] == deletion
    assert graph['cutpoints'] == cuts
    all_block_edges = []
    incident = {v: [] for v in vertices}
    for label, block in sorted(graph['blocks'].items()):
        bs, es = block['vertices'], block['all_edges']
        assert bs == sorted({v for edge in es for v in edge})
        subadj = adjacency(bs, es)
        assert (len(bs) == 2 and len(es) == 1) or (len(bs) == 3 and all(len(ws) == 2 for ws in subadj.values()))
        all_block_edges.extend(es)
        for v in bs:
            incident[v].append(label)
    assert sorted(all_block_edges) == edges
    assert graph['incident_blocks'] == incident
    assert {v for v in vertices if len(incident[v]) > 1} == set(cuts)
    tree_vertices = ['block:' + b for b in sorted(graph['blocks'])] + ['cut:' + v for v in cuts]
    tree_edges = sorted([sorted(['block:' + b, 'cut:' + v]) for v in cuts for b in incident[v]])
    tree_adj = adjacency(tree_vertices, tree_edges)
    assert len(components(tree_vertices, tree_adj)) == 1
    assert len(tree_edges) == len(tree_vertices) - 1
    return adj


def solve_from_M(C, adj_M, beta):
    """No supplied lists, alphabetical order, all original M incident edges."""
    current = dict(beta)
    current['s'] = 3
    tuples = []
    def visit(i):
        if i == len(C):
            tuples.append([current[v] for v in C])
            return
        v = C[i]
        for color in range(4):
            if any(current.get(w, -1) == color for w in adj_M[v]):
                continue
            current[v] = color
            visit(i + 1)
            del current[v]
    visit(0)
    return sorted(tuples)


def solve_lists(C, edges, lists):
    adj = adjacency(C, edges)
    current, result = {}, []
    def visit(i):
        if i == len(C):
            result.append([current[v] for v in C])
            return
        v = C[i]
        for color in lists[v]:
            if all(current.get(w, -1) != color for w in adj[v]):
                current[v] = color
                visit(i + 1)
                del current[v]
    visit(0)
    return sorted(result)


def verify(data):
    assert data['base'] == '337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f'
    assert data['actual_target_source_count'] == 0
    assert data['actual_target_source_status'] == 'not triggered'
    results = []
    for fixture in data['source_like_fixtures']:
        graph = fixture['C']
        C = graph['vertex_order']
        C_adj = verify_graph(graph)
        M = fixture['M_vertex_order']
        M_edges = fixture['all_M_edges']
        M_adj = adjacency(M, M_edges)
        B, beta = fixture['ordered_frame'], fixture['literal_beta']
        assert B == ['B0', 'B1', 'B2', 'B3', 'B4']
        assert beta == dict(zip(B, [0, 1, 0, 1, 2]))
        assert sorted(v for v in M if v not in B and v != 's') == C
        assert [e for e in M_edges if all(v in C for v in e)] == graph['all_edges']
        frame = sorted([sorted([B[i], B[(i + 1) % 5]]) for i in range(5)])
        assert [e for e in M_edges if all(v in B for v in e)] == frame
        assert all(beta[a] != beta[b] for a, b in frame)
        attachments = {v: sorted(b for b in M_adj[v] if b in B) for v in C}
        contacts = [v for v in M_adj['s'] if v in C]
        assert contacts == fixture['ordered_s_contacts'] == ['a1', 'q']
        assert [b for b in M_adj['s'] if b in B] == fixture['s_boundary_spokes'] == ['B0', 'B1', 'B4']
        assert attachments == fixture['all_boundary_attachments']
        assert fixture['degree_M'] == {v: len(ws) for v, ws in M_adj.items()}
        assert all(len(M_adj[v]) == 4 for v in C) and len(M_adj['s']) == 5
        lists = {v: [c for c in range(4) if c not in {beta[b] for b in attachments[v]}
                     and not (v in contacts and c == 3)] for v in C}
        assert lists == fixture['all_LD_lists']
        assert all(len(lists[v]) >= len(C_adj[v]) for v in C)
        tuples = solve_from_M(C, M_adj, beta)
        assert tuples == fixture['complete_C_LD_coloring_tuples']
        expected_M = []
        for tup in tuples:
            colors = beta | {'s': 3} | dict(zip(C, tup))
            assert all(colors[a] != colors[b] for a, b in M_edges)
            expected_M.append([colors[v] for v in M])
        expected_M.sort()
        assert expected_M == fixture['complete_M_beta_lift_tuples']
        G_edges = fixture['all_G_edges']
        assert G_edges == sorted(M_edges + [['B2', 'r']])
        G_adj = adjacency(M, G_edges)
        assert len(G_adj['r']) == len(G_adj['s']) == 5
        assert all(len(G_adj[v]) == 4 for v in C if v != 'r')
        epsilon_G = sum(len(G_adj[v]) - 4 for v in C + ['s'])
        assert epsilon_G == fixture['epsilon_G'] == 2
        assert fixture['epsilon_G_definition'] == 'sum(degree_G(v)-4 for all internal vertices v)'
        assert 'epsilon=2' not in fixture['missing_source_prerequisites']
        expected_G = [t for t in expected_M if all(dict(zip(M, t))[a] != dict(zip(M, t))[b] for a, b in G_edges)]
        assert expected_G == fixture['complete_G_beta_lift_tuples']
        fibres = []
        for pair in itertools.product(range(4), repeat=2):
            selected = [t for t in tuples if [t[C.index(v)] for v in contacts] == list(pair)]
            fibres.append({'ordered_contact_tuple': list(pair), 'complete_C_coloring_tuples': selected})
        assert fibres == fixture['all_ordered_contact_fibres_including_empty']
        assert [f['ordered_contact_tuple'] for f in fibres if f['complete_C_coloring_tuples']] == fixture['complete_ordered_contact_relation']
        parts = components([v for v in C if v != 'r'], C_adj)
        ownership = {'L': next(p for p in parts if 'a1' in p), 'S': next(p for p in parts if 'q' in p)}
        assert ownership == fixture['LS_ownership']
        supports = {label: sorted({b for v in part for b in attachments[v]}) for label, part in ownership.items()}
        assert supports == fixture['actual_synthetic_supports']
        assert supports['S'] == ['B0', 'B1']
        W = fixture['W']['off_skeleton_vertices']
        assert W == ['y', 'z']
        x = fixture['W']['attachment_x']
        assert sorted({v for w in W for v in C_adj[w] if v not in W}) == [x]
        assert len(components(W, C_adj)) == 1
        checks = {}
        for v, block in [('w1', 'J1'), ('w2', 'J2')]:
            checks[v] = {'noncutpoint': v not in graph['cutpoints'], 'not_s_contact': v not in contacts,
                         'only_block_is_named_cycle': graph['incident_blocks'][v] == [block],
                         'degree_C_two': len(C_adj[v]) == 2, 'D_in_list': 3 in lists[v],
                         'all_boundary_colors_avoid_D': all(beta[b] != 3 for b in attachments[v])}
        assert checks == fixture['private_witness_checks']
        assert bool(expected_M) == fixture['M_accepts_beta']
        results.append({'name': fixture['name'], 'C_LD_tuples': len(tuples), 'M_lifts': len(expected_M),
                        'G_lifts': len(expected_G), 'epsilon_G': epsilon_G, 'status': 'triggered and holds',
                        'private_witness_status': fixture['private_witness_preservation_status']})
    saturated = data['saturated_local_degree_control']
    adj = verify_graph(saturated['C_before_W'])
    assert len(adj['q']) == saturated['d_C_before_W'] == 3
    assert saturated['s_contact_indicator'] == 1 and saturated['boundary_attachment_count_before_W'] == 0
    assert saturated['degree_M_after_nonempty_W_at_least'] == 5 > saturated['required_degree_M'] == 4
    negative = data['unsupported_cutpoint_inference_negative']
    graph = negative['C']
    adj = verify_graph(graph)
    palettes = negative['block_palettes']
    lists = {v: sorted({c for b in graph['incident_blocks'][v] for c in palettes[b]}) for v in graph['vertex_order']}
    assert lists == negative['all_lists']
    assert all(len(lists[v]) == len(adj[v]) for v in graph['vertex_order'])
    assert all(set(palettes[a]).isdisjoint(palettes[b]) for v in graph['vertex_order']
               for a, b in itertools.combinations(graph['incident_blocks'][v], 2))
    assert solve_lists(graph['vertex_order'], graph['all_edges'], lists) == negative['complete_coloring_tuples'] == []
    assert 3 in lists['x'] and 3 not in palettes['triangle'] and 3 in palettes['bridge']
    assert negative['status'] == 'counterexample'
    return {'independent_original_edge_status': 'triggered and holds',
            'actual_target_source_status': 'not triggered', 'fixtures': results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', required=True)
    args = parser.parse_args()
    with open(args.certificate) as source:
        data = json.load(source)
    print(json.dumps(verify(data), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ValueError, KeyError, TypeError, IndexError) as error:
        print('FAIL: ' + repr(error), file=sys.stderr)
        raise SystemExit(1)
