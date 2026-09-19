#!/usr/bin/env python3
"""Degree-four saturated star cuts for 397/action 2, with saved disk controls."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import networkx as nx

from c5_sector_forced_connectivity import PAIRS, observed_partition

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_joint_identity/observations.json'
DISKS = ROOT / 'artifacts/c5_sector_targets/observations.json'
OUT = ROOT / 'artifacts/c5_sector_saturated_cuts/observations.json'


def edges(g):
    return sorted(sorted(e) for e in g.edges())


def subdivision(g, p, q):
    """Build and directly verify the nine paths; no planarity oracle."""
    a, b, c, d = p[0], q[0], p[-1], q[-1]
    assert a < b < c < d
    assert not set(p) & set(q)
    assert not (set(p[1:-1]) | set(q[1:-1])) & set(range(5))
    inner = g.subgraph(set(g) - set(range(5)))
    assert nx.is_connected(inner)
    r = min((nx.shortest_path(inner, x, y) for x in p[1:-1] for y in q[1:-1]),
            key=lambda path: (len(path), path))
    assert not set(r[1:-1]) & set(p + q)
    x, y = r[0], r[-1]
    ix, iy = p.index(x), q.index(y)
    nine = [list(range(a, b+1)), list(reversed(list(range(d, 5)) + list(range(a+1)))),
            p[:ix+1], list(reversed(range(b, c+1))), list(range(c, d+1)),
            list(reversed(p[ix:])), list(reversed(q[:iy+1])), q[iy:], list(reversed(r))]
    closed = g.copy()
    closed.add_edges_from([(0, 1), (0, 4)])
    left, right = [a, c, y], [b, d, x]
    used = set()
    for path, (u, v) in zip(nine, product(left, right), strict=True):
        assert (path[0], path[-1]) == (u, v)
        assert len(path) == len(set(path))
        assert all(closed.has_edge(s, t) for s, t in zip(path, path[1:]))
        assert not set(path[1:-1]) & (used | set(left + right))
        used.update(path[1:-1])
    return dict(P=p, Q=q, R=r, left=left, right=right, nine_paths=nine)


def analyze(g, c, selected):
    assert all(c[u] != c[v] for u, v in g.edges())
    assert [c[v] for v in range(5)] == [0, 1, 0, 2, 1]
    actual = nx.node_connected_component(g.subgraph(v for v in g if c[v] in (0, 1)), 0)
    assert actual == selected and selected & set(range(5)) == {0, 1, 2}
    inner = set(g) - set(range(5))
    assert all(g.degree[v] <= 4 for v in inner)
    raw = {v: 1-c[v] if v in selected else c[v] for v in g}
    assert all(raw[u] != raw[v] for u, v in g.edges())
    minus1 = g.subgraph(selected - {1})
    connected = nx.has_path(minus1, 0, 2)
    types = {d: {v for v in selected & inner if c[v] == 1 and
                 Counter(c[w] for w in g[v]) == Counter({0: 2, d: 2})} for d in (2, 3)}
    assert not types[2] & types[3]
    layers = []
    for d, coloring, pair, end in ((2, raw, (0, 2), 3), (3, c, (1, 3), 4)):
        route_graph = g.subgraph(v for v in g if coloring[v] in pair)
        route = nx.shortest_path(route_graph, 1, end) if nx.has_path(route_graph, 1, end) else None
        cut_graph = g.subgraph(selected - {1} - types[d])
        bypass = nx.shortest_path(cut_graph, 0, 2) if nx.has_path(cut_graph, 0, 2) else None
        entry = dict(d=d, saturated_stars=sorted(types[d]), required_route=route,
                     cut_separates=bypass is None, bypass=bypass, nonplanar_certificate=None)
        if route is not None and bypass is not None:
            # Any intersection would have two old-0 neighbors on bypass and
            # two old-d neighbors on route, hence belong to the removed type.
            assert not set(route) & set(bypass)
            entry['nonplanar_certificate'] = subdivision(g, bypass, route)
        layers.append(entry)
    result = dict(selected=sorted(selected), minus1_connects_0_2=connected, layers=layers)
    if connected and all(e['required_route'] is not None and e['cut_separates'] for e in layers):
        path = nx.shortest_path(minus1, 0, 2)
        t2, t3 = [next(v for v in path if v in types[d]) for d in (2, 3)]
        lo, hi = sorted((path.index(t2), path.index(t3)))
        a = next(v for v in path[lo+1:hi] if c[v] == 0)
        d3 = sorted(g[t3])
        d3 = [v for v in d3 if c[v] == 3]
        d2 = next(v for v in sorted(g[t2]) if c[v] == 2 and v != 3)
        six = [t2, t3, a, d2] + d3
        assert len(six) == len(set(six)) == 6 and set(six) <= inner
        result['six_internal_vertices'] = six
    return result


def check_rotation(record):
    closed = nx.Graph(record['edges'])
    apex = max(closed) + 1
    closed.add_edges_from((apex, v) for v in range(5))
    embedding = nx.PlanarEmbedding()
    embedding.set_data({int(v): ns for v, ns in record['apex_rotation'].items()})
    embedding.check_structure()
    assert set(embedding) == set(closed)
    assert {tuple(sorted(e)) for e in embedding.edges()} == {tuple(sorted(e)) for e in closed.edges()}


def build():
    upstream, disks = (json.loads(p.read_text()) for p in (UPSTREAM, DISKS))
    for saved in (upstream, disks):
        for name, expected in saved['input_sha256'].items():
            assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    counts, witnesses = Counter(), []
    source_profile = json.loads((ROOT / 'artifacts/c5_sector_cross_row/observations.json').read_text())['abstract']['states'][397]
    for old in upstream['witnesses']:
        g = nx.Graph(old['edges'])
        c = dict(zip(old['vertices'], old['coloring'], strict=True))
        assert json.loads(json.dumps([observed_partition(g, c, p) for p in PAIRS])) == source_profile['partitions']
        selected = set(old['move']['component'])
        item = analyze(g, c, selected)
        counts['source397_moves'] += 1
        for layer in item['layers']:
            counts['source_applicable_routes'] += layer['required_route'] is not None
            counts['verified_subdivisions'] += layer['nonplanar_certificate'] is not None
        witnesses.append(dict(source_index=old['source_index'], coloring_id=old['coloring_id'],
                              vertices=old['vertices'], coloring=old['coloring'], edges=edges(g), analysis=item))
    # Only previously saved small disk graphs; no new graph or larger search.
    disk_audits = []
    for index, record in enumerate(disks['inverse_search']['disk_records']):
        counts['saved_disk_graphs'] += 1
        g = nx.Graph(record['edges'])
        g.remove_edges_from([(0, 1), (0, 4)])
        if set(g[0]) & set(g[4]):
            continue
        check_rotation(record)
        counts['no_common_neighbor_disk_graphs'] += 1
        inner = sorted(set(g) - set(range(5)))
        assert g.degree[0] == 2 and all(g.degree[v] == 4 for v in inner)
        assert nx.is_connected(g.subgraph(inner))
        queries = []
        for cs in product(range(4), repeat=len(inner)):
            c = dict(enumerate((0, 1, 0, 2, 1))) | dict(zip(inner, cs))
            if any(c[u] == c[v] for u, v in g.edges()):
                continue
            counts['disk_proper_source_row_colorings'] += 1
            selected = nx.node_connected_component(g.subgraph(v for v in g if c[v] in (0, 1)), 0)
            if selected & set(range(5)) != {0, 1, 2}:
                continue
            counts['disk_selected_moves'] += 1
            item = analyze(g, c, selected)
            profile = [observed_partition(g, c, pair) for pair in PAIRS]
            counts['disk_exact_source397'] += json.loads(json.dumps(profile)) == source_profile['partitions']
            for layer in item['layers']:
                assert layer['nonplanar_certificate'] is None
                if layer['required_route'] is not None:
                    assert layer['cut_separates']
                    counts[f'disk_applicable_d{layer["d"]}'] += 1
                    counts['disk_nonvacuous_cuts'] += item['minus1_connects_0_2']
            counts['disk_both_required_routes'] += all(e['required_route'] is not None for e in item['layers'])
            queries.append(dict(coloring=[c[v] for v in sorted(g)],
                                source_profile=profile,
                                analysis=item))
        disk_audits.append(dict(saved_index=index, vertices=sorted(g), edges=edges(g), queries=queries))
    inputs = {UPSTREAM, DISKS, Path(__file__).resolve()}
    for saved in (upstream, disks):
        inputs.update(ROOT / p for p in saved['input_sha256'])
    return dict(schema=1, baseline='3aaca0b',
        scope='Necessary degree-four disk cuts and conditional six-inner-vertex bound; '
              'saved controls only, no profile deletion, no general 3903 exclusion.',
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
        summary=dict(counts), source_witnesses=witnesses, disk_audits=disk_audits,
        closure_effect=dict(profile_deletions=0, inherited_profiles=603, fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
