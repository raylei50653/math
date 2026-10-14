#!/usr/bin/env python3
"""Independent brute-force replay; imports no producer code."""
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
certificate = json.loads((ROOT / 'controls/fibres.json').read_text())
qrows = ((0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 2, 1), (0, 1, 2, 3))
names = ('ABAB', 'ABAC', 'ABCB', 'ABCD')
total = 0


def reachable(edges, coloring, start, pair):
    reached = {start}
    while True:
        larger = reached | {v for edge in edges if reached.intersection(edge)
                            and all(coloring[w] in pair for w in edge) for v in edge}
        if larger == reached:
            return reached
        reached = larger


def switched(edges, coloring, start, pair):
    selected = reachable(edges, coloring, start, pair)
    return tuple(pair[0] + pair[1] - c if v in selected else c
                 for v, c in enumerate(coloring))


for record in certificate['records']:
    edges = record['edges']
    n = 1 + max(v for edge in edges for v in edge)
    assert {v for edge in edges for v in edge} == set(range(n))
    assert reachable(edges, (0,) * n, 0, (0, 1)) == set(range(n))
    assert {tuple(e) for e in edges if max(e) < 4} == {(0, 1), (1, 2), (2, 3), (0, 3)}
    fibres = []
    for word, q in zip(names, qrows):
        brute = {q + tail for tail in itertools.product(range(4), repeat=n - 4)
                 if all((q + tail)[a] != (q + tail)[b] for a, b in edges)}
        saved = {tuple(row) for row in record['fibres'][word]}
        assert brute == saved, (record['name'], word)
        total += len(brute)
        fibres.append(brute)
    separate = {f for f in fibres[2] if 0 not in reachable(edges, f, 2, (0, 2))}
    connected = fibres[2] - separate
    assert {switched(edges, f, 2, (0, 2)) for f in fibres[0]} == separate
    assert {switched(edges, f, 3, (1, 3)) for f in fibres[3]} == connected
    assert {switched(edges, f, 2, (0, 2)) for f in separate} == fibres[0]
    assert {switched(edges, f, 3, (1, 3)) for f in connected} == fibres[3]
    if record['pq']:
        p, q = record['pq']
        assert p >= 4 and q >= 4
        assert {0, p, q} in [set(f) for f in record['oriented_faces'] if len(f) == 3]

# Direct raw-colour local r table, without the producer's canonical relabelling.
smaller_rows = []
for z, s, v, t in qrows:
    good = []
    for p, q in itertools.permutations((1, 2, 3), 2):
        okay = True
        for r in set(range(4)) - {s, v, t}:
            if z == r and s != t:
                okay = False
            elif z == r and s == t:
                okay &= {p, q} == set(range(4)) - {z, s}
            elif s != t:
                okay &= {p, q} == {s, t}
            else:
                missing, = set(range(4)) - {z, s, r}
                okay &= missing in {p, q}
        if okay:
            good.append((p, q))
    smaller_rows.append(good)
assert smaller_rows == [[(2, 3), (3, 2)], [(1, 2), (2, 1)],
                        [(2, 3), (3, 2)], []]
assert total == certificate['complete_fixed_Q_colorings'] == 42
print(json.dumps({'status': 'PASS', 'independent_bruteforce_graphs': 7,
                  'complete_fixed_Q_colorings': total, 'full_set_bijections': 14,
                  'r_degree5_joint_table': 'PASS', 'actual_target_sources': 0}))
