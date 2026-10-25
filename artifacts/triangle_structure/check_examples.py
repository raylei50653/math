#!/usr/bin/env python3
"""Independently check the finite embedded examples, numbering, and colour counts.

Run: python3 artifacts/triangle_structure/check_examples.py
Only the six explicit examples are checked; this is not a graph enumeration.
"""

import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent


def edge(u, v):
    return tuple(sorted((u, v)))


def signed_area(points):
    return sum(
        a[0] * b[1] - a[1] * b[0]
        for a, b in zip(points, points[1:] + points[:1])
    ) / 2


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def connected(adjacency):
    if not adjacency:
        return False
    reached = {next(iter(adjacency))}
    queue = deque(reached)
    while queue:
        for v in adjacency[queue.popleft()]:
            if v not in reached:
                reached.add(v)
                queue.append(v)
    return len(reached) == len(adjacency)


def colour_count(adjacency, q):
    """Exhaustive assignments, fixing one colour then restoring its q choices."""
    order = sorted(adjacency, key=lambda v: (-len(adjacency[v]), v))
    colours = {order[0]: 0}

    def visit(i):
        if i == len(order):
            return 1
        v = order[i]
        forbidden = {colours[u] for u in adjacency[v] if u in colours}
        count = 0
        for colour in range(q):
            if colour not in forbidden:
                colours[v] = colour
                count += visit(i + 1)
        colours.pop(v, None)
        return count

    return q * visit(1)


