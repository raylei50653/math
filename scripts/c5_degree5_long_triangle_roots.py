#!/usr/bin/env python3
"""Four-row long-cycle root interfaces; list evidence only, no source minors."""
import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_long_triangle_roots/observations.json'
U, D = 15, 3
PAIRS = tuple(sum(1 << c for c in cs) for cs in combinations(range(4), 2))
TRIPLES = tuple(U ^ (1 << c) for c in range(4))


def colors(mask):
    return [c for c in range(4) if mask & (1 << c)]


def singleton(mask):
    return mask if mask.bit_count() == 1 else 0


def step(message, allowed):
    return sum(1 << c for c in colors(allowed) if message & ~(1 << c))


def roots(lists):
    result = 0
    for c in colors(lists[0]):
        message = 1 << c
        for allowed in lists[1:]:
            message = step(message, allowed)
        if message & ~(1 << c):
            result |= 1 << c
    return result


def brute(lists):
    result = 0
    for cs in product(*map(colors, lists)):
        if all(a != b for a, b in zip(cs, cs[1:] + cs[:1])):
            result |= 1 << cs[0]
    return result


def arm_states():
    """Least closure of exact four-row messages under all six pair steps."""
    initial = (1, 2, 4, 8)
    paths = {initial: ()}
    queue = deque([initial])
    while queue:
        state = queue.popleft()
        for pair in PAIRS:
            target = tuple(step(m, pair) for m in state)
            if target not in paths:
                paths[target] = paths[state] + (pair,)
                queue.append(target)
    for state in paths:
        for wanted in (1, 2, 4, 8):
            assert sum(m == wanted for m in state) <= 1
        assert all(tuple(step(m, p) for m in state) in paths for p in PAIRS)
    return paths


def conditioned(lists, position, state):
    result = []
    for message in state:
        row = list(lists)
        row[position] &= ~singleton(message)
        result.append(roots(row))
    return tuple(result)


