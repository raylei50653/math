#!/usr/bin/env python3
"""Fixed C9 endpoint facts only; not a source-graph search."""
import argparse
import copy
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT = HERE / 'certificate.json'


def build():
    n = 9
    def distance(u, v):
        d = abs(u-v)
        return min(d, n-d)
    edges = [(i, (i+1) % n) for i in range(n)]
    witnesses = []
    for i, j in itertools.combinations(range(n), 2):
        endpoints = sorted(set(edges[i] + edges[j]))
        bad = [(u, v) for u, v in itertools.combinations(endpoints, 2)
               if distance(u, v) in (2, 3)]
        assert bad
        witnesses.append({'edges': [i, j], 'endpoints': endpoints,
                          'forbidden_contact_pair': list(bad[0]),
                          'distance': distance(*bad[0])})
    allowed = []
    for mask in range(1 << n):
        vertices = [i for i in range(n) if mask >> i & 1]
        if all(distance(u, v) in (1, 4)
               for u, v in itertools.combinations(vertices, 2)):
            allowed.append(vertices)
    triples = sorted(sorted([i, (i+1) % n, (i+5) % n]) for i in range(n))
    assert len(witnesses) == 36
    assert max(map(len, allowed)) == 3
    assert sorted(s for s in allowed if len(s) == 3) == triples
    counts = {str(j): sum(len(s) == j for s in allowed) for j in range(4)}
    assert counts == {'0': 1, '1': 9, '2': 18, '3': 9}
    return {'scope': 'fixed C9 contacts after the source apex theorem',
            'cycle_length': n, 'forbidden_distances': [2, 3],
            'edge_pair_witnesses': witnesses, 'allowed_contact_subsets': allowed,
            'allowed_subset_counts': counts, 'maximum_contacts': 3,
            'distinct_edge_third_vertices': 9,
            'conditional_inner_count_bound': 18}


def verify(data):
    assert data == build(), 'fixed C9 geometry certificate mismatch'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    if args.write:
        with CERT.open('x') as stream:
            json.dump(build(), stream, indent=2, sort_keys=True)
            stream.write('\n')
    data = json.loads(CERT.read_text())
    verify(data)
    failures = []
    if args.negative:
        missing = copy.deepcopy(data)
        del missing['edge_pair_witnesses'][0]
        altered = copy.deepcopy(data)
        altered['cycle_length'] = 8
        for name, bad in [('missing_edge_pair_witness', missing),
                          ('wrong_cycle_length', altered)]:
            try:
                verify(bad)
            except AssertionError:
                failures.append(name)
            else:
                raise AssertionError('negative control accepted: ' + name)
        assert len(failures) == 2
    print(json.dumps({'status': 'PASS', 'edge_pairs': 36,
                      'allowed_contact_subsets': 37,
                      'maximum_contacts': 3, 'negative_controls_rejected': failures},
                     sort_keys=True))


if __name__ == '__main__':
    main()
