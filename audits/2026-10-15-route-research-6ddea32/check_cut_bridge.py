#!/usr/bin/env python3
"""Full finite cut/matching correspondence controls; no source exclusion."""
import argparse
from collections import defaultdict
from itertools import combinations, product
import json
from pathlib import Path


def controls():
    ico = set()
    for i in range(5):
        ico.update(tuple(sorted(e)) for e in
                   [(0, 1+i), (1+i, 1+(i+1)%5), (11, 6+i),
                    (6+i, 6+(i+1)%5), (1+i, 6+i), (1+i, 6+(i-1)%5)])
    bip = {tuple(sorted((i, (i+1)%5))) for i in range(5)}
    bip.update((i, a) for a in (5, 6) for i in range(5))
    return [('icosahedron', 12, sorted(ico)), ('pentagonal_bipyramid', 7, sorted(bip))]


def bipartite(n, edges, a):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if a[u] == a[v]:
            adj[u].append(v)
            adj[v].append(u)
    b = [-1]*n
    for start in range(n):
        if b[start] >= 0:
            continue
        b[start] = 0
        todo = [start]
        while todo:
            u = todo.pop()
            for v in adj[u]:
                if b[v] < 0:
                    b[v] = b[u] ^ 1
                    todo.append(v)
                elif b[v] == b[u]:
                    return None
    assert all(a[u] != a[v] or b[u] != b[v] for u, v in edges)
    return b


def check_graph(name, n, edges):
    edge_set = set(edges)
    faces = [t for t in combinations(range(n), 3)
             if all(e in edge_set for e in combinations(t, 2))]
    inc = defaultdict(list)
    for i, t in enumerate(faces):
        for e in combinations(t, 2):
            inc[e].append(i)
    assert len(edges) == 3*n-6 and len(faces) == 2*n-4
    assert all(len(inc[e]) == 2 for e in edges)
    dual_edges = [tuple(inc[e]) for e in edges]
    dual_adj = [[] for _ in faces]
    for k, (u, v) in enumerate(dual_edges):
        dual_adj[u].append((v, k))
        dual_adj[v].append((u, k))
    assert all(len(a) == 3 for a in dual_adj)
    matchings = set()

    def search(free, chosen):
        if not free:
            matchings.add(tuple(sorted(chosen)))
            return
        u = min(free)
        for v, k in dual_adj[u]:
            if v in free:
                search(free-{u, v}, chosen+[k])
    search(set(range(len(faces))), [])
    rows = []
    for tail in product(range(2), repeat=n-1):
        a = (0,)+tail
        if any(len({a[v] for v in t}) == 1 for t in faces):
            continue
        matching = tuple(k for k, (u, v) in enumerate(edges) if a[u] == a[v])
        assert matching in matchings
        seen = set()
        lengths = []
        for start in range(len(faces)):
            if start in seen:
                continue
            todo = [start]
            seen.add(start)
            component = []
            while todo:
                u = todo.pop()
                component.append(u)
                remaining = [(v, k) for v, k in dual_adj[u] if k not in matching]
                assert len(remaining) == 2
                for v, _ in remaining:
                    if v not in seen:
                        seen.add(v)
                        todo.append(v)
            lengths.append(len(component))
        b = bipartite(n, edges, a)
        assert (b is not None) == all(length % 2 == 0 for length in lengths)
        rows.append({'a': a, 'matching': matching, 'complement_cycle_lengths': sorted(lengths),
                     'second_cut_witness': b})
    assert {r['matching'] for r in rows} == matchings
    assert len(rows) == len(matchings)
    even = sum(r['second_cut_witness'] is not None for r in rows)
    assert 0 < even < len(rows)  # Meaningful odd-complement negative controls exist.
    return {'name': name, 'vertices': n, 'edges': edges, 'faces': faces,
            'ordinary_matchings': len(rows), 'even_complement_matchings': even, 'rows': rows}


def certificate():
    return {'schema': 'cut-matching-bridge-v1',
            'scope': 'Finite controls only; neither graph is a full minimal source.',
            'controls': [check_graph(*args) for args in controls()]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    observed = json.loads(json.dumps(certificate()))
    if args.write:
        with args.write.open('x') as stream:
            json.dump(observed, stream, indent=2)
            stream.write('\n')
    else:
        if json.loads(args.check.read_text()) != observed:
            raise SystemExit('FAIL: stored certificate differs from exhaustive recomputation')
    print(json.dumps({'status': 'PASS', 'controls': [
        {k: item[k] for k in ('name', 'ordinary_matchings', 'even_complement_matchings')}
        for item in observed['controls']]}))


if __name__ == '__main__':
    main()