def check(graph):
    points = {v['source_id']: (v['x'], v['y']) for v in graph['vertices']}
    assert len(points) == len(graph['vertices'])
    faces = graph['bounded_faces']
    boundary = graph['boundary']
    assert len(boundary) >= 3 and len(set(boundary)) == len(boundary)
    assert set(boundary) <= set(points)
    assert len({frozenset(f) for f in faces}) == len(faces)
    assert all(len(f) == 3 and len(set(f)) == 3 for f in faces)
    incidence = defaultdict(list)
    adjacency = {v: set() for v in points}
    links = {v: defaultdict(set) for v in points}
    areas = []
    for i, face in enumerate(faces):
        assert set(face) <= set(points)
        area = signed_area([points[v] for v in face])
        assert area > 0, (graph['id'], 'non-CCW face', i)
        areas.append(area)
        for j, u in enumerate(face):
            v, w = face[(j + 1) % 3], face[(j + 2) % 3]
            incidence[edge(u, v)].append((i, u, v))
            adjacency[u].add(v)
            adjacency[v].add(u)
            links[u][v].add(w)
            links[u][w].add(v)
    assert connected(adjacency)
    border = {edge(u, boundary[(i + 1) % len(boundary)]) for i, u in enumerate(boundary)}
    assert border == {e for e, inc in incidence.items() if len(inc) == 1}
    for e, inc in incidence.items():
        assert len(inc) in (1, 2)
        if len(inc) == 2:
            assert inc[0][1:] == inc[1][1:][::-1]
    for i, u in enumerate(boundary):
        v = boundary[(i + 1) % len(boundary)]
        assert incidence[edge(u, v)][0][1:] == (u, v)
    for v, link in links.items():
        assert connected(link)
        degrees = Counter(map(len, link.values()))
        if v in boundary:
            assert degrees[1] == 2 and set(degrees) <= {1, 2}
        else:
            assert set(degrees) == {2}
    outer_area = signed_area([points[v] for v in boundary])
    assert outer_area > 0 and abs(sum(areas) - outer_area) < 1e-8
    edges = list(incidence)
    for (u, v), (s, t) in itertools.combinations(edges, 2):
        if len({u, v, s, t}) < 4:
            continue
        a, b, c, d = (points[x] for x in (u, v, s, t))
        x, y, z, w = cross(a, b, c), cross(a, b, d), cross(c, d, a), cross(c, d, b)
        assert not (x * y < -1e-12 and z * w < -1e-12), 'crossing edges'
        for p in (c, d):
            if abs(cross(a, b, p)) < 1e-10:
                assert not (min(a[0], b[0]) - 1e-10 <= p[0] <= max(a[0], b[0]) + 1e-10
                            and min(a[1], b[1]) - 1e-10 <= p[1] <= max(a[1], b[1]) + 1e-10), 'overlap'
    n, m, t, b = len(points), len(edges), len(faces), len(boundary)
    assert m == 3 * n - b - 3 and t == 2 * n - b - 2
    curvature = sum((4 if v in boundary else 6) - len(ns) for v, ns in adjacency.items())
    assert curvature == 6

    numbered = graph['numbering']
    vids = {v['source_id']: v['vertex_id'] for v in numbered['vertices']}
    eids = {edge(*e['source_vertices']): e['edge_id'] for e in numbered['edges']}
    nf = numbered['faces']
    assert set(vids) == set(points) and set(vids.values()) == {f'v{i}' for i in range(n)}
    assert set(eids) == set(edges) and set(eids.values()) == {f'e{i}' for i in range(m)}
    assert [f['face_id'] for f in nf] == [f'f{i}' for i in range(t)]
    assert sorted(f['source_face'] for f in nf) == list(range(t))
    fids = {f['source_face']: f['face_id'] for f in nf}
    first_v, first_e = {}, {}
    for f in nf:
        i, ordered = f['source_face'], f['source_vertices']
        original = faces[i]
        assert any(ordered == original[j:] + original[:j] for j in range(3))
        assert f['entry_edge'] == ordered[:2]
        assert f['vertices'] == [vids[v] for v in ordered]
        for j, u in enumerate(ordered):
            v = ordered[(j + 1) % 3]
            first_v.setdefault(u, f'v{len(first_v)}')
            first_e.setdefault(edge(u, v), f'e{len(first_e)}')
            assert f['edges'][j] == eids[edge(u, v)]
            other = [k for k, _, _ in incidence[edge(u, v)] if k != i]
            assert f['neighbors'][j] == (fids[other[0]] if other else 'F∞')
    assert first_v == vids and first_e == eids
    assert nf[0]['source_vertices'][:2] == graph['root_edge']
    assert nf[0]['vertices'] == ['v0', 'v1', 'v2']
    dual = {i: set() for i in range(t)}
    for inc in incidence.values():
        if len(inc) == 2:
            i, j = inc[0][0], inc[1][0]
            dual[i].add(j)
            dual[j].add(i)
    distances = {nf[0]['source_face']: 0}
    queue = deque(distances)
    while queue:
        i = queue.popleft()
        for j in dual[i]:
            if j not in distances:
                distances[j] = distances[i] + 1
                queue.append(j)
    assert len(distances) == t
    assert [distances[f['source_face']] for f in nf] == sorted(distances.values())

    counts = {str(q): colour_count(adjacency, q) for q in (3, 4)}
    expected = {'wheel5': (0, 120), 'wheel6': (6, 264), 'wheel7': (0, 504),
                'k4': (0, 24), 'octahedron': (6, 96), 'octahedron-insert': (0, 96)}
    assert tuple(counts.values()) == expected[graph['id']]
    interior_degrees = sorted(len(adjacency[v]) for v in points if v not in boundary)
    assert bool(counts['3']) == all(d % 2 == 0 for d in interior_degrees)
    facial = {frozenset(f) for f in faces}
    if b == 3:
        facial.add(frozenset(boundary))
    nonfacial = [list(vs) for vs in itertools.combinations(points, 3)
                if all(v in adjacency[u] for u, v in itertools.combinations(vs, 2))
                and frozenset(vs) not in facial]
    return {'id': graph['id'], 'V': n, 'E': m, 'bounded_triangles': t, 'boundary_length': b,
            'interior_degrees': interior_degrees, 'disk_curvature_sum': curvature,
            'proper_vertex_colourings_with_named_colours': counts,
            'nonfacial_triangle_cycles': nonfacial,
            'checks': 'CCW incidence, disk links, areas, noncrossing edges, Euler, curvature, numbering, dual BFS levels, exhaustive colour counts'}


def main():
    path = HERE / 'examples.json'
    data = json.loads(path.read_text())
    results = [check(g) for g in data['examples']]
    output = {
        'scope': 'Six explicit finite simple triangulations of a disk with a simple outer cycle; not enumeration or a new general colouring theorem.',
        'examples_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'external_sources': [
            {'url': 'https://arxiv.org/html/1605.01688v4', 'use': 'Theorem 3: internally even near-triangulations are exactly the 3-colourable ones.'},
            {'url': 'https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt', 'use': 'Plane embedding requires cyclic orders; disk triangulation generation is available.'}],
        'numbering_contract': 'Root oriented boundary edge and orientation fixed; face-dual BFS; reuse original vertex identity; separate vertex, edge and face IDs. Numbering depends on root and graph.',
        'results': results,
    }
    (HERE / 'validation.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'checked': len(results), 'results': results}, ensure_ascii=False))


if __name__ == '__main__':
    main()
