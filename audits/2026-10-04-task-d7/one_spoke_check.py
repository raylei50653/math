#!/usr/bin/env python3
"""Independent small-domain audit of E2 section 5.2. Imports no repo checker.

Reads the pinned 102-record interface as data, recomputes its shield filtering,
two-row candidates, local palette constraints, and cycle-arc K5 certificates.
This is an interface audit, not arbitrary-size source-graph enumeration.
"""
from functools import lru_cache
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COLORS = frozenset(range(4))
PERMUTATIONS = tuple(permutations(range(4)))
Q = (0, 1, 0, 1, 2)
FAR = ((0, 1, 2, 0, 1), (0, 1, 2, 0, 2))


def subsets(xs, maximum=None):
    xs = tuple(sorted(xs))
    return tuple(frozenset(s) for n in range(len(xs) + 1)
                 if maximum is None or n <= maximum for s in combinations(xs, n))


def frame_edges(support):
    return frozenset(i for i in range(5)
                     if i in support and (i + 1) % 5 in support)


def record_key(spoke, supports, bans):
    return spoke, tuple(tuple(sorted(s)) for s in supports), tuple(tuple(sorted(b)) for b in bans)


@lru_cache(None)
def candidate_bans(support, ban, row):
    maps = [pi for pi in PERMUTATIONS if all(pi[Q[i]] == row[i] for i in support)]
    if maps:
        images = {frozenset(pi[c] for c in ban) for pi in maps}
        assert len(images) == 1
        return tuple(images)
    seen, oldseen = {row[i] for i in support}, {Q[i] for i in support}
    removed = {d for d in COLORS - seen - oldseen
               if any(len({a, d, e}) == 3 for a in ban for e in COLORS - oldseen)}
    return tuple(fs for fs in subsets(COLORS, 2)
                 if not fs & removed and all(len(seen | {a}) >= 2 for a in fs)
                 and all(frozenset(pi[c] for c in fs) == fs for pi in PERMUTATIONS
                         if all(pi[c] == c for c in seen)))


def whole_graph_matches(spoke, supports, bans, row, lookup):
    """Test all literal dihedral/color maps; never normalize pieces separately."""
    result = set()
    for sign, shift in product((1, -1), range(5)):
        geometry = tuple((sign * i + shift) % 5 for i in range(5))
        target_spoke = geometry[spoke]
        if target_spoke not in (0, 1, 4):
            continue
        for pi in PERMUTATIONS:
            if any(pi[row[i]] != Q[geometry[i]] for i in range(5)):
                continue
            key = record_key(target_spoke,
                             [{geometry[i] for i in s} for s in supports],
                             [{pi[c] for c in b} for b in bans])
            if key in lookup:
                result.add(lookup[key])
    return result


@lru_cache(None)
def local_options(support, q, p, eq, ep):
    eq, ep = frozenset(eq), frozenset(ep)
    allowed = []
    for t in subsets(support):
        # Exact invariance/covariance of the rooted residual under boundary maps.
        if any(frozenset(pi[c] for c in eq) != eq for pi in PERMUTATIONS
               if all(pi[q[i]] == q[i] for i in t)):
            continue
        if any(frozenset(pi[c] for c in ep) != ep for pi in PERMUTATIONS
               if all(pi[p[i]] == p[i] for i in t)):
            continue
        stable = {c for c in COLORS if all((q[i] == c) == (p[i] == c) for i in t)}
        if eq & stable != ep & stable:
            continue
        if any(frozenset(pi[c] for c in eq) != ep for pi in PERMUTATIONS
               if all(pi[q[i]] == p[i] for i in t)):
            continue
        allowed.append(t)
    return tuple(allowed)


def connected_frame_arcs():
    arcs = []
    for mask in product(range(3), repeat=5):
        bags = [frozenset(i for i, c in enumerate(mask) if c == b) for b in range(3)]
        if not all(bags):
            continue
        if all(len(frame_edges(b)) == len(b) - 1 for b in bags):
            arcs.append(tuple(bags))
    assert len(arcs) == 60
    return tuple(arcs)


ARCS = connected_frame_arcs()


