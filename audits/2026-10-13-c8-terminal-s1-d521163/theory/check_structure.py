#!/usr/bin/env python3
"""Read-only comparison of all 80 H patches against the paper's original links.

Expected edges, C-neighbor paths, directed incident faces, and degrees are built
from PROOF.md formulas, independently of the transfer face construction. The
external B-C collar is deliberately removed: authority.py checks that input.
"""
from itertools import product
from pathlib import Path
import copy
import importlib.util
import json


ROOT = Path(__file__).resolve().parent
TRANSFER = ROOT.parent / 'transfer' / 'check.py'
spec = importlib.util.spec_from_file_location('s1_transfer_structure_subject', TRANSFER)
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)

C = tuple(f'c{i}' for i in range(8))
T = tuple(f't{i}' for i in range(8))
B = tuple(f'b{i}' for i in range(5))


def edge(a, b):
    return tuple(sorted((a, b)))


def oriented(face):
    face = tuple(face)
    return min(face[k:] + face[:k] for k in range(len(face)))


def expected(kind, pair, side, slot):
    a = (pair + 4 * side) % 8
    endpoints = ('x',) if kind == 'PINCH' else ('x', 'y')
    e = endpoints[0 if kind == 'PINCH' else side]
    f = endpoints[0 if kind == 'PINCH' else 1 - side]
    d = [e] + [T[(a + k) % 8] for k in range(4)]
    d.insert(slot + 1, 'w')
    rim = (f,) + tuple(T[(a + 4 + k) % 8] for k in range(4))
    edges = {edge(C[z], C[(z + 1) % 8]) for z in range(8)}
    edges |= {edge(T[z], C[q % 8]) for z in range(8) for q in (z, z + 1)}
    edges |= {edge(v, C[q]) for v in endpoints for q in (pair, (pair + 4) % 8)}
    edges.add(edge('w', C[(a + slot) % 8]))
    edges |= {edge(d[z], d[(z + 1) % 6]) for z in range(6)}
    edges |= {edge(rim[z], rim[(z + 1) % 5]) for z in range(5)}
    edges |= {edge('zF', v) for v in rim}
    if kind == 'BRIDGE':
        edges.add(edge('x', 'y'))
    links = {}
    for z in range(8):
        if z == a:
            path = [T[(a - 1) % 8], f] + ([e] if e != f else []) + [T[a]]
            if slot == 0:
                path.insert(-1, 'w')
        elif z == (a + 4) % 8:
            path = [T[(a + 3) % 8], e] + ([f] if e != f else []) + [T[(a + 4) % 8]]
            if slot == 4:
                path.insert(1, 'w')
        else:
            path = [T[(z - 1) % 8], T[z]]
            if z == (a + slot) % 8:
                path.insert(1, 'w')
        links[C[z]] = path
    return a, endpoints, tuple(d), edges, links


def validate(graph, kind, pair, side, slot):
    a, endpoints, d, edges, links = expected(kind, pair, side, slot)
    actual = {tuple(ed) for ed in graph['edges'] if not set(ed) & set(B)}
    assert actual == edges, 'original H edge set differs'
    assert tuple(graph['D']) == d, 'original D order or singleton slot differs'
    for z, c in enumerate(C):
        degree = sum(c in ed for ed in actual)
        assert degree == 4 + len(endpoints) * (z in (pair, (pair + 4) % 8)) + (z == (a + slot) % 8), 'C degree differs'
        path = links[c]
        expected_pairs = {edge(path[k], path[k + 1]) for k in range(len(path) - 1)}
        original_faces = [face for face in graph['faces'] if c in face
                          and all(v not in B and v not in C for v in face if v != c)]
        actual_pairs = {edge(*[v for v in face if v != c]) for face in original_faces}
        assert actual_pairs == expected_pairs, 'original C link path differs'
        expected_oriented = {oriented((c, path[k + 1], path[k])) for k in range(len(path) - 1)}
        assert {oriented(face) for face in original_faces} == expected_oriented, 'original C-link face orientation differs'
        # Reading the saved full rotation after removing B and C neighbors must
        # recover exactly the same directed inner-neighbor path, up to its
        # cyclic starting position. The saved successor maps previous to next.
        rotation = tuple(v for v in graph['rotations'][c] if v not in B and v not in C)
        assert oriented(rotation) == oriented(tuple(path)), 'saved original rotation differs'


def rejected(graph, configuration):
    try:
        validate(graph, *configuration)
    except AssertionError:
        return True
    raise AssertionError('structural corruption was accepted')


def main():
    collar = (0, 1, 2, 0, 0)
    count = 0
    fixtures = {}
    for configuration in product(('PINCH', 'BRIDGE'), range(4), range(2), range(5)):
        graph, *_ = subject.exterior(*configuration, collar)
        validate(graph, *configuration)
        count += 1
        if configuration in (('PINCH', 0, 0, 0), ('BRIDGE', 0, 0, 4)):
            fixtures[configuration] = graph
    endpoint = ('PINCH', 0, 0, 0)
    wrong_slot = copy.deepcopy(fixtures[endpoint])
    wrong_slot['edges'].remove(edge('w', 'c0'))
    wrong_slot['edges'].append(edge('w', 'c1'))
    rejected(wrong_slot, endpoint)
    bridge = ('BRIDGE', 0, 0, 4)
    no_bridge = copy.deepcopy(fixtures[bridge])
    no_bridge['edges'].remove(edge('x', 'y'))
    rejected(no_bridge, bridge)
    reversed_face = copy.deepcopy(fixtures[bridge])
    faces = list(reversed_face['faces'])
    fid = next(k for k, face in enumerate(faces) if set(face) == {'c0', 'x', 'y'})
    faces[fid] = tuple(reversed(faces[fid]))
    reversed_face['faces'] = tuple(faces)
    rejected(reversed_face, bridge)
    print(json.dumps({
        'status': 'PASS', 'original_H_configurations': count,
        'original_C_links_and_degrees': count * 8,
        'checks': ['original H edges', 'named D order', 'all five singleton slots',
                   'both half orientations', 'C degrees', 'C link paths',
                   'oriented original C-link faces', 'saved cyclic rotations'],
        'negative_controls': {'endpoint_singleton_wrong_attachment': 'rejected',
                              'original_bridge_omitted': 'rejected',
                              'original_bridge_face_reversed': 'rejected'},
        'evidence_files_written': False,
    }, sort_keys=True))


if __name__ == '__main__':
    main()
