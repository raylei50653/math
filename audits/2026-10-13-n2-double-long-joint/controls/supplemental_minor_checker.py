#!/usr/bin/env python3
"""Four explicit local K5 controls; no source or T1 full-hypothesis claim."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tree(vertices, edges):
    vertices = set(vertices)
    seen = {min(vertices)}
    chosen = []
    while seen != vertices:
        available = [e for e in edges if e[0] in vertices and e[1] in vertices
                     and ((e[0] in seen) != (e[1] in seen))]
        assert available, ('disconnected original bag', vertices, seen)
        e = available[0]
        chosen.append(list(e))
        seen.update(e)
    return chosen


def record(p_owner, z_owner):
    v_owner = 11 - p_owner if p_owner == z_owner else 5
    edges = [(b, (b+1) % 5) for b in range(5)]
    edges += [(7, 8), (8, 9), (9, 7), (9, 10), (7, 0), (8, 0), (9, 1),
              (10, 2), (10, 3), (p_owner, 7), (z_owner, 8), (v_owner, 10),
              (11, 12), (5, 11), (11, 3), (11, 4), (6, 12), (12, 4), (12, 0), (5, 0)]
    edges = sorted({tuple(sorted(e)) for e in edges})
    nbr = {v: {b if a == v else a for a, b in edges if v in (a,b)} for v in range(13)}
    C, Q, roots = [7, 8, 9, 10], [11, 12], [5, 6]
    assert all(len(nbr[v]) == 4 for v in C + Q)
    assert all(any(r in nbr[v] for v in C) for r in roots)
    assert all(any(r in nbr[v] for v in Q) for r in roots)
    assert all(len(nbr[v] & set(roots)) <= 1 for v in C)
    assert [v for v in C if v in nbr[7] and v in nbr[8]] == [9]
    support_c = sorted(set().union(*(nbr[v] & set(range(5)) for v in C)))
    support_q = sorted(set().union(*(nbr[v] & set(range(5)) for v in Q)))
    assert support_c == [0, 1, 2, 3] and support_q == [0, 3, 4]
    bags = [[0], [5, 6, 11, 12], [7], [8], [1, 2, 3, 4, 9, 10]]
    assert len(set().union(*map(set, bags))) == sum(map(len, bags))
    trees = [tree(bag, edges) for bag in bags]
    witnesses = []
    for i, j in itertools.combinations(range(5), 2):
        options = [e for e in edges if (e[0] in bags[i] and e[1] in bags[j])
                   or (e[1] in bags[i] and e[0] in bags[j])]
        assert options, ('missing adjacency', i, j)
        witnesses.append({'bag_pair': [i, j], 'original_edge': list(options[0])})
    W = []
    for root in roots:
        W.append(sorted(set().union(*(nbr[v] & set(range(5)) for v in C if root in nbr[v]))))
    assert set().union(*map(set, W)) == {0, 2, 3}
    return {'name': 'private_leaf_pair_owners_%d_%d' % (p_owner, z_owner),
            'boundary': list(range(5)), 'ordered_roots': roots,
            'C_original_vertices': C, 'Q_original_vertices': Q,
            'C_ordered_contacts': [[v for v in C if root in nbr[v]] for root in roots],
            'Q_ordered_contacts': [[v for v in Q if root in nbr[v]] for root in roots],
            'actual_attachments': {str(v): sorted(nbr[v] & set(range(5))) for v in C + Q},
            'complete_original_degrees': {str(v): len(nbr[v]) for v in range(13)},
            'original_edges': edges, 'original_C_leaf_cycle': [7, 8, 9],
            'adjacent_private_contacts': [7, 8], 'ordered_private_contact_owners': [p_owner, z_owner],
            'vertex10_owner': v_owner, 'h': 0, 'actual_root_spoke': [5, 0],
            'actual_supports': {'C': support_c, 'Q': support_q},
            'W_C_by_ordered_root': W,
            'K5_original_branch_sets': bags, 'K5_original_bag_spanning_trees': trees,
            'all_ten_original_adjacencies': witnesses,
            'K5_minor_status': 'triggered and holds',
            'disk_rotation_status': 'impossible by certified original K5 minor',
            'T1_full_premise_status': 'not triggered',
            'T1_missing_premises': ['contact10 has actual boundary attachments2,3, so W_C is not contained in {h}'],
            'full_target_source_status': 'not triggered',
            'full_target_missing_premises': ['nonplanar', 'root degrees need not be five', 'no original Sigma critical relation certified']}


def generate():
    controls = [record(a,b) for a,b in itertools.product([5,6],repeat=2)]
    assert len(controls) == 4
    return {'scope': 'four fixed original local minor controls only; no source search or full T1 calibration',
            'declared_vertex_order': list(range(13)),
            'four_owner_variants': controls,
            'counts': {'local_minor_controls': 4, 'certified_K5_minors': 4,
                       'original_bag_spanning_trees': 20, 'original_cross_adjacencies': 40,
                       'full_T1_triggers': 0, 'full_target_sources': 0},
            'full_target_source_status': 'not triggered'}


def main():
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    p.add_argument('--artifact', type=Path, default=HERE/'supplemental_minors.json')
    args = p.parse_args()
    result = generate()
    data = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.write:
        with args.artifact.open('xb') as f:
            f.write(data)
    else:
        assert args.artifact.read_bytes() == data, 'artifact mismatch'
    print(json.dumps({'mode':'write' if args.write else 'check','bytes':len(data),'sha256':sha(data),
                      'counts':result['counts']},sort_keys=True))


if __name__=='__main__':
    main()
