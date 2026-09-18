#!/usr/bin/env python3
"""Two disjoint long odd cycles: both contraction orders and source witnesses.

Read-only --check; no planarity oracle or regeneration of earlier certificates.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

import networkx as nx

import c5_degree5_long_triangle_minors as mixed
from c5_k4_blocks import Q, coloring

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_two_long_cycles/observations.json'
Z, D = 5, 3
tree, odd = mixed.tree, mixed.odd


def criticality(graph, lengths):
    assert graph.degree(Z) == 5
    assert set(graph[Z]) & set(range(5)) == {0, 1, 4}
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    inner = graph.subgraph([v for v in graph if v > Z])
    cycles = nx.cycle_basis(inner)
    assert nx.is_connected(inner) and sorted(map(len, cycles)) == sorted(lengths)
    assert len(cycles) == 2 and not set(cycles[0]) & set(cycles[1])
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z, b) for b in (0, 1, 4))
    ws = [coloring(relaxed, dict(enumerate(Q)) | {Z: a}) for a in range(4)]
    assert [a for a, w in enumerate(ws) if w is None] == [D]
    deletions = []
    for e in tree.edges(graph):
        if e in tree.CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        w = coloring(child, dict(enumerate(Q)))
        assert w is not None, e
        assert all(w[b] == Q[b] for b in range(5))
        assert all(w[u] != w[v] for u, v in child.edges)
        deletions.append(dict(edge=e, colors=[w[v] for v in sorted(graph)]))
    return dict(vertices=sorted(graph), degrees=[[v, graph.degree(v)] for v in sorted(graph)],
                z_colors=[None if w is None else [w[v] for v in sorted(graph)] for w in ws],
                deletions=deletions)


def root_rows(graph, bridge):
    """Cut each bridge endpoint towards the other cycle, retain its own arm.

    Boundary q and z=a are shared pins. No marginalization across different a.
    The actual source graph, including D leaves, determines every row.
    """
    result = []
    for r, neighbor in ((bridge[0], bridge[1]), (bridge[-1], bridge[-2])):
        inner = graph.subgraph([v for v in graph if v > Z]).copy()
        inner.remove_edge(r, neighbor)
        component = nx.node_connected_component(inner, r)
        side = graph.subgraph(set(component) | set(range(6))).copy()
        side.remove_edges_from((Z, b) for b in (0, 1, 4))
        assert len(set(side[Z])-set(range(5))) == 1
        rows = [[c for c in range(4) if coloring(
            side, dict(enumerate(Q)) | {Z: a, r: c}) is not None] for a in range(4)]
        assert all(rows) and len(rows[D]) == 1
        result.append(dict(root=r, rows=rows))
    return result


def build():
    saved = json.loads(mixed.OUT.read_text())
    dependencies = {str(Path(__file__).relative_to(ROOT))}
    for name, digest in saved['source_sha256'].items():
        assert tree.digest(ROOT/name) == digest, name
        dependencies.add(name)
    for name, digest in saved['input_sha256'].items():
        assert tree.digest(ROOT/name) == digest, name
    records, counts, palette_pairs = [], Counter(), set()
    lengths_domain = ((1, 2, 2), (2, 1, 4), (3, 4, 2))
    for index, row in enumerate(saved['controls']):
        target = nx.Graph(row['target_edges'])
        first = nx.Graph(row['source_edges'])  # cycle 1 long, cycle 2 triangle
        c1 = row['retained']
        cycles = nx.cycle_basis(target.subgraph([v for v in target if v > Z]))
        c2 = sorted(next(c for c in cycles if not set(c) & set(c1)))
        f = row['form']
        if 'word' in f:
            _, bans, _ = mixed.arms.skeleton(f)
        else:
            _, bans = mixed.marks.skeleton(f)
        palette2 = sorted(mixed.U-bans[next(v for v in c2 if len(bans[v]) == 2)])
        palette_pairs.add((tuple(row['palette']), tuple(palette2)))
        l1 = sum(len(p)-1 for p in row['cycle_paths'])
        variant = [5, 7, 9].index(l1)
        lengths2 = lengths_domain[(variant+1) % 3]
        l2 = sum(lengths2)
        source, b2, paths2 = odd.expand_cycle(first, c2, set(palette2), lengths2, variant+1)
        b1 = {b['target']: b['source'] for b in row['minor']['branch_sets']}
        new2 = set(source)-set(first)
        second = source.subgraph(set(target) | new2).copy()  # opposite intermediate
        second.add_edges_from(zip(c1, c1[1:]+c1[:1]))
        source_to_second = dict(b1) | {v: [v] for v in sorted(new2)}
        second_to_target = {v: b2[v] for v in target}
        bridge = min((nx.shortest_path(target.subgraph([v for v in target if v > Z]), u, v)
                      for u in c1 for v in c2), key=lambda p: (len(p), p))
        graphs = (source, first, second, target)
        expected_lengths = ((l1, l2), (l1, 3), (3, l2), (3, 3))
        checks = [criticality(g, ls) for g, ls in zip(graphs, expected_lengths)]
        rows = [root_rows(g, bridge) for g in graphs]
        assert all(r == rows[0] for r in rows)
        steps = [tree.validate_minor(source, first, b2),
                 tree.validate_minor(first, target, b1),
                 tree.validate_minor(source, second, source_to_second),
                 tree.validate_minor(second, target, second_to_target)]
        composed = tree.compose_minor(b2, b1)
        opposite = tree.compose_minor(source_to_second, second_to_target)
        assert composed == opposite and composed[Z] == [Z]
        # Every edge outside the two replaced cycles survives in the source.
        cycle_edges = {tuple(sorted(e)) for c in (c1, c2) for e in zip(c, c[1:]+c[:1])}
        assert set(tree.edges(target))-cycle_edges <= set(tree.edges(source))
        witness = row['target_subdivision']
        augmented = target.copy()
        augmented.add_edges_from((max(target)+1, b) for b in range(5))
        tree.validate_subdivision(augmented, witness)
        counts['_'.join(row['endpoint_types'])] += 1
        records.append(dict(mixed_control=index, endpoint_types=row['endpoint_types'],
            palettes=[row['palette'], palette2], lengths=[l1, l2], bridge=bridge,
            cycle_paths=[row['cycle_paths'], paths2],
            graphs=[dict(name=n, edges=tree.edges(g), root_rows=r, **check)
                    for n, g, r, check in zip(('source', 'first_long', 'second_long', 'target'),
                                              graphs, rows, checks)],
            steps=steps, orders=[[0, 1], [2, 3]],
            composed_minor=tree.validate_minor(source, target, composed),
            target_subdivision=witness,
            source_obstruction=tree.topology_on_source(source, target, composed, witness)))
    assert counts == {a+'_'+b: 36 for a in ('same', 'distinct') for b in ('same', 'distinct')}
    return dict(schema=1,
        scope='Two disjoint odd-cycle blocks, three-spoke fixed-q degree-five obstruction; unbounded proof in report, not Lean.',
        source_sha256={n: tree.digest(ROOT/n) for n in sorted(dependencies)},
        input_sha256={str(mixed.OUT.relative_to(ROOT)): tree.digest(mixed.OUT)},
        networkx_version=nx.__version__, controls=records,
        summary=dict(sources=len(records), endpoint_types=dict(counts),
            ordered_lengths=[[5, 7], [7, 9], [9, 5]], palette_pairs=len(palette_pairs),
            contraction_orders=2*len(records), step_minors=4*len(records),
            root_pin_queries=4*2*4*4*len(records),
            source_deletion_colorings=sum(len(r['graphs'][0]['deletions']) for r in records),
            all_deletion_colorings=sum(len(g['deletions']) for r in records for g in r['graphs'])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
