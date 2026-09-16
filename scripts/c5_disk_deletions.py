#!/usr/bin/env python3
"""Replay plantri C5 disks for k=0..3 and every one-edge nonboundary deletion.

uv run --with networkx==3.5 python scripts/c5_disk_deletions.py [--check]
Completeness depends on plantri; geometry and all 240 boundary rows are replayed.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib
from itertools import permutations, product
import json
from pathlib import Path

import networkx as nx

from boundary_relations import normalize
from c5_cell_enumerator import REPS
from local_closure import direct_graph_extend

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_disk_deletions'
CYCLE = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
BOUNDARY = tuple(b for b in product(range(4), repeat=5)
                 if all(b[u] != b[v] for u, v in CYCLE))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def faces_of(rotation):
    """Traverse every dart of a spherical rotation system exactly once."""
    seen, faces = set(), []
    for u, neighbors in enumerate(rotation):
        assert len(neighbors) == len(set(neighbors)) and u not in neighbors
        for v in neighbors:
            assert u in rotation[v]
            if (u, v) in seen:
                continue
            face, a, b = [], u, v
            while (a, b) not in seen:
                seen.add((a, b))
                face.append(a)
                ring = rotation[b]
                a, b = b, ring[(ring.index(a) - 1) % len(ring)]
            assert (a, b) == (u, v)
            faces.append(face)
    return faces


def parse_disk(line, k):
    count, data = line.split()
    n = int(count)
    rotation = [[ord(c) - ord('a') for c in row] for row in data.split(',')]
    assert n == 5 + k == len(rotation)
    assert all(0 <= v < n for row in rotation for v in row)
    edges = {tuple(sorted((u, v))) for u, row in enumerate(rotation) for v in row}
    faces = faces_of(rotation)
    assert n - len(edges) + len(faces) == 2
    assert len(edges) == 3 * k + 7
    outer, = [f for f in faces if len(f) == 5]
    assert len(set(outer)) == 5
    assert all(len(f) == 5 or (len(f) == 3 and len(set(f)) == 3) for f in faces)
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(edges)
    assert nx.is_connected(graph)
    assert nx.check_planarity(graph)[0]
    return edges, outer, rotation


def canonical(n, edges):
    """Fix boundary pointwise; quotient only interior vertex permutations."""
    candidates = []
    for p in permutations(range(5, n)):
        labels = tuple(range(5)) + p
        candidates.append(tuple(sorted(tuple(sorted((labels[u], labels[v])))
                                       for u, v in edges)))
    return min(candidates)


@lru_cache(None)
def relation(n, edges):
    # Independent formulations: brute-force interior tuples versus vertex backtracking.
    accepted = set()
    for j, b in enumerate(REPS):
        for x in product(range(4), repeat=n - 5):
            c = b + x
            if all(c[u] != c[v] for u, v in edges):
                accepted.add(j)
                break
    bits = sum(1 << j for j in accepted)
    full = []
    for b in BOUNDARY:
        actual = direct_graph_extend(n, edges, b)
        assert actual == (REPS.index(normalize(b)) in accepted)
        full.append(actual)
    return bits, format(sum(int(x) << j for j, x in enumerate(full)), '060x')


def build():
    manifest = json.loads((OUT / 'plantri/manifest.json').read_text())
    assert [r['k'] for r in manifest['runs']] == list(range(4))
    rows, stats, geometry, first_seen = [], [], [], {}
    for run in manifest['runs']:
        k, sources = run['k'], {}
        n = 5 + k
        path = OUT / 'plantri' / run['file']
        assert sha(path) == run['sha256']
        lines = path.read_text().splitlines()
        assert len(lines) == run['count']
        for index, line in enumerate(lines):
            edges, outer, rotation = parse_disk(line, k)
            geometry.append(dict(k=k, source_index=index, rotation=rotation, outer=outer))
            # Both directions and every starting position: D5 is not quotiented.
            for direction in (1, -1):
                for shift in range(5):
                    order = [outer[(shift + direction * i) % 5] for i in range(5)]
                    order += sorted(set(range(n)) - set(outer))
                    label = {v: i for i, v in enumerate(order)}
                    key = canonical(n, [(label[u], label[v]) for u, v in edges])
                    assert CYCLE <= set(key)
                    sources.setdefault(key, []).append([index, direction, shift])
        start = len(rows)
        for edges, origins in sorted(sources.items()):
            bits, full = relation(n, edges)
            deletions = []
            for edge in sorted(set(edges) - CYCLE):
                child = canonical(n, set(edges) - {edge})
                after, after_full = relation(n, child)
                assert bits & after == bits
                deletions.append(dict(edge=edge, sigma=after, full=after_full))
            rows.append(dict(id=f'k{k}-t{len(rows)-start}', k=k, edges=edges,
                             origins=origins, sigma=bits, full=full,
                             successors=sorted({d['sigma'] for d in deletions}),
                             strict_successors=sorted({d['sigma'] for d in deletions
                                                       if d['sigma'] != bits}),
                             deletions=deletions))
        group = rows[start:]
        parents = {r['sigma'] for r in group}
        children = {d['sigma'] for r in group for d in r['deletions']}
        for bits in sorted(parents | children):
            first_seen.setdefault(bits, k)
        stats.append(dict(k=k, embedded_unlabelled_parents=len(lines),
                          boundary_fixed_parents=len(group),
                          deletion_edges=sum(len(r['deletions']) for r in group),
                          parent_relations=sorted(parents), child_relations=sorted(children),
                          child_only_relations=sorted(children - parents),
                          strict_deletions=sum(d['sigma'] != r['sigma'] for r in group
                                               for d in r['deletions']),
                          cumulative_relations=len(first_seen)))
    collisions = []
    for k in range(4):
        groups = defaultdict(list)
        for row in rows:
            if row['k'] == k:
                groups[row['sigma']].append(row)
        stats[k]['equal_sigma_parent_pairs'] = sum(len(g) * (len(g) - 1) // 2
                                                    for g in groups.values())
        for bits, group in sorted(groups.items()):
            for field in ('successors', 'strict_successors'):
                classes = defaultdict(list)
                for row in group:
                    classes[tuple(row[field])].append(row['id'])
                if len(classes) > 1:
                    ordered = sorted(classes.items())
                    collisions.append(dict(k=k, sigma=bits, comparison=field,
                                           classes=[dict(values=key, parents=ids)
                                                    for key, ids in ordered],
                                           witness=[ordered[0][1][0], ordered[1][1][0]]))
        stats[k]['all_successor_collision_groups'] = sum(
            c['k'] == k and c['comparison'] == 'successors' for c in collisions)
        stats[k]['strict_successor_collision_groups'] = sum(
            c['k'] == k and c['comparison'] == 'strict_successors' for c in collisions)
    baseline_path = ROOT / 'artifacts/c5_cells/cells.json'
    baseline = json.loads(baseline_path.read_text())
    # Existing catalogue has one row per relation, in "cells".
    assert baseline['pattern_order'] == [list(b) for b in REPS]
    baseline_bits = {int(b) for b in baseline['cells']}
    multiplicities = Counter(r['sigma'] for r in rows)
    deletion_multiplicities = Counter(d['sigma'] for r in rows for d in r['deletions'])
    return dict(schema=1, scope=dict(k=list(range(4)), boundary='ordered C5',
                    parents='simple embedded disks; all bounded faces triangles; chords allowed',
                    deletion='exactly one edge outside the five boundary-cycle edges',
                    parent_quotient='interior permutations only; fixed boundary labels',
                    completeness='external plantri 5.8; no completion lemma used',
                    excluded_from_search=['k>=4', 'two or more deletions', 'boundary-edge deletion',
                                          'vertex deletion', 'loops or parallel edges']),
                inputs=manifest, source_sha256={str(p.relative_to(ROOT)): sha(p) for p in
                    [Path(__file__).resolve(), ROOT / 'scripts/local_closure.py',
                     ROOT / 'scripts/c5_cell_enumerator.py', ROOT / 'scripts/boundary_relations.py']},
                pattern_order=REPS, boundary_rows=BOUNDARY,
                encoding='sigma: S4 orbit mask; full: bit j = boundary_rows[j]; D5 not quotiented',
                statistics=stats, collisions=collisions,
                first_seen_in_sample={str(b): k for b, k in sorted(first_seen.items())},
                parent_realizations=dict(sorted(multiplicities.items())),
                one_deletion_realizations=dict(sorted(deletion_multiplicities.items())),
                baseline=dict(path=str(baseline_path.relative_to(ROOT)), sha256=sha(baseline_path),
                              relations=len(baseline_bits), new_relations=sorted(set(first_seen)-baseline_bits)),
                geometry=geometry, parents=rows,
                verification=dict(unique_graph_relations=relation.cache_info().currsize,
                                  direct_boundary_queries=240 * relation.cache_info().currsize))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    path = OUT / 'observations.json'
    if args.check:
        assert path.read_text() == data, 'artifact differs; rebuild explicitly'
    else:
        path.write_text(data)
    print(json.dumps({key: result[key] for key in ('baseline', 'verification')}, indent=2))
    for row in result['statistics']:
        print(json.dumps({key: len(value) if isinstance(value, list) else value
                          for key, value in row.items()}))
    print('collision groups:', len(result['collisions']))
    print('first collisions:', json.dumps(result['collisions'][:2]))


if __name__ == '__main__':
    main()
