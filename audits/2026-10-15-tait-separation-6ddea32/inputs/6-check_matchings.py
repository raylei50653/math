#!/usr/bin/env python3
"""Independent finite controls for C4 Tait-lock review (stdlib only)."""
from collections import defaultdict, deque
from itertools import combinations
import argparse
import json
from pathlib import Path


def graph(n, edge_pairs):
    edges = sorted({tuple(sorted(e)) for e in edge_pairs})
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    faces = [tuple(t) for t in combinations(range(n), 3)
             if all(v in adj[u] for u, v in combinations(t, 2))]
    incidence = defaultdict(list)
    for i, face in enumerate(faces):
        for edge in combinations(face, 2):
            incidence[edge].append(i)
    assert len(edges) == 3 * n - 6 and len(faces) == 2 * n - 4
    assert all(len(incidence[e]) == 2 for e in edges)
    orientations = {0: 1}
    queue = deque([0])
    def direction(face, edge):
        return 1 if (face.index(edge[0]) + 1) % 3 == face.index(edge[1]) else -1
    while queue:
        i = queue.popleft()
        for edge in combinations(faces[i], 2):
            j = next(j for j in incidence[edge] if j != i)
            required = -orientations[i] * direction(faces[i], edge) * direction(faces[j], edge)
            if j in orientations:
                assert orientations[j] == required
            else:
                orientations[j] = required
                queue.append(j)
    assert len(orientations) == len(faces)
    for v in range(n):
        link_edges = [e for e in combinations(sorted(adj[v]), 2) if e in incidence]
        link_adj = {w: set() for w in adj[v]}
        for a, b in link_edges:
            link_adj[a].add(b)
            link_adj[b].add(a)
        assert all(len(neighbours) == 2 for neighbours in link_adj.values())
        reached = {next(iter(link_adj))}
        todo = list(reached)
        while todo:
            for w in link_adj[todo.pop()] - reached:
                reached.add(w)
                todo.append(w)
        assert reached == set(link_adj)
    dual_incident = [[] for _ in faces]
    for k, edge in enumerate(edges):
        for i in incidence[edge]:
            dual_incident[i].append(k)
    return edges, adj, faces, incidence, dual_incident


def complete_colourings(adj, fixed):
    colours = [-1] * len(adj)
    for v, c in fixed.items():
        colours[v] = c
    result = []
    def search():
        uncoloured = [v for v, c in enumerate(colours) if c < 0]
        if not uncoloured:
            result.append(tuple(colours))
            return
        options = {v: set(range(4)) - {colours[w] for w in adj[v] if colours[w] >= 0}
                   for v in uncoloured}
        v = min(uncoloured, key=lambda v: (len(options[v]), -len(adj[v]), v))
        for c in sorted(options[v]):
            colours[v] = c
            search()
        colours[v] = -1
    search()
    return result


def perfect_matchings(incidence, edges, dual_incident):
    endpoints = [tuple(incidence[e]) for e in edges]
    result = []
    def search(free, selected):
        if not free:
            result.append(frozenset(selected))
            return
        v = min(free)
        for k in dual_incident[v]:
            w = next(w for w in endpoints[k] if w != v)
            if w in free:
                search(free - {v, w}, selected + [k])
    search(set(range(len(dual_incident))), [])
    return result


def edge_components(selected, incidence, edges, dual_incident):
    remaining = set(selected)
    result = []
    while remaining:
        seed = min(remaining)
        comp = {seed}
        todo = [seed]
        remaining.remove(seed)
        while todo:
            k = todo.pop()
            for v in incidence[edges[k]]:
                for j in dual_incident[v]:
                    if j in remaining:
                        remaining.remove(j)
                        comp.add(j)
                        todo.append(j)
        result.append(frozenset(comp))
    return result


def connectivity(adj):
    n = len(adj)
    for k in range(n - 1):
        for removed in combinations(range(n), k):
            free = set(range(n)) - set(removed)
            seen = {min(free)}
            todo = list(seen)
            while todo:
                for v in adj[todo.pop()] & free - seen:
                    seen.add(v)
                    todo.append(v)
            if seen != free:
                return k
    return n - 1


def check_xor_contract():
    high_count = low_count = 0
    from itertools import product
    for z, x, y, b in product(range(4), repeat=4):
        if len({z, x, y}) != 3 or z == b:
            continue
        high_count += 1
        missing = next(iter(set(range(4)) - {z, x, y}))
        assert (b == missing) == ((x ^ y) == (z ^ b))
    for z, x, y, p, q in product(range(4), repeat=5):
        if len({z, x, y}) != 3 or len({z, p, q}) != 3:
            continue
        low_count += 1
        assert ({x, y} == {p, q}) == ((x ^ y) == (p ^ q))
    assert (high_count, low_count) == (72, 144)
    return {'high_branch_local_assignments': high_count, 'two_faces_local_assignments': low_count}


