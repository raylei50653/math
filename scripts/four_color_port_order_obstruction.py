#!/usr/bin/env python3
"""Classify every port order of one fixed five-cycle Tait pole.

No graph search and no 4CT oracle. The same 30 full edge colorings are tested
in all 120 labeled terminal orders. Per-system noncrossing admits a second,
non-disk order class; a common disk embedding admits only the cycle order.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import ck_kempe_obstruction as ck

ROOT = Path(__file__).resolve().parents[1]
PAIRS = tuple(combinations((1, 2, 3), 2))
EDGES = tuple((i, 5 + i) for i in range(5)) + tuple((i, (i + 1) % 5) for i in range(5))


def full_colorings():
    result = []
    for values in product((1, 2, 3), repeat=5):
        if any(values[i - 1] == values[i] for i in range(5)):
            continue
        spokes = tuple(6 - values[i - 1] - values[i] for i in range(5))
        labels = spokes + values
        assert all({labels[j] for j, edge in enumerate(EDGES) if v in edge} == {1, 2, 3}
                   for v in range(5))
        result.append(labels)
    assert len(result) == 30
    return result


def systems(labels):
    result = []
    for pair in PAIRS:
        adj = {v: [] for v in range(10)}
        for edge, color in zip(EDGES, labels):
            if color in pair:
                u, v = edge
                adj[u].append(v)
                adj[v].append(u)
        todo = {v for v in adj if adj[v]}
        paths = []
        while todo:
            root = min(todo)
            seen, queue = {root}, [root]
            for v in queue:
                for u in adj[v]:
                    if u not in seen:
                        seen.add(u)
                        queue.append(u)
            todo -= seen
            ends = tuple(sorted(v - 5 for v in seen if v >= 5))
            assert len(ends) == 2  # all components are paths
            paths.append(ends)
        result.append(tuple(sorted(paths)))
    return result


def dihedral_class(order):
    return min(tuple(order[(offset + sign * i) % 5] for i in range(5))
               for offset in range(5) for sign in (1, -1))


def report():
    states = full_colorings()
    original_systems = [systems(s) for s in states]
    records = []
    for order in permutations(range(5)):
        position = {vertex: i for i, vertex in enumerate(order)}
        words = [tuple(s[vertex] for vertex in order) for s in states]
        support = set()
        for word in words:
            boundary = [0]
            for color in word[:-1]:
                boundary.append(boundary[-1] ^ color)
            assert boundary[-1] ^ word[-1] == 0
            support.add(ck.normalize(boundary))
        mask = sum(1 << ck.patterns(5).index(b) for b in support)
        crossings = []
        for si, ss in enumerate(original_systems):
            for pi, paths in enumerate(ss):
                translated = [tuple(sorted(position[v] for v in path)) for path in paths]
                for (a, b), (c, d) in combinations(translated, 2):
                    if a < c < b < d or c < a < d < b:
                        crossings.append(dict(state=si, pair=PAIRS[pi],
                                              paths=translated, edge_colors=states[si]))
        # For a cycle with one terminal leaf at every vertex, a disk drawing
        # must have all leaves on the same side in the cycle's own order.
        # Conversely, drawing concentric pentagons realizes each such order.
        disk_order = all((order[(i + 1) % 5] - order[i]) % 5 == 1 for i in range(5)) or all(
            (order[(i + 1) % 5] - order[i]) % 5 == 4 for i in range(5))
        records.append(dict(port_order=order, dihedral_class=dihedral_class(order),
                            support_mask=mask, disk_order=disk_order,
                            all_state_systems_noncrossing=not crossings,
                            crossing_systems=len(crossings),
                            first_crossing=crossings[0] if crossings else None))
    good = [r for r in records if r['all_state_systems_noncrossing']]
    planar = [r for r in records if r['disk_order']]
    ghost = [r for r in good if not r['disk_order']]
    assert len(records) == 120 and len(planar) == 10 and len(good) == 20 and len(ghost) == 10
    assert {r['support_mask'] for r in planar} == {91}
    assert {r['support_mask'] for r in ghost} == {932}
    assert len({r['dihedral_class'] for r in records}) == 12
    assert all(ck.failure(r['support_mask'], ck.obligations(5)) is not None
               for r in records if not r['all_state_systems_noncrossing'])
    groups = []
    for key in sorted({r['dihedral_class'] for r in records}):
        members = [r for r in records if r['dihedral_class'] == key]
        assert len(members) == 10
        representative = next(r for r in members if r['port_order'] == key)
        groups.append(representative | dict(labeled_orders=len(members)))
    return dict(scope='All terminal orders on one fixed cycle pole; no general disk classification.',
                edges=EDGES, complete_edge_colorings=states,
                summary=dict(colorings=len(states), labeled_port_orders=len(records),
                             dihedral_classes=len(groups), state_system_checks=120 * 30 * 3,
                             noncrossing_orders=len(good), genuine_disk_orders=len(planar),
                             non_disk_noncrossing_orders=len(ghost),
                             disk_support_mask=91, non_disk_noncrossing_mask=932,
                             crossing_order_negative_controls=120 - len(good)),
                classes=groups, orders=records,
                sources={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                         for p in (Path(__file__), ROOT / 'scripts/ck_kempe_obstruction.py')})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert args.check.read_text() == payload, 'Port-order certificate differs from exact replay'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
