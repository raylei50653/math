#!/usr/bin/env python3
"""Replay the two-vertex deletion identities on saved symbolic skeletons."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_leaf_exception/observations.json'
OUT = ROOT / 'artifacts/c5_sector_leaf_reduction/observations.json'
W, B, A, P, Q, R, U = range(5, 12)
PAIRS = list(combinations(range(4), 2))


def partition(g, coloring, pair, retained=None):
    h = g.subgraph(v for v in g if coloring[v] in pair)
    keep = set(g) if retained is None else set(retained)
    return sorted(sorted(set(comp) & keep) for comp in nx.connected_components(h) if set(comp) & keep)


def audit(old):
    g = nx.Graph(old['forced_edges'])
    c = dict(enumerate(old['coloring']))
    selected = set(old['selected'])
    raw = {v: 1-c[v] if v in selected else c[v] for v in g}
    assert set(g[0]) == {B, W} and set(g[W]) == {0, P, Q, R}
    assert [c[v] for v in (B, W, P, Q, R)] == [1, 1, 2, 3, 3]
    j = g.subgraph(set(g) - {0, W}).copy()
    records = []
    for name, coloring, special in (('old', c, (1, 3)), ('new', raw, (0, 3))):
        for pair in PAIRS:
            projected = partition(g, coloring, pair, j)
            before_join = partition(j, coloring, pair)
            h = j.copy()
            if pair == special:
                # Connectivity only: the virtual edge joins equal-color q,r;
                # it is NOT an edge or a proper-coloring claim about J.
                h.add_edge(Q, R)
            predicted = partition(h, coloring, pair)
            assert projected == predicted
            records.append(dict(coloring=name, pair=list(pair), reduced_partition=before_join,
                                restored_partition=projected, join_ports=[Q, R] if pair == special else None))
    for pair, coloring in (((0, 2), c), ((0, 3), c), ((1, 2), raw), ((1, 3), raw)):
        assert [0] in partition(g, coloring, pair)
    assert all(j.degree[v] == g.degree[v] - (v in {B, P, Q, R}) for v in j)
    old13 = j.subgraph(v for v in j if c[v] in (1, 3))
    assert nx.has_path(old13, 1, Q) and nx.has_path(old13, R, 4)
    assert not nx.has_path(old13, Q, R)
    return dict(extra_color=old['extra_color'],
                scope='Saved necessary edge skeleton, not a full sector realization.',
                removed=[0, W], ports=dict(b=B, p=P, q=Q, r=R),
                reduced_edges=sorted(sorted(e) for e in j.edges()),
                degree_losses={str(v): g.degree[v]-j.degree[v] for v in sorted(j)},
                pair_identities=records)


def build():
    saved = json.loads(UPSTREAM.read_text())
    for name, expected in saved['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    cases = [audit(old) for old in saved['cut_equality']]
    inputs = {UPSTREAM, Path(__file__).resolve()}
    inputs.update(ROOT / name for name in saved['input_sha256'])
    return dict(schema=1,
                scope='All-vertex two-color partition identities for deleting frame0 and the saturated leaf; no complete Sigma or disk equivalence.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                summary=dict(saved_symbolic_skeletons=len(cases), full_vertex_partition_identities=12*len(cases),
                             automatic_isolation_checks=4*len(cases), marked_degree_losses=4*len(cases)),
                cases=cases, closure_effect=dict(profile_deletions=0, inherited_profiles=603, fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
