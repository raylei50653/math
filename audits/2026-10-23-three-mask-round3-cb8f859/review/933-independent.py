#!/usr/bin/env python3
"""Independent polygon-diagonal and literal full-fibre reconstruction."""
from itertools import combinations, product
import hashlib
import json

ROWS = ('01012', '01021', '01023', '01201', '01202', '01203', '01212', '01213', '01231', '01232')
E = ('a', 'n', 'R', 'L', 'q', 'c', 'x', 'y')
H = ('a', 'n', 'R', 'L', 'q', 'b')


def canonical(word):
    lookup = {}
    return tuple(lookup.setdefault(c, len(lookup)) for c in word)


def main():
    diagonals = [(i, j) for i, j in combinations(range(6), 2) if j-i not in (1, 5)]
    def cross(p, q):
        a, b = p
        c, d = q
        return len(set(p+q)) == 4 and ((a < c < b) != (a < d < b))
    triangles = sorted({tuple(sorted(tuple(sorted((H[i], H[j]))) for i, j in ds))
                        for ds in combinations(diagonals, 3)
                        if not any(cross(p, q) for p, q in combinations(ds, 2))})
    assert len(triangles) == 14
    tuples = sorted({canonical(t) for t in product(range(4), repeat=8)
                     if all(t[i] != t[(i+1) % 8] for i in range(8))})
    assert len(tuples) == 274
    index = {t: i for i, t in enumerate(tuples)}
    base = list(zip(E, E[1:]+E[:1])) + [('a', 'b'), ('b', 'c'), ('b', 'q')]
    matrices = [[[0]*274 for _ in ROWS] for _ in triangles]
    empty = [0]*14
    for ri, word in enumerate(ROWS):
        x, y, a, b, c = map(int, word)
        for n, R, L, q in product(range(4), repeat=4):
            colors = dict(zip(E, (a, n, R, L, q, c, x, y)), b=b)
            proper_base = all(colors[u] != colors[v] for u, v in base)
            for j, ds in enumerate(triangles):
                if proper_base and all(colors[u] != colors[v] for u, v in ds):
                    matrices[j][ri][index[canonical(tuple(colors[v] for v in E))]] += 1
                else:
                    empty[j] += 1
    records = []
    for j, ds in enumerate(triangles):
        blob = json.dumps(matrices[j], separators=(',', ':')).encode()
        records.append({'id': j, 'diagonals': ds, 'matrix': matrices[j],
                        'matrix_sha256': hashlib.sha256(blob).hexdigest(),
                        'local_empty_fibres': empty[j], 'local_full_lifts': 2560-empty[j]})
    print(json.dumps({'status': 'PASS', 'triangulations': records,
                      'literal_local_fibres': 14*2560,
                      'source_realization_checked': False}, sort_keys=True))


if __name__ == '__main__':
    main()
