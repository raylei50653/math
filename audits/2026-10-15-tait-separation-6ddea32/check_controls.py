#!/usr/bin/env python3
"""Six named finite controls for ordinary matching separation; stdlib only."""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def input_seal():
    data = json.loads((HERE / 'INPUTS.json').read_text())
    for row in data['inputs']:
        for path in [ROOT / row['path'], HERE / row['frozen']]:
            assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], path
    return data['base']


def adjacency(n, edges, removed=()):
    removed = set(removed)
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if i not in removed:
            adj[u].append((v, i))
            adj[v].append((u, i))
    return adj


def components(adj):
    unseen = set(range(len(adj)))
    result = []
    while unseen:
        todo = [min(unseen)]
        comp = set(todo)
        unseen.remove(todo[0])
        while todo:
            for v, _ in adj[todo.pop()]:
                if v in unseen:
                    unseen.remove(v)
                    comp.add(v)
                    todo.append(v)
        result.append(sorted(comp))
    return result


def bipartition(adj):
    colour = {}
    for root in range(len(adj)):
        if root in colour:
            continue
        colour[root] = 0
        todo = [root]
        while todo:
            u = todo.pop()
            for v, _ in adj[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    todo.append(v)
                elif colour[v] == colour[u]:
                    return None
    return [colour[v] for v in range(len(adj))]


def all_matchings(n, edges):
    adj = adjacency(n, edges)
    result = []

    def visit(free, matching):
        if not free:
            result.append(sorted(matching))
            return
        u = min(free)
        for v, i in adj[u]:
            if v in free:
                visit(free - {u, v}, matching + [i])

    visit(set(range(n)), [])
    return sorted(result)


def independent_count(n, edges):
    """Vertex-subset DP, independent of stored matching list and recursion above."""
    masks = [0] * n
    for u, v in edges:
        masks[u] |= 1 << v
        masks[v] |= 1 << u

    @lru_cache(None)
    def count(mask):
        if mask == 0:
            return 1
        vertices = [v for v in range(n) if mask >> v & 1]
        u = min(vertices, key=lambda v: ((masks[v] & mask).bit_count(), -v))
        rest = mask ^ (1 << u)
        return sum(count(rest ^ (1 << v)) for v in vertices if masks[u] >> v & 1)

    return count((1 << n) - 1)


def matrix_rank(rows):
    if not rows:
        return 0
    a = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        unit = a[rank][col]
        a[rank] = [v / unit for v in a[rank]]
        for i in range(rank + 1, len(a)):
            factor = a[i][col]
            if factor:
                a[i] = [v - factor * w for v, w in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def cycle_components(n, edges, matching):
    adj = adjacency(n, edges, matching)
    assert all(len(row) == 2 for row in adj)
    result = []
    for comp in components(adj):
        start = min(comp)
        cycle = [start]
        previous, current = start, min(v for v, _ in adj[start])
        while current != start:
            cycle.append(current)
            next_vertex = next(v for v, _ in adj[current] if v != previous)
            previous, current = current, next_vertex
        assert set(cycle) == set(comp)
        result.append(cycle)
    return result


def small_cuts(n, edges):
    cuts = []
    for size in (1, 2, 3):
        for removed in combinations(range(len(edges)), size):
            comps = components(adjacency(n, edges, removed))
            if len(comps) > 1:
                cuts.append({'edges': list(removed), 'shores': comps})
    return cuts


def prism(k):
    return sorted({tuple(sorted(e)) for i in range(k)
                   for e in [(i, (i + 1) % k), (i + k, (i + 1) % k + k), (i, i + k)]})


def icosahedron_dual():
    primal = sorted({tuple(sorted(e)) for i in range(5) for e in
                     [(0, 1 + i), (1 + i, 1 + (i + 1) % 5),
                      (11, 6 + i), (6 + i, 6 + (i + 1) % 5),
                      (1 + i, 6 + i), (1 + i, 6 + (i - 1) % 5)]})
    primal_set = set(primal)
    faces = [list(t) for t in combinations(range(12), 3)
             if all(tuple(e) in primal_set for e in combinations(t, 2))]
    edge_faces = [[i for i, face in enumerate(faces) if u in face and v in face]
                  for u, v in primal]
    assert len(faces) == 20 and all(len(row) == 2 for row in edge_faces)
    for v in range(12):
        link = [face for face in faces if v in face]
        neighbours = sorted({u for face in link for u in face if u != v})
        assert len(link) == len(neighbours) == 5
        link_edges = [sorted(u for u in face if u != v) for face in link]
        link_adj = adjacency(12, link_edges)
        assert all(len(link_adj[u]) == 2 for u in neighbours)
        assert any(comp == neighbours for comp in components(link_adj))
    # Coherently orient all triangular faces; shared edges must run oppositely.
    oriented = {0: faces[0]}
    todo = [0]
    while todo:
        i = todo.pop()
        face = oriented[i]
        for k in range(3):
            u, v = face[k], face[(k + 1) % 3]
            edge_id = primal.index(tuple(sorted((u, v))))
            j = next(j for j in edge_faces[edge_id] if j != i)
            if j not in oriented:
                w = next(w for w in faces[j] if w not in (u, v))
                oriented[j] = [v, u, w]
                todo.append(j)
            else:
                assert (oriented[j].index(v) + 1) % 3 == oriented[j].index(u)
    assert len(oriented) == 20 and 12 - len(primal) + len(faces) == 2
    return edge_faces, {'primal_vertices': 12, 'primal_edges': primal,
                        'oriented_primal_faces': [oriented[i] for i in range(20)],
                        'dual_edge_to_primal_edge': list(range(len(primal))),
                        'roles_z_x_y_b': [0, 2, 3, 5],
                        'fixed_frame_z_x_y': [0, 2, 1],
                        'marked_edge_indices': [primal.index((2, 3)), primal.index((0, 5))],
                        'source_status': 'not triggered: icosahedron is not a minimum C5 source'}


def make_control(name, n, edges, marked=None, primal=None):
    edges = [tuple(e) for e in edges]
    adj = adjacency(n, edges)
    assert all(len(row) == 3 for row in adj)
    assert len(set(frozenset(e) for e in edges)) == len(edges)
    assert len(components(adj)) == 1
    matchings = all_matchings(n, edges)
    assert len(matchings) == independent_count(n, edges)
    assert len(matchings) == len({tuple(m) for m in matchings})
    for matching in matchings:
        assert sorted(v for i in matching for v in edges[i]) == list(range(n))
    cycles = [cycle_components(n, edges, m) for m in matchings]
    oddness = [sum(len(c) % 2 for c in cs) for cs in cycles]
    assert all(o % 2 == 0 for o in oddness)
    cuts = small_cuts(n, edges)
    edge_connectivity = min(len(cut['edges']) for cut in cuts)
    nontrivial_three_cuts = [cut for cut in cuts if len(cut['edges']) == 3
                            and all(len(shore) > 1 for shore in cut['shores'])]
    lemma_domain = edge_connectivity == 3 and not nontrivial_three_cuts
    rows = [[int(i in m) for i in range(len(edges))] for m in matchings]
    affine_rank = matrix_rank([[a - b for a, b in zip(row, rows[0])] for row in rows[1:]])
    incidence_rank = matrix_rank([[int(v in edge) for edge in edges] for v in range(n)])
    if lemma_domain:
        assert affine_rank == len(edges) - incidence_rank
    pair_records = []
    for e, f in combinations(range(len(edges)), 2):
        first = [i for i, m in enumerate(matchings) if e in m and f not in m]
        second = [i for i, m in enumerate(matchings) if f in m and e not in m]
        residual = adjacency(n, edges, (e, f))
        parts = bipartition(residual)
        connected = len(components(residual)) == 1
        opposite_internal = (parts is not None
                             and parts[edges[e][0]] == parts[edges[e][1]]
                             and parts[edges[f][0]] == parts[edges[f][1]]
                             and parts[edges[e][0]] != parts[edges[f][0]])
        exception = connected and opposite_internal
        if lemma_domain:
            assert (not first and not second) == exception
            assert bool(first) == bool(second)
        separating = first + second
        omega = min((oddness[i] for i in separating), default=None)
        pair_records.append({'e': e, 'f': f, 'first_only': first, 'second_only': second,
                             'residual_connected': connected,
                             'residual_bipartition': parts,
                             'bipartite_exception': exception, 'omega': omega})
    if marked is None:
        marked = [0, 1]
    marked = sorted(marked)
    marked_record = next(row for row in pair_records if [row['e'], row['f']] == marked)
    result = {'name': name, 'vertices': n, 'edges': edges, 'all_perfect_matchings': matchings,
              'all_complement_cycles': cycles, 'oddness_by_matching': oddness,
              'cuts_of_size_at_most_3': cuts, 'all_edge_pair_records': pair_records,
              'marked_pair': marked_record, 'primal': primal,
              'summary': {'name': name, 'perfect_matchings': len(matchings),
                          'even_complement_matchings': oddness.count(0),
                          'edge_connectivity': edge_connectivity,
                          'nontrivial_three_cuts': len(nontrivial_three_cuts),
                          'lemma_domain': lemma_domain,
                          'affine_rank': affine_rank, 'incidence_rank': incidence_rank,
                          'pairs_checked': len(pair_records),
                          'mutually_dependent_pairs': sum(not r['first_only'] and not r['second_only']
                                                        for r in pair_records),
                          'marked_omega': marked_record['omega'],
                          'source_status': 'not triggered: finite named control only'}}
    return result


def certificate():
    base = input_seal()
    k4 = list(combinations(range(4), 2))
    cube = sorted({tuple(sorted((i, i ^ (1 << j)))) for i in range(8) for j in range(3)})
    triangular = prism(3)
    pentagonal = prism(5)
    petersen = sorted({tuple(sorted(e)) for i in range(5) for e in
                       [(i, (i + 1) % 5), (i, i + 5), (i + 5, (i + 2) % 5 + 5)]})
    dodecahedral, primal = icosahedron_dual()
    controls = [
        make_control('K4_opposite_edges', 4, k4, [k4.index((0, 1)), k4.index((2, 3))]),
        make_control('cube', 8, cube),
        make_control('triangular_prism', 6, triangular,
                     [triangular.index((0, 1)), triangular.index((3, 4))]),
        make_control('pentagonal_prism', 10, pentagonal,
                     [pentagonal.index((0, 1)), pentagonal.index((5, 6))]),
        make_control('Petersen_nonplanar_oddness_control', 10, petersen),
        make_control('icosahedron_dual', 20, dodecahedral,
                     primal['marked_edge_indices'], primal),
    ]
    assert controls[0]['summary']['marked_omega'] is None
    assert controls[3]['summary']['lemma_domain']
    assert controls[3]['summary']['marked_omega'] is None
    assert not controls[2]['summary']['lemma_domain']
    assert controls[4]['summary']['marked_omega'] == 2
    assert all(row['omega'] == 2 for row in controls[4]['all_edge_pair_records'])
    assert controls[5]['summary']['marked_omega'] == 0
    assert controls[5]['summary']['mutually_dependent_pairs'] == 0
    return {'schema': 'ordinary-pm-separation-controls-v1', 'base': base,
            'scope': 'Six named graphs only; ordinary PM theorem has paper proof. No true C5 minimum source enumerated.',
            'controls': controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--write', type=Path)
    actions.add_argument('--check', type=Path)
    args = parser.parse_args()
    observed = json.loads(json.dumps(certificate(), sort_keys=True))
    if args.write:
        with args.write.open('x') as handle:
            json.dump(observed, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write('\n')
    else:
        stored = json.loads(args.check.read_text())
        if stored != observed:
            raise SystemExit('FAIL: certificate is malformed, incomplete, or differs from complete reconstruction')
    print(json.dumps({'status': 'PASS', 'base': observed['base'],
                      'frozen_input_drift': 0,
                      'controls': [row['summary'] for row in observed['controls']]},
                     ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
