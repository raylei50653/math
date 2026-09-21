#!/usr/bin/env python3
"""Five-inner symbolic path proof; no candidate-graph or coloring search."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_five_inner/observations.json'
UPSTREAM = ROOT / 'artifacts/c5_sector_frame_cut/observations.json'
FRAME = set(range(5))
BASE = [(1, 2), (2, 3), (3, 4), (0, 6), (6, 5), (5, 1)]


def edge_list(g):
    return sorted(sorted(e) for e in g.edges())


def gamma_paths(g, u, v):
    h = g.subgraph((set(g) - FRAME) | {u, v})
    return sorted(list(p) for p in nx.all_simple_paths(h, u, v))


def violation(g, c, selected):
    for v in range(5, 10):
        if g.degree[v] > 4:
            return dict(reason='inner_degree_above_four', vertex=v, neighbors=sorted(g[v]))
    h = g.subgraph(selected - {1})
    if nx.has_path(h, 0, 2):
        return dict(reason='frame_cut_violated', path=nx.shortest_path(h, 0, 2))
    raw = {v: 1-c[v] if v in selected else c[v] for v in g}
    for label, colors, coloring, u, v in (
        ('source02', (0, 2), c, 0, 2), ('source02', (0, 2), c, 0, 3),
        ('new13', (1, 3), raw, 0, 4)):
        h = g.subgraph(v for v in g if coloring[v] in colors)
        if nx.has_path(h, u, v):
            return dict(reason='required_separation_violated', layer=label,
                        path=nx.shortest_path(h, u, v))
    for a, b, d, e in combinations(range(5), 4):
        for p, q in product(gamma_paths(g, a, d), gamma_paths(g, b, e)):
            if not set(p) & set(q):
                assert all(g.has_edge(x, y) for r in (p, q) for x, y in zip(r, r[1:]))
                return dict(reason='alternating_disjoint_gamma_paths', paths=[p, q])
    return None


def build():
    # a,b,p,q are the already-proved witnesses, not newly searched vertices.
    # r is the sole remaining vertex. Enumerate only typed simple path choices
    # in a relaxed supergraph; arbitrary extra edges are NOT enumerated.
    records, counts = [], Counter()
    for color in range(4):
        for inside in ((False, True) if color in (0, 1) else (False,)):
            c = dict(enumerate([0, 1, 0, 2, 1, 0, 1, 2, 3, color]))
            selected = {0, 1, 2, 5, 6} | ({9} if inside else set())
            allowed = nx.Graph()
            allowed.add_nodes_from(range(10))
            for u, v in combinations(range(10), 2):
                if c[u] == c[v]:
                    continue
                if u in FRAME and v in FRAME and [u, v] not in [[1, 2], [2, 3], [3, 4]]:
                    continue
                if c[u] in (0, 1) and c[v] in (0, 1) and ((u in selected) != (v in selected)):
                    continue
                allowed.add_edge(u, v)
            raw = {v: 1-c[v] if v in selected else c[v] for v in allowed}
            old13 = allowed.subgraph(v for v in allowed if c[v] in (1, 3))
            new02 = allowed.subgraph(v for v in allowed if raw[v] in (0, 2))
            ps = [p for p in gamma_paths(old13, 1, 4) if p[1] == 8]
            qs = [p for p in gamma_paths(new02, 1, 3) if p[1] == 7]
            assert ps and qs
            for p, q in product(ps, qs):
                g = nx.Graph()
                g.add_nodes_from(range(10))
                g.add_edges_from(BASE)
                for route in (p, q):
                    g.add_edges_from(zip(route, route[1:]))
                assert all(allowed.has_edge(u, v) for u, v in g.edges())
                result = violation(g, c, selected)
                if result is None:
                    # Any completion must give 0 at least two neighbors.
                    # Test each possible incident edge independently: rejected
                    # edges have monotone obstructions, so cannot be repaired
                    # by any other added edges.
                    for vertex, required in ((0, 2),):
                        excluded, possible = [], []
                        for w in sorted(allowed[vertex]):
                            h = g.copy()
                            h.add_edge(vertex, w)
                            why = violation(h, c, selected)
                            if why:
                                excluded.append(dict(neighbor=w, obstruction=why))
                            else:
                                possible.append(w)
                        if len(possible) < required:
                            result = dict(reason='insufficient_possible_neighbors', vertex=vertex,
                                          required=required, possible=possible, excluded=excluded)
                            break
                assert result is not None, (color, inside, p, q)
                counts[result['reason']] += 1
                counts['path_skeletons'] += 1
                records.append(dict(extra_color=color, extra_in_S=inside, selected=sorted(selected),
                                    coloring=[c[v] for v in range(10)], old13=p, new02=q,
                                    forced_edges=edge_list(g), obstruction=result))
    saved = json.loads(UPSTREAM.read_text())
    for name, expected in saved['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    inputs = {UPSTREAM, Path(__file__).resolve()}
    inputs.update(ROOT / name for name in saved['input_sha256'])
    return dict(schema=1, scope='Symbolic five-inner path lemma; inner degree at most four, degree_G(0)>=2; no graph completion search.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                summary=dict(counts), cases=records,
                closure_effect=dict(profile_deletions=0, inherited_profiles=603, fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    text = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == text, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