def canonical(c):
    rename = {}
    return tuple(rename.setdefault(x, len(rename) + 1) for x in c)


def check(name, n, pairs, roles, target_edges=None):
    edges, adj, faces, incidence, dual_incident = graph(n, pairs)
    z, x, y, b = roles
    assert tuple(sorted((z, x, y))) in faces
    assert tuple(sorted((z, b))) in edges
    colourings = complete_colourings(adj, {z: 0, x: 2, y: 1})
    assert colourings
    raw_tait = {tuple(f[u] ^ f[v] for u, v in edges) for f in colourings}
    tait = {canonical(c) for c in raw_tait}
    assert len(tait) == len(colourings)
    for c in raw_tait:
        assert all({c[k] for k in ks} == {1, 2, 3} for ks in dual_incident)
    matchings = perfect_matchings(incidence, edges, dual_incident)
    even_matchings = []
    all_edges = set(range(len(edges)))
    for matching in matchings:
        complement = edge_components(all_edges - matching, incidence, edges, dual_incident)
        if all(len(cycle) % 2 == 0 for cycle in complement):
            even_matchings.append(matching)
            # Construct a Tait colouring from each even-complement perfect matching.
            edge_colours = [1 if k in matching else 0 for k in range(len(edges))]
            for cycle in complement:
                k = min(cycle)
                start, vertex = incidence[edges[k]]
                first_head = vertex
                edge_colour = 2
                while edge_colours[k] == 0:
                    edge_colours[k] = edge_colour
                    next_edges = [j for j in dual_incident[vertex] if j in cycle and j != k]
                    assert len(next_edges) == 1
                    k = next_edges[0]
                    vertex = next(v for v in incidence[edges[k]] if v != vertex)
                    edge_colour = 5 - edge_colour
                assert edge_colours[k] == edge_colour and vertex == first_head
            assert all({edge_colours[k] for k in ks} == {1, 2, 3} for ks in dual_incident)
            # Integrate XOR labels back on the same primal graph; check all edges.
            vertex_colours = {z: 0}
            todo = [z]
            edge_indices = {e: k for k, e in enumerate(edges)}
            while todo:
                u = todo.pop()
                for v in adj[u]:
                    expected = vertex_colours[u] ^ edge_colours[edge_indices[tuple(sorted((u, v)))]]
                    if v in vertex_colours:
                        assert vertex_colours[v] == expected
                    else:
                        vertex_colours[v] = expected
                        todo.append(v)
            assert len(vertex_colours) == n
            assert canonical(tuple(edge_colours)) in tait
    assert set(even_matchings) == {
        frozenset(k for k, a in enumerate(c) if a == colour)
        for c in raw_tait for colour in (1, 2, 3)
    }
    locked_pairs = []
    for k, j in combinations(range(len(edges)), 2):
        colour_test = any(c[k] != c[j] for c in raw_tait)
        matching_test = any((k in m) != (j in m) for m in even_matchings)
        assert colour_test == matching_test
        if not colour_test:
            locked_pairs.append((edges[k], edges[j]))
            # The all-colouring lock forces both corresponding bichromatic cycles.
            for c in raw_tait:
                for other in {1, 2, 3} - {c[k]}:
                    cycles = edge_components({i for i, a in enumerate(c) if a in {c[k], other}},
                                             incidence, edges, dual_incident)
                    assert next(cycle for cycle in cycles if k in cycle) == next(cycle for cycle in cycles if j in cycle)
    adjacency = {c: set() for c in tait}
    for c in tait:
        for a, d in combinations((1, 2, 3), 2):
            cycles = edge_components({i for i, v in enumerate(c) if v in {a, d}},
                                     incidence, edges, dual_incident)
            for cycle in cycles:
                swapped = tuple(d if i in cycle and v == a else a if i in cycle else v
                                for i, v in enumerate(c))
                neighbour = canonical(swapped)
                assert neighbour in tait
                adjacency[c].add(neighbour)
    unseen = set(tait)
    classes = []
    while unseen:
        seed = min(unseen)
        reached = {seed}
        todo = [seed]
        unseen.remove(seed)
        while todo:
            for neighbour in adjacency[todo.pop()] - reached:
                reached.add(neighbour)
                unseen.remove(neighbour)
                todo.append(neighbour)
        classes.append(reached)
    if target_edges is None:
        target_edges = ((x, y), (z, b))
    target = tuple(edges.index(tuple(sorted(e))) for e in target_edges)
    summary = {
        'name': name, 'primal_vertices': n, 'vertex_connectivity': connectivity(adj), 'degree_sequence': [len(a) for a in adj], 'primal_edges': len(edges), 'dual_vertices': len(faces),
        'normalized_complete_colourings': len(colourings), 'perfect_matchings': len(matchings),
        'even_complement_matchings': len(even_matchings), 'edge_pair_equivalences_checked': len(edges) * (len(edges)-1)//2,
        'globally_locked_edge_pairs': len(locked_pairs), 'normalized_tait_kempe_class_sizes': sorted(len(c) for c in classes),
        'target_edges': [edges[i] for i in target],
        'target_separating_even_matchings': sum((target[0] in m) != (target[1] in m) for m in even_matchings),
        'target_separating_colourings': sum(c[target[0]] != c[target[1]] for c in raw_tait),
        'target_globally_locked': all(c[target[0]] == c[target[1]] for c in raw_tait),
        'target_lock_class_sizes': sorted(len(cls) for cls in classes if all(c[target[0]] == c[target[1]] for c in cls)),
    }
    witness_data = {}
    if name == 'icosahedron':
        assert b not in adj[x] | adj[y]
        assert {len(a) for a in adj} == {5}
        f = (0, 1, 2, 1, 2, 3, 3, 0, 3, 0, 2, 1)
        g = (0, 1, 2, 1, 3, 2, 0, 3, 0, 1, 3, 2)
        assert f in colourings and g in colourings
        fc = tuple(f[u] ^ f[v] for u, v in edges)
        gc = tuple(g[u] ^ g[v] for u, v in edges)
        assert fc[target[0]] == fc[target[1]] == 3
        assert (gc[target[0]], gc[target[1]]) == (3, 2)
        hamilton_cycles = []
        for a, d in combinations((1, 2, 3), 2):
            cycles = edge_components({i for i, v in enumerate(fc) if v in {a, d}},
                                     incidence, edges, dual_incident)
            assert len(cycles) == 1 and len(cycles[0]) == len(faces)
            hamilton_cycles.append({'colours': [a, d], 'edge_indices': sorted(cycles[0])})
        witness_data = {'f': f, 'g': g, 'f_dual_hamilton_cycles': hamilton_cycles}
    elif name == 'pentagonal_bipyramid_shared_endpoint_control':
        assert all(f[5] == f[6] for f in colourings)
    return {
        'summary': summary,
        'primal_edges': edges,
        'primal_faces': faces,
        'fixed_vertex_frame': [[z, 0], [x, 2], [y, 1]],
        'target_edge_indices': target,
        'normalized_complete_colourings': sorted(colourings),
        'perfect_matchings_by_edge_indices': sorted(sorted(m) for m in matchings),
        'even_complement_matchings_by_edge_indices': sorted(sorted(m) for m in even_matchings),
        'canonical_tait_colourings': sorted(tait),
        'canonical_edge_kempe_classes': sorted(sorted(cls) for cls in classes),
        'globally_locked_edge_pairs': locked_pairs,
        'witnesses': witness_data,
    }

