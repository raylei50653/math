#!/usr/bin/env python3
"""Disjoint triangles: direct private ports and a bridge color walk.

Unbounded coverage is a paper reduction, not a graph catalogue or Lean proof.
--check replays stored subdivisions without a planarity search.
"""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

import c5_degree5_triangle_components as triangle
import c5_degree5_tree_components as tree
from c5_k4_blocks import CYCLE, Q, U, coloring
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_bridge_triangles/observations.json'
D, Z = 3, 5
PAIRS = tuple(map(frozenset, combinations(range(3), 2)))


def forms():
    for s, t in product(PAIRS, repeat=2):
        for n in range(1, 5):
            for word in permutations(range(4), n):
                if word[0] not in s and word[-1] not in t:
                    yield dict(left=sorted(s), right=sorted(t), word=list(word))


def skeleton(form):
    s, t, word = set(form['left']), set(form['right']), form['word']
    assert D not in s | t and word[0] not in s and word[-1] not in t
    assert all(a != b for a, b in zip(word, word[1:]))
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((Z, b) for b in (0, 1, 4, 7, 10))
    graph.add_edges_from(combinations((6, 7, 8), 2))
    graph.add_edges_from(combinations((9, 10, 11), 2))
    path = [6] + list(range(12, 11+len(word))) + [9]
    graph.add_edges_from(zip(path, path[1:]))
    lists = {6: s | {word[0]}, 7: s | {D}, 8: s,
             9: t | {word[-1]}, 10: t | {D}, 11: t}
    lists.update({v: {a, b} for v, a, b in zip(path[1:-1], word, word[1:])})
    return graph, {v: U-cs for v, cs in lists.items()}, path


def make_graph(form, choices):
    graph, _, _ = skeleton(form)
    nxt = max(graph)+1
    for v, c, bs in choices:
        if c == D:
            graph.add_edge(v, nxt)
            graph.add_edges_from((nxt, b) for b in bs)
            nxt += 1
        else:
            graph.add_edge(v, bs[0])
    return graph


def criticality(graph):
    assert graph.degree(Z) == 5
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    inner = graph.subgraph([v for v in graph if v > Z])
    assert nx.is_connected(inner)
    cycles = nx.cycle_basis(inner)
    assert len(cycles) == 2 and all(len(c) == 3 for c in cycles)
    assert not (set(cycles[0]) & set(cycles[1]))
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z, b) for b in (0, 1, 4))
    ws = [coloring(relaxed, dict(enumerate(Q)) | {Z: a}) for a in range(4)]
    assert [a for a, w in enumerate(ws) if w is None] == [D]
    deletions = []
    for e in tree.edges(graph):
        if e in CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        w = coloring(child, dict(enumerate(Q)))
        assert w is not None, e
        deletions.append(dict(edge=e, coloring=[w[v] for v in sorted(graph)]))
    return dict(z_colorings=[None if w is None else [w[v] for v in sorted(graph)] for w in ws],
                q_deletions=deletions)


def local_controls():
    subsets = [set(cs) for n in range(5) for cs in combinations(range(4), n)]
    joins = []
    for left, right in product(subsets, repeat=2):
        actual = any(x != y for x, y in product(left, right))
        expected = bool(left and right) and not (left == right and len(left) == 1)
        assert actual == expected
        joins.append([sorted(left), sorted(right), actual])
    roots = []
    for s in PAIRS:
        for c in sorted(U-s):
            table = []
            for a in range(4):
                actual = {x for x, y, w in product(s | {c}, (s | {D})-{a}, s)
                          if len({x, y, w}) == 3}
                assert actual == ({c} if a == D else s | {c})
                table.append(sorted(actual))
            roots.append(dict(palette=sorted(s), bridge_color=c, messages=table))
    # Forgetting the common z color would miss the collision at D.
    table = roots[0]['messages']
    assert table[D] == [2] and set().union(*map(set, table)) == {0, 1, 2}
    return dict(bridge_set_queries=len(joins), bridge_sha256=sha256(json.dumps(joins).encode()).hexdigest(),
                root_queries=4*len(roots), roots=roots,
                negative_control=dict(left=table, right=table, actual_forbidden=[D],
                                      unconditioned_marginals_forbidden=[]))


