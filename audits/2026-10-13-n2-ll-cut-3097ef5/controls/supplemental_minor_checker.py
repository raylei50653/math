#!/usr/bin/env python3
"""Original K3,3 calibration for adjacent private contacts of different owners.

Four globally relabelled controls, no planarity or full-source qualification.
"""
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
    answer = []
    while reached != vertices:
        options = [e for e in edges if set(e) <= vertices
                   and ((e[0] in reached) != (e[1] in reached))]
        require(bool(options), 'disconnected original bag')
        answer.append(options[0])
        reached.update(options[0])
    return answer


def graph():
    edges = [(j, (j + 1) % 5) for j in range(5)]
    edges += [(7, 8), (8, 9), (9, 7), (9, 10), (5, 7), (6, 8), (6, 10),
              (7, 0), (8, 1), (9, 2), (10, 2), (10, 3), (5, 0), (6, 3)]
    q = list(range(11, 16))
    edges += list(zip(q, q[1:])) + list(zip(q, [5, 5, 5, 6, 6]))
    for v, attachments in zip(q, [[3, 4], [4], [4], [0], [4, 0]]):
        edges += [(v, h) for h in attachments]
    return sorted([min(a, b), max(a, b)] for a, b in edges)


def verify_local_premises(record):
    edges = record['original_edges']
    nbr = {v: {b if v == a else a for a, b in edges if v in (a, b)} for v in range(16)}
    b = set(record['ordered_boundary'])
    r, s = record['ordered_roots']
    c, q = set(record['C']), set(record['Q'])
    p, z, a = record['leaf_triangle_order']
    require(len(nbr[r]) == len(nbr[s]) == 5, 'wrong original root degree')
    require(all(len(nbr[v]) == 4 for v in c | q), 'wrong ordinary degree')
    require(s not in nbr[r], 'roots adjacent')
    require(nbr[p] & c == {z, a} and nbr[z] & c == {p, a}, 'contacts not private leaf-cycle vertices')
    require(z in nbr[p] and a in nbr[p] and a in nbr[z], 'missing leaf triangle edge')
    require(nbr[a] & (c - {p, z, a}), 'triangle not attached as leaf block')
    require(nbr[p] & {r, s} == {r} and nbr[z] & {r, s} == {s}, 'wrong private owners')
    require(len(nbr[p] & b) == len(nbr[z] & b) == 1, 'private boundary attachment not singleton')
    require(len(nbr[s] & c) >= 2, 'missing remaining original s contact')
    require(len(set().union(*(nbr[v] & b for v in c))) >= 3, 'C not long')
    require(len(set().union(*(nbr[v] & b for v in q))) >= 3, 'Q not long')
    require(all(nbr[root] & c and nbr[root] & q for root in [r, s]), 'pieces not original mixed')
    require(not any(v in c and w in q or v in q and w in c for v, w in edges), 'cross-piece edge')
    tree(c, edges)
    tree(q, edges)
    tree(c - {p, z}, edges)
    tree({r, s} | c | q, edges)
    require(set().union(*(nbr[v] & b for v in {r, s} | c | q)) == b, 'not full B-touch')
    for v in {r, s} | c | q:
        tree(({r, s} | c | q) - {v}, edges)
    return nbr


def verify_minor(record):
    edges = record['original_edges']
    bags = record['original_K33_bags']
    r, s = record['ordered_roots']
    p, z, _ = record['leaf_triangle_order']
    expected = [[p], [s], record['ordered_boundary'], sorted([r] + record['Q']),
                [z], sorted(set(record['C']) - {p, z})]
    require(bags == expected, 'wrong named original minor bags')
    flat = [v for bag in bags for v in bag]
    require(len(flat) == len(set(flat)) and set(flat) <= set(range(16)), 'overlapping or foreign bag vertex')
    trees = record['original_bag_spanning_trees']
    require(len(trees) == 6, 'missing bag spanning tree')
    for bag, spanning in zip(bags, trees):
        require(all(e in edges and set(e) <= set(bag) for e in spanning), 'non-original bag tree edge')
        tree(bag, spanning)
    crossing = record['all_nine_original_cross_edges']
    require([e['bag_pair'] for e in crossing] == [[i, j] for i in range(3) for j in range(3, 6)],
            'missing required K3,3 cross adjacency')
    for item in crossing:
        i, j = item['bag_pair']
        a, b = item['original_edge']
        require([a, b] in edges, 'missing original minor cross edge')
        require((a in bags[i] and b in bags[j]) or (b in bags[i] and a in bags[j]), 'wrong cross edge endpoints')


