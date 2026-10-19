#!/usr/bin/env python3
"""Independent direct whole-cap backtracking against C's complete products."""
import gzip
import json
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = ('a','n','R','L','q','u','s','v','w','t')
ROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
STARS = {
    'b': ('a','c','p','q'), 'p': ('a','b','q','h','n'),
    'h': ('p','q','L','R','n'), 'c': ('b','q','u','s','x'),
    'x': ('y','c','r','s'), 'y': ('x','a','r','t'),
    'r': ('x','y','t','w','v','s'),
}
OPS = (
    ('q', (('q','s'),('q','x'))), ('q', (('q','x'),('u','x'))),
    ('u', (('b','u'),('u','x'))), ('s', (('b','s'),('b','u'))),
    ('s', (('b','s'),('q','s'))),
)


def canonical(word):
    names = {}
    return ''.join(str(names.setdefault(c, len(names))) for c in word)


def assignments(core, removed, added):
    edges = {tuple(sorted((v,w))) for v, ns in STARS.items() for w in ns
             if v not in removed and w not in removed}
    edges.update(tuple(sorted(e)) for e in added)
    adjacent = {}
    for v,w in edges:
        adjacent.setdefault(v, set()).add(w)
        adjacent.setdefault(w, set()).add(v)
    order = tuple(v for v in ('c','h','p','b','r','x','y') if v not in removed)
    f = dict(core)
    def visit(i):
        if i == len(order):
            yield dict(f)
            return
        v = order[i]
        for colour in range(4):
            if any(f.get(w) == colour for w in adjacent[v]):
                continue
            f[v] = colour
            yield from visit(i+1)
        f.pop(v, None)
    if any(v in f and w in f and f[v] == f[w] for v,w in edges):
        return
    yield from visit(0)


def main():
    cert = json.loads(gzip.decompress((HERE/'C/certificate.json.gz').read_bytes()))
    caps = json.loads(gzip.decompress((HERE/'C/cap-lifts.json.gz').read_bytes()))
    tested = lifts = empty = 0
    for i, (word, cap) in enumerate(zip(cert['core_states'], caps, strict=True)):
        assert tuple(cap['core']) == tuple(word)
        core = dict(zip(PINS, word, strict=True))
        multiplier = factorial(4-len(set(word)))
        for j in range(6):
            removed, added = ((), ()) if j == 0 else (('c',), OPS[j-1][1])
            direct = list(assignments(core, removed, added))
            frame = 'c' if j == 0 else OPS[j-1][0]
            counts = [0]*10
            actual = set()
            for f in direct:
                counts[ROWS.index(canonical(tuple(f[v] for v in ('x','y','a','b',frame))))] += 1
                actual.add(tuple(f[v] for v in ('b','p','h','x','y','r')) + ((f['c'],) if j == 0 else ()))
            expected = set()
            groups = cap['original_by_c'] if j == 0 else [cap['candidates'][j-1]]
            for group in groups:
                for left in group['left']:
                    for right in group['right']:
                        expected.add(tuple(left)+tuple(right)+((group['c'],) if j == 0 else ()))
            assert actual == expected, ('incomplete Cartesian lift', i, j)
            matrix = cert['original_matrix'] if j == 0 else cert['candidate_matrices'][j-1]
            for row, count in enumerate(counts):
                assert count % multiplier == 0
                assert count//multiplier == matrix[row][i], ('literal matrix', i, j, ROWS[row])
            tested += 1
            lifts += len(actual)
            empty += not actual
    print(json.dumps({'pass':True,'independent_method':'direct full original stars backtracking',
                      'core_states':len(caps),'complete_cap_fibres_checked':tested,
                      'full_lifts_checked':lifts,'empty_cap_fibres_checked':empty,
                      'literal_matrix_entries_checked':10*tested,
                      'source_realized':False},sort_keys=True))


if __name__ == '__main__':
    main()
