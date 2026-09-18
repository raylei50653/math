#!/usr/bin/env python3
"""R28: all attachment positions on a shared three-cycle chain, list evidence."""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

from c5_degree5_long_triangle_roots import U, D, PAIRS, TRIPLES, colors, singleton, roots, arm_states
from c5_degree5_three_cycle_roots import relation, restrict

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_three_cycle_positions/observations.json'


@lru_cache(None)
def joined(cycles, h):
    return restrict(relation(cycles[1], h), roots(cycles[0]), roots(cycles[2]))


def private_positions(lengths, h):
    return tuple((j, i) for j, n in enumerate(lengths) for i in range(n)
                 if i != 0 and not (j == 1 and i == h))


def rigid(cycles, h):
    private = [[v for i, v in enumerate(ls) if i != 0 and not (j == 1 and i == h)]
               for j, ls in enumerate(cycles)]
    s = private[1][0]
    return (s in PAIRS and all(v == s for v in private[1])
            and all(v == U ^ s for v in private[0] + private[2]))


def brute_accepts(cycles, h):
    """Independent graph backtracking; does not call transfer or root routines."""
    ids, lists, adjacency = [], [], []
    for j, ls in enumerate(cycles):
        row = []
        for i, allowed in enumerate(ls):
            if j == 1 and i == 0:
                v = ids[0][0]
            elif j == 2 and i == 0:
                v = ids[1][h]
            else:
                v = len(lists)
                lists.append(allowed)
                adjacency.append(set())
            row.append(v)
        ids.append(row)
        for u, v in zip(row, row[1:] + row[:1]):
            adjacency[u].add(v)
            adjacency[v].add(u)
    assignment = {}

    def visit():
        if len(assignment) == len(lists):
            return True
        choices = []
        for v, allowed in enumerate(lists):
            if v not in assignment:
                mask = allowed
                for w in adjacency[v]:
                    if w in assignment:
                        mask &= ~(1 << assignment[w])
                choices.append((mask.bit_count(), v, mask))
        _, v, mask = min(choices)
        for c in colors(mask):
            assignment[v] = c
            if visit():
                return True
        assignment.pop(v, None)
        return False
    return visit()


def retained(lengths, h, marks):
    result = []
    for j, n in enumerate(lengths):
        keep = {0, h} if j == 1 else {0}
        keep.update(i for block, i in marks if block == j)
        size = 5 if len(keep) == 4 else 3
        for i in range(n):
            if len(keep) == size:
                break
            keep.add(i)
        assert len(keep) == size
        result.append(tuple(sorted(keep)))
    return tuple(result)


def conditioned(lengths, h, s, marks, extras, states, a):
    cycles = [[U if i == 0 or (j == 1 and i == h) else (s if j == 1 else U ^ s)
               for i in range(n)] for j, n in enumerate(lengths)]
    for (j, i), c in zip(marks, extras):
        cycles[j][i] |= 1 << c
    for (j, i), state in zip(marks, states):
        cycles[j][i] &= ~singleton(state[a])
    return tuple(map(tuple, cycles))


