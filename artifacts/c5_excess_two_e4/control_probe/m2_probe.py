#!/usr/bin/env python3
"""Two finite, named m=2 positive-control templates; no general exclusion.

Template A is H=K2,2 (four privates), all required spokes varied (10000).
Template B adds one fixed 951 binary triangle at each root (eight privates),
varying both one-spoke roots and both two-spoke mixed singletons (2500).
Finite backtracking supplies exact Sigma and deletion witnesses. Output uses
exclusive-create and --check is a deterministic byte replay.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

B = tuple(range(5))
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in B)
T4 = frozenset((2, 5, 7, 8, 9))
OUT = Path(__file__).resolve().with_suffix('.json')


def normalized(q):
    found = {}
    return tuple(found.setdefault(c, len(found)) for c in q)


REPS = tuple(sorted({normalized(q) for q in product(range(4), repeat=5)
                     if all(q[i] != q[(i + 1) % 5] for i in B)}))


def extension(vertices, edges, q):
    ns = {v: set() for v in vertices}
    for a, b in edges:
        ns[a].add(b)
        ns[b].add(a)
    f = dict(enumerate(q))
    def rec():
        left = set(vertices) - set(f)
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


def sigma(vertices, edges):
    witnesses = {str(i): extension(vertices, edges, q) for i, q in enumerate(REPS)}
    witnesses = {i: {str(v): c for v, c in sorted(f.items())}
                 for i, f in witnesses.items() if f is not None}
    indices = sorted(map(int, witnesses))
    ordered = sorted({tuple(p[c] for c in REPS[i]) for i in indices
                      for p in permutations(range(4))})
    return dict(mask=sum(1 << i for i in indices), accepted_indices=indices,
                complete_ordered_rows=ordered, representative_extensions=witnesses)


def disk(vertices, edges):
    g = nx.Graph()
    g.add_nodes_from(vertices)
    g.add_edges_from(edges)
    apex = max(vertices) + 1
    aug = nx.Graph(g)
    aug.add_edges_from((apex, b) for b in B)
    planar, emb = nx.check_planarity(aug)
    if not planar:
        return None
    rotation = {v: [w for w in emb.neighbors_cw_order(v) if w != apex]
                for v in vertices}
    cut = nx.PlanarEmbedding()
    cut.set_data(rotation)
    cut.check_structure()
    marked, faces = set(), []
    for u in vertices:
        for v in rotation[u]:
            if (u, v) not in marked:
                faces.append(cut.traverse_face(u, v, marked))
    outer = next((f for f in faces if len(f) == 5 and set(f) == set(B)), None)
    assert outer is not None
    return dict(rotation={str(v): ns for v, ns in rotation.items()}, faces=faces,
                designated_outer_C5=outer)


def template(name, vertices, fixed, variables):
    counts = Counter()
    failed, controls = [], []
    fixed = FRAME | frozenset(tuple(sorted(e)) for e in fixed)
    choices = [tuple(combinations(B, n)) for _, n in variables]
    for supports in product(*choices):
        counts['named_spoke_combinations'] += 1
        edges = fixed | frozenset(tuple(sorted((r, b))) for (r, _), support in
                                 zip(variables, supports) for b in support)
        degree = {v: sum(v in e for e in edges) for v in vertices if v not in B}
        assert degree[5] == degree[6] == 5
        assert all(degree[v] == 4 for v in degree if v not in (5, 6))
        assert (5, 6) not in edges and sum(d - 4 for d in degree.values()) == 2
        emb = disk(vertices, edges)
        if emb is None:
            continue
        counts['disk'] += 1
        sig = sigma(vertices, edges)
        if not T4 <= set(sig['accepted_indices']):
            counts['disk_T4_failure'] += 1
            continue
        counts['disk_T4_all'] += 1
        counts['disk_T4_sigma_' + str(sig['mask'])] += 1
        row = dict(variable_spokes={str(v): support for (v, _), support in
                                    zip(variables, supports)},
                   edges=sorted(edges), degree=degree, sigma=sig, embedding=emb)
        deletions = []
        for e in sorted(edges - FRAME):
            after = sigma(vertices, edges - {e})
            new = sorted(set(after['accepted_indices']) - set(sig['accepted_indices']))
            deletions.append(dict(edge=e, sigma_after=after, new_indices=new,
                                  critical=bool(new)))
            if not new:
                row['first_noncritical_edge'] = e
                row['Sigma_after_first_noncritical_edge'] = after
                failed.append(row)
                counts['disk_T4_noncritical'] += 1
                break
        else:
            counts['disk_T4_Sigma_edge_minimal'] += 1
            row['nonframe_edge_deletions'] = deletions
            controls.append(row)
    return dict(name=name, vertices=vertices, roots=[5, 6], m=2,
                fixed_edges=sorted(fixed), variable_spoke_counts=variables,
                counts=dict(sorted(counts.items())), noncritical_disk_T4_rows=failed,
                positive_controls=controls)


def build():
    a = template('A_K22_four_privates', tuple(range(9)),
                 ((5, 7), (5, 8), (6, 7), (6, 8)),
                 ((5, 3), (6, 3), (7, 2), (8, 2)))
    b = template('B_K22_plus_fixed_binary_at_each_root', tuple(range(13)),
                 ((5, 7), (5, 8), (6, 7), (6, 8),
                  (5, 9), (5, 10), (9, 10), (0, 9), (1, 9), (0, 10), (4, 10),
                  (6, 11), (6, 12), (11, 12), (1, 11), (2, 11), (2, 12), (3, 12)),
                 ((5, 1), (6, 1), (7, 2), (8, 2)))
    return dict(schema='e4-nonadjacent-m2-control-probe-v1', base_commit='2ac279b',
                scope='Only two fixed m2 interiors, 10000+2500 named spoke assignments; no arbitrary source exclusion.',
                no_four_color_theorem_oracle=True, networkx_version=nx.__version__,
                B=B, pattern_order=REPS, T4_indices=sorted(T4), templates=[a, b],
                positive_control_count=sum(len(t['positive_controls']) for t in (a, b)))


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
    print(json.dumps(dict(templates={t['name']: t['counts'] for t in result['templates']},
                          controls=result['positive_control_count']), sort_keys=True))
    print('CHECK OK' if args.check else 'CREATED m2_probe.json')


if __name__ == '__main__':
    main()
