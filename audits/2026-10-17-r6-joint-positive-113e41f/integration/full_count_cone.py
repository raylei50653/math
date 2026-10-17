#!/usr/bin/env python3
"""Common exact count cone on the entire original nine-boundary disk.

This is a necessary relaxation, never a graph realization.  A coordinate
keeps the canonical row AND its relative complementary palette pairing;
orbit vectors retain all labelled-member multiplicities.
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'frozen/audits/2026-10-16-r6-319-joint-parity-f1faf74/C/full-source-exploration.json'
PAIRS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
PAIR_KEYS = tuple(frozenset(frozenset(p) for p in pairing) for pairing in PAIRS)
EDGES = tuple((i, (i + 1) % 9) for i in range(9))
PATTERNS = ('ABABC', 'ABACB', 'ABACD', 'ABCAB', 'ABCAC', 'ABCAD', 'ABCBC', 'ABCBD', 'ABCDB', 'ABCDC')


def canon(values):
    mapping = {}
    row = tuple(mapping.setdefault(v, len(mapping)) for v in values)
    return row


def name(row):
    return ''.join('ABCD'[v] for v in row)


def bit(row):
    return 1 << PATTERNS.index(name(canon(row)))


def coordinate(row, pairing):
    mapping = {}
    canonical = tuple(mapping.setdefault(v, len(mapping)) for v in row)
    missing = set(range(4)) - mapping.keys()
    for colour in sorted(missing):
        mapping[colour] = len(mapping)
    key = frozenset(frozenset(mapping[c] for c in palette) for palette in pairing)
    return canonical, PAIR_KEYS.index(key)


@lru_cache(None)
def partitions(vertices):
    if not vertices:
        return ((),)
    result = []
    def extend(labels):
        if len(labels) != len(vertices):
            for label in range(max(labels) + 2):
                extend(labels + (label,))
            return
        by_vertex = dict(zip(vertices, labels))
        if any(by_vertex[a] != by_vertex[b] for a, b in EDGES if a in by_vertex and b in by_vertex):
            return
        result.append(tuple(tuple(v for v in vertices if by_vertex[v] == k) for k in range(max(labels) + 1)))
    extend((0,))
    return tuple(result)


def noncrossing(blocks):
    for first, second in combinations(blocks, 2):
        for a, c in combinations(first, 2):
            if any(a < b < c for b in second) and any(b < a or b > c for b in second):
                return False
    return True


@lru_cache(None)
def orbit_vectors(row, palette_index):
    pairing = PAIRS[palette_index]
    choices = [partitions(tuple(v for v, c in enumerate(row) if c in palette)) for palette in pairing]
    result = set()
    for left, right in product(*choices):
        if not noncrossing(left + right):
            continue
        marked = [(block, pairing[0]) for block in left] + [(block, pairing[1]) for block in right]
        labelled = []
        for flags in product((False, True), repeat=len(marked)):
            image = list(row)
            for flag, (block, palette) in zip(flags, marked):
                if flag:
                    for v in block:
                        image[v] = sum(palette) - image[v]
            labelled.append(tuple(image))
        assert len(set(labelled)) == 2 ** len(marked)
        counts = Counter(coordinate(image, pairing) for image in labelled)
        result.add(tuple(sorted(counts.items())))
    return tuple(sorted(result))


@lru_cache(None)
def projections(row):
    c, s, j, i, w, t, a, p, q = row
    source = 0
    u = 0
    for v in range(4):
        if v in (s, j, i, w):
            continue
        if c == a:
            u |= bit((c, s, v, w, t))
        for r in range(4):
            if r in (s, v, w, t):
                continue
            for x in range(4):
                if x in (c, s, r):
                    continue
                for y in range(4):
                    if y in (x, r, t, a):
                        continue
                    for b in range(4):
                        if b not in (a, c, p, q):
                            source |= bit((x, y, a, b, c))
    caps = (bit((c, s, i, w, t)) if c == a and s != i else 0,
            bit((c, s, j, w, t)) if c == a and j != w else 0)
    return source, u, *caps


def build(source_mask):
    data = json.loads(INPUT.read_text())
    record = next(r for r in data['results'] if r['source_mask'] == source_mask)
    rows = tuple(tuple('ABCD'.index(c) for c in r) for r in record['fixed_rows'])
    rows = tuple(sorted(rows))
    index = {row: i for i, row in enumerate(rows)}
    vectors = set()
    for row in rows:
        for palette in range(3):
            for vector in orbit_vectors(row, palette):
                if all(member in index for (member, _), _ in vector):
                    vectors.add(tuple(sorted((3 * index[member] + pair, count) for (member, pair), count in vector)))
    vectors = tuple(sorted(vectors))
    positivity = []
    for projection, mask in enumerate((source_mask, 319, 1022, 1022)):
        for b in range(10):
            if mask >> b & 1:
                indices = tuple(i for i, row in enumerate(rows) if projections(row)[projection] >> b & 1)
                assert indices
                positivity.append((projection, b, indices))
    for row in rows:
        assert projections(row)[0] & ~source_mask == 0
        assert projections(row)[1] & ~319 == 0
        assert projections(row)[2] & ~1022 == 0
        assert projections(row)[3] & ~1022 == 0
    return rows, vectors, tuple(positivity)


def binding():
    return {p.name: sha256(p.read_bytes()).hexdigest() for p in (Path(__file__), INPUT)}


def verify(cert, model, source_mask):
    rows, vectors, positivity = model
    assert cert['binding'] == binding()
    assert cert['source_mask'] == source_mask
    assert cert['canonical_rows'] == [name(r) for r in rows]
    assert cert['orbit_vectors'] == len(vectors)
    assert cert['source_realizability'] == 'not triggered'
    n = tuple(Fraction(x) for x in cert['common_counts'])
    assert len(n) == len(rows) and all(x >= 0 for x in n)
    reconstructed = [Fraction(0) for _ in range(3 * len(rows))]
    seen = set()
    for index, value in cert['nonzero_cube_weights']:
        assert 0 <= index < len(vectors) and index not in seen
        seen.add(index)
        value = Fraction(value)
        assert value > 0
        for coordinate_index, multiplicity in vectors[index]:
            reconstructed[coordinate_index] += value * multiplicity
    assert all(reconstructed[3 * i + p] == n[i] for i in range(len(rows)) for p in range(3))
    assert cert['positive_projections'] == [[p, b, list(ii)] for p, b, ii in positivity]
    assert all(sum(n[i] for i in ii) >= 1 for _, _, ii in positivity)
    assert cert['total_count'] == str(sum(n))


def solve(model, source_mask):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    rows, vectors, positivity = model
    nsize = len(rows)
    size = nsize + len(vectors)
    ri, ci, vv = [], [], []
    for i in range(nsize):
        for p in range(3):
            ri.append(3 * i + p); ci.append(i); vv.append(-1)
    for j, vector in enumerate(vectors):
        for i, multiplicity in vector:
            ri.append(i); ci.append(nsize + j); vv.append(multiplicity)
    eq = coo_matrix((vv, (ri, ci)), shape=(3 * nsize, size)).tocsr()
    ur, uc = [], []
    for j, (_, _, indices) in enumerate(positivity):
        for i in indices:
            ur.append(j); uc.append(i)
    ub = coo_matrix((-np.ones(len(ur)), (ur, uc)), shape=(len(positivity), size)).tocsr()
    objective = np.zeros(size); objective[:nsize] = 1
    result = linprog(objective, A_eq=eq, b_eq=np.zeros(3 * nsize), A_ub=ub,
                     b_ub=-np.ones(len(positivity)), bounds=(0, None), method='highs')
    if not result.success:
        raise RuntimeError('Numerical solver did not provide feasibility; no exclusion: ' + result.message)
    exact = tuple(Fraction(float(v)).limit_denominator(1000000) for v in result.x)
    cert = {'schema': 'original-nine-boundary-common-count-feasible-v1', 'binding': binding(),
            'source_mask': source_mask, 'canonical_rows': [name(r) for r in rows],
            'orbit_vectors': len(vectors), 'labelled_rows': 24 * nsize,
            'common_counts': [str(v) for v in exact[:nsize]],
            'nonzero_cube_weights': [[i, str(exact[nsize + i])] for i in range(len(vectors)) if exact[nsize + i] > 0],
            'positive_projections': [[p, b, list(ii)] for p, b, ii in positivity],
            'total_count': str(sum(exact[:nsize])), 'source_realizability': 'not triggered',
            'conclusion': 'The full nine-boundary common-count relaxation is exactly feasible; joint positivity remains OPEN.'}
    verify(cert, model, source_mask)
    return cert


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-mask', type=int, choices=(932, 933, 941), required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--solve', action='store_true')
    args = parser.parse_args()
    model = build(args.source_mask)
    if args.solve:
        cert = solve(model, args.source_mask)
        with args.certificate.open('x') as out:
            json.dump(cert, out, indent=2); out.write('\n')
    else:
        cert = json.loads(args.certificate.read_text())
        verify(cert, model, args.source_mask)
    print(json.dumps({'ok': True, 'source_mask': args.source_mask, 'rows': len(model[0]),
                      'orbit_vectors': len(model[1]), 'equations': 3 * len(model[0]),
                      'positive_projections': len(model[2]), 'total_count': cert['total_count'],
                      'positive_counts': sum(Fraction(v) > 0 for v in cert['common_counts'])}))


if __name__ == '__main__':
    main()
