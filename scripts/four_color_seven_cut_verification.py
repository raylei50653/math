#!/usr/bin/env python3
"""Exhaustive necessary one-step planar Kempe screen for seven cut incidences.

Standard library only; no graph-colouring solver or Four Colour Theorem oracle.
Actual component partitions on either side are among the partitions checked here.
The arbitrary-source reduction to this finite screen is a separate paper proof.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
PERMUTATIONS = tuple(permutations(range(4)))


def normalize(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def partitions(xs):
    if not xs:
        yield ()
        return
    x, *rest = xs
    for p in partitions(rest):
        yield ((x,),) + p
        for j in range(len(p)):
            yield p[:j] + ((x,) + p[j],) + p[j + 1:]


def noncrossing(blocks):
    owner = {v: j for j, block in enumerate(blocks) for v in block}
    return not any(owner[a] == owner[c] and owner[b] == owner[d]
                   and owner[a] != owner[b]
                   for a, b, c, d in combinations(sorted(owner), 4))


@lru_cache(None)
def incompatible(fixed, moving):
    cells = set(zip(fixed, moving))
    return not any(all(a != p[b] for a, b in cells) for p in PERMUTATIONS)


@lru_cache(None)
def options(row, split, planar=True):
    """Every possible boundary component partition, with every single-block swap.

    The partition joins both complementary colour pairs before noncrossing is
    tested. Different splits may choose unrelated partitions: this deliberately
    weakens same-source compatibility, so zero survivors remains sound.
    """
    pairs = SPLITS[split]
    left = [i for i, c in enumerate(row) if c in pairs[0]]
    right = [i for i, c in enumerate(row) if c in pairs[1]]
    result = []
    for p in partitions(left):
        for q in partitions(right):
            blocks = p + q
            if planar and not noncrossing(blocks):
                continue
            swaps = []
            for block in blocks:
                pair = next(pair for pair in pairs if row[block[0]] in pair)
                changed = list(row)
                for i in block:
                    changed[i] = sum(pair) - changed[i]
                swaps.append(normalize(changed))
            result.append(tuple(swaps))
    return tuple(result)


def first_obstruction(fixed, moving, planar=True):
    """A failed split means every admissible partition has a gluable block swap."""
    for split in range(3):
        if not any(all(incompatible(fixed, changed) for changed in swaps)
                   for swaps in options(moving, split, planar)):
            return split
    return None


def partition_controls():
    # Independently generate all partitions by restricted-growth words.
    generated = {normalize(tuple(j for i in range(7)
                                 for j, block in enumerate(p) if i in block))
                 for p in partitions(list(range(7)))}
    independent = {word for word in product(range(7), repeat=7)
                   if all(word[i] <= max(word[:i], default=-1) + 1
                          for i in range(7))}
    assert generated == independent and len(generated) == 877
    assert sum(noncrossing(p) for p in partitions(list(range(7)))) == 429
    assert not noncrossing(((0, 2), (1, 3)))
    assert noncrossing(((0, 3), (1, 2)))
    return dict(bell_7=877, noncrossing_partitions_7=429,
                independent_generators_equal=True)


def algebra_controls():
    # The proposed stronger assertion p0~i in the 02 partition is false.
    a = (0, 0, 0, 1, 1, 1, 2)
    b = (0, 1, 2, 0, 1, 2, 0)
    anchor_results = []
    for mask in range(8):
        changed = list(a)
        for i in range(3):
            if mask >> i & 1:
                changed[i] = 3
        blocked = incompatible(b, normalize(changed))
        assert blocked == (mask in (0, 7))
        anchor_results.append(blocked)
    allowed = []
    for blocks in partitions([0, 1, 2, 6]):
        stays_blocked = True
        for block in blocks:
            changed = list(a)
            for i in block:
                changed[i] = 2 - changed[i]
            stays_blocked &= incompatible(b, normalize(changed))
        if stays_blocked:
            allowed.append(tuple(sorted(tuple(sorted(block)) for block in blocks)))
    expected = {((0, 1, 2), (6,)), ((0, 6), (1, 2)), ((0, 1, 2, 6),)}
    assert set(allowed) == expected
    assert all(any(1 in block and 2 in block for block in p) for p in allowed)
    return dict(X_03_three_point_subset_swaps_blocked=anchor_results,
                X_02_allowed_partitions=[list(map(list, p)) for p in sorted(allowed)],
                terminal_order=['p0', 'p1', 'p2', 'q0', 'q1', 'q2', 'i'],
                p1_p2_must_connect=True, p0_i_need_not_connect=True)


def report():
    controls = partition_controls()
    algebra = algebra_controls()
    rows = sorted({normalize(row) for row in product(range(3), repeat=7)
                   if len(set(row)) == 3})
    assert len(rows) == 301
    pairs = [(a, b) for a in rows for b in rows if incompatible(a, b)]
    assert len(pairs) == 2520
    signatures = []
    outcomes = Counter()
    orientations = Counter()
    for a, b in pairs:
        cells = set(zip(a, b))
        rectangles = [set(product(rs, cs))
                      for height, width in ((2, 3), (3, 2))
                      for rs in combinations(sorted(set(a)), height)
                      for cs in combinations(sorted(set(b)), width)
                      if set(product(rs, cs)) <= cells]
        assert len(cells) == 7 and len(rectangles) == 1
        assert len(cells - rectangles[0]) == 1
        y_obstruction = first_obstruction(a, b)
        x_obstruction = first_obstruction(b, a)
        y_survives = y_obstruction is None
        x_survives = x_obstruction is None
        outcomes[f'X_{int(x_survives)}_Y_{int(y_survives)}'] += 1
        shape = ''.join(map(str, sorted(Counter(a).values(), reverse=True)))
        orientations[f'a_{shape}_total'] += 1
        if y_survives:
            orientations[f'a_{shape}_Y_survives'] += 1
        assert not (x_survives and y_survives)
        assert first_obstruction(a, b, planar=False) is None
        assert first_obstruction(b, a, planar=False) is None
        signatures.append([a, b, x_obstruction, y_obstruction])
    assert outcomes == Counter(X_0_Y_0=1400, X_1_Y_0=560, X_0_Y_1=560)
    assert orientations == Counter(a_331_total=1260, a_322_total=1260,
                                   a_331_Y_survives=168, a_322_Y_survives=392)
    # Fixed labelled terminals, cyclic orders modulo rotation, singleton omitted.
    terminals = ('p0', 'q0', 'p1', 'q1', 'p2', 'q2')
    adjacent = 0
    for tail in permutations(terminals[1:]):
        cycle = (terminals[0],) + tail
        if all((cycle.index(f'p{c}') - cycle.index(f'q{c}')) % 6 in (1, 5)
               for c in range(3)):
            adjacent += 1
    assert adjacent == 16
    return dict(
        scope='Necessary one-component-swap screen, all 2520 canonical 3/3 Hall failures; arbitrary planar sources handled by paper proof, not enumerated.',
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        fixed_source='4476049',
        counts=dict(exactly_three_colour_rows=301, ordered_pairs=301 ** 2,
                    Hall_failures=2520, X_single_side_survivors=560,
                    Y_single_side_survivors=560, both_side_survivors=0,
                    without_topology_both_side_survivors=2520),
        outcome_counts=dict(sorted(outcomes.items())),
        orientation_counts=dict(sorted(orientations.items())),
        circular_labelled_orders=dict(six_terminals_mod_rotation=16,
                                      after_singleton_insertion_mod_rotation=96,
                                      canonical_a331_Y_survivors=168),
        exhaustive_decision_sha256=sha256(json.dumps(signatures, separators=(',', ':')).encode()).hexdigest(),
        controls=controls,
        algebra_controls=algebra,
        assertions=dict(all_failures_rectangle_plus_one=True,
                        all_24_colour_permutations_checked=True,
                        all_homogeneous_noncrossing_partitions_checked=True,
                        only_single_component_swaps_used=True,
                        both_sides_use_same_incidence_cycle=True,
                        no_cross_split_compatibility_assumed=True,
                        repeated_endpoint_identifications_not_needed=True,
                        arbitrary_planar_source_enumeration=False,
                        lean_proof=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
