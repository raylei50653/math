#!/usr/bin/env python3
"""A true planar ear control passes twelve remote cubes but escapes in two splits.

This finite negative control does not realize D16.  It preserves the fixed
original two-center disk and certifies every initial complete split cube,
the actual dual reversal, fixed base02 paths immune to remote12 exchanges,
and the exact finite Kempe graph with a shortest literal escape.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import four_color_three_step_kempe_escape as escape

ROOT = Path(__file__).resolve().parents[1]
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def split_cubes(initial, all_components):
    result = []
    for split in SPLITS:
        components = [(pair, block) for pair in split
                      for block in all_components[escape.PAIRS.index(pair)]]
        targets = []
        for bits in product((False, True), repeat=len(components)):
            target = list(initial)
            for selected, (pair, block) in zip(bits, components):
                if selected:
                    for v in block:
                        target[v] = sum(pair) - target[v]
            targets.append(target)
            assert escape.normalize(escape.boundary(target)) in escape.D16
        result.append(dict(split=split,
                           components=[dict(pair=pair, vertices=[v + 2 for v in block])
                                       for pair, block in components],
                           all_subset_targets=targets))
    return result


def named_remote_tests(initial, edges):
    adjacency = escape.adjacency(len(initial), edges)
    comps = escape.components(initial, adjacency)
    boundary = {v - 2 for v in escape.CYCLE}
    records = []
    for target, terminals in (((0, 2), (2, 4)), ((0, 2), (2, 5)), ((2, 3), (4, 5))):
        for move in escape.PAIRS:
            if len(set(move) & set(target)) != 1:
                continue
            remote = [block for block in comps[escape.PAIRS.index(move)]
                      if not boundary.intersection(block)]
            orientations = []
            for bits in product((False, True), repeat=len(remote)):
                changed = list(initial)
                for selected, block in zip(bits, remote):
                    if selected:
                        for v in block:
                            changed[v] = sum(move) - changed[v]
                target_components = escape.components(changed, adjacency)[escape.PAIRS.index(target)]
                root_component = next(block for block in target_components if terminals[0] - 2 in block)
                orientations.append(dict(swap_bits=bits, coloring=changed,
                                         root_target_component=[v + 2 for v in root_component],
                                         connected=terminals[1] - 2 in root_component))
            assert all(o['connected'] for o in orientations)
            records.append(dict(switching_pair=move, target_pair=target, terminals=terminals,
                                remote_components=[[v + 2 for v in b] for b in remote],
                                all_orientations=orientations, robust=True))
    assert len(records) == 12
    return records


def make_certificate():
    import four_color_three_step_cross_split_exclusion as prior
    edges = tuple(sorted(set(prior.THETA12_H_EDGES) | {(3, 9), (5, 11), (6, 9)}))
    faces = []
    replacements = {
        (2, 3, 8, 9): ((2, 3, 9), (3, 8, 9)),
        (2, 9, 10, 6): ((2, 9, 6), (9, 10, 6)),
        (5, 10, 11, 7): ((5, 10, 11), (5, 11, 7)),
    }
    for face in prior.THETA12_G_FACES:
        faces.extend(replacements.get(face, (face,)))
    embedding = prior.verify_sphere_and_disk_embedding(12, edges, tuple(faces))
    initial = prior.THETA12_WITNESS_H
    record = escape.build_control('TRIANGULATED-EAR-GUARD-12', edges, initial)
    comp = escape.components(initial, escape.adjacency(10, edges))
    record['initial_complete_split_cubes'] = split_cubes(initial, comp)
    record['all_named_remote_tests'] = named_remote_tests(initial, edges)
    vertices = tuple(range(2, 12))
    r20_fibre = [row for row in prior.enumerate_colorings(vertices, edges)
                 if escape.boundary(row) == (0, 1, 2, 1, 2, 1)]
    assert len(r20_fibre) == 2
    record['complete_literal_r20_fibre'] = [
        dict(source=row, all_named_remote_tests=named_remote_tests(row, edges),
             complete_split_cubes=split_cubes(row, escape.components(row, escape.adjacency(10, edges))))
        for row in r20_fibre]
    record['embedding'] = embedding
    record['fixed_ear_cut'] = dict(path23=[4, 8, 9, 10, 5],
                                   target13_excursion=[8, 11, 10],
                                   source02_ear=[9, 11], source02_path=[2, 9, 11, 4],
                                   target13_path=[3, 8, 11, 10, 6],
                                   trapped01_component=[7, 11])
    record['remote12_robustness'] = dict(
        boundary12_component=[3, 4, 5, 6, 7, 9], remote12_components=[],
        base02_vertex_order=[2, 4, 5, 9, 11],
        base02_edges=[[2, 9], [4, 11], [5, 11], [9, 11]],
        fixed_z_to_b_path=[2, 9, 11, 4], fixed_z_to_c_path=[2, 9, 11, 5],
        all_base_vertices_in_one_component=True,
        scope='This initial lift only; not a property of every lift on this graph.')
    assert record['quotient_states'] == 40 and record['literal_colorings'] == 960
    assert record['shortest_literal_escape']['steps'] == 2
    return dict(schema='three-step-ear-guard-control-v1',
                claim='Finite true planar control: the entire literal r20 fibre passes all twelve named remote-connectivity cubes and all source D16 split cubes, but full D16 closure fails.',
                controls=[record])


def verify_embedding(record):
    """Direct face/dart/link check independent of the original embedding checker."""
    h_edges = {tuple(e) for e in record['edges']}
    center_edges = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 7),
                    (1, 2), (1, 5), (1, 6), (1, 7)}
    edges = h_edges | center_edges
    faces = record['embedding']['g_oriented_faces']
    assert len(faces) == 20 and all(len(f) == 3 for f in faces)
    darts = Counter((face[i], face[(i + 1) % len(face)])
                    for face in faces for i in range(len(face)))
    assert darts == Counter({e: 1 for a, b in edges for e in ((a, b), (b, a))})
    assert 12 - len(edges) + len(faces) == 2
    links = defaultdict(dict)
    for face in faces:
        for i, u in enumerate(face):
            assert face[i - 1] not in links[u]
            links[u][face[i - 1]] = face[(i + 1) % len(face)]
    rotation = {}
    for u, link in links.items():
        start = min(link)
        row = [start]
        while link[row[-1]] != start:
            assert link[row[-1]] not in row
            row.append(link[row[-1]])
        assert len(row) == len(link)
        rotation[u] = [v for v in row if v >= 2]
    found = []
    seen = set()
    for u, v in darts:
        if min(u, v) < 2 or (u, v) in seen:
            continue
        walk = []
        a, b = u, v
        while (a, b) not in seen:
            seen.add((a, b))
            walk.append(a)
            order = rotation[b]
            a, b = b, order[(order.index(a) + 1) % len(order)]
        found.append(walk)
    assert len(found) == 13
    assert 10 - len(h_edges) + len(found) == 2
    c0 = [f for f in found if len(f) == 6 and set(f) == set(escape.CYCLE)]
    assert len(c0) == 1
    c0 = c0[0]
    i = c0.index(2)
    assert tuple(c0[i:] + c0[:i]) in (escape.CYCLE, (2, 6, 5, 7, 4, 3))


def replay(data):
    graph_check = escape.replay(data)
    record = data['controls'][0]
    verify_embedding(record)
    initial = record['initial_coloring']
    edges = record['edges']
    comps = escape.replay_components(initial, edges)
    assert record['initial_complete_split_cubes'] == json.loads(json.dumps(split_cubes(initial, comps)))
    for cube in record['initial_complete_split_cubes']:
        for target in cube['all_subset_targets']:
            assert all(target[u - 2] != target[v - 2] for u, v in edges)
    tests = record['all_named_remote_tests']
    expected_tests = [(move, target, terminals)
                      for target, terminals in (((0, 2), (2, 4)), ((0, 2), (2, 5)), ((2, 3), (4, 5)))
                      for move in escape.PAIRS if len(set(move) & set(target)) == 1]
    assert len(tests) == len(expected_tests) == 12
    for test, (move, target, terminals) in zip(tests, expected_tests):
        assert test['switching_pair'] == list(move)
        assert test['target_pair'] == list(target) and test['terminals'] == list(terminals)
        remote = [block for block in comps[escape.PAIRS.index(move)]
                  if not {v + 2 for v in block}.intersection(escape.CYCLE)]
        assert test['remote_components'] == [[v + 2 for v in block] for block in remote]
        all_bits = list(product((False, True), repeat=len(remote)))
        assert len(test['all_orientations']) == len(all_bits)
        for orientation, bits in zip(test['all_orientations'], all_bits):
            assert orientation['swap_bits'] == list(bits)
            selected = {v for bit, block in zip(bits, remote) if bit for v in block}
            changed = [sum(move) - c if v in selected else c for v, c in enumerate(initial)]
            assert changed == orientation['coloring']
            assert escape.boundary(changed) == escape.boundary(initial)
            assert all(changed[u - 2] != changed[v - 2] for u, v in edges)
            target_components = escape.replay_components(changed, edges)[escape.PAIRS.index(target)]
            root_component = next(block for block in target_components if terminals[0] - 2 in block)
            assert orientation['root_target_component'] == [v + 2 for v in root_component]
            assert orientation['connected'] == (terminals[1] - 2 in root_component)
            assert orientation['connected']
        assert test['robust']
    fibre = record['complete_literal_r20_fibre']
    pinned = dict(zip(escape.CYCLE, (0, 1, 2, 1, 2, 1)))
    expected_fibre = []
    for private in product(range(4), repeat=4):
        f = pinned | dict(zip((8, 9, 10, 11), private))
        if all(f[u] != f[v] for u, v in edges):
            expected_fibre.append([f[v] for v in record['ordered_vertices']])
    assert len(fibre) == len(expected_fibre) == 2
    assert [entry['source'] for entry in fibre] == expected_fibre
    for entry in fibre:
        source = entry['source']
        source_comps = escape.replay_components(source, edges)
        assert entry['complete_split_cubes'] == json.loads(json.dumps(split_cubes(source, source_comps)))
        assert len(entry['all_named_remote_tests']) == 12
        for test, (move, target, terminals) in zip(entry['all_named_remote_tests'], expected_tests):
            assert test['switching_pair'] == list(move) and test['target_pair'] == list(target)
            assert test['terminals'] == list(terminals)
            remote = [block for block in source_comps[escape.PAIRS.index(move)]
                      if not set(v + 2 for v in block).intersection(escape.CYCLE)]
            assert test['remote_components'] == [[v + 2 for v in block] for block in remote]
            bits_family = list(product((False, True), repeat=len(remote)))
            assert len(test['all_orientations']) == len(bits_family)
            for row, bits in zip(test['all_orientations'], bits_family):
                assert row['swap_bits'] == list(bits)
                selected = {v for bit, block in zip(bits, remote) if bit for v in block}
                changed = [sum(move) - c if v in selected else c for v, c in enumerate(source)]
                assert row['coloring'] == changed
                assert escape.boundary(changed) == escape.boundary(source)
                assert all(changed[u - 2] != changed[v - 2] for u, v in edges)
                parts = escape.replay_components(changed, edges)[escape.PAIRS.index(target)]
                root = next(block for block in parts if terminals[0] - 2 in block)
                assert row['root_target_component'] == [v + 2 for v in root]
                assert row['connected'] == (terminals[1] - 2 in root)
                assert row['connected']
            assert test['robust']
    robust = record['remote12_robustness']
    b12 = next(block for block in comps[escape.PAIRS.index((1, 2))] if 1 in block)
    assert sorted(v + 2 for v in b12) == robust['boundary12_component']
    assert len(comps[escape.PAIRS.index((1, 2))]) == 1
    f = dict(zip(record['ordered_vertices'], initial))
    base = {v for v, color in f.items() if color == 0} | {v + 2 for v in b12 if initial[v] == 2}
    assert sorted(base) == robust['base02_vertex_order']
    base_edges = [e for e in edges if e[0] in base and e[1] in base]
    assert base_edges == robust['base02_edges']
    for key in ('fixed_z_to_b_path', 'fixed_z_to_c_path'):
        path = robust[key]
        assert path[0] == 2 and path[-1] == (4 if key.endswith('b_path') else 5)
        assert set(path) <= base
        assert all(sorted((u, v)) in base_edges for u, v in zip(path, path[1:]))
        assert all(f[v] in (0, 2) for v in path)
    cut = record['fixed_ear_cut']
    assert cut['path23'] == [4, 8, 9, 10, 5]
    assert all(f[v] in (2, 3) for v in cut['path23'])
    assert next([v + 2 for v in block] for block in comps[0] if 5 in block) == cut['trapped01_component']
    target = initial.copy()
    for v in cut['trapped01_component']:
        target[v - 2] = 1 - target[v - 2]
    target_comps = escape.replay_components(target, edges)
    z02 = next(block for block in comps[1] if 0 in block)
    z02_after = next(block for block in target_comps[1] if 0 in block)
    assert {2, 3} <= set(z02) and not ({2, 3} & set(z02_after))
    a13 = next(block for block in comps[4] if 1 in block)
    a13_after = next(block for block in target_comps[4] if 1 in block)
    assert 4 not in a13 and 4 in a13_after
    for key, coloring, pair in [('source02_path', initial, (0, 2)),
                                ('target13_path', target, (1, 3))]:
        path = cut[key]
        assert all(coloring[v - 2] in pair for v in path)
        assert all(sorted((u, v)) in edges for u, v in zip(path, path[1:]))
    return dict(passed=True, graph_check=graph_check,
                all_initial_split_cube_target_counts=[len(c['all_subset_targets'])
                                                     for c in record['initial_complete_split_cubes']],
                genus_zero_triangular_embedding_and_original_c0_checked=True,
                actual_dual_reversal_checked=True, fixed_base02_paths_checked=True,
                all_named_remote_tests_checked=len(tests),
                all_named_remote_orientations_checked=sum(len(t['all_orientations']) for t in tests),
                complete_literal_r20_fibre_checked=len(fibre),
                all_r20_fibre_lifts_pass_named_remote_tests=True,
                general_d16_exclusion='OPEN')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--replay', type=Path)
    args = parser.parse_args()
    if args.replay:
        print(json.dumps(replay(json.loads(args.replay.read_text())), indent=2))
        return
    if args.out_dir is None:
        parser.error('--out-dir or --replay required')
    args.out_dir.mkdir(parents=True, exist_ok=False)
    result = make_certificate()
    path = args.out_dir / 'results.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    names = ('four_color_three_step_ear_guard_control.py',
             'four_color_three_step_kempe_escape.py',
             'four_color_three_step_cross_split_exclusion.py')
    manifest = {str(Path('scripts') / n): sha256((ROOT / 'scripts' / n).read_bytes()).hexdigest()
                for n in names}
    manifest['results.json'] = sha256(path.read_bytes()).hexdigest()
    (args.out_dir / 'verification.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(result['controls'][0]['all_component_summary'], indent=2))


if __name__ == '__main__':
    main()