def rejection(name, expected, call):
    try:
        call()
    except ValueError as error:
        require(str(error) == expected, str(error))
        return {'name': name, 'status': 'rejected', 'reason': str(error)}
    raise ValueError('negative mutation passed')


def make_record(exchange_roots, exchange_contacts):
    image = {v: v for v in range(16)}
    if exchange_roots:
        image[5], image[6] = 6, 5
    if exchange_contacts:
        image[7], image[8] = 8, 7
    edges = sorted([min(image[a], image[b]), max(image[a], image[b])] for a, b in graph())
    r, s, p, z, a = [image[v] for v in [5, 6, 7, 8, 9]]
    c, q, b = list(range(7, 11)), list(range(11, 16)), list(range(5))
    bags = [[p], [s], b, sorted([r] + q), [z], sorted(set(c) - {p, z})]
    crossing = []
    for i in range(3):
        for j in range(3, 6):
            edge = next(e for e in edges if (e[0] in bags[i] and e[1] in bags[j])
                        or (e[1] in bags[i] and e[0] in bags[j]))
            if i == 2 and j == 3:
                edge = [3, 11]  # Actual Q attachment; do not use an incidental spoke.
            crossing.append({'bag_pair': [i, j], 'original_edge': edge})
    record = {'name': 'different_owner_leaf_pair_roots%d_contacts%d' % (exchange_roots, exchange_contacts),
              'whole_graph_vertex_image': {str(v): image[v] for v in range(16)},
              'ordered_boundary': b, 'ordered_roots': [r, s], 'C': c, 'Q': q,
              'original_edges': edges, 'leaf_triangle_order': [p, z, a],
              'original_K33_bags': bags, 'original_bag_spanning_trees': [tree(bag, edges) for bag in bags],
              'all_nine_original_cross_edges': crossing}
    nbr = verify_local_premises(record)
    verify_minor(record)
    record.update({'complete_original_degrees': {str(v): len(nbr[v]) for v in range(16)},
                   'actual_attachments': {str(v): sorted(nbr[v] & set(b)) for v in c + q},
                   'actual_C_contacts_by_root': [sorted(nbr[root] & set(c)) for root in [r, s]],
                   'actual_Q_contacts_by_root': [sorted(nbr[root] & set(q)) for root in [r, s]],
                   'actual_supports': [sorted(set().union(*(nbr[v] & set(b) for v in part))) for part in [c, q]],
                   'H_biconnected': True, 'local_lemma_status': 'triggered and holds',
                   'full_target_source_status': 'not triggered',
                   'full_target_missing_hypotheses': ['nonplanar by original K3,3', 'full Sigma933/941 and criticality not certified']})
    omitted = copy.deepcopy(record)
    omitted['all_nine_original_cross_edges'].pop()
    record['missing_cross_adjacency_control'] = rejection('omitted adjacency', 'missing required K3,3 cross adjacency',
                                                         lambda: verify_minor(omitted))
    deleted = copy.deepcopy(record)
    # s to the C-remainder is one actual original cross edge, independently necessary.
    deleted_edge = next(item['original_edge'] for item in crossing if item['bag_pair'] == [1, 5])
    deleted['original_edges'].remove(deleted_edge)
    record['deleted_original_edge_control'] = dict(rejection('deleted original cross edge', 'missing original minor cross edge',
                                                             lambda: verify_minor(deleted)), deleted_original_edge=deleted_edge)
    return record


def generate():
    controls = [make_record(a, b) for a, b in itertools.product([False, True], repeat=2)]
    return {'base': '3097ef5be241b7777451a5ef8a663f3987d6b866',
            'scope': 'new local original K3,3 lemma calibration; no complete-source claim',
            'four_whole_graph_exchange_variants': controls,
            'counts': {'local_lemma_triggers': 4, 'original_K33_minors': 4, 'original_bag_trees': 24,
                       'original_cross_adjacencies': 36, 'negative_controls_rejected': 8, 'qualified_full_target_sources': 0},
            'full_target_source_status': 'not triggered'}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE / 'supplemental_minors.json')
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
