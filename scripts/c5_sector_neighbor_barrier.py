#!/usr/bin/env python3
"""Unbounded path-intersection lemma, replayed on existing controls only."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_saturated_cuts/observations.json'
OUT = ROOT / 'artifacts/c5_sector_neighbor_barrier/observations.json'
FRAME = set(range(5))


def audit(g, c, selected, disk):
    assert all(c[u] != c[v] for u, v in g.edges())
    assert [c[v] for v in range(5)] == [0, 1, 0, 2, 1]
    assert nx.node_connected_component(g.subgraph(v for v in g if c[v] in (0, 1)), 0) == selected
    assert selected & FRAME == {0, 1, 2}
    assert all(g.degree[v] <= 4 for v in set(g) - FRAME)
    assert {tuple(sorted(e)) for e in g.subgraph(FRAME).edges()} == {(1, 2), (2, 3), (3, 4)}
    raw = {v: 1-c[v] if v in selected else c[v] for v in g}
    h2 = g.subgraph(v for v in g if raw[v] in (0, 2))
    h3 = g.subgraph(v for v in g if c[v] in (1, 3))
    paths2 = sorted(list(p) for p in nx.all_simple_paths(h2, 1, 3))
    paths3 = sorted(list(p) for p in nx.all_simple_paths(h3, 1, 4))
    # Check every path pair in the saved graph, not just a chosen shortest pair.
    for p in paths2:
        for q in paths3:
            assert set(p) & set(q) == {1}
    b3 = set(nx.node_connected_component(h2.subgraph(set(h2) - {1}), 3))
    records = []
    for w in sorted(set(g[0]) & b3):
        route = nx.shortest_path(h2.subgraph(b3), w, 3)
        p = [0] + route
        assert len(p) == len(set(p)) and not set(p[1:-1]) & FRAME
        assert c[w] in (1, 2)
        comparisons = []
        for q in paths3:
            common = set(p) & set(q)
            assert common <= {w}
            if common:
                assert c[w] == 1 and w in selected
                assert Counter(c[v] for v in g[w]) == Counter({0: 1, 2: 1, 3: 2})
                assert set(g[w]) & selected == {0}
            if disk:
                assert common == {w}
            comparisons.append(dict(old13=q, intersection=sorted(common)))
        records.append(dict(neighbor=w, route=p, comparisons=comparisons))
    if disk and paths3 and g.degree[0] == 2:
        assert len(records) <= 1
    return dict(old13_paths=paths3, new02_paths=paths2,
                path_pairs=len(paths2)*len(paths3), B3=sorted(b3), neighbors=records)


def build():
    saved = json.loads(UPSTREAM.read_text())
    for name, expected in saved['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    counts, sources, disks = Counter(), [], []
    for old in saved['source_witnesses']:
        g = nx.Graph(old['edges'])
        c = dict(zip(old['vertices'], old['coloring'], strict=True))
        result = audit(g, c, set(old['analysis']['selected']), False)
        counts['source_controls'] += 1
        counts['source_path_pairs'] += result['path_pairs']
        counts['source_disjoint_neighbor_path_pairs'] += sum(
            not row['intersection'] for n in result['neighbors'] for row in n['comparisons'])
        sources.append(dict(source_index=old['source_index'], coloring_id=old['coloring_id'], analysis=result))
    # Revalidate saved rotations directly; do not call a planarity oracle.
    raw_disks = json.loads((ROOT / 'artifacts/c5_sector_targets/observations.json').read_text())
    for old in saved['disk_audits']:
        record = raw_disks['inverse_search']['disk_records'][old['saved_index']]
        closed = nx.Graph(record['edges'])
        apex = max(closed) + 1
        closed.add_edges_from((apex, v) for v in range(5))
        embedding = nx.PlanarEmbedding()
        embedding.set_data({int(v): ns for v, ns in record['apex_rotation'].items()})
        embedding.check_structure()
        assert set(embedding) == set(closed)
        assert {tuple(sorted(e)) for e in embedding.edges()} == {tuple(sorted(e)) for e in closed.edges()}
        g = nx.Graph(old['edges'])
        closed.remove_node(apex)
        closed.remove_edges_from([(0, 1), (0, 4)])
        assert set(closed) == set(g) and {tuple(sorted(e)) for e in closed.edges()} == {tuple(sorted(e)) for e in g.edges()}
        results = []
        for query in old['queries']:
            c = dict(zip(old['vertices'], query['coloring'], strict=True))
            result = audit(g, c, set(query['analysis']['selected']), True)
            counts['disk_moves'] += 1
            counts['disk_path_pairs'] += result['path_pairs']
            counts['disk_old13_applicable'] += bool(result['old13_paths'])
            counts['disk_neighbor_comparisons'] += sum(len(n['comparisons']) for n in result['neighbors'])
            results.append(dict(coloring=query['coloring'], analysis=result))
        disks.append(dict(saved_index=old['saved_index'], queries=results))
    # Typed local incidence certificates: distinct colors force distinct neighbors.
    # These are local proof data, not candidate graphs or realizability examples.
    local = dict(interior_crossing=dict(neighbor_colors=[0, 2, 2, 3, 3], minimum_degree=5),
                 first_neighbor_crossing=dict(neighbor_colors=[0, 2, 3, 3], degree=4,
                                              S_neighbors=['frame0']))
    assert len(local['interior_crossing']['neighbor_colors']) > 4
    assert Counter(local['first_neighbor_crossing']['neighbor_colors'])[0] == 1
    inputs = {UPSTREAM, Path(__file__).resolve()}
    inputs.update(ROOT / name for name in saved['input_sha256'])
    return dict(schema=1, scope='Necessary unbounded path and neighbor lemmas; no general transition exclusion.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                summary=dict(counts), local_incidence=local, source_controls=sources, disk_controls=disks,
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
