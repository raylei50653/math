#!/usr/bin/env python3
"""Independent boundary-component algebra for the actual-E transport proof.

No exterior graph is enumerated or inferred from a partition. Every actual
complete E colouring induces one of these necessary noncrossing partitions.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIN = ('a', 'n', 'R', 'L', 'q', 'c', 'x', 'y')
POS = {v: i for i, v in enumerate(PIN)}
COL = range(4)


def canonical(t):
    names = {}
    return ''.join(str(names.setdefault(v, len(names))) for v in t)


def partitions(prefix=(0,)):
    if len(prefix) == 8:
        yield prefix
    else:
        for label in range(max(prefix) + 2):
            yield from partitions(prefix + (label,))


def noncrossing(p):
    return not any(p[a] == p[c] and p[b] == p[d] and p[a] != p[b]
                   for a, b, c, d in itertools.combinations(range(8), 4))


NC = tuple(p for p in partitions() if noncrossing(p))
assert len(NC) == 1430


def compatible(t, palettes, crossing=False):
    side = {v: j for j, pair in enumerate(palettes) for v in pair}
    family = partitions() if crossing else NC
    for p in family:
        if any(p[i] == p[j] and side[t[i]] != side[t[j]]
               for i in range(8) for j in range(i)):
            continue
        if any(side[t[i]] == side[t[(i+1) % 8]] and p[i] != p[(i+1) % 8]
               for i in range(8)):
            continue
        yield p


def same(p, u, v):
    return p[POS[u]] == p[POS[v]]


def flip(t, p, vertex, pair):
    label = p[POS[vertex]]
    swap = dict(zip(pair, reversed(pair)))
    return tuple(swap[v] if p[i] == label else v for i, v in enumerate(t))


def lifts(t):
    a, n, r, l, q, c, x, y = t
    out = []
    for b, p, h in itertools.product(COL, repeat=3):
        if b in {a, c, q} or p in {a, b, q, h, n} or h in {p, q, l, r, n}:
            continue
        out.append({'bph': [b, p, h], 'literal_row': [x, y, a, b, c],
                    'canonical_row': canonical((x, y, a, b, c))})
    return out


def has_lift(t, bph, row):
    return any(z['bph'] == list(bph) and z['canonical_row'] == row for z in lifts(t))


def tau_first(qtype, p, crossing=False):
    t = (0, 2, 3, 0, 3, 1, 0, 1) if qtype == 1 else (0, 2, 0, 2, 3, 1, 0, 1)
    if same(p, 'n', 'q'):
        z = 'L' if qtype == 1 else 'R'
        changed = flip(t, p, z, (0, 1))
        assert has_lift(changed, (2, 1, 0), '01021'), ('tau_first', qtype, p, changed)
        return 'old_tau', changed
    changed = flip(t, p, 'q', (2, 3))
    expected = (0, 2, 3, 0, 2, 1, 0, 1) if qtype == 1 else (0, 2, 0, 3, 2, 1, 0, 1)
    assert changed == expected
    assert flip(changed, p, 'q', (2, 3)) == t
    return 'intermediate', changed


def tau_second(qtype, t, p):
    z = 'R' if qtype == 1 else 'L'
    if same(p, z, 'y'):
        changed = flip(t, p, 'a', (0, 2))
        assert has_lift(changed, (0, 3, 1), '01201'), ('tau_second_y', qtype, p, changed)
        assert flip(changed, p, 'a', (0, 2)) == t
        return 'beta', changed
    if same(p, z, 'c'):
        changed = flip(t, p, 'q', (0, 2))
        assert has_lift(changed, (2, 3, 1), '01021'), ('tau_second_c', qtype, p, changed)
        return 'old_tau_c', changed
    changed = flip(t, p, z, (1, 3))
    assert has_lift(changed, (3, 1, 3), '01021'), ('tau_second_free', qtype, p, changed)
    return 'old_tau_free', changed


def tau_records():
    result = []
    for qtype in (1, 2):
        t = (0, 2, 3, 0, 3, 1, 0, 1) if qtype == 1 else (0, 2, 0, 2, 3, 1, 0, 1)
        first = []
        for p in compatible(t, ((0, 1), (2, 3))):
            branch, changed = tau_first(qtype, p)
            first.append({'partition': p, 'branch': branch, 'changed': changed,
                          'all_old_lifts': lifts(changed)})
        u = (0, 2, 3, 0, 2, 1, 0, 1) if qtype == 1 else (0, 2, 0, 3, 2, 1, 0, 1)
        second = []
        for p in compatible(u, ((0, 2), (1, 3))):
            branch, changed = tau_second(qtype, u, p)
            second.append({'partition': p, 'branch': branch, 'changed': changed,
                           'all_old_lifts': lifts(changed)})
        result.append({'candidate': f'Q{qtype}', 'initial': t, 'all_initial_old_lifts': lifts(t),
                       'first': first, 'second': second})
    return result


def rho_records():
    records = []
    for b, q, qtype in itertools.product((0, 1), (0, 1, 3), (1, 2)):
        if q == b:
            continue
        delta = next(v for v in COL if v not in {2, b, q})
        t = (2, b, q, 2, q, 2, 0, 1) if qtype == 1 else (2, b, 2, b, q, 2, 0, 1)
        cases = []
        for p in compatible(t, ((b, q), (2, delta))):
            if same(p, 'n', 'q'):
                z = 'L' if qtype == 1 else 'R'
                changed = flip(t, p, z, (2, delta))
                target = '01202' if b == 0 else '01212'
                assert has_lift(changed, (b, delta, 2), target)
                branch = 'old_same_rho'
                normalized = changed
            else:
                changed = flip(t, p, 'q', (b, q))
                target = ('01212' if b == 0 else '01202') if q == 3 else '01232'
                assert has_lift(changed, (delta, q, delta), target)
                branch = 'old_other_rho' if q == 3 else 'old_alpha_h3'
                normalized = changed
                if q != 3:
                    swapped = changed[POS['x']] == 1
                    normalized = tuple(1-v if v in (0, 1) else v for v in changed) if swapped else changed
                    assert normalized[POS['x']] == 0 and normalized[POS['y']] == 1
                    assert has_lift(normalized, (3, 1-normalized[POS['q']], 3), '01232')
                    # This is the exact inverse palette decision, using only target and fixed source row.
                    reverse_swap = normalized[POS['n']] != b
                    assert reverse_swap == swapped
                    target_hits_anchor = same(p, 'q', 'x')
                    assert b == (normalized[POS['n']] ^ int(target_hits_anchor))
                    unnormalized = tuple(1-v if v in (0, 1) else v for v in normalized) if reverse_swap else normalized
                    assert flip(unnormalized, p, 'q', (0, 1)) == t
            cases.append({'partition': p, 'branch': branch, 'changed': changed,
                          'normalized': normalized, 'all_old_lifts': lifts(changed)})
        records.append({'candidate': f'Q{qtype}', 'row_b': b, 'q': q, 'initial': t,
                        'all_initial_old_lifts': lifts(t), 'cases': cases})
    # Images of the two candidate domains are disjoint for either fixed negative row.
    for b in (0, 1):
        images = []
        for qtype in (1, 2):
            images.append({tuple(c['normalized']) for r in records if r['row_b'] == b and r['candidate'] == f'Q{qtype}'
                           for c in r['cases'] if c['branch'] == 'old_alpha_h3'})
        assert images[0].isdisjoint(images[1])
    # Across different source rows, target component connectivity recovers the row.
    images_by_domain = []
    for b, qtype in itertools.product((0, 1), (1, 2)):
        images_by_domain.append({(tuple(c['normalized']), tuple(c['partition']))
                                 for r in records if r['row_b'] == b and r['candidate'] == f'Q{qtype}'
                                 for c in r['cases'] if c['branch'] == 'old_alpha_h3'})
    for first, second in itertools.combinations(images_by_domain, 2):
        assert first.isdisjoint(second)
    return records


def degree_four_identity():
    rows = []
    for q, l, r, b in itertools.product(COL, repeat=4):
        if q == l or l == r or r == b or b == q:
            continue
        hs = [h for h in COL if h not in (q, l, r, b)]
        assert len(hs) == int(q == r) + int(l == b)
        rows.append({'qlrb': [q, l, r, b], 'all_h': hs, 'Q1': q == r, 'Q2': l == b})
    return rows


def negative_controls():
    # Removing planarity invalidates the proposed transports: crossing components can trap both sides.
    hits = []
    for qtype in (1, 2):
        t = (0, 2, 3, 0, 3, 1, 0, 1) if qtype == 1 else (0, 2, 0, 2, 3, 1, 0, 1)
        for p in compatible(t, ((0, 1), (2, 3)), crossing=True):
            try:
                tau_first(qtype, p)
            except AssertionError:
                hits.append({'candidate': f'Q{qtype}', 'crossing_partition': p})
                break
    assert len(hits) == 2
    # The old-tau-empty premise is essential: the verified proper branches can end in old tau.
    tau = tau_records()
    old_tau = [x for r in tau for x in r['first'] if x['branch'] == 'old_tau']
    assert old_tau and all(x['all_old_lifts'] for x in old_tau)
    return {'dropping_planarity_breaks_transport': hits,
            'dropping_old_tau_empty_does_not_force_beta': old_tau[0],
            'erased_empty_lift_control': {'initial_tau_lift_sets_are_empty': all(not r['all_initial_old_lifts'] for r in tau)}}


def build():
    return {'scope': 'complete local lifts and necessary actual-E component partitions, not source realization',
            'pin_order': PIN, 'noncrossing_partition_count': len(NC), 'tau': tau_records(),
            'rho': rho_records(), 'degree_four': degree_four_identity(), 'negative_controls': negative_controls(),
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


parser = argparse.ArgumentParser()
parser.add_argument('--write', action='store_true')
args = parser.parse_args()
result = build()
path = ROOT/'certificate.json'
normalized = json.loads(json.dumps(result))
if args.write:
    with path.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
else:
    assert json.loads(path.read_text()) == normalized
print(json.dumps({'tau_first_cases': [len(r['first']) for r in result['tau']],
                  'tau_second_cases': [len(r['second']) for r in result['tau']],
                  'rho_cases': [len(r['cases']) for r in result['rho']],
                  'degree_four_rows': len(result['degree_four']),
                  'negative_controls': 'passed'}))
