#!/usr/bin/env python3
"""Exact C5 circulation, support, and split-wise integer orbit certificates.

Run with --check to replay the saved certificate; without it, write the JSON.
This checks abstract count vectors, not planar disk realizability. No graph
catalogue search, new Lean theorem, or external ray-completeness oracle.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

from c5_adjacent_singleton_counts import (
    FOUR, THREE, LABELED, PAIRS, chord_totals, orbit_options,
)
from c5_b5_face import compress, edge_counts, poles
from c5_kempe_screen import INDEX, REPS, failure, normalize, obligations

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/circulation_audit.json'
X = [FOUR[tuple(sorted((i, (i - 2) % 5)))] for i in range(5)]
Y = [THREE[i] for i in range(5)]
EDGES = [(i, (i + 2) % 5, X[i], f'X{i}') for i in range(5)]
EDGES += [(i, (i - 1) % 5, Y[i], f'Y{i}') for i in range(5)]


def rref(rows):
    """Canonical nonzero row basis over Q; no floating-point arithmetic."""
    a = [list(map(Fraction, row)) for row in rows]
    k = 0
    for j in range(len(a[0])):
        pivot = next((p for p in range(k, len(a)) if a[p][j]), None)
        if pivot is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        divisor = a[k][j]
        a[k] = [v / divisor for v in a[k]]
        for p in range(len(a)):
            if p != k:
                factor = a[p][j]
                a[p] = [x - factor * y for x, y in zip(a[p], a[k])]
        k += 1
    return [row for row in a if any(row)]


def support(counts):
    return sum(1 << j for j, n in enumerate(counts) if n)


def balanced(counts):
    return all(sum(counts[j] for u, _, j, _ in EDGES if u == i) ==
               sum(counts[j] for _, v, j, _ in EDGES if v == i)
               for i in range(5))


def parameter_m(counts):
    totals = chord_totals(counts)
    assert len(set(totals)) == 1
    m = totals[0] - sum(counts[j] for j in Y)
    assert 5 * m == sum(counts[j] for j in X) - 3 * sum(counts[j] for j in Y)
    return m


def simple_cycles():
    lookup = {(u, v): j for u, v, j, _ in EDGES}
    result = []
    for length in range(3, 6):
        for vertices in permutations(range(5), length):
            if vertices[0] != min(vertices):
                continue  # Quotient only by rotation, not direction reversal.
            pairs = list(zip(vertices, vertices[1:] + vertices[:1]))
            if not all(e in lookup for e in pairs):
                continue
            bits = [lookup[e] for e in pairs]
            counts = [int(j in bits) for j in range(10)]
            if length == 3:
                name = f'T{next(i for i, j in enumerate(X) if counts[j])}'
            elif length == 4:
                name = f'F{next(i for i, j in enumerate(Y) if counts[j])}'
            else:
                name = 't' if all(counts[j] for j in X) else 'W'
            assert balanced(counts)
            result.append(dict(name=name, vertices=vertices, bits=bits,
                               counts=counts, mask=support(counts),
                               m=parameter_m(counts)))
    assert len(result) == len({c['mask'] for c in result}) == 12
    # Independently compare with the explicit five rotations of each short cycle.
    expected = {}
    for i in range(5):
        expected[f'T{i}'] = {X[i], Y[(i + 1) % 5], Y[(i + 2) % 5]}
        expected[f'F{i}'] = {Y[i]} | {
            X[j] for j in range(5) if i not in (j, (j - 2) % 5)}
    expected['t'], expected['W'] = set(X), set(Y)
    assert {c['name']: set(c['bits']) for c in result} == expected
    assert Counter((len(c['vertices']), c['m']) for c in result) == {
        (3, -1): 5, (4, 0): 5, (5, 1): 1, (5, -3): 1}
    return sorted(result, key=lambda c: c['name'])


def reachable(mask, start):
    seen = {start}
    todo = [start]
    while todo:
        u = todo.pop()
        for tail, head, bit, _ in EDGES:
            if tail == u and mask >> bit & 1 and head not in seen:
                seen.add(head)
                todo.append(head)
    return seen


def decompose(counts, cycles):
    """Replay integer circulation subtraction and exact reconstruction."""
    remaining = list(counts)
    assert all(n >= 0 for n in remaining) and balanced(remaining)
    terms = []
    while any(remaining):
        cycle = next(c for c in cycles if all(remaining[j] for j in c['bits']))
        weight = min(remaining[j] for j in cycle['bits'])
        before = sum(n > 0 for n in remaining)
        remaining = [n - weight * v for n, v in zip(remaining, cycle['counts'])]
        assert balanced(remaining) and all(n >= 0 for n in remaining)
        assert sum(n > 0 for n in remaining) < before
        terms.append(dict(cycle=cycle['name'], weight=weight))
    by_name = {c['name']: c['counts'] for c in cycles}
    assert counts == [sum(t['weight'] * by_name[t['cycle']][j] for t in terms)
                      for j in range(10)]
    return terms


def report():
    assert len({frozenset((u, v)) for u, v, _, _ in EDGES}) == 10
    ordered = sorted(EDGES, key=lambda e: e[2])
    incidence = [[int(u == i) - int(v == i) for u, v, _, _ in ordered]
                 for i in range(5)]
    totals = [[int(j in (X[i], Y[i], Y[(i - 2) % 5])) for j in range(10)]
              for i in range(5)]
    differences = [[x - y for x, y in zip(row, totals[0])] for row in totals[1:]]
    basis = rref(incidence)
    assert basis == rref(differences) and len(basis) == 4
    assert balanced([1] * 10)  # Strictly positive point: cone dimension is also six.
    cycles = simple_cycles()
    by_name = {c['name']: c for c in cycles}

    table = obligations()
    accepted, rejected = [], []
    for mask in range(1024):
        active = [c for c in cycles if c['mask'] & mask == c['mask']]
        counts = [sum(c['counts'][j] for c in active) for j in range(10)]
        cyclic = support(counts) == mask
        blocked = [(u, v, bit, reachable(mask, v)) for u, v, bit, _ in EDGES
                   if mask >> bit & 1 and u not in reachable(mask, v)]
        assert cyclic == (not blocked)
        old_failure = failure(mask, table)
        assert cyclic == (old_failure is None), mask
        if cyclic:
            assert balanced(counts)
            parameter_m(counts)
            accepted.append(dict(mask=mask, counts=counts,
                                 unit_cycles=[c['name'] for c in active],
                                 greedy_decomposition=decompose(counts, cycles)))
        else:
            u, v, bit, closed = blocked[0]
            # No edge leaves closed, but the selected positive edge enters it.
            assert v in closed and u not in closed
            assert all(head in closed for tail, head, j, _ in EDGES
                       if tail in closed and mask >> j & 1)
            rejected.append(dict(mask=mask, entering_edge_bit=bit,
                                 closed_vertices=sorted(closed),
                                 kempe_failure=old_failure))
    assert len(accepted) == 154 and accepted[0]['mask'] == 0
    assert len(rejected) == 870

    saved_rays = json.loads((ROOT / 'artifacts/c5_cells/b5_face.json').read_text())
    assert saved_rays['pattern_order'] == [list(b) for b in REPS]
    raw_rays = [compress(edge_counts(p)) for p in poles()]
    assert raw_rays == [r['primitive_counts'] for r in saved_rays['rays']]
    assert {tuple(r) for r in raw_rays} == {tuple(c['counts']) for c in cycles}
    ray_map = [dict(ray=i + 1, cycle=next(c['name'] for c in cycles
                                       if c['counts'] == r))
               for i, r in enumerate(raw_rays)]

    split_covers = []
    for pairs in PAIRS:
        options = orbit_options(pairs)
        assert len(options) == 70 and len(LABELED) == 240
        covers = []
        for c in cycles:
            lifted = [c['counts'][INDEX[normalize(b)]] for b in LABELED]
            active = {j for j, n in enumerate(lifted) if n}
            selected = [j for j, op in enumerate(options)
                        if set(op['boundaries']) <= active]
            coverage = Counter(v for j in selected for v in options[j]['boundaries'])
            assert all(coverage[j] == n for j, n in enumerate(lifted))
            covers.append(dict(cycle=c['name'], orbit_indices=selected, weight=1))
        split_covers.append(dict(pairs=pairs, options=options, covers=covers))

    faces = []
    for mask in range(32):
        p = [i for i in range(5) if mask >> i & 1]
        if any((i + 1) % 5 in p for i in p):
            continue
        allowed = by_name['t']['mask'] | sum(1 << Y[i] for i in p)
        retained = [c['name'] for c in cycles if c['mask'] & allowed == c['mask']]
        assert set(retained) == {'t'} | {f'F{i}' for i in p}
        containing = [i for i in range(5) if set(p) <= {i, (i - 2) % 5}]
        assert containing
        for i in containing:
            assert by_name['t']['counts'][X[i]] == 1
            assert all(by_name[f'F{j}']['counts'][X[i]] == 0 for j in p)
        faces.append(dict(singleton_support=p, retained_cycles=retained,
                          star_coefficient_read_at_X=containing))
    assert len(faces) == 11

    perturbed = [1] * 10
    perturbed[X[0]] += 1
    broken_star = by_name['t']['mask'] ^ (1 << X[0])
    assert not balanced(perturbed) and len(set(chord_totals(perturbed))) > 1
    assert failure(broken_star, table) is not None
    assert by_name['t']['m'] == 1 and failure(by_name['t']['mask'], table) is None
    assert not by_name['t']['mask'] & by_name['W']['mask']
    sources = [Path(__file__), ROOT / 'scripts/c5_kempe_screen.py',
               ROOT / 'scripts/c5_adjacent_singleton_counts.py',
               ROOT / 'scripts/c5_b5_face.py', ROOT / 'artifacts/c5_cells/b5_face.json']
    return dict(
        trust='Paper circulation algebra plus exact finite certificates. '
              'Independent split decompositions are not one graph/coloring space. '
              'No planar realizability theorem or new Lean proof.',
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sources},
        summary=dict(rank=4, dimension=6, simple_cycles=12,
                     nonempty_masks=1023, accepted_nonempty=153, rejected=870,
                     screen_mismatches=0, zero_mask_accepted=True,
                     b5_ray_matches=12, split_cycle_covers=36,
                     labeled_coordinates_per_cover=240, independent_faces=11),
        pattern_order=REPS,
        edges=[dict(tail=u, head=v, bit=j, name=name) for u, v, j, name in EDGES],
        linear_algebra=dict(incidence=incidence, chord_totals=totals,
                            chord_total_differences=differences,
                            common_rref=[[str(v) for v in row] for row in basis]),
        cycles=cycles, accepted=accepted, rejected=rejected, b5_ray_map=ray_map,
        labeled_assignments=LABELED, split_orbit_covers=split_covers,
        independent_faces=faces,
        negative_controls=dict(perturbed_counts=perturbed, broken_star_mask=broken_star,
                               pure_star_mask=by_name['t']['mask'],
                               disjoint_wheel_mask=by_name['W']['mask']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    data = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'C5 circulation certificate differs'
    else:
        OUT.write_text(data)
    print(json.dumps(result['summary'], sort_keys=True))
