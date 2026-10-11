#!/usr/bin/env python3
"""Second complete-fibre check reconstructs C/lists from supplied M edges."""
import argparse
import itertools
import json
import sys


def adj_from_edges(vertices, edges):
    a = {v: [] for v in vertices}
    for v, w in edges:
        assert v != w and v in a and w in a
        a[v].append(w)
        a[w].append(v)
    assert all(len(ws) == len(set(ws)) for ws in a.values())
    return {v: sorted(ws) for v, ws in a.items()}


def connected_parts(vertices, adj):
    pending = set(vertices)
    result = []
    while pending:
        todo = [sorted(pending)[0]]
        pending.remove(todo[0])
        component = []
        while todo:
            v = todo.pop(0)
            component.append(v)
            for w in adj[v]:
                if w in pending:
                    pending.remove(w)
                    todo.append(w)
        result.append(sorted(component))
    return sorted(result)


def original_edge_query(C, M_adj, beta, s_color):
    """Fixed alphabetical order; every check reads original M edges directly."""
    current = dict(beta)
    current['s'] = s_color
    result = []
    def visit(i):
        if i == len(C):
            result.append([current[v] for v in C])
            return
        v = C[i]
        for c in range(4):
            if any(current.get(w, -1) == c for w in M_adj[v]):
                continue
            current[v] = c
            visit(i + 1)
            del current[v]
    visit(0)
    return sorted(result)


def verify(data):
    result = []
    for fixture in data['fixtures']:
        graph = fixture['original_C']
        vertices = fixture['M_vertex_order']
        B = fixture['ordered_frame']
        beta = fixture['proper_literal_beta']
        edges = fixture['all_original_M_edges']
        adj = adj_from_edges(vertices, edges)
        C = sorted(v for v in vertices if v not in B and v != 's')
        C_edges = sorted([e for e in edges if e[0] in C and e[1] in C])
        assert C == graph['vertex_order']
        assert C_edges == graph['all_original_C_edges']
        C_adj = adj_from_edges(C, C_edges)
        assert len(connected_parts(C, C_adj)) == 1
        assert {v:len(ws) for v,ws in C_adj.items()} == graph['degree_C']
        deletion = {v:connected_parts([w for w in C if w != v], C_adj) for v in C}
        assert deletion == graph['all_vertex_deletion_components']
        cuts = [v for v in C if len(deletion[v]) > 1]
        assert cuts == graph['cut_vertices_reconstructed_from_original_edges']
        attachments = {v:sorted(w for w in adj[v] if w in B) for v in C}
        assert attachments == fixture['all_original_attachments']
        contacts = sorted(w for w in adj['s'] if w in C)
        assert contacts == fixture['s_ordered_contacts']
        assert all(len(adj[v]) == 4 for v in C) and len(adj['s']) == 5
        fibres = []
        lists_D = {}
        for sc in range(4):
            tuples = original_edge_query(C, adj, beta, sc)
            query = fixture['complete_four_s_queries'][sc]
            assert query['s_color'] == sc and not query['s_B_spokes_imposed']
            assert tuples == query['complete_C_coloring_fibre']
            lists = {v:[c for c in range(4) if c not in {beta[b] for b in attachments[v]}
                          and not (v in contacts and c == sc)] for v in C}
            assert lists == query['all_original_derived_lists']
            expected_fibres = []
            for pair in itertools.product(range(4), repeat=2):
                selected = [tup for tup in tuples if [tup[C.index(v)] for v in contacts] == list(pair)]
                expected_fibres.append({'contact_color_tuple':list(pair),'complete_C_coloring_fibre':selected})
            assert expected_fibres == query['all_contact_fibres_including_empties']
            assert [rec['contact_color_tuple'] for rec in expected_fibres if rec['complete_C_coloring_fibre']] == query['complete_contact_relation']
            fibres.append(tuples)
            if sc == 3:
                lists_D = lists
                assert all(len(lists[v]) >= len(C_adj[v]) for v in C)
                assert all((3 not in lists[v]) if v in contacts else (3 in lists[v]) for v in C)
        full = []
        for sc, tuples in enumerate(fibres):
            if any(sc == beta[w] for w in adj['s'] if w in B):
                continue
            for tup in tuples:
                colors = dict(zip(C, tup)) | beta | {'s':sc}
                assert all(colors[v] != colors[w] for v, w in edges)
                full.append([colors[v] for v in vertices])
        full.sort()
        assert full == fixture['full_M_beta_lift_fibre']
        G_edges = fixture['all_original_G_edges']
        actual_G = []
        for tup in full:
            colors = dict(zip(vertices, tup))
            if all(colors[v] != colors[w] for v,w in G_edges):
                actual_G.append(tup)
        assert actual_G == fixture['full_G_beta_lift_fibre']
        LS = connected_parts([v for v in C if v != 'r'],C_adj)
        actualL=next(comp for comp in LS if 'a' in comp)
        actualS=next(comp for comp in LS if 'q' in comp)
        supports = {label:sorted({b for v in comp for b in attachments[v]})
                    for label,comp in [('L',actualL),('S',actualS)]}
        assert supports == fixture['actual_component_boundary_supports']
        frame = sorted([e for e in edges if e[0] in B and e[1] in B])
        pair = len(supports['S']) == 2 and supports['S'] in frame
        assert pair == fixture['S_true_original_edge_pair_support']
        if 'unsupported_D_propagation_counterexample' in fixture:
            negative = fixture['unsupported_D_propagation_counterexample']
            palettes = negative['block_palettes_in_one_literal_frame']
            for v in C:
                incident=graph['incident_blocks'][v]
                union=sorted({c for block in incident for c in palettes[block]})
                assert union==lists_D[v]
                assert all(set(palettes[a]).isdisjoint(palettes[b]) for a,b in itertools.combinations(incident,2))
            assert 3 in lists_D['x'] and 3 not in palettes['J1'] and 3 in palettes['branch']
            assert not full and not pair
        result.append({'fixture':fixture['name'],'status':'triggered and holds',
                       'query_fibre_counts':[len(q) for q in fibres], 'full_M_lifts':len(full),
                       'S_actual_support':supports['S'], 'S_true_edge_pair':pair})
    return {'independent_original_M_edge_reconstruction_status':'triggered and holds',
            'actual_target_source_status':'not triggered','fixtures':result}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',required=True)
    args=parser.parse_args()
    with open(args.certificate) as f:data=json.load(f)
    print(json.dumps(verify(data),sort_keys=True))


if __name__=='__main__':
    try:main()
    except (AssertionError,ValueError,KeyError,TypeError,IndexError) as error:
        print('FAIL: '+repr(error),file=sys.stderr)
        raise SystemExit(1)
