#!/usr/bin/env python3
"""Read-only exhaustive replay of three fixed named controls; stdlib only."""
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


def surgery(n, edges, M, N, old_cycles):
    M, N = set(M), set(N); D = M ^ N
    assert onecycle(n, edges, D)
    B = N - M; A = M - N
    F = set(range(len(edges))) - M
    a = adj(n, edges, F - B); paths = []; untouched = []
    for comp in components(a):
        ends = sorted(v for v in comp if len(a[v]) == 1)
        if not ends:
            assert all(len(a[v]) == 2 for v in comp); untouched.append(comp); continue
        assert len(ends) == 2
        path = [ends[0]]; prev = None; cur = ends[0]
        while cur != ends[1]:
            nxt = next(v for v, _ in a[cur] if v != prev)
            path.append(nxt); prev, cur = cur, nxt
        assert set(path) == set(comp); paths.append(path)
    endpoints = sorted(v for path in paths for v in (path[0], path[-1]))
    assert len(endpoints) == len(set(endpoints)) == 2 * len(B)
    def parities(connectors):
        compressed = [(p[0], p[-1], (len(p)-1) % 2) for p in paths]
        compressed += [(edges[k][0], edges[k][1], 1) for k in sorted(connectors)]
        a2 = {v: [] for v in endpoints}
        for k, (u, v, parity) in enumerate(compressed):
            a2[u].append((v, k)); a2[v].append((u, k))
        assert all(len(row) == 2 for row in a2.values())
        unseen = set(endpoints); result = []
        while unseen:
            root = min(unseen); unseen.remove(root); todo = [root]; used = set(); vertices = [root]
            while todo:
                for v, k in a2[todo.pop()]:
                    used.add(k)
                    if v in unseen: unseen.remove(v); vertices.append(v); todo.append(v)
            result.append({'endpoints': sorted(vertices), 'parity': sum(compressed[k][2] for k in used) % 2})
        return result
    before, after = parities(B), parities(A)
    predicted = sum(row['parity'] for row in after) - sum(row['parity'] for row in before)
    actual = sum(len(c)%2 for c in cycles(n, edges, N))-sum(len(c)%2 for c in old_cycles)
    assert predicted == actual
    touches = Counter(next(i for i, c in enumerate(old_cycles) if edges[k][0] in c) for k in B)
    transversal = all(v == 1 for v in touches.values())
    odd_touched = sum(len(old_cycles[i]) % 2 for i in touches)
    if transversal:
        assert len(after) == 1 and actual == (odd_touched % 2) - odd_touched
    return {'cycle_edges': sorted(D), 'removed_from_factor': sorted(B), 'added_to_factor': sorted(A),
            'paths': paths, 'untouched_cycles': untouched, 'old_compressed': before,
            'new_compressed': after, 'oddness_delta': actual, 'transversal': transversal}


