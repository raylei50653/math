#!/usr/bin/env python3
"""Independent literal cap review of D; imports neither D nor old models."""
from pathlib import Path
from itertools import product
import hashlib
import json

D = Path(__file__).resolve().parent
F = D.parent / 'frozen'
CERT = D.parent / 'D/certificate.json'
PATCH = F / 'audits/2026-10-19-r6-941-existence-f13eb4d/C/certificate.json'
CAT = F / 'audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json'
ROWS = ('01012', '01021', '01023', '01201', '01202', '01203', '01212', '01213', '01231', '01232')


def canonical(t):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in t)


def states(n, prefix=(0,)):
    if len(prefix) == n:
        if proper(prefix):
            yield prefix
        return
    for c in range(min(3, max(prefix) + 1) + 1):
        if c != prefix[-1]:
            yield from states(n, prefix + (c,))


def proper(t):
    return all(t[i] != t[(i + 1) % len(t)] for i in range(len(t)))


def mask(v):
    return sum(1 << i for i, a in enumerate(v) if a)


six, eight, ten = [list(states(n)) for n in (6, 8, 10)]
i6, i8, i10 = [{t: i for i, t in enumerate(ss)} for ss in (six, eight, ten)]
assert (len(eight), len(ten)) == (274, 2461)
patch = json.loads(PATCH.read_text())
assert patch['rim_states'] == list(map(list, six))
assert len(patch['candidates']) == 1552
signatures = {}
for op in patch['candidates']:
    n = 6 + op['internal']
    edges = op['edges']
    eq = op['equality_mask']
    blocks = [{i} for i in range(n)]
    for j, (a, b) in enumerate(edges):
        if not eq >> j & 1:
            continue
        first = next(s for s in blocks if a in s)
        second = next(s for s in blocks if b in s)
        if first is not second:
            first.update(second)
            blocks.remove(second)
    unequal = [(i, (i + 1) % 6) for i in range(6)] + [edge for j, edge in enumerate(edges) if not eq >> j & 1]
    assert all(not any(a in block and b in block for block in blocks) for a, b in unequal)
    assert op['completed_k_delta'] == -2 + op['internal'] - (n - len(blocks)) < 0
    lifts = []
    for s in six:
        allowed = []
        for c in range(4) if op['internal'] else (None,):
            u = s + (c,) if op['internal'] else s
            if all((u[a] == u[b]) == bool(eq >> j & 1) for j, (a, b) in enumerate(edges)):
                allowed.append(c)
        lifts.append(allowed)
    assert lifts == op['lifts']
    signature = tuple(map(len, lifts))
    sid = op['signature_id']
    assert sid not in signatures or signatures[sid] == signature
    signatures[sid] = signature
assert len(signatures) == len(set(signatures.values())) == 90
catalogue = set(map(int, json.loads(CAT.read_text())['cells']))
cert = json.loads(CERT.read_text())
summaries = []
for rec in cert['records']:
    z = rec['core_counts']
    exterior = []
    for a, n, R, L, q, c, x, y in eight:
        count = 0
        for s, v, w, t, r in product(range(4), repeat=5):
            core = (a, n, R, L, q, c, s, v, w, t)
            if proper(core) and x not in (s, r) and y not in (t, r) and r not in (s, v, w, t):
                count += z[i10[canonical(core)]]
        exterior.append(count)
    counts = {g: [0] * 10 for g in ('G', 'Q1', 'Q2', 'GB', 'J1', 'J2')}
    rim_weights = [[0] * len(six) for _ in ROWS]
    for j, row in enumerate(ROWS):
        x, y, a, b, c = map(int, row)
        for n, R, L, q in product(range(4), repeat=4):
            e = (a, n, R, L, q, c, x, y)
            if not proper(e) or b in (a, c, q):
                continue
            weight = exterior[i8[canonical(e)]]
            counts['G'][j] += weight * sum(
                p not in (a, b, q, n, h) and h not in (p, q, L, R, n)
                for p, h in product(range(4), repeat=2))
            counts['Q1'][j] += weight * (b == n and R == q)
            counts['Q2'][j] += weight * (b == n == L)
            counts['GB'][j] += weight * (b not in (n, R, L))
            counts['J1'][j] += weight * (b == L and a != R)
            counts['J2'][j] += weight * (a != L and a != R and b != L)
            rim_weights[j][i6[canonical((a, b, q, L, R, n))]] += weight
    for sid, sig in signatures.items():
        counts['P' + str(sid)] = [sum(a * b for a, b in zip(row, sig)) for row in rim_weights]
    assert counts == rec['graph_counts']
    assert {g: mask(v) for g, v in counts.items()} == rec['masks']
    assert all(mask(v) in catalogue for g, v in counts.items() if g != 'G')
    U = []
    for row in ROWS:
        a, s, v, w, t = map(int, row)
        value = 0
        for n, R, L, q in product(range(4), repeat=4):
            core = (a, n, R, L, q, a, s, v, w, t)
            if proper(core):
                value += z[i10[canonical(core)]] * sum(
                    p not in (a, q, n, h) and h not in (p, q, L, R, n)
                    for p, h in product(range(4), repeat=2))
        U.append(value)
    assert mask(U) == 319
    da_db = []
    for h, n in ((0, 1), (1, 2)):
        ids = set()
        for R, L, v, w in product(range(4), repeat=4):
            core = (0, n, R, L, 2, 0, 1, v, w, 1)
            if not proper(core) or 0 in (1, v, w) or h in (3, 2, L, R, n):
                continue
            ids.add(i10[canonical(core)])
        da_db.append(sum(z[i] for i in ids))
    assert all(da_db)
    summaries.append({'branch': rec['branch'], 'J1_counts': counts['J1'],
                      'J2_counts': counts['J2'], 'U_counts': U, 'da_db': da_db,
                      'distinct_patch_masks': sorted({mask(counts['P' + str(i)]) for i in range(90)})})
print(json.dumps({'status': 'PASS', 'patch_operations': 1552, 'patch_count_signatures': 90,
                  'records': summaries, 'source_realized': False,
                  'D_certificate_sha256': hashlib.sha256(CERT.read_bytes()).hexdigest()}, sort_keys=True))
