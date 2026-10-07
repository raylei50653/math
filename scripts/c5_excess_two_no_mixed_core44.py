#!/usr/bin/env python3
"""Exclude the U1 no-mixed two-root (4,4) identity for full Sigma 933/941.

Read 344 inherited bridge-marker cores, independently enumerate whole-graph
colorings, and restore every missing spoke at each bridge root. Paper also
excludes the (2,3) identity. No planarity oracle or historical producer imports.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_excess_two_mixed_omission/observations.json'
OUT = ROOT / 'artifacts/c5_excess_two_no_mixed_core44/observations.json'


def normalize(word):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in word)


def colorings(edges, row, roots):
    vertices = set().union(*map(set, edges))
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    coloring = dict(enumerate(row))
    found = {}

    def visit():
        remaining = vertices - coloring.keys()
        if not remaining:
            found.setdefault(tuple(coloring[v] for v in roots),
                             tuple(coloring[v] for v in sorted(vertices)))
            return
        options = {v: set(range(4)) - {coloring[u] for u in adjacency[v] if u in coloring}
                   for v in remaining}
        v = min(remaining, key=lambda x: (len(options[x]), -len(adjacency[x]), x))
        for c in sorted(options[v]):
            coloring[v] = c
            visit()
            del coloring[v]

    visit()
    return found


def build():
    data = json.loads(INPUT.read_text())
    rows = data['pattern_order']
    index = {tuple(r): i for i, r in enumerate(rows)}
    orbits = {str(mask): sorted({sum(1 << index[normalize(
        [row[(sign*j+shift) % 5] for j in range(5)])]
        for ri, row in enumerate(rows) if mask >> ri & 1)
        for sign in (-1, 1) for shift in range(5)}) for mask in (933, 941)}
    assert orbits == data['target_D5_orbits']
    targets = set().union(*map(set, orbits.values()))
    forms, histogram = [], Counter()
    cases, checks = 0, 0
    for input_id, source in enumerate(data['original_marked_cores']):
        edges = {tuple(e) for e in source['edges']}
        roots = tuple(source['original_root_order'])
        interior = source['interior_order']
        assert len(set(roots)) == 2 and roots in edges
        triangles = [t for t in combinations(interior, 3)
                     if all(e in edges for e in combinations(t, 2))]
        reached, pending = {roots[0]}, [roots[0]]
        while pending:
            v = pending.pop()
            for a, b in edges - {roots}:
                if a >= 5 and v in (a, b):
                    w = b if v == a else a
                    if w not in reached:
                        reached.add(w)
                        pending.append(w)
        assert roots[1] not in reached  # Literal internal bridge, not a triangle edge.
        if source['family'] == 'double_triangle':
            assert len(interior) == 6 and len(triangles) == 2
            assert not set(triangles[0]) & set(triangles[1])
            assert {e for e in edges if e[0] >= 5} == {
                e for t in triangles for e in combinations(t, 2)} | {roots}
        assert all(sum(v in e for e in edges) == 4 for v in interior)
        relations = [colorings(edges, row, roots) for row in rows]
        assert sum(1 << ri for ri, rel in enumerate(relations) if rel) == 1022
        assert [set(rel) for rel in relations] == [set(map(tuple, r['original_bridge_retained_pairs']))
                                                   for r in source['rows']]
        saved_rows = [dict(root_pairs=sorted(rel), full_coloring_witnesses=[rel[t] for t in sorted(rel)])
                      for rel in relations]
        restorations = []
        for bz, bw in product([b for b in range(5) if (b, roots[0]) not in edges],
                              [b for b in range(5) if (b, roots[1]) not in edges]):
            restored = [(bz, roots[0]), (bw, roots[1])]
            complete = edges | set(restored)
            assert [sum(r in e for e in complete) for r in roots] == [5, 5]
            retained = []
            sigma = 0
            for ri, (row, rel) in enumerate(zip(rows, relations, strict=True)):
                filtered = {t for t in rel if t[0] != row[bz] and t[1] != row[bw]}
                assert filtered == set(colorings(complete, row, roots))
                pairs = saved_rows[ri]['root_pairs']
                retained.append([j for j, t in enumerate(pairs) if t in filtered])
                if filtered:
                    sigma |= 1 << ri
                checks += 1
            assert sigma not in targets
            restorations.append(dict(restored_spokes=restored, sigma=sigma,
                row_pair_indices=retained))
            histogram[sigma] += 1
            cases += 1
        forms.append(dict(input_form_id=input_id, family=source['family'], original_root_order=roots,
            core_edges=sorted(edges), coloring_vertex_order=sorted(set().union(*map(set, edges))),
            original_unary_vertices=[r['vertices'] for r in source['original_retained_unaries']],
            core_rows=saved_rows, restorations=restorations))
    assert len(forms) == 344 and cases == 3498 and checks == 34980
    return dict(schema=1, scope='U1 two-root44 no-mixed identity only; full Sigma933/941 and whole-graph D5 images; paper handles arbitrary-size reduction and (2,3)',
        source_sha256={str(INPUT.relative_to(ROOT)): sha256(INPUT.read_bytes()).hexdigest(),
                       str(Path(__file__).resolve().relative_to(ROOT)): sha256(Path(__file__).read_bytes()).hexdigest()},
        pattern_order=rows, target_D5_orbits=orbits, forms=forms,
        witness_semantics='Same core whole-graph coloring after literal spoke filtering; empty relations independently recomputed on restored edges',
        summary=dict(cores=len(forms), restorations=cases, independent_restored_row_checks=checks,
                     family_core_counts=dict(Counter(f['family'] for f in forms)),
                     family_restoration_counts={family: sum(len(f['restorations'])
                         for f in forms if f['family'] == family) for family in {f['family'] for f in forms}},
                     sigma_histogram=dict(sorted(histogram.items())), target_hits=0,
                     graph_census=False, source_realizability_claimed=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate differs; do not overwrite historical inputs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='checked' if args.check else 'written', **data['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
