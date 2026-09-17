#!/usr/bin/env python3
"""Odd-cycle root interfaces and named boundary-fixed cycle shortening controls.

Unbounded coverage is a paper proof. No new disk catalogue or planarity search.
"""
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path

import networkx as nx

from c5_disk_deletions import sha
from c5_tree_cores import Q
from c5_triangle_tree_palettes import (
    U, PAIRS, edge, list_coloring, criticality, normalized_graph, make_core,
    pruning_control,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_odd_cycle_roots/observations.json'


def root_available(lists):
    """Path transfer with the deleted cycle vertex pinned at both ends."""
    answer = set()
    for root in U:
        possible = {root}
        for allowed in lists:
            possible = {c for c in allowed if possible - {c}}
        if possible - {root}:
            answer.add(root)
    return answer


def interface_controls():
    states = PAIRS + [U]
    rows = []
    for length in (3, 5, 7):
        counts, witnesses, masks = Counter(), {}, set()
        digest = hashlib.sha256()
        for lists in product(states, repeat=length-1):
            available = root_available(lists)
            assert len(available) >= 2
            constant = all(p == lists[0] for p in lists) and len(lists[0]) == 2
            assert (len(available) == 2) == constant
            if constant:
                assert available == U-lists[0]
            # Independent exhaustive color assignments for all C3/C5 inputs.
            if length <= 5:
                direct = {r for colors in product(*lists)
                          if all(a != b for a, b in zip(colors, colors[1:]))
                          for r in U if r != colors[0] and r != colors[-1]}
                assert available == direct
            key = ''.join(map(str, sorted(available)))
            masks.add(key)
            counts[str(len(available))] += 1
            witnesses.setdefault(key, list(map(sorted, lists)))
            digest.update((json.dumps([list(map(sorted, lists)), sorted(available)])+'\n').encode())
        assert len(masks) == (7 if length == 3 else 11)
        rows.append(dict(length=length, counts=dict(sorted(counts.items())),
                         witnesses=dict(sorted(witnesses.items())), sha256=digest.hexdigest()))
    # Complete unrooted C5 test: only the six constant pairs fail.
    rejected = []
    ring = [edge(i, (i+1) % 5) for i in range(5)]
    for lists in product(states, repeat=5):
        coloring = list_coloring(range(5), ring, lists)
        constant = all(p == lists[0] for p in lists) and len(lists[0]) == 2
        assert (coloring is None) == constant
        if coloring is None:
            rejected.append(list(map(sorted, lists)))
    negative = [{0, 1}, {0, 1}, {0, 2}, {0, 2}]
    assert root_available(negative) == {1, 2, 3}
    # In particular this new interface always meets every triangle-side pair.
    assert all(root_available(negative) & p for p in PAIRS)
    return dict(rooted=rows, unrooted_C5_inputs=7**5, unrooted_C5_rejected=rejected,
                negative_control=dict(path_lists=list(map(sorted, negative)), available=[1, 2, 3]))


def mixed_core(tree, length, slots, base):
    """One long root block, all other blocks triangles; fixed named controls."""
    assert nx.is_tree(tree)
    assert len(slots) == tree.degree(0) and len(set(slots)) == len(slots)
    assert all(0 <= v < length for v in slots)
    distances = nx.single_source_shortest_path_length(tree, 0)
    palettes = {t: base if distances[t] % 2 == 0 else U-base for t in tree}
    shared = {edge(t, s): i for i, (t, s) in enumerate(sorted(tree.edges()))}
    residual = [U for _ in shared]
    cycles = {}
    for t in sorted(tree):
        if t == 0:
            cycle = [None]*length
            for s, slot in zip(sorted(tree[t]), slots):
                cycle[slot] = shared[edge(t, s)]
        else:
            cycle = [shared[edge(t, s)] for s in sorted(tree[t])]
            assert len(cycle) <= 3
            cycle += [None]*(3-len(cycle))
        for i, v in enumerate(cycle):
            if v is None:
                cycle[i] = len(residual)
                residual.append(palettes[t])
        cycles[t] = cycle
    inner = sorted({edge(c[i], c[(i+1) % len(c)]) for c in cycles.values() for i in range(len(c))})
    return palettes, shared, cycles, residual, inner


def shortening_control(name, tree, length, slots, keep_slots, base):
    palettes, shared, cycles, residual, inner = mixed_core(tree, length, slots, base)
    n, edges, leaves = normalized_graph(residual, inner)
    critical_edges = criticality(n, edges)
    # Every directed interface is independently checked on its whole concrete side.
    roots = []
    for t in sorted(tree):
        for s in sorted(tree[t]):
            cut = tree.copy()
            cut.remove_edge(t, s)
            side = nx.node_connected_component(cut, t)
            vertices = sorted({v for x in side for v in cycles[x]})
            es = [e for e in inner if set(e) <= set(vertices)]
            r = shared[edge(t, s)]
            available = [c for c in U if list_coloring(vertices, es, residual, {r: c}) is not None]
            assert set(available) == U-palettes[t]
            roots.append(dict(side=t, other=s, root=r+5, available=available))

    keep_slots = sorted(keep_slots)
    assert len(keep_slots) == 3
    ring = cycles[0]
    selected = {ring[i] for i in keep_slots}
    kept_tree = {0}
    for s in tree[0]:
        if shared[edge(0, s)] in selected:
            cut = tree.copy()
            cut.remove_edge(0, s)
            kept_tree |= nx.node_connected_component(cut, s)
    assert len(kept_tree) >= 2
    kept_core = selected | {v for t in kept_tree-{0} for v in cycles[t]}
    kept_vertices = set(range(5)) | {v+5 for v in kept_core}
    kept_vertices |= {leaf+5 for v, leaf in leaves.items() if v in kept_core}
    branches = {v: {v} for v in kept_vertices}
    # Delete every unselected attachment first. Contract only bare cycle arcs.
    for j, start in enumerate(keep_slots):
        stop = keep_slots[(j+1) % 3]
        i = (start+1) % length
        while i != stop:
            branches[ring[start]+5].add(ring[i]+5)
            i = (i+1) % length
    used = set().union(*branches.values())
    deleted = sorted(set(range(n))-used)
    surviving = sorted(branches)
    relabel = {v: i for i, v in enumerate(surviving)}
    target_edges = {edge(relabel[u], relabel[v]) for u, v in edges
                    if u in kept_vertices and v in kept_vertices}
    target_edges |= {edge(relabel[ring[keep_slots[i]]+5], relabel[ring[keep_slots[(i+1) % 3]]+5])
                     for i in range(3)}
    target_edges = sorted(target_edges)
    target_branches = [sorted(branches[v]) for v in surviving]
    source = nx.Graph(edges)
    flat = [v for bs in target_branches for v in bs]
    assert len(flat) == len(set(flat))
    assert all(target_branches[b] == [b] for b in range(5))
    assert all(nx.is_connected(source.subgraph(bs)) for bs in target_branches)
    assert all(any(source.has_edge(a, b) for a in target_branches[u] for b in target_branches[v])
               for u, v in target_edges)
    target_critical = criticality(len(surviving), target_edges)

    # Identify the shortened graph with an existing triangle-tree control, then
    # carry its boundary-fixed pruning and saved small-template subdivision.
    labels = {t: i for i, t in enumerate(sorted(kept_tree))}
    reduced_tree = nx.relabel_nodes(tree.subgraph(kept_tree), labels)
    reduced_palettes, _, _, _, ls, es = make_core(reduced_tree, base)
    cn, canonical, _ = normalized_graph(ls, es)
    assert cn == len(surviving)

    def marked(es):
        g = nx.Graph(es)
        nx.set_node_attributes(g, {v: v if v < 5 else -1 for v in g}, 'boundary')
        return g

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        marked(canonical), marked(target_edges), node_match=lambda a, b: a['boundary'] == b['boundary'])
    assert matcher.is_isomorphic()
    mapping = matcher.mapping
    assert all(mapping[b] == b for b in range(5))
    assert {edge(mapping[u], mapping[v]) for u, v in canonical} == set(target_edges)
    center = next(t for t in sorted(reduced_tree) if 3 not in reduced_palettes[t])
    pruning = pruning_control(reduced_tree, base, center)
    assert pruning['source_edges'] == canonical
    return dict(name=name, length=length, tree_edges=sorted(map(list, tree.edges())),
                attachment_slots=slots, retained_slots=keep_slots, palette=sorted(base),
                source_vertices=n, source_edges=edges, source_critical_edges=critical_edges,
                directed_root_interfaces=roots, deleted_vertices=deleted,
                target_branch_sets=target_branches, target_edges=target_edges,
                target_critical_edges=target_critical, canonical_vertex_map=[mapping[v] for v in range(cn)],
                triangle_tree_pruning=pruning)


