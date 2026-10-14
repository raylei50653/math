#!/usr/bin/env python3
"""Necessary six-pin Kempe control; no graph realizability is asserted."""
import argparse
import itertools
import json
from functools import lru_cache
from hashlib import sha256
from pathlib import Path

PINS = ('z', 's', 'r', 't', 'p', 'q')
COLORS = range(4)
EDGES = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (4, 5), (5, 0))
PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
Q_TYPES = ((0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 2, 1), (0, 1, 2, 3))


def canonical(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def name(row):
    return ''.join('ABCD'[c] for c in row)


def allowed(row):
    if any(row[a] == row[b] for a, b in EDGES):
        return False
    q_type = canonical(row[:4])
    if q_type == Q_TYPES[0]:
        return set(row[4:]) == set(COLORS) - set(row[:4])
    if q_type == Q_TYPES[2]:
        return True
    if q_type == Q_TYPES[3]:
        return set(row[4:]) == {row[1], row[3]}
    return False


def partitions(items):
    """Every set partition, once; order is deterministic."""
    if not items:
        yield ()
        return
    first = items[0]
    for part in partitions(items[1:]):
        yield ((first,),) + part
        for index, block in enumerate(part):
            yield part[:index] + ((first,) + block,) + part[index + 1:]


def outer_noncrossing(part):
    """Only the honest Jordan boundary Q is used, not a pinched boundary."""
    labels = {v: i for i, block in enumerate(part) for v in block}
    z, s, r, t = (labels[v] for v in range(4))
    return not (z == r and s == t and z != s)


@lru_cache(None)
def pair_partitions(row, pair):
    vertices = tuple(v for v, c in enumerate(row) if c in pair)
    edges = tuple((a, b) for a, b in EDGES if a in vertices and b in vertices)
    result = []
    for part in partitions(vertices):
        labels = {v: i for i, block in enumerate(part) for v in block}
        if all(labels[a] == labels[b] for a, b in edges):
            result.append(part)
    return tuple(result)


def switch_orbit(row, parts, pairing):
    blocks = parts[0] + parts[1]
    colors = (pairing[0],) * len(parts[0]) + (pairing[1],) * len(parts[1])
    result = set()
    for mask in range(1 << len(blocks)):
        switched = list(row)
        for i, block in enumerate(blocks):
            if mask & (1 << i):
                a, b = colors[i]
                for v in block:
                    switched[v] = b if switched[v] == a else a
        result.add(canonical(switched))
    return frozenset(result)


def all_options(row, pairing):
    result = []
    for a, b in itertools.product(*(pair_partitions(row, pair) for pair in pairing)):
        if outer_noncrossing(a + b):
            result.append((a, b, switch_orbit(row, (a, b), pairing)))
    return result


def calculate():
    labelled = [row for row in itertools.product(COLORS, repeat=6) if allowed(row)]
    rows = sorted({canonical(row) for row in labelled})
    assert len(labelled) == 216 and len(rows) == 9
    assert len(tuple(partitions(tuple(range(6))))) == 203
    options = {row: [all_options(row, pairing) for pairing in PAIRINGS] for row in rows}
    live = set(rows)
    rounds = []
    while True:
        dead = {row for row in live if any(
            not any(orbit <= live for a, b, orbit in choices)
            for choices in options[row])}
        rounds.append({'live': [name(row) for row in sorted(live)],
                       'removed': [name(row) for row in sorted(dead)]})
        if not dead:
            break
        live -= dead
    assert set(rows) - live == {(0, 1, 2, 1, 1, 2), (0, 1, 2, 1, 2, 1)}
    fixed = [[row for row in labelled if row[:4] == q] for q in Q_TYPES]
    surviving_fixed = [[row for row in group if canonical(row) in live] for group in fixed]
    assert [len(group) for group in fixed] == [2, 0, 6, 2]
    assert [len(group) for group in surviving_fixed] == [2, 0, 4, 2]
    assert sum(canonical(row) in live for row in labelled) == 168

    # Deliberate negative controls. The old three-row support-only control
    # contains ABCBBC, which fails this necessary Kempe test.
    bad = (0, 1, 2, 1, 1, 2)
    assert allowed(bad) and bad not in live
    crossing = ((0, 2), (1, 3), (4, 5))
    assert not outer_noncrossing(crossing)
    edge_split = ((0,), (1, 2, 3))
    assert edge_split not in pair_partitions((0, 1, 0, 1, 2, 3), (0, 1))
    wrong_palette = (0, 1, 0, 1, 1, 2)
    assert not allowed(wrong_palette)

    survivors = []
    for row in sorted(live):
        records = []
        for pairing, choices in zip(PAIRINGS, options[row]):
            passing = []
            for a, b, orbit in choices:
                if orbit <= live:
                    passing.append({'parts': [a, b],
                                    'successors': [name(r) for r in sorted(orbit)]})
            assert passing
            records.append({'pairing': pairing, 'options': passing})
        survivors.append({'row': name(row), 'pairings': records})
    return {
        'status': 'PASS; necessary abstract control, not a graph',
        'pins': PINS,
        'skeleton_edges': EDGES,
        'noncrossing_boundary': PINS[:4],
        'colour_pairings': PAIRINGS,
        'initial_labelled_rows': len(labelled),
        'initial_orbits': [name(row) for row in rows],
        'initial_fixed_Q_row_counts': [len(group) for group in fixed],
        'rounds': rounds,
        'surviving_labelled_rows': 168,
        'surviving_fixed_Q_row_counts': [len(group) for group in surviving_fixed],
        'surviving_fixed_Q_rows': [[name(row) for row in group] for group in surviving_fixed],
        'survivors': survivors,
        'negative_controls': {
            'old_ABCB_BC_abstract_row_rejected': True,
            'alternating_outer_partition_rejected': True,
            'mandatory_edge_split_rejected': True,
            'wrong_ABAB_palette_rejected': True,
        },
        'actual_target_sources': 0,
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('interface.json'))
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert args.certificate.read_text() == payload, 'Interface certificate differs'
    else:
        with args.certificate.open('x') as handle:
            handle.write(payload)
    print(json.dumps({'ok': True, 'orbits': [9, 7], 'fixed_Q_rows': [10, 8],
                      'surviving_labelled_rows': 168, 'actual_target_sources': 0}))


if __name__ == '__main__':
    main()