def build_control(g):
    n, edges, faces = g['n'], g['edges'], g['faces']; E = set(range(len(edges)))
    assert all(0 <= u < v < n for u, v in edges)
    assert len(edges) == len({tuple(e) for e in edges})
    assert len(components(adj(n, edges))) == 1 and all(len(row) == 3 for row in adj(n, edges))
    emb = embedding(n, edges, faces); ms = matchings(n, edges); sets = list(map(set, ms))
    cs = [cycles(n, edges, M) for M in ms]
    odd = [sum(len(c) % 2 for c in row) for row in cs]
    mass = [sum(len(c) for c in row if len(c) % 2) for row in cs]
    assert all(o % 2 == 0 for o in odd)
    e, f, start = g['e'], g['f'], g['matching_index']; M0 = sets[start]
    assert (e in M0) != (f in M0)
    def allowed(i):
        if g['mode'] == 'fixed_direction':
            return (e in sets[i]) == (e in M0) and (f in sets[i]) == (f in M0)
        assert g['mode'] == 'xor'
        return (e in sets[i]) != (f in sets[i])
    states = [i for i in range(len(ms)) if allowed(i)]; allowed_edges = []; graph = {i: [] for i in states}
    checked_surgeries = 0
    for i, j in combinations(states, 2):
        if onecycle(n, edges, sets[i] ^ sets[j]):
            surgery(n, edges, ms[i], ms[j], cs[i]); checked_surgeries += 1
            allowed_edges.append([i, j]); graph[i].append(j); graph[j].append(i)
    # Both fixed-indicator classes must be connected, with empty classes skipped.
    direction_components = []
    for sign in (False, True):
        subset = {i for i in states if (e in sets[i]) == sign}
        if not subset: continue
        root = min(subset); seen = {root}; todo = [root]
        while todo:
            for j in graph[todo.pop()]:
                if j in subset and j not in seen: seen.add(j); todo.append(j)
        assert seen == subset
        direction_components.append(sorted(subset))
    todo = deque([start]); previous = {start: None}; end = None
    while todo:
        i = todo.popleft()
        if odd[i] == 0: end = i; break
        for j in graph[i]:
            if j not in previous: previous[j] = i; todo.append(j)
    assert end is not None
    path = []
    while end is not None: path.append(end); end = previous[end]
    path.reverse()
    moves = [{'to': j, 'surgery': surgery(n, edges, ms[start], ms[j], cs[start])} for j in graph[start]]
    all_moves = [j for j in range(len(ms)) if onecycle(n, edges, sets[start] ^ sets[j])]
    reversed_descent = [j for j in all_moves if odd[j] < odd[start] and (e in sets[j]) != (f in sets[j]) and not allowed(j)]
    small_cuts = []
    for size in (1, 2, 3):
        for removed in combinations(range(len(edges)), size):
            comps = components(adj(n, edges, E - set(removed)))
            if len(comps) > 1: small_cuts.append({'edges': list(removed), 'shores': comps})
    transversal_moves = []
    if 'transversal' in g['name']:
        for i in range(len(ms)):
            if not odd[i]: continue
            for j in range(len(ms)):
                if onecycle(n, edges, sets[i] ^ sets[j]):
                    result = surgery(n, edges, ms[i], ms[j], cs[i])
                    if result['transversal']: transversal_moves.append([i, j])
        assert transversal_moves == []
    else:
        assert odd[start] == 2
        assert all((odd[j], mass[j]) >= (odd[start], mass[start]) for j in graph[start])
        assert len(path) == 3
    if g['name'] == 'dodecahedron_4sum':
        assert len(ms) == 365 and len(states) == 60 and len(graph[start]) == 12
        assert all(odd[j] == 2 and mass[j] == 36 for j in graph[start])
        assert mass[start] == 10 and reversed_descent
        assert all(len(c['edges']) == 3 and min(map(len, c['shores'])) == 1 for c in small_cuts)
        assert min(emb['primal_degrees']) == 5
        assert len(set(emb['primal_edges'][e] + emb['primal_edges'][f])) == 4
    return {'name': g['name'], 'mode': g['mode'], 'source_status': g['source_status'],
            'embedding': emb, 'marked_primal_edges': [emb['primal_edges'][e], emb['primal_edges'][f]],
            'matchings': [{'edges': M, 'complement_cycles': C, 'oddness': o, 'odd_vertex_mass': w}
                          for M,C,o,w in zip(ms,cs,odd,mass)],
            'admissible_state_indices': states, 'complete_admissible_single_cycle_edges': allowed_edges,
            'direction_classes': direction_components, 'start': start, 'complete_start_moves': moves,
            'shortest_path_to_even': path, 'opposite_direction_direct_descents': reversed_descent,
            'all_cuts_size_at_most_3': small_cuts, 'transversal_moves_from_all_bad_states': transversal_moves,
            'summary': {'matching_count': len(ms), 'admissible_count': len(states),
                        'admissible_even_count': sum(odd[i] == 0 for i in states),
                        'single_cycle_exchange_edges': len(allowed_edges), 'start_neighbours': len(graph[start]),
                        'checked_surgeries': checked_surgeries}}


def build():
    base = seal()
    return {'schema': 'oddness-descent-v1', 'base': base,
            'scope': 'Three fixed named controls; no complete minimum source and no general omega=0 claim.',
            'controls': [build_control(g) for g in json.loads((HERE / 'graphs.json').read_text())]}


def main():
    parser = argparse.ArgumentParser(); flags = parser.add_mutually_exclusive_group(required=True)
    flags.add_argument('--write', type=Path); flags.add_argument('--check', type=Path)
    args = parser.parse_args(); result = build()
    if args.write:
        with args.write.open('x') as stream: json.dump(result, stream, indent=2); stream.write('\n')
    else:
        assert json.loads(args.check.read_text()) == result, 'certificate mismatch'
    print(json.dumps({'status': 'PASS', 'input_drift': 0, 'controls': {r['name']: r['summary'] for r in result['controls']}}, sort_keys=True))

if __name__ == '__main__': main()
