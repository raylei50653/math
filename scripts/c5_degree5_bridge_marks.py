#!/usr/bin/env python3
"""Marked binary-list interfaces for disjoint triangles; no topology claim.

Finite semantic controls and candidate normal forms. --check is read-only.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

import c5_degree5_tree_components as tree
import c5_degree5_triangle_components as tri
from c5_k4_blocks import Q, U, coloring

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_bridge_marks/observations.json'
D, Z = 3, 5


def forms():
    for f in tri.forms():
        if f['kind'] != 'distinct':
            continue
        for mark in range(len(f['left'])-1):
            yield dict(kind='one', palette=f['palette'], left=list(f['left']),
                       right=list(f['right']), marks=[mark])
    for name, walk in tree.motifs():
        for marks in combinations(range(len(walk)-1), 2):
            yield dict(kind='two', motif=name, walk=list(walk), marks=list(marks))


def skeleton(form):
    if form['kind'] == 'one':
        base = dict(form, kind='distinct')
        graph, bans = tri.skeleton(base)
        walk, first = form['left'], 9
    else:
        base = dict(form, kind='tree')
        graph, bans = tri.skeleton(base)
        walk, first = form['walk'], 6
    for mark in form['marks']:
        root, x = first+mark, max(graph)+1
        pair = {walk[mark], walk[mark+1]}
        assert bans[root] == U-pair
        bans[root], bans[x], bans[x+1] = set(), pair, pair
        graph.add_edges_from(((root, x), (root, x+1), (x, x+1)))
    return graph, bans


def make_graph(form):
    graph, bans = skeleton(form)
    choices = [opts[0] for opts in tri.attachment_options(bans)]
    nxt = max(graph)+1
    for v, c, bs in choices:
        if c == D:
            graph.add_edge(v, nxt)
            graph.add_edges_from((nxt, b) for b in bs)
            nxt += 1
        else:
            graph.add_edge(v, bs[0])
    return graph, choices


def semantics(graph):
    assert graph.degree(Z) == 5
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    interior = graph.subgraph([v for v in graph if v > Z])
    cycles = nx.cycle_basis(interior)
    assert nx.is_connected(interior) and len(cycles) == 2
    assert all(len(c) == 3 for c in cycles) and not set(cycles[0]) & set(cycles[1])
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z, b) for b in (0, 1, 4))
    witnesses = [coloring(relaxed, dict(enumerate(Q)) | {Z: a}) for a in range(4)]
    assert [a for a, w in enumerate(witnesses) if w is None] == [D]
    deletion_witnesses = []
    for e in tree.edges(graph):
        if e in tree.CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        w = coloring(child, dict(enumerate(Q)))
        assert w is not None, e
        deletion_witnesses.append(dict(edge=e, colors=[w[v] for v in sorted(graph)]))
    return dict(z_colors=[None if w is None else [w[v] for v in sorted(graph)] for w in witnesses],
                deletions=deletion_witnesses)


def root_controls():
    rows = []
    for s, t in product(tree.PAIRS, repeat=2):
        actual = {r for r, x, y in product(U, s, t) if len({r, x, y}) == 3}
        assert actual == (U-s if s == t else U)
        rows.append(dict(left=sorted(s), right=sorted(t), root=sorted(actual)))
    return rows


def reductions():
    counts, digest = Counter(), sha256()
    # Mark indices name list steps, not colors. Removed marks lose their gadget.
    def audit(walk, marks, closed):
        original = walk
        initial = marks
        while True:
            if closed:
                step = tree.reduction(walk)
                if step is None:
                    break
                target, retained, _ = step
            else:
                interval = next(((i, j) for i in range(len(walk))
                                 for j in range(i+1, len(walk)) if walk[i] == walk[j]), None)
                if interval is None:
                    break
                i, j = interval
                target = walk[:i]+walk[j:]
                retained = list(range(i))+list(range(j, len(walk)-1))
            assert all({target[k], target[k+1]} == {walk[i], walk[i+1]}
                       for k, i in enumerate(retained))
            marks = tuple(k for k, i in enumerate(retained) if i in marks)
            if closed:
                assert tree.root_bans([{a, b} for a, b in zip(target, target[1:])]) == {D}
            else:
                lists = [{a, b} for a, b in zip(target, target[1:])]
                outputs = [tri.arm_message(lists, a) for a in range(4)]
                assert outputs[D] == {original[-1]}
                assert all(outputs[a] != {original[-1]} for a in range(3))
            counts['steps'] += 1
            walk = tuple(target)
        counts[('closed' if closed else 'open')+'_remaining_'+str(len(marks))] += 1
        digest.update(json.dumps([original, initial, closed, walk, marks]).encode())

    def visit(walk):
        n = len(walk)-1
        if n:
            for mark in range(n):
                audit(walk, (mark,), False)
        if n >= 3 and walk[-1] == D and len(set(walk)) >= 3:
            for marks in combinations(range(n), 2):
                audit(walk, marks, True)
        if n < 6:
            for c in sorted(U-{walk[-1]}):
                visit(walk+(c,))
    visit((D,))
    # A bad unconstrained shortening really loses the single-forbidden-color invariant.
    good, bad = (D, 0, D, 1, D), (D, 1, D)
    assert tree.root_bans([{a, b} for a, b in zip(good, good[1:])]) == {D}
    assert tree.root_bans([{a, b} for a, b in zip(bad, bad[1:])]) == {1, D}
    return dict(max_steps=6, counts=dict(sorted(counts.items())), sha256=digest.hexdigest(),
                negative_control=dict(source=good, target=bad, source_bans=[D], target_bans=[1, D]))


def build():
    rows, counts = [], Counter()
    for form in forms():
        graph, choices = make_graph(form)
        rows.append(dict(form=form, choices=choices, edges=tree.edges(graph), **semantics(graph)))
        counts[form['kind']] += 1
    names = ('c5_degree5_bridge_marks', 'c5_degree5_triangle_components',
             'c5_degree5_tree_components', 'c5_k4_blocks', 'c5_odd_join_cores',
             'c5_disk_deletions', 'c5_cell_enumerator', 'local_closure', 'boundary_relations')
    controls = reductions()
    return dict(schema=1, scope='Fixed-q interfaces and candidate marked normal forms only; no topology or source minor certificate.',
                source_sha256={f'scripts/{n}.py': tree.digest(ROOT/'scripts'/f'{n}.py') for n in names},
                roots=root_controls(), reductions=controls, templates=rows,
                summary=dict(forms=dict(counts), root_queries=36, reduction_counts=controls['counts']))


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
