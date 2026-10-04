#!/usr/bin/env python3
"""Bounded positive-control construction, never a general source exclusion.

Exactly two named triangle hubs inherited from the fixed 951 graph, connected
by a sole mixed singleton; only the three size-two spoke sets vary (1000).
No four-colour theorem oracle: finite MRV backtracking and NetworkX planarity.
Output is exclusive-create; --check replays against the saved bytes.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product, permutations
import json
from pathlib import Path

import networkx as nx

B = tuple(range(5))
V = tuple(range(12))
Z, W, X = 5, 10, 11
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in B)
BASE = frozenset(((5, 6), (5, 9), (6, 9), (10, 7), (10, 8), (7, 8),
                  (5, 11), (10, 11), (0, 6), (1, 6), (0, 9), (4, 9),
                  (1, 7), (2, 7), (2, 8), (3, 8))) | FRAME
T4 = frozenset((2, 5, 7, 8, 9))
OUT = Path(__file__).resolve().with_suffix('.json')


def normalized(q):
    found = {}
    return tuple(found.setdefault(c, len(found)) for c in q)


REPS = tuple(sorted({normalized(q) for q in product(range(4), repeat=5)
                     if all(q[i] != q[(i + 1) % 5] for i in B)}))


def extension(edges, q):
    ns = {v: set() for v in V}
    for a, b in edges:
        ns[a].add(b)
        ns[b].add(a)
    f = dict(enumerate(q))
    def rec():
        left = set(V) - set(f)
        if not left:
            return dict(f)
        options = {v: sorted(set(range(4)) - {f[u] for u in ns[v] if u in f})
                   for v in left}
        v = min(left, key=lambda u: (len(options[u]), -len(ns[u]), u))
        for c in options[v]:
            f[v] = c
            got = rec()
            if got is not None:
                return got
        f.pop(v, None)
        return None
    return rec()


def sigma(edges):
    witnesses = {str(i): extension(edges, q) for i, q in enumerate(REPS)}
    witnesses = {i: {str(v): c for v, c in sorted(f.items())}
                 for i, f in witnesses.items() if f is not None}
    indices = sorted(map(int, witnesses))
    ordered = sorted({tuple(p[c] for c in REPS[i]) for i in indices
                      for p in permutations(range(4))})
    return dict(mask=sum(1 << i for i in indices), accepted_indices=indices,
                complete_ordered_rows=ordered, representative_extensions=witnesses)


def disk(edges):
    g = nx.Graph()
    g.add_nodes_from(V)
    g.add_edges_from(edges)
    apex = 12
    aug = nx.Graph(g)
    aug.add_edges_from((apex, b) for b in B)
    planar, emb = nx.check_planarity(aug)
    if not planar:
        return None
    rotation = {v: [w for w in emb.neighbors_cw_order(v) if w != apex] for v in V}
    cut = nx.PlanarEmbedding()
    cut.set_data(rotation)
    cut.check_structure()
    marked, faces = set(), []
    for u in V:
        for v in rotation[u]:
            if (u, v) not in marked:
                faces.append(cut.traverse_face(u, v, marked))
    outer = next((f for f in faces if len(f) == 5 and set(f) == set(B)), None)
    assert outer is not None
    return dict(rotation={str(v): ns for v, ns in rotation.items()}, faces=faces,
                designated_outer_C5=outer)


def build():
    counts = Counter()
    disk_rows, controls = [], []
    choices = tuple(combinations(B, 2))
    for zs, ws, xs in product(choices, repeat=3):
        counts['named_spoke_combinations'] += 1
        edges = BASE | frozenset(tuple(sorted((r, b))) for r, support in
                               ((Z, zs), (W, ws), (X, xs)) for b in support)
        degree = {v: sum(v in e for e in edges) for v in V if v not in B}
        assert degree[Z] == degree[W] == 5
        assert all(degree[v] == 4 for v in degree if v not in (Z, W))
        assert (Z, W) not in edges and sum(d - 4 for d in degree.values()) == 2
        emb = disk(edges)
        if emb is None:
            continue
        counts['disk'] += 1
        sig = sigma(edges)
        row = dict(root_spokes={str(Z): zs, str(W): ws}, mixed_spokes=xs,
                   edges=sorted(edges), degree=degree, sigma=sig, embedding=emb)
        disk_rows.append(row)
        if not T4 <= set(sig['accepted_indices']):
            counts['disk_T4_failure'] += 1
            continue
        counts['disk_T4_all'] += 1
        deletions = []
        for e in sorted(edges - FRAME):
            after = sigma(edges - {e})
            new = sorted(set(after['accepted_indices']) - set(sig['accepted_indices']))
            deletions.append(dict(edge=e, sigma_after=after, new_indices=new,
                                  critical=bool(new)))
        row['nonframe_edge_deletions'] = deletions
        if all(d['critical'] for d in deletions):
            counts['disk_T4_Sigma_edge_minimal'] += 1
            controls.append(row)
        else:
            counts['disk_T4_noncritical'] += 1
    return dict(schema='e4-nonadjacent-split-hub-control-probe-v1',
                scope='Only 1000 named spokes on one fixed seven-private split-hub template; no general conclusion.',
                base_commit='2ac279b', no_four_color_theorem_oracle=True,
                networkx_version=nx.__version__, vertices=V, B=B, roots=[Z, W],
                fixed_edges=sorted(BASE), variable_spokes={'root_z': 2, 'root_w': 2, 'mixed_x': 2},
                pattern_order=REPS, T4_indices=sorted(T4), counts=dict(sorted(counts.items())),
                disk_rows=disk_rows, positive_controls=controls,
                conclusion=('Positive control found in this finite template.' if controls else
                            'No positive control in this fixed template; arbitrary nonadjacent sources are not excluded.'))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    result = build()
    data = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    if args.check:
        assert OUT.read_bytes() == data
    else:
        with OUT.open('xb') as f:
            f.write(data)
    print(json.dumps(dict(counts=result['counts'], controls=len(result['positive_controls'])), sort_keys=True))
    print('CHECK OK' if args.check else 'CREATED split_hub_probe.json')


if __name__ == '__main__':
    main()
