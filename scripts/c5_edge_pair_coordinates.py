#!/usr/bin/env python3
"""Exact C5 edge-pair coordinates and an equivalent finite Kempe screen.

No graph search, realizability oracle, or new topology formalization.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_kempe_screen import REPS, failure, normalize, obligations

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/edge_pair_coordinates.json'


def difference(b):
    return tuple(b[i] ^ b[(i + 1) % 5] for i in range(5))


def minority_pair(b):
    d = difference(b)
    return tuple(i for i in range(5) if d.count(d[i]) == 1)


PAIRS = tuple(map(minority_pair, REPS))


def clauses():
    result = []
    for source, pair in enumerate(PAIRS):
        for fixed in pair:
            moving = next(i for i in pair if i != fixed)
            cycle = [i for i in range(5) if i != fixed]
            alternatives = [cycle[(cycle.index(moving) + step) % 4]
                            for step in (-1, 1)]
            targets = sorted(PAIRS.index(tuple(sorted((fixed, r))))
                             for r in alternatives)
            result.append(dict(source=source, fixed=fixed, moving=moving,
                               targets=targets))
    return result


def accepts(mask, rules):
    return all(not (mask >> c['source'] & 1)
               or any(mask >> j & 1 for j in c['targets']) for c in rules)


def report():
    assignments = [b for b in product(range(4), repeat=5)
                   if all(b[i] != b[(i + 1) % 5] for i in range(5))]
    words = Counter(map(difference, assignments))
    assert len(assignments) == 240 and len(words) == 60
    assert set(words.values()) == {4}
    assert set(PAIRS) == set(combinations(range(5), 2))
    orbit_sizes = Counter(normalize(b) for b in assignments)
    assert set(orbit_sizes.values()) == {24}
    for d in words:
        assert sorted(Counter(d).values()) == [1, 1, 3]
        for initial in range(4):
            b = [initial]
            for x in d[:-1]:
                b.append(b[-1] ^ x)
            assert difference(b) == d

    # Every S4 permutation is uniquely translation composed with a linear map.
    affine_checks = 0
    for p in permutations(range(4)):
        t = p[0]
        linear = tuple(p[x] ^ t for x in range(4))
        assert all(linear[x ^ y] == (linear[x] ^ linear[y])
                   for x, y in product(range(4), repeat=2))
        for b in assignments:
            image = tuple(p[x] for x in b)
            assert difference(image) == tuple(linear[x] for x in difference(b))
            assert minority_pair(image) == minority_pair(b)
            affine_checks += 1

    # Active vertex action i -> sign*i+r. Reflection has a -1 edge offset.
    dihedral_checks = 0
    for sign, r in product((1, -1), range(5)):
        for b in assignments:
            image = [None] * 5
            for i, color in enumerate(b):
                image[(sign * i + r) % 5] = color
            edge_image = lambda i: (i + r) % 5 if sign == 1 else (r - i - 1) % 5
            assert minority_pair(image) == tuple(sorted(map(edge_image, minority_pair(b))))
            dihedral_checks += 1

    rows = []
    for bit, b in enumerate(REPS):
        p = PAIRS[bit]
        three = max(b) == 2
        assert three == ((p[0] - p[1]) % 5 in (1, 4))
        singleton = next((i for i in range(5) if b.count(b[i]) == 1), None) if three else None
        if three:
            assert p == tuple(sorted(((singleton - 1) % 5, singleton)))
        rows.append(dict(bit=bit, pattern=''.join(map(str, b)),
                         differences=difference(b), edge_pair=p,
                         vertex_colors=max(b) + 1, singleton=singleton))

    rules = clauses()
    table = obligations()
    accepted = []
    for mask in range(1024):
        actual = accepts(mask, rules)
        assert actual == (failure(mask, table) is None), mask
        # Independent formulation: every selected neighbor has a selected C4 neighbor.
        graph_rule = True
        for fixed in range(5):
            cycle = [i for i in range(5) if i != fixed]
            neighbors = {next(x for x in PAIRS[j] if x != fixed)
                         for j in range(10) if mask >> j & 1 and fixed in PAIRS[j]}
            graph_rule &= all(any(cycle[(cycle.index(j) + step) % 4] in neighbors
                                     for step in (-1, 1)) for j in neighbors)
        assert actual == graph_rule
        if actual and mask:
            accepted.append(mask)
    assert len(rules) == 20 and len(accepted) == 153
    t4 = sum(1 << j for j, b in enumerate(REPS) if max(b) == 3)
    supersets = [s for s in range(1024) if s & t4 == t4]
    assert len(supersets) == 32 and all(s in accepted for s in supersets)

    catalogue_path = ROOT / 'artifacts/c5_cells/cells.json'
    catalogue = json.loads(catalogue_path.read_text())
    assert catalogue['pattern_order'] == [list(b) for b in REPS]
    known = set(map(int, catalogue['cells']))
    assert len(known) == 132 and known <= set(accepted)
    exterior = [s for s in accepted if all(s & t for t in known)]
    assert len(exterior) == 142
    remaining = sorted(set(exterior) - known)
    assert len(remaining) == 10
    sources = [Path(__file__), ROOT / 'scripts/c5_kempe_screen.py', catalogue_path]
    return dict(evidence='Finite coordinate and predicate equivalence; not disk realizability.',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in sources},
                checks=dict(assignments=240, edge_words=60, color_equivariance=affine_checks,
                            dihedral_equivariance=dihedral_checks, masks=1024),
                rows=rows, clauses=rules, nonempty_accepted=accepted,
                all_T4_supersets=supersets, exterior_accepted=exterior,
                remaining_unknown=remaining)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = report()
    encoded = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate mismatch; regenerate and review.'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print('C5 edge pairs: 240 assignments, 60 words, 20 clauses; 1024 masks agree; '
          '153 nonempty / 142 exterior / 10 unknown.')


if __name__ == '__main__':
    main()
