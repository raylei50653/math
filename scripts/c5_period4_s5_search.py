#!/usr/bin/env python3
"""Exact bounded fixed-rotation search for the prescribed five-step return.

Input: plantri ASCII rotation systems. No isomorphism or boundary dihedral
quotient is taken by this checker. For each stored rotation, every degree-five
center is checked using precisely that rotation's displayed neighbor order.
Graph generation completeness is a separate plantri dependency; replay of
these concrete input graphs and their complete ABACD fibres is self-contained.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audits/2026-10-30-c5-period4-s5'
PLANTRI = ROOT / 'audits/2026-10-14-r6-319-enumeration-676b102/src/plantri'
STEPS = (((0, 3), 2), ((1, 3), 4), ((1, 2), 1), ((0, 2), 3), ((0, 3), 0))
BOUNDARIES = ((0, 1, 3, 2, 3), (0, 1, 3, 2, 1), (0, 2, 3, 2, 1),
              (0, 2, 3, 0, 1), (3, 2, 3, 0, 1))
ALIGN = (2, 3, 1, 0)


def parse(line):
    order, raw = line.split()
    rotation = [[ord(x) - ord('a') for x in row] for row in raw.split(',')]
    assert int(order) == len(rotation)
    return rotation


def sphere_faces(rotation):
    n = len(rotation)
    unseen = {(u, v) for u, vs in enumerate(rotation) for v in vs}
    assert len(unseen) == sum(map(len, rotation))
    assert all(u != v and (v, u) in unseen for u, v in unseen)
    answer = []
    while unseen:
        u, v = first = min(unseen)
        face = []
        while True:
            unseen.remove((u, v))
            face.append(u)
            vs = rotation[v]
            w = vs[(vs.index(u) - 1) % len(vs)]
            u, v = v, w
            if (u, v) == first:
                break
        assert len(face) == len(set(face)) == 3
        answer.append(face)
    assert n - sum(map(len, rotation)) // 2 + len(answer) == 2
    # Verify a single sphere: the rotation graph is connected.
    seen, todo = {0}, [0]
    for u in todo:
        for v in rotation[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    assert len(seen) == n
    return answer


def structural_test(rotation, faces):
    """All simple cycles of length 3..5, with their actual open sides."""
    n = len(rotation)
    adj = list(map(set, rotation))
    assert min(map(len, adj)) >= 5
    owners = defaultdict(list)
    for j, f in enumerate(faces):
        for i in range(3):
            owners[tuple(sorted((f[i], f[(i + 1) % 3])))].append(j)
    assert all(len(rows) == 2 for rows in owners.values())
    counts = {3: 0, 4: 0, 5: 0}
    bad34, bad5 = [], []
    for root in range(n):
        stack = [[root]]
        while stack:
            path = stack.pop()
            u = path[-1]
            if len(path) >= 3 and root in adj[u] and path[1] < path[-1]:
                length = len(path)
                counts[length] += 1
                cut = {tuple(sorted((path[i], path[(i + 1) % length]))) for i in range(length)}
                unseen, sides = set(range(len(faces))), []
                while unseen:
                    first = min(unseen)
                    unseen.remove(first)
                    todo = [first]
                    for j in todo:
                        f = faces[j]
                        for i in range(3):
                            edge = tuple(sorted((f[i], f[(i + 1) % 3])))
                            if edge in cut:
                                continue
                            for k in owners[edge]:
                                if k in unseen:
                                    unseen.remove(k)
                                    todo.append(k)
                    sides.append(sorted({v for j in todo for v in faces[j]} - set(path)))
                assert len(sides) == 2
                assert not set(sides[0]) & set(sides[1])
                assert set(sides[0]) | set(sides[1]) == set(range(n)) - set(path)
                sides.sort(key=lambda row: (len(row), row))
                if length <= 4 and sides[0]:
                    bad34.append(dict(cycle=path, sides=sides))
                if length == 5 and len(sides[0]) >= 2:
                    bad5.append(dict(cycle=path, sides=sides))
            if len(path) < 5:
                for v in sorted(rotation[u], reverse=True):
                    if v > root and v not in path:
                        stack.append(path + [v])
    return dict(degrees=list(map(len, adj)), short_cycle_counts=counts,
                separating34=bad34, forbidden5=bad5,
                legal=not bool(bad34 or bad5))


def fibre(adj):
    """Every literal complete coloring with the displayed ABACD boundary."""
    n = len(adj)
    colors = [0, 1, 0, 2, 3] + [-1] * (n - 5)
    answer = []
    def visit():
        todo = [v for v in range(5, n) if colors[v] < 0]
        if not todo:
            answer.append(tuple(colors))
            return
        avail = {v: set(range(4)) - {colors[w] for w in adj[v]} for v in todo}
        v = min(todo, key=lambda v: (len(avail[v]), -len(adj[v]), v))
        for x in sorted(avail[v]):
            colors[v] = x
            visit()
        colors[v] = -1
    visit()
    return sorted(answer)


def component(adj, colors, pair, root):
    assert colors[root] in pair
    seen, todo = {root}, [root]
    for u in todo:
        for v in sorted(adj[u]):
            if colors[v] in pair and v not in seen:
                seen.add(v)
                todo.append(v)
    return seen


def one_round(adj, colors, with_moves=False):
    q, moves = colors, []
    for (pair, root), expected in zip(STEPS, BOUNDARIES):
        comp = component(adj, q, pair, root)
        q = tuple(sum(pair) - x if v in comp else x for v, x in enumerate(q))
        if with_moves:
            moves.append(dict(pair=pair, root=root, component=sorted(comp), colors=q))
        if q[:5] != expected:
            return None, moves
    return tuple(ALIGN[x] for x in q), moves


def cycles_of(partial):
    cycles, seen = [], set()
    for start in sorted(partial):
        q, path, local = start, [], {}
        while q in partial and q not in local and q not in seen:
            local[q] = len(path)
            path.append(q)
            q = partial[q]
        if q in local:
            cycles.append(path[local[q]:])
        seen.update(path)
    return cycles


def witness(name, rotation, faces, center, order, adj, cycle):
    rounds = []
    for j, colors in enumerate(cycle):
        target, moves = one_round(adj, colors, True)
        assert target == cycle[(j + 1) % len(cycle)]
        rounds.append(dict(source_colors=colors,
                           moves=[dict(pair=m['pair'], root=order[m['root']],
                                       component=[order[v] for v in m['component']], colors=m['colors'])
                                  for m in moves], normalized_colors=target))
    edges = sorted((u, v) for u, row in enumerate(rotation) for v in row if u < v)
    return dict(name=name, n=len(rotation), original_edges=edges, sphere_faces=faces,
                rotation=rotation, center=center, boundary=rotation[center],
                exterior_vertices=order, exterior_edges=[e for e in edges if center not in e],
                cycle=cycle, rounds=rounds)


def scan(paths):
    domains, witnesses = [], []
    for path in paths:
        records = []
        for graph_id, line in enumerate(path.read_text().splitlines()):
            rotation = parse(line)
            faces = sphere_faces(rotation)
            geo = structural_test(rotation, faces)
            centers = []
            if geo['legal']:
                for center, boundary in enumerate(rotation):
                    if len(boundary) != 5:
                        continue
                    order = boundary + sorted(set(range(len(rotation))) - set(boundary) - {center})
                    index = {u: j for j, u in enumerate(order)}
                    adj = [{index[w] for w in rotation[u] if w != center} for u in order]
                    colors = fibre(adj)
                    partial = {}
                    for c in colors:
                        target, _ = one_round(adj, c)
                        if target is not None:
                            partial[c] = target
                    assert set(partial.values()) <= set(colors)
                    assert len(set(partial.values())) == len(partial)
                    cycles = cycles_of(partial)
                    centers.append(dict(center=center, boundary=boundary, fibre_size=len(colors),
                                        complete_rounds=len(partial), cycle_lengths=list(map(len, cycles))))
                    for cyc in cycles:
                        if len(cyc) == 4:
                            witnesses.append(witness(f'{path.name}:{graph_id}:v{center}', rotation,
                                                     faces, center, order, adj, cyc))
            records.append(dict(graph=graph_id, topology=geo, centers=centers))
            if (graph_id + 1) % 100 == 0:
                print(f'{path.name}: {graph_id + 1} graphs, {len(witnesses)} period-four witnesses', flush=True)
        domains.append(dict(input=str(path.relative_to(ROOT)), sha256=sha256(path.read_bytes()).hexdigest(),
                            records=records))
        print(f'{path.name}: finished {len(records)} graphs', flush=True)
    summary = []
    for d in domains:
        legal = [r for r in d['records'] if r['topology']['legal']]
        centers = [c for r in legal for c in r['centers']]
        summary.append(dict(input=d['input'], graphs=len(d['records']), legal=len(legal),
                            degree5_centers=len(centers), fibre_states=sum(c['fibre_size'] for c in centers),
                            complete_rounds=sum(c['complete_rounds'] for c in centers),
                            cycle_lengths=[k for c in centers for k in c['cycle_lengths']]))
    result = dict(schema='c5-period4-s5-bounded-search-v1',
                  scope='Every stored rotation, every degree-five center; boundary is exactly the displayed neighbor order. All complete literal ABACD fibre colorings; actual full-O components. No boundary rotation/reflection quotient or additional frames are used.',
                  trust='Concrete input replay is independent of plantri classification. Catalogue completeness depends on external plantri generation. Finite no-witness result is not a universal theorem. Full Kempe blockedness requires independent replay of each witness.',
                  generation_binary=str(PLANTRI.relative_to(ROOT)),
                  generation_binary_sha256=sha256(PLANTRI.read_bytes()).hexdigest(),
                  summary=summary, domains=domains, witnesses=witnesses)
    return result


def control_report():
    path = ROOT / 'audits/2026-10-29-kempe-realizability/source/controls.json'
    rows = []
    for item in json.loads(path.read_text())['controls']:
        n = item['deleted_vertex'] + 1
        original_adj = [set() for _ in range(n)]
        for u, v in item['original_edges']:
            original_adj[u].add(v)
            original_adj[v].add(u)
        geo = structural_test([sorted(row) for row in original_adj], item['sphere_faces'])
        assert geo['legal'] == item['topology']['satisfies_structural_class']
        adj = [set() for _ in range(n - 1)]
        for u, v in item['exterior_edges']:
            adj[u].add(v)
            adj[v].add(u)
        colors, partial = fibre(adj), {}
        for c in colors:
            target, _ = one_round(adj, c)
            if target is not None:
                partial[c] = target
        cycles = cycles_of(partial)
        rows.append(dict(name=item['name'], original_edges=item['original_edges'],
                         sphere_faces=item['sphere_faces'], boundary=item['boundary'],
                         deleted_vertex=item['deleted_vertex'], source_structural_class=geo['legal'],
                         source_forbidden5=geo['forbidden5'], fibre_size=len(colors),
                         complete_rounds=len(partial), cycle_lengths=list(map(len, cycles)), cycles=cycles))
    assert rows[0]['cycle_lengths'] == [4] and not rows[0]['source_structural_class']
    assert all(row['source_structural_class'] and not row['cycle_lengths'] for row in rows[1:])
    return dict(schema='c5-period4-negative-controls-v1', input=str(path.relative_to(ROOT)),
                input_sha256=sha256(path.read_bytes()).hexdigest(), rows=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--min-order', type=int, default=12)
    parser.add_argument('--max-order', type=int, default=24)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--controls', action='store_true', help='Replay the frozen Errera and five flip controls only')
    args = parser.parse_args()
    if args.controls:
        encoded = json.dumps(control_report(), indent=2) + '\n'
        target = OUT / 'search-control-check.json'
        if args.check:
            assert target.read_text() == encoded
        else:
            target.write_text(encoded)
        print('CONTROL CHECK OK' if args.check else 'CONTROLS CREATED')
        return
    folder = OUT / 'search-inputs'
    folder.mkdir(parents=True, exist_ok=True)
    paths = [folder / f'n{n}.ascii' for n in range(args.min_order, args.max_order + 1)]
    if args.generate:
        log = []
        for n, path in zip(range(args.min_order, args.max_order + 1), paths):
            command = [str(PLANTRI.relative_to(ROOT)), '-m5', '-c5', '-a', str(n), str(path.relative_to(ROOT))]
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True)
            log.append(dict(argv=command, stdout=run.stdout, stderr=run.stderr,
                            output_sha256=sha256(path.read_bytes()).hexdigest()))
        (OUT / 'search-generation.json').write_text(json.dumps(log, indent=2) + '\n')
    result = scan(paths)
    encoded = json.dumps(result, indent=2) + '\n'
    target = OUT / 'search-certificate.json'
    if args.check:
        assert target.read_text() == encoded
    else:
        target.write_text(encoded)
        (OUT / 'search-witnesses.json').write_text(json.dumps(dict(witnesses=result['witnesses']), indent=2) + '\n')
    print(json.dumps(dict(status='CHECK OK' if args.check else 'CREATED', summary=result['summary'],
                          witnesses=len(result['witnesses'])), sort_keys=True))


if __name__ == '__main__':
    main()
