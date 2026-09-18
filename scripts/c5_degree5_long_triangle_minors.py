#!/usr/bin/env python3
"""Mixed disjoint long-cycle/triangle source minors; no planarity search.

Unbounded reduction is in the accompanying report. --check is read-only.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

import networkx as nx

import c5_degree5_bridge_arms as arms
import c5_degree5_bridge_mark_minors as marked
import c5_degree5_bridge_marks as marks
import c5_degree5_long_triangle_roots as roots
import c5_degree5_odd_cycle_components as odd
import c5_degree5_triangle_components as tri
import c5_degree5_tree_components as tree
from c5_k4_blocks import Q, U, coloring

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_long_triangle_minors/observations.json'
INPUTS = (arms.OUT, marked.OUT, roots.OUT)
Z, D = 5, 3


def criticality(graph, length):
    assert graph.degree(Z) == 5
    assert set(graph[Z]) & set(range(5)) == {0, 1, 4}
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    inner = graph.subgraph([v for v in graph if v > Z])
    cycles = nx.cycle_basis(inner)
    assert nx.is_connected(inner) and sorted(map(len, cycles)) == [3, length]
    assert not set(cycles[0]) & set(cycles[1])
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
        deletions.append(dict(edge=e, colors=[w[v] for v in sorted(graph)]))
    return dict(vertices=sorted(graph), degrees=[[v, graph.degree(v)] for v in sorted(graph)],
                z_colors=[None if w is None else [w[v] for v in sorted(graph)] for w in ws],
                deletions=deletions)


def selected_targets(inputs):
    # Two representatives per (ordered endpoint type, long-cycle palette):
    # shortest and longest available paths. This is a mechanism control domain,
    # not an exhaustive claim about source graphs or target wiring.
    buckets = {}

    def offer(key, score, item):
        if key not in buckets:
            buckets[key] = [(score, item), (score, item)]
        if score < buckets[key][0][0]:
            buckets[key][0] = (score, item)
        if score > buckets[key][1][0]:
            buckets[key][1] = (score, item)

    for i, row in enumerate(inputs[0]['templates']):
        f = row['form']
        score = len(f['a']) + len(f['b']) + len(f['word'])
        offer(('distinct', 'distinct', tuple(f['left'])), score,
              (0, i, [6, 7, 8], f['left']))
    for i, row in enumerate(inputs[1]['templates']):
        f = row['form']
        skeleton, bans = marks.skeleton(f)
        cycles = sorted(sorted(c) for c in nx.cycle_basis(skeleton.subgraph(
            [v for v in skeleton if v > Z])))
        assert len(cycles) == 2
        types = ['same' if any(not bans[v] for v in c) else 'distinct' for c in cycles]
        for j, cycle in enumerate(cycles):
            private = next(v for v in cycle if len(bans[v]) == 2)
            palette = sorted(U-bans[private])
            offer((types[j], types[1-j], tuple(palette)), len(skeleton),
                  (1, i, cycle, palette))
    expected = {(a, b, tuple(sorted(s))) for a in ('same', 'distinct')
                for b in ('same', 'distinct') for s in tree.PAIRS}
    assert set(buckets) == expected
    for key, pair in sorted(buckets.items()):
        for size, (_, item) in zip(('short', 'long'), pair):
            yield key, size, item


def build():
    inputs = [json.loads(p.read_text()) for p in INPUTS]
    dependencies = {str(Path(__file__).relative_to(ROOT))}
    for saved in inputs:
        for name, digest in saved['source_sha256'].items():
            assert tree.digest(ROOT/name) == digest, name
            dependencies.add(name)
        for name, digest in saved.get('input_sha256', {}).items():
            assert tree.digest(ROOT/name) == digest, name
    dependencies.add('scripts/c5_degree5_odd_cycle_components.py')
    records, counts = [], Counter()
    lengths_domain = ((1, 2, 2), (2, 1, 4), (3, 4, 2))
    for key, size, (origin, index, retained, palette) in selected_targets(inputs):
        saved, f = inputs[origin], inputs[origin]['templates'][index]['form']
        if origin == 0:
            _, bans, _ = arms.skeleton(f)
            choices = [opts[0] for opts in tri.attachment_options(bans)]
            target = arms.make_graph(f, choices)
        else:
            target, choices = marks.make_graph(f)
        target_check = criticality(target, 3)
        witness = odd.subdivision_for(target, saved['subdivisions'])
        for variant, lengths in enumerate(lengths_domain):
            source, branches, paths = odd.expand_cycle(target, retained, set(palette), lengths, variant)
            source_check = criticality(source, sum(lengths))
            minor = tree.validate_minor(source, target, branches)
            assert branches[Z] == [Z]
            # All retained vertices and their attachments survive with unchanged
            # incidence; only the selected cycle edges are replaced by arcs.
            cycle_edges = {tuple(sorted(e)) for e in zip(retained, retained[1:]+retained[:1])}
            assert set(tree.edges(target))-cycle_edges <= set(tree.edges(source))
            counts[key[0]+'_'+key[1]] += 1
            records.append(dict(endpoint_types=list(key[:2]), palette=palette, path_size=size,
                input=str(INPUTS[origin].relative_to(ROOT)), template=index, form=f, choices=choices,
                retained=retained, cycle_paths=paths, source_edges=tree.edges(source),
                source_check=source_check, target_edges=tree.edges(target), target_check=target_check,
                minor=minor, target_subdivision=witness,
                source_obstruction=tree.topology_on_source(source, target, branches, witness)))
    assert counts == {a+'_'+b: 36 for a in ('same', 'distinct') for b in ('same', 'distinct')}
    return dict(schema=1,
        scope='Disjoint one long odd cycle plus triangle, three-spoke degree-five fixed-q reduction; paper proof, not Lean.',
        source_sha256={n: tree.digest(ROOT/n) for n in sorted(dependencies)},
        input_sha256={str(p.relative_to(ROOT)): tree.digest(p) for p in INPUTS},
        networkx_version=nx.__version__, controls=records,
        summary=dict(sources=len(records), endpoint_types=dict(counts), cycle_lengths=[5, 7, 9],
                     palettes=6, targets=48, deletion_colorings=sum(
                         len(r['source_check']['deletions']) for r in records)))


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
