#!/usr/bin/env python3
"""Exclude t=1, (2,1,1,1) by fixed original supports and literal row profiles.

This checks a finite necessary domain and full six-port gluing.  It does not
enumerate source graphs, assert disk realizability, or formalize the paper proof.
"""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U, normalize
from c5_excess_two_three_unary import orbit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_binary_three_unary/observations.json'
COLORS = tuple(range(4))
SINGLETONS = tuple(i for i, b in enumerate(ROWS) if len(set(b)) == 3)


def invariant_sets(seen, capacity):
    stabilizers = [p for p in permutations(COLORS) if all(p[c] == c for c in seen)]
    return [tuple(a) for n in range(capacity + 1) for a in combinations(COLORS, n)
            if all({p[c] for c in a} == set(a) for p in stabilizers)]


def transport(base, values, forbidden):
    maps = [p for p in permutations(COLORS)
            if all(p[a] == b for a, b in zip(base, values))]
    assert maps
    answers = {tuple(sorted(p[c] for c in forbidden)) for p in maps}
    assert len(answers) == 1
    return answers.pop()


def gluing_controls():
    pairs = tuple(product(COLORS, repeat=2))
    domains = [tuple(c for c in COLORS if bits >> c & 1) for bits in range(1, 16)]
    digest = sha256()
    checked = 0

    def check(relation, unary):
        nonlocal checked
        tuples = tuple((a, x, y, u, v, w) for a in COLORS for x, y in relation
                       for u, v, w in product(*unary) if a not in (x, y, u, v, w))
        # Independently assemble a union of singleton binary-relation joins.
        lifted = tuple(sorted({(a, x, y, *uv) for x, y in relation
                               for uv in product(*unary)
                               for a in U - {x, y} - set(uv)}))
        assert tuples == lifted
        forbidden = set.intersection(*(set(p) for p in relation))
        forbidden |= set().union(*(set(s) if len(s) == 1 else set() for s in unary))
        assert {t[0] for t in tuples} == U - forbidden
        # Any actual spoke is a further literal root restriction.
        for color in COLORS:
            joined = tuple(t for t in tuples if t[0] != color)
            assert {t[0] for t in joined} == U - forbidden - {color}
        digest.update(json.dumps([relation, unary, tuples], separators=(',', ':')).encode())
        checked += 1

    for pair in pairs:
        for unary in product(domains, repeat=3):
            check((pair,), unary)
    for relation in combinations(pairs, 2):
        for colors in product(COLORS, repeat=3):
            check(relation, tuple((c,) for c in colors))
    return dict(singleton_binary_all_unary_domains=16 * 15**3,
                two_tuple_binary_singleton_unary_domains=120 * 4**3,
                full_six_port_checks=checked, spoke_restrictions=4 * checked,
                tuples_sha256=digest.hexdigest())


def build():
    targets = {str(mask): orbit(mask) for mask in (933, 941)}
    target_set = set().union(*(set(v) for v in targets.values()))
    span_cases = [spans for spans in product(range(1, 6), repeat=4) if sum(spans) <= 5]
    assert len(span_cases) == 5
    edge_sets = invariant_sets({0, 1}, 2)
    short_sets = [f for f in edge_sets if len(f) <= 1]
    assert short_sets == [(), (0,), (1,)]
    assert not [f for f in invariant_sets(set(), 2) if f]
    assert invariant_sets({0}, 2) == [(), (0,)]
    local_patterns = ((0, 1, 0), (0, 1, 2))
    choices = [invariant_sets(set(row), 2) for row in local_patterns]
    assert list(map(len, choices)) == [5, 11]
    profiles = []
    comparisons = []
    for forbidden_by_pattern in product(*choices):
        profile = []
        for row in ROWS:
            values = row[:3]
            shape = normalize(values)
            index = local_patterns.index(shape)
            profile.append(transport(local_patterns[index], values, forbidden_by_pattern[index]))
        pid = len(profiles)
        profiles.append(dict(id=pid, forbidden_by_local_pattern=forbidden_by_pattern,
                             literal_ten_row_forbidden=profile))
        # Preserve the three original unary identities in their common cyclic order.
        for endpoints in product((0, 1), repeat=3):
            selected = tuple(edge[side] for edge, side in
                             zip(((2, 3), (3, 4), (4, 0)), endpoints))
            for spoke in range(5):
                mask = sum(1 << i for i, row in enumerate(ROWS)
                           if U - {row[spoke]} - {row[j] for j in selected} - set(profile[i]))
                assert mask not in target_set, (pid, selected, spoke, mask)
                comparisons.append(dict(profile_id=pid, unary_endpoint_sides=endpoints,
                                        original_unary_selected_boundary=selected,
                                        spoke=spoke, resulting_mask=mask))
    assert len(profiles) == 55 and len(comparisons) == 2200
    # If a unary owns the sole length-two envelope, all rejected rows must be
    # rainbow on that one fixed envelope.  No row-specific choice of arc occurs.
    unary_long = []
    for target in sorted(target_set):
        for start in range(5):
            arc = tuple((start + j) % 5 for j in range(3))
            misses = [i for i in SINGLETONS if not target >> i & 1
                      and len({ROWS[i][j] for j in arc}) < 3]
            assert misses
            unary_long.append(dict(target=target, fixed_unary_envelope=arc,
                                   rejected_rows_missing_third_color=misses))
    gluing = gluing_controls()
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_excess_two_three_unary.py']
    return dict(schema=1, scope='t=1 original (2,1,1,1) complete-source exclusion',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in paths}, pattern_order=ROWS, target_orbits=targets,
                original_component_order=['A_binary', 'U0', 'U1', 'U2'],
                ordered_ports=['r', 'A_x', 'A_y', 'U0_u', 'U1_v', 'U2_w'],
                positive_span_cases=span_cases,
                short_edge_invariant_sets_before_pair_exclusion=edge_sets,
                short_edge_invariant_sets_after_pair_exclusion=short_sets,
                local_binary_envelope=[0, 1, 2], local_patterns=local_patterns,
                local_profile_choices=choices, binary_profiles=profiles,
                binary_long_comparisons=comparisons, unary_long_exclusions=unary_long,
                gluing_controls=gluing,
                paper_dependencies=['original component slack and literal complete gluing',
                    'edge-minimal private-factor witness and tight degree lists',
                    'connected-exterior K4 exclusion and common-root support lifts',
                    'binary pair original bridge path and original-path frame-arc K5'],
                summary=dict(positive_span_cases=len(span_cases), binary_profiles=len(profiles),
                    binary_long_comparisons=len(comparisons), unary_long_comparisons=len(unary_long),
                    remaining=0, full_six_port_checks=gluing['full_six_port_checks'],
                    graph_enumeration=False, disk_realizability_claimed=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
