#!/usr/bin/env python3
"""Independent stdlib replay of exact original-path cut/fibre certificates.

No producer, solver, or other repository module is imported. Reconstructs
embedded regions with dual union-find, enumerates complete literal colorings
in a dynamic vertex order, and checks every separator assignment and rejoin.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

C0 = (2, 3, 4, 7, 5, 6)
D16 = {tuple(map(int, word)) for word in (
    '010201 010212 010213 010231 012012 012021 012102 012121 '
    '012123 012132 012301 012302 012312 012313 012321 012323'
).split()}
CENTER_EDGES = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 7),
                (1, 2), (1, 5), (1, 6), (1, 7))


def normalize(row):
    names = {}
    result = []
    for c in row:
        if c not in names:
            names[c] = len(names)
        result.append(names[c])
    return tuple(result)


def edge_set(edges):
    return {tuple(sorted(e)) for e in edges}


def coloring_set(vertices, edges):
    """Literal colors, dynamic saturation ordering independent of producer."""
    neighbors = {v: set() for v in vertices}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    assigned = {}
    result = set()

    def visit():
        if len(assigned) == len(vertices):
            result.add(tuple(assigned[v] for v in vertices))
            return
        u = max((v for v in vertices if v not in assigned),
                key=lambda v: (len({assigned[w] for w in neighbors[v] if w in assigned}),
                               len(neighbors[v]), v))
        forbidden = {assigned[w] for w in neighbors[u] if w in assigned}
        for c in range(4):
            if c not in forbidden:
                assigned[u] = c
                visit()
                del assigned[u]

    visit()
    return result


def check_sphere(vertices, edges, faces):
    assert len(edges) == len(edge_set(edges))
    expected = Counter((u, v) for a, b in edges for u, v in ((a, b), (b, a)))
    darts = Counter((f[j], f[(j + 1) % len(f)])
                    for f in faces for j in range(len(f)))
    assert darts == expected
    assert len(vertices) - len(edges) + len(faces) == 2
    rotation = {v: {} for v in vertices}
    for f in faces:
        for j, v in enumerate(f):
            previous = f[j - 1]
            assert previous not in rotation[v]
            rotation[v][previous] = f[(j + 1) % len(f)]
    cyclic_orders = {}
    for v in vertices:
        rule = rotation[v]
        assert rule
        start = min(rule)
        walk = [start]
        current = rule[start]
        while current != start:
            assert current not in walk
            walk.append(current)
            current = rule[current]
        assert set(walk) == set(rule)
        cyclic_orders[v] = walk
    # A connected rotation with Euler characteristic two is a sphere embedding.
    neighbors = {v: set() for v in vertices}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    reached = {vertices[0]}
    queue = list(reached)
    for v in queue:
        for w in neighbors[v] - reached:
            reached.add(w)
            queue.append(w)
    assert reached == set(vertices)
    return cyclic_orders


def check_cut(rec):
    embed = rec['embedding']
    vertices = rec['original_h_vertex_order']
    edges = edge_set(embed['h_edges'])
    hfaces = embed['h_oriented_faces']
    hrot = check_sphere(vertices, list(edges), hfaces)
    gvertices = [0, 1] + vertices
    gedges = edges | set(CENTER_EDGES)
    check_sphere(gvertices, list(gedges), embed['g_oriented_faces'])
    outer_ids = [i for i, f in enumerate(hfaces) if len(f) == 6 and set(f) == set(C0)]
    assert len(outer_ids) == 1
    outer = outer_ids[0]
    outer_word = hfaces[outer]
    k = outer_word.index(2)
    outer_word = tuple(outer_word[k:] + outer_word[:k])
    assert outer_word in (C0, (2, 6, 5, 7, 4, 3))
    path = rec['path']
    assert path[0] == 4 and path[-1] == 5 and len(path) == len(set(path))
    assert set(path[1:-1]).isdisjoint(C0)
    cuts = edge_set(zip(path, path[1:]))
    assert cuts <= edges
    witness = dict(zip(vertices, rec['seed_coloring']))
    assert all(witness[u] != witness[v] for u, v in edges)
    assert all(witness[v] in (2, 3) for v in path)
    parent = list(range(len(hfaces)))

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    incidence = defaultdict(list)
    for i, f in enumerate(hfaces):
        for j, u in enumerate(f):
            incidence[tuple(sorted((u, f[(j + 1) % len(f)])))].append(i)
    for edge, ids in incidence.items():
        assert len(ids) == 2
        if outer not in ids and edge not in cuts:
            parent[root(ids[0])] = root(ids[1])
    groups = defaultdict(set)
    for i in range(len(hfaces)):
        if i != outer:
            groups[root(i)].add(i)
    regions = list(groups.values())
    assert len(regions) == 2
    for side in (rec['left'], rec['right']):
        ids = set(side['original_face_indices'])
        assert ids in regions
        regions.remove(ids)
        se = {tuple(sorted((hfaces[i][j], hfaces[i][(j + 1) % len(hfaces[i])])))
              for i in ids for j in range(len(hfaces[i]))}
        assert edge_set(side['edges']) == se
        assert side['vertices'] == sorted({v for edge in se for v in edge})
        attachments = [[u, [v for v in hrot[u]
                             if v not in path and tuple(sorted((u, v))) in se]]
                       for u in path]
        assert attachments == side['ordered_path_attachments']
    assert not regions
    left, right = rec['left'], rec['right']
    assert 2 in left['vertices'] and 7 not in left['vertices']
    assert 7 in right['vertices'] and 2 not in right['vertices']
    assert set(left['vertices']) & set(right['vertices']) == set(path)
    assert edge_set(left['edges']) & edge_set(right['edges']) == cuts
    assert edge_set(left['edges']) | edge_set(right['edges']) == edges
    assert left['arc_order'] == [2, 3, 6] and right['arc_order'] == [7]
    return edges


def center_fibre(row):
    assign = dict(zip(C0, row))
    result = []
    for a, b in product(range(4), repeat=2):
        f = assign | {0: a, 1: b}
        if all(f[u] != f[v] for u, v in CENTER_EDGES):
            result.append([a, b])
    return result


def check_escape(cert, rec, records):
    assert cert is not None
    lam = tuple(cert['separator'])
    fib = records[lam]
    zi, wi = cert['left_coloring_index'], cert['right_coloring_index']
    assert zi in fib['left_fibre'] and wi in fib['right_fibre']
    zassign = dict(zip(rec['left']['vertices'], rec['left']['colorings'][zi]))
    wassign = dict(zip(rec['right']['vertices'], rec['right']['colorings'][wi]))
    assert all(zassign[v] == wassign[v] for v in rec['path'])
    assign = zassign | wassign
    assert cert['full_h_coloring'] == [assign[v] for v in rec['original_h_vertex_order']]
    row = [assign[v] for v in C0]
    assert row == cert['c0_row']
    assert normalize(row) not in D16
    assert center_fibre(row) == cert['center_lifts']
    assert cert['center_lifts']


def check_remote_lock(rec, full, edges):
    vertices = rec['original_h_vertex_order']
    neighbors = {v: set() for v in vertices}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    fixed = sorted(row for row in full
                   if tuple(row[v - 2] for v in C0) == (0, 1, 2, 1, 2, 1))
    saved = rec['remote_lock_check']
    assert [r['source'] for r in saved['records']] == [list(r) for r in fixed]
    counts = Counter()
    for row, record in zip(fixed, saved['records']):
        f = dict(zip(vertices, row))
        parent = {v: v for v in vertices if f[v] in (1, 2)}

        def root(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        for u, v in edges:
            if u in parent and v in parent:
                parent[root(u)] = root(v)
        groups = defaultdict(set)
        for v in parent:
            groups[root(v)].add(v)
        boundary_component = groups[root(3)]
        assert boundary_component & set(C0) == {3, 4, 5, 6, 7}
        remote = sorted(sorted(k) for k in groups.values() if k != boundary_component)
        boundary_hits = sorted(v for v in neighbors[2] & boundary_component if f[v] == 2)
        mixed = [k for k in remote if {f[v] for v in neighbors[2] & set(k)} == {1, 2}]
        assert record['boundary_12_component'] == sorted(boundary_component)
        assert record['all_remote_12_components'] == remote
        assert record['boundary_color2_neighbors'] == boundary_hits
        assert record['remote_components_with_both_neighbor_colors'] == mixed
        counts['i'] += bool(boundary_hits)
        counts['ii'] += bool(mixed)
        if boundary_hits or mixed:
            assert 'escape' not in record
            continue
        counts['escape'] += 1
        cert = record['escape']
        selected = [k for k in remote if any(f[v] == 2 for v in neighbors[2] & set(k))]
        assert cert['swapped_remote_components'] == selected
        changed = {v for k in selected for v in k}
        intermediate = {v: 3 - c if v in changed else c for v, c in f.items()}
        assert cert['intermediate'] == [intermediate[v] for v in vertices]
        assert tuple(intermediate[v] for v in C0) == (0, 1, 2, 1, 2, 1)
        assert all(intermediate[v] != 2 for v in neighbors[2])
        assert all(intermediate[u] != intermediate[v] for u, v in edges)
        target = intermediate | {2: 2}
        assert cert['target'] == [target[v] for v in vertices]
        assert tuple(target[v] for v in vertices) in full
        assert tuple(target[v] for v in C0) == (2, 1, 2, 1, 2, 1)
        assert all(target[u] != target[v] for u, v in edges)
        assert cert['center_lifts'] == center_fibre((2, 1, 2, 1, 2, 1))
        assert cert['center_lifts']
    assert saved['fixed_literal_20_lifts'] == len(fixed)
    assert saved['alternative_i_holds'] == counts['i']
    assert saved['alternative_ii_holds'] == counts['ii']
    assert saved['explicit_escapes'] == counts['escape']
    return dict(fixed_literal_20_lifts=len(fixed), alternative_i_holds=counts['i'],
                alternative_ii_holds=counts['ii'], explicit_escapes=counts['escape'],
                independent_union_find_checked=True)


def replay_control(rec):
    edges = check_cut(rec)
    vertices = rec['original_h_vertex_order']
    path = rec['path']
    left, right = rec['left'], rec['right']
    for side in (left, right):
        rows = [tuple(row) for row in side['colorings']]
        assert len(rows) == len(set(rows))
        assert set(rows) == coloring_set(side['vertices'], side['edges'])
    records = {tuple(r['separator']): r for r in rec['separator_fibres']}
    assert len(records) == len(rec['separator_fibres']) == 4 ** len(path)
    assert set(records) == set(product(range(4), repeat=len(path)))
    maps = []
    for side in (left, right):
        pos = {v: i for i, v in enumerate(side['vertices'])}
        fibres = defaultdict(list)
        for i, row in enumerate(side['colorings']):
            fibres[tuple(row[pos[v]] for v in path)].append(i)
        maps.append((pos, fibres))
    joined = set()
    nonempty = 0
    for lam, fib in records.items():
        (lp, lf), (rp, rf) = maps
        assert fib['left_fibre'] == lf[lam]
        assert fib['right_fibre'] == rf[lam]
        if lf[lam] and rf[lam]:
            nonempty += 1
        us = sorted({tuple(left['colorings'][i][lp[v]] for v in (2, 3, 6)) for i in lf[lam]})
        ts = sorted({right['colorings'][i][rp[7]] for i in rf[lam]})
        assert fib['left_triples'] == [list(u) for u in us]
        assert fib['right_colors'] == ts
        forbidden = [[list(u), t] for u in us for t in ts
                     if normalize((u[0], u[1], lam[0], t, lam[-1], u[2])) not in D16]
        assert fib['forbidden_rectangles'] == forbidden
        for zi in lf[lam]:
            za = dict(zip(left['vertices'], left['colorings'][zi]))
            for wi in rf[lam]:
                wa = dict(zip(right['vertices'], right['colorings'][wi]))
                assert all(za[v] == wa[v] for v in path)
                assign = za | wa
                full = tuple(assign[v] for v in vertices)
                assert all(assign[u] != assign[v] for u, v in edges)
                assert full not in joined
                joined.add(full)
    independent_full = coloring_set(vertices, edges)
    assert joined == independent_full
    verification = rec['verification']
    assert verification['h_colorings'] == verification['joined_colorings'] == len(joined)
    assert verification['all_fibres_including_empty'] == 4 ** len(path)
    assert verification['nonempty_common_separator_fibres'] == nonempty
    seed = dict(zip(vertices, rec['seed_coloring']))
    seed_lam = tuple(seed[v] for v in path)
    assert verification['seed_separator'] == list(seed_lam)
    record = records[seed_lam]
    assert record['left_triples'] == verification['seed_left_triples']
    assert record['right_colors'] == verification['seed_right_colors']
    assert len(record['forbidden_rectangles']) == verification['seed_forbidden_rectangles']
    check_escape(verification['some_accepted_escape'], rec, records)
    check_escape(verification['seed_accepted_escape'], rec, records)
    assert verification['seed_accepted_escape']['separator'] == list(seed_lam)
    remote = check_remote_lock(rec, independent_full, edges) if 'remote_lock_check' in rec else None
    return dict(name=rec['name'], h_colorings=len(joined),
                left_colorings=len(left['colorings']), right_colorings=len(right['colorings']),
                all_separator_assignments=4 ** len(path),
                nonempty_common_separator_fibres=nonempty,
                seed_forbidden_rectangles=len(record['forbidden_rectangles']),
                accepted_seed_escape_checked=True, original_embedded_cut_checked=True,
                all_actual_attachments_checked=True, remote_lock_check=remote)


def check_rectangles(tables):
    assert len(tables) in (3, 4)
    lengths = []
    for rec in tables:
        b, c = rec['end_colors']
        ts = rec['right_support']
        allowed = []
        for z, a, d in product(range(4), repeat=3):
            rows = [(z, a, b, w, c, d) for w in ts]
            proper = all(all(row[j] != row[(j + 1) % 6] for j in range(6)) for row in rows)
            if proper and all(normalize(row) in D16 for row in rows):
                allowed.append([z, a, d])
        assert allowed == rec['allowed_left_triples']
        lengths.append(len(allowed))
    assert lengths == ([9, 12, 6] if len(tables) == 3 else [9, 12, 6, 6])
    return lengths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    args = parser.parse_args()
    summary = json.loads(args.results.read_text())
    counts = check_rectangles(summary['rectangle_tables'])
    checked = []
    for advertised in summary['controls']:
        path = args.results.parent / (advertised['name'].lower() + '.json')
        rec = json.loads(path.read_text())
        assert {k: v for k, v in advertised.items() if k not in ('name', 'path')} == rec['verification']
        assert advertised['name'] == rec['name'] and advertised['path'] == rec['path']
        checked.append(replay_control(rec))
    print(json.dumps(dict(passed=True, independent_coloring_order='dynamic saturation with literal colors',
                         independent_cut_algorithm='union-find on original face dual',
                         rectangle_table_sizes=counts, controls=checked,
                         scope='Finite named graphs and exact relation identities only; general D16 exclusion remains OPEN.'), indent=2))


if __name__ == '__main__':
    main()