def has_minor(t0, t1, exterior):
    if not t0 or not t1:
        return True  # Already impossible; no minor claim needed.
    for x, y, z in ARCS:
        if z & exterior and all(t & x and t & y for t in (*t0, *t1)):
            # Three proper connected cycle arcs are pairwise adjacent.
            assert all(any((i + 1) % 5 in b or (i - 1) % 5 in b for i in a)
                       for a, b in combinations((x, y, z), 2))
            return True
    return False


def first_bridge_excluded(item):
    for k in range(2):
        fq, fp = item['bans'], item['far_bans']
        q, p = Q, item['far_row']
        a, b = fq[k], fp[k]
        support = tuple(item['supports'][k])
        exterior = frozenset({item['spoke']} | item['supports'][1-k])
        if len(a) == len(b) == 1:
            continue
        if len(a) == len(b) == 2:
            t = local_options(support, q, p, tuple(sorted(a)), tuple(sorted(b)))
            if has_minor(t, t, exterior):
                return True
            continue
        if len(a) == 1:
            q, p, a, b = p, q, b, a
        c = next(iter(b))
        variants = []
        for beta in COLORS - {c}:
            for gamma in COLORS - {beta}:
                t0 = local_options(support, q, p, tuple(sorted(a)), tuple(sorted((c, beta))))
                t1 = local_options(support, q, p, tuple(sorted(a)), tuple(sorted((beta, gamma))))
                variants.append(has_minor(t0, t1, exterior))
        if all(variants):
            return True
    return False


def carrier_excluded(item):
    for k in range(2):
        a, b, q, p = item['bans'][k], item['far_bans'][k], Q, item['far_row']
        if sorted((len(a), len(b))) != [1, 2]:
            continue
        if len(a) == 1:
            a, b, q, p = b, a, p, q
        c = next(iter(b))
        if 3 not in a or c == 3:
            continue
        exterior = frozenset({item['spoke']} | item['supports'][1-k])
        possibilities = []
        for d in COLORS - {3, c}:
            t = local_options(tuple(item['supports'][k]), q, p,
                              tuple(sorted(a)), tuple(sorted((d, 3))))
            possibilities.append(has_minor(t, t, exterior))
        if all(possibilities):
            return True
    return False


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    reached = {next(iter(vertices))}
    while True:
        new = {v for u, v in edges if u in reached and v in vertices}
        new |= {u for u, v in edges if v in reached and u in vertices}
        if new <= reached:
            return reached == vertices
        reached |= new


def final_terminal_checks():
    artifact = json.loads((ROOT / 'artifacts/c5_excess_one_e2_951_remaining/final_sidebranch_terminal_blocks.json').read_text())
    minor_count = 0
    for case in artifact['cases']:
        for skeleton in case['actual_terminal_cycle_K5_skeletons']:
            edges = {frozenset(e) for e in skeleton['source_edges']}
            directed = [tuple(e) for e in edges]
            bags = list(map(set, skeleton['branch_sets']))
            assert len(bags) == 5 and all(connected(b, directed) for b in bags)
            assert all(not a & b for a, b in combinations(bags, 2))
            for a, b in combinations(bags, 2):
                assert any(e & a and e & b for e in edges)
            for witness in skeleton['ten_adjacencies']:
                assert frozenset(witness['actual_edge']) in edges
                a, b = [bags[i] for i in witness['branches']]
                assert set(witness['actual_edge']) & a and set(witness['actual_edge']) & b
            minor_count += 1
    assert minor_count == 12

    # Independently compute joint private-vertex lists, retaining one color map
    # for BOTH rows and both actual attachment pairs.
    table_count = 0
    for support, q, p, pairs in [
            ((1, 2, 3), Q, FAR[0], ((1, 2), (2, 3))),
            ((0, 3, 4), FAR[0], Q, ((0, 4), (3, 4)))]:
        assert len({q[i] for i in support}) == 2
        for pi in PERMUTATIONS:
            joint = [(COLORS - {pi[q[i]] for i in pair},
                      COLORS - {pi[p[i]] for i in pair}) for pair in pairs]
            assert joint[0][0] == joint[1][0] == {pi[2], pi[3]}
            assert joint[0][1] != joint[1][1]
            table_count += len(joint)
    assert table_count == 96
    return minor_count, table_count


