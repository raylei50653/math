#!/usr/bin/env python3
"""Exact original-path cuts, complete side fibres and D16 rectangle certificates.

The three saved planar controls are finite evidence only.  This program checks
all separator assignments, including empty fibres, and never identifies two
original vertices or joins independently renamed colour frames.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import four_color_three_step_cross_split_exclusion as controls

COLORS = range(4)
C0 = controls.CYCLE
S = {tuple(map(int, word)) for word in (
    '010201 010212 010213 010231 012012 012021 012102 012121 '
    '012123 012132 012301 012302 012312 012313 012321 012323'
).split()}


def norm(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def enumerate_rows(vertices, edges):
    """Enumerate full literal assignments by original vertex identity."""
    pos = {v: i for i, v in enumerate(vertices)}
    earlier = [[] for _ in vertices]
    for u, v in edges:
        a, b = sorted((pos[u], pos[v]))
        earlier[b].append(a)
    row = [0] * len(vertices)
    def visit(i):
        if i == len(vertices):
            yield tuple(row)
            return
        forbidden = {row[j] for j in earlier[i]}
        for c in COLORS:
            if c not in forbidden:
                row[i] = c
                yield from visit(i + 1)
    return list(visit(0))


def path23(edges, f):
    adj = defaultdict(list)
    for u, v in edges:
        if f[u] in (2, 3) and f[v] in (2, 3):
            adj[u].append(v)
            adj[v].append(u)
    queue = deque([(4,)])
    seen = {4}
    while queue:
        path = queue.popleft()
        if path[-1] == 5:
            return path
        for v in sorted(adj[path[-1]]):
            if v not in seen:
                seen.add(v)
                queue.append(path + (v,))
    raise AssertionError('No original 23 path')


def cut_faces(embedding, path):
    faces = embedding['h_oriented_faces']
    outer = next(i for i, f in enumerate(faces) if len(f) == 6 and set(f) == set(C0))
    cuts = {tuple(sorted(e)) for e in zip(path, path[1:])}
    incidence = defaultdict(list)
    for i, face in enumerate(faces):
        for e in zip(face, face[1:] + face[:1]):
            incidence[tuple(sorted(e))].append(i)
    dual = defaultdict(set)
    for edge, incident in incidence.items():
        assert len(incident) == 2
        a, b = incident
        if outer not in incident and edge not in cuts:
            dual[a].add(b)
            dual[b].add(a)
    unseen = set(range(len(faces))) - {outer}
    regions = []
    while unseen:
        region = {min(unseen)}
        queue = list(region)
        for a in queue:
            for b in dual[a] - region:
                region.add(b)
                queue.append(b)
        unseen -= region
        regions.append(region)
    assert len(regions) == 2
    sides = []
    for region in regions:
        edges = sorted({tuple(sorted(e)) for i in region
                        for e in zip(faces[i], faces[i][1:] + faces[i][:1])})
        vertices = sorted({v for edge in edges for v in edge})
        # Preserve the embedding order of every actual edge attaching to L.
        rotation = defaultdict(dict)
        for face in faces:
            for j, u in enumerate(face):
                rotation[u][face[j - 1]] = face[(j + 1) % len(face)]
        attachments = []
        edge_set = set(edges)
        for u in path:
            nxt = rotation[u]
            start = min(nxt)
            cyclic = [start]
            while nxt[cyclic[-1]] != start:
                cyclic.append(nxt[cyclic[-1]])
            attachments.append([u, [v for v in cyclic
                                     if v not in path and tuple(sorted((u, v))) in edge_set]])
        sides.append(dict(vertices=vertices, edges=edges,
                          original_face_indices=sorted(region),
                          ordered_path_attachments=attachments))
    zside = next(s for s in sides if 2 in s['vertices'])
    wside = next(s for s in sides if 7 in s['vertices'])
    assert zside is not wside
    assert set(zside['vertices']) & set(wside['vertices']) == set(path)
    assert set(map(tuple, zside['edges'])) & set(map(tuple, wside['edges'])) == cuts
    return zside, wside


def build_side(side, path, arc):
    vertices = side['vertices']
    pos = {v: i for i, v in enumerate(vertices)}
    rows = enumerate_rows(vertices, side['edges'])
    fibres = {lam: [] for lam in product(COLORS, repeat=len(path))}
    for i, row in enumerate(rows):
        fibres[tuple(row[pos[v]] for v in path)].append(i)
    side.update(arc_order=list(arc), colorings=rows)
    return fibres, {
        lam: sorted({tuple(rows[i][pos[v]] for v in arc) for i in ids})
        for lam, ids in fibres.items()
    }


def accepted(word):
    f = dict(zip(C0, word))
    return [(x, y) for x, y in product(COLORS, repeat=2)
            if all((f | {0: x, 1: y})[u] != (f | {0: x, 1: y})[v]
                   for u, v in controls.CENTER_ONLY_EDGES)]


def rectangle_tables():
    records = []
    for b, c in ((2, 2),):
        for ts in ((0, 1), (3,), (0, 1, 3)):
            proper = [u for u in product(COLORS, repeat=3)
                      if all(u[1] != b and u[2] != c and u[0] not in (u[1], u[2])
                             and t not in (b, c) for t in ts)]
            allowed = [u for u in proper
                       if all(norm((u[0], u[1], b, t, c, u[2])) in S for t in ts)]
            records.append(dict(end_colors=[b, c], right_support=list(ts),
                                allowed_left_triples=allowed))
    assert [len(r['allowed_left_triples']) for r in records] == [9, 12, 6]
    return records


def remote_lock_check(vertices, edges, full):
    """Construct escape if neither alternative of the remote-neighbour lemma holds."""
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    records = []
    for row in sorted(full):
        f = dict(zip(vertices, row))
        if tuple(f[v] for v in C0) != (0, 1, 2, 1, 2, 1):
            continue
        remaining = {v for v in vertices if f[v] in (1, 2)}
        comps = []
        while remaining:
            comp = {min(remaining)}
            queue = list(comp)
            for u in queue:
                for v in (adjacency[u] & remaining) - comp:
                    comp.add(v)
                    queue.append(v)
            comps.append(comp)
            remaining -= comp
        boundary = next(k for k in comps if 3 in k)
        assert boundary & set(C0) == {3, 4, 7, 5, 6}
        remote = [k for k in comps if k is not boundary]
        alternative_i = sorted(v for v in adjacency[2] & boundary if f[v] == 2)
        mixed = [sorted(k) for k in remote
                 if {f[v] for v in adjacency[2] & k} == {1, 2}]
        record = dict(source=row, boundary_12_component=sorted(boundary),
                      all_remote_12_components=[sorted(k) for k in remote],
                      boundary_color2_neighbors=alternative_i,
                      remote_components_with_both_neighbor_colors=mixed)
        if not alternative_i and not mixed:
            selected = [k for k in remote if any(f[v] == 2 for v in adjacency[2] & k)]
            g = dict(f)
            for k in selected:
                for v in k:
                    g[v] = 3 - g[v]
            assert tuple(g[v] for v in C0) == (0, 1, 2, 1, 2, 1)
            assert all(g[v] != 2 for v in adjacency[2])
            h = dict(g)
            h[2] = 2
            target = tuple(h[v] for v in vertices)
            assert target in full
            assert tuple(h[v] for v in C0) == (2, 1, 2, 1, 2, 1)
            record['escape'] = dict(swapped_remote_components=[sorted(k) for k in selected],
                                    intermediate=tuple(g[v] for v in vertices), target=target,
                                    center_lifts=accepted((2, 1, 2, 1, 2, 1)))
        records.append(record)
    return dict(fixed_literal_20_lifts=len(records),
                alternative_i_holds=sum(bool(r['boundary_color2_neighbors']) for r in records),
                alternative_ii_holds=sum(bool(r['remote_components_with_both_neighbor_colors']) for r in records),
                explicit_escapes=sum('escape' in r for r in records), records=records)


def verify_control(name, n, edges, faces, witness):
    embedding = controls.verify_sphere_and_disk_embedding(n, edges, faces)
    f = dict(zip(range(2, n), witness))
    path = path23(edges, f)
    zside, wside = cut_faces(embedding, path)
    zfib, us = build_side(zside, path, (2, 3, 6))
    wfib, ts = build_side(wside, path, (7,))
    vertices = tuple(range(2, n))
    zpos = {v: i for i, v in enumerate(zside['vertices'])}
    wpos = {v: i for i, v in enumerate(wside['vertices'])}
    full = set(enumerate_rows(vertices, edges))
    reconstructed = set()
    records = []
    first_escape = None
    for lam in zfib:
        violations = []
        for u in us[lam]:
            for (t,) in ts[lam]:
                row = (u[0], u[1], lam[0], t, lam[-1], u[2])
                if norm(row) not in S:
                    violations.append([list(u), t])
        for zi in zfib[lam]:
            for wi in wfib[lam]:
                zr = zside['colorings'][zi]
                wr = wside['colorings'][wi]
                glued = tuple(zr[zpos[v]] if v in zpos else wr[wpos[v]] for v in vertices)
                assert glued in full
                assert glued not in reconstructed
                reconstructed.add(glued)
                row = tuple(glued[v - 2] for v in C0)
                if first_escape is None and norm(row) not in S and accepted(row):
                    first_escape = dict(separator=list(lam), left_coloring_index=zi,
                                        right_coloring_index=wi, full_h_coloring=glued,
                                        c0_row=row, center_lifts=accepted(row))
        records.append(dict(separator=list(lam), left_fibre=zfib[lam],
                            right_fibre=wfib[lam], left_triples=us[lam],
                            right_colors=[r[0] for r in ts[lam]],
                            forbidden_rectangles=violations))
    assert reconstructed == full
    seed_lam = tuple(f[v] for v in path)
    seed = next(r for r in records if tuple(r['separator']) == seed_lam)
    assert {0, 1}.issubset(set(seed['right_colors']))
    seed_escape = None
    for u, t in seed['forbidden_rectangles']:
        row = (u[0], u[1], 2, t, 2, u[2])
        if accepted(row):
            zi = next(i for i in seed['left_fibre']
                      if tuple(zside['colorings'][i][zpos[v]] for v in (2, 3, 6)) == tuple(u))
            wi = next(i for i in seed['right_fibre'] if wside['colorings'][i][wpos[7]] == t)
            zr, wr = zside['colorings'][zi], wside['colorings'][wi]
            glued = tuple(zr[zpos[v]] if v in zpos else wr[wpos[v]] for v in vertices)
            seed_escape = dict(separator=list(seed_lam), left_coloring_index=zi,
                               right_coloring_index=wi, full_h_coloring=glued,
                               c0_row=row, center_lifts=accepted(row))
            break
    return dict(name=name, original_h_vertex_order=vertices, embedding=embedding,
                path=path, seed_coloring=witness, left=zside, right=wside,
                remote_lock_check=remote_lock_check(vertices, edges, full),
                separator_fibres=records,
                verification=dict(h_colorings=len(full), joined_colorings=len(reconstructed),
                                  all_fibres_including_empty=len(records),
                                  nonempty_common_separator_fibres=sum(bool(zfib[x] and wfib[x]) for x in zfib),
                                  seed_separator=list(seed_lam), seed_left_triples=seed['left_triples'],
                                  seed_right_colors=seed['right_colors'],
                                  seed_forbidden_rectangles=len(seed['forbidden_rectangles']),
                                  seed_accepted_escape=seed_escape,
                                  some_accepted_escape=first_escape))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    cases = [
        ('RADIAL-MINDEG5-14', 14, controls.RADIAL14_H_EDGES, controls.RADIAL14_G_FACES, controls.RADIAL14_WITNESS_H),
        ('THETA-VIOLATOR-12', 12, controls.THETA12_H_EDGES, controls.THETA12_G_FACES, controls.THETA12_WITNESS_H),
        ('BUFFER-2STEP-19', 19, controls.BUFFER19_H_EDGES, controls.BUFFER19_G_FACES, controls.BUFFER19_WITNESS_H),
    ]
    paths = []
    summaries = []
    for case in cases:
        result = verify_control(*case)
        path = args.out_dir / (case[0].lower() + '.json')
        path.write_text(json.dumps(result, separators=(',', ':')) + '\n')
        paths.append(path)
        summaries.append(dict(name=case[0], path=result['path'], **result['verification']))
    result = dict(claim='Finite exact cut/rejoin checks; general D16 exclusion remains OPEN.',
                  rectangle_tables=rectangle_tables(), controls=summaries)
    path = args.out_dir / 'results.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    paths.append(path)
    sources = [Path(__file__), Path(controls.__file__)]
    manifest = {str(p.resolve()): sha256(p.read_bytes()).hexdigest() for p in sources + paths}
    (args.out_dir / 'verification.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for summary in summaries:
        print(summary['name'], 'full:', summary['h_colorings'], 'seed U/T:',
              len(summary['seed_left_triples']), summary['seed_right_colors'],
              'forbidden:', summary['seed_forbidden_rectangles'])


if __name__ == '__main__':
    main()
