#!/usr/bin/env python3
"""Read-only exhaustive replay of four fixed named controls; stdlib only."""
import argparse
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def seal():
    data = json.loads((HERE / 'INPUTS.json').read_text())
    for row in data['inputs']:
        for path in [ROOT / row['path'], HERE / row['frozen']]:
            assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], path
    for row in data['local_inputs']:
        assert hashlib.sha256((HERE / row['path']).read_bytes()).hexdigest() == row['sha256']
    return data['base']


def adj(n, edges, selected=None):
    a = [[] for _ in range(n)]
    for k in range(len(edges)) if selected is None else sorted(selected):
        u, v = edges[k]; a[u].append((v, k)); a[v].append((u, k))
    return a


def components(a):
    unseen = set(range(len(a))); out = []
    while unseen:
        root = min(unseen); unseen.remove(root); todo = [root]; comp = [root]
        while todo:
            for v, _ in a[todo.pop()]:
                if v in unseen:
                    unseen.remove(v); comp.append(v); todo.append(v)
        out.append(sorted(comp))
    return out


def matchings(n, edges):
    a = adj(n, edges); out = []
    def visit(free, sofar):
        if not free:
            out.append(sorted(sofar)); return
        u = min(free)
        for v, k in a[u]:
            if v in free: visit(free - {u, v}, sofar + [k])
    visit(set(range(n)), [])
    # Independently count by minimum remaining degree vertex subset DP.
    masks = [sum(1 << v for v, _ in row) for row in a]
    @lru_cache(None)
    def count(mask):
        if not mask: return 1
        vs = [v for v in range(n) if mask >> v & 1]
        u = min(vs, key=lambda v: ((masks[v] & mask).bit_count(), -v))
        return sum(count(mask ^ (1 << u) ^ (1 << v)) for v in vs if masks[u] >> v & 1)
    out.sort(); assert len(out) == count((1 << n) - 1)
    return out


def cycles(n, edges, M):
    a = adj(n, edges, set(range(len(edges))) - set(M))
    assert all(len(row) == 2 for row in a)
    out = []
    for comp in components(a):
        root = min(comp); previous = root; current = min(v for v, _ in a[root]); row = [root]
        while current != root:
            row.append(current)
            nxt = next(v for v, _ in a[current] if v != previous)
            previous, current = current, nxt
        assert set(row) == set(comp); out.append(row)
    return out


def onecycle(n, edges, D):
    if not D: return False
    a = adj(n, edges, D)
    assert all(len(row) in (0, 2) for row in a)
    return len([c for c in components(a) if len(c) > 1]) == 1


def embedding(n, edges, faces):
    darts = []
    for face in faces:
        assert len(face) >= 3 and len(face) == len(set(face))
        darts += list(zip(face, face[1:] + face[:1]))
    assert Counter(darts) == Counter((u, v) for a, b in edges for u, v in [(a, b), (b, a)])
    assert n - len(edges) + len(faces) == 2
    # Coherent face traversal, connected graph and each vertex link one cycle
    # certify a sphere embedding, independently of the generation library.
    rotation = []
    for v in range(n):
        successor = {}
        for face in faces:
            if v in face:
                i = face.index(v); successor[face[i-1]] = face[(i+1) % len(face)]
        assert len(successor) == 3
        root = min(successor); ring = [root]; cur = successor[root]
        while cur != root:
            assert cur not in ring; ring.append(cur); cur = successor[cur]
        assert len(ring) == 3; rotation.append(ring)
    primal_edges = []
    for u, v in edges:
        fs = [i for i, face in enumerate(faces) if (u, v) in list(zip(face, face[1:]+face[:1])) or (v, u) in list(zip(face, face[1:]+face[:1]))]
        assert len(fs) == 2; primal_edges.append(fs)
    assert len({tuple(sorted(e)) for e in primal_edges}) == len(primal_edges)
    triangles = [[i for i, face in enumerate(faces) if v in face] for v in range(n)]
    assert all(len(t) == 3 for t in triangles)
    return {'rotation': rotation, 'primal_edges': primal_edges,
            'primal_triangular_faces': triangles, 'primal_degrees': list(map(len, faces))}


def difference_cycles(n, edges, M, N):
    D = set(M) ^ set(N)
    a = adj(n, edges, D)
    assert all(len(row) in (0, 2) for row in a)
    return [sorted(k for k in D if edges[k][0] in comp)
            for comp in components(a) if len(comp) > 1]


