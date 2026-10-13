#!/usr/bin/env python3
"""Tiny standard-library countercontrols for exact boundary obligations."""
from itertools import product
import argparse
import json
from pathlib import Path


def wheel4_counts():
    rows = [(0,1,0,1), (0,1,0,2), (0,1,2,1), (0,1,2,3)]
    return {''.join(map(str, row)): sum(all(c != x for x in row) for c in range(4)) for row in rows}


def ear_graph(t):
    n = 4*t
    edges = {tuple(sorted((i, (i+1)%n))) for i in range(n)}
    for i in range(t):
        a,b,c,d = range(4*i,4*i+4)
        edges.add((a,d))
        edges.update((v,n+i) for v in (a,b,c,d))
    return n, sorted(edges)


def source_hub_lifts(row, t):
    n, edges = ear_graph(t)
    return [list(hubs) for hubs in product(range(4), repeat=t)
            if all((tuple(row)+hubs)[a] != (tuple(row)+hubs)[b] for a,b in edges)]


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    w4 = wheel4_counts()
    assert w4 == {'0101': 2, '0102': 1, '0121': 1, '0123': 0}
    results = []
    for t in (2,3,4):
        rows = [sum(([(0,2,0,1), (0,1,3,1)][bit] for bit in word), ())
                for word in product((0,1), repeat=t)]
        lifts = [source_hub_lifts(row, t) for row in rows]
        assert all(len(x) == 1 for x in lifts)
        n = 4*t
        allowed_edges = [(a,b) for a in range(n) for b in range(a+1,n)
                         if all(row[a] != row[b] for row in rows)]
        pairs = 0
        bad_rows = []
        for j, row in enumerate(rows):
            for other in rows[j+1:]:
                i = next(i for i in range(t) if row[4*i+1] != other[4*i+1])
                bad = list(row)
                bad[4*i+1], bad[4*i+2] = 2,3
                assert all(bad[a] != bad[b] for a,b in allowed_edges)
                assert not source_hub_lifts(bad,t)
                # Every terminal colour in bad occurs in one of these two rows.
                assert all(x in (row[v],other[v]) for v,x in enumerate(bad))
                pairs += 1
                bad_rows.append(dict(pair=[j, rows.index(other)], row=bad))
        results.append(dict(t=t, boundary_size=4*t, source_internal_vertices=t,
                            accepted_rows=[list(x) for x in rows], full_hub_lifts=lifts,
                            compatible_boundary_edges=allowed_edges,
                            conflicting_pairs=pairs, forbidden_coordinate_hybrids=bad_rows,
                            proved_representative_internal_lower_bound=(t+1)//2))
    result = dict(status='PASS', wheel4_complete_canonical_fibres=w4,
                  ear_wheels=results, universal_claim='Paper argument covers every integer t >= 2; finite controls above are t=2,3,4 only.')
    result_path = Path(__file__).resolve().parent/'scope_controls_result.json'
    if args.write:
        with result_path.open('x') as out:
            out.write(json.dumps(result,indent=2)+'\n')
    else:
        assert json.loads(result_path.read_text()) == json.loads(json.dumps(result))
    print(json.dumps(dict(status='PASS', wheel4=w4, ear_wheel_t=[x['t'] for x in results],
                          pair_checks=sum(x['conflicting_pairs'] for x in results))))


if __name__ == '__main__':
    main()
