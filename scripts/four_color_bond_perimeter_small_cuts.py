#!/usr/bin/env python3
"""Finite original-embedding audit of the 10/12 small-cut perimeter lemmas.

No colouring oracle and no abstract 9--11 incidence D-table enumeration.
The arbitrary-source bounds are paper arguments, not inferred from this sample.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]


def capped_antiprism(r):
    graph = nx.Graph()
    for i in range(r):
        j = (i + 1) % r
        graph.add_edges_from([(i, j), (r + i, r + j),
                              (i, r + i), (j, r + i),
                              (2 * r, i), (2 * r + 1, r + i)])
    return graph


def original_faces(embedding):
    seen, answer = set(), []
    for u in sorted(embedding):
        for v in embedding.neighbors_cw_order(u):
            if (u, v) not in seen:
                face = embedding.traverse_face(u, v, seen)
                assert len(face) == 3
                answer.append(face)
    return answer


def short_cycles(graph):
    answer = []
    for start in sorted(graph):
        def visit(path):
            last = path[-1]
            if 3 <= len(path) <= 5 and graph.has_edge(last, start) and path[1] < last:
                answer.append(tuple(path))
            if len(path) == 5:
                return
            for nxt in sorted(graph[last]):
                if nxt > start and nxt not in path:
                    visit(path + [nxt])
        visit([start])
    return sorted(answer)


def short_cycle_sides(graph, faces):
    dual = nx.Graph()
    dual.add_nodes_from(range(len(faces)))
    edge_faces = defaultdict(list)
    for j, face in enumerate(faces):
        for u, v in zip(face, face[1:] + face[:1]):
            edge_faces[tuple(sorted((u, v)))].append(j)
    for fs in edge_faces.values():
        assert len(fs) == 2
        dual.add_edge(*fs)
    checks = []
    for cycle in short_cycles(graph):
        cut_dual = dual.copy()
        for u, v in zip(cycle, cycle[1:] + cycle[:1]):
            cut_dual.remove_edge(*edge_faces[tuple(sorted((u, v)))])
        components = sorted(map(sorted, nx.connected_components(cut_dual)))
        assert len(components) == 2
        sides = sorted([sorted(set().union(*(set(faces[j]) for j in fs)) - set(cycle))
                        for fs in components])
        assert set(sides[0]).isdisjoint(sides[1])
        assert set(sides[0]) | set(sides[1]) == set(graph) - set(cycle)
        assert min(map(len, sides)) <= (0 if len(cycle) <= 4 else 1)
        checks.append(dict(cycle=cycle, side_vertices=sides))
    return checks


def connected(side, neighbor_masks):
    if not side:
        return False
    visited, frontier = 0, side & -side
    while frontier:
        visited |= frontier
        neighbors = 0
        bits = frontier
        while bits:
            bit = bits & -bits
            neighbors |= neighbor_masks[bit.bit_length() - 1]
            bits -= bit
        frontier = neighbors & side & ~visited
    return visited == side


def perimeter_walk(side, rotation, faces):
    if len(side) == 1:
        return [], [], 0
    expected = set()
    for face in faces:
        if sum(v in side for v in face) == 2:
            expected.update((u, v) for u, v in zip(face, face[1:] + face[:1])
                            if u in side and v in side)
    assert expected
    first = min(expected)
    restricted = {u: [v for v in rotation[u] if v in side] for u in side}
    u, v = first
    walk, darts = [], []
    while True:
        assert (u, v) not in darts
        walk.append(u)
        darts.append((u, v))
        neighbors = restricted[v]
        u, v = v, neighbors[(neighbors.index(u) - 1) % len(neighbors)]
        if (u, v) == first:
            break
    assert set(darts) == expected
    bridges = [list(edge) for edge in sorted({tuple(sorted((u, v))) for u, v in darts
                                             if (v, u) in expected})]
    return walk, bridges, len(expected)


def classify_b5(graph, side, walk, bridges):
    assert len(walk) == 5
    induced = graph.subgraph(side)
    if bridges:
        assert len(bridges) == 1 and len(side) == 4 and len(set(walk)) == 4
        assert induced.number_of_edges() == 4
        assert sorted(dict(induced.degree()).values()) == [1, 2, 2, 3]
        return 'triangle_plus_one_bridge'
    assert len(set(walk)) == 5 and len(side) in (5, 6)
    if len(side) == 5:
        assert induced.number_of_edges() == 7
        return 'triangulated_pentagon'
    middle, = side - set(walk)
    assert set(induced[middle]) == set(walk)
    assert induced.number_of_edges() == 10
    return 'pentagonal_wheel'


def audit(name, graph):
    n = len(graph)
    assert sorted(graph) == list(range(n))
    planar, embedding = nx.check_planarity(graph)
    assert planar and graph.number_of_edges() == 3 * n - 6
    assert min(dict(graph.degree()).values()) >= 5
    rotation = {u: list(embedding.neighbors_cw_order(u)) for u in sorted(graph)}
    faces = original_faces(embedding)
    cycle_checks = short_cycle_sides(graph, faces)
    neighbor_masks = [sum(1 << v for v in graph[u]) for u in range(n)]
    all_vertices = (1 << n) - 1
    totals, shapes, samples = Counter(), Counter(), {}
    mincuts = {'all_nonempty': n * n, 'sides_ge_3': n * n,
               'sides_ge_4': n * n, 'sides_ge_7': n * n}
    selected = []
    disconnected_small_cuts = []
    b5_examples = {}
    # Identify complementary cuts once by fixing vertex 0 on X.
    for mask in range(1, all_vertices, 2):
        complement = all_vertices ^ mask
        X = {v for v in range(n) if mask >> v & 1}
        Y = set(graph) - X
        small = min(len(X), len(Y))
        crossing = [(u, v) for u, v in graph.edges() if (u in X) != (v in X)]
        m = len(crossing)
        totals['all_unordered_vertex_cuts'] += 1
        mincuts['all_nonempty'] = min(mincuts['all_nonempty'], m)
        for threshold in (3, 4, 7):
            if small >= threshold:
                key = f'sides_ge_{threshold}'
                mincuts[key] = min(mincuts[key], m)
        assert m >= 5
        if small >= 2:
            assert m >= 8
        if small >= 3:
            assert m >= 9
        if small >= 4:
            assert m >= 10
        if small >= 7:
            assert m >= 12
        cx, cy = connected(mask, neighbor_masks), connected(complement, neighbor_masks)
        if m <= 12 and small >= 3:
            assert cx and cy
            totals['small_cuts_with_large_sides_connected'] += 1
        if not (cx and cy):
            if m <= 12:
                totals['disconnected_cuts_at_most_12'] += 1
                disconnected_small_cuts.append(dict(X=sorted(X), cut_size=m,
                    side_sizes=[len(X), len(Y)], X_connected=cx, Y_connected=cy))
            continue
        totals['connected_bonds'] += 1
        wx, bridges_x, bx = perimeter_walk(X, rotation, faces)
        wy, bridges_y, by = perimeter_walk(Y, rotation, faces)
        assert bx + by == m
        assert len(wx) == bx and len(wy) == by
        for side, other, walk, bridges, b in ((X, Y, wx, bridges_x, bx), (Y, X, wy, bridges_y, by)):
            if len(side) >= 3 and b <= 4:
                assert len(side) <= b and set(walk) == side
            if len(other) >= 2 and b == 5:
                label = classify_b5(graph, side, walk, bridges)
                shapes[label] += 1
                if label not in b5_examples:
                    b5_examples[label] = dict(side=sorted(side), opposite=sorted(other),
                        cut_size=m, exterior_face_walk=walk, bridges=bridges)
        if m == 9 and small >= 3:
            side = X if len(X) <= len(Y) else Y
            assert len(side) == 3 and graph.subgraph(side).number_of_edges() == 3
            assert all(graph.degree(v) == 5 for v in side)
            assert frozenset(side) in {frozenset(face) for face in faces}
            totals['nine_cuts_facial_555'] += 1
        if m == 12 and small >= 7:
            assert bx == by == 6
            assert len(wx) == len(set(wx)) == len(wy) == len(set(wy)) == 6
            endpoint_X = {u if u in X else v for u, v in crossing}
            endpoint_Y = {v if u in X else u for u, v in crossing}
            assert set(wx) == endpoint_X and set(wy) == endpoint_Y
            totals['twelve_cuts_ge_7_perimeters_6_6'] += 1
            totals['twelve_cuts_ge_7_two_simple_C6_endpoint_sets'] += 1
            samples.setdefault('twelve_cut_ge_7', dict(X=sorted(X), Y=sorted(Y), cut_size=m,
                X_walk=wx, Y_walk=wy, perimeters=[bx, by]))
        if m == 12 and sorted((bx, by)) == [5, 7]:
            side5 = X if bx == 5 else Y
            assert len(side5) <= 6
            samples.setdefault('twelve_cut_perimeters_5_7', dict(X=sorted(X), Y=sorted(Y),
                cut_size=m, X_walk=wx, Y_walk=wy, perimeters=[bx, by],
                size_of_perimeter_5_side=len(side5)))
            if len(side5) == 6:
                samples.setdefault('twelve_cut_perimeters_5_7_wheel_side_size_6',
                    dict(X=sorted(X), Y=sorted(Y), cut_size=m, X_walk=wx, Y_walk=wy,
                         perimeters=[bx, by], size_of_perimeter_5_side=6))
        if m <= 12 and small >= 3:
            selected.append(dict(X=sorted(X), cut_size=m, side_sizes=[len(X), len(Y)],
                X_face_walk=wx, Y_face_walk=wy, X_bridges=bridges_x, Y_bridges=bridges_y,
                perimeters=[bx, by]))
    if n < 14:
        mincuts['sides_ge_7'] = None
    return dict(name=name, vertices=list(range(n)),
                original_edges=sorted(tuple(sorted(e)) for e in graph.edges()),
                original_rotation_cw=rotation, original_oriented_faces=faces,
                short_cycle_side_checks=cycle_checks,
                short_cycle_counts=dict(sorted(Counter(map(lambda r: len(r['cycle']), cycle_checks)).items())),
                counts=dict(sorted(totals.items())), minimum_cuts=mincuts,
                b5_shape_counts=dict(sorted(shapes.items())), b5_examples=b5_examples,
                samples=samples, complete_unordered_disconnected_cuts_at_most_12=disconnected_small_cuts,
                complete_unordered_cuts_at_most_12_sides_ge_3=selected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    cases = [audit('icosahedron', nx.icosahedral_graph()),
             audit('capped-antiprism-6', capped_antiprism(6)),
             audit('capped-antiprism-7', capped_antiprism(7))]
    assert 'twelve_cut_ge_7' in cases[1]['samples']
    assert 'twelve_cut_perimeters_5_7_wheel_side_size_6' in cases[2]['samples']
    assert any('triangle_plus_one_bridge' in case['b5_examples'] for case in cases)
    sources = ['scripts/four_color_bond_perimeter_small_cuts.py',
               'docs/four_color_eight_cut_three_step_continuation.md']
    report = dict(schema='four-color-bond-perimeter-small-cuts-v1',
        baseline='e1a90fea41702d7c98747716a5960198aecbecb3', networkx_version=nx.__version__,
        scope='Three fixed original triangulations only; arbitrary-source bounds are paper lemmas.',
        sources_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources},
        cases=cases)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps([dict(name=case['name'], counts=case['counts'], minimum_cuts=case['minimum_cuts'],
        short_cycle_counts=case['short_cycle_counts'], b5_shape_counts=case['b5_shape_counts'])
        for case in cases], sort_keys=True))


if __name__ == '__main__':
    main()