def primitive(parts, e, f):
    if len(parts) == 1:
        return sum(k in parts[0] for k in (e, f)) in (0, 2)
    return (len(parts) == 2 and
            sorted([sorted(k for k in (e, f) if k in part) for part in parts]) == [[e], [f]])


def surgery(n, edges, M, N):
    M, N = set(M), set(N)
    parts = difference_cycles(n, edges, M, N)
    assert parts
    A, B = M - N, N - M
    a = adj(n, edges, set(range(len(edges))) - M - B)
    paths, untouched = [], []
    for comp in components(a):
        ends = sorted(v for v in comp if len(a[v]) == 1)
        if not ends:
            assert all(len(a[v]) == 2 for v in comp)
            untouched.append(comp)
            continue
        assert len(ends) == 2
        path, previous, current = [ends[0]], None, ends[0]
        while current != ends[1]:
            nxt = next(v for v, _ in a[current] if v != previous)
            path.append(nxt)
            previous, current = current, nxt
        assert set(path) == set(comp)
        paths.append(path)
    endpoints = sorted(v for path in paths for v in (path[0], path[-1]))
    assert len(endpoints) == len(set(endpoints)) == 2 * len(B)
    def compressed(connectors):
        compressed_edges = [(p[0], p[-1], (len(p) - 1) % 2) for p in paths]
        compressed_edges += [(edges[k][0], edges[k][1], 1) for k in sorted(connectors)]
        a2 = {v: [] for v in endpoints}
        for k, (u, v, parity) in enumerate(compressed_edges):
            a2[u].append((v, k)); a2[v].append((u, k))
        assert all(len(row) == 2 for row in a2.values())
        unseen, result = set(endpoints), []
        while unseen:
            root = min(unseen); unseen.remove(root)
            todo, vertices, used = [root], [root], set()
            while todo:
                for v, k in a2[todo.pop()]:
                    used.add(k)
                    if v in unseen:
                        unseen.remove(v); vertices.append(v); todo.append(v)
            result.append({'endpoints': sorted(vertices),
                           'parity': sum(compressed_edges[k][2] for k in used) % 2})
        return result
    old, new = compressed(B), compressed(A)
    old_cycles, new_cycles = cycles(n, edges, M), cycles(n, edges, N)
    actual = sum(len(c) % 2 for c in new_cycles) - sum(len(c) % 2 for c in old_cycles)
    assert actual == sum(r['parity'] for r in new) - sum(r['parity'] for r in old)
    supports = [sorted({i for i, c in enumerate(old_cycles)
                        if any(edges[k][0] in c for k in set(part) - M)}) for part in parts]
    touches = Counter(next(i for i, c in enumerate(old_cycles) if edges[k][0] in c) for k in B)
    transversal = all(count == 1 for count in touches.values())
    if transversal:
        assert len(new) == len(parts)
        rs = [sum(len(old_cycles[i]) % 2 for i in support) for support in supports]
        assert actual == sum(r % 2 - r for r in rs)
    individual_delta = []
    for part in parts:
        co = cycles(n, edges, M ^ set(part))
        individual_delta.append(sum(len(c) % 2 for c in co) - sum(len(c) % 2 for c in old_cycles))
    independent = all(not (set(supports[i]) & set(supports[j]))
                      for i, j in combinations(range(len(parts)), 2))
    if independent:
        assert actual == sum(individual_delta)
    return {'difference_cycles': parts, 'removed_from_factor': sorted(B),
            'added_to_factor': sorted(A), 'paths': paths, 'untouched_cycles': untouched,
            'old_compressed': old, 'new_compressed': new, 'oddness_delta': actual,
            'old_factor_supports': supports, 'individual_deltas': individual_delta,
            'support_disjoint': independent, 'transversal': transversal}


def full_tait_lifts(n, edges, M, cs):
    if any(len(c) % 2 for c in cs):
        return []
    edge_index = {tuple(e): k for k, e in enumerate(edges)}
    result = []
    for choices in range(1 << len(cs)):
        row = [0 if k in M else -1 for k in range(len(edges))]
        for i, c in enumerate(cs):
            for j, (u, v) in enumerate(zip(c, c[1:] + c[:1])):
                row[edge_index[tuple(sorted((u, v)))]] = 1 + ((j + (choices >> i & 1)) % 2)
        assert all({row[k] for _, k in local} == {0, 1, 2} for local in adj(n, edges))
        result.append(row)
    return result


