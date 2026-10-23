#!/usr/bin/env python3
"""Independent r,x,y cap lift enumeration on the same literal D boundary.

Only enumerates the fixed original cap; it does not generate exterior disks.
The two forbidden E words are original source zeros, not discarded cap lifts.
"""
from itertools import product
import json

E = ('a', 'n', 'R', 'L', 'q', 'c', 'x', 'y')
D = ('a', 'n', 'R', 'L', 'q', 'c', 's', 'v', 'w', 't')
PREFIX = dict(zip(D[:6], (0, 1, 0, 2, 3, 0)))
CAP = {tuple(sorted(e)) for e in [
    ('x', 'y'), ('x', 'c'), ('x', 's'), ('x', 'r'),
    ('y', 'a'), ('y', 't'), ('y', 'r'),
    ('r', 's'), ('r', 'v'), ('r', 'w'), ('r', 't')]}
D_EDGES = set(zip(D, D[1:] + D[:1]))
ZERO_WORDS = {(0, 1, 0, 2, 3, 0, 1, 2), (0, 1, 0, 2, 3, 0, 2, 1)}


def main():
    records = []
    raw = {'U': 0, 'V': 0}
    for tail in product(range(4), repeat=4):
        colours = {**PREFIX, **dict(zip(D[6:], tail))}
        if any(colours[a] == colours[b] for a, b in D_EDGES):
            continue
        lifts = []
        for r, x, y in product(range(4), repeat=3):
            c = {**colours, 'r': r, 'x': x, 'y': y}
            if all(c[a] != c[b] for a, b in CAP):
                lifts.append({'rxy': [r, x, y], 'E': [c[k] for k in E],
                              'forbidden_source_zero': tuple(c[k] for k in E) in ZERO_WORDS})
        queries = {'U': [lift for lift in lifts if lift['rxy'][1:] == [1, 3]],
                   'V': [lift for lift in lifts if lift['rxy'][1:] == [3, 1]]}
        if not any(queries.values()):
            continue
        for name in raw:
            raw[name] += len(queries[name])
        records.append({'svwt': list(tail), 'all_cap_lifts': lifts,
                        'U_lifts': [r['rxy'] for r in queries['U']],
                        'V_lifts': [r['rxy'] for r in queries['V']],
                        'whole_D_fibre_forced_empty': any(r['forbidden_source_zero'] for r in lifts)})
    survivors = [r for r in records if not r['whole_D_fibre_forced_empty']]
    expected = {(2, 1, 3, 2), (2, 3, 1, 2), (3, 0, 3, 1),
                (3, 1, 0, 1), (1, 0, 1, 3), (1, 3, 0, 3)}
    if len(records) != 24 or raw != {'U': 14, 'V': 14}:
        raise ValueError('wrong complete related domain')
    if {tuple(r['svwt']) for r in survivors} != expected:
        raise ValueError('wrong full-lift survivor fibres')
    for record in survivors:
        common = bool(record['U_lifts'] and record['V_lifts'])
        if common:
            if record['U_lifts'] != [[0, 1, 3]] or record['V_lifts'] != [[0, 3, 1]]:
                raise ValueError('wrong pointwise common swap')
        else:
            if any(rxy[0] != 2 for rxy in record['U_lifts'] + record['V_lifts']):
                raise ValueError('private residual must force r=2')
    print(json.dumps({'status': 'PASS', 'raw_query_lifts': raw,
                      'related_complete_D_tuples': len(records),
                      'whole_D_fibres_forced_empty': len(records) - len(survivors),
                      'remaining_D_tuples': [r['svwt'] for r in survivors],
                      'records': records, 'source_realized': False}, sort_keys=True))


if __name__ == '__main__':
    main()
