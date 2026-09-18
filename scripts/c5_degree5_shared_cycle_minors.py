#!/usr/bin/env python3
"""Shared odd cycles: boundary-fixed minors and fixed-q source witnesses.

Read-only --check replays saved R15 subdivisions, without a planarity oracle.
Unbounded coverage is proved separately in the accompanying report.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

import networkx as nx

import c5_degree5_shared_triangles as shared
import c5_degree5_shared_cycle_roots as roots
import c5_degree5_odd_cycle_components as odd
from c5_k4_blocks import Q, U, coloring

tree = shared.tree
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_shared_cycle_minors/observations.json'
Z, D = 5, 3


def cycle_data(form):
    skeleton, bans = shared.skeleton(form)
    cycles = sorted(sorted(c) for c in nx.cycle_basis(skeleton.subgraph(
        [v for v in skeleton if v > Z])))
    common, = set(cycles[0]) & set(cycles[1])
    cycles = [[common] + [v for v in c if v != common] for c in cycles]
    if form['kind'] in ('same', 'opposite'):
        palettes = [form['palette'], sorted(U-set(form['palette']))]
    else:
        palettes = [sorted(U-bans[next(v for v in c if v != common and len(bans[v]) == 2)])
                    for c in cycles]
    assert set(palettes[0]) == U-set(palettes[1])
    return cycles, palettes, common


def selected_targets(saved):
    buckets = {}
    for index, row in enumerate(saved['templates']):
        f = row['form']
        _, palettes, _ = cycle_data(f)
        key = (f['kind'], tuple(palettes[0]))
        score = len(shared.skeleton(f)[0])
        if key not in buckets:
            buckets[key] = [(score, index), (score, index)]
        if score < buckets[key][0][0]:
            buckets[key][0] = (score, index)
        if score > buckets[key][1][0]:
            buckets[key][1] = (score, index)
    assert set(buckets) == {(k, tuple(sorted(p))) for k in ('same', 'opposite', 'marked')
                            for p in tree.PAIRS}
    for key, pair in sorted(buckets.items()):
        for size, (_, index) in zip(('short', 'long'), pair):
            yield key, size, index


def graph_check(graph, lengths, common, forbidden=(D,), critical=True):
    assert graph.degree(Z) == 5
    assert set(graph[Z]) & set(range(5)) == {0, 1, 4}
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    inner = graph.subgraph([v for v in graph if v > Z])
    cycles = nx.cycle_basis(inner)
    assert nx.is_connected(inner) and len(cycles) == 2
    assert sorted(map(len, cycles)) == sorted(lengths)
    assert set(cycles[0]) & set(cycles[1]) == {common}
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z, b) for b in (0, 1, 4))
    vertices = sorted(graph)

    def witness(g, pins):
        w = coloring(g, pins)
        if w is None:
            return None
        assert all(w[v] == c for v, c in pins.items())
        assert all(w[u] != w[v] for u, v in g.edges)
        return [w[v] for v in vertices]

    rows = [witness(relaxed, dict(enumerate(Q)) | {Z: a}) for a in range(4)]
    assert [a for a, w in enumerate(rows) if w is None] == list(forbidden)
    deletions = []
    if critical:
        for e in tree.edges(graph):
            if e in tree.CYCLE:
                continue
            child = graph.copy()
            child.remove_edge(*e)
            w = witness(child, dict(enumerate(Q)))
            assert w is not None, e
            deletions.append(dict(edge=e, colors=w))
    return dict(vertices=vertices, degrees=[[v, graph.degree(v)] for v in vertices],
                z_colors=rows, deletions=deletions)


def build():
    saved = json.loads(shared.OUT.read_text())
    interface = json.loads(roots.OUT.read_text())
    dependencies = {str(Path(__file__).relative_to(ROOT)),
                    'scripts/c5_degree5_odd_cycle_components.py'}
    for old in (saved, interface):
        for name, digest in old['source_sha256'].items():
            assert tree.digest(ROOT/name) == digest, name
            dependencies.add(name)
        for name, digest in old.get('input_sha256', {}).items():
            assert tree.digest(ROOT/name) == digest, name
    arc = {3: (1, 1, 1), 5: (1, 2, 2), 7: (2, 1, 4), 9: (3, 4, 2)}
    domain = ((5, 3), (3, 7), (5, 7), (7, 9), (9, 5))
    records, counts = [], Counter()
    for key, size, index in selected_targets(saved):
        row = saved['templates'][index]
        form, choices = row['form'], row['representative_choices']
        target = shared.make_graph(form, choices)
        cycles, palettes, common = cycle_data(form)
        witness = shared.subdivision_for(target, saved['subdivisions'])
        for variant, (l1, l2) in enumerate(domain):
            first, b1, paths1 = odd.expand_cycle(target, cycles[0], set(palettes[0]), arc[l1], variant)
            source, b2, paths2 = odd.expand_cycle(first, cycles[1], set(palettes[1]), arc[l2], variant+1)
            new2 = set(source)-set(first)
            second = source.subgraph(set(target) | new2).copy()
            second.add_edges_from(zip(cycles[0], cycles[0][1:]+cycles[0][:1]))
            source_to_second = dict(b1) | {v: [v] for v in sorted(new2)}
            second_to_target = {v: b2[v] for v in target}
            graphs = (source, first, second, target)
            lengths = ((l1, l2), (l1, 3), (3, l2), (3, 3))
            checks = [graph_check(g, ls, common) for g, ls in zip(graphs, lengths)]
            assert all([w is not None for w in c['z_colors']] == [True, True, True, False]
                       for c in checks)
            steps = [tree.validate_minor(source, first, b2),
                     tree.validate_minor(first, target, b1),
                     tree.validate_minor(source, second, source_to_second),
                     tree.validate_minor(second, target, second_to_target)]
            composed = tree.compose_minor(b2, b1)
            opposite = tree.compose_minor(source_to_second, second_to_target)
            assert composed == opposite and composed[Z] == [Z]
            assert all(set(composed[v]) & set(target) == {v} for v in target)
            cycle_edges = {tuple(sorted(e)) for c in cycles for e in zip(c, c[1:]+c[:1])}
            assert set(tree.edges(target))-cycle_edges <= set(tree.edges(source))
            counts[key[0]] += 1
            records.append(dict(template=index, form=form, choices=choices, path_size=size,
                palettes=palettes, retained=cycles, shared_root=common, lengths=[l1, l2],
                cycle_paths=[paths1, paths2],
                graphs=[dict(name=n, edges=tree.edges(g), **check) for n, g, check in
                        zip(('source', 'first_long', 'second_long', 'target'), graphs, checks)],
                steps=steps, orders=[[0, 1], [2, 3]],
                composed_minor=tree.validate_minor(source, target, composed),
                target_subdivision=witness,
                source_obstruction=tree.topology_on_source(source, target, composed, witness)))
    # Actual graph control: rejecting D alone does not establish minimality.
    form = dict(kind='marked', walk=[D, 0, D], mark=0)
    _, bans = shared.skeleton(form)
    choices = [opts[0] for opts in shared.triangle.attachment_options(bans)]
    target = shared.make_graph(form, choices)
    cycles, palettes, common = cycle_data(form)
    first, b1, _ = odd.expand_cycle(target, cycles[0], set(palettes[0]), arc[5], 0)
    source, b2, _ = odd.expand_cycle(first, cycles[1], set(palettes[1]), arc[7], 1)
    negative = []
    for g, ls in ((source, (5, 7)), (target, (3, 3))):
        check = graph_check(g, ls, common, forbidden=(0, D), critical=False)
        child = g.copy()
        child.remove_edge(Z, 0)
        assert coloring(child, dict(enumerate(Q))) is None
        negative.append(dict(edges=tree.edges(g), **check, failed_deletion=[Z, 0]))
    assert counts == dict(same=60, opposite=60, marked=60)
    return dict(schema=1,
        scope='Shared two odd-cycle blocks, fixed-q three-spoke degree-five source minors; paper coverage, not Lean or full Sigma.',
        source_sha256={n: tree.digest(ROOT/n) for n in sorted(dependencies)},
        input_sha256={str(p.relative_to(ROOT)): tree.digest(p) for p in (shared.OUT, roots.OUT)},
        networkx_version=nx.__version__, controls=records,
        double_forbidden_control=dict(form=form, choices=choices, graphs=negative,
            minor=tree.validate_minor(source, target, tree.compose_minor(b2, b1))),
        summary=dict(sources=len(records), endpoint_types=dict(counts), targets=36,
            ordered_lengths=[list(p) for p in domain], contraction_orders=2*len(records),
            step_minors=4*len(records), z_color_queries=16*len(records),
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
