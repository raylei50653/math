#!/usr/bin/env python3
"""Triangle-tree palette induction and boundary-fixed pruning controls.

The unbounded induction and minor coverage are paper proofs. This checker tests
the local algebra and named structural controls; it does not search larger disks.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from c5_disk_deletions import CYCLE, sha
from c5_tree_cores import Q, lifted_edges, options
from c5_triangle_forks import witness_edges
from c5_two_triangle_blocks import templates as pair_templates
from c5_shared_triangle_blocks import templates as triple_templates
from c5_four_triangle_star import templates as star_templates

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_triangle_tree_palettes/observations.json'
U = frozenset(range(4))
PAIRS = [frozenset(p) for p in combinations(range(4), 2)]


def edge(u, v):
    return tuple(sorted((u, v)))


def local_controls():
    states = PAIRS + [U]
    apex, triangles, replacements = [], [], []
    for a, b in product(states, repeat=2):
        available = {r for r in U if any(len({r, x, y}) == 3
                                         for x, y in product(a, b))}
        expected = U-a if a == b and len(a) == 2 else U
        assert available == expected
        apex.append(dict(left=sorted(a), right=sorted(b), available=sorted(available)))
    for a, b, c in product(states, repeat=3):
        actual = any(len(set(cs)) == 3 for cs in product(a, b, c))
        assert actual == (not (a == b == c and len(a) == 2))
        triangles.append(dict(lists=list(map(sorted, (a, b, c))), colorable=actual))
    for p in PAIRS:
        if 3 in p:
            continue
        for mask in range(16):
            k = {c for c in U if mask & (1 << c)}
            assert k & (U-p) == k-p
            replacements.append(dict(forbidden=sorted(p), retained_mask=mask,
                                     available=sorted(k-p)))
        # K can take every colour of P. Deleting either new spoke frees that colour.
        for c in p:
            assert p-(p-{c}) == {c}
    return dict(apex=apex, triangles=triangles, replacements=replacements)


def list_coloring(vertices, edges, lists, fixed=None):
    """Independent exact backtracking; no triangle or message semantics."""
    neighbors = {v: set() for v in vertices}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    colors = dict(fixed or {})
    assert all(c in lists[v] for v, c in colors.items())
    if any(u in colors and v in colors and colors[u] == colors[v] for u, v in edges):
        return None

    def visit():
        if len(colors) == len(vertices):
            return dict(colors)
        choices = {v: set(lists[v])-{colors[u] for u in neighbors[v] if u in colors}
                   for v in vertices if v not in colors}
        v = min(choices, key=lambda x: (len(choices[x]), x))
        for c in sorted(choices[v]):
            colors[v] = c
            result = visit()
            if result is not None:
                return result
            del colors[v]
        return None

    return visit()


def criticality(n, edges):
    vertices = list(range(n))
    lists = [U]*n
    fixed = dict(enumerate(Q))
    assert all(sum(v in e for e in edges) == 4 for v in range(5, n))
    assert list_coloring(vertices, edges, lists, fixed) is None
    deleted = sorted(set(edges)-CYCLE)
    for e in deleted:
        assert list_coloring(vertices, [f for f in edges if f != e], lists, fixed) is not None
    return deleted


def make_core(tree, base):
    assert nx.is_tree(tree) and max(dict(tree.degree()).values()) <= 3
    distances = nx.single_source_shortest_path_length(tree, 0)
    palettes = {t: base if distances[t] % 2 == 0 else U-base for t in tree}
    shared = {edge(u, v): i for i, (u, v) in enumerate(sorted(tree.edges()))}
    lists = [U for _ in shared]
    triangles, owners = {}, {}
    for t in sorted(tree):
        vertices = [shared[edge(t, s)] for s in sorted(tree[t])]
        while len(vertices) < 3:
            v = len(lists)
            vertices.append(v)
            lists.append(palettes[t])
            owners[v] = t
        triangles[t] = vertices
    inner = sorted({edge(u, v) for tri in triangles.values() for u, v in combinations(tri, 2)})
    return palettes, shared, triangles, owners, lists, inner


def normalized_graph(residual, inner):
    lists = [p | {3} for p in residual]
    edges = list(inner)
    leaves = {}
    for v, p in enumerate(residual):
        if 3 not in p:
            leaves[v] = len(lists)
            edges.append((v, len(lists)))
            lists.append(frozenset({3}))
    ns = tuple(options(sorted(set(range(3))-p))[0] for p in lists)
    return len(lists)+5, lifted_edges(edges, ns), leaves


def rooted_controls(tree, shared, triangles, lists, inner, palettes):
    rows = []
    for t, s in sorted((t, s) for t in tree for s in tree[t]):
        cut = tree.copy()
        cut.remove_edge(t, s)
        side = nx.node_connected_component(cut, t)
        vertices = sorted({v for x in side for v in triangles[x]})
        root = shared[edge(t, s)]
        edges = [e for e in inner if set(e) <= set(vertices)]
        available = [c for c in range(4)
                     if list_coloring(vertices, edges, lists, {root: c}) is not None]
        assert set(available) == U-palettes[t]
        rows.append(dict(side_triangle=t, other_triangle=s, root=root+5, available=available))
    return rows


def existing_target(n, edges, count):
    """Match a saved small template, then verify its actual Kuratowski model."""
    name, templates = {2: ('c5_two_triangle_blocks', pair_templates),
                       3: ('c5_shared_triangle_blocks', triple_templates),
                       4: ('c5_four_triangle_star', star_templates)}[count]
    prior = json.loads((ROOT / f'artifacts/{name}/observations.json').read_text())

    def graph(es):
        g = nx.Graph(es)
        nx.set_node_attributes(g, {v: v if v < 5 else -1 for v in g}, 'boundary')
        return g

    target = graph(edges)
    for kind, metadata, lists, inner in templates():
        if count == 2 and kind != 'shared':
            continue
        if len(lists)+5 != n:
            continue
        old = lifted_edges(inner, tuple(options(sorted(set(range(3))-p))[0] for p in lists))
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            graph(old), target, node_match=lambda a, b: a['boundary'] == b['boundary'])
        if not matcher.is_isomorphic():
            continue
        mapping = matcher.mapping
        assert all(mapping[b] == b for b in range(5))
        assert {edge(mapping[u], mapping[v]) for u, v in old} == set(edges)
        apex = set(old) | {(b, n) for b in range(5)}
        for wi, witness in enumerate(prior['subdivisions']):
            if witness_edges(witness) <= apex:
                full_map = {**mapping, n: n}
                translated = dict(model=witness['model'],
                                  branch_vertices=[full_map[v] for v in witness['branch_vertices']],
                                  paths=[[full_map[v] for v in p] for p in witness['paths']])
                assert witness_edges(translated) <= set(edges) | {(b, n) for b in range(5)}
                return dict(dependency=name, kind=kind, metadata=metadata,
                            template_vertex_map=[mapping[v] for v in range(n)],
                            subdivision_index=wi, target_subdivision=translated)
        raise AssertionError('no saved subdivision covers the matched representative')
    raise AssertionError('minor did not match an existing template')


def pruning_control(tree, base, center):
    palettes, shared, triangles, owners, residual, inner = make_core(tree, base)
    assert 3 not in palettes[center]
    n, edges, leaves = normalized_graph(residual, inner)
    source_critical = criticality(n, edges)
    roots = rooted_controls(tree, shared, triangles, residual, inner, palettes)
    keep = {center, *tree[center]}
    source = nx.Graph(edges)
    branch_sets = {v: {v} for v in range(n)}
    removed, prunings, spokes = set(), [], []
    for t in sorted(keep):
        for s in sorted(set(tree[t])-keep):
            cut = tree.copy()
            cut.remove_edge(t, s)
            side = nx.node_connected_component(cut, s)
            root = shared[edge(t, s)]+5
            core_side = {v for x in side for v in triangles[x]}
            absorbed = {v+5 for v in core_side} - {root}
            absorbed |= {leaf+5 for v, leaf in leaves.items() if v in core_side}
            assert not absorbed & removed
            assert 3 not in palettes[s]
            branch = {root} | absorbed
            assert nx.is_connected(source.subgraph(branch))
            chosen = []
            for c in sorted(palettes[s]):
                contacts = sorted((v, b) for v in absorbed for b in range(5)
                                  if source.has_edge(v, b) and Q[b] == c)
                assert contacts
                v, b = contacts[0]
                chosen.append(dict(color=c, source_edge=edge(v, b), target_edge=edge(root, b)))
                spokes.append(edge(root, b))
            branch_sets[root] = branch
            removed |= absorbed
            prunings.append(dict(root=root, forbidden=sorted(palettes[s]),
                                 removed_triangles=sorted(side), absorbed=sorted(absorbed), contacts=chosen))
    surviving = sorted(set(range(n))-removed)
    relabel = {v: i for i, v in enumerate(surviving)}
    target_edges = sorted({edge(relabel[u], relabel[v]) for u, v in edges
                           if u not in removed and v not in removed}
                          | {edge(relabel[u], relabel[v]) for u, v in spokes})
    target_branches = [sorted(branch_sets[v]) for v in surviving]
    flattened = [v for bs in target_branches for v in bs]
    assert len(flattened) == len(set(flattened)) == n
    assert all(target_branches[b] == [b] for b in range(5))
    for bs in target_branches:
        assert nx.is_connected(source.subgraph(bs))
    for u, v in target_edges:
        assert any(source.has_edge(a, b) for a in target_branches[u] for b in target_branches[v])
    target_critical = criticality(len(surviving), target_edges)
    return dict(tree_edges=sorted(map(list, tree.edges())), base_palette=sorted(base), center=center,
                kept_triangles=sorted(keep), source_vertices=n, source_edges=edges,
                source_critical_edges=source_critical, directed_root_interfaces=roots,
                prunings=prunings, target_edges=target_edges, target_branch_sets=target_branches,
                target_critical_edges=target_critical,
                existing_target=existing_target(len(surviving), target_edges, len(keep)))


def build():
    # Named controls, not a catalogue: both bipartitions and centre degrees 1/2/3.
    trees = [('pair', nx.path_graph(2)), ('triple', nx.path_graph(3)),
             ('four_chain', nx.path_graph(4)), ('four_star', nx.star_graph(3)),
             ('long_path', nx.path_graph(7)),
             ('branched', nx.Graph([(0, 1), (0, 2), (0, 3), (1, 4), (1, 5),
                                    (2, 6), (2, 7), (3, 8), (3, 9)]))]
    controls = []
    for name, tree in trees:
        for base in PAIRS:
            palettes, _, _, _, _, _ = make_core(tree, base)
            # One representative for each non-D centre degree in this assignment.
            centers = {}
            for t in sorted(tree):
                if 3 not in palettes[t]:
                    centers.setdefault(tree.degree(t), t)
            for center in centers.values():
                controls.append(dict(name=name, **pruning_control(tree, base, center)))
    assert {len(r['kept_triangles']) for r in controls} == {2, 3, 4}
    assert any(len(r['prunings']) >= 2 for r in controls)
    dependencies = ['c5_shared_pair_bridge', 'c5_two_triangle_blocks',
                    'c5_shared_triangle_blocks', 'c5_three_triangle_blocks',
                    'c5_four_triangle_chain', 'c5_four_triangle_star']
    sources = {f'scripts/{Path(__file__).stem}.py'}
    for name in dependencies:
        prior = json.loads((ROOT / f'artifacts/{name}/observations.json').read_text())
        for path, digest in prior['source_sha256'].items():
            assert sha(ROOT/path) == digest, path
            sources.add(path)
        for path, digest in prior.get('dependency_sha256', {}).items():
            assert sha(ROOT/path) == digest, path
    return dict(schema=1, fixed_pattern=Q,
                scope='Finite algebra and named minor controls; unbounded coverage is a paper proof.',
                local_controls=local_controls(), structural_controls=controls,
                source_sha256={p: sha(ROOT/p) for p in sorted(sources)},
                dependency_sha256={f'artifacts/{s}/observations.json':
                                   sha(ROOT/f'artifacts/{s}/observations.json') for s in dependencies})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(dict(apex_inputs=len(result['local_controls']['apex']),
                          triangle_inputs=len(result['local_controls']['triangles']),
                          replacement_inputs=len(result['local_controls']['replacements']),
                          structural_controls=len(result['structural_controls']),
                          pruned_branches=sum(len(r['prunings']) for r in result['structural_controls'])), indent=2))


if __name__ == '__main__':
    main()
