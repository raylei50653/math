#!/usr/bin/env python3
"""Exact remote-12 cut criterion on the fixed original H and a complete lift.

Finite control evidence only: the paper criterion is valid for arbitrary H,
but the supplied graphs do not establish general D16 exclusion.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C0 = (2, 3, 4, 7, 5, 6)
R20 = (0, 1, 2, 1, 2, 1)
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
S = {tuple(map(int, w)) for w in (
    '010201 010212 010213 010231 012012 012021 012102 012121 '
    '012123 012132 012301 012302 012312 012313 012321 012323'
).split()}
INNER = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 7),
         (1, 2), (1, 5), (1, 6), (1, 7))
PRIOR = 'audits/2026-10-30-three-step-separator-fibres-v2-19f2262'


def norm(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def components(adj, vertices):
    unseen = set(vertices)
    result = []
    while unseen:
        start = min(unseen)
        part = {start}
        queue = [start]
        for u in queue:
            for v in sorted((adj[u] & unseen) - part):
                part.add(v)
                queue.append(v)
        unseen -= part
        result.append(tuple(sorted(part)))
    return result


def fixed_lifts(vertices, edges):
    adj = adjacency(vertices, edges)
    f = dict(zip(C0, R20))
    remaining = tuple(v for v in vertices if v not in f)
    results = []
    def visit(i):
        if i == len(remaining):
            results.append(tuple(f[v] for v in vertices))
            return
        v = remaining[i]
        used = {f[u] for u in adj[v] if u in f}
        for c in range(4):
            if c not in used:
                f[v] = c
                visit(i + 1)
        f.pop(v, None)
    assert all(f[u] != f[v] for u, v in edges if u in f and v in f)
    visit(0)
    return sorted(results)


def boundary_cubes(f, adj):
    records = []
    for split in SPLITS:
        blocks = [(pair, block) for pair in split
                  for block in components(adj, [v for v in adj if f[v] in pair])
                  if set(block) & set(C0)]
        orbit = set()
        for bits in product((0, 1), repeat=len(blocks)):
            g = dict(f)
            for bit, (pair, block) in zip(bits, blocks):
                if bit:
                    for v in block:
                        g[v] = sum(pair) - g[v]
            orbit.add(tuple(g[v] for v in C0))
        records.append(dict(blocks=[dict(pair=pair, vertices=block) for pair, block in blocks],
                            literal_boundary_orbit=sorted(orbit),
                            contained_in_d16=all(norm(row) in S for row in orbit)))
    return records


def center_fibre(f):
    return [(x, y) for x, y in product(range(4), repeat=2)
            if all((f | {0: x, 1: y})[u] != (f | {0: x, 1: y})[v] for u, v in INNER)]


def general_cut_test(vertices, edges, f, move, target, terminals):
    adj = adjacency(vertices, edges)
    alpha = next(iter(set(move) & set(target)))
    gamma = next(iter(set(target) - set(move)))
    pair_comps = components(adj, [v for v in vertices if f[v] in move])
    fixed = [k for k in pair_comps if set(k) & set(C0)]
    remote = [k for k in pair_comps if not set(k) & set(C0)]
    fixed_vertices = {v for k in fixed for v in k}
    base = components(adj, [v for v in vertices if f[v] == gamma or
                            (f[v] == alpha and v in fixed_vertices)])
    owner = {v: i for i, k in enumerate(base) for v in k}
    hyper = [dict(vertex=v, remote_index=i, original_color=f[v],
                  base_neighbors=sorted({owner[u] for u in adj[v] if f[u] == gamma}))
             for i, k in enumerate(remote) for v in k]
    root, goal = map(owner.__getitem__, terminals)
    cuts = []
    if root != goal:
        free = [i for i in range(len(base)) if i not in (root, goal)]
        for bits in product((0, 1), repeat=len(free)):
            X = {root} | {i for i, bit in zip(free, bits) if bit}
            crossing = [set() for _ in remote]
            for h in hyper:
                pins = set(h['base_neighbors'])
                if pins & X and pins - X:
                    crossing[h['remote_index']].add(h['original_color'])
            mixed = [i for i, cs in enumerate(crossing) if len(cs) == 2]
            cuts.append(dict(root_side=sorted(X), crossing_colors=[sorted(cs) for cs in crossing],
                             unavoidable_remote_indices=mixed))
    orientations = []
    escape = None
    for bits in product((0, 1), repeat=len(remote)):
        g = dict(f)
        for bit, k in zip(bits, remote):
            if bit:
                for v in k:
                    g[v] = sum(move) - g[v]
        kroot = next(k for k in components(adj, [v for v in vertices if g[v] in target])
                     if terminals[0] in k)
        connected = terminals[1] in kroot
        orientations.append(dict(swap_bits=bits, root_target_component=kroot, connected=connected))
        if escape is None and not connected:
            h = dict(g)
            for v in kroot:
                h[v] = sum(target) - h[v]
            assert all(h[u] != h[v] for u, v in edges)
            fibre = center_fibre(h)
            assert fibre
            X = sorted({owner[v] for v in kroot if v in owner})
            assert any(c['root_side'] == X and not c['unavoidable_remote_indices'] for c in cuts)
            escape = dict(swap_bits=bits, intermediate=tuple(g[v] for v in vertices),
                          swapped_target_component=kroot, final=tuple(h[v] for v in vertices),
                          final_boundary=tuple(h[v] for v in C0), center_fibre=fibre, root_base_cut=X)
    robust = all(o['connected'] for o in orientations)
    assert robust == (root == goal or all(c['unavoidable_remote_indices'] for c in cuts))
    return dict(switching_pair=move, target_pair=target, terminals=terminals,
                shared_color=alpha, preserved_color=gamma,
                boundary_touching_move_components=fixed, remote_move_components=remote,
                base_components=base, stars=hyper, all_separating_cuts=cuts,
                all_remote_orientations=orientations, robust=robust, explicit_escape=escape)


def record_lift(vertices, edges, row):
    f = dict(zip(vertices, row))
    adj = adjacency(vertices, edges)
    pair_comps = components(adj, [v for v in vertices if f[v] in (1, 2)])
    B = next(k for k in pair_comps if 3 in k)
    assert set(B) & set(C0) == {3, 4, 7, 5, 6}
    remote = [k for k in pair_comps if k != B]
    base = components(adj, [v for v in vertices if f[v] == 0 or (f[v] == 2 and v in B)])
    owner = {v: i for i, block in enumerate(base) for v in block}
    hyperedges = [dict(vertex=v, remote_index=i, original_color=f[v],
                       base_neighbors=sorted({owner[u] for u in adj[v] if f[u] == 0}))
                  for i, k in enumerate(remote) for v in k]
    cut_tests = []
    for target in (4, 5):
        root, goal = owner[2], owner[target]
        tests = []
        if root != goal:
            free = [i for i in range(len(base)) if i not in (root, goal)]
            for bits in product((0, 1), repeat=len(free)):
                X = {root} | {i for i, bit in zip(free, bits) if bit}
                crossing = [set() for _ in remote]
                for hyper in hyperedges:
                    pins = set(hyper['base_neighbors'])
                    if pins & X and pins - X:
                        crossing[hyper['remote_index']].add(hyper['original_color'])
                mixed = [i for i, colors in enumerate(crossing) if colors == {1, 2}]
                tests.append(dict(root_side=sorted(X),
                                  crossing_colors=[sorted(cs) for cs in crossing],
                                  unavoidable_remote_indices=mixed))
        cut_tests.append(dict(target_vertex=target, root_base=root, target_base=goal,
                              all_separating_cuts=tests,
                              robust=(root == goal or all(t['unavoidable_remote_indices'] for t in tests))))
    orientations = []
    bad = None
    for bits in product((0, 1), repeat=len(remote)):
        g = dict(f)
        for bit, k in zip(bits, remote):
            if bit:
                for v in k:
                    g[v] = 3 - g[v]
        kz = next(k for k in components(adj, [v for v in vertices if g[v] in (0, 2)]) if 2 in k)
        reached = [t for t in (4, 5) if t in kz]
        orientations.append(dict(swap_bits=bits, z_02_component=kz, reached_targets=reached))
        if bad is None and len(reached) != 2:
            target = dict(g)
            for v in kz:
                target[v] = 2 - target[v]
            fibre = center_fibre(target)
            assert fibre
            assert norm(tuple(target[v] for v in C0)) not in S
            assert all(target[u] != target[v] for u, v in edges)
            missing = next(t for t in (4, 5) if t not in kz)
            # Reachable base components provide a corresponding separating cut.
            X = sorted({owner[v] for v in kz if v in owner})
            cut = next(t for t in cut_tests if t['target_vertex'] == missing)
            witness = next(t for t in cut['all_separating_cuts'] if t['root_side'] == X)
            assert not witness['unavoidable_remote_indices']
            bad = dict(swap_bits=bits, intermediate=tuple(g[v] for v in vertices),
                       swapped_z_02_component=kz, target=tuple(target[v] for v in vertices),
                       target_boundary=tuple(target[v] for v in C0),
                       complete_center_fibre=fibre, target_vertex_separated=missing,
                       root_base_cut=X)
    for test in cut_tests:
        assert test['robust'] == all(test['target_vertex'] in o['reached_targets'] for o in orientations)
    neighbor_i = [v for v in adj[2] & set(B) if f[v] == 2]
    neighbor_ii = [i for i, k in enumerate(remote) if {f[v] for v in adj[2] & set(k)} == {1, 2}]
    cubes = boundary_cubes(f, adj)
    family = [general_cut_test(vertices, edges, f, move, target, terminals)
              for target, terminals in (((0, 2), (2, 4)), ((0, 2), (2, 5)), ((2, 3), (4, 5)))
              for move in combinations(range(4), 2) if len(set(move) & set(target)) == 1]
    return dict(source=row, boundary_12_component=B, remote_12_components=remote,
                base_components=base, hyperedges=hyperedges,
                target_cut_tests=cut_tests, all_remote_orientations=orientations,
                neighbor_condition=bool(neighbor_i or neighbor_ii),
                global_robustness=all(t['robust'] for t in cut_tests),
                source_boundary_cubes=cubes,
                all_three_source_cubes_in_d16=all(t['contained_in_d16'] for t in cubes),
                explicit_escape=bad, all_cross_split_tests=family,
                all_cross_split_robustness=all(t['robust'] for t in family))


def build_case(path):
    prior = json.loads(path.read_text())
    vertices = prior['original_h_vertex_order']
    edges = prior['embedding']['h_edges']
    rows = fixed_lifts(vertices, edges)
    records = [record_lift(vertices, edges, row) for row in rows]
    counts = dict(fixed_literal_20_lifts=len(records),
                  neighbor_condition_pass=sum(r['neighbor_condition'] for r in records),
                  global_robustness_pass=sum(r['global_robustness'] for r in records),
                  neighbor_pass_global_fail=sum(r['neighbor_condition'] and not r['global_robustness'] for r in records),
                  all_three_source_cubes_pass=sum(r['all_three_source_cubes_in_d16'] for r in records),
                  cubes_pass_global_fail=sum(r['all_three_source_cubes_in_d16'] and not r['global_robustness'] for r in records),
                  cubes_pass_global_pass=sum(r['all_three_source_cubes_in_d16'] and r['global_robustness'] for r in records),
                  cubes_and_neighbor_pass=sum(r['all_three_source_cubes_in_d16'] and r['neighbor_condition'] for r in records),
                  cubes_and_neighbor_pass_global_fail=sum(r['all_three_source_cubes_in_d16'] and r['neighbor_condition'] and not r['global_robustness'] for r in records),
                  all_cross_split_robustness_pass=sum(r['all_cross_split_robustness'] for r in records),
                  prior_both_pass_cross_split_fail=sum(r['all_three_source_cubes_in_d16'] and r['neighbor_condition'] and not r['all_cross_split_robustness'] for r in records))
    return dict(name=prior['name'], original_vertex_order=vertices, h_edges=edges,
                input_path=str(path.relative_to(ROOT)), input_sha256=sha256(path.read_bytes()).hexdigest(),
                records=records, counts=counts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    cases = [build_case(ROOT / PRIOR / filename) for filename in (
        'radial-mindeg5-14.json', 'theta-violator-12.json', 'buffer-2step-19.json')]
    result = dict(schema='three-step-remote-cut-v1',
                  scope='Exact cut-versus-orientation criterion on finite named graphs; general D16 exclusion remains OPEN.',
                  original_cycle=C0, fixed_literal_row=R20, controls=cases)
    output = args.out_dir / 'results.json'
    output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    inputs = [Path(__file__), ROOT / 'scripts/four_color_three_step_remote_cut_replay.py',
              *(ROOT / c['input_path'] for c in cases)]
    manifest = dict(inputs={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
                    outputs={'results.json': sha256(output.read_bytes()).hexdigest()})
    (args.out_dir / 'verification.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps([dict(name=c['name'], **c['counts']) for c in cases], indent=2))


if __name__ == '__main__':
    main()
