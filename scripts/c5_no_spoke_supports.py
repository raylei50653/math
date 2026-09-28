#!/usr/bin/env python3
"""Necessary circular supports and target separation for no-spoke cores.

Arbitrary-size annulus ordering and completion coverage are paper proofs.
The finite forbidden-set options below are bounds on whole relations, never
independent endpoint marginals or assertions of source realizability.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

from c5_no_spoke_exterior import covers
from c5_single_spoke_completion import audit_completion, COMPLETION_SOURCE
from c5_single_spoke_cores import PI, Q, RHO, TARGETS, T4, U, PERMS, SUPPORTS, transport
from c5_single_spoke_root_conservation import local_audit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_no_spoke_supports/observations.json'
PARTS = ((2, 2, 1), (2, 1, 1, 1))


def circular_supports(r):
    """All ordered, disjoint positive spans in one boundary turn; C0 first."""
    result = {}
    for anchor in range(5):
        for tail in permutations(range(1, r)):
            order = (0,) + tail

            def visit(lifted, end):
                j = len(lifted)
                if j == r:
                    supports = [None] * r
                    lifts = [None] * r
                    for k, t in zip(order, lifted):
                        supports[k] = tuple(sorted(x % 5 for x in t))
                        lifts[k] = t
                    item = dict(order=order, lifts=tuple(lifts))
                    result.setdefault(tuple(supports), []).append(item)
                    return
                starts = (anchor,) if j == 0 else range(end, anchor + 5)
                for start in starts:
                    # Every remaining component needs at least one boundary edge.
                    for stop in range(start + 1, anchor + 6 - (r - j - 1)):
                        for mask in range(1 << (stop - start - 1)):
                            t = (start,) + tuple(x for x in range(start + 1, stop)
                                                if mask >> (x-start-1) & 1) + (stop,)
                            visit(lifted + (t,), stop)
            visit((), anchor)
    return result


def independent_arc_supports(r):
    """Independent exhaustive packing of cyclic hulls by boundary-edge masks."""
    arcs = []
    for support in SUPPORTS:
        if len(support) < 2:
            continue
        for start in support:
            length = max((i - start) % 5 for i in support)
            mask = sum(1 << ((start+j) % 5) for j in range(length))
            arcs.append((support, mask))
    result = set()

    def visit(supports, used):
        if len(supports) == r:
            result.add(supports)
            return
        for support, mask in arcs:
            if not used & mask:
                visit(supports + (support,), used | mask)
    visit((), 0)
    return result


def verify_placement(supports, placement):
    order, lifts = placement['order'], placement['lifts']
    assert sorted(order) == list(range(len(supports))) and order[0] == 0
    for s, t in zip(supports, lifts):
        assert tuple(sorted(x % 5 for x in t)) == s and len(set(t)) == len(t)
        assert 0 < max(t) - min(t) < 5
    assert all(max(lifts[a]) <= min(lifts[b]) for a, b in zip(order, order[1:]))
    assert max(lifts[order[-1]]) <= min(lifts[0]) + 5


def port_rotations(parts, placement):
    ports = [tuple(f'c{k}p{j}' for j in range(n)) for k, n in enumerate(parts)]
    result = [sum((choices[k] for k in placement['order']), ())
              for choices in product(*(tuple(permutations(p)) for p in ports))]
    assert all(len(word) == len(set(word)) == 5 for word in result)
    return result


@lru_cache(None)
def component_options(arity, support, ban, row):
    images, ps = transport(support, ban, row)
    assert len(images) <= 1
    if images:
        return dict(exact=True, permutation=ps[0], options=images)
    seen = {row[i] for i in support}
    absent_both = U - seen - {Q[i] for i in support}
    options = []
    for mask in range(16):
        f = frozenset(c for c in U if mask >> c & 1)
        if len(f) > arity:
            continue
        if not all({p[c] for c in f} == f for p in PERMS if all(p[c] == c for c in seen)):
            continue
        if arity == 1 and any((a == c) != (d == c)
                              for a in ban for d in f for c in absent_both):
            continue
        options.append(tuple(sorted(f)))
    return dict(exact=False, absent_both=sorted(absent_both), options=tuple(options))


def completion(supports, bans, k, target):
    reflected = target == 0
    ss = tuple(tuple(sorted(RHO[i] for i in s)) for s in supports) if reflected else supports
    f = tuple(sorted(PI[c] for c in bans[k])) if reflected else bans[k]
    if 0 in ss[k] or f not in ((0,), (3,)):
        return None
    routes = [(j, l) for j in range(len(ss)) for l in range(len(ss))
              if j != l and k not in (j, l) and 1 in ss[j] and 4 in ss[l]]
    if not routes:
        return None
    j, l = routes[0]
    return dict(reflected=reflected, frame_supports=ss, frame_ban=f,
                routes=[dict(component=j, contact=f'c{j}p0', boundary=1),
                        dict(component=l, contact=f'c{l}p0', boundary=4)],
                excluded=(2, 3) if reflected else (0, 3))


def row_evidence(parts, supports, bans, row, use_completion=False):
    entries, choices = [], []
    for k, (n, s, f) in enumerate(zip(parts, supports, bans)):
        item = dict(component=k, **component_options(n, s, f, row))
        if use_completion and n == 2:
            proof = completion(supports, bans, k, TARGETS.index(row))
            if proof:
                item['completion'] = proof
                item['options'] = tuple(x for x in item['options'] if not set(x) & set(proof['excluded']))
        assert item['options'], 'incompatible source constraints must be reported separately'
        entries.append(item)
        choices.append(item['options'])
    known = set().union(*(set(xs[0]) for xs in choices if len(xs) == 1))
    possible = set().union(*(set(f) for xs in choices for f in xs))
    covering = next((fs for fs in product(*choices) if set().union(*map(set, fs)) == U), None)
    status = 'reject' if known == U else 'unresolved' if covering is not None else 'accept'
    return dict(row=row, status=status, components=entries,
                guaranteed_z_colors=sorted(U - possible),
                necessary_cover_if_rejected=covering)


def reflect_supports(supports, bans):
    return (tuple(tuple(sorted(RHO[i] for i in s)) for s in supports),
            tuple(tuple(sorted(PI[c] for c in f)) for f in bans))


def reflection_audit(r, geometries):
    parts, supports, bans = r['parts'], r['supports'], r['bans']
    ss, fs = reflect_supports(supports, bans)
    assert reflect_supports(ss, fs) == (supports, bans)
    assert ss in geometries[len(parts)]
    # Reverse geometry, preserving the named tuple coordinates.
    for p in r['placements']:
        order = (0,) + tuple(reversed(p['order'][1:]))
        anchor = (3 - max(p['lifts'][0])) % 5
        lifts, end = [None] * len(parts), anchor
        for k in order:
            t = tuple(sorted(3 - x for x in p['lifts'][k]))
            while min(t) < end:
                t = tuple(x + 5 for x in t)
            while min(t) - 5 >= end:
                t = tuple(x - 5 for x in t)
            lifts[k], end = t, max(t)
        moved = dict(order=order, lifts=tuple(lifts))
        verify_placement(ss, moved)
        assert moved in geometries[len(parts)][ss]
        old_words = port_rotations(parts, p)
        new_words = set(port_rotations(parts, moved))
        for word in old_words:
            reverse = tuple(reversed(word))
            start = next(i for i, name in enumerate(reverse) if name.startswith('c0'))
            assert reverse[start:] + reverse[:start] in new_words
    targets = []
    for e in r.get('targets', []):
        raw = tuple(PI[e['row'][RHO[i]]] for i in range(5))
        # The base algebra is equivariant on the raw row; completion is moved
        # as a whole theorem, never re-normalizing only the target against q.
        before = row_evidence(parts, supports, bans, e['row'])
        after = row_evidence(parts, ss, fs, raw)
        assert before['status'] == after['status']
        for a, b in zip(before['components'], after['components']):
            assert {tuple(sorted(PI[c] for c in x)) for x in a['options']} == set(b['options'])
        targets.append(dict(raw_row=raw, status=e['status'],
                            guaranteed_z_colors=sorted(PI[c] for c in e['guaranteed_z_colors'])))
    return dict(supports=ss, bans=fs, targets=targets)


def relation_controls():
    # Enumerate all nonempty unary/binary relations, keeping whole tuples.
    counts = {}
    for n in (1, 2):
        tuples = tuple(product(range(4), repeat=n))
        count = 0
        for mask in range(1, 1 << len(tuples)):
            rel = tuple(t for j, t in enumerate(tuples) if mask >> j & 1)
            f = set.intersection(*(set(t) for t in rel))
            assert len(f) <= n
            assert U - f == {a for a in U if any(all(c != a for c in t) for t in rel)}
            moved = tuple(tuple(PI[c] for c in t) for t in rel)
            assert set.intersection(*(set(t) for t in moved)) == {PI[c] for c in f}
            count += 1
        counts[str(n)] = count
    rel = ((0, 3), (3, 0))
    marginals = product(*(set(t[j] for t in rel) for j in range(2)))
    assert set.intersection(*(set(t) for t in rel)) == {0, 3}
    assert set.intersection(*(set(t) for t in marginals)) == set()
    return counts


def build():
    geometries = {r: circular_supports(r) for r in (3, 4)}
    for r, geometry in geometries.items():
        assert set(geometry) == independent_arc_supports(r)
        for ss, ps in geometry.items():
            for p in ps:
                verify_placement(ss, p)
        assert all(len(ps) == 1 for ps in geometry.values())
    assert tuple(map(len, geometries.values())) == (480, 360)
    assert ((0, 2), (1, 3), (0, 4)) not in geometries[3]
    assert ((0, 1), (1, 2), (2, 3, 4)) in geometries[3]
    assert completion(((2, 3, 4), (1, 4), (0, 2)), ((3,), (0,), (1,)), 0, 1) is None
    assert completion(((2, 3, 4), (0, 1), (0, 4)), ((3,), (0,), (2,)), 0, 1)
    source = ROOT / 'artifacts/c5_no_spoke_exterior/observations.json'
    saved = json.loads(source.read_text())
    assert saved['covers'] == covers()
    records, counts = [], {}
    for parts in PARTS:
        counter = Counter()
        for c in covers():
            if tuple(c['partition']) != parts:
                continue
            bans = tuple(tuple(f) for f in c['forbidden'])
            for supports, placements in sorted(geometries[len(parts)].items()):
                if any(transport(s, f, Q)[0] != (f,) for s, f in zip(supports, bans)):
                    continue
                if any(len({Q[i] for i in s} | {a}) < 2
                       for s, f in zip(supports, bans) for a in f):
                    continue
                counter['necessary'] += 1
                r = dict(index=len(records), parts=parts, bans=bans, supports=supports,
                         placements=placements,
                         port_rotations=port_rotations(parts, placements[0]))
                failure = next((e for row in T4 if
                                (e := row_evidence(parts, supports, bans, row))['status'] == 'reject'), None)
                if failure:
                    r.update(status='T4_rejected', evidence=failure)
                    counter['T4_rejected'] += 1
                else:
                    targets = [row_evidence(parts, supports, bans, p, True) for p in TARGETS]
                    base = [row_evidence(parts, supports, bans, p) for p in TARGETS]
                    r.update(status='retained', targets=targets,
                             base_target_status=[e['status'] for e in base])
                    counter['retained'] += 1
                    counter['/'.join(e['status'] for e in targets)] += 1
                    counter['completion_new_accepts'] += sum(
                        e['status'] == 'accept' and b['status'] != 'accept' for e, b in zip(targets, base))
                r['reflection'] = reflection_audit(r, geometries)
                records.append(r)
        counts[','.join(map(str, parts))] = dict(sorted(counter.items()))
    assert counts['2,1,1,1'] == dict(necessary=96, T4_rejected=48, retained=48,
                                      **{'accept/accept': 48}, completion_new_accepts=12)
    assert counts['2,2,1']['necessary'] == 1952 and counts['2,2,1']['retained'] == 616
    lookup = {(r['parts'], r['bans'], r['supports']): r for r in records}
    for r in records:
        ss, fs = reflect_supports(r['supports'], r['bans'])
        assert lookup[r['parts'], fs, ss]['status'] == r['status']
    # The four singleton roles have just two surviving support families.
    families = sorted({tuple(s for f, s in sorted(zip(r['bans'], r['supports'])))
                       for r in records if r['parts'] == PARTS[1] and r['status'] == 'retained'})
    assert families == [((0, 1), (1, 2), (0, 4), (2, 3, 4)),
                        ((1, 2), (2, 3), (3, 4), (0, 1, 4))]
    paths = [Path(__file__), source, ROOT / 'scripts/c5_no_spoke_exterior.py',
             ROOT / 'scripts/c5_single_spoke_cores.py', COMPLETION_SOURCE,
             ROOT / 'scripts/c5_single_spoke_completion.py',
             ROOT / 'scripts/c5_two_spoke_middle_21.py',
             ROOT / 'scripts/c5_single_spoke_root_conservation.py']
    return dict(schema=1, scope='necessary support table; arbitrary-size paper order and separation, no disk realizability or new Lean theorem',
                inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                geometry_counts={str(r): len(g) for r, g in geometries.items()},
                counts=counts, four_component_support_families=families,
                relation_controls=relation_controls(), root_controls=local_audit(),
                completion_cover=audit_completion(json.loads(COMPLETION_SOURCE.read_text())),
                records=records)


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
    print(json.dumps(result['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
