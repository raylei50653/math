#!/usr/bin/env python3
"""Independent original-edge check of the triple quotient's local arithmetic.

No source generator or other checker is imported. Facial planarity, the
nonedge ell-r and relative source colourability remain paper obligations.
"""
import itertools
import json

PINS = ('z', 's', 'r', 't', 'q', 'ell', 'm')
EDGES = (('z', 's'), ('s', 'r'), ('r', 't'), ('t', 'z'),
         ('z', 'q'), ('q', 'ell'), ('ell', 'm'), ('m', 'z'))
CAP = (('z', 'x'), ('s', 'x'), ('r', 'x'), ('x', 'y'),
       ('z', 'y'), ('r', 'y'), ('t', 'y'),
       ('p', 'z'), ('p', 'q'), ('p', 'ell'), ('p', 'm'))


def orbit(values):
    names = {}
    return ''.join(names.setdefault(v, chr(65 + len(names))) for v in values)


def run():
    proper = 0
    quotient = []
    survivors = []
    for values in itertools.product(range(4), repeat=7):
        f = dict(zip(PINS, values))
        if any(f[u] == f[v] for u, v in EDGES):
            continue
        proper += 1
        if not f['z'] == f['r'] == f['ell']:
            continue
        lifts = []
        for x, y, p in itertools.product(range(4), repeat=3):
            g = dict(f, x=x, y=y, p=p)
            if all(g[u] != g[v] for u, v in CAP):
                lifts.append((x, y, p))
        bad = [(x, y, p) for x, y, p in lifts
               if {x, y} != {p, f['q']}]
        row = {'pins': values, 'word': orbit(values),
               'all_cap_lifts': lifts, 'target_lifts': bad}
        quotient.append(row)
        if not bad:
            survivors.append(row)
    assert len(survivors) == 24
    assert {row['word'] for row in survivors} == {'ABABCAB'}
    assert all(len(row['all_cap_lifts']) == 2 for row in survivors)
    # A complete-source witness in the quotient must retain each original edge.
    for vertex in ('s', 't'):
        assert not [row for row in survivors
                    if row['pins'][PINS.index(vertex)] != row['pins'][-1]]
    return {'scope': 'Fixed local colour arithmetic only; no source realization',
            'proper_face_assignments': proper,
            'quotient_assignments': len(quotient),
            'surviving_labelled_assignments': len(survivors),
            'surviving_word': 'ABABCAB',
            'm_s_edge_survivors': 0, 'm_t_edge_survivors': 0,
            'all_quotient_rows_including_empty_lifts': quotient}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