def build():
    cases = [
        ('one_triangle', nx.path_graph(2), 5, [0], [0, 1, 3]),
        ('two_spread', nx.star_graph(2), 7, [1, 5], [1, 3, 5]),
        ('all_five_shared', nx.star_graph(5), 5, [0, 1, 2, 3, 4], [0, 2, 4]),
        ('deep_branches', nx.Graph([(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (4, 6)]),
         9, [0, 4, 8], [0, 3, 6]),
        ('long_center_star', nx.star_graph(3), 9, [0, 3, 6], [0, 3, 6]),
    ]
    controls = [shortening_control(name, tree, length, slots, keep, base)
                for name, tree, length, slots, keep in cases for base in PAIRS]
    dependencies = ['c5_triangle_tree_palettes', 'c5_pentagon_branches']
    sources = {f'scripts/{Path(__file__).stem}.py'}
    for name in dependencies:
        prior = json.loads((ROOT/f'artifacts/{name}/observations.json').read_text())
        for path, digest in prior['source_sha256'].items():
            assert sha(ROOT/path) == digest, path
            sources.add(path)
        for path, digest in prior.get('dependency_sha256', {}).items():
            assert sha(ROOT/path) == digest, path
    return dict(schema=1, fixed_pattern=Q,
                scope='One long odd-cycle block plus triangles and bridges; paper coverage, finite controls, no Lean theorem.',
                interfaces=interface_controls(), shortening_controls=controls,
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
    print(json.dumps(dict(rooted=[dict(length=r['length'], counts=r['counts'])
                                  for r in result['interfaces']['rooted']],
                          unrooted_inputs=result['interfaces']['unrooted_C5_inputs'],
                          shortening_controls=len(result['shortening_controls'])), indent=2))


if __name__ == '__main__':
    main()
