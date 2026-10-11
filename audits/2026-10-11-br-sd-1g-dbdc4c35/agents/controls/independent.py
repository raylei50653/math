#!/usr/bin/env python3
"""Independent domain-propagation replay of submitted complete finite lifts."""
import argparse
import itertools
import json
import sys


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for e in edges:
        assert len(e) == 2 and e[0] != e[1]
        a, b = e
        assert a in adj and b in adj and b not in adj[a], 'invalid or duplicate edge'
        adj[a].add(b)
        adj[b].add(a)
    return adj


def enumerate_lifts(vertices, edges, input_lists):
    adj = adjacency(vertices, edges)
    answer = []
    def visit(current, domains):
        if len(current) == len(vertices):
            answer.append([current[v] for v in vertices])
            return
        v = next(v for v in vertices if v not in current)
        for color in sorted(domains[v]):
            if any(current.get(w) == color for w in adj[v]):
                continue
            reduced = {w: set(domains[w]) for w in vertices}
            legal = True
            for w in adj[v]:
                if w not in current:
                    reduced[w].discard(color)
                    if not reduced[w]:
                        legal = False
                        break
            if legal:
                visit(current | {v: color}, reduced)
    visit({}, {v: set(input_lists[v]) for v in vertices})
    return sorted(answer)


def check_graph_beta(vertices, edges, beta):
    adj = adjacency(vertices, edges)
    lists = {v: [beta[v]] if v in beta else [c for c in range(4)] for v in vertices}
    for v in vertices:
        if v not in beta:
            forbidden = {beta[w] for w in adj[v] if w in beta}
            lists[v] = [c for c in lists[v] if c not in forbidden]
    return enumerate_lifts(vertices, edges, lists)


def check(data):
    assert data['base'] == 'dbdc4c35f785519c8e3cb0260807f0d2feb82469'
    assert data['actual_target_source_count'] == 0 and data['actual_target_source_status'] == 'not triggered'
    counts = []
    for f in data['source_like_fixtures']:
        C = f['C']['vertex_order']
        edges = f['C']['all_edges']
        adj = adjacency(C, edges)
        assert {v: len(adj[v]) for v in C} == f['C']['degree']
        contacts = f['ordered_s_contacts']
        attachments = f['all_boundary_attachments']
        beta = f['literal_beta']
        lists = {}
        for v in C:
            assert len(adj[v]) + len(attachments[v]) + int(v in contacts) == 4, 'complete degree fails'
            excluded = {beta[b] for b in attachments[v]} | ({3} if v in contacts else set())
            lists[v] = [c for c in range(4) if c not in excluded]
        assert lists == f['all_LD_lists']
        expected_C = enumerate_lifts(C, edges, lists)
        assert expected_C == f['complete_C_LD_coloring_tuples'], 'missing or invalid complete C lift'
        vertices = f['M_G_vertex_order']
        expected_M = check_graph_beta(vertices, f['all_M_edges'], beta)
        expected_G = check_graph_beta(vertices, f['all_G_edges'], beta)
        assert expected_M == f['complete_M_beta_lift_tuples'], 'missing or invalid complete M beta lift'
        assert expected_G == f['complete_G_beta_lift_tuples'], 'missing or invalid complete G beta lift'
        assert all(t[vertices.index('s')] == 3 for t in expected_M)
        expected_from_C = sorted([[(beta | {'s': 3} | dict(zip(C, t)))[v] for v in vertices] for t in expected_C])
        assert expected_from_C == expected_M, 'full C/M extension equivalence fails'
        fibres = f['all_16_ordered_pq_fibres_including_empty']
        assert [g['ordered_pq_tuple'] for g in fibres] == [list(p) for p in itertools.product(range(4), repeat=2)]
        for g in fibres:
            pin = g['ordered_pq_tuple']
            assert g['complete_C_tuples'] == [t for t in expected_C if [t[C.index(v)] for v in contacts] == pin]
            assert g['complete_M_tuples'] == [t for t in expected_M if [t[vertices.index(v)] for v in contacts] == pin]
            assert g['complete_G_tuples'] == [t for t in expected_G if [t[vertices.index(v)] for v in contacts] == pin]
        for label in ['L', 'S']:
            actual = sorted({b for v in f['LS_ownership'][label] for b in attachments[v]})
            assert actual == f['actual_synthetic_supports'][label]
        assert f['actual_synthetic_supports']['S'] == ['B0', 'B1']
        for w in ['W1', 'W2']:
            off = set(f[w]['vertices'])
            outside = {v for y in off for v in adj[y] if v not in off}
            assert outside == {f[w]['single_attachment_x']}, 'extra skeleton branch contact'
            assert all(y in f['LS_ownership'][f[w]['ownership']] for y in off)
        assert f['source_contract_status'] == 'not triggered'
        assert f['M_rejects_literal_beta'] is False and f['M_beta_inclusion_minimal'] is False
        counts.append(len(expected_M))
    n = data['negative_controls']
    for key in ['cutpoint_and_W1_D_routing', 'first_branch_D_overstatement']:
        f = n[key]
        vertices = f['C']['vertex_order']
        assert enumerate_lifts(vertices, f['C']['all_edges'], f['all_lists']) == f['complete_C_list_coloring_tuples']
        for v in vertices:
            labels = f['C']['incident_blocks'][v]
            union = sorted({c for label in labels for c in f['all_block_palettes'][label]})
            assert union == f['all_lists'][v]
            assert all(set(f['all_block_palettes'][a]).isdisjoint(f['all_block_palettes'][b])
                       for a, b in itertools.combinations(labels, 2))
    f = n['M_minimality_omission']
    assert check_graph_beta(f['M_vertex_order'], f['all_M_edges'], f['literal_beta']) == f['complete_M_beta_lift_tuples']
    deleted = [e for e in f['all_M_edges'] if e != f['deleted_original_edge']]
    assert check_graph_beta(f['M_vertex_order'], deleted, f['literal_beta']) == f['complete_deleted_edge_beta_lift_tuples'] == []
    f = n['marginal_full_lift_negative']
    assert enumerate_lifts(f['vertex_order'], f['all_edges'], f['all_lists']) == f['complete_coloring_tuples']
    assert f['false_marginally_admitted_tuple'] not in f['complete_coloring_tuples']
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', required=True)
    args = parser.parse_args()
    with open(args.certificate) as source:
        data = json.load(source)
    counts = check(data)
    print(json.dumps({'status': 'triggered and holds', 'complete_M_lift_counts': counts,
                      'actual_target_source_status': 'not triggered'}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ValueError, KeyError, TypeError, IndexError) as error:
        print('FAIL: ' + repr(error), file=sys.stderr)
        raise SystemExit(1)
