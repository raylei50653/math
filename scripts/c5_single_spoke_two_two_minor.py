#!/usr/bin/env python3
"""Replay residual support symmetry and source-fixed K5 extraction controls.

No source graph search. The original (2,2) table remains an immutable input;
arbitrary-size coverage is the paper argument, not the finite controls.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_two_two_minor/observations.json'
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)
PERMS = tuple(permutations(range(4)))
EXPECTED_IDS = [110, 111, 116, 117, 119, 120, 125, 126, 130, 131, 132,
                133, 134, 348, 351, 352, 353, 354, 355, 356, 357, 358,
                367, 368, 369, 370]


def subsets(values):
    values = sorted(values)
    return [frozenset(c) for n in range(len(values) + 1)
            for c in combinations(values, n)]


def residual_audit():
    rows = []
    for pair in combinations(range(4), 2):
        f = frozenset(pair)
        for contact, direct, branches in product((False, True), subsets(U), subsets(U)):
            if direct & branches:
                continue  # Incident palettes lie in both original lists.
            lists = [U - direct - ({a} if contact else set()) for a in pair]
            if any(not branches <= ls for ls in lists):
                continue
            expected = [f - {a} if contact else f for a in pair]
            if [ls - branches for ls in lists] != expected:
                continue
            assert direct | branches == U - f
            rows.append(dict(forbidden=pair, contact=contact,
                             direct_colors=sorted(direct),
                             branch_palette_union=sorted(branches),
                             residual_without_z=sorted(U - direct - branches)))
    assert len(rows) == 48
    return rows


def support_audit():
    """All local supports, all pair bans, and all 24 pointwise stabilizers."""
    rows = []
    for pair in combinations(range(4), 2):
        f = frozenset(pair)
        required_colors = U - f if 3 in f else f
        for support in subsets(range(5)):
            seen = {Q[i] for i in support}
            stabilizer = [p for p in PERMS if all(p[c] == c for c in seen)]
            violating = [p for p in stabilizer if {p[c] for c in f} != f]
            assert (not violating) == (required_colors <= seen)
            if f == {1, 2} and 1 not in support and not violating:
                assert {3, 4} <= support
            rows.append(dict(forbidden=pair, actual_support=sorted(support),
                             required_colors=sorted(required_colors),
                             invariant=not violating,
                             violating_permutation=violating[0] if violating else None))
    assert len(rows) == 192
    return rows


def connected(bag, edges):
    if not bag:
        return False
    seen = {min(bag)}
    while True:
        more = seen | {v for u, v in edges if u in seen and v in bag}
        more |= {u for u, v in edges if v in seen and u in bag}
        if more == seen:
            return seen == bag
        seen = more


def verify_minor(edges, bags):
    assert len(bags) == 5
    used = set()
    for bag in bags:
        assert not used & bag and connected(bag, edges)
        used |= bag
    witnesses = []
    for i, j in combinations(range(5), 2):
        choices = [(u, v) for u, v in sorted(edges)
                   if (u in bags[i] and v in bags[j]) or
                      (v in bags[i] and u in bags[j])]
        assert choices, (i, j)
        witnesses.append(dict(bags=[i, j], edge=choices[0]))
    return witnesses


def control(length, edge_index, styles):
    """An extracted topology skeleton, not a degree/list-realizable source."""
    assert length % 2 == 1 and 1 <= edge_index <= length
    edges = set()

    def edge(u, v):
        assert u != v
        edges.add(tuple(sorted((u, v))))

    for i in range(5):
        edge(f'b{i}', f'b{(i + 1) % 5}')
    path = [f'x{i}' for i in range(length + 1)]
    for u, v in zip(path, path[1:]):
        edge(u, v)
    edge('z', path[0])
    edge('z', path[-1])
    edge('z', 'b0')
    endpoints = path[edge_index - 1:edge_index + 1]
    bags = []
    tethers = []
    for root, style in zip(endpoints, styles):
        bag = {root}
        if style == 'direct':
            routes = [[root, 'b3'], [root, 'b4']]
        elif style == 'shared_trunk':
            w = root + '_w'
            routes = [[root, w, 'b3'], [root, w, 'b4']]
        else:
            y, w = root + '_y', root + '_w'
            routes = [[root, y, 'b3'], [root, w, 'b4']]
            if style == 'shared_cycle':
                edge(y, w)
        for route in routes:
            bag.update(route[:-1])
            for u, v in zip(route, route[1:]):
                edge(u, v)
        bags.append(bag)
        tethers.append(routes)
    bags += [({'z', 'b0', 'b1', 'b2'} | set(path)) - set(endpoints),
             {'b3'}, {'b4'}]
    witnesses = verify_minor(edges, bags)
    return dict(length=length, edge_index=edge_index, styles=styles,
                edges=sorted(edges), branch_sets=[sorted(b) for b in bags],
                actual_tether_routes=tethers, adjacencies=witnesses)


def negative_controls():
    base = control(1, 1, ('direct', 'direct'))
    edges = set(map(tuple, base['edges']))
    bags = list(map(set, base['branch_sets']))
    broken = [
        ('missing_spoke', edges - {('b0', 'z')}, bags),
        ('missing_tether', edges - {('b3', 'x0')}, bags),
        ('overlapping_bags', edges, [bags[0] | {'x1'}] + bags[1:]),
    ]
    rejected = []
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(f'negative control passed: {name}')
    return rejected


def refine_table():
    data = json.loads(SOURCE.read_text())
    excluded, retained = [], []
    for row in data['records']:
        if row['T4_status'] != 'retained':
            continue
        components = [k for k, (support, ban) in enumerate(zip(row['supports'], row['bans']))
                      if row['spoke'] == 0 and ban == [1, 2] and 1 not in support]
        if components:
            assert all({3, 4} <= set(row['supports'][k]) for k in components)
            excluded.append(dict(source_id=row['id'], witness_components=components,
                                 original_record=row,
                                 source_status='excluded_by_source_fixed_K5'))
        else:
            retained.append(row)
    assert [r['source_id'] for r in excluded] == EXPECTED_IDS
    assert len(retained) == 354
    keys = {(r['spoke'], tuple(map(tuple, r['supports'])), tuple(map(tuple, r['bans'])))
            for r in retained}
    assert len(keys) == len(retained)
    for s, supports, bans in keys:
        swapped = (s, supports[::-1], bans[::-1])
        assert swapped in keys and swapped != (s, supports, bans)
    assert len({min(key, (key[0], key[1][::-1], key[2][::-1])) for key in keys}) == 177
    counts = Counter('/'.join(t['status'] for t in r['targets']) for r in retained)
    assert counts['accept/accept'] == 104 and counts['reject/reject'] == 0
    # Reflection is carried by the inherited whole-relation transport. Save
    # its original data without separately enumerating reflected sources.
    assert all(r['original_record']['reflection']['spoke'] == 3 for r in excluded)
    return dict(excluded=excluded, remaining_source_ids=[r['id'] for r in retained],
                original_retained=380, excluded_labeled=26, remaining_labeled=354,
                remaining_component_swap_types=177, remaining_targets=dict(sorted(counts.items())))


def build():
    controls = [control(length, i, styles) for length in (1, 3, 5, 7)
                for i in range(1, length + 1)
                for styles in product(('direct', 'separate_bridges', 'shared_cycle',
                                       'shared_trunk'), repeat=2)]
    assert len(controls) == 256
    paths = [SOURCE, Path(__file__), ROOT / 'scripts/c5_single_spoke_two_two.py',
             ROOT / 'scripts/c5_single_spoke_bridge_path.py',
             ROOT / 'scripts/c5_single_spoke_branch_palettes.py']
    return dict(scope='paper source exclusion; finite residual/symmetry/minor controls only',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in paths},
                residual_rows=residual_audit(), support_rows=support_audit(),
                minor_controls=controls, negative_controls=negative_controls(),
                table=refine_table())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(dict(residual_rows=len(result['residual_rows']),
                          support_rows=len(result['support_rows']),
                          minor_controls=len(result['minor_controls']),
                          excluded=result['table']['excluded_labeled'],
                          remaining=result['table']['remaining_labeled'],
                          remaining_targets=result['table']['remaining_targets']), sort_keys=True))


if __name__ == '__main__':
    main()
