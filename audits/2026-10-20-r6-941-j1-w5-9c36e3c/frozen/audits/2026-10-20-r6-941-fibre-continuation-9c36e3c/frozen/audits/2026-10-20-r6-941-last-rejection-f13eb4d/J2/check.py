#!/usr/bin/env python3
"""Exact same-source J2 rejection normal forms; no realization inference."""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
FROZEN = AUDIT / 'frozen'
MODEL = 'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
PREVIOUS = 'audits/2026-10-19-r6-941-existence-f13eb4d/C/comparisons.json'
NAMES = ('a', 'n', 'R', 'L', 'q', 'c', 's', 'v', 'w', 't')
PAIRS = ((0, 1), (0, 2), (0, 3))


def calculate():
    manifest = {r['path']: r for r in json.loads((AUDIT / 'INPUTS.json').read_text())}
    hashes = {}
    for name in (MODEL, PREVIOUS):
        raw = (FROZEN / name).read_bytes()
        hashes[name] = hashlib.sha256(raw).hexdigest()
        expected = manifest[name]
        assert hashes[name] == expected['sha256']
        assert len(raw) == expected['bytes']
    spec = importlib.util.spec_from_file_location('frozen_j2_model', FROZEN / MODEL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    I = m.interfaces()
    K = m.kempe(10, I['ten'])
    ix8 = {t: i for i, t in enumerate(I['eight'])}
    ix10 = {t: i for i, t in enumerate(I['ten'])}
    # All ten literal fibres and every original p,h lift, including empties.
    records = []
    matrix8 = [[0] * len(I['eight']) for _ in m.ROWS]
    for j, row in enumerate(m.ROWS):
        x, y, a, b, c = map(int, row)
        for n, R, L, q in product(range(4), repeat=4):
            e = (a, n, R, L, q, c, x, y)
            proper = m.proper(e) and b not in (a, c, q)
            lifts = [(p, h) for p, h in product(range(4), repeat=2)
                     if proper and p not in (a, b, q, n, h)
                     and h not in (p, q, L, R, n)]
            good = proper and a != L and a != R and b != L
            ei = ix8[m.canonical(e)] if m.proper(e) else -1
            if good:
                matrix8[j][ei] += 1
            records.append([j, n, R, L, q, ei, proper, good, lifts])
    matrix10 = [[0] * len(I['ten']) for _ in m.ROWS]
    for j, row in enumerate(matrix8):
        for e, value in enumerate(row):
            for i, weight in I['T'][e]:
                matrix10[j][i] += value * weight
    old = json.loads((FROZEN / PREVIOUS).read_text())
    assert old['matrices']['J2'] == {'E': matrix8, 'F': matrix10}
    zero = {i for i in range(len(I['ten']))
            if any(I['C']['G'][j][i] for j in (1, 4, 6))
            or I['C']['Q2'][9][i]
            or any(matrix10[j][i] for j in range(10) if not (943 >> j) & 1)}
    live, rounds = m.close(K, set(range(len(I['ten']))) - zero)
    old_live = next(r['live'] for r in old['records'][1]['survivors']
                    if r['mask'] == 943)
    assert live == old_live
    live_set = set(live)

    # Independent literal enumeration of the entire T fibre cap.
    literal_lifts = [[] for _ in I['ten']]
    for n, R, L, q, s, v, w, t in product(range(4), repeat=8):
        u = (0, n, R, L, q, 1, s, v, w, t)
        if not m.proper(u) or q in (1, 2) or L in (0, 2) or R == 0:
            continue
        for r in range(4):
            if s == 0 or t == 1 or r in (s, v, w, t, 0, 1):
                continue
            literal_lifts[ix10[m.canonical(u)]].append([list(u), r])
    assert list(map(len, literal_lifts)) == matrix10[1]
    selected = [i for i in live if literal_lifts[i]]
    assert len(selected) == 12
    assert all(len(literal_lifts[i]) == 1 for i in selected)
    expected = set()
    for R, L, q in ((3, 1, 3), (2, 1, 3), (2, 3, 0)):
        for d in (2, 3):
            for v, w in ((0, 1), (1, 0)):
                expected.add(((0, 1, R, L, q, 1, d, v, w, d), 5 - d))
    assert {(tuple(literal_lifts[i][0][0]), literal_lifts[i][0][1])
            for i in selected} == expected
    # They are complete F fibres, with no original left-cap extension at all.
    assert all(not I['core_caps'][i]['left'] for i in selected)

    # Enumerate actual-partition necessary conditions directly, not the old
    # deduplicated column representatives, so every full boundary block is kept.
    parts = [p for p in m.growth(10) if m.noncrossing(p)
             and sum(p[i] != p[(i + 1) % 10] for i in range(10)) == 2 * max(p)]
    forms = []
    for i in selected:
        u, r = literal_lifts[i][0]
        pair_records = []
        for pair in PAIRS:
            other = tuple(c for c in range(4) if c not in pair)
            swap = {pair[0]: pair[1], pair[1]: pair[0],
                    other[0]: other[1], other[1]: other[0]}
            admissible = []
            for p in parts:
                if any((u[j] in pair) != (u[k] in pair)
                       for j in range(10) for k in range(j) if p[j] == p[k]):
                    continue
                if any((u[j] in pair) == (u[(j + 1) % 10] in pair)
                       and p[j] != p[(j + 1) % 10] for j in range(10)):
                    continue
                orbit = [ix10[m.canonical(tuple(
                    swap[u[j]] if mask >> p[j] & 1 else u[j]
                    for j in range(10)))] for mask in range(1 << (max(p) + 1))]
                if any(k not in live_set for k in orbit):
                    continue
                blocks = [[NAMES[j] for j in range(10) if p[j] == k]
                          for k in range(max(p) + 1)]
                admissible.append({'partition': p, 'blocks': blocks,
                                   'orbit_indices_with_multiplicity': orbit})
            assert admissible
            pair_records.append({'pair': pair, 'complement': other,
                                 'partitions': admissible})
        triple = tuple(u[k] for k in (2, 3, 4))
        family = ((3, 1, 3), (2, 1, 3), (2, 3, 0)).index(triple) + 1
        if family == 2:
            assert len(pair_records[2]['partitions']) == 1
        if family == 3:
            assert len(pair_records[1]['partitions']) == 1
        forms.append({'core_index': i, 'canonical_core': I['ten'][i],
                      'literal_core': u, 'r': r, 'family': family,
                      'original_left_lifts': I['core_caps'][i]['left'],
                      'pair_records': pair_records})
    return {
        'source_realized': False,
        'status': 'J2 rejection remains OPEN; exact necessary fibre normal forms',
        'input_sha256': hashes,
        'boundary': ['x', 'y', 'a', 'b', 'c'], 'rows': m.ROWS,
        'core_boundary': NAMES,
        'fixed_assumptions': ['full frozen r6/941 original source', 'a2=0', 'M(J2)=943'],
        'E_records': records, 'J2_matrices': {'E': matrix8, 'F': matrix10},
        'all_T_literal_lifts_including_empties': literal_lifts,
        'zero_seed': sorted(zero), 'zero_closure_rounds': rounds, 'live': live,
        'forms': forms,
        'T_functional': [[i, 1] for i in selected],
        'partitions_total': sum(len(p['partitions']) for f in forms for p in f['pair_records']),
        'family_pair_partition_counts': {
            str(family): sorted({tuple(len(p['partitions']) for p in f['pair_records'])
                                for f in forms if f['family'] == family})
            for family in (1, 2, 3)},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = ap.parse_args()
    result = json.loads(json.dumps(calculate()))
    if args.build:
        with args.certificate.open('x') as f:
            json.dump(result, f, separators=(',', ':'))
            f.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == result
    print(json.dumps({k: result[k] for k in (
        'status', 'T_functional', 'partitions_total',
        'family_pair_partition_counts')}, sort_keys=True))


if __name__ == '__main__':
    main()