def audit():
    source_path = ROOT / 'artifacts/c5_single_spoke_residual_locality/observations.json'
    source = json.loads(source_path.read_text())
    records = [r['original_record'] for r in source['table']['retained']]
    assert len(records) == 102
    assert sum(list(map(len, r['bans'])) == [1, 2] for r in records) == 51
    assert sum(list(map(len, r['bans'])) == [2, 1] for r in records) == 51
    lookup = {record_key(r['spoke'], r['supports'], r['bans']): r['id'] for r in records}
    passing, schedules = [], []
    for r in records:
        supports = list(map(frozenset, r['supports']))
        shields = [frame_edges(s) for s in supports]
        s = r['spoke']
        if not all(len(t) >= 3 and len(e) == len(t) - 1 for t, e in zip(supports, shields)):
            continue
        if shields[0] & shields[1] or any({(s - 1) % 5, s, (s + 1) % 5} <= t for t in supports):
            continue
        assert supports[0] | supports[1] | {s} == set(range(5))
        passing.append(r['id'])
        for p in FAR:
            candidates = [candidate_bans(tuple(sorted(t)), tuple(b), p)
                          for t, b in zip(supports, r['bans'])]
            for fs in product(*candidates):
                if fs[0] & fs[1] or len(fs[0]) + len(fs[1]) != 3:
                    continue
                if fs[0] | fs[1] != COLORS - {p[s]}:
                    continue
                matching = whole_graph_matches(s, supports, fs, p, lookup)
                if not matching:
                    continue
                schedules.append(dict(source_id=r['id'], spoke=s, supports=supports,
                                      bans=tuple(map(frozenset, r['bans'])), far_row=p,
                                      far_bans=fs, matching_records=matching))
    original = json.loads((ROOT / 'artifacts/c5_excess_one_e2_951_remaining/observations.json').read_text())
    ledger = original['t1_double_minimal_ledger']
    assert passing == ledger['shield_pass_source_ids']
    identity = lambda r: (r['source_id'], r['far_row'], tuple(tuple(sorted(b)) for b in r['far_bans']))
    expected = {(r['original_source_id'], tuple(r['far_row']), tuple(map(tuple, r['far_forbidden'])))
                for r in ledger['schedules']}
    assert {identity(r) for r in schedules} == expected
    assert len(passing) == 30 and len(schedules) == 54
    first = [r for r in schedules if first_bridge_excluded(r)]
    survivors = [r for r in schedules if not first_bridge_excluded(r)]
    carriers = [r for r in survivors if carrier_excluded(r)]
    last = [r for r in survivors if not carrier_excluded(r)]
    assert len(first) == 36 and len(survivors) == 18
    assert len(carriers) == 14 and len(last) == 4
    assert {r['source_id'] for r in last} == {82, 317, 477, 817}
    splits = []
    for r in last:
        k = next(k for k in range(2) if len(r['bans'][k]) == 2)
        eq, ep = tuple(sorted(r['bans'][k])), tuple(sorted(r['far_bans'][k]))
        assert eq == ep == (2, 3)
        t = local_options(tuple(r['supports'][k]), Q, r['far_row'], eq, ep)
        common = set.intersection(*(set(a) for a in t))
        assert len(common) == 1
        for a, b in product(t, repeat=2):
            if a | b != r['supports'][k]:
                continue
            if len(frame_edges(a)) != len(a) - 1 or len(frame_edges(b)) != len(b) - 1:
                continue
            if frame_edges(a) & frame_edges(b):
                continue
            splits.append(dict(source_id=r['source_id'], supports=[sorted(a), sorted(b)]))
    assert len(splits) == 8
    minor_count, table_count = final_terminal_checks()
    return dict(interface_records=102, shield_source_records=30, schedules=54,
                first_bridge_closed=36, carrier_closed=14, last_four_ids=sorted({r['source_id'] for r in last}),
                final_shield_splits=splits,
                terminal_K5_skeletons=minor_count, terminal_joint_palette_rows=table_count,
                limits='No arbitrary-size graph enumeration or repository checker import; paper induction remains separate.')


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
