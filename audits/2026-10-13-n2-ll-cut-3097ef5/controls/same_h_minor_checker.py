#!/usr/bin/env python3
"""K5-H controls with no root-boundary spoke, for all four owners."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tree(vertices, edges):
    vertices = set(vertices)
    reached = {min(vertices)}
    result = []
    while reached != vertices:
        options = [edge for edge in edges if set(edge) <= vertices
                   and ((edge[0] in reached) != (edge[1] in reached))]
        require(bool(options), 'disconnected original bag')
        result.append(options[0])
        reached.update(options[0])
    return result


def validate(record):
    edges = record['original_edges']
    nbr = {v: {b if v == a else a for a, b in edges if v in (a, b)} for v in range(13)}
    p, z, a, v = 7, 8, 9, 10
    b, c, q, roots = set(range(5)), {7, 8, 9, 10}, {11, 12}, {5, 6}
    require(all(len(nbr[w]) == 4 for w in c | q), 'wrong complete ordinary degree')
    require(all(not (nbr[root] & b) for root in roots), 'root-boundary spoke must be absent')
    require(nbr[p] & b == nbr[z] & b == {0}, 'wrong common actual attachment')
    require(nbr[p] & c == {z, a} and nbr[z] & c == {p, a}, 'not private adjacent leaf-cycle contacts')
    require(nbr[a] & c == {p, z, v}, 'wrong leaf triangle attachment')
    require(len(nbr[p] & roots) == len(nbr[z] & roots) == 1, 'not nonshared contacts')
    require(all(nbr[root] & c and nbr[root] & q for root in roots), 'original pieces not mixed')
    require(len(set().union(*(nbr[w] & b for w in c))) >= 3, 'C not long')
    require(len(set().union(*(nbr[w] & b for w in q))) >= 3, 'Q not long')
    tree(c - {p, z}, edges)
    tree(roots | q, edges)
    require(record['boundary_arcs'] == [[3, 4, 0], [3, 2, 1, 0]], 'wrong literal boundary arcs')
    require(3 in set().union(*(nbr[w] & b for w in q)), 'missing a-Q attachment')
    require(1 in set().union(*(nbr[w] & b for w in c - {p, z})), 'missing b-Crest attachment')
    bags = record['original_K5_bags']
    require(bags == [[7], [8], [0], [3, 4, 5, 6, 11, 12], [1, 2, 9, 10]], 'wrong original bags')
    flat = [w for bag in bags for w in bag]
    require(len(flat) == len(set(flat)) and set(flat) == set(range(13)), 'overlapping or foreign bags')
    require(len(record['original_bag_spanning_trees']) == 5, 'missing original bag spanning tree')
    for bag, spanning in zip(bags, record['original_bag_spanning_trees']):
        require(all(edge in edges and set(edge) <= set(bag) for edge in spanning), 'non-original bag edge')
        tree(bag, spanning)
    crossing = record['all_ten_original_cross_edges']
    require([item['bag_pair'] for item in crossing] == [list(pair) for pair in itertools.combinations(range(5), 2)],
            'missing K5 cross adjacency')
    for item in crossing:
        i, j = item['bag_pair']
        u, w = item['original_edge']
        require([u, w] in edges, 'missing original cross edge')
        require((u in bags[i] and w in bags[j]) or (w in bags[i] and u in bags[j]), 'wrong original cross endpoints')


def record(p_owner, z_owner):
    v_owner = 11 - p_owner if p_owner == z_owner else 5
    edges = [(j, (j + 1) % 5) for j in range(5)]
    edges += [(7, 8), (8, 9), (9, 7), (9, 10), (7, 0), (8, 0), (9, 1), (10, 2), (10, 3),
              (p_owner, 7), (z_owner, 8), (v_owner, 10),
              (11, 12), (5, 11), (6, 12), (11, 3), (11, 4), (12, 4), (12, 0)]
    edges = sorted([min(u, v), max(u, v)] for u, v in edges)
    bags = [[7], [8], [0], [3, 4, 5, 6, 11, 12], [1, 2, 9, 10]]
    crossing = []
    for i, j in itertools.combinations(range(5), 2):
        edge = next(e for e in edges if (e[0] in bags[i] and e[1] in bags[j])
                    or (e[1] in bags[i] and e[0] in bags[j]))
        crossing.append({'bag_pair': [i, j], 'original_edge': edge})
    value = {'name': 'same_h_no_spoke_owners_%d_%d' % (p_owner, z_owner),
             'ordered_boundary': list(range(5)), 'ordered_roots': [5, 6],
             'original_C': [7, 8, 9, 10], 'original_Q': [11, 12],
             'leaf_triangle': [7, 8, 9], 'ordered_private_contact_owners': [p_owner, z_owner],
             'vertex10_owner': v_owner, 'common_original_boundary_neighbor_h': 0,
             'selected_Q_attachment_a': 3, 'selected_Crest_attachment_b': 1,
             'boundary_arcs': [[3, 4, 0], [3, 2, 1, 0]],
             'original_edges': edges, 'original_K5_bags': bags,
             'original_bag_spanning_trees': [tree(bag, edges) for bag in bags],
             'all_ten_original_cross_edges': crossing,
             'root_boundary_spokes': [], 'local_K5_H_status': 'triggered and holds',
             'full_target_source_status': 'not triggered',
             'missing_full_target_hypotheses': ['nonplanar by original K5', 'root degrees are not five',
                                                'complete Sigma933/941 and criticality not certified']}
    validate(value)
    nbr = {v: {b if v == a else a for a, b in edges if v in (a, b)} for v in range(13)}
    value['complete_original_degrees'] = {str(v): len(nbr[v]) for v in range(13)}
    value['actual_attachments'] = {str(v): sorted(nbr[v] & set(range(5))) for v in range(7, 13)}
    value['actual_contacts_by_piece_then_root'] = [[sorted(nbr[root] & set(c)) for root in [5, 6]]
                                                   for c in [range(7, 11), range(11, 13)]]
    bad = copy.deepcopy(value)
    bad['all_ten_original_cross_edges'].pop()
    try:
        validate(bad)
    except ValueError as error:
        require(str(error) == 'missing K5 cross adjacency', str(error))
        value['negative_missing_adjacency'] = {'status': 'rejected', 'reason': str(error)}
    else:
        raise ValueError('missing adjacency accepted')
    return value


def generate():
    return {'base': '3097ef5be241b7777451a5ef8a663f3987d6b866',
            'scope': 'local generalized K5-H; no root-h spoke or full-source claim',
            'four_owner_controls': [record(a, b) for a, b in itertools.product([5, 6], repeat=2)],
            'counts': {'local_K5_H_triggers': 4, 'original_bag_trees': 20, 'original_cross_adjacencies': 40,
                       'negative_controls_rejected': 4, 'qualified_full_target_sources': 0},
            'full_target_source_status': 'not triggered'}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE / 'same_h_minors.json')
    args = parser.parse_args()
    result = generate()
    data = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    if args.write:
        with args.artifact.open('xb') as stream:
            stream.write(data)
    else:
        require(args.artifact.read_bytes() == data, 'artifact mismatch')
    print(json.dumps({'mode': 'write' if args.write else 'check', 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest(), 'counts': result['counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