def certificate():
    ico_pairs = []
    for i in range(5):
        ico_pairs.extend([(0, 1+i), (1+i, 1+(i+1)%5), (11, 6+i), (6+i, 6+(i+1)%5),
                          (1+i, 6+i), (1+i, 6+(i-1)%5)])
    bipyramid_pairs = [(i, (i+1)%5) for i in range(5)] + [(u, i) for u in (5, 6) for i in range(5)]
    controls = [check('icosahedron', 12, ico_pairs, (0, 2, 3, 5)),
                check('pentagonal_bipyramid_shared_endpoint_control', 7, bipyramid_pairs,
                      (5, 0, 1, 0), ((5, 0), (6, 0)))]
    assert controls[0]['summary']['vertex_connectivity'] == 5
    assert controls[0]['summary']['target_separating_colourings'] > 0
    assert controls[0]['summary']['target_lock_class_sizes']
    assert controls[1]['summary']['vertex_connectivity'] == 4
    assert controls[1]['summary']['target_globally_locked']
    return {'schema': 'c4-tait-lock-finite-controls-v1',
            'scope': 'Finite controls only; Kempe classes refer to dual edge-Kempe moves modulo global colour names. Neither graph is an original minimal source; no Lean theorem.',
            'xor_contract': check_xor_contract(), 'controls': controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', type=Path, help='write the complete finite certificate')
    parser.add_argument('--check', nargs='?', type=Path,
                        const=Path(__file__).with_name('matchings.json'),
                        help='recompute and compare the complete certificate (default: adjacent matchings.json)')
    args = parser.parse_args()
    observed = certificate()
    # JSON round-trip converts tuples to lists before exact comparison.
    observed = json.loads(json.dumps(observed))
    if args.check:
        expected = json.loads(args.check.read_text())
        if observed != expected:
            raise SystemExit('FAIL: stored certificate differs from complete recomputation')
    if args.write:
        args.write.write_text(json.dumps(observed, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'certificate_checked': bool(args.check),
                      'xor_contract': observed['xor_contract'],
                      'controls': [c['summary'] for c in observed['controls']]}, indent=2))


if __name__ == '__main__':
    main()
