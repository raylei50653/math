#!/usr/bin/env python3
"""Independent stdlib-only replay of the actual remote-cut certificate.

Imports no producer or repository solver. Uses union-find for connectivity and
dynamic saturation for the complete fixed-boundary coloring enumeration.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

C0 = (2, 3, 4, 7, 5, 6)
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
D16 = {tuple(map(int, w)) for w in (
    '010201 010212 010213 010231 012012 012021 012102 012121 '
    '012123 012132 012301 012302 012312 012313 012321 012323').split()}
INNER = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 7),
         (1, 2), (1, 5), (1, 6), (1, 7))


def normalize(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def partitions(vertices, edges):
    parent = {v: v for v in vertices}
    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for u, v in edges:
        if u in parent and v in parent:
            parent[root(u)] = root(v)
    groups = {}
    for v in parent:
        groups.setdefault(root(v), []).append(v)
    return sorted(tuple(sorted(g)) for g in groups.values())


def enumerate_complete(vertices, edges):
    neighbors = {v: set() for v in vertices}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    f = dict(zip(C0, (0, 1, 2, 1, 2, 1)))
    results = set()
    def visit():
        if len(f) == len(vertices):
            results.add(tuple(f[v] for v in vertices))
            return
        v = max((v for v in vertices if v not in f),
                key=lambda v: (len({f[u] for u in neighbors[v] if u in f}), len(neighbors[v]), v))
        used = {f[u] for u in neighbors[v] if u in f}
        for c in (3, 2, 1, 0):
            if c not in used:
                f[v] = c
                visit()
        del f[v]
    visit()
    return results


def center_rows(f):
    result = []
    for x in range(4):
        for y in range(4):
            g = f | {0: x, 1: y}
            if all(g[u] != g[v] for u, v in INNER):
                result.append([x, y])
    return result


def check_general_test(saved, f, vertices, edges, move, target_pair, terminals):
    alpha = next(iter(set(move) & set(target_pair)))
    gamma = next(iter(set(target_pair) - set(move)))
    parts = partitions([v for v in vertices if f[v] in move], edges)
    fixed = [k for k in parts if set(k) & set(C0)]
    remote = [k for k in parts if not set(k) & set(C0)]
    fixed_vertices = set(v for k in fixed for v in k)
    base = partitions([v for v in vertices if f[v] == gamma or
                       (f[v] == alpha and v in fixed_vertices)], edges)
    owner = {v: i for i, k in enumerate(base) for v in k}
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)} for v in vertices}
    stars = [dict(vertex=v, remote_index=i, original_color=f[v],
                  base_neighbors=sorted({owner[u] for u in neighbors[v] if f[u] == gamma}))
             for i, k in enumerate(remote) for v in k]
    assert saved['switching_pair'] == list(move)
    assert saved['target_pair'] == list(target_pair)
    assert saved['terminals'] == list(terminals)
    assert saved['shared_color'] == alpha and saved['preserved_color'] == gamma
    assert saved['boundary_touching_move_components'] == list(map(list, fixed))
    assert saved['remote_move_components'] == list(map(list, remote))
    assert saved['base_components'] == list(map(list, base))
    assert saved['stars'] == stars
    root, goal = map(owner.__getitem__, terminals)
    cuts = {tuple(c['root_side']): c for c in saved['all_separating_cuts']}
    assert len(cuts) == len(saved['all_separating_cuts'])
    cut_robust = True
    expected_cuts = set()
    for mask in range(1 << len(base)):
        X = {i for i in range(len(base)) if mask >> i & 1}
        if root not in X or goal in X:
            continue
        expected_cuts.add(tuple(sorted(X)))
        crossing = [set() for _ in remote]
        for h in stars:
            pins = set(h['base_neighbors'])
            if pins & X and pins - X:
                crossing[h['remote_index']].add(h['original_color'])
        mixed = [i for i, cs in enumerate(crossing) if len(cs) == 2]
        item = cuts[tuple(sorted(X))]
        assert item['crossing_colors'] == [sorted(cs) for cs in crossing]
        assert item['unavoidable_remote_indices'] == mixed
        cut_robust &= bool(mixed)
        if not mixed:
            bits = tuple(int(alpha in cs) for cs in crossing)
            g = dict(f)
            for bit, k in zip(bits, remote):
                if bit:
                    for v in k:
                        g[v] = sum(move) - g[v]
            root_comp = next(k for k in partitions([v for v in vertices if g[v] in target_pair], edges)
                             if terminals[0] in k)
            assert terminals[1] not in root_comp
    assert expected_cuts == set(cuts)
    orientations = []
    first_bad = None
    for bits in product((0, 1), repeat=len(remote)):
        g = dict(f)
        for bit, k in zip(bits, remote):
            if bit:
                for v in k:
                    g[v] = sum(move) - g[v]
        assert tuple(g[v] for v in C0) == (0, 1, 2, 1, 2, 1)
        assert all(g[u] != g[v] for u, v in edges)
        root_comp = next(k for k in partitions([v for v in vertices if g[v] in target_pair], edges)
                         if terminals[0] in k)
        connected = terminals[1] in root_comp
        orientations.append(dict(swap_bits=list(bits), root_target_component=list(root_comp), connected=connected))
        if first_bad is None and not connected:
            first_bad = (bits, g, root_comp)
    assert saved['all_remote_orientations'] == orientations
    switch_robust = all(o['connected'] for o in orientations)
    assert switch_robust == cut_robust == saved['robust']
    escape = saved['explicit_escape']
    if first_bad is None:
        assert escape is None
    else:
        bits, g, root_comp = first_bad
        target = dict(g)
        for v in root_comp:
            target[v] = sum(target_pair) - target[v]
        assert escape['swap_bits'] == list(bits)
        assert escape['intermediate'] == [g[v] for v in vertices]
        assert escape['swapped_target_component'] == list(root_comp)
        assert escape['final'] == [target[v] for v in vertices]
        assert escape['final_boundary'] == [target[v] for v in C0]
        assert escape['center_fibre'] == center_rows(target)
        assert escape['center_fibre']
        assert all(target[u] != target[v] for u, v in edges)
        assert escape['root_base_cut'] == sorted({owner[v] for v in root_comp if v in owner})
    return switch_robust


def check_record(record, vertices, edges):
    f = dict(zip(vertices, record['source']))
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)} for v in vertices}
    def comps(g, pair):
        return partitions([v for v in vertices if g[v] in pair], edges)
    bparts = comps(f, (1, 2))
    B = next(k for k in bparts if 3 in k)
    remote = [k for k in bparts if k != B]
    assert record['boundary_12_component'] == list(B)
    assert record['remote_12_components'] == list(map(list, remote))
    base = partitions([v for v in vertices if f[v] == 0 or (f[v] == 2 and v in B)], edges)
    assert record['base_components'] == list(map(list, base))
    owner = {v: i for i, k in enumerate(base) for v in k}
    hyper = [dict(vertex=v, remote_index=i, original_color=f[v],
                  base_neighbors=sorted({owner[u] for u in neighbors[v] if f[u] == 0}))
             for i, k in enumerate(remote) for v in k]
    assert hyper == record['hyperedges']
    cube_good = True
    for split, saved in zip(SPLITS, record['source_boundary_cubes']):
        blocks = [(pair, k) for pair in split for k in comps(f, pair) if set(k) & set(C0)]
        assert saved['blocks'] == [dict(pair=list(pair), vertices=list(k)) for pair, k in blocks]
        orbit = set()
        for bits in product((0, 1), repeat=len(blocks)):
            g = dict(f)
            for bit, (pair, k) in zip(bits, blocks):
                if bit:
                    for v in k:
                        g[v] = sum(pair) - g[v]
            orbit.add(tuple(g[v] for v in C0))
        good = all(normalize(r) in D16 for r in orbit)
        assert saved['literal_boundary_orbit'] == list(map(list, sorted(orbit)))
        assert good == saved['contained_in_d16']
        cube_good &= good
    assert len(record['source_boundary_cubes']) == 3
    assert record['all_three_source_cubes_in_d16'] == cube_good
    robust_by_switches = {4: True, 5: True}
    orientation_records = []
    first_bad = None
    for bits in product((0, 1), repeat=len(remote)):
        g = dict(f)
        for bit, k in zip(bits, remote):
            if bit:
                for v in k:
                    g[v] = 3 - g[v]
        assert all(g[u] != g[v] for u, v in edges)
        kz = next(k for k in comps(g, (0, 2)) if 2 in k)
        reached = [t for t in (4, 5) if t in kz]
        orientation_records.append(dict(swap_bits=list(bits), z_02_component=list(kz), reached_targets=reached))
        for t in (4, 5):
            robust_by_switches[t] &= t in kz
        if first_bad is None and len(reached) < 2:
            first_bad = (bits, g, kz)
    assert record['all_remote_orientations'] == orientation_records
    for t, test in zip((4, 5), record['target_cut_tests']):
        root, goal = owner[2], owner[t]
        assert test['target_vertex'] == t and test['root_base'] == root and test['target_base'] == goal
        saved = {tuple(s['root_side']): s for s in test['all_separating_cuts']}
        assert len(saved) == len(test['all_separating_cuts'])
        expected = set()
        cut_good = True
        for mask in range(1 << len(base)):
            X = {i for i in range(len(base)) if mask >> i & 1}
            if root not in X or goal in X:
                continue
            expected.add(tuple(sorted(X)))
            crossing = [set() for _ in remote]
            for h in hyper:
                pins = set(h['base_neighbors'])
                if pins & X and pins - X:
                    crossing[h['remote_index']].add(h['original_color'])
            mixed = [i for i, cs in enumerate(crossing) if cs == {1, 2}]
            item = saved[tuple(sorted(X))]
            assert item['crossing_colors'] == [sorted(cs) for cs in crossing]
            assert item['unavoidable_remote_indices'] == mixed
            cut_good &= bool(mixed)
            if not mixed:
                # Independently construct the orientation disabling this cut.
                bits = tuple(int(2 in cs) for cs in crossing)
                g = dict(f)
                for bit, k in zip(bits, remote):
                    if bit:
                        for v in k:
                            g[v] = 3 - g[v]
                kz = next(k for k in comps(g, (0, 2)) if 2 in k)
                assert t not in kz
        assert expected == set(saved)
        assert test['robust'] == cut_good == robust_by_switches[t]
    assert len(record['target_cut_tests']) == 2
    global_good = all(robust_by_switches.values())
    assert record['global_robustness'] == global_good
    local = bool([v for v in neighbors[2] & set(B) if f[v] == 2]
                 or [k for k in remote if {f[v] for v in neighbors[2] & set(k)} == {1, 2}])
    assert record['neighbor_condition'] == local
    escape = record['explicit_escape']
    if first_bad is None:
        assert escape is None
    else:
        bits, g, kz = first_bad
        target = dict(g)
        for v in kz:
            target[v] = 2 - target[v]
        assert escape['swap_bits'] == list(bits)
        assert escape['intermediate'] == [g[v] for v in vertices]
        assert escape['swapped_z_02_component'] == list(kz)
        assert escape['target'] == [target[v] for v in vertices]
        assert escape['target_boundary'] == [target[v] for v in C0]
        assert escape['complete_center_fibre'] == center_rows(target)
        assert escape['complete_center_fibre']
        assert normalize(tuple(target[v] for v in C0)) not in D16
        assert all(target[u] != target[v] for u, v in edges)
        assert escape['target_vertex_separated'] == next(t for t in (4, 5) if t not in kz)
        assert escape['root_base_cut'] == sorted({owner[v] for v in kz if v in owner})
    tests = [(move, target, terminals)
             for target, terminals in (((0, 2), (2, 4)), ((0, 2), (2, 5)), ((2, 3), (4, 5)))
             for move in combinations(range(4), 2) if len(set(move) & set(target)) == 1]
    assert len(record['all_cross_split_tests']) == len(tests) == 12
    family_good = [check_general_test(saved, f, vertices, edges, *test)
                   for saved, test in zip(record['all_cross_split_tests'], tests)]
    assert record['all_cross_split_robustness'] == all(family_good)
    return local, global_good, cube_good, all(family_good)


def replay(path):
    result = json.loads(path.read_text())
    assert result['original_cycle'] == list(C0)
    assert result['fixed_literal_row'] == [0, 1, 2, 1, 2, 1]
    summaries = []
    for case in result['controls']:
        vertices, edges = case['original_vertex_order'], case['h_edges']
        expected = enumerate_complete(vertices, edges)
        actual = [tuple(r['source']) for r in case['records']]
        assert len(actual) == len(set(actual)) and set(actual) == expected
        checks = [check_record(r, vertices, edges) for r in case['records']]
        counts = dict(fixed_literal_20_lifts=len(checks), neighbor_condition_pass=sum(l for l, g, c, a in checks),
                      global_robustness_pass=sum(g for l, g, c, a in checks),
                      neighbor_pass_global_fail=sum(l and not g for l, g, c, a in checks),
                      all_three_source_cubes_pass=sum(c for l, g, c, a in checks),
                      cubes_pass_global_fail=sum(c and not g for l, g, c, a in checks),
                      cubes_pass_global_pass=sum(c and g for l, g, c, a in checks),
                      cubes_and_neighbor_pass=sum(c and l for l, g, c, a in checks),
                      cubes_and_neighbor_pass_global_fail=sum(c and l and not g for l, g, c, a in checks),
                      all_cross_split_robustness_pass=sum(a for l, g, c, a in checks),
                      prior_both_pass_cross_split_fail=sum(c and l and not a for l, g, c, a in checks))
        assert counts == case['counts']
        summaries.append(dict(name=case['name'], **counts))
    return dict(status='pass', results_sha256=sha256(path.read_bytes()).hexdigest(),
                independent_coloring_enumeration='dynamic saturation', independent_connectivity='union-find',
                all_cut_sets_and_all_remote_orientations_checked=True, controls=summaries,
                scope='Finite named graphs and exact criterion only; general D16 exclusion remains OPEN.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    rendered = json.dumps(replay(args.results), indent=2) + '\n'
    if args.out:
        args.out.write_text(rendered)
    print(rendered, end='')
