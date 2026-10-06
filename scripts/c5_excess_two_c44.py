#!/usr/bin/env python3
"""C44: all minimal literal rejected-row cores of the ES/ER k<=9 q domain.

See artifacts/c5_excess_two_c44/REPORT.md for definitions and completeness.
No topology/source lemmas prune this core search. Removing edges increases
acceptance; only accepted children are discarded. Low-degree peeling preserves
every extension decision and cannot remove a minimal core. One-pass <=1
monochromatic-edge colorings determine all edge deletions simultaneously.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from multiprocessing import get_context
from pathlib import Path
import time

from c5_kempe_screen import REPS
from c5_excess_two_independent_coloring import sigma_mask, find_extension

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_c44'
INPUT = ROOT / 'artifacts/c5_excess_two_independent_search'
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
SINGLETON = {6: 0, 4: 1, 3: 2, 1: 3, 0: 4}


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(',', ':')) + '\n').encode()


def emit(path, value, check=False):
    data = encode(value)
    if check:
        if path.read_bytes() != data:
            raise AssertionError(f'byte mismatch: {path}')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data),
            'sha256': sha256(data).hexdigest()}


def inputs(kmax=9, kmin=3):
    for kind in ('NA', 'AD', 'D6'):
        for k in range(kmin, kmax + 1):
            layer_path = INPUT / f'{kind}_k{k}.json'
            layer = json.loads(layer_path.read_bytes())
            assert layer['comparison']['consistent']
            count = 0
            for chunk in layer['q_orbit_chunks']:
                path = ROOT / chunk['path']
                data = path.read_bytes()
                assert sha256(data).hexdigest() == chunk['sha256']
                records = json.loads(data)['q_orbits']
                assert len(records) == chunk['orbits']
                for record in records:
                    count += 1
                    yield {'type': kind, 'k': k, 'source': chunk['path'],
                           'source_sha256': chunk['sha256'], 'record': record}
            assert count == len(layer['q_orbits'])


def peel(edges):
    """Greedy four-color extension makes degree<=3 private vertices irrelevant."""
    edges = frozenset(edges)
    while True:
        degree = Counter(v for edge in edges for v in edge)
        small = {v for v, d in degree.items() if v >= 5 and d < 4}
        if not small:
            return tuple(sorted(edges))
        edges = frozenset((a, b) for a, b in edges if a not in small and b not in small)


def one_pass(edges, row_index):
    """Exact decision and full witnesses for every single-edge deletion.

    Each assignment with one violated edge accepts precisely that deletion.
    A zero-violation assignment accepts the parent. No monochromatic edges
    incident to future vertices are counted until their second endpoint is set.
    """
    vertices = tuple(sorted({v for e in edges for v in e} | set(range(5))))
    adjacent = {v: [] for v in vertices}
    for i, (a, b) in enumerate(edges):
        adjacent[a].append((b, i))
        adjacent[b].append((a, i))
    colors = dict(enumerate(REPS[row_index]))
    witnesses = {}
    accepting = None

    def visit(bad):
        nonlocal accepting
        remaining = [v for v in vertices if v not in colors]
        if not remaining:
            coloring = tuple(colors[v] for v in vertices)
            if bad is None:
                accepting = coloring
                return True
            witnesses.setdefault(edges[bad], coloring)
            return False
        # Deterministic MRV only changes order, never the assignments visited.
        v = min(remaining, key=lambda u: (
            -len({colors[w] for w, _ in adjacent[u] if w in colors}),
            -len(adjacent[u]), u))
        for color in range(4):
            violations = [i for w, i in adjacent[v] if colors.get(w) == color]
            if len(violations) > (1 if bad is None else 0):
                continue
            colors[v] = color
            if visit(violations[0] if violations else bad):
                del colors[v]
                return True
            del colors[v]
        return False

    visit(None)
    return vertices, accepting, witnesses


def minimal_cores(edges, row_index):
    """Enumerate all minimal rejecting edge sets, retaining the literal frame."""
    seen, minimal = set(), {}
    initial = tuple(sorted(edges))
    original_profile = {}
    stats = Counter()

    def recurse(current):
        current = peel(current)
        if current in seen:
            return
        seen.add(current)
        vertices, accepting, witnesses = one_pass(current, row_index)
        if current == initial:
            original_profile.update(witnesses)
        stats['one_pass_states'] += 1
        if accepting is not None:
            stats['accepted_prunes'] += 1
            return
        children = {peel(set(current) - {edge})
                    for edge in current if edge not in FRAME and edge not in witnesses}
        stats['one_pass_deletion_decisions'] += len(current) - 5
        if children:
            for child in sorted(children):
                recurse(child)
        else:
            assert len(witnesses) == len(current) - 5
            minimal[current] = (vertices, witnesses)
    recurse(tuple(sorted(edges)))
    return minimal, stats, original_profile


def pieces(edges, roots):
    private = {v for e in edges for v in e if v >= 5} - set(roots)
    adjacent = {v: set() for v in private}
    for a, b in edges:
        if a in private and b in private:
            adjacent[a].add(b)
            adjacent[b].add(a)
    out = []
    while private:
        seed = min(private)
        component, todo = set(), [seed]
        while todo:
            v = todo.pop()
            if v not in component:
                component.add(v)
                todo.extend(adjacent[v] - component)
        private -= component
        owners = sorted(r for r in roots if any(
            (a == r and b in component) or (b == r and a in component)
            for a, b in edges))
        out.append({'vertices': sorted(component), 'owners': owners})
    return out


def core_record(edges, roots, vertices, witnesses):
    degree = Counter(v for e in edges for v in e)
    retained = tuple(v for v in vertices if v >= 5)
    original_pieces = pieces(edges, roots)
    assert all(degree[v] >= 4 for v in retained)
    root_degrees = [degree[r] if r in retained else None for r in roots]
    mask = sigma_mask(edges)
    return {'vertices': list(vertices), 'edges': list(edges),
            'root_degrees': root_degrees,
            'root_degree_type': '/'.join('absent' if d is None else str(d)
                                       for d in sorted(root_degrees, key=lambda x: -1 if x is None else x)),
            'private_size': len(retained), 'total_size': len(vertices),
            'nonframe_edges': len(edges) - 5, 'sigma_mask': mask,
            'mixed_components': [p for p in original_pieces if len(p['owners']) == 2],
            'contains_mixed_component': any(len(p['owners']) == 2 for p in original_pieces),
            'minimality_witnesses_checked': len(witnesses)}


def analyze(item):
    kind, k, source = item['type'], item['k'], item['record']
    roots = (5,) if kind == 'D6' else (5, 6)
    edges = tuple(map(tuple, source['canonical_edges']))
    assert sigma_mask(edges, n_vertices=k+5) == source['sigma_mask']
    rows, totals = [], Counter()
    deletion_masks = {e: source['sigma_mask'] for e in edges if e not in FRAME}
    for qi in sorted(i for i in range(10) if not source['sigma_mask'] >> i & 1):
        assert qi in SINGLETON
        found, stats, original_profile = minimal_cores(edges, qi)
        for edge in original_profile:
            deletion_masks[edge] |= 1 << qi
        totals.update(stats)
        assert found
        records = []
        for core, (vertices, witnesses) in sorted(found.items()):
            assert all(len(coloring) == len(vertices) for coloring in witnesses.values())
            for deleted, coloring in witnesses.items():
                assignment = dict(zip(vertices, coloring))
                assert tuple(assignment[i] for i in range(5)) == REPS[qi]
                assert all(assignment[a] != assignment[b] for a, b in core if (a, b) != deleted)
            data = core_record(core, roots, vertices, witnesses)
            assert not data['sigma_mask'] >> qi & 1
            totals['core_minimality_witnesses'] += len(witnesses)
            records.append(data)
        rows.append({'row_index': qi, 'literal_row': list(REPS[qi]),
                     'singleton_position': SINGLETON[qi], 'core_count': len(records),
                     'cores': records, 'search': dict(sorted(stats.items()))})
    assert deletion_masks == {tuple(d['edge']): d['sigma_mask'] for d in source['deletion_sigmas']}
    assert all(mask != source['sigma_mask'] for mask in deletion_masks.values()) == source['critical']
    totals['source_full_deletion_masks_checked'] = len(deletion_masks)
    return {'type': kind, 'k': k, 'code': source['code'],
            'source': item['source'], 'source_sha256': item['source_sha256'],
            'canonical_edges': list(edges), 'roots': list(roots),
            'sigma_mask': source['sigma_mask'], 'Q': source['Q'],
            'critical': source['critical'], 'orbit_size': source['orbit_size'],
            'stabilizer_size': source['stabilizer_size'], 'rows': rows,
            'search_totals': dict(sorted(totals.items()))}


def summary(records):
    out = {}
    for kind in ('NA', 'AD', 'D6'):
        population = [r for r in records if r['type'] == kind]
        by_pop = {}
        for pop in ('all_q', 'critical'):
            selected = [r for r in population if pop == 'all_q' or r['critical']]
            counts = Counter()
            joint = Counter()
            per_row = Counter()
            weighted = Counter()
            for graph in selected:
                for row in graph['rows']:
                    per_row[str(row['core_count'])] += 1
                    for core in row['cores']:
                        counts[core['root_degree_type']] += 1
                        joint[(core['root_degree_type'], core['private_size'],
                               core['contains_mixed_component'])] += 1
                        weighted[core['root_degree_type']] += graph['orbit_size']
            by_pop[pop] = {'orbits': len(selected), 'labelled_graphs': sum(g['orbit_size'] for g in selected),
                           'rejection_rows': sum(len(g['rows']) for g in selected),
                           'core_occurrences': sum(counts.values()),
                           'root_degree_types': dict(sorted(counts.items())),
                           'labelled_root_degree_types': dict(sorted(weighted.items())),
                           'cores_per_row': dict(sorted(per_row.items())),
                           'joint_degree_size_mixed': [
                               {'degree_type': d, 'private_size': size, 'mixed': mixed, 'count': n}
                               for (d, size, mixed), n in sorted(joint.items())]}
        out[kind] = by_pop
    return out


def brute_compare(records, check):
    from c5_excess_two_c44_brute import brute_all_rows
    comparisons = []
    for graph in records:
        if graph['k'] > 6:
            continue
        stats = {}
        expected = brute_all_rows(graph['k'], graph['canonical_edges'],
                                  [row['row_index'] for row in graph['rows']], stats=stats)
        unfiltered_stats = None
        if graph['k'] <= 5:
            unfiltered_stats = {}
            unfiltered = brute_all_rows(graph['k'], graph['canonical_edges'],
                                        [row['row_index'] for row in graph['rows']],
                                        degree_filter=False, stats=unfiltered_stats)
            assert unfiltered == expected
        per_row = []
        for row in graph['rows']:
            actual = sorted(tuple(map(tuple, core['edges'])) for core in row['cores'])
            assert actual == expected[row['row_index']], (graph['code'], row['row_index'])
            per_row.append({'row_index': row['row_index'], 'optimized_cores': actual,
                            'brute_cores': expected[row['row_index']], 'equal': True})
        comparisons.append({'type': graph['type'], 'k': graph['k'], 'code': graph['code'],
                            'rows': len(graph['rows']), 'core_counts': [r['core_count'] for r in graph['rows']],
                            'equal': True, 'brute': stats, 'per_row': per_row,
                            'unfiltered_brute_k_le_5': unfiltered_stats})
    data = {'method': 'independent exhaustive nonframe edge subsets + numeric DFS',
            'comparisons': comparisons,
            'stages': {label: {'orbits': len(part), 'rows': sum(g['rows'] for g in part),
                              'all_equal': all(g['equal'] for g in part)}
                       for label, part in [('k_le_5', [g for g in comparisons if g['k'] <= 5]),
                                           ('k_6', [g for g in comparisons if g['k'] == 6])]}}
    emit(OUT / 'brute_comparison.json', data, check)
    return data['stages']


def named_counterexample(records):
    from c5_excess_two_c44_input_audit import faces, mask_images
    candidates = [(graph['k'], graph['type'], graph['code'], row['row_index'], graph, row, core)
                  for graph in records for row in graph['rows'] for core in row['cores']
                  if core['root_degrees'] == [4, 4]]
    if not candidates:
        return None
    _, _, _, _, graph, row, core = min(candidates, key=lambda x: x[:4] +
                                                   (x[6]['private_size'], x[6]['edges']))
    source = next(g['record'] for g in inputs(graph['k'], graph['k']) if g['record']['code'] == graph['code'])
    edges = tuple(map(tuple, core['edges']))
    vertices = core['vertices']
    rotations = source['augmented_rotation']
    augmented_edges = set(edges) | {(i, graph['k'] + 5) for i in range(5)}
    core_rotation = {str(v): [w for w in rotations[str(v)] if tuple(sorted((v, w))) in augmented_edges]
                     for v in vertices + [graph['k'] + 5]}
    augmented_faces = faces({int(v): tuple(ns) for v, ns in core_rotation.items()})
    apex = graph['k'] + 5
    disk_faces = faces({int(v): tuple(w for w in ns if w != apex)
                        for v, ns in core_rotation.items() if int(v) != apex})
    assert len(vertices) + 1 - len(augmented_edges) + len(augmented_faces) == 2
    assert len(vertices) - len(edges) + len(disk_faces) == 2
    assert any(len(f) == 5 and set(f) == set(range(5)) for f in disk_faces)
    witnesses = []
    for edge in edges:
        if edge in FRAME:
            continue
        coloring = find_extension([e for e in edges if e != edge], row['row_index'],
                                  n_vertices=graph['k'] + 5)
        assert coloring is not None
        witnesses.append({'edge': edge, 'vertices': vertices,
                          'colouring': [coloring[v] for v in vertices]})
    # Exhaustive Cartesian evidence, independent of optimized one-pass search.
    accepted = 0
    private = [v for v in vertices if v >= 5]
    for colors in product(range(4), repeat=len(private)):
        assignment = dict(enumerate(REPS[row['row_index']])) | dict(zip(private, colors))
        accepted += all(assignment[a] != assignment[b] for a, b in edges)
    assert accepted == 0
    return {'name': f'C44-{graph["type"]}{graph["k"]}-row{row["row_index"]}-44', 'source_graph': graph,
            'source_augmented_rotation': source['augmented_rotation'],
            'source_deletion_sigmas': source['deletion_sigmas'],
            'rejection_row': {key: row[key] for key in ('row_index', 'literal_row', 'singleton_position')},
            'core': core, 'core_augmented_rotation': core_rotation,
            'core_augmented_faces': augmented_faces, 'core_disk_faces': disk_faces,
            'edge_deletion_witnesses': witnesses,
            'cartesian_rejection': {'assignments': 4**len(private), 'accepting': accepted},
            'target_full_sigma_hypothesis': graph['sigma_mask'] in set(mask_images(933) + mask_images(941))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', choices=('small', 'full'), default='full')
    parser.add_argument('--jobs', type=int, default=8)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.jobs <= 16:
        parser.error('jobs must lie in 1..16')
    start = time.monotonic()
    if args.stage == 'full':
        comparison = json.loads((OUT / 'brute_comparison.json').read_bytes())
        assert all(s['all_equal'] for s in comparison['stages'].values())
        assert comparison['stages']['k_6']['orbits'] > 0
    items = list(inputs(6 if args.stage == 'small' else 9))
    if args.jobs == 1:
        records = list(map(analyze, items))
    else:
        # Linux fork needs no forkserver listening socket in restricted runners.
        with get_context('fork').Pool(args.jobs) as pool:
            records = list(pool.imap(analyze, items, chunksize=8))
    records.sort(key=lambda r: (('NA', 'AD', 'D6').index(r['type']), r['k'], r['code']))
    if args.stage == 'small':
        stages = brute_compare(records, args.check)
        emit(OUT / 'small_summary.json', {'statistics': summary(records), 'brute_stages': stages}, args.check)
        print(f'SMALL PASS {len(records)} orbits; {stages}; seconds={time.monotonic()-start:.3f}', flush=True)
        return
    # Save compact full per-orbit/per-row records in chunks below 1 MB.
    manifests, batch, size, sequence = [], [], 0, 1
    for record in records:
        length = len(encode(record))
        if batch and size + length > 700_000:
            manifests.append(emit(OUT / 'orbits' / f'chunk_{sequence:04d}.json',
                                  {'orbits': batch}, args.check))
            sequence += 1
            batch, size = [], 0
        batch.append(record)
        size += length
    if batch:
        manifests.append(emit(OUT / 'orbits' / f'chunk_{sequence:04d}.json', {'orbits': batch}, args.check))
    counterexample = named_counterexample(records)
    if counterexample is not None:
        emit(OUT / f'counterexample_{counterexample["name"]}.json', counterexample, args.check)
    totals = Counter()
    for graph in records:
        totals.update(graph['search_totals'])
    data = {'schema': 'c44-v1', 'input_base': 'b2ca452', 'k_max': 9,
            'statistics': summary(records), 'output_chunks': manifests,
            'search_totals': dict(sorted(totals.items())),
            'branch': 'counterexample' if counterexample else 'finite_absence',
            'counterexample_name': counterexample['name'] if counterexample else None}
    emit(OUT / 'summary.json', data, args.check)
    print(f'FULL PASS {len(records)} orbits; branch={data["branch"]}; '
          f'cores={totals["core_minimality_witnesses"]} deletion witnesses; '
          f'seconds={time.monotonic()-start:.3f}', flush=True)


if __name__ == '__main__':
    main()
