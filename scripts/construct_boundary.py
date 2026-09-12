#!/usr/bin/env python3
"""Seeded disk-triangulation flips and aligned Sigma intersections; no 4CT oracle.

The sampled patches have an induced C5. A BAD union would be a planar graph
with a separating C5, not necessarily a disk patch. Negative results are sampled.
"""
import argparse
import hashlib
import itertools as it
import json
import random
from pathlib import Path

import networkx as nx
from search_boundary import CYCLE, COLORINGS, REPS, canonical, normalize, raw_mask


def accepted(n, edges):
    """Fixed-boundary backtracking; retain all ten boundary equality patterns."""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def extend(colors):
        todo = [v for v in range(5, n) if colors[v] < 0]
        if not todo:
            return True
        v = max(todo, key=lambda v: (len({colors[w] for w in adj[v]
                                         if colors[w] >= 0}), len(adj[v]), -v))
        forbidden = {colors[w] for w in adj[v]}
        for color in range(4):
            if color not in forbidden:
                colors[v] = color
                if extend(colors):
                    colors[v] = -1
                    return True
        colors[v] = -1
        return False

    return tuple(b for b in REPS
                 if all(b[u] != b[v] for u, v in edges if v < 5)
                 and extend(list(b) + [-1] * (n - 5)))


def triangles(n, edges):
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(sorted(edges))
    planar, emb = nx.check_planarity(g)
    assert planar
    seen, inner = set(), []
    outer = 0
    for u in range(n):
        for v in emb.neighbors_cw_order(u):
            if (u, v) in seen:
                continue
            face = emb.traverse_face(u, v, seen)
            if len(face) == 5 and set(face) == set(range(5)):
                outer += 1
            else:
                assert len(face) == 3, face
                inner.append(tuple(sorted(face)))
    assert outer == 1
    return sorted(inner)


def initial(n, rng):
    edges = set(CYCLE) | {(i, 5) for i in range(5)}
    for v in range(6, n):
        face = rng.choice(triangles(v, edges))
        edges.update((u, v) for u in face)
    return edges


def flip(n, edges, rng):
    faces = triangles(n, edges)
    choices = []
    for edge in sorted(edges - set(CYCLE)):
        opposite = [next(v for v in f if v not in edge)
                    for f in faces if set(edge) <= set(f)]
        assert len(opposite) == 2
        new = tuple(sorted(opposite))
        if new not in edges and new[1] >= 5:
            choices.append((edge, new))
    if choices:
        old, new = rng.choice(choices)
        edges = (edges - {old}) | {new}
    return edges


def certificate(n, edges, s):
    from search_boundary import planar_data
    data = planar_data(n, edges)
    assert data is not None
    _, emb, faces, disk = data
    full = [c for c in COLORINGS if normalize(c) in s]
    c = dict(n=n, edges=sorted(edges), boundary=list(range(5)), sigma=full,
             color_orbits=s, sigma_bits_hex=format(raw_mask(full), '060x'),
             dihedral_orbits=sorted({canonical(b) for b in s}),
             rotation=[list(emb.neighbors_cw_order(v)) for v in range(n)],
             faces=faces, cofacial_test=disk)
    c['sha256'] = hashlib.sha256(json.dumps(c, sort_keys=True,
                                         separators=(',', ':')).encode()).hexdigest()
    return c


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed', type=int, default=20260911)
    p.add_argument('--max-patch-n', type=int, default=10)
    p.add_argument('--steps', type=int, default=1000)
    p.add_argument('--max-union-n', type=int, default=15)
    p.add_argument('--output', default='artifacts/construction')
    a = p.parse_args()
    assert a.max_patch_n >= 6 and a.steps > 0
    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(a.seed)
    states, seen, counts, certs = {}, set(), {}, []
    pair_checks = 0
    for n in range(6, a.max_patch_n + 1):
        edges = initial(n, rng)
        counts[n] = dict(samples=0, distinct_graphs=0, new_states=0)
        for step in range(a.steps):
            edges = flip(n, edges, rng)
            counts[n]['samples'] += 1
            key = (n, tuple(sorted(edges)))
            if key in seen:
                continue
            seen.add(key)
            counts[n]['distinct_graphs'] += 1
            s = accepted(n, sorted(edges))
            if s and all(len(set(b)) == 4 for b in s):
                certs.append(certificate(n, edges, s))
                break
            if s in states:
                continue
            counts[n]['new_states'] += 1
            for t, (m, other) in sorted(states.items()):
                if n + m - 5 > a.max_union_n:
                    continue
                pair_checks += 1
                common = tuple(sorted(set(s) & set(t)))
                if not common or any(len(set(b)) <= 3 for b in common):
                    continue
                renamed = {(u if u < 5 else u + n - 5,
                            v if v < 5 else v + n - 5) for u, v in other}
                union = edges | renamed
                assert accepted(n + m - 5, sorted(union)) == common
                certs.append(certificate(n + m - 5, union, common))
                break
            states[s] = (n, tuple(sorted(edges)))
            if certs:
                break
        print(n, counts[n], 'states', len(states), 'BAD', len(certs), flush=True)
        if certs:
            break
    summary = dict(seed=a.seed, networkx=nx.__version__, steps=a.steps,
                   max_patch_n=a.max_patch_n, max_union_n=a.max_union_n,
                   per_n=counts, pair_checks=pair_checks, bad_count=len(certs),
                   scope='seeded induced-C5 disk triangulations; not exhaustive',
                   states=[dict(orbits=s, n=n, edges=e) for s, (n, e)
                           in sorted(states.items())])
    (out / 'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2)+'\n')
    (out / 'bad_certificates.jsonl').write_text(''.join(
        json.dumps(c, sort_keys=True, separators=(',', ':'))+'\n' for c in certs))


if __name__ == '__main__':
    main()
