#!/usr/bin/env python3
"""Independent finite position/chord review; topology remains a paper obligation."""
from itertools import combinations
import json


def alternate(a, b, c, d, n):
    return len({a, b, c, d}) == 4 and (((c-a) % n < (b-a) % n)
                                                     != ((d-a) % n < (b-a) % n))


def main():
    pairs = [tuple(sorted((i, (i+4) % 9))) for i in range(9)]
    crossing, shared = [], []
    for p, q in combinations(pairs, 2):
        if alternate(*p, *q, 9):
            crossing.append([p, q])
        else:
            common = set(p) & set(q)
            assert len(common) == 1
            u = next(iter(common))
            v, w = next(x for x in p if x != u), next(x for x in q if x != u)
            assert (v-w) % 9 in (1, 8)
            shared.append({'pairs': [p, q], 'common': u, 'adjacent_other_ends': [v, w]})
    # Pocket order is (u,x,v,w,y). The C9 has no u-v or u-w edge;
    # a third C9 contact excludes x-w and y-v. Only x-y can remain.
    diagonals = [e for e in combinations(range(5), 2) if (e[1]-e[0]) not in (1, 4)]
    allowed = [(1, 4)]
    triangulations = [ts for ts in combinations(diagonals, 2)
                      if not alternate(*ts[0], *ts[1], 5)]
    assert len(triangulations) == 5
    assert not [ts for ts in triangulations if set(ts) <= set(allowed)]
    print(json.dumps({'status': 'PASS', 'distance_four_pairs': pairs,
                      'crossing_distinct_pairs': len(crossing),
                      'shared_endpoint_distinct_pairs': shared,
                      'pentagon_triangulations': len(triangulations),
                      'empty_pocket_possible_triangulations': 0,
                      'source_realization_checked': False}, sort_keys=True))


if __name__ == '__main__':
    main()