def build():
    counts, digest, controls = Counter(), sha256(), {}
    def record(kind, data):
        counts[kind] += 1
        digest.update((json.dumps([kind, data], separators=(',', ':')) + '\n').encode())

    # Exhaustive arbitrary >=2 lists, independent graph oracle, no rigidity assumed.
    for ls in product(PAIRS + TRIPLES + (U,), repeat=5):
        cycles = ((U, ls[0], ls[1]), (U, U, ls[2]), (U, ls[3], ls[4]))
        q = joined(cycles, 1)
        assert bool(q) == brute_accepts(cycles, 1)
        assert (not q) == rigid(cycles, 1)
        counts['arbitrary_rejections'] += not bool(q)
        record('arbitrary_triangle_lists', [ls, q])

    profiles = arm_states()
    by_color = {c: tuple(st for st in profiles if st[D] == 1 << c) for c in range(4)}
    shapes = ((3, 3, 3), (5, 5, 5), (5, 7, 9))
    for lengths in shapes:
        for h in range(1, lengths[1]):
            positions = private_positions(lengths, h)
            for marks in combinations_with_replacement(positions, 2):
                same = marks[0] == marks[1]
                keeps = retained(lengths, h, marks)
                hh = keeps[1].index(h)
                for s in PAIRS:
                    palettes = [s if j == 1 else U ^ s for j, _ in marks]
                    for extras in product(*(colors(U ^ p) for p in palettes)):
                        if same and extras[0] == extras[1]:
                            continue
                        for states in product(*(by_color[c] for c in extras)):
                            rows, short_rows = [], []
                            for a in range(4):
                                cycles = conditioned(lengths, h, s, marks, extras, states, a)
                                q = joined(cycles, h)
                                assert (not q) == rigid(cycles, h)
                                short = tuple(tuple(ls[i] for i in keep) for ls, keep in zip(cycles, keeps))
                                qq = joined(short, hh)
                                for bits in product((False, True), repeat=3):
                                    partial = tuple(short[j] if bits[j] else cycles[j] for j in range(3))
                                    assert bool(joined(partial, hh if bits[1] else h)) == bool(q)
                                if lengths == (3, 3, 3):
                                    assert bool(q) == brute_accepts(cycles, h)
                                    counts['conditioned_graph_checks'] += 1
                                rows.append(q)
                                short_rows.append(qq)
                            forbidden = sum(1 << a for a, q in enumerate(rows) if not q)
                            assert forbidden & (1 << D)
                            if not same:
                                assert forbidden == 1 << D
                            else:
                                # Freeing the marked point gives the complementary pair.
                                j, i = marks[0]
                                intrinsic = [list(ls) for ls in conditioned(lengths, h, s, marks, extras, states, D)]
                                intrinsic[j][i] = U
                                mask = 0
                                for c in range(4):
                                    intrinsic[j][i] = 1 << c
                                    mask |= bool(joined(tuple(map(tuple, intrinsic)), h)) << c
                                assert mask == U ^ palettes[0]
                                expected = sum(1 << a for a in range(4)
                                    if not (mask & ~(singleton(states[0][a]) | singleton(states[1][a]))))
                                assert forbidden == expected
                                if forbidden != 1 << D:
                                    counts['same_point_extra_rejection'] += 1
                                    controls.setdefault('same_point_extra_rejection', dict(lengths=lengths,
                                        h=h, marks=marks, s=s, extras=extras, paths=[profiles[st] for st in states],
                                        rows=rows, forbidden=forbidden))
                            if rows != short_rows:
                                controls.setdefault('ordered_relation_changes', dict(lengths=lengths, h=h,
                                    marks=marks, s=s, extras=extras, states=states, keeps=keeps,
                                    source_rows=rows, target_rows=short_rows))
                            kind = 'same_point' if same else 'distinct_' + ''.join(str(j) for j, _ in marks)
                            if len(keeps[1]) == 5:
                                counts['pentagon_target_queries'] += 1
                                controls.setdefault('four_distinct_middle_marks', dict(lengths=lengths, h=h,
                                    marks=marks, kept=keeps, distinguished=sorted({0,h,*[i for _,i in marks]})))
                            record(kind, [lengths,h,marks,s,extras,states,rows,short_rows])

    cycles = ((U,12,12), (U,U,3), (U,12,12))
    assert not joined(cycles,1)
    relaxed = restrict(relation(cycles[1],1), U, roots(cycles[2]))
    assert relaxed
    controls['deleting_unmarked_leaf_changes_acceptance'] = dict(cycles=cycles, h=1,
        leaf_root=roots(cycles[0]), before=0, after=relaxed)
    assert len(controls) == 4
    files = [Path(__file__), ROOT/'scripts/c5_degree5_three_cycle_roots.py',
             ROOT/'scripts/c5_degree5_long_triangle_roots.py']
    return dict(schema=1, scope='All arm positions on a shared three-odd-cycle chain; fixed-q list evidence only. No new graph minor or disk exclusion.',
        summary=dict(counts), query_sha256=digest.hexdigest(), controls=controls,
        source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
