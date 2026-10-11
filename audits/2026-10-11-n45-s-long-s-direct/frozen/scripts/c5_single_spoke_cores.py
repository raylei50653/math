#!/usr/bin/env python3
"""Finite necessary covers/supports after the arbitrary-size slit-disk reduction.

No source graph enumeration; retained records are not disk realizations.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

Q = (0, 1, 0, 1, 2)
U = frozenset(range(4))
RHO = (3, 2, 1, 0, 4)
PI = (1, 0, 2, 3)
PERMS = tuple(permutations(range(4)))
PARTS = ((4,), (3, 1), (2, 2), (2, 1, 1))
ROWS = tuple(b for b in product(range(4), repeat=5)
             if all(b[i] != b[(i+1) % 5] for i in range(5)))
T4 = tuple(b for b in ROWS if len(set(b)) == 4)
TARGETS = ((0, 1, 0, 2, 1), (0, 1, 2, 1, 2))
SUPPORTS = tuple(tuple(i for i in range(5) if mask >> i & 1)
                 for mask in range(1, 32))
OUT = Path(__file__).resolve().parents[1] / 'artifacts/c5_single_spoke_cores/observations.json'


def covers(s, parts):
    a = U - {Q[s]}
    subsets = [frozenset(c for c in a if mask >> c & 1) for mask in range(16)]
    subsets = sorted(set(subsets) - {frozenset()}, key=lambda x: tuple(sorted(x)))
    result = []
    for fs in product(subsets, repeat=len(parts)):
        if any(len(f) > n for f, n in zip(fs, parts)) or set().union(*fs) != a:
            continue
        if all(f - set().union(*(fs[j] for j in range(len(fs)) if j != i))
               for i, f in enumerate(fs)):
            result.append(tuple(tuple(sorted(f)) for f in fs))
    return result


@lru_cache(None)
def transport(support, ban, row):
    ps = tuple(p for p in PERMS if all(p[Q[i]] == row[i] for i in support))
    images = {tuple(sorted(p[c] for c in ban)) for p in ps}
    return tuple(sorted(images)), ps


@lru_cache(None)
def lifts(s, support):
    """Both copies of b_s are allowed; they are the same source vertex."""
    base = tuple(sorted((i-s) % 5 for i in support if i != s))
    if s not in support:
        return (base,)
    return tuple(tuple(sorted(base + ends)) for ends in ((0,), (5,), (0, 5)))


def placements(s, supports):
    """A witness for each possible component order, keeping component labels."""
    found = []
    for order in permutations(range(len(supports))):
        for lifted in product(*(lifts(s, x) for x in supports)):
            if all(max(lifted[a]) <= min(lifted[b]) for a, b in zip(order, order[1:])):
                found.append(dict(order=order, lifted_supports=lifted))
                break
    return found


def reflect(r):
    return dict(spoke=RHO[r['spoke']],
                bans=[tuple(sorted(PI[c] for c in f)) for f in r['bans']],
                supports=[tuple(sorted(RHO[i] for i in x)) for x in r['supports']])


def row_evidence(s, supports, bans, row):
    known, possible, evidence, unknown, bounds = set(), set(), [], [], []
    for k, (support, ban) in enumerate(zip(supports, bans)):
        images, ps = transport(support, ban, row)
        assert len(images) <= 1
        if images:
            known.update(images[0])
            possible.update(images[0])
            evidence.append(dict(component=k, permutation=ps[0], forbidden=images[0]))
        else:
            unknown.append(k)
            seen = {row[i] for i in support}
            absent = U - seen
            arity = (2, 1, 1)[k]
            bound = seen | (absent if len(absent) <= arity else set())
            possible.update(bound)
            bounds.append(dict(component=k, arity=arity, seen=sorted(seen),
                               possible_forbidden=sorted(bound)))
    available = U - {row[s]}
    status = ('reject' if available <= known else
              'accept' if available - possible else 'unresolved')
    return dict(row=row, status=status, known=evidence, unknown=unknown,
                available=sorted(available), remaining_after_known=sorted(available-known),
                unknown_bounds=bounds, guaranteed_z_colors=sorted(available-possible))


def verify_evidence(r, e):
    row, blocked = e['row'], set()
    for item in e['known']:
        k, p = item['component'], item['permutation']
        assert sorted(p) == list(range(4))
        assert all(p[Q[i]] == row[i] for i in r['supports'][k])
        expected = {p[c] for c in r['bans'][k]}
        assert expected == set(item['forbidden'])
        blocked.update(expected)
    if e['status'] == 'reject':
        assert U - {row[r['spoke']]} <= blocked
    elif e['status'] == 'accept':
        possible = set(blocked)
        for item in e['unknown_bounds']:
            k = item['component']
            seen = {row[i] for i in r['supports'][k]}
            stable_sets = []
            for mask in range(16):
                f = {a for a in U if mask >> a & 1}
                if len(f) <= item['arity'] and all(
                        {p[a] for a in f} == f for p in PERMS
                        if all(p[c] == c for c in seen)):
                    stable_sets.append(f)
            exact_bound = set().union(*stable_sets)
            assert exact_bound == set(item['possible_forbidden'])
            possible.update(exact_bound)
        assert U - {row[r['spoke']]} - possible == set(e['guaranteed_z_colors'])
        assert e['guaranteed_z_colors']


def binary_relations():
    result = []
    for a in range(4):
        candidates = tuple(t for t in product(range(4), repeat=2) if a in t)
        relations = []
        for mask in range(1 << len(candidates)):
            rel = tuple(t for j, t in enumerate(candidates) if mask >> j & 1)
            if not rel:
                continue
            forbidden = set.intersection(*(set(t) for t in rel))
            release = [next((t for t in rel if t[j] == a and t[1-j] != a), None)
                       for j in range(2)]
            if forbidden == {a} and all(release):
                relations.append(dict(tuples=rel, release_witnesses=release))
        assert len(relations) == 95
        result.append(dict(forbidden=a, relations=relations))
    for entry in result:
        target = {tuple(tuple(t) for t in r['tuples']) for r in result[PI[entry['forbidden']]]['relations']}
        for r in entry['relations']:
            assert tuple(sorted(tuple(PI[c] for c in t) for t in r['tuples'])) in target
    return result


def source_controls():
    source = OUT.parents[1] / 'c5_degree5_interfaces/observations.json'
    data = json.loads(source.read_text())
    checked = []
    for w in data['witnesses']:
        if w['port_partition'] != [2, 2]:
            continue
        z, edges = w['z'], [tuple(e) for e in w['edges']]
        adj = {v: set() for e in edges for v in e}
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        spoke, = sorted(adj[z] & set(range(5)))
        assert len(adj[z]) == 5 and all(len(adj[v]) == 4 for v in adj if v >= 5 and v != z)
        cs = w['patterns'][0]['components']
        supports = [tuple(sorted(set().union(*(adj[v] & set(range(5)) for v in c['vertices'])))) for c in cs]
        pos = placements(spoke, supports)
        assert pos
        rot = w['apex_rotation'][z]
        j = rot.index(spoke)
        port_word = rot[j+1:] + rot[:j]
        owner = {v: k for k, c in enumerate(cs) for v in c['ports']}
        word = tuple(owner[v] for v in port_word)
        assert word in ((0, 0, 1, 1), (1, 1, 0, 0))
        all_rows = []
        q_bans = None
        for row in ROWS:
            relations, bans = [], []
            for c in cs:
                vs, ps = c['vertices'], c['ports']
                possible = set()
                for colors in product(range(4), repeat=len(vs)):
                    f = dict(zip(vs, colors))
                    if all(f[u] != f[v] for u, v in edges if u in f and v in f) and all(
                            f[v] != row[i] for v in vs for i in adj[v] if i < 5):
                        possible.add(tuple(f[v] for v in ps))
                assert possible
                relations.append(sorted(possible))
                bans.append(tuple(sorted(set.intersection(*(set(t) for t in possible)))))
                reflected_row = tuple(PI[row[RHO[i]]] for i in range(5))
                reflected = set()
                for colors in product(range(4), repeat=len(vs)):
                    f = dict(zip(vs, colors))
                    if all(f[u] != f[v] for u, v in edges if u in f and v in f) and all(
                            f[v] != reflected_row[RHO[i]] for v in vs for i in adj[v] if i < 5):
                        reflected.add(tuple(f[v] for v in ps))
                assert reflected == {tuple(PI[c] for c in t) for t in possible}
            allowed = U - {row[spoke]} - set().union(*map(set, bans))
            # Independent whole-source coloring join, with every component tuple intact.
            direct = {a for a in U if a != row[spoke] and any(
                all(a not in t for t in pair) for pair in product(*relations))}
            assert allowed == direct
            if row == Q:
                q_bans = tuple(bans)
                assert q_bans in covers(spoke, (2, 2)) and not allowed
                assert all(set(rel) == set(permutations(ban)) for rel, ban in zip(relations, bans))
            all_rows.append(dict(row=row, relations=relations, forbidden=bans, z_allowed=sorted(allowed)))
        for deletion in w['q_deletions']:
            f, e = deletion['witness'], tuple(deletion['edge'])
            assert tuple(f[:5]) == Q and all(f[u] != f[v] for u, v in edges if (u, v) != e)
        expected_edges = {e for e in edges if max(e) >= 5}
        assert {tuple(d['edge']) for d in w['q_deletions']} == expected_edges
        assert not w['accepts_T4']
        checked.append(dict(source_index=w['source_index'], spoke=spoke, supports=supports,
                            port_word=word, placements=pos, q_bans=q_bans,
                            deletion_count=len(expected_edges), rows=all_rows))
    assert len(checked) == 16
    return dict(source_sha256=sha256(source.read_bytes()).hexdigest(), witnesses=checked,
                scope='existing (2,2) disk sources; they fail T4, not (2,1,1) realizations')


def run():
    def canonical(row):
        order = list(dict.fromkeys(row))
        return tuple(order.index(c) for c in row)
    assert [canonical(tuple(PI[b[RHO[i]]] for i in range(5))) for b in TARGETS] == list(reversed(TARGETS))
    cover_table = []
    for s in range(5):
        for parts in PARTS:
            fs = covers(s, parts)
            assert len(fs) == {(4,): 1, (3, 1): 3, (2, 2): 12, (2, 1, 1): 6}[parts]
            mapped = {tuple(tuple(sorted(PI[c] for c in f)) for f in item) for item in fs}
            assert mapped == set(covers(RHO[s], parts))
            cover_table.append(dict(spoke=s, parts=parts, covers=fs))
    records, counts = [], Counter()
    # Other spoke positions are transported, not independently screened.
    for s in (0, 1, 4):
        for bans in covers(s, (2, 1, 1)):
            choices = [tuple(x for x in SUPPORTS if transport(x, f, Q)[0] == (f,)) for f in bans]
            for supports in product(*choices):
                counts[f'{s}:stabilizer_pass'] += 1
                pos = placements(s, supports)
                if not pos:
                    counts[f'{s}:order_rejected'] += 1
                    continue
                r = dict(spoke=s, bans=bans, supports=supports, placements=pos)
                # A K4-free Gallai tree has a vertex of internal degree <= 2.
                # One exterior colour would force every internal degree >= 3.
                if any(len({Q[i] for i in x} | set(f)) < 2 for x, f in zip(supports, bans)):
                    counts[f'{s}:one_exterior_color_rejected'] += 1
                    continue
                fail = next((e for b in T4
                             if (e := row_evidence(s, supports, bans, b))['status'] == 'reject'), None)
                if fail:
                    verify_evidence(r, fail)
                    r.update(status='T4_rejected', evidence=fail)
                else:
                    all_support = {s} | set().union(*map(set, supports))
                    targets = [row_evidence(s, supports, bans, b) for b in TARGETS]
                    for e in targets:
                        verify_evidence(r, e)
                    # The inherited unattached-boundary lemma applies to both targets.
                    if len(all_support) < 5:
                        assert set(range(5)) - all_support == {4}
                        status = 'separated_unattached'
                    elif all(e['status'] == 'accept' for e in targets):
                        status = 'separated_support'
                    else:
                        status = 'unresolved'
                    r.update(status=status, targets=targets)
                counts[f'{s}:{r["status"]}'] += 1
                reflected = reflect(r)
                assert reflect(reflected) == dict(spoke=s, bans=list(bans), supports=list(supports))
                for x, f in zip(reflected['supports'], reflected['bans']):
                    assert transport(x, f, Q)[0] == (f,)
                # Reflection reverses the slit line, component blocks and port orientation.
                reflected['placements'] = [dict(order=tuple(reversed(p['order'])),
                    lifted_supports=[tuple(sorted(5-v for v in x)) for x in p['lifted_supports']])
                    for p in pos]
                for p in reflected['placements']:
                    for x, support in zip(p['lifted_supports'], reflected['supports']):
                        assert x in lifts(reflected['spoke'], support)
                    assert all(max(p['lifted_supports'][a]) <= min(p['lifted_supports'][b])
                               for a, b in zip(p['order'], p['order'][1:]))
                r['reflection'] = reflected
                records.append(r)
    # Arity-four, arity-three, arity-two and arity-one tuple transport is pointwise;
    # enumerate every tuple to check queries and the common colour permutation.
    tuple_checks = 0
    for n in (1, 2, 3, 4):
        for t in product(range(4), repeat=n):
            rt = tuple(PI[c] for c in t)
            for a in U:
                assert (all(c != a for c in t) == all(c != PI[a] for c in rt))
                tuple_checks += 1
    color_support_types = [r for r in records if r['status'] != 'T4_rejected'
                           and list(r['bans']) == sorted(r['bans'])]
    assert Counter(r['spoke'] for r in color_support_types) == {0: 4, 1: 3, 4: 12}
    return dict(scope='necessary actual-support and contact-order types; no graph realizability claim',
                representatives=[0, 1, 4], covers=cover_table, counts=dict(sorted(counts.items())),
                tuple_transport_checks=tuple_checks, binary_relation_schemas=binary_relations(),
                source_controls=source_controls(), color_support_type_count=len(color_support_types), records=records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
