#!/usr/bin/env python3
"""Finite parity calibration only; no hypothetical source enumeration."""
import argparse
import itertools
import json
import random

T = ('m', 'z', 'v', 'w', 'p', 'q')
P = frozenset(T[2:])
MARKS = {'e': {'v', 'w'}, 'f': {'p', 'q'}, 'g': {'m', 'z'}}


def charge(odd):
    return 6 + ('m' in odd) - ('z' in odd) - len(odd & P) + len(odd - set(T))


def marked(names):
    result = set()
    for name in names:
        result ^= MARKS[name]
    return result


def odd_incidence(edges):
    result = set()
    for u, v in edges:
        result.symmetric_difference_update((u, v))
    return result


def run(seed):
    rng = random.Random(seed)
    masks = list(range(64))
    rng.shuffle(masks)
    assert charge(set()) == 6
    assert charge(marked('ef')) == 2
    assert charge(marked('eg')) == 4
    assert charge(marked('efg')) == 2
    pentagon_edges = [(i, (i + 1) % 5) for i in range(5)]
    for four in itertools.combinations(range(5), 4):
        assert sum(u in four and v in four for u, v in pentagon_edges) == 3
    for length in (5, 7):
        spokes = [('c', f'r{i}') for i in range(length)]
        assert odd_incidence(spokes) == {'c'} | {f'r{i}' for i in range(length)}

    one_counts = {}
    for family, force in (('110', 'ef'), ('101', 'eg')):
        for tau in (0, 1):
            base = marked('efg' if tau else force)
            best = -999
            count = 0
            for mask in masks:
                pins = {u for j, u in enumerate(T) if mask & (1 << j)}
                nfree = 6 - len(pins)
                if nfree < 1:  # The actual center lies outside T.
                    continue
                cap = pins | {f'u{j}' for j in range(nfree)}
                universe = list(T) + [f'u{j}' for j in range(nfree + 2)]
                extras = itertools.combinations(universe, 2) if tau else [()]
                for edge in extras:
                    q = charge(base ^ cap ^ set(edge))
                    best = max(best, q)
                    count += 1
                    assert q <= (8 if family == '110' and not tau else 10)
            one_counts[f'{family}_tau{tau}'] = {'states': count, 'max_charge': best}

    seven_best = -999
    for mask in masks:
        pins = {u for j, u in enumerate(T) if mask & (1 << j)}
        cap = pins | {f'u{j}' for j in range(8 - len(pins))}
        seven_best = max(seven_best, charge(marked('efg') ^ cap))
    assert seven_best == 10

    memberships = list(itertools.product(range(4), repeat=6))
    rng.shuffle(memberships)
    total = admitted = equality = one_slack = 0
    reject_bad_base = reject_bad_hub_sign = False
    for membership in memberships:
        pins1 = {u for u, x in zip(T, membership) if x & 1}
        pins2 = {u for u, x in zip(T, membership) if x & 2}
        free1, free2 = 6 - len(pins1), 6 - len(pins2)
        # Each cap needs a private unmarked center. Remaining unmarked
        # vertices are interchangeable for charge, hence this quotient is exact.
        for common_free in range(min(free1, free2)):
            common = {f'b{i}' for i in range(common_free)}
            k1 = pins1 | common | {f'a{i}' for i in range(free1 - common_free)}
            k2 = pins2 | common | {f'c{i}' for i in range(free2 - common_free)}
            assert len(k1) == len(k2) == 6
            r_cap = len(k1 & k2)
            epsilon = int('m' in (k1 ^ k2))
            q = charge(marked('efg') ^ k1 ^ k2)
            correct = 14 - 2*r_cap - 2*epsilon
            assert q == correct
            reject_bad_base |= q != 15 - 2*r_cap - 2*epsilon
            reject_bad_hub_sign |= q != 14 - 2*r_cap + 2*epsilon
            total += 1
            if q >= 12:
                admitted += 1
                assert r_cap + epsilon <= 1
                assert q - 12 == 2*(1-r_cap-epsilon)
                equality += q == 12
                one_slack += q == 14
    assert reject_bad_base and reject_bad_hub_sign
    return {
        'authority': 'finite six-pin parity quotient; paper theorem is arbitrary-size',
        'source_instances': 0,
        'source_tests': 'not triggered',
        'single_W5': one_counts,
        'single_W7_max_charge': seven_best,
        'two_W5': {'states': total, 'necessary_degree_admissible': admitted,
                   'zero_total_slack': equality, 'total_slack_two': one_slack},
        'negative_controls': {'wrong_constant_rejected': reject_bad_base,
                              'wrong_m_toggle_sign_rejected': reject_bad_hub_sign},
        'result': 'PASS',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(run(args.seed), indent=2, sort_keys=True))
