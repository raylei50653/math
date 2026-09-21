#!/usr/bin/env python3
"""Symbolic leaf-exception bounds; no candidate graphs or completions searched."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_neighbor_barrier/observations.json'
OUT = ROOT / 'artifacts/c5_sector_leaf_exception/observations.json'
FRAME = set(range(5))
W, B, A, P, Q, R, U = range(5, 12)


def check_path(g, path, c=None, pair=None):
    assert len(path) == len(set(path))
    assert all(g.has_edge(x, y) for x, y in zip(path, path[1:]))
    if c is not None:
        assert all(c[v] in pair for v in path)


def alternating(g, first, second):
    check_path(g, first)
    check_path(g, second)
    assert not set(first) & set(second)
    assert not (set(first[1:-1]) | set(second[1:-1])) & FRAME
    assert first[0] < second[0] < first[-1] < second[-1]
    return dict(reason='alternating_disjoint_gamma_paths', paths=[first, second])


def cut_equality(color):
    c = dict(enumerate([0, 1, 0, 2, 1, 1, 1, 0, 2, 3, 3, color]))
    selected = {0, 1, 2, W, B, A} | ({U} if color == 1 else set())
    raw = {v: 1-c[v] if v in selected else c[v] for v in c}
    paths = [[0, B, A, 1], [1, Q, W, R, 4], [1, P, U, 3], [0, W, P, U, 3]]
    g = nx.Graph()
    g.add_nodes_from(c)
    g.add_edges_from([(1, 2), (2, 3), (3, 4)])
    for path in paths:
        g.add_edges_from(zip(path, path[1:]))
    # This is a forced edge skeleton, not a completed realization of S.
    assert all(c[x] != c[y] for x, y in g.edges())
    assert all(raw[x] != raw[y] for x, y in g.edges())
    assert all(g.degree[v] <= 4 for v in set(g) - FRAME)
    check_path(g, paths[0], c, (0, 1))
    check_path(g, paths[1], c, (1, 3))
    check_path(g, paths[2], raw, (0, 2))
    assert Counter(c[v] for v in g[W]) == Counter({0: 1, 2: 1, 3: 2})
    excluded, possible = [], []
    for v in sorted(set(g) - {B}):
        h = g.copy()
        h.add_edge(B, v)
        if c[v] == c[B]:
            why = dict(reason='improper', edge=[B, v])
        elif c[v] in (0, 1) and v not in selected:
            why = dict(reason='maximal_S_violated', edge=[B, v])
        elif v == 2:
            check_path(h, [0, B, 2], c, (0, 1))
            why = dict(reason='frame_cut_violated', path=[0, B, 2])
        elif v in (3, P):
            route = [0, B, 3] if v == 3 else [0, B, P, U, 3]
            why = alternating(h, route, paths[1])
        else:
            assert v in (0, A, Q, R)
            possible.append(v)
            continue
        excluded.append(dict(neighbor=v, obstruction=why))
    assert set(possible) == {0, A, Q, R}
    h = g.copy()
    h.add_edges_from([(B, Q), (B, R)])
    bypass = [1, Q, B, R, 4]
    check_path(h, bypass, c, (1, 3))
    pair_obstruction = alternating(h, paths[3], bypass)
    return dict(extra_color=color, extra_in_S=color == 1,
                coloring=[c[v] for v in sorted(c)], selected=sorted(selected),
                forced_edges=sorted(sorted(e) for e in g.edges()), forced_paths=paths,
                b_possible_neighbors=possible, excluded=excluded,
                incompatible_neighbor_pair=[Q, R], pair_obstruction=pair_obstruction,
                b_degree_upper_bound=3)


def noncut_witnesses():
    # Waypoints represent possibly long paths, not edges or newly built graphs.
    records = []
    for order in (['w', 't3'], ['t3', 'w']):
        waypoints = ['frame1'] + order + ['frame4']
        intervals = [dict(start=x, end=y, internal_old3=f'd3_{i}')
                     for i, (x, y) in enumerate(zip(waypoints, waypoints[1:]))]
        witnesses = {'w': 1, 't2': 1, 't3': 1, 'a': 0, 'p': 2,
                     'd3_0': 3, 'd3_1': 3, 'd3_2': 3}
        assert len(witnesses) == 8
        assert Counter(witnesses.values()) == Counter({0: 1, 1: 3, 2: 1, 3: 3})
        records.append(dict(old13_waypoint_order=waypoints, disjoint_open_intervals=intervals,
                            eight_internal_witness_colors=witnesses))
    return records


def build():
    saved = json.loads(UPSTREAM.read_text())
    for name, expected in saved['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    cases = [cut_equality(color) for color in (0, 1)]
    noncut = noncut_witnesses()
    inputs = {UPSTREAM, Path(__file__).resolve()}
    inputs.update(ROOT / name for name in saved['input_sha256'])
    return dict(schema=1,
                scope='Conditional bounds for N(0) intersect B3 nonempty: cut >=7 under degree<=4, >=8 under degree=4; noncut >=8 under degree<=4.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                summary=dict(cut_seven_inner_types=len(cases),
                             individual_neighbor_exclusions=sum(len(c['excluded']) for c in cases),
                             incompatible_neighbor_pairs=len(cases), noncut_waypoint_orders=len(noncut)),
                cut_equality=cases, noncut_witnesses=noncut,
                closure_effect=dict(profile_deletions=0, inherited_profiles=603, fixed_point_recomputed=False))


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