def templates(saved):
    pool = [] if saved is None else saved['subdivisions']
    pool_edges = [{tuple(sorted(e)) for p in w['paths'] for e in zip(p, p[1:])} for w in pool]
    records, cover, total = [], sha256(), 0
    for index, form in enumerate(forms()):
        _, bans, _ = skeleton(form)
        options = triangle.attachment_options(bans)
        first = [opts[0] for opts in options]
        representative = make_graph(form, first)
        semantics = criticality(representative)
        interior = set(tree.edges(representative.subgraph([v for v in representative if v >= Z])))
        bcolors = {v: sorted(Q[b] for b in representative[v] if b < 5)
                   for v in representative if v >= Z}
        n = 0
        for choices in product(*options):
            graph = make_graph(form, choices)
            assert graph.degree(Z) == 5 and all(graph.degree(v) == 4 for v in graph if v > Z)
            assert set(graph) == set(representative)
            assert set(tree.edges(graph.subgraph([v for v in graph if v >= Z]))) == interior
            assert all(sorted(Q[b] for b in graph[v] if b < 5) == cs for v, cs in bcolors.items())
            apex = max(graph)+1
            graph.add_edges_from((apex, b) for b in range(5))
            es = set(tree.edges(graph))
            wi = next((i for i, wes in enumerate(pool_edges) if wes <= es), None)
            if wi is None:
                assert saved is None, ('missing subdivision', index, choices)
                witness = kuratowski_certificate(graph)
                wi = len(pool)
                pool.append(witness)
                pool_edges.append(tree.validate_subdivision(graph, witness))
            tree.validate_subdivision(graph, pool[wi])
            cover.update(json.dumps([index, choices, tree.edges(graph), wi]).encode())
            n += 1
        records.append(dict(form=form, lifts=n, representative_choices=first, **semantics))
        total += n
    return records, pool, total, cover.hexdigest()


def long_controls(records, pool):
    controls = []
    # One source for each ordered palette pair; both endpoint and interior loops.
    for s, t in product(PAIRS, repeat=2):
        row = next(r for r in records if r['form']['left'] == sorted(s)
                   and r['form']['right'] == sorted(t) and len(r['form']['word']) >= 3)
        for i in (0, 1):
            short = row['form']
            word = short['word']
            c = next(c for c in range(4) if c != word[i])
            long = dict(short, word=word[:i]+[word[i], c]+word[i:])
            _, bans, source_path = skeleton(long)
            choices = [opts[0] for opts in triangle.attachment_options(bans)]
            source = make_graph(long, choices)
            semantics = criticality(source)
            _, _, target_path = skeleton(short)
            retained = source_path[:i+1]+source_path[i+3:]
            mapping = dict(zip(retained, target_path)) | {v: v for v in range(12)}
            # Core labels 6 and 9 are already identical on both sides.
            branches = {v: [old] for old, v in mapping.items()}
            branches[target_path[i]].extend(source_path[i+1:i+3])
            new_choices = []
            old_leaf, new_leaf = max(skeleton(long)[0])+1, max(skeleton(short)[0])+1
            for v, color, bs in choices:
                if v in mapping:
                    new_choices.append((mapping[v], color, bs))
                    if color == D:
                        branches[new_leaf] = [old_leaf]
                        new_leaf += 1
                if color == D:
                    old_leaf += 1
            target = make_graph(short, new_choices)
            criticality(target)
            cert = tree.validate_minor(source, target, branches)
            augmented = target.copy()
            augmented.add_edges_from((max(target)+1, b) for b in range(5))
            es = set(tree.edges(augmented))
            witness = next(w for w in pool if {tuple(sorted(e)) for p in w['paths']
                                              for e in zip(p, p[1:])} <= es)
            controls.append(dict(form=long, choices=choices, source_edges=tree.edges(source),
                                 **semantics, target_form=short, target_choices=new_choices,
                                 minor=cert, source_obstruction=tree.topology_on_source(source, target, branches, witness)))
    return controls


def build(saved):
    records, pool, lifts, fingerprint = templates(saved)
    controls = long_controls(records, pool)
    names = ('c5_degree5_bridge_triangles', 'c5_degree5_triangle_components',
             'c5_degree5_tree_components', 'c5_k4_blocks', 'c5_odd_join_cores',
             'c5_disk_deletions', 'c5_cell_enumerator', 'local_closure', 'boundary_relations')
    return dict(schema=1, scope='Direct private ports on separate triangles; arbitrary bridge path; no general two-port exclusion.',
                source_sha256={f'scripts/{name}.py': tree.digest(ROOT/'scripts'/f'{name}.py') for name in names},
                networkx_version=nx.__version__, local=local_controls(), templates=records,
                subdivisions=pool, ordered_lift_sha256=fingerprint, long_controls=controls,
                summary=dict(templates=len(records), lifts=lifts, subdivisions=len(pool),
                             long_sources=len(controls), disk=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build(json.loads(OUT.read_text()) if args.check else None)
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