def local_colour_switch(n, edges, row, e, f):
    assert (row[e] == 0) != (row[f] == 0)
    beta = row[f] if row[e] == 0 else row[e]
    selected = {k for k, col in enumerate(row) if col in (0, beta)}
    comps = [comp for comp in components(adj(n, edges, selected))
             if edges[e][0] in comp or edges[f][0] in comp]
    changed = sorted(k for k in selected if any(edges[k][0] in comp for comp in comps))
    out = list(row)
    for k in changed:
        out[k] = beta if row[k] == 0 else 0
    assert len(comps) in (1, 2)
    assert (out[e] == 0) != (row[e] == 0)
    assert (out[f] == 0) != (row[f] == 0)
    return out, changed


def build_control(g):
    n, edges, e, f = g['n'], g['edges'], g['e'], g['f']
    assert e < f
    assert all(0 <= u < v < n for u, v in edges)
    assert len(edges) == len({tuple(edge) for edge in edges})
    assert all(len(row) == 3 for row in adj(n, edges))
    assert len(components(adj(n, edges))) == 1
    emb = embedding(n, edges, g['faces']) if g['faces'] is not None else None
    ms = matchings(n, edges); sets = list(map(frozenset, ms))
    index = {M: i for i, M in enumerate(sets)}
    cs = [cycles(n, edges, M) for M in ms]
    odd = [sum(len(c) % 2 for c in C) for C in cs]
    mass = [sum(len(c) for c in C if len(c) % 2) for C in cs]
    lifts = [full_tait_lifts(n, edges, M, C) for M, C in zip(sets, cs)]
    states = [i for i, M in enumerate(sets) if (e in M) != (f in M)]
    start = g['start']
    if start is None:
        start = next(i for i in states if odd[i])
    assert start in states and odd[start] > 0
    adjacency = {i: [] for i in states}; moves = []; pair_types = Counter()
    canonical_paths = []
    for i, j in combinations(states, 2):
        parts = difference_cycles(n, edges, sets[i], sets[j])
        opposite = (e in sets[i]) != (e in sets[j])
        tagged = [p for p in parts if e in p or f in p]
        if not opposite:
            assert not tagged
            pair_types['same_direction'] += 1
        elif len(tagged) == 1:
            assert e in tagged[0] and f in tagged[0]
            pair_types['opposite_same_cycle'] += 1
        else:
            assert len(tagged) == 2 and all(sum(k in p for k in (e, f)) == 1 for p in tagged)
            pair_types['opposite_distinct_cycles'] += 1
        # Canonical path never assumes an even-complement endpoint.
        batches = [[p] for p in parts if p not in tagged] + ([tagged] if tagged else [])
        current, path = sets[i], [i]
        for batch in batches:
            delta = set().union(*map(set, batch))
            nxt = frozenset(current ^ delta)
            assert nxt in index and index[nxt] in states and primitive(batch, e, f)
            current = nxt; path.append(index[current])
        assert current == sets[j]
        if opposite and len(canonical_paths) < 2 and len(tagged) == len(canonical_paths) + 1:
            canonical_paths.append({'from': i, 'to': j, 'path': path,
                                    'difference_cycles': parts, 'marked_cycle_count': len(tagged)})
        if primitive(parts, e, f):
            row = surgery(n, edges, ms[i], ms[j])
            adjacency[i].append(j); adjacency[j].append(i)
            moves.append([i, j, len(parts), row['oddness_delta']])
    seen, todo = {states[0]}, [states[0]]
    while todo:
        for j in adjacency[todo.pop()]:
            if j not in seen:
                seen.add(j); todo.append(j)
    assert seen == set(states)
    lifted = {tuple(row): (i, j) for i in states for j, row in enumerate(lifts[i])}
    switched = []
    for i in states:
        for lift_index, row in enumerate(lifts[i]):
            out, changed = local_colour_switch(n, edges, row, e, f)
            assert tuple(out) in lifted
            target, target_lift = lifted[tuple(out)]
            assert target in adjacency[i] and odd[target] == 0
            back, changed_back = local_colour_switch(n, edges, out, e, f)
            assert back == row and changed_back == changed
            switched.append([i, lift_index, target, target_lift, changed])
    weights = [sum(len(lifts[i]) for i in states if (e in sets[i]) == sign) for sign in (True, False)]
    assert weights[0] == weights[1]
    start_moves = []
    for j in adjacency[start]:
        row = surgery(n, edges, ms[start], ms[j])
        row['to'] = j
        row['individual_matching_indices'] = [index[frozenset(sets[start] ^ set(part))]
                                               for part in row['difference_cycles']]
        start_moves.append(row)
    named = None
    if g['roles_z_x_y_b'] is not None:
        z, x, y, b = g['roles_z_x_y_b']; assert len({z, x, y, b}) == 4
        pe = {tuple(sorted(edge)) for edge in emb['primal_edges']}
        assert set(emb['primal_edges'][e]) == {x, y} and set(emb['primal_edges'][f]) == {z, b}
        assert sorted([z, x, y]) in [sorted(t) for t in emb['primal_triangular_faces']]
        assert tuple(sorted([b, x])) not in pe and tuple(sorted([b, y])) not in pe
        assert emb['primal_degrees'][z] >= 7 and min(emb['primal_degrees']) >= 5
        cuts = []
        for size in (1, 2, 3):
            for removed in combinations(range(len(edges)), size):
                comp = components(adj(n, edges, set(range(len(edges))) - set(removed)))
                if len(comp) > 1:
                    assert size == 3 and min(map(len, comp)) == 1
                    cuts.append({'edges': list(removed), 'shores': comp})
        named = {'roles_z_x_y_b': [z, x, y, b], 'bx_by_absent': True,
                 'all_cuts_size_at_most_3': cuts, 'complete_minimum_source': 'not triggered'}
    singles = [row for row in start_moves if len(row['difference_cycles']) == 1]
    doubles = [row for row in start_moves if len(row['difference_cycles']) == 2]
    if g['name'] == 'tutte_xor_trap':
        assert len(singles) == 37 and len(doubles) == 38
        assert all((odd[row['to']], mass[row['to']]) >= (odd[start], mass[start]) for row in singles)
        assert [row['to'] for row in doubles if odd[row['to']] == 0] == [397, 434]
    if g['name'] == 'petersen_positive_oddness':
        assert all(value == 2 for value in odd) and weights == [0, 0]
        # Direct girth and no-bridge checks give an elementary nonplanarity
        # certificate: a sphere embedding would have F=7 and 2E>=5F.
        for removed, (u, v) in enumerate(edges):
            reduced = adj(n, edges, set(range(len(edges))) - {removed})
            distance, queue = {u: 0}, deque([u])
            while queue:
                a = queue.popleft()
                for b, _ in reduced[a]:
                    if b not in distance:
                        distance[b] = distance[a] + 1; queue.append(b)
            assert len(distance) == n and distance[v] >= 4
        assert 2 * len(edges) < 5 * (2 - n + len(edges))
    return {'name': g['name'], 'source_status': g['source_status'], 'embedding': emb,
            'named_geometry': named, 'e': e, 'f': f,
            'matchings': [{'edges': M, 'complement_cycles': C, 'oddness': o,
                          'odd_vertex_mass': w, 'full_tait_lifts': L}
                         for M, C, o, w, L in zip(ms, cs, odd, mass, lifts)],
            'admissible_states': states, 'complete_primitive_moves': moves,
            'all_pair_decomposition_counts': dict(sorted(pair_types.items())),
            'canonical_path_examples': canonical_paths, 'start': start,
            'complete_start_moves': start_moves, 'local_colour_involution': switched,
            'summary': {'matching_count': len(ms), 'xor_states': len(states),
                        'xor_even_states': sum(odd[i] == 0 for i in states),
                        'single_moves': sum(row[2] == 1 for row in moves),
                        'double_moves': sum(row[2] == 2 for row in moves),
                        'start_single_neighbours': len(singles), 'start_double_neighbours': len(doubles),
                        'start_single_even': sum(odd[row['to']] == 0 for row in singles),
                        'start_double_even': sum(odd[row['to']] == 0 for row in doubles),
                        'direction_weights': weights, 'all_pair_canonical_paths_checked': sum(pair_types.values())}}


def build():
    return {'schema': 'xor-batch-descent-v1', 'base': seal(),
            'scope': 'Named finite controls, no source realization or general omega=0 claim.',
            'controls': [build_control(g) for g in json.loads((HERE / 'graphs.json').read_text())]}


def main():
    parser = argparse.ArgumentParser()
    flags = parser.add_mutually_exclusive_group(required=True)
    flags.add_argument('--write', type=Path); flags.add_argument('--check', type=Path)
    args = parser.parse_args(); result = build()
    if args.write:
        with args.write.open('x') as stream:
            json.dump(result, stream, indent=2); stream.write('\n')
    else:
        assert json.loads(args.check.read_text()) == result, 'certificate mismatch'
    print(json.dumps({'status': 'PASS', 'input_drift': 0,
                      'controls': {g['name']: g['summary'] for g in result['controls']}}, sort_keys=True))


if __name__ == '__main__':
    main()


