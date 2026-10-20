#!/usr/bin/env python3
"""Independent literal partition enumeration for the sibling J1 certificate."""
from pathlib import Path
from itertools import product
import hashlib
import importlib.util
import json

D = Path(__file__).resolve().parent
P = D.parent / 'J1/certificate.json'
C = json.loads(P.read_text())
model = D.parent / 'frozen/audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
spec = importlib.util.spec_from_file_location('j1_review_frozen_model', model)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
states = [t for t in m.growth(10, four=True) if m.proper(t)]
index = {t: i for i, t in enumerate(states)}
live = set(C['final_live'])
parts = [p for p in m.growth(10) if m.noncrossing(p)
         and sum(p[i] != p[(i + 1) % 10] for i in range(10)) == 2 * max(p)]
names = ('a', 'n', 'R', 'L', 'q', 'c', 's', 'v', 'w', 't')
literal = []
for n, R, L, q, s, v, w, t in product(range(4), repeat=8):
    u = (0, n, R, L, q, 1, s, v, w, t)
    if not m.proper(u) or q in (1, 2) or L != 2 or R == 0:
        continue
    for r in range(4):
        if s == 0 or t == 1 or r in (s, v, w, t, 0, 1):
            continue
        i = index[m.canonical(u)]
        if i in live:
            literal.append((u, r, i))
assert set(literal) == {(tuple(t['core']), t['r'], t['core_id'])
                        for t in C['eight_surviving_literal_fibres']}
assert len(literal) == 8
partition_count = 0
for target in C['component_records']:
    u = tuple(target['core'])
    for rec in target['splits']:
        sep = rec['color_map']
        reverse = {x: i for i, x in enumerate(sep)}
        pp = []
        for p in parts:
            if any(sep[u[j]] // 2 != sep[u[k]] // 2
                   for j in range(10) for k in range(j) if p[j] == p[k]):
                continue
            if any(sep[u[j]] // 2 == sep[u[(j + 1) % 10]] // 2
                   and p[j] != p[(j + 1) % 10] for j in range(10)):
                continue
            orbit = [index[m.canonical(tuple(
                reverse[sep[u[j]] ^ 1] if mask >> p[j] & 1 else u[j]
                for j in range(10)))] for mask in range(1 << (max(p) + 1))]
            if all(i in live for i in orbit):
                pp.append(p)
        assert set(pp) == set(map(tuple, rec['partitions']))
        together = [[names[j], names[k]] for j in range(10) for k in range(j + 1, 10)
                    if all(p[j] == p[k] for p in pp)]
        apart = [[names[j], names[k]] for j in range(10) for k in range(j + 1, 10)
                 if sep[u[j]] // 2 == sep[u[k]] // 2
                 and all(p[j] != p[k] for p in pp)]
        assert together == rec['forced_together']
        assert apart == rec['forced_apart']
        partition_count += len(pp)
print(json.dumps({'status': 'PASS', 'literal_fibres': len(literal),
                  'independently_enumerated_partitions': partition_count,
                  'certificate_sha256': hashlib.sha256(P.read_bytes()).hexdigest()},
                 sort_keys=True))
