#!/usr/bin/env python3
"""Exact counting identities and abstract Kempe countermodels; no graph search.

python3 scripts/c5_adjacent_singleton_counts.py [--check]
Disk topology is a paper premise. Countermodels below are count vectors, NOT
realizing graphs. All arithmetic and orbit coverage checks are exact integers.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_kempe_screen import (REPS, INDEX, PAIRS, normalize, partitions,
                            noncrossing, push)

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / 'artifacts/c5_cells/cells.json'
SCREEN = ROOT / 'artifacts/c5_cells/kempe_screen.json'
OUT = ROOT / 'artifacts/c5_cells/adjacent_singleton_counts.json'
CYCLE = tuple((i, (i + 1) % 5) for i in range(5))
CHORDS = tuple((u, v) for u, v in combinations(range(5), 2)
               if (u - v) % 5 not in (1, 4))
FOUR = {next((u, v) for u, v in CHORDS if b[u] == b[v]): j
        for j, b in enumerate(REPS) if max(b) == 3}
THREE = {next(i for i in range(5) if b.count(b[i]) == 1): j
         for j, b in enumerate(REPS) if max(b) == 2}
LABELED = tuple(b for b in product(range(4), repeat=5)
                if all(b[u] != b[v] for u, v in CYCLE))
LAB_INDEX = {b: i for i, b in enumerate(LABELED)}


def chord_totals(counts):
    return [counts[FOUR[u, v]] + counts[THREE[u]] + counts[THREE[v]]
            for u, v in CHORDS]


def identity(counts):
    return len(set(chord_totals(counts))) == 1


def count_extensions(k, edges):
    edges = set(CYCLE) | {tuple(sorted(e)) for e in edges}
    result = []
    for b in REPS:
        result.append(sum(all(c[u] != c[v] for u, v in edges)
                          for inner in product(range(4), repeat=k)
                          for c in [b + inner]))
    return result


def orbit_options(pairs):
    """Labeled boundary swap orbits, with a noncrossing partition witness."""
    found = {}
    for b in LABELED:
        for p in partitions([i for i in range(5) if b[i] in pairs[0]]):
            for q in partitions([i for i in range(5) if b[i] in pairs[1]]):
                blocks = p + q
                if not noncrossing(blocks):
                    continue
                owner = {v: j for j, block in enumerate(blocks) for v in block}
                if any(any(b[u] in pair and b[v] in pair for pair in pairs)
                       and owner[u] != owner[v] for u, v in CYCLE):
                    continue
                orbit = []
                for selected in range(1 << len(blocks)):
                    c = list(b)
                    for j, block in enumerate(blocks):
                        if selected >> j & 1:
                            pair = next(pair for pair in pairs if b[block[0]] in pair)
                            for i in block:
                                c[i] = pair[1] if b[i] == pair[0] else pair[0]
                    orbit.append(LAB_INDEX[tuple(c)])
                key = tuple(sorted(orbit))
                assert len(key) == len(set(key))
                found.setdefault(key, dict(start=LAB_INDEX[b], blocks=blocks))
    return [dict(boundaries=o, **found[o]) for o in sorted(found)]


def support(counts):
    return sum(1 << i for i, n in enumerate(counts) if n)


def report():
    catalog = json.loads(CAT.read_text())
    assert catalog['pattern_order'] == [list(b) for b in REPS]
    # The inclusion-exclusion proof uses these noncrossing partition indicators.
    nc = [p for p in partitions(list(range(5))) if noncrossing(p)]
    basis = []
    for p in nc:
        vec = [int(all(len({b[i] for i in block}) == 1 for block in p)) for b in REPS]
        assert identity(vec)
        if any(vec):
            basis.append(dict(blocks=p, counts=vec))
    assert len(nc) == 42 and len(basis) == 6
    witnesses = []
    for mask, entry in sorted(catalog['cells'].items(), key=lambda x: int(x[0])):
        counts = count_extensions(entry['k_eff'], entry['edges'])
        assert support(counts) == int(mask)
        assert identity(counts), (mask, counts)
        witnesses.append(dict(mask=int(mask), counts=counts,
                              common_total=chord_totals(counts)[0]))
    # Crossing boundary chords are not a disk realization in the specified order.
    crossing = count_extensions(0, [(0, 2), (1, 3)])
    assert not identity(crossing)
    perturbed = [1] * 10
    perturbed[0] += 1
    assert not identity(perturbed)
    # T is abstract. F_i is the actual triangulated pentagon fan at v_i.
    t = [int(max(b) == 3) for b in REPS]
    fans = [count_extensions(0, [e for e in CHORDS if i in e]) for i in range(5)]
    for i, f in enumerate(fans):
        assert f[THREE[i]] == 1 and sum(f[j] for j in THREE.values()) == 1
        assert all(f[j] == int(i not in e) for e, j in FOUR.items())
    templates = [t] + fans
    options = [orbit_options(pairs) for pairs in PAIRS]
    covers = []
    for counts in templates:
        split_covers = []
        active = {j for j, b in enumerate(LABELED) if counts[INDEX[normalize(b)]]}
        for ops in options:
            selected = [j for j, op in enumerate(ops) if set(op['boundaries']) <= active]
            coverage = Counter(v for j in selected for v in ops[j]['boundaries'])
            assert all(coverage[j] == counts[INDEX[normalize(b)]]
                       for j, b in enumerate(LABELED))
            split_covers.append(selected)
        covers.append(split_covers)
    countermodels = []
    independent = [p for n in range(3) for p in combinations(range(5), n)
                   if all((u-v) % 5 not in (1, 4) for u, v in combinations(p, 2))]
    for p in independent:
        counts = [t[j] + sum(fans[i][j] for i in p) for j in range(10)]
        assert identity(counts)
        certificates = []
        for split, ops in enumerate(options):
            weights = Counter(covers[0][split])
            for i in p:
                weights.update(covers[i + 1][split])
            coverage = Counter()
            for j, weight in weights.items():
                for v in ops[j]['boundaries']:
                    coverage[v] += weight
            assert all(coverage[j] == counts[INDEX[normalize(b)]]
                       for j, b in enumerate(LABELED))
            certificates.append([[j, weights[j]] for j in sorted(weights)])
        countermodels.append(dict(singleton_support=p, mask=support(counts), counts=counts,
                                  common_total=chord_totals(counts)[0],
                                  orbit_weights=certificates))
    screen = json.loads(SCREEN.read_text())
    known = set(map(int, catalog['cells']))
    combined = set(screen['kempe_masks']) - set(map(int, screen['exterior_rejections']))
    assert len(combined) == 142
    assert all(push(s, v, spoke) in combined for s in combined
               for v in range(5) for spoke in (False, True))
    for row in countermodels:
        if row['singleton_support']:
            assert row['mask'] in combined - known
        else:
            assert row['mask'] in set(map(int, screen['exterior_rejections']))
    return dict(
        trust='Exact external integer checks; counting identity has a paper disk-topology proof, not Lean. Abstract count vectors do not assert graph realizability.',
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                for p in (CAT, SCREEN, ROOT / 'scripts/c5_kempe_screen.py', Path(__file__))},
        pattern_order=REPS, chord_order=CHORDS,
        noncrossing_partitions=len(nc), nonzero_partition_indicators=basis,
        catalogue_witnesses=witnesses,
        labeled_boundary_order=LABELED, complementary_splits=PAIRS,
        orbit_options=options, template_counts=templates, template_covers=covers,
        abstract_countermodels=countermodels,
        controls=dict(crossing_chord_counts=crossing, crossing_chord_totals=chord_totals(crossing),
                      perturbed_counts_rejected=True),
        combined_push=dict(states=len(combined), transitions=len(combined)*10, failures=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Report differs; inspect before regeneration.'
    else:
        OUT.write_text(encoded)
    print(json.dumps(dict(witnesses=len(result['catalogue_witnesses']),
                          noncrossing_partitions=result['noncrossing_partitions'],
                          abstract_countermodels=len(result['abstract_countermodels']),
                          combined_push=result['combined_push']), sort_keys=True))


if __name__ == '__main__':
    main()
