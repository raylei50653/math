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


def original_dual(g):
    vertices, edges = g['J_vertices'], g['J_edges']
    faces = [list(face) for face in g['J_faces']]
    dual = [[i for i, face in enumerate(faces) if set(edge) <= set(face)] for edge in edges]
    assert all(len(row) == 2 for row in dual)
    oriented, queue = {0: faces[0]}, [0]
    def darts(face): return list(zip(face, face[1:] + face[:1]))
    while queue:
        i = queue.pop()
        for k, (u, v) in enumerate(edges):
            if i not in dual[k]: continue
            j = next(t for t in dual[k] if t != i)
            want = (v, u) if (u, v) in darts(oriented[i]) else (u, v)
            if j not in oriented:
                oriented[j] = faces[j] if want in darts(faces[j]) else list(reversed(faces[j]))
                queue.append(j)
            assert want in darts(oriented[j])
    qfaces = []
    for v in vertices:
        around = sorted(i for i, face in enumerate(faces) if v in face)
        ring, current = [], around[0]
        while current not in ring:
            ring.append(current)
            face = oriented[current]; w = face[(face.index(v) + 1) % 3]
            k = edges.index(sorted((v, w)))
            current = next(i for i in dual[k] if i != current)
        assert current == ring[0] and sorted(ring) == around
        qfaces.append(ring)
    emb = embedding(len(faces), dual, qfaces)
    assert emb['primal_edges'] == edges
    return len(faces), dual, qfaces, emb


def subsets_components(allowed, masks):
    unseen, result = allowed, []
    while unseen:
        seed = unseen & -unseen; unseen ^= seed
        comp, frontier = seed, seed
        while frontier:
            bit = frontier & -frontier; frontier ^= bit
            v = bit.bit_length() - 1; new = masks[v] & unseen
            unseen ^= new; comp |= new; frontier |= new
        result.append(comp)
    return result


def bit_vertices(bits):
    return [v for v in range(bits.bit_length()) if bits >> v & 1]


def residual_matchings(n, edges, free, banned):
    a = adj(n, edges, set(range(len(edges))) - set(banned)); out = []
    def rec(free, current):
        if not free:
            out.append(sorted(current)); return
        u = min(free)
        for v, k in a[u]:
            if v in free: rec(free - {u, v}, current + [k])
    rec(set(free), [])
    return sorted(out)


