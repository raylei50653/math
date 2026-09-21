#!/usr/bin/env python3
"""Frame-1 cut branch: colored witnesses and forced four-inner obstruction."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_sector_saturated_cuts import analyze, check_rotation, subdivision, edges

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_saturated_cuts/observations.json'
OUT = ROOT / 'artifacts/c5_sector_frame_cut/observations.json'


def audit(g, c, selected):
    base = analyze(g, c, selected)
    if base['minus1_connects_0_2']:
        return None
    blocks = sorted(sorted(b) for b in nx.connected_components(g.subgraph(selected - {1})))
    path = nx.shortest_path(g.subgraph(selected - {2}), 0, 1)
    assert not set(path[1:-1]) & set(range(5))
    b, a = path[1], path[-2]
    assert c[b] == 1 and c[a] == 0 and a != b
    portals = []
    for block in blocks:
        ns = sorted(set(g[1]) & set(block))
        assert ns and all(c[v] == 0 for v in ns)
        portals.append(dict(block=block, neighbors_of_1=ns))
    four = [a, b]
    neighbors = [a, 2]
    last_entry = None
    for layer in base['layers']:
        route = layer['required_route']
        if route is None:
            continue
        w = route[1]
        assert w >= 5 and c[w] == layer['d']
        four.append(w)
        neighbors.append(w)
        if layer['d'] == 3:
            t = next(v for v in reversed(route) if v in selected)
            last_entry = dict(vertex=t, block=next((i for i, bs in enumerate(blocks) if t in bs), None))
    assert len(set(four)) == len(four) and set(four) <= set(g) - set(range(5))
    assert len(set(neighbors)) == len(neighbors) and set(neighbors) <= set(g[1])
    raw = {v: 1-c[v] if v in selected else c[v] for v in g}
    cuts = []
    for d, pairs in ((2, [(0, 4)]), (3, [(0, 2), (0, 4), (2, 4)])):
        h = g.subgraph(v for v in g if raw[v] in (1, d))
        for u, v in pairs:
            component = sorted(nx.node_connected_component(h, u))
            cuts.append(dict(d=d, pair=[u, v], separated=v not in component, component=component))
    return dict(blocks=portals, path_0_1=path, distinct_inner_vertices=four,
                distinct_neighbors_of_1=neighbors, degree_G_1=g.degree[1],
                degree_K_1=g.degree[1]+1, required_routes=base['layers'],
                old13_last_entry=last_entry, new_separations=cuts)


def forced_templates():
    # These are forced SUBGRAPHS in the paper's |C|=4 case, not new
    # degree-regular candidate graphs or an enlargement of the saved corpus.
    # a=5 (old 0), b=6 (old 1), p=7 (old 2), q=8 (old 3).
    forced = [(0, 6), (6, 5), (5, 1), (1, 2), (2, 3), (3, 4),
              (1, 8), (8, 4), (1, 7), (7, 6), (6, 3)]
    result = []
    for connector in (5, 7):
        g = nx.Graph(forced + [(8, connector)])
        cert = subdivision(g, [0, 6, 3], [1, 8, 4])
        result.append(dict(connector=[8, connector], edges=edges(g), certificate=cert))
    return result


def build():
    saved = json.loads(UPSTREAM.read_text())
    for name, expected in saved['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    disks_path = ROOT / 'artifacts/c5_sector_targets/observations.json'
    disks = json.loads(disks_path.read_text())['inverse_search']['disk_records']
    counts = Counter()
    controls = []
    for record in saved['disk_audits']:
        check_rotation(disks[record['saved_index']])
        g = nx.Graph(record['edges'])
        inner = set(g) - set(range(5))
        assert nx.is_connected(g.subgraph(inner))
        assert all(g.degree[v] == 4 for v in inner)
        assert edges(g.subgraph(range(5))) == [[1, 2], [2, 3], [3, 4]]
        for query in record['queries']:
            counts['saved_moves'] += 1
            c = dict(zip(record['vertices'], query['coloring'], strict=True))
            selected = set(query['analysis']['selected'])
            item = audit(g, c, selected)
            if item is None:
                continue
            counts['frame_cut_moves'] += 1
            n = sum(x['required_route'] is not None for x in item['required_routes'])
            counts[f'frame_cut_with_{n}_routes'] += 1
            counts['frame_cut_all_new_separations'] += all(x['separated'] for x in item['new_separations'])
            if n == 2:
                assert len(inner) >= 5
                counts['full_route_cases'] += 1
            if item['old13_last_entry'] is not None:
                counts['last_entry_is_frame1'] += item['old13_last_entry']['vertex'] == 1
            controls.append(dict(saved_index=record['saved_index'], vertices=record['vertices'],
                                 coloring=query['coloring'], analysis=item))
    templates = forced_templates()
    counts['forced_subgraph_subdivisions'] = len(templates)
    inputs = {UPSTREAM, Path(__file__).resolve(), ROOT / 'scripts/c5_sector_saturated_cuts.py'}
    inputs.update(ROOT / name for name in saved['input_sha256'])
    return dict(schema=1, baseline='597890b',
                scope='Paper frame-cut bound |C|>=5 for disk with both routes; saved weaker controls and forced subgraphs only.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                summary=dict(counts), disk_controls=controls, forced_four_inner_subgraphs=templates,
                closure_effect=dict(profile_deletions=0, inherited_profiles=603, fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == text, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
