#!/usr/bin/env python3
"""A same-disk, same-rooted-action counterexample to cut-length sufficiency."""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_cut_interfaces import ROOT, EdgeModel, Move, check_transition
from c5_complementary_cube import encode, singleton_of

SOURCE = ROOT / 'artifacts/c5_cells/corner_disks.json'
OUT = ROOT / 'artifacts/c5_cells/equal_cut_witness.json'
BOUNDARY = ((0, 0), (4, 0), (6, 3), (3, 6), (0, 4))
ROUTES = (
    (((0, 2), (2, 3, 7, 9, 19, 21)), ((2, 3), (9,))),
    (((2, 3), (8, 14)), ((0, 3), (9,)), ((0, 2), (2, 3, 7, 14, 21))),
)


def det(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def drawing(model):
    """Solve an exact linear system, then verify the drawing without relying
    on any theorem that the chosen linear system must give an embedding.
    """
    n = model.n
    matrix = []
    for v in range(5, n):
        row = [Q(len(model.adj[v]) if v == w else -int(w in model.adj[v]))
               for w in range(5, n)]
        row += [sum((Q(BOUNDARY[w][axis]) for w in model.adj[v] if w < 5), Q(0))
                for axis in (0, 1)]
        matrix.append(row)
    for j in range(n - 5):
        pivot = next(i for i in range(j, n - 5) if matrix[i][j])
        matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
        scale = matrix[j][j]
        matrix[j] = [x / scale for x in matrix[j]]
        for i in range(n - 5):
            if i != j:
                scale = matrix[i][j]
                matrix[i] = [a - scale * b for a, b in zip(matrix[i], matrix[j])]
    points = [tuple(map(Q, p)) for p in BOUNDARY] + [tuple(r[-2:]) for r in matrix]
    assert len(set(points)) == n
    # Strictly convex boundary, with every other vertex strictly inside.
    for i in range(5):
        u, v = i, (i + 1) % 5
        assert all(det(points[u], points[v], points[w]) > 0
                   for w in range(n) if w not in (u, v))
    # No non-endpoint vertex on an edge, including incident collinear overlaps.
    for u, v in model.edges:
        a, b = points[u], points[v]
        for w in range(n):
            if w in (u, v):
                continue
            c = points[w]
            on = (det(a, b, c) == 0 and all(min(a[k], b[k]) <= c[k] <= max(a[k], b[k])
                                          for k in (0, 1)))
            assert not on
    disjoint_pairs = 0
    for (u, v), (w, z) in combinations(model.edges, 2):
        if {u, v} & {w, z}:
            continue
        disjoint_pairs += 1
        a, b, c, d = [points[i] for i in (u, v, w, z)]
        assert not (det(a, b, c) * det(a, b, d) < 0
                    and det(c, d, a) * det(c, d, b) < 0)
    areas = []
    for face in model.dual.faces:
        a, b, c = [points[i] for i in face]
        area = det(a, b, c)
        assert area > 0
        areas.append(area)
        assert all(not (det(a, b, points[w]) > 0 and det(b, c, points[w]) > 0
                        and det(c, a, points[w]) > 0)
                   for w in range(n) if w not in face)
    polygon_area = sum(points[i][0] * points[(i + 1) % 5][1]
                       - points[i][1] * points[(i + 1) % 5][0] for i in range(5))
    assert sum(areas) == polygon_area
    return dict(coordinates=[[str(x), str(y)] for x, y in points],
                doubled_face_areas=list(map(str, areas)), doubled_polygon_area=str(polygon_area),
                disjoint_edge_pairs_checked=disjoint_pairs,
                claim='Exact noncrossing straight-line triangulation of the convex boundary pentagon.')


def report():
    source = json.loads(SOURCE.read_text())
    disk, = [s for s in source['survivors'] if s['disk'] == 811]
    graph = dict(name='survivor-811', n=disk['n'], edges=disk['edges'],
                 faces=disk['oriented_faces'])
    model = EdgeModel(graph)
    geometry = drawing(model)
    seed = tuple(disk['states'][0]['coloring'])
    rows = []
    for route in ROUTES:
        c, history = seed, []
        for pair, component in route:
            action = Move(pair, component)
            d = model.apply(c, action)
            history.append(dict(source=c, pair=pair, component=component, target=d,
                                source_compatible=model.compatible(c), target_compatible=model.compatible(d)))
            c = d
        action, = [a for a in model.actions(c) if a.pair == (0, 1) and 0 in a.component]
        d = model.apply(c, action)
        event = model.edge_replay(c, action)
        cut = set(event['cut_edges'])
        escapes = [dict(pair=a.pair, component=a.component, target=model.apply(d, a),
                        singleton=singleton_of(model.apply(d, a))) for a in model.actions(d)
                   if singleton_of(model.apply(d, a)) in (1, 3, 4)]
        rows.append(dict(source=c, history=history, source_state=model.dual.state(c, True),
            source_compatible=model.compatible(c), action=dict(pair=action.pair, component=action.component),
            cut_length=len(cut), event=event, target=d, target_state=model.dual.state(d, True),
            target_compatible=model.compatible(d), immediate_escapes=escapes,
            old_component_sizes_and_cuts=[sorted((t, len(es), len(cut & set(es))) for t, es in system)
                                          for system in model.dual.systems(c)],
            interfaces=check_transition(model, c, action)))
    a, b = rows
    assert a['source'] != b['source'] and a['source'][:5] == b['source'][:5]
    assert a['source_state'] == b['source_state']
    assert a['source_compatible'] and b['source_compatible']
    assert a['cut_length'] == b['cut_length'] == 21
    assert a['target'][:5] == b['target'][:5]
    assert a['target_state'][1] != b['target_state'][1]
    assert a['target_state'][2:4] == b['target_state'][2:4]
    assert not a['target_compatible'] and b['target_compatible']
    assert a['immediate_escapes'] and not b['immediate_escapes']
    # A concrete connected-class route goes backwards along history A and
    # forwards along history B; every intermediate state here is also safe.
    current = a['source']
    class_route = list(reversed(a['history'])) + b['history']
    for event in class_route:
        current = model.apply(current, Move(event['pair'], event['component']))
        assert model.compatible(current)
    assert current == b['source']
    # A component from one coloring must not silently be reused in the other.
    stale = Move(a['action']['pair'], a['action']['component'])
    assert stale not in model.actions(b['source'])
    try:
        model.apply(b['source'], stale)
    except ValueError:
        pass
    else:
        raise AssertionError('Stale component accepted')
    predecessors = json.loads((ROOT / 'artifacts/c5_cells/edge_choices.json').read_text())
    files = {SOURCE, Path(__file__).resolve(), ROOT / 'artifacts/c5_cells/edge_choices.json',
             ROOT / 'scripts/c5_cut_interfaces.py',
             ROOT / 'scripts/c5_edge_choices.py'}
    files.update(ROOT / p for p in predecessors['hashes'] if p.startswith('scripts/'))
    return dict(trust='Exact rational embedding and complete coloring certificate; paper proof, not Lean.',
        graph=graph, geometry=geometry, seed=seed, witnesses=rows,
        same_class_route=[dict(pair=e['pair'], component=e['component']) for e in class_route],
        summary=dict(vertices=model.n, edges=len(model.edges), faces=len(model.faces),
            cut_lengths=[r['cut_length'] for r in rows],
            source_cycles=a['source_state'][-1], target_cycles=[r['target_state'][-1] for r in rows],
            target_compatible=[r['target_compatible'] for r in rows],
            class_route_length=len(class_route)),
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(files)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    content = encode(result) + '\n'
    if args.check:
        assert OUT.read_text() == content, 'Certificate differs; inspect before regenerating.'
    else:
        OUT.write_text(content)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
