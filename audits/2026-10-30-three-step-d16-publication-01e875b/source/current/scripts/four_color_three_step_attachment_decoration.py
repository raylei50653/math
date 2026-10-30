#!/usr/bin/env python3
"""Exact K4 edge decoration: neighbour-test no gain, connectivity/classes retained.

Producer imports the existing BUFFER source. Replay imports no repository code,
enumerates old colourings independently, and recomputes induced components by
union-find. The arbitrary-size theorem is paper evidence, not a finite search.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CYCLE = (2, 3, 4, 7, 5, 6)
PAIRS = tuple(combinations(range(4), 2))
NEW = (19, 20)
ADDED = ((2, 19), (2, 20), (3, 19), (3, 20), (19, 20))


def normalize(row):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in row)


def encode(value):
    return json.dumps(value, separators=(',', ':')).encode()


def union_components(row, vertices, edges):
    f = dict(zip(vertices, row))
    result = []
    for pair in PAIRS:
        parent = {v: v for v in vertices if f[v] in pair}
        def root(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for u, v in edges:
            if u in parent and v in parent:
                parent[root(u)] = root(v)
        grouped = defaultdict(list)
        for v in sorted(parent):
            grouped[root(v)].append(v)
        result.append(tuple(sorted(tuple(vs) for vs in grouped.values())))
    return tuple(result)


def dfs_components(row, vertices, edges):
    f = dict(zip(vertices, row))
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    result = []
    for pair in PAIRS:
        left = {v for v in vertices if f[v] in pair}
        grouped = []
        while left:
            queue = [min(left)]
            left.remove(queue[0])
            for u in queue:
                for v in sorted(adj[u] & left):
                    left.remove(v)
                    queue.append(v)
            grouped.append(tuple(sorted(queue)))
        result.append(tuple(sorted(grouped)))
    return tuple(result)


def enum_independent(vertices, edges):
    # Dynamic saturation order; producer uses restricted-growth original order.
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assigned = {2: 0, 3: 1}
    rows = set()
    leaves = 0
    def visit():
        nonlocal leaves
        if len(assigned) == len(vertices):
            rows.add(normalize(tuple(assigned[v] for v in vertices)))
            leaves += 1
            return
        v = max((v for v in vertices if v not in assigned),
                key=lambda v: (len({assigned[w] for w in adjacency[v] if w in assigned}),
                               len(adjacency[v]), -v))
        forbidden = {assigned[w] for w in adjacency[v] if w in assigned}
        for c in range(4):
            if c not in forbidden:
                assigned[v] = c
                visit()
                del assigned[v]
    visit()
    assert leaves == 2 * len(rows)
    return sorted(rows)


def check_embedding(n, edges, faces):
    expected = {(u, v) for a, b in edges for u, v in ((a, b), (b, a))}
    darts = Counter((face[j], face[(j + 1) % len(face)])
                    for face in faces for j in range(len(face)))
    assert darts == Counter({dart: 1 for dart in expected})
    assert n - len(edges) + len(faces) == 2
    rotations = {}
    for v in range(n):
        nxt = {}
        for face in faces:
            for j, u in enumerate(face):
                if u == v:
                    assert face[j - 1] not in nxt
                    nxt[face[j - 1]] = face[(j + 1) % len(face)]
        start = min(nxt)
        order = [start]
        while nxt[order[-1]] != start:
            order.append(nxt[order[-1]])
            assert len(order) <= len(nxt)
        assert len(order) == len(nxt)
        rotations[v] = order
    assert set(rotations[0]) == {1, 2, 3, 4, 7}
    assert set(rotations[1]) == {0, 2, 5, 6, 7}
    rots = {u: [v for v in rotations[u] if v >= 2] for u in range(2, n)}
    seen = set()
    facial = []
    for u in rots:
        for v in rots[u]:
            if (u, v) in seen:
                continue
            face = []
            a, b = u, v
            while (a, b) not in seen:
                seen.add((a, b))
                face.append(a)
                a, b = b, rots[b][(rots[b].index(a) + 1) % len(rots[b])]
            facial.append(face)
    assert len([f for f in facial if len(f) == 6 and set(f) == set(CYCLE)]) == 1
    assert n - 2 - (len(edges) - 9) + len(facial) == 2


def full_boundary_partition(parts):
    return tuple(tuple(sorted(tuple(v for v in b if v in CYCLE)
                              for b in blocks if set(b) & set(CYCLE))) for blocks in parts)


def summarize(rows, old_vertices, old_edges, components):
    vertices = old_vertices + NEW
    edges = tuple(sorted(set(old_edges) | set(ADDED)))
    extensions = sorted(row + ext for row in rows
                        for ext in permutations(sorted(set(range(4)) - {row[0], row[1]})))
    old_set, ext_set = set(rows), set(extensions)
    lookup = {row: i for i, row in enumerate(rows)}
    ext_lookup = {row: i for i, row in enumerate(extensions)}
    old_actions = []
    new_actions = []
    boundaries = Counter()
    new_boundaries = Counter()
    old_fixed = []
    remote_checks = []
    extra_actions = 0
    neighbour_i = neighbour_ii = 0
    old_connected = dict()
    for i, row in enumerate(rows):
        parts = components(row, old_vertices, old_edges)
        f = dict(zip(old_vertices, row))
        boundaries[tuple(f[v] for v in CYCLE)] += 1
        record = []
        for p, blocks in enumerate(parts):
            for block in blocks:
                target = normalize(tuple(sum(PAIRS[p]) - f[v] if v in block else f[v]
                                         for v in old_vertices))
                assert target in old_set
                record.append((p, tuple(block), lookup[target]))
        old_actions.append(record)
        if tuple(f[v] for v in CYCLE) == (0, 1, 2, 1, 2, 1):
            old_fixed.append(row)
            idx12, idx02 = PAIRS.index((1, 2)), PAIRS.index((0, 2))
            remotes = [b for b in parts[idx12] if not set(b) & set(CYCLE)]
            status = []
            for bits in product((False, True), repeat=len(remotes)):
                selected = {v for yes, b in zip(bits, remotes) if yes for v in b}
                changed = tuple(3 - f[v] if v in selected else f[v] for v in old_vertices)
                changed_parts = components(changed, old_vertices, old_edges)
                zblock = next(b for b in changed_parts[idx02] if 2 in b)
                status.append({4, 5} <= set(zblock))
                for ext in permutations((2, 3)):
                    newrow = changed + ext
                    newparts = components(newrow, vertices, edges)
                    assert full_boundary_partition(newparts) == full_boundary_partition(changed_parts)
                    newremotes = [b for b in newparts[idx12] if not set(b) & set(CYCLE)]
                    assert newremotes == remotes
            old_connected[row] = all(status)
            remote_checks.append(dict(source=list(row), remote_components=[list(b) for b in remotes],
                                      all_subset_connection_status=status))
    for i, row in enumerate(extensions):
        f = dict(zip(vertices, row))
        oldrow = row[:-2]
        oldparts = components(oldrow, old_vertices, old_edges)
        parts = components(row, vertices, edges)
        assert full_boundary_partition(parts) == full_boundary_partition(oldparts)
        assert all(f[u] != f[v] for u, v in edges)
        new_boundaries[tuple(f[v] for v in CYCLE)] += 1
        record = []
        projected = []
        for p, blocks in enumerate(parts):
            for block in blocks:
                restriction = tuple(v for v in block if v in old_vertices)
                if restriction:
                    assert restriction in oldparts[p]
                    projected.append((p, restriction))
                else:
                    extra_actions += 1
                    assert set(block) == set(NEW)
                target = normalize(tuple(sum(PAIRS[p]) - f[v] if v in block else f[v]
                                         for v in vertices))
                assert target in ext_set
                record.append((p, tuple(block), ext_lookup[target]))
        assert sorted(projected) == sorted((p, b) for p, bs in enumerate(oldparts) for b in bs)
        # Both fibre points are related by the wholly new unused-colour edge.
        swapped_ext = oldrow + tuple(reversed(row[-2:]))
        assert any(extensions[j] == swapped_ext and set(b) == set(NEW) for _, b, j in record)
        new_actions.append(record)
        if tuple(f[v] for v in CYCLE) == (0, 1, 2, 1, 2, 1):
            idx12 = PAIRS.index((1, 2))
            boundary = next(b for b in parts[idx12] if 3 in b)
            neighbors = {v if u == 2 else u for u, v in edges if 2 in (u, v)}
            neighbour_i += any(f[v] == 2 for v in neighbors & set(boundary))
            remotes = [b for b in parts[idx12] if not set(b) & set(CYCLE)]
            neighbour_ii += any({f[v] for v in neighbors & set(b)} == {1, 2} for b in remotes)
    assert new_boundaries == Counter({r: 2 * count for r, count in boundaries.items()})
    # Literal fibres include all 4096 words; each canonical row has 24 common colour frames.
    literal_old = Counter()
    for row in rows:
        for perm in permutations(range(4)):
            literal_old[tuple(perm[row[v - 2]] for v in CYCLE)] += 1
    literal_fibres = [dict(row=list(word), old_lifts=literal_old[word], new_lifts=2 * literal_old[word])
                      for word in product(range(4), repeat=6)]
    return dict(old_normalized_colorings=[list(r) for r in rows],
                decorated_normalized_colorings=[list(r) for r in extensions],
                complete_literal_boundary_fibre_counts=literal_fibres,
                all_old_transition_sha256=sha256(encode(old_actions)).hexdigest(),
                all_new_transition_sha256=sha256(encode(new_actions)).hexdigest(),
                remote_subset_checks=remote_checks,
                counts=dict(old_normalized=len(rows), decorated_normalized=len(extensions),
                            old_literal=24 * len(rows), decorated_literal=24 * len(extensions),
                            old_single_component_actions=sum(map(len, old_actions)),
                            new_single_component_actions=sum(map(len, new_actions)),
                            wholly_new_actions=extra_actions,
                            literal_boundary_words=len(literal_fibres),
                            old_fixed_012121=len(old_fixed), new_fixed_012121=2 * len(old_fixed),
                            new_neighbor_alternative_i=neighbour_i,
                            new_neighbor_alternative_ii=neighbour_ii,
                            old_remote02_robust=sum(old_connected.values()),
                            decorated_remote02_robust=2 * sum(old_connected.values())))


def make_certificate():
    import four_color_three_step_cross_split_exclusion as old
    import four_color_three_step_kempe_escape as kempe
    old_edges = old.BUFFER19_H_EDGES
    old_faces = old.BUFFER19_G_FACES
    faces = []
    for face in old_faces:
        if face == (2, 3, 10):
            # K4 on {2,3,19,20}, inserted inside the old face adjacent to edge23.
            faces += [(2, 3, 20), (3, 19, 20), (19, 2, 20), (2, 19, 3, 10)]
        else:
            faces.append(face)
    inner = old.CENTER_ONLY_EDGES
    decorated_edges = tuple(sorted(set(old_edges) | set(ADDED)))
    check_embedding(19, tuple(sorted(set(old_edges) | set(inner))), old_faces)
    check_embedding(21, tuple(sorted(set(decorated_edges) | set(inner))), faces)
    rows = kempe.enumerate_normalized(17, old_edges)
    data = summarize(rows, tuple(range(2, 19)), old_edges, dfs_components)
    data.update(schema='three-step-edge-k4-decoration-v1', old_g_vertices=19,
                decorated_g_vertices=21, original_cycle=CYCLE,
                old_h_edges=old_edges, decorated_h_edges=decorated_edges,
                old_g_faces=old_faces, decorated_g_faces=faces,
                new_vertices=NEW, added_edges=ADDED,
                scope='Finite BUFFER verification of a general paper decoration theorem; D16 exclusion remains OPEN.')
    return data


def replay(path):
    data = json.loads(path.read_text())
    old_edges = tuple(map(tuple, data['old_h_edges']))
    decorated_edges = tuple(map(tuple, data['decorated_h_edges']))
    inner = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 7), (1, 2), (1, 5), (1, 6), (1, 7))
    assert data['old_g_vertices'] == 19 and data['decorated_g_vertices'] == 21
    assert tuple(data['new_vertices']) == NEW and tuple(map(tuple, data['added_edges'])) == ADDED
    assert set(decorated_edges) == set(old_edges) | set(ADDED)
    check_embedding(19, tuple(sorted(set(old_edges) | set(inner))), data['old_g_faces'])
    check_embedding(21, tuple(sorted(set(decorated_edges) | set(inner))), data['decorated_g_faces'])
    rows = enum_independent(tuple(range(2, 19)), old_edges)
    # Enumerate decorated complete colourings independently too, rather than relying on factor2.
    ext_rows = enum_independent(tuple(range(2, 21)), decorated_edges)
    assert ext_rows == sorted(row + ext for row in rows for ext in permutations((2, 3)))
    expected = summarize(rows, tuple(range(2, 19)), old_edges, union_components)
    for key, value in expected.items():
        assert value == data[key], key
    return dict(passed=True, independent_enumeration='DSATUR, literal colors after fixed ordered edge',
                independent_components='union-find', counts=data['counts'],
                source_sha256=sha256(path.read_bytes()).hexdigest(),
                scope=data['scope'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out-dir', type=Path)
    p.add_argument('--replay', type=Path)
    args = p.parse_args()
    if args.replay:
        print(json.dumps(replay(args.replay), indent=2))
        return
    if args.out_dir is None:
        p.error('--out-dir or --replay is required')
    args.out_dir.mkdir(parents=True, exist_ok=False)
    data = make_certificate()
    path = args.out_dir / 'results.json'
    path.write_text(json.dumps(data, separators=(',', ':')) + '\n')
    names = ('four_color_three_step_attachment_decoration.py', 'four_color_three_step_kempe_escape.py',
             'four_color_three_step_cross_split_exclusion.py', 'ck_kempe_obstruction.py',
             'four_color_counts_cone_verification.py')
    manifest = dict(base_sha=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    inputs={str(Path('scripts') / n): sha256((ROOT / 'scripts' / n).read_bytes()).hexdigest() for n in names},
                    outputs={'results.json': sha256(path.read_bytes()).hexdigest()})
    (args.out_dir / 'verification.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(data['counts'], indent=2))


if __name__ == '__main__':
    main()
