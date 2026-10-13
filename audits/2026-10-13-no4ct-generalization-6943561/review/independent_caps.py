#!/usr/bin/env python3
"""Independent recurrence, dart topology, and edge-DFS audit. No producer import."""
from collections import Counter
from functools import lru_cache
from itertools import product
import argparse
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


@lru_cache(None)
def polygon(vertices):
    if len(vertices) == 2:
        return ((),)
    result = []
    # Unique face incident with the polygon's base edge (first,last).
    for flags in product((0, 1), repeat=len(vertices)-2):
        indices = [0] + [i+1 for i, x in enumerate(flags) if x] + [len(vertices)-1]
        if len(indices) < 3:
            continue
        root = tuple(vertices[i] for i in indices)
        gaps = [polygon(vertices[a:b+1]) for a, b in zip(indices, indices[1:])]
        for subparts in product(*gaps):
            result.append(tuple(sorted((root,) + tuple(f for part in subparts for f in part))))
    assert len(result) == len(set(result))
    return tuple(result)


def edge(a, b):
    return tuple(sorted((a, b)))


def proper_rows():
    result = []
    def rec(word):
        if len(word) == 8:
            if word[-1] != word[0]:
                result.append(tuple(word))
            return
        for c in range(min(3, max(word, default=-1)+1)+1):
            if not word or c != word[-1]:
                rec(word+[c])
    rec([])
    return result


def full_lifts(row, edges, n):
    colors = list(row) + [-1]*(n-8)
    neighbors = [[] for _ in range(n)]
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
        if a < 8 and b < 8 and row[a] == row[b]:
            return []
    result = []
    def visit(v):
        if v == n:
            result.append(colors[8:].copy())
            return
        for c in range(4):
            if all(colors[w] != c for w in neighbors[v]):
                colors[v] = c
                visit(v+1)
                colors[v] = -1
    visit(8)
    return result


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    cert = json.loads(gzip.decompress((ROOT/'caps_certificate.json.gz').read_bytes()))
    rows = proper_rows()
    assert [list(x) for x in rows] == cert['boundary_rows']
    query_data = json.loads((ROOT/'frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())
    queries = {q['query_id']: q['support'] for q in query_data['queries']
               if q['status'] == 'necessary_condition_residual'}
    all_faces = polygon(tuple(range(8)))
    assert len(all_faces) == 903
    cycle = {edge(i, (i+1)%8) for i in range(8)}
    expected_keys = {}
    for faces in all_faces:
        edges = {edge(f[i], f[(i+1)%len(f)]) for f in faces for i in range(len(f))}
        chords = tuple(sorted(edges-cycle))
        eligible = [f for f in faces if len(f) > 3]
        for flags in product((0, 1), repeat=len(eligible)):
            selected = tuple(f for f, yes in zip(eligible, flags) if yes)
            key = (chords, selected)
            assert key not in expected_keys
            expected_keys[key] = faces
    seen = set()
    counters = Counter()
    common = (1 << len(rows))-1
    minima = {name: len(rows) for name in queries}
    # For each named row, retain a cap that rejects it. These are different caps.
    rejector = {}
    for cap in cert['caps']:
        chords = tuple(tuple(x) for x in cap['chords'])
        selected = tuple(tuple(x) for x in cap['hub_faces'])
        key = (chords, selected)
        assert key in expected_keys and key not in seen
        seen.add(key)
        polygons = expected_keys[key]
        assert tuple(tuple(f) for f in cap['dissection_faces']) == polygons
        assert cap['boundary_order'] == [f'c{i}' for i in range(8)]
        assert cap['hub_names'] == [f'z{i}' for i in range(len(selected))]
        edges = cycle | set(chords)
        actual_faces = [tuple(reversed(range(8)))]
        for f in polygons:
            if f not in selected:
                actual_faces.append(f)
            else:
                z = 8+selected.index(f)
                edges.update(edge(z, v) for v in f)
                actual_faces.extend((f[i], f[(i+1)%len(f)], z) for i in range(len(f)))
        darts = Counter((f[i], f[(i+1)%len(f)]) for f in actual_faces for i in range(len(f)))
        assert darts == Counter({d: 1 for a, b in edges for d in ((a, b), (b, a))})
        assert 8+len(selected)-len(edges)+len(actual_faces) == 2
        # Faces are obtained by convex-polygon subdivision and interior face fans;
        # the darts/Euler check additionally verifies the complete named embedding.
        full = [full_lifts(row, edges, 8+len(selected)) for row in rows]
        assert full == cap['full_hub_lifts_by_literal_row']
        relation = sum(1 << i for i, lifts in enumerate(full) if lifts)
        assert relation == cap['relation']
        common &= relation
        for i, lifts in enumerate(full):
            if not lifts:
                rejector.setdefault(i, cap['id'])
        hits = {name: (support & relation).bit_count() for name, support in queries.items()}
        assert hits == cap['upper_support_intersection']
        for name, count in hits.items():
            assert count > 0
            minima[name] = min(minima[name], count)
        counters['caps'] += 1
        counters['fibres'] += len(full)
        counters['empty_fibres'] += sum(not f for f in full)
        counters['full_lifts'] += sum(map(len, full))
    assert seen == set(expected_keys)
    assert counters['caps'] == 2274
    assert common == 0 and len(rejector) == 274
    assert minima == cert['summary']['minimum_intersections']
    for local, published in [('fibres','full_fibres'), ('empty_fibres','empty_fibres'), ('full_lifts','full_lifts')]:
        assert counters[local] == cert['summary'][published]
    result = dict(status='PASS', method='independent base-face recurrence; complete darts; graph-edge DFS',
                  dissections=len(all_faces), **counters, minimum_intersections=minima,
                  intersection_of_all_cap_relations=common,
                  row_rejecting_cap={str(i): cap_id for i, cap_id in sorted(rejector.items())},
                  quantifier='Every cap separately intersects every residual upper support; no single row is accepted by every cap. Neither statement supplies an actual residual source.')
    result_path = HERE/'independent_caps_result.json'
    if args.write:
        with result_path.open('x') as out:
            out.write(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        assert json.loads(result_path.read_text()) == result
    print(json.dumps({k: v for k, v in result.items() if k != 'row_rejecting_cap'}, sort_keys=True))


if __name__ == '__main__':
    main()
