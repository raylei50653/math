#!/usr/bin/env python3
"""Finite checks for the paper count-cone reduction; not a topology proof."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_adjacent_singleton_counts import CHORDS, FOUR, THREE, LABELED, chord_totals
from c5_kempe_screen import REPS, normalize

ROOT = Path(__file__).resolve().parents[1]
COUNTS = ROOT / 'artifacts/c5_cells/adjacent_singleton_counts.json'
OUT = ROOT / 'artifacts/c5_cells/count_cone_bridge.json'


def edge_word(b):
    return tuple(b[i] ^ b[(i + 1) % 5] for i in range(5))


def fill_polygon(boundary):
    """Clip a properly colored ear, or cone an alternating residual polygon."""
    colors = list(boundary)
    polygon = list(range(len(colors)))
    triangles = []
    while len(polygon) > 3:
        ear = next((i for i in range(len(polygon))
                    if colors[polygon[i - 1]] != colors[polygon[(i + 1) % len(polygon)]]), None)
        if ear is None:
            assert len({colors[v] for v in polygon}) == 2
            hub = len(colors)
            colors.append(next(c for c in range(4) if c not in {colors[v] for v in polygon}))
            triangles.extend((polygon[i], polygon[(i + 1) % len(polygon)], hub)
                             for i in range(len(polygon)))
            return colors, triangles
        triangles.append((polygon[ear - 1], polygon[ear], polygon[(ear + 1) % len(polygon)]))
        del polygon[ear]
    triangles.append(tuple(polygon))
    return colors, triangles


def check_fill(boundary, colors, triangles):
    n = len(boundary)
    assert colors[:n] == list(boundary)
    assert len(colors) <= n + 1
    directed = Counter((t[i], t[(i + 1) % 3]) for t in triangles for i in range(3))
    edges = {tuple(sorted(e)) for e in directed}
    boundary_edges = {tuple(sorted((i, (i + 1) % n))) for i in range(n)}
    assert all(len(set(t)) == 3 and len({colors[v] for v in t}) == 3 for t in triangles)
    for i in range(n):
        assert directed[i, (i + 1) % n] == 1
        assert directed[(i + 1) % n, i] == 0
    for u, v in edges - boundary_edges:
        assert directed[u, v] == directed[v, u] == 1
    assert len(colors) - len(edges) + len(triangles) == 1


def report():
    fibers = Counter(edge_word(b) for b in LABELED)
    parity_words = {w for w in product((1, 2, 3), repeat=5)
                    if all(w.count(c) % 2 == 1 for c in (1, 2, 3))}
    assert set(fibers) == parity_words and set(fibers.values()) == {4}
    mapping = []
    for kind, base in [('a', (1, 1, 2, 3, 1)), ('b', (1, 2, 1, 1, 3))]:
        for rotation in range(5):
            w = tuple(base[(j - rotation) % 5] for j in range(5))
            b = [0]
            for c in w[:-1]:
                b.append(b[-1] ^ c)
            assert b[-1] ^ w[-1] == 0
            rep = normalize(b)
            assert max(rep) == (2 if kind == 'a' else 3)
            mapping.append(dict(kind=kind, rotation=rotation, edge_word=w, pattern=rep))
    assert {tuple(row['pattern']) for row in mapping} == set(REPS)

    independent = []
    for mask in range(32):
        p = {i for i in range(5) if mask >> i & 1}
        if any(i in p and (i + 1) % 5 in p for i in range(5)):
            continue
        containing = [e for e in CHORDS if p <= set(e)]
        assert containing
        independent.append(dict(support=sorted(p), containing_chords=containing))
    # Check the linear formula symbolically, one basis coordinate at a time:
    # coordinates are (m,y_0,...,y_4), not a bounded sample of count vectors.
    for coordinate in range(6):
        m = int(coordinate == 0)
        y = [int(coordinate == i + 1) for i in range(5)]
        x = {e: m + sum(y[i] for i in range(5) if i not in e) for e in CHORDS}
        assert 3 * sum(y) - sum(x.values()) == -5 * m
        for row in independent:
            if all(y[i] == 0 for i in range(5) if i not in row['support']):
                assert all(x[e] == m for e in row['containing_chords'])

    old = json.loads(COUNTS.read_text())
    witnesses = []
    for row in old['catalogue_witnesses']:
        c = row['counts']
        ys = sum(c[i] for i in THREE.values())
        xs = sum(c[i] for i in FOUR.values())
        m = chord_totals(c)[0] - ys
        assert 3 * ys - xs == -5 * m
        witnesses.append(dict(mask=row['mask'], m=m, conjectured_slack=3 * ys - xs))
    abstract = []
    for row in old['abstract_countermodels']:
        c = row['counts']
        slack = 3 * sum(c[i] for i in THREE.values()) - sum(c[i] for i in FOUR.values())
        assert slack == -5
        abstract.append(dict(mask=row['mask'], conjectured_slack=slack))

    polygons = []
    for n in range(3, 10):
        words = {normalize(w) for w in product(range(4), repeat=n)
                 if all(w[i] != w[(i + 1) % n] for i in range(n))}
        hubs = 0
        for w in sorted(words):
            c, t = fill_polygon(w)
            check_fill(w, c, t)
            hubs += len(c) - n
        polygons.append(dict(length=n, color_orbits=len(words), fills_using_hub=hubs))
    c, t = fill_polygon((0, 1, 0, 1))
    try:
        check_fill((0, 1, 0, 1), c, t[:-1])
    except AssertionError:
        pass
    else:
        raise AssertionError('missing-triangle negative control was accepted')
    return dict(
        trust='External finite checks. General completion and disk/dual bridges are paper proofs; Conjecture 9 is NOT assumed true by this checker.',
        source='https://arxiv.org/pdf/1907.04066v2',
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                for p in (Path(__file__), COUNTS, ROOT / 'scripts/c5_adjacent_singleton_counts.py',
                          ROOT / 'scripts/c5_kempe_screen.py')},
        boundary_assignments=len(LABELED), edge_words=len(fibers), fibers_per_edge_word=4,
        literature_mapping=mapping, independent_supports=independent,
        algebra_basis_coordinates=6, catalogue_count_checks=witnesses,
        abstract_violations=abstract, polygon_fills=polygons,
        missing_triangle_rejected=True,
        near_triangulation_size_formula='dual_vertices = 2 * interior_vertices + 4',
        cited_corollary_20_limit='dual_vertices < 30; hence interior_vertices <= 12')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(report(), indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'count-cone bridge artifact differs'
        print('count-cone bridge: exact replay OK')
    else:
        OUT.write_text(data)
        print(OUT.relative_to(ROOT))
