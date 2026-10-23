#!/usr/bin/env python3
"""Independent whole-colouring check of sector colour symmetrization.

Uses only the sealed third-round oriented control faces, no producer imports.
These are controls, not full original 932 sources.
"""
from collections import Counter
from itertools import permutations, product
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SOURCE = REPO / 'audits/2026-10-23-three-mask-round3-cb8f859/932/certificate.json'


def full_counts(control, beta):
    vertices = control['boundary'] + control['private_vertices']
    adj = {v: set() for v in vertices}
    for face in control['oriented_faces']:
        for a, b in zip(face, face[1:] + face[:1]):
            adj[a].add(b)
            adj[b].add(a)
    assigned = {'c0': 0, 'c4': beta}
    counts = Counter()

    def visit():
        if len(assigned) == len(vertices):
            counts[tuple(assigned[v] for v in control['boundary'])] += 1
            return
        domains = {v: set(range(4)) - {assigned[w] for w in adj[v] if w in assigned}
                   for v in vertices if v not in assigned}
        v = min(domains, key=lambda w: (len(domains[w]), -len(adj[w]), w))
        for colour in sorted(domains[v]):
            assigned[v] = colour
            visit()
            del assigned[v]

    visit()
    return counts


def rows(beta, length):
    result = []
    for interior in product(range(4), repeat=length):
        path = (beta,) + interior + (0,) if length == 4 else (0,) + interior + (beta,)
        if all(a != b for a, b in zip(path, path[1:])):
            result.append(interior)
    return result


def matrix_rank_one(matrix):
    pivot = next(((i, j) for i, row in enumerate(matrix)
                  for j, value in enumerate(row) if value), None)
    if pivot is None:
        return True
    i0, j0 = pivot
    p = matrix[i0][j0]
    return all(matrix[i][j] * p == matrix[i][j0] * matrix[i0][j]
               for i in range(len(matrix)) for j in range(len(matrix[0])))


def inspect(control, beta):
    counts = full_counts(control, beta)
    short, long = rows(beta, 3), rows(beta, 4)
    def value(u, v):
        return counts[(0,) + u + (beta,) + v]
    raw = [[value(u, v) for v in long] for u in short]
    unused = [c for c in range(4) if c not in {0, beta}]
    maps = []
    for image in permutations(unused):
        mapping = dict(zip(unused, image))
        maps.append(tuple(mapping.get(c, c) for c in range(4)))
    averaged = [[sum(value(u, tuple(p[c] for c in v)) for p in maps)
                 for v in long] for u in short]
    if not matrix_rank_one(averaged):
        raise ValueError('symmetrized matrix is not rank one')
    if matrix_rank_one(raw):
        raise ValueError('control no longer detects raw rank-one misuse')
    proper = len(short) * len(long)
    return {'id': control['id'], 'anchors': [0, beta],
            'matrix_dimensions': [len(short), len(long)],
            'proper_original_fibres': proper, 'empty_original_fibres': proper - len(counts),
            'whole_full_lifts': sum(counts.values()), 'symmetry_group_size': len(maps),
            'raw_rank_one': False, 'column_group_sum_rank_one': True,
            'complete_source_status': 'not triggered'}


def main():
    source = json.loads(SOURCE.read_text())
    result = [inspect(control, beta) for control in source['geometric_controls'] for beta in (1, 0)]
    print(json.dumps({'status': 'PASS', 'controls': result, 'source_exclusion': False}, sort_keys=True))


if __name__ == '__main__':
    main()