def tutte_analysis(n, edges, forced, banned, full_pm, no_nontrivial_3cut):
    X = set().union(*(set(edges[k]) for k in forced))
    assert len(X) == 4 and not (X & set(edges[banned]))
    live = sorted(set(range(n)) - X)
    x_edges = [k for k, edge in enumerate(edges) if set(edge) <= X]
    residual = residual_matchings(n, edges, live, {banned})
    family = [i for i, M in enumerate(full_pm) if set(forced) <= set(M) and banned not in M]
    assert residual == sorted([sorted(set(full_pm[i]) - set(forced)) for i in family])
    masks = [0] * n
    for k, (u, v) in enumerate(edges):
        if k != banned and u not in X and v not in X:
            masks[u] |= 1 << v; masks[v] |= 1 << u
    all_live = sum(1 << v for v in live)
    barriers, histogram, maximum = [], Counter(), -n
    for bits in range(1 << len(live)):
        S = sum(1 << v for i, v in enumerate(live) if bits >> i & 1)
        comps = subsets_components(all_live ^ S, masks)
        odd = [c for c in comps if c.bit_count() % 2]
        deficiency = len(odd) - S.bit_count()
        maximum = max(maximum, deficiency); histogram[deficiency] += 1
        if deficiency > 0:
            if no_nontrivial_3cut: assert deficiency == 2
            barriers.append({'S': bit_vertices(S), 'components': list(map(bit_vertices, comps)),
                             'odd_components': list(map(bit_vertices, odd)), 'deficiency': deficiency})
    assert bool(residual) == (not barriers)
    maximal = []
    if barriers:
        max_size = max(len(row['S']) for row in barriers)
        for row in barriers:
            if len(row['S']) != max_size: continue
            assert row['components'] == row['odd_components']
            S = set(row['S']); comps = list(map(set, row['components']))
            comp_rows = []
            for C in comps:
                cut = [k for k, (u, v) in enumerate(edges) if (u in C) != (v in C)]
                witnesses = []
                for v in sorted(C):
                    found = residual_matchings(n, edges, C - {v}, {banned})
                    assert found
                    witnesses.append({'deleted': v, 'matching': found[0]})
                mu = (len(cut) - 3) // 2
                if no_nontrivial_3cut:
                    assert len(cut) % 2 == 1 and mu >= 0
                    assert (mu == 0) == (len(C) == 1)
                comp_rows.append({'vertices': sorted(C), 'cut_edges': cut, 'mu': mu,
                                  'factor_critical_deletions': witnesses})
            u, v = edges[banned]
            positions = [next((i for i, C in enumerate(comps) if a in C), None) for a in (u, v)]
            tau = int(None not in positions and positions[0] != positions[1])
            internal_S = [k for k, edge in enumerate(edges) if set(edge) <= S]
            S_X = [k for k, (u, v) in enumerate(edges) if (u in S and v in X) or (v in S and u in X)]
            lhs = sum(c['mu'] for c in comp_rows) + len(internal_S) + len(S_X)
            rhs = 3 - len(x_edges) + tau
            if no_nontrivial_3cut:
                assert lhs == rhs <= 2
                assert all(len(c['cut_edges']) in (3, 5, 7) for c in comp_rows)
            maximal.append(row | {'component_data': comp_rows, 'tau': tau,
                                  'internal_S_edges': internal_S, 'S_X_edges': S_X,
                                  'budget_lhs': lhs, 'budget_rhs': rhs,
                                  'budget_domain_triggered': no_nontrivial_3cut})
    return {'forced': forced, 'forbidden': banned, 'X': sorted(X), 'Q_X_edges': x_edges,
            'family_indices': family, 'all_residual_matchings': residual,
            'subsets_checked': 1 << len(live), 'deficiency_histogram': {str(k): histogram[k] for k in sorted(histogram)},
            'maximum_deficiency': maximum, 'all_barriers': barriers,
            'maximum_cardinality_barriers': maximal}


def direct_colourings(vertices, edges):
    a = {v: set() for v in vertices}
    for u, v in edges: a[u].add(v); a[v].add(u)
    order = sorted(vertices, key=lambda v: (-len(a[v]), v)); out, current = [], {}
    def rec(i):
        if i == len(order):
            out.append([current[v] for v in vertices]); return
        v = order[i]
        for col in range(4):
            if all(current.get(w) != col for w in a[v]):
                current[v] = col; rec(i + 1); del current[v]
    rec(0)
    return sorted(out)


