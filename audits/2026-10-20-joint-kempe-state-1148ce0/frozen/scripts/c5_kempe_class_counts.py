#!/usr/bin/env python3
"""Kempe-class chord identities: exact boundary certificates and fixed-witness replay.

python3 scripts/c5_kempe_class_counts.py [--check]
No new graph search. Graph-to-orbit topology and class decomposition are paper
arguments, not Lean proofs. Never apply the exterior/4CT screen to one class.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_adjacent_singleton_counts import (
    CAT, CHORDS, CYCLE, FOUR, INDEX, LABELED, PAIRS, REPS, THREE,
    chord_totals, identity, normalize, orbit_options,
)

from c5_kempe_screen import failure, obligations

ROOT = Path(__file__).resolve().parents[1]
COUNTS = ROOT / 'artifacts/c5_cells/adjacent_singleton_counts.json'
OUT = ROOT / 'artifacts/c5_cells/kempe_class_counts.json'
# y_3 - x_02 - y_2 + x_03. Rotation supplies all chord-total equalities.
FUNCTIONAL = (((0, 2, 0, 1, 2), 1), ((0, 2, 0, 1, 3), -1),
              ((0, 2, 1, 0, 2), -1), ((0, 2, 1, 0, 3), 1))


def classes(k, edges):
    """Enumerate all proper colorings modulo global S4, then actual Kempe moves.

    Every proper C5 uses >=3 colors, so its S4 action is free. Each full-coloring
    orbit contributes exactly one extension to its canonical boundary assignment.
    """
    n = k + 5
    edges = sorted(set(tuple(sorted(e)) for e in (*CYCLE, *edges)))
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    colors = set()
    order = sorted(range(5, n), key=lambda v: (-len(adj[v]), v))
    for b in REPS:
        c = list(b) + [-1] * k
        if any(c[u] == c[v] for u, v in edges if v < 5):
            continue

        def extend(depth):
            if depth == k:
                colors.add(tuple(c))
                return
            v = order[depth]
            forbidden = {c[u] for u in adj[v]}
            for color in range(4):
                if color not in forbidden:
                    c[v] = color
                    extend(depth + 1)
            c[v] = -1

        extend(0)
    assert all(normalize(c) == c for c in colors)
    pending = set(colors)
    result = []
    while pending:
        start = min(pending)
        pending.remove(start)
        queue = [start]
        for c in queue:
            for pair in combinations(range(4), 2):
                unseen = {i for i in range(n) if c[i] in pair}
                while unseen:
                    root = min(unseen)
                    unseen.remove(root)
                    component = [root]
                    for u in component:
                        for v in sorted(adj[u] & unseen):
                            unseen.remove(v)
                            component.append(v)
                    swapped = list(c)
                    for u in component:
                        swapped[u] = pair[0] + pair[1] - c[u]
                    target = normalize(swapped)
                    assert target in colors
                    if target in pending:
                        pending.remove(target)
                        queue.append(target)
        counts = Counter(INDEX[c[:5]] for c in queue)
        vec = [counts[j] for j in range(10)]
        result.append(dict(representative=start, size=len(queue), counts=vec,
                           chord_totals=chord_totals(vec)))
    return result


def report():
    options = orbit_options(PAIRS[0])
    certificates = []
    for rotation in range(5):
        weights = {tuple(b[(i + rotation) % 5] for i in range(5)): w
                   for b, w in FUNCTIONAL}
        residuals = [sum(weights.get(LABELED[i], 0) for i in op['boundaries'])
                     for op in options]
        assert not any(residuals)
        coefficients = [sum(w for b, w in weights.items() if INDEX[normalize(b)] == j)
                        for j in range(10)]
        left = tuple(sorted(((0-rotation) % 5, (3-rotation) % 5)))
        right = tuple(sorted(((0-rotation) % 5, (2-rotation) % 5)))
        expected = [0] * 10
        for e, sign in ((left, 1), (right, -1)):
            expected[FOUR[e]] += sign
            for i in e:
                expected[THREE[i]] += sign
        assert coefficients == expected
        certificates.append(dict(rotation=rotation, functional=[(b, w) for b, w in weights.items()],
                                 left_chord=left, right_chord=right, coefficients=coefficients,
                                 orbit_residuals=residuals))
    # The five equality pairs connect all five chords.
    reached = {CHORDS[0]}
    for _ in range(5):
        for cert in certificates:
            a, b = cert['left_chord'], cert['right_chord']
            if a in reached or b in reached:
                reached.update((a, b))
    assert reached == set(CHORDS)
    table = obligations()
    four_mask = sum(1 << j for j in FOUR.values())
    support_replay = []
    for e in CHORDS:
        allowed = four_mask | sum(1 << THREE[i] for i in e)
        masks = [mask for mask in range(1, 1024)
                 if not mask & ~allowed and mask >> FOUR[e] & 1
                 and failure(mask, table) is None]
        assert len(masks) == 4 and all(mask & four_mask == four_mask for mask in masks)
        support_replay.append(dict(chord=e, class_support_candidates=masks))
    catalog = json.loads(CAT.read_text())
    known_counts = {r['mask']: r['counts'] for r in json.loads(COUNTS.read_text())['catalogue_witnesses']}
    replay = []
    for mask, entry in sorted(catalog['cells'].items(), key=lambda p: int(p[0])):
        cs = classes(entry['k_eff'], entry['edges'])
        assert all(identity(c['counts']) for c in cs)
        total = [sum(c['counts'][j] for c in cs) for j in range(10)]
        assert sum(1 << j for j, v in enumerate(total) if v) == int(mask)
        assert total == known_counts[int(mask)]
        # This is classwise algebra only; independent support is a hypothesis.
        for c in cs:
            p = [i for i in range(5) if c['counts'][THREE[i]]]
            for e in CHORDS:
                if set(p) <= set(e) and c['counts'][FOUR[e]] > 0:
                    assert all(c['counts'][j] > 0 for j in FOUR.values())
        replay.append(dict(mask=int(mask), classes=cs))
    # Icosahedron in triangle (0,1,4); expose C5 by a path 1-2-3-4 outside.
    # Fixed positive control for a disconnected Kempe space, not a graph search.
    multi_edges = [(0,1),(0,4),(0,8),(0,10),(0,13),(1,4),(1,5),(1,10),
                   (1,11),(4,5),(4,8),(4,9),(5,6),(5,9),(5,11),(6,7),
                   (6,9),(6,11),(6,12),(7,8),(7,9),(7,12),(7,13),
                   (8,9),(8,13),(10,11),(10,12),(10,13),(11,12),(12,13)]
    multiple = classes(9, multi_edges)
    assert len(multiple) == 10
    assert all(c['size'] == 7 and identity(c['counts']) for c in multiple)
    crossing = classes(0, [(0, 2), (1, 3)])
    assert any(not identity(c['counts']) for c in crossing)
    # A missing term must fail the local certificate, catching a vacuous check.
    broken = dict(FUNCTIONAL[:-1])
    assert any(sum(broken.get(LABELED[i], 0) for i in op['boundaries']) for op in options)
    files = [CAT, COUNTS, Path(__file__), ROOT / 'scripts/c5_adjacent_singleton_counts.py',
             ROOT / 'scripts/c5_kempe_screen.py']
    return dict(trust='Exact finite certificates and witness replay; arbitrary disk/class soundness is a paper proof, not Lean. No graph realizability or exterior condition for individual classes.',
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
                pattern_order=REPS, split=PAIRS[0], orbit_options=options,
                certificates=certificates, support_replay=support_replay, witness_replay=replay,
                controls=dict(crossing_chords=crossing, missing_term_detected=True,
                              multiple_classes=dict(k=9, edges=multi_edges, classes=multiple)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate differs; inspect before regeneration.'
    else:
        OUT.write_text(encoded)
    rows = result['witness_replay']
    print(json.dumps(dict(witnesses=len(rows), classes=sum(len(r['classes']) for r in rows),
                          multiple_class_witnesses=sum(len(r['classes']) > 1 for r in rows),
                          local_equalities=len(result['certificates']) * len(result['orbit_options']),
                          control_classes=len(result['controls']['multiple_classes']['classes'])),
                     sort_keys=True))


if __name__ == '__main__':
    main()