def build():
    counts, digest = Counter(), sha256()

    def record(kind, data):
        counts[kind] += 1
        digest.update((json.dumps([kind, data], separators=(',', ':')) + '\n').encode())

    # Arbitrary C5 lists, before using obstruction rigidity. Effective p list
    # has >=2 colors; all other private vertices have exactly two.
    for pos in range(1, 5):
        for lr, lp, private in product(TRIPLES, PAIRS + TRIPLES, product(PAIRS, repeat=3)):
            lists = [lr]
            it = iter(private)
            lists.extend(lp if i == pos else next(it) for i in range(1, 5))
            actual = roots(lists)
            assert actual == brute(lists)
            if actual.bit_count() == 1:
                palette = lr ^ actual
                assert all(x == palette for x in lists[1:])
            record('distinct_arbitrary_c5', [pos, lists, actual])
    for private in product(PAIRS, repeat=4):
        lists = [U, *private]
        actual = roots(lists)
        assert actual == brute(lists) and actual.bit_count() >= 2
        assert (actual.bit_count() == 2) == (len(set(private)) == 1)
        if actual.bit_count() == 2:
            assert actual == U ^ private[0]
        record('same_arbitrary_c5', [lists, actual])

    paths = arm_states()
    for state, path in paths.items():
        for a in range(4):
            available = 0
            for cs in product(*map(colors, path)):
                walk = (a, *cs)
                if all(x != y for x, y in zip(walk, walk[1:])):
                    available |= 1 << walk[-1]
            assert available == state[a]
            record('arm_tuple_rows', [state, path, a, available])
    interfaces = {'distinct': set(), 'same': set()}
    for palette in PAIRS:
        complement = U ^ palette
        for n in (3, 5, 7, 9):
            for state in sorted(paths):
                intrinsic = roots([U] + [palette] * (n - 1))
                assert intrinsic == complement
                actual = conditioned([U] + [palette] * (n - 1), 0, state)
                expected = tuple(complement & ~singleton(m) for m in state)
                assert actual == expected
                assert actual == conditioned([U, palette, palette], 0, state)
                record('same_four_rows', [palette, n, state, actual])
                if actual[D].bit_count() == 1:
                    interfaces['same'].add(actual)
                for c, d in product(colors(complement), repeat=2):
                    if state[D] != 1 << d:
                        continue
                    for pos in range(1, n):
                        lists = [palette] * n
                        lists[0], lists[pos] = palette | (1 << c), palette | (1 << d)
                        actual = conditioned(lists, pos, state)
                        expected = tuple(1 << c if a == D else lists[0] for a in range(4))
                        assert actual == expected
                        assert actual == conditioned([lists[0], lists[pos], palette], 1, state)
                        interfaces['distinct'].add(actual)
                        record('distinct_four_rows', [palette, n, pos, c, d, state, actual])

    # Join every obstruction-compatible side profile against every other side
    # profile through the entire finite closure of pair-list bridge transfers.
    # A direct bridge is the identity transfer followed by inequality.
    all_interfaces = sorted(interfaces['distinct'] | interfaces['same'])
    def join(left, right, transfer):
        rejected = []
        for a in range(4):
            message = 0
            for c in colors(left[a]):
                message |= transfer[c]
            rejected.append(not any(message & ~(1 << c) for c in colors(right[a])))
        return rejected
    forbiddens = Counter()
    double_rejection = None
    for left, right, transfer in product(all_interfaces, all_interfaces, sorted(paths)):
        rejected = join(left, right, transfer)
        forbiddens[sum(1 << a for a, bad in enumerate(rejected) if bad)] += 1
        if rejected[D] and sum(rejected) > 1 and double_rejection is None:
            double_rejection = dict(left_rows=left, right_rows=right,
                                    bridge_pair_path=paths[transfer],
                                    forbidden_colors=[a for a in range(4) if rejected[a]])
        record('coupled_four_rows', [left, right, transfer, rejected])

    # Nonuniform private lists really give a triple intrinsic root set, and an
    # arbitrary retained triangle changes it. This is outside D rigidity.
    general = [U, 3, 3, 5, 5]
    reduced = [U, 3, 5]
    assert roots(general) == 14 and roots(reduced) == U
    # Same-point four rows are not the distinct-point {c}/triple formula.
    state = (1, 2, 4, 8)  # zero-length external arm
    same = conditioned([U, 3, 3, 3, 3], 0, state)
    assert same == (12, 12, 8, 4)
    # Arbitrary pinning is stronger than the conditional interface queries.
    pinning = [4, 3, 4, 3, 3]
    assert roots(pinning) == 4 and roots([4, 4, 3]) == 0
    return dict(
        schema=1,
        scope='Fixed-q four-row list root interfaces for disjoint long odd cycle plus triangle; no source minor or topology certificate.',
        source_sha256={str(Path(__file__).relative_to(ROOT)): sha256(Path(__file__).read_bytes()).hexdigest()},
        summary=dict(counts, arm_profiles=len(paths),
                     distinct_interfaces=len(interfaces['distinct']), same_interfaces=len(interfaces['same']),
                     coupled_forbidden_masks={str(k): v for k, v in sorted(forbiddens.items())}),
        query_sha256=digest.hexdigest(),
        arm_profiles=[dict(rows=s, pair_path=paths[s]) for s in sorted(paths)],
        interfaces={k: sorted(v) for k, v in interfaces.items()},
        negative_controls=dict(
            coupled_double_rejection=double_rejection,
            nonuniform_triple=dict(source_lists=general, source_roots=roots(general),
                                   retained_positions=[0, 1, 3], triangle_lists=reduced, triangle_roots=roots(reduced)),
            same_point=dict(palette=3, arm_rows=state, root_rows=same),
            pinning=dict(source_lists=pinning, source_roots=4, triangle_lists=[4, 4, 3], triangle_roots=0)))


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
