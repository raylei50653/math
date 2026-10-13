#!/usr/bin/env python3
"""Independent direct verification: no import from the producing checker.

Enumerates noncrossing partitions of all seven boundary positions directly,
rebuilds transfers from literal collar adjacencies, and recolors every frozen
cap graph. The finite graph controls are distinct from the universal proof.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'frozen/audits/2026-10-12-neartri-complete-relation-reductions-5d70a399'


def canon(word):
    seen = []
    result = []
    for x in word:
        if x not in seen:
            seen.append(x)
        result.append(seen.index(x))
    return tuple(result)


def proper_patterns(n):
    return sorted(set(canon(x) for x in product(range(4), repeat=n)
                      if all(x[i] != x[(i+1) % n] for i in range(n))))


def parts(prefix=(0,)):
    if len(prefix) == 7:
        yield prefix
    else:
        for x in range(max(prefix)+2):
            yield from parts(prefix+(x,))


def independent_table(patterns):
    index = {p: i for i, p in enumerate(patterns)}
    nc = [q for q in parts() if not any(q[a] == q[c] and q[b] == q[d] and q[a] != q[b]
                                      for a, b, c, d in combinations(range(7), 4))]
    table = []
    for p in patterns:
        record = []
        for first in ((0, 1), (0, 2), (0, 3)):
            second = tuple(c for c in range(4) if c not in first)
            side = [0 if c in first else 1 for c in p]
            swap = dict((a, b) for pair in (first, second) for a, b in (pair, pair[::-1]))
            orbits = set()
            for q in nc:
                if any(q[i] == q[j] and side[i] != side[j] for i, j in combinations(range(7), 2)):
                    continue
                if any(side[i] == side[(i+1) % 7] and q[i] != q[(i+1) % 7] for i in range(7)):
                    continue
                orbit = set()
                for toggles in product((False, True), repeat=max(q)+1):
                    changed = canon(swap[c] if toggles[q[i]] else c for i, c in enumerate(p))
                    orbit.add(index[changed])
                orbits.add(frozenset(orbit))
            record.append(orbits)
        table.append(record)
    return table


def greatest_fixed(allowed, table):
    current = set(allowed)
    while True:
        revised = {i for i in current if all(any(o <= current for o in options)
                                           for options in table[i])}
        if revised == current:
            return current
        current = revised


def mask(values):
    return sum(2**i for i in values)


def bits(value, n=91):
    return {i for i in range(n) if value & 2**i}


def literal_cap_relation(n, edges, patterns):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    accepted = []
    for pi, row in enumerate(patterns):
        if any(row[u] == row[v] for u, v in edges if u < 7 and v < 7):
            continue
        colors = list(row) + [-1] * (n-7)
        def extend(uncolored):
            if not uncolored:
                return True
            choices = [(set(range(4)) - {colors[w] for w in adj[v]}, v) for v in uncolored]
            available, v = min(choices, key=lambda item: (len(item[0]), item[1]))
            for c in available:
                colors[v] = c
                if extend(uncolored - {v}):
                    colors[v] = -1
                    return True
            colors[v] = -1
            return False
        if extend(set(range(7, n))):
            accepted.append(pi)
    return mask(accepted)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--skip-literal-caps', action='store_true', help='For deliberate corruption probes only.')
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    old = json.loads((BASE / 'collar_certificate.json').read_text())
    caps = json.loads((HERE / 'frozen/cap_probe.json').read_text())
    for name, digest in certificate['input_sha256'].items():
        assert sha256((HERE.parent / name).read_bytes()).hexdigest() == digest, 'input hash'
    patterns = proper_patterns(7)
    assert [list(p) for p in patterns] == certificate['inner_pattern_order']
    table = independent_table(patterns)
    assert [[[mask(o) for o in sorted(options, key=mask)] for options in row] for row in table] == old['kempe_obligations']['7'], 'Kempe table'
    # Original names: u0=a0, u1=a1, u2=extra at b2, u3=a2,
    # u4=a3, u5=extra at b4, u6=a4; never rotate or reflect.
    supports = [(0, 1), (1, 2), (2,), (2, 3), (3, 4), (4,), (4, 0)]
    outer_patterns = proper_patterns(5)
    case = next(c for c in old['cases'] if c['boundary_extras'] == [0, 0, 1, 0, 1])
    columns = []
    full_lifts = []
    for row in patterns:
        lifts = [b for b in product(range(4), repeat=5)
                 if all(b[i] != b[(i+1) % 5] for i in range(5))
                 and all(row[j] != b[i] for j, at in enumerate(supports) for i in at)]
        columns.append({outer_patterns.index(canon(b)) for b in lifts})
        full_lifts.append([list(b) for b in lifts])
    assert [mask(x) for x in columns] == case['column_masks']
    assert full_lifts == case['outer_lifts_for_each_named_inner_row'], 'complete lifts'
    upper = bits(certificate['upper_mask'])
    target = bits(941, 10)
    def outer(selected):
        return set().union(*(columns[i] for i in selected))
    assert len(upper) == 55 and greatest_fixed(upper, table) == upper
    mandatory = {i for i in upper if outer(greatest_fixed(upper - {i}, table)) != target}
    assert mandatory == set(certificate['mandatory_indices']) and len(mandatory) == 45
    optional = sorted(upper - mandatory)
    assert optional == certificate['optional_indices']
    completions = []
    checks = []
    for selected in product((False, True), repeat=10):
        chosen = mandatory | {i for i, include in zip(optional, selected) if include}
        if greatest_fixed(chosen, table) == chosen and outer(chosen) == target:
            completions.append(mask(chosen))
    assert set(completions) == {r['mask'] for r in certificate['residuals']} and len(completions) == 72
    assert min(m.bit_count() for m in completions) == 47
    for r in certificate['residuals']:
        chosen = bits(r['mask'])
        assert r['accepted_indices'] == sorted(chosen)
        assert r['rejected_indices'] == sorted(set(range(91)) - chosen)
        for i, witness in zip(r['accepted_indices'], r['kempe_orbit_witnesses']):
            for s, orbit in enumerate(witness):
                assert frozenset(bits(orbit)) in table[i][s] and bits(orbit) <= chosen
    concise = certificate['row42_forcing']
    assert concise['forced_inner_index'] == 42 and concise['forced_inner_word'] == '0120231'
    assert concise['inner_preimages'] == sorted(i for i in upper if 9 in columns[i]) == [6, 58, 89]
    for entry in concise['implications']:
        possible = [o for o in table[entry['row']][entry['split']] if o <= upper]
        assert len(possible) == 1 and entry['forced'] in possible[0]
        assert mask(possible[0]) == entry['unique_allowed_orbit']
    for start in concise['inner_preimages']:
        reached = {start}
        while True:
            more = reached | {e['forced'] for e in concise['implications'] if e['row'] in reached}
            if more == reached:
                break
            reached = more
        assert 42 in reached, ('missing implication path to row42', start)
    cap_masks = sorted(map(int, caps['relations']))
    assert cap_masks == certificate['cap_mask_order'] and len(cap_masks) == 3383
    for minimal, hit_vector in zip(certificate['minimal_masks'], certificate['minimal_mask_cap_hit_indices']):
        for cap, row in zip(cap_masks, hit_vector):
            assert minimal & 2**row and cap & 2**row
    assert all(any(m & c == m for m in certificate['minimal_masks']) for c in completions)
    if not args.skip_literal_caps:
        for claimed, graph in caps['relations'].items():
            actual = literal_cap_relation(graph['actual_cap_vertex_count'], graph['actual_cap_edges'], patterns)
            assert actual == int(claimed), ('literal cap mismatch', claimed, actual)
    result = dict(status='PASS', independent_Kempe_rows=91, independent_Kempe_splits=273,
                  full_outer_lift_rows=91, mandatory_rows=45, exact_residual_count=72,
                  cardinality_lower_bound=47, row42_forcing='verified',
                  literal_cap_graphs=0 if args.skip_literal_caps else 3383,
                  literal_cap_row_queries=0 if args.skip_literal_caps else 3383*91,
                  source_status='not triggered')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