def build_control(g):
    if 'J_vertices' in g:
        n, edges, faces, emb = original_dual(g)
        marks = [g['J_edges'].index(edge) for edge in g['marked_original_edges']]
    else:
        n, edges, marks = g['Q_n'], g['Q_edges'], g['marks']
        faces = emb = None
    assert len(set().union(*(set(edges[k]) for k in marks))) == 6
    assert all(len(row) == 3 for row in adj(n, edges))
    if g['name'] == 'petersen_double_obstruction':
        for removed, (u, v) in enumerate(edges):
            a = adj(n, edges, set(range(len(edges))) - {removed})
            dist, todo = {u: 0}, deque([u])
            while todo:
                at = todo.popleft()
                for to, _ in a[at]:
                    if to not in dist: dist[to] = dist[at] + 1; todo.append(to)
            assert len(dist) == n and dist[v] >= 4
        assert 2 * len(edges) < 5 * (2 - n + len(edges))
    small_cuts = []
    for size in (1, 2, 3):
        for deleted in combinations(range(len(edges)), size):
            comps = components(adj(n, edges, set(range(len(edges))) - set(deleted)))
            if len(comps) > 1: small_cuts.append({'edges': list(deleted), 'shores': comps})
    no_nontrivial = all(len(row['edges']) == 3 and min(map(len, row['shores'])) == 1 for row in small_cuts)
    ms = matchings(n, edges); cs = [cycles(n, edges, M) for M in ms]
    lifts = [full_tait_lifts(n, edges, set(M), C) for M, C in zip(ms, cs)]
    e, f, h = marks
    families = {'110': tutte_analysis(n, edges, [e, f], h, ms, no_nontrivial),
                '101': tutte_analysis(n, edges, [e, h], f, ms, no_nontrivial)}
    weights = {pat: sum(len(lifts[i]) for i in family['family_indices']) for pat, family in families.items()}
    primal = None
    if emb:
        vertices, original = g['J_vertices'], g['J_edges']
        rows = direct_colourings(vertices, original)
        root_rows = [row for row in rows if row[0] == 0]
        recovered = []
        for group in lifts:
            for lift in group:
                values, queue = {0: 0}, [0]
                while queue:
                    v = queue.pop()
                    for k, (a, b) in enumerate(original):
                        if v not in (a, b): continue
                        w = b if v == a else a; colour = values[v] ^ (lift[k] + 1)
                        if w in values: assert values[w] == colour
                        else: values[w] = colour; queue.append(w)
                recovered.append([values[v] for v in vertices])
        assert sorted(recovered) == root_rows
        event_counts = {'110': 0, '101': 0}; source_good = 0
        for row in rows:
            de, df, dg = [row[a] ^ row[b] for a, b in g['marked_original_edges']]
            event_counts['110'] += de == df != dg
            event_counts['101'] += de == dg != df
            source_good += (de == df) == (de == dg)
        assert all(event_counts[pat] == 12 * weights[pat] for pat in families)
        assert source_good + sum(event_counts.values()) == len(rows)
        primal = {'all_complete_J_colourings': rows, 'all_root_zero_lifts': root_rows,
                  'event_counts': event_counts, 'combined_bad_count': sum(event_counts.values()),
                  'source_predicate_good_count': source_good}
    return {'name': g['name'], 'source_status': 'not triggered', 'Q_n': n, 'Q_edges': edges,
            'Q_faces': faces, 'embedding': emb, 'marks_e_f_g': marks,
            'all_cuts_size_at_most_3': small_cuts, 'no_nontrivial_3cut': no_nontrivial,
            'matchings': [{'edges': M, 'complement_cycles': C, 'all_tait_lifts': L}
                         for M, C, L in zip(ms, cs, lifts)], 'families': families,
            'weights': weights, 'primal': primal,
            'summary': {'Q_n': n, 'all_PM': len(ms), 'P110': len(families['110']['family_indices']),
                        'P101': len(families['101']['family_indices']), 'W110': weights['110'],
                        'W101': weights['101'], 'tutte_subsets': sum(r['subsets_checked'] for r in families.values()),
                        'no_nontrivial_3cut': no_nontrivial}}


def build():
    return {'base': seal(), 'schema': 'three-edge-matchings-v1',
            'controls': [build_control(g) for g in json.loads((HERE / 'graphs.json').read_text())]}


def main():
    parser = argparse.ArgumentParser(); options = parser.add_mutually_exclusive_group(required=True)
    options.add_argument('--write', type=Path); options.add_argument('--check', type=Path)
    args = parser.parse_args(); result = build()
    if args.write:
        with args.write.open('x') as stream: json.dump(result, stream, indent=2); stream.write('\n')
    else:
        assert json.loads(args.check.read_text()) == result, 'certificate mismatch'
    print(json.dumps({'status': 'PASS', 'input_drift': 0,
                      'controls': {g['name']: g['summary'] for g in result['controls']}}, sort_keys=True))


if __name__ == '__main__': main()


