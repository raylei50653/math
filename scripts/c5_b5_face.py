#!/usr/bin/env python3
"""Replay Figure 3's twelve B5 rays, support faces and ordered gluing.

The completeness of the ray list is cited Lemma 6, not re-proved here.
All extension counts are independently enumerated on the transcribed 5-poles.
Run without arguments to write the certificate, or with --check to replay it.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from math import gcd
from functools import reduce
from pathlib import Path

from c5_adjacent_singleton_counts import REPS, FOUR, THREE, CHORDS, count_extensions
from c5_kempe_screen import normalize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/b5_face.json'
SOURCE = 'https://arxiv.org/pdf/1907.04066v2'
WORDS = tuple(w for w in product((1, 2, 3), repeat=5)
              if all(w.count(c) % 2 == 1 for c in (1, 2, 3)))


def boundary(w):
    b = [0]
    for c in w[:-1]:
        b.append(b[-1] ^ c)
    assert b[-1] ^ w[-1] == 0
    return normalize(b)


def poles():
    """Figure 3, printed p.7: terminal i is vertex -i-1; others cubic.

    R1..5: tripod plus a terminal-to-terminal edge (a loop at deleted v).
    R6..10: three-vertex tree. R11: pentagon. R12: pentagram.
    Paper drawings run port labels counterclockwise; labels are preserved.
    """
    result = []
    bases = [([(-1, 0), (-2, 0), (-5, 0), (-3, -4)], 1),
             ([(-1, 0), (0, 1), (0, 2), (-2, 1), (-3, 1),
               (-4, 2), (-5, 2)], 3)]
    for edges, n in bases:
        for shift in range(5):
            def turn(v):
                return -(((-v - 1 - shift) % 5) + 1) if v < 0 else v
            result.append(dict(vertices=n, edges=[(turn(u), turn(v)) for u, v in edges]))
    for step in (1, 2):
        result.append(dict(vertices=5, edges=[(-i-1, i) for i in range(5)] +
                           [(i, (i + step) % 5) for i in range(5)]))
    return result


def edge_counts(pole):
    """Enumerate internal edge colors for each fixed labeled parity word."""
    edges = pole['edges']
    degrees = Counter(v for e in edges for v in e)
    assert all(degrees[v] == 3 for v in range(pole['vertices']))
    assert all(degrees[-i-1] == 1 for i in range(5))
    internal = [i for i, e in enumerate(edges) if min(e) >= 0]
    ans = {}
    for w in WORDS:
        fixed = {}
        valid = True
        for i, e in enumerate(edges):
            colors = {w[-v-1] for v in e if v < 0}
            if len(colors) > 1:
                valid = False
            if colors:
                fixed[i] = min(colors)
        ans[w] = 0
        if not valid:
            continue
        for values in product((1, 2, 3), repeat=len(internal)):
            colors = fixed | dict(zip(internal, values))
            if all(len({colors[i] for i, e in enumerate(edges) if v in e}) == 3
                   for v in range(pole['vertices'])):
                ans[w] += 1
    return ans


def compress(counts):
    result = []
    for b in REPS:
        values = {counts[w] for w in WORDS if boundary(w) == b}
        assert len(values) == 1
        result.append(values.pop())
    return result


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def report():
    graphs = poles()
    full = [edge_counts(p) for p in graphs]
    raw = [compress(c) for c in full]
    scales = [reduce(gcd, c) for c in raw]
    rays = [[v // s for v in c] for c, s in zip(raw, scales)]
    assert len({tuple(r) for r in rays}) == 12
    t = [int(max(b) == 3) for b in REPS]
    fans = [count_extensions(0, [e for e in CHORDS if i in e]) for i in range(5)]
    wheel = count_extensions(1, [(i, 5) for i in range(5)])
    assert rays[11] == t and rays[10] == wheel
    for r, e in zip(rays[:5], [(2, 4), (1, 3), (0, 2), (1, 4), (0, 3)]):
        assert r == [int(b[e[0]] == b[e[1]]) for b in REPS]
    fan_ray = [rays.index(f) + 1 for f in fans]
    assert set(fan_ray) == set(range(6, 11))
    labels = {j: f'x_{u}{v}' for (u, v), j in FOUR.items()}
    labels.update({j: f'y_{i}' for i, j in THREE.items()})
    rows = []
    for i, r in enumerate(rays):
        y = [r[THREE[j]] for j in range(5)]
        m = r[FOUR[0, 2]] - sum(y[j] for j in (1, 3, 4))
        assert all(r[k] == m + sum(y[j] for j in range(5) if j not in e)
                   for e, k in FOUR.items())
        rows.append(dict(ray=i+1, pole=graphs[i], raw_counts=raw[i],
                         primitive_counts=r, raw_scale=scales[i], m=m, y=y,
                         support=[labels[j] for j, v in enumerate(r) if v]))
    faces = []
    # All 11 independent supports; S1 and S2 are the requested representatives.
    for mask in range(32):
        p = [i for i in range(5) if mask >> i & 1]
        if any(i in p and (i+1) % 5 in p for i in range(5)):
            continue
        support = {j for j in range(10) if t[j]} | {THREE[i] for i in p}
        retained = [i+1 for i, r in enumerate(rays)
                    if all(not r[j] for j in range(10) if j not in support)]
        assert retained == sorted([12] + [fan_ray[i] for i in p])
        # Unique decomposition: c=x_e=m, a_i=y_i, since P lies in chord e.
        containing = [e for e in CHORDS if set(p) <= set(e)]
        assert containing
        for e in containing:
            assert t[FOUR[e]] == 1 and all(fans[i][FOUR[e]] == 0 for i in p)
        faces.append(dict(P=p, retained_rays=retained, containing_chords=containing))
    # Every S4 boundary orbit has 24 assignments and 6 parity words.
    assert set(Counter(boundary(w) for w in WORDS).values()) == {6}
    pairing = [[6 * dot(a, b) for b in rays] for a in rays]
    assert all(sum(full[i][w]*full[j][w] for w in WORDS) ==
               pairing[i][j]*scales[i]*scales[j]
               for i in range(12) for j in range(12))
    # Audit all cyclic/reversed port alignments explicitly; no independent renaming.
    alignments = []
    for sign in (1, -1):
        for shift in range(5):
            perm = [(sign*i+shift) % 5 for i in range(5)]
            transformed = [compress({w: full[j][tuple(w[k] for k in perm)] // scales[j]
                                    for w in WORDS}) for j in range(12)]
            assert all(r in rays for r in transformed)
            table = [[sum((full[i][w] // scales[i]) *
                          (full[j][tuple(w[k] for k in perm)] // scales[j]) for w in WORDS)
                      for j in range(12)] for i in range(12)]
            assert table == [[6*dot(a, b) for b in transformed] for a in rays]
            alignments.append(dict(port_map=perm, ray_permutation=[rays.index(r)+1 for r in transformed],
                                   pairing=table))
    filters = []
    for p in ([0], [0, 2]):
        fr = [fan_ray[i]-1 for i in p]
        isolators = [j+1 for j in range(11) if pairing[11][j] > 0 and
                     all(pairing[i][j] == 0 for i in fr)]
        zero_closures = [j+1 for j in range(12) if pairing[11][j] == 0 and
                         all(pairing[i][j] == 0 for i in fr)]
        assert isolators and not zero_closures
        filters.append(dict(P=p, planar_ray_fan_annihilators=isolators,
                            zero_pairing_rays=zero_closures,
                            petersen_pairings={str(j): pairing[11][j-1] for j in isolators}))
    # Negative controls: dropping orbit multiplicity or rotating only one port
    # frame changes an actual gluing count, despite color-renaming invariance.
    assert dot(rays[2], rays[11]) == 1 and pairing[2][11] == 6
    assert alignments[1]['pairing'] != pairing
    # The wheel distinguishes pure t from a fan-containing mixture.
    assert pairing[11][10] == 0 and all(pairing[i-1][10] == 6 for i in fan_ray)
    # Lemma 13.2(ii): equality on chord j gives precisely x_j,y_(j+3),y_(j+4).
    case_ii = []
    for j in range(5):
        e = tuple(sorted((j, (j+2) % 5)))
        actual = {k for k, b in enumerate(REPS) if b[e[0]] == b[e[1]]}
        expected = {FOUR[e], THREE[(j+3) % 5], THREE[(j+4) % 5]}
        assert actual == expected
        case_ii.append(dict(chord=e, support=[labels[k] for k in sorted(actual)]))
    return dict(trust='Exact finite enumeration of transcribed Figure 3. Ray completeness is cited Lemma 6; no planar nonrealizability or Kempe confinement proof.',
                source=SOURCE, source_pdf_sha256='d5460af5e98369b0e704ee043ba8daed806944db8dd5854b8b1d990bc104f26e',
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                        for p in (Path(__file__), ROOT/'scripts/c5_adjacent_singleton_counts.py',
                                  ROOT/'scripts/c5_kempe_screen.py')},
                coordinate_order=[labels[j] for j in range(10)],
                pattern_order=REPS, parity_words=len(WORDS), rays=rows,
                fan_ray_by_vertex=fan_ray, independent_faces=faces,
                primitive_gluing_pairing=pairing, dihedral_alignments=alignments,
                negative_controls=dict(omitted_multiplicity_detected=True,
                                       one_sided_port_rotation_detected=True),
                filters=filters, lemma_13_2_case_ii=case_ii)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(report(), indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'B5 face certificate differs'
        print('B5 face: exact replay OK')
    else:
        OUT.write_text(data)
        print(OUT.relative_to(ROOT))
