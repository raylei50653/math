#!/usr/bin/env python3
"""Independent small controls for D6 items 5/6; never imports a producer.

Enumerates just 500 six-attachment P3 configurations, finite root roles, and
subsets of the already bounded <= 3-edge child sector. It does not enumerate
unary interiors or assert that a necessary geometric profile is realizable.
The Jordan/annulus necessity of the sector and block order is paper evidence.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)
PARTITIONS = {0: [()], 1: [(1,)], 2: [(2,), (1, 1)],
              3: [(3,), (2, 1), (1, 1, 1)]}


def subsets(items, nonempty=False):
    items = tuple(sorted(items))
    return [frozenset(s) for n in range(int(nonempty), len(items) + 1)
            for s in combinations(items, n)]


def signature(role):
    return (tuple(role['spoke_colors']), tuple(role['unary_contacts']),
            tuple(map(tuple, role['unary_forbidden'])), tuple(role['residual']))


def side_roles(E):
    """Derive roles by assigning the forbidden colors, rather than the 18-form table."""
    covered = U - E
    result = []
    for t in range(4):
        for spokes in combinations(sorted(covered & {0, 1, 2}), t):
            remaining = covered - set(spokes)
            for ports in PARTITIONS[3 - t]:
                choices = [[f for f in subsets(remaining, True) if len(f) <= n]
                           for n in ports]
                for fs in product(*choices):
                    if set().union(*fs) != remaining:
                        continue
                    if sum(map(len, fs)) != len(remaining):
                        continue
                    result.append((tuple(spokes), ports,
                                   tuple(tuple(sorted(f)) for f in fs), tuple(sorted(E))))
    return result


def role_join(a, Ez, Ew):
    F = {(a, 3), (3, a)}

    def release_works(released, other):
        return any(x != y and (x, y) not in F for x in released for y in other)

    found = set()
    for z, w in product(side_roles(Ez), side_roles(Ew)):
        if any(not release_works(fs, Ew) for fs in z[2]):
            continue
        if any(not release_works((s,), Ew) for s in z[0]):
            continue
        if any(not release_works(fs, Ez) for fs in w[2]):
            continue
        if any(not release_works((s,), Ez) for s in w[0]):
            continue
        found.add((z, w))
    return found


def residual_shapes(a):
    F = {(a, 3), (3, a)}
    found = []
    candidates = [s for s in subsets(U, True) if len(s) <= 2]
    for Ez, Ew in product(candidates, repeat=2):
        pairs = set(product(Ez, Ew))
        offdiag = {(x, y) for x, y in pairs if x != y}
        if Ez & Ew and offdiag and offdiag <= F:
            found.append((Ez, Ew))
    expected = [(frozenset({a, 3}), frozenset({a, 3})),
                (frozenset({a}), frozenset({a, 3})),
                (frozenset({3}), frozenset({a, 3})),
                (frozenset({a, 3}), frozenset({a})),
                (frozenset({a, 3}), frozenset({3}))]
    assert set(found) == set(expected)
    return expected


def bounded_geometries(S0, S1, S2, Ez, Ew):
    """Generate within each <= 3-edge sector, avoiding the original 114,048-product loop."""
    found = set()
    candidates = 0

    def support_observes(A, E):
        colors = {Q[v] for v in A}
        if len(E) == 2:
            return (U - E) <= colors
        color = next(iter(E))
        return ({0, 1, 2} <= colors) if color == 3 else color in colors

    for anchor in S0:
        arc_len = min((v - anchor) % 5 for v in S0 if v != anchor)
        I = tuple(range(anchor, anchor + arc_len + 1))
        u, v = sorted(anchor + (p - anchor) % 5 for p in S1)
        s = anchor + (S2[0] - anchor) % 5
        if v > I[-1] or s > I[-1]:
            continue
        for lo, hi in ((I[0], u), (u, v), (v, I[-1])):
            if not lo <= s <= hi:
                continue
            child = tuple(range(lo, hi + 1))
            assert len(child) <= 4
            choices = [subsets(child, True), subsets(child, True)]
            for Z, W in product(*choices):
                candidates += 1
                Az, Aw = tuple(sorted(v % 5 for v in Z)), tuple(sorted(v % 5 for v in W))
                if not support_observes(Az, Ez) or not support_observes(Aw, Ew):
                    continue
                # Both root blocks lie on the same side of the x2 tether;
                # either root block comes first. Coincident endpoints are legal.
                ordered = ((max(Z) <= min(W) and
                            (s <= min(Z) or max(W) <= s)) or
                           (max(W) <= min(Z) and
                            (s <= min(W) or max(Z) <= s)))
                if ordered:
                    found.add((Az, Aw))
    return found, candidates


def main():
    common = json.loads((HERE / 'snapshot/artifacts/c5_mixed_p3_common_endpoint/observations.json').read_bytes())
    saved_geometries = common['geometry']['retained_geometries']
    saved_cases = {c['name']: c for c in common['local']['cases']}
    saved_supports = {(g['case_name'], tuple(g['actual_side_supports'][0]),
                      tuple(g['actual_side_supports'][1])) for g in saved_geometries}
    found_supports = set()
    counts = Counter()
    roles_by_a = {}
    for a in (0, 1, 2):
        shapes = residual_shapes(a)
        joined = set().union(*(role_join(a, Ez, Ew) for Ez, Ew in shapes))
        saved = {(signature(common['local']['side_roles'][z]),
                  signature(common['local']['side_roles'][w]))
                 for z, w in common['local']['joins_by_a'][str(a)]}
        assert joined == saved
        assert len(joined) == 125
        assert all(z[1] and w[1] for z, w in joined)
        assert [len(role_join(a, Ez, Ew)) for Ez, Ew in shapes] == [25] * 5
        roles_by_a[a] = {'full_role_joins': len(joined), 'without_unary_at_a_root': 0}

    for local_id, supports in enumerate(product(combinations(range(5), 3),
                                                combinations(range(5), 2),
                                                combinations(range(5), 1))):
        counts['local_supports'] += 1
        lists = [U - {Q[v] for v in S} for S in supports]
        tuples = {t for t in product(*lists) if t[0] != t[1] and t[1] != t[2]}
        F = {(x, y) for x, y in product(U, repeat=2)
             if not any(t[2] != x and t[2] != y for t in tuples)}
        if not F:
            continue
        counts['nonempty_F_local_supports'] += 1
        c = Q[supports[2][0]]
        d, = lists[1] - {3}
        a, = U - {3, c, d}
        assert tuples == {(3, d, a), (3, d, 3)}
        assert F == {(a, 3), (3, a)}
        for branch, (Ez, Ew) in enumerate(residual_shapes(a)):
            counts['local_residual_cases'] += 1
            geometries, n = bounded_geometries(*supports, Ez, Ew)
            counts['bounded_sector_subset_products'] += n
            name = f'CPP-{local_id:03d}-{branch}'
            if geometries:
                counts['retained_cases'] += 1
                for Az, Aw in geometries:
                    found_supports.add((name, Az, Aw))
            else:
                counts['no_necessary_geometry_cases'] += 1
    assert found_supports == saved_supports
    assert counts['retained_cases'] == 36
    assert len(found_supports) == 140

    scope = json.loads((AUDIT / 'snapshot/audits/2026-10-04-task-d5/c4/scope_ledger.json').read_bytes())
    expected_keys = set()
    for g in saved_geometries:
        for join_id in saved_cases[g['case_name']]['side_join_ids']:
            expected_keys.add((g['case_name'], g['id'], join_id))
    actual_keys = {tuple(row['key']) for row in scope['ledger']}
    assert actual_keys == expected_keys and len(actual_keys) == 3500
    first = scope['ledger'][0]
    first_unary = first['original_unary_components'][0]
    assert first['key'] == ['CPP-131-0', 0, 0]
    assert first_unary['component'] == 'D_z_0'
    assert first_unary['actual_own_support'] == [1, 2]
    result = {'evidence': 'Independent finite necessary-profile control; paper topology and unbounded unary proofs remain separate.',
              'counts': dict(counts), 'retained_geometries': len(found_supports),
              'scope_keys': len(actual_keys), 'roles_by_a': roles_by_a,
              'saved_domain_comparisons': 'exact sets equal, not counts only',
              'old_short_support_example': {'key': first['key'], 'component': first_unary['component'],
                                            'actual_own_support': first_unary['actual_own_support']}}
    out = HERE / 'independent_scope_results.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
