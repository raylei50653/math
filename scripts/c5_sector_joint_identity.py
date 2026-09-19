#!/usr/bin/env python3
"""Joint retained bases and frame-4 cuts for the fixed 397/action-2 query."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_sector_common_core import CROSS, SOURCE, components, project, packed
from c5_sector_forced_connectivity import PAIRS, observed_partition

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_common_core/observations.json'
OUT = ROOT / 'artifacts/c5_sector_joint_identity/observations.json'


def joint_interface(g, c, selected):
    """Both layers use the same original vertex IDs, including outside vertices."""
    assert {c[v] for v in selected} <= {0, 1}
    stars = {x: sorted(v for v in selected if c[v] == x) for x in (0, 1)}
    outside = sorted(v for v in g if c[v] == 1 and v not in selected)
    layers, owners = [], {}
    for d in (2, 3):
        h = g.subgraph(outside + sorted(v for v in g if c[v] == d))
        blocks = components(h)
        base = nx.Graph()
        owner = {}
        for i, block in enumerate(blocks):
            base.add_node(f'r{i}', members=list(block), marks=[v for v in block if v < 5])
            owner.update((v, f'r{i}') for v in block)
        layer = dict(d=d, retained_blocks=blocks,
                     retained_edges=sorted(sorted(e) for e in h.edges()), extensions={})
        for side, x in (('old', 1), ('new', 0)):
            q = base.copy()
            incidences = []
            for v in stars[x]:
                q.add_node(f's{v}', vertex=v, marks=[v] if v < 5 else [])
                neighbors = sorted(w for w in g[v] if c[w] == d)
                incidences.extend([v, w] for w in neighbors)
                q.add_edges_from((f's{v}', owner[w]) for w in neighbors)
                # Properness / maximality: no omitted star-to-outside edges.
                assert not set(g[v]) & set(outside)
            groups = sorted(tuple(sorted(block)) for block in nx.connected_components(q))
            node_group = {n: i for i, block in enumerate(groups) for n in block}
            vertex_group = {v: node_group[n] for v, n in owner.items()}
            vertex_group.update((v, node_group[f's{v}']) for v in stars[x])
            owners[d, side] = vertex_group
            root = next(block for block in groups if owner[4] in block)
            # Save a full closed cut, including unmarked quotient nodes.
            assert all((u in root) == (v in root) for u, v in q.edges())
            layer['extensions'][side] = dict(
                incidences=incidences, quotient=packed(q), partition=project(q),
                components=groups, root4_nodes=root,
                root4_vertices=sorted(v for v, k in vertex_group.items()
                                      if k == vertex_group[4]))
        layers.append(layer)
    # Shared vertices are joined by ORIGINAL ID, never by local component number.
    identities = []
    relevant = set(outside) | selected | {v for v in g if c[v] in (2, 3)}
    for v in sorted(relevant):
        identities.append(dict(vertex=v, old_color=c[v], selected=v in selected,
            memberships=[dict(d=d, side=side, component=owners[d, side].get(v))
                         for d in (2, 3) for side in ('old', 'new')]))
    return dict(stars=stars, outside1=outside,
                selected_edges=sorted(sorted(e) for e in g.subgraph(selected).edges()),
                identities=identities, layers=layers), owners


def build():
    upstream = json.loads(UPSTREAM.read_text())
    for name, expected in upstream['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    saved = json.loads(CROSS.read_text())
    source, target = (saved['abstract']['states'][i] for i in (397, 330))
    assert source['row'] == [0, 1, 0, 2, 1]
    assert target['row'] == [0, 1, 0, 2, 0]
    requirement = next(r for r in saved['abstract']['closed_successors'] if r['state'] == 397)
    assert requirement['successors'][2] == 330
    records = {r['source_index']: r for r in json.loads(SOURCE.read_text())['proper_hits']}
    audits, graph_obstructions, counts = [], [], Counter()
    for control in saved['controls']:
        g = nx.Graph(records[control['source_index']]['sector_edges'])
        g.remove_edges_from([(0, 1), (0, 4)])
        assert sorted(g) == control['vertices']
        common_neighbors = sorted(set(g[0]) & set(g[4]))
        # A target profile separating same-colored 0,4 in every mixed pair
        # forbids a shared neighbor of ANY color, independently of source c.
        assert target['row'][0] == target['row'][4] == 0
        assert all(not any(0 in b and 4 in b for b in target['partitions'][PAIRS.index((0, d))])
                   for d in (1, 2, 3))
        paths = [[0, w, 4] for w in common_neighbors]
        assert all(g.has_edge(p[0], p[1]) and g.has_edge(p[1], p[2]) for p in paths)
        graph_obstructions.append(dict(source_index=control['source_index'],
            common_neighbors_0_4=common_neighbors, paths=paths,
            excludes_target330_on_this_graph=bool(paths)))
        for ci, colors in enumerate(control['colorings']):
            if colors[:5] != source['row']:
                continue
            c = dict(zip(control['vertices'], colors, strict=True))
            profile = [observed_partition(g, c, p) for p in PAIRS]
            if json.loads(json.dumps(profile)) != source['partitions']:
                continue
            assert all(c[u] != c[v] for u, v in g.edges())
            choices = [set(b) for b in components(g.subgraph(v for v in g if c[v] in (0, 1)))
                       if set(b) & set(range(5)) == {0, 1, 2}]
            assert len(choices) == 1
            selected = choices[0]
            matches = [(mi, m) for mi, m in enumerate(control['moves'][ci])
                       if m['pair'] == [0, 1] and set(m['component']) == selected]
            assert len(matches) == 1
            mi, move = matches[0]
            raw = {v: 1-c[v] if v in selected else c[v] for v in g}
            assert all(raw[u] != raw[v] for u, v in g.edges())
            assert [raw[v] for v in range(5)] == [1, 0, 1, 2, 1]
            short_paths = []
            for w in common_neighbors:
                assert c[w] in (2, 3) and w not in selected
                assert raw[w] == c[w]
                short_paths.append(dict(path=[0, w, 4], old_color=c[w], new_raw_pair=[1, c[w]]))
            interface, owners = joint_interface(g, c, selected)
            for layer in interface['layers']:
                d = layer['d']
                for side, coloring in (('old', c), ('new', raw)):
                    extension = layer['extensions'][side]
                    assert extension['partition'] == observed_partition(g, coloring, (1, d))
                    actual = components(g.subgraph(v for v in g if coloring[v] in (1, d)))
                    predicted = sorted(sorted(v for v, k in owners[d, side].items() if k == i)
                                       for i in range(len(extension['components'])))
                    assert predicted == actual
                    counts['full_vertex_partition_checks'] += 1
            # FRAME makes the positive new-12 requirement automatic.
            assert g.has_edge(2, 3) and g.has_edge(3, 4)
            assert owners[2, 'new'][2] == owners[2, 'new'][3] == owners[2, 'new'][4]
            tests = dict(new12_0_separate_4=owners[2, 'new'][0] != owners[2, 'new'][4],
                         new13_0_separate_4=owners[3, 'new'][0] != owners[3, 'new'][4],
                         new13_2_separate_4=owners[3, 'new'][2] != owners[3, 'new'][4],
                         new13_0_separate_2=owners[3, 'new'][0] != owners[3, 'new'][2])
            projected_match = all(json.loads(json.dumps(layer['extensions']['new']['partition'])) ==
                                  target['partitions'][PAIRS.index((0, layer['d']))]
                                  for layer in interface['layers'])
            assert all(tests.values()) == projected_match
            # A shortest old-13 path's last selected star is a mandatory old port.
            path = nx.shortest_path(g.subgraph(v for v in g if c[v] in (1, 3)), 1, 4)
            last = max(i for i, v in enumerate(path) if v in selected)
            port, neighbor = path[last:last+2]
            assert c[port] == 1 and c[neighbor] == 3
            h3root = next(b for b in interface['layers'][1]['retained_blocks'] if 4 in b)
            assert set(path[last+1:]) <= set(h3root)
            assert all(owners[3, 'new'][v] == owners[3, 'new'][4] for v in path[last+1:])
            s_paths = [nx.shortest_path(g.subgraph(selected), v, port) for v in (0, 2)]
            counts['source_moves'] += 1
            counts['old13_port_witnesses'] += 1
            counts['target_two_rows_match'] += projected_match
            for name, passed in tests.items():
                counts[f'failed_{name}'] += not passed
            audits.append(dict(source_index=control['source_index'], coloring_id=ci, move_id=mi,
                vertices=control['vertices'], coloring=colors, edges=sorted(sorted(e) for e in g.edges()),
                move=move, interface=interface, tests=tests, target_two_rows_match=projected_match,
                shared_neighbor_obstructions=short_paths,
                old13_port=dict(path=path, star=port, d_vertex=neighbor,
                                retained_suffix=path[last+1:], selected_paths=s_paths)))
    assert audits
    inputs = {UPSTREAM, CROSS, SOURCE, Path(__file__).resolve()}
    inputs.update(ROOT / p for p in upstream['input_sha256'])
    return dict(schema=1, baseline='3aaca0b',
                scope='Same-pair joint retained bases, frame-4 cuts and old-13 ports. '
                      'Only existing 397/action-2 controls; no universal exclusion or new graphs.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                summary=dict(controls_scanned=len(saved['controls']),
                             graphs_excluding_target330=sum(bool(r['paths']) for r in graph_obstructions),
                             **counts), witnesses=audits, graph_obstructions=graph_obstructions,
                candidate=dict(source=397, action=2, target=330,
                               tested_new_raw_pairs=[[1, 2], [1, 3]],
                               full_transition_decided=False),
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
