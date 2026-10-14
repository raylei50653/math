#!/usr/bin/env python3
"""All-lift control for deleting original degree-six r, retaining p,q.

The Kempe control is necessary only: actual sources and full multiplicities
are not represented. Its sole noncrossing input is the honest outer C5.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = tuple(range(4))
PINS = ('z', 's', 'v', 'w', 't', 'p', 'q')
EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (5, 6), (6, 0))
PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
CATALOGUE_SHA256 = '04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def name(row):
    return ''.join('ABCD'[c] for c in row)


def old_allowed(q, pq):
    """Exact old upper joint relation, with the Kempe-derived ABCB restriction."""
    z, s, r, t = q
    if any(q[i] == q[(i + 1) % 4] for i in range(4)):
        return False
    if len(set((z,) + tuple(pq))) != 3:
        return False
    if z == r:
        return s == t and set(pq) == set(COLORS) - {z, s}
    if s == t:
        return bool(set(pq) & (set(COLORS) - set(q)))
    return set(pq) == {s, t}


def lifts(row):
    return tuple(c for c in COLORS if c not in row[1:5])


def allowed(row, edges=EDGES):
    if any(row[a] == row[b] for a, b in edges):
        return False
    z, s, v, w, t, p, q = row
    return all(old_allowed((z, s, r, t), (p, q)) for r in lifts(row))


def independent_allowed(row):
    """Separate restricted-growth case table, with one global colour frame."""
    if any(row[a] == row[b] for a, b in EDGES):
        return False
    table = {
        (0, 1, 0, 1): ((2, 3), (3, 2)),
        (0, 1, 0, 2): (),
        (0, 1, 2, 1): ((1, 3), (2, 3), (3, 1), (3, 2)),
        (0, 1, 2, 3): ((1, 3), (3, 1)),
    }
    for r in COLORS:
        if all(r != row[i] for i in (1, 2, 3, 4)):
            lifted = canonical((row[0], row[1], r, row[4], row[5], row[6]))
            if lifted[4:] not in table[lifted[:4]]:
                return False
    return True


def partitions(items):
    if not items:
        yield ()
        return
    first = items[0]
    for part in partitions(items[1:]):
        yield ((first,),) + part
        for i, block in enumerate(part):
            yield part[:i] + ((first,) + block,) + part[i + 1:]


def noncrossing(part):
    labels = {v: i for i, block in enumerate(part) for v in block}
    return all(not (labels[a] == labels[c] and labels[b] == labels[d]
                   and labels[a] != labels[b])
               for a, b, c, d in combinations(range(5), 4))


@lru_cache(None)
def pair_partitions(row, pair, edges):
    vertices = tuple(v for v, color in enumerate(row) if color in pair)
    mandatory = [(a, b) for a, b in edges if a in vertices and b in vertices]
    result = []
    for part in partitions(vertices):
        labels = {v: i for i, block in enumerate(part) for v in block}
        if all(labels[a] == labels[b] for a, b in mandatory):
            result.append(part)
    return tuple(result)


def switch_orbit(row, parts, pairing):
    blocks = parts[0] + parts[1]
    pairs = (pairing[0],) * len(parts[0]) + (pairing[1],) * len(parts[1])
    result = set()
    for mask in range(1 << len(blocks)):
        successor = list(row)
        for i, block in enumerate(blocks):
            if mask >> i & 1:
                a, b = pairs[i]
                for v in block:
                    successor[v] = b if successor[v] == a else a
        result.add(canonical(successor))
    return frozenset(result)


def options(row, pairing, edges):
    result = []
    for parts in product(*(pair_partitions(row, pair, edges) for pair in pairing)):
        if noncrossing(parts[0] + parts[1]):
            result.append((parts, switch_orbit(row, parts, pairing)))
    return result


def fixed_point(rows, edges):
    opts = {row: [options(row, pairing, edges) for pairing in PAIRINGS] for row in rows}
    live = set(rows)
    rounds = []
    while True:
        dead = {row for row in live if any(
            not any(orbit <= live for parts, orbit in choices)
            for choices in opts[row])}
        rounds.append({'live': [name(row) for row in sorted(live)],
                       'removed': [name(row) for row in sorted(dead)]})
        if not dead:
            break
        live -= dead
    witnesses = []
    for row in sorted(live):
        records = []
        for pairing, choices in zip(PAIRINGS, opts[row]):
            passing = [{'parts': parts, 'successors': [name(x) for x in sorted(orbit)]}
                       for parts, orbit in choices if orbit <= live]
            need(bool(passing), 'missing survivor option')
            records.append({'pairing': pairing, 'options': passing})
        witnesses.append({'row': name(row), 'pairings': records})
    return live, {'rounds': rounds, 'survivors': witnesses}


def calculate():
    catalogue_bytes = (HERE / 'cells.json').read_bytes()
    need(sha256(catalogue_bytes).hexdigest() == CATALOGUE_SHA256, 'frozen catalogue drift')
    catalogue = json.loads(catalogue_bytes)
    patterns = [tuple(row) for row in catalogue['pattern_order']]
    masks = sorted(map(int, catalogue['cells']))
    need(len(masks) == 132, 'catalogue cardinality')
    proper = {canonical(row) for row in product(COLORS, repeat=5)
              if all(row[i] != row[(i + 1) % 5] for i in range(5))}
    need(set(patterns) == proper, 'complete C5 orbit list')
    all_rows = list(product(COLORS, repeat=7))
    need(all(allowed(row) == independent_allowed(row) for row in all_rows),
         'two all-lift implementations differ')
    labelled = [row for row in all_rows if allowed(row)]
    orbits = sorted({canonical(row) for row in labelled})
    fixed_rows = []
    possible_mask = 0
    for i, boundary in enumerate(patterns):
        pq = [x for x in permutations(COLORS, 2) if allowed(boundary + x)]
        if pq:
            possible_mask |= 1 << i
        fixed_rows.append({'index': i, 'boundary': name(boundary),
                           'r_lifts': name(lifts(boundary)),
                           'ordered_pq': [name(x) for x in pq]})
    candidates = [m for m in masks if not m & ~possible_mask]
    need(possible_mask == 319 and candidates == [271, 314, 319], 'unexpected C5 screen')
    cases = []
    for extra in ((), ((4, 5),), ((1, 6),), ((4, 5), (1, 6)),
                  ((4, 5), (3, 5)), ((1, 6), (2, 6))):
        edges = EDGES + extra
        for mask in candidates:
            initial = [row for row in orbits
                       if mask >> patterns.index(canonical(row[:5])) & 1
                       and all(row[a] != row[b] for a, b in extra)]
            live, certificate = fixed_point(initial, edges)
            support = sum(1 << i for i, boundary in enumerate(patterns)
                          if any(canonical(row[:5]) == boundary for row in live))
            cases.append({'extra_edges': [(PINS[a], PINS[b]) for a, b in extra],
                          'catalogue_mask': mask, 'initial_orbits': len(initial),
                          'surviving_orbits': len(live), 'surviving_support': support,
                          'complete_support_retained': support == mask, **certificate})
    need(len(tuple(partitions(tuple(range(7))))) == 877, 'Bell number')
    need(not noncrossing(((0, 2), (1, 3), (4,), (5,), (6,))), 'crossing negative')
    need(not allowed((0, 1, 2, 1, 2, 1, 3)), 'bad lift negative')
    return {'status': 'PASS; local all-lift screen and necessary Kempe control only',
            'pins': PINS, 'skeleton_edges': EDGES, 'noncrossing_boundary': PINS[:5],
            'table': fixed_rows, 'allowed_outer_mask': possible_mask,
            'catalogue_candidates': candidates, 'labelled_rows': len(labelled),
            'orbits': [name(row) for row in orbits], 'kempe_cases': cases,
            'negative_controls': {'all_16384_rows_crosschecked': True,
                                  'Bell7_877': True, 'crossing_rejected': True,
                                  'bad_lift_rejected': True},
            'actual_target_sources': 0,
            'catalogue_sha256': CATALOGUE_SHA256,
            'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'transfer.json')
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2) + '\n'
    if args.check:
        need(args.certificate.read_text() == payload, 'transfer certificate differs')
    else:
        with args.certificate.open('x') as handle:
            handle.write(payload)
    print(json.dumps({'ok': True, 'catalogue_candidates': result['catalogue_candidates'],
                      'labelled_rows': result['labelled_rows'], 'orbits': len(result['orbits']),
                      'kempe_cases': [{key: case[key] for key in (
                          'extra_edges', 'catalogue_mask', 'surviving_orbits',
                          'surviving_support', 'complete_support_retained')}
                                      for case in result['kempe_cases']]}, sort_keys=True))


if __name__ == '__main__':
    main()
