#!/usr/bin/env python3
"""Eleven-state recursion and sequential odd-cycle minors: finite controls only.

Unbounded cluster coverage and disk exclusion are paper arguments. No planarity
search, boundary identification, or assertion of full-relation preservation.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from c5_disk_deletions import sha
from c5_odd_cycle_roots import root_available
from c5_tree_cores import Q
from c5_triangle_tree_palettes import (
    U, PAIRS, edge, list_coloring, criticality, normalized_graph, make_core,
    pruning_control,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_multi_odd_cycles/observations.json'
STATES = PAIRS + [frozenset(p) for p in combinations(U, 3)] + [U]


def local_controls():
    rows = []
    for length in (3, 5):
        counts, witnesses = Counter(), {}
        digest = hashlib.sha256()
        for lists in product(STATES, repeat=length-1):
            actual = root_available(lists)
            direct = {r for colors in product(*lists)
                      if all(a != b for a, b in zip(colors, colors[1:]))
                      for r in U if r != colors[0] and r != colors[-1]}
            assert actual == direct and frozenset(actual) in STATES
            constant = len(lists[0]) == 2 and all(p == lists[0] for p in lists)
            assert (len(actual) == 2) == constant
            if constant:
                assert actual == U-lists[0]
            if length == 3:
                assert len(actual) != 3
            key = ''.join(map(str, sorted(actual)))
            counts[len(actual)] += 1
            witnesses.setdefault(key, list(map(sorted, lists)))
            digest.update((json.dumps([list(map(sorted, lists)), sorted(actual)])+'\n').encode())
        rows.append(dict(length=length, inputs=11**(length-1),
                         counts={str(k): v for k, v in sorted(counts.items())},
                         witnesses=witnesses, sha256=digest.hexdigest()))
    joins = []
    for a, b in product(STATES, repeat=2):
        rejected = not (a & b)
        assert rejected == (len(a) == len(b) == 2 and a == U-b)
        joins.append(dict(left=sorted(a), right=sorted(b), rejected=rejected))
    return dict(rooted=rows, joins=joins)


def core(tree, lengths, base):
    assert nx.is_tree(tree)
    distances = nx.single_source_shortest_path_length(tree, 0)
    palettes = {t: base if distances[t] % 2 == 0 else U-base for t in tree}
    shared = {edge(t, s): i for i, (t, s) in enumerate(sorted(tree.edges()))}
    residual = [U for _ in shared]
    cycles, slots = {}, {}
    for t in sorted(tree):
        length = lengths[t]
        assert length >= 3 and length % 2 and tree.degree(t) <= length
        cycle = [None]*length
        slots[t] = {}
        for i, s in enumerate(sorted(tree[t])):
            slot = i*length//tree.degree(t)
            slots[t][s] = slot
            cycle[slot] = shared[edge(t, s)]
        for i, v in enumerate(cycle):
            if v is None:
                cycle[i] = len(residual)
                residual.append(palettes[t])
        cycles[t] = cycle
    inner = sorted({edge(c[i], c[(i+1) % len(c)])
                    for c in cycles.values() for i in range(len(c))})
    return palettes, cycles, residual, inner, slots


def message_check(tree, cycles, residual, inner):
    @lru_cache(None)
    def message(t, s):
        root, = set(cycles[t]) & set(cycles[s])
        i = cycles[t].index(root)
        path = cycles[t][i+1:] + cycles[t][:i]
        lists = []
        for v in path:
            children = [x for x in tree[t] if x != s and v in cycles[x]]
            assert len(children) <= 1
            lists.append(message(children[0], t) if children else residual[v])
        return frozenset(root_available(lists))

    rows = []
    for t in sorted(tree):
        for s in sorted(tree[t]):
            cut = tree.copy()
            cut.remove_edge(t, s)
            side = nx.node_connected_component(cut, t)
            vertices = sorted({v for x in side for v in cycles[x]})
            es = [e for e in inner if set(e) <= set(vertices)]
            root, = set(cycles[t]) & set(cycles[s])
            direct = {c for c in U if list_coloring(vertices, es, residual, {root: c}) is not None}
            assert direct == message(t, s)
            rows.append(dict(side=t, other=s, root=root, available=sorted(direct)))
    return rows


def nonpalette_controls():
    # Both long sides return a triple, so their common root admits three colors.
    tree = nx.path_graph(2)
    _, cycles, residual, inner, _ = core(tree, {0: 5, 1: 5}, PAIRS[0])
    for t in tree:
        for v, p in zip(cycles[t][1:], ({0, 1}, {0, 1}, {0, 2}, {0, 2})):
            residual[v] = frozenset(p)
    direct = list_coloring(range(len(residual)), inner, residual)
    roots = message_check(tree, cycles, residual, inner)
    assert direct is not None and all(r['available'] == [1, 2, 3] for r in roots)
    pair = dict(cycles=cycles, lists=list(map(sorted, residual)), edges=inner,
                directed_interfaces=roots, coloring=direct)
    # A downstream triple is actually consumed by another long cycle. Verify
    # the resulting upstream message against its entire concrete side.
    chain = nx.path_graph(3)
    _, cycles, residual, inner, _ = core(chain, {0: 5, 1: 5, 2: 5}, PAIRS[0])
    for v, p in zip(cycles[2][1:], ({0, 1}, {0, 1}, {0, 2}, {0, 2})):
        residual[v] = frozenset(p)
    roots = message_check(chain, cycles, residual, inner)
    assert next(r for r in roots if (r['side'], r['other']) == (2, 1))['available'] == [1, 2, 3]
    assert len(next(r for r in roots if (r['side'], r['other']) == (1, 0))['available']) >= 3
    direct = list_coloring(range(len(residual)), inner, residual)
    assert direct is not None
    return [pair, dict(cycles=cycles, lists=list(map(sorted, residual)), edges=inner,
                       directed_interfaces=roots, coloring=direct)]


def verify_minor(n, edges, target_edges, branches):
    source = nx.Graph()
    source.add_nodes_from(range(n))
    source.add_edges_from(edges)
    flat = [v for bs in branches for v in bs]
    assert len(flat) == len(set(flat)) and set(flat) <= set(range(n))
    assert all(branches[b] == [b] for b in range(5))
    assert all(bs and nx.is_connected(source.subgraph(bs)) for bs in branches)
    witnesses = []
    for u, v in target_edges:
        contacts = sorted(edge(a, b) for a in branches[u] for b in branches[v]
                          if source.has_edge(a, b))
        assert contacts
        witnesses.append(dict(target_edge=[u, v], source_edge=contacts[0]))
    return dict(deleted_vertices=sorted(set(range(n))-set(flat)), edge_witnesses=witnesses)


def check_state(n, edges, cycles, palettes):
    critical = criticality(n, edges)
    graph = nx.Graph(edges)
    assert nx.is_connected(graph.subgraph(range(5, n)))
    for v in range(5, n):
        spoke_colors = [Q[b] for b in graph[v] if b < 5]
        assert len(spoke_colors) == len(set(spoke_colors))
    tree = nx.Graph()
    tree.add_nodes_from(cycles)
    for t, s in combinations(sorted(cycles), 2):
        overlap = set(cycles[t]) & set(cycles[s])
        assert len(overlap) <= 1
        if overlap:
            tree.add_edge(t, s)
            assert palettes[t] == U-palettes[s]
    assert nx.is_tree(tree)
    residual = [U]*n
    for v in {v for c in cycles.values() for v in c}:
        owners = [t for t in cycles if v in cycles[t]]
        residual[v] = U if len(owners) == 2 else palettes[owners[0]]
    inner = sorted({edge(c[i], c[(i+1) % len(c)])
                    for c in cycles.values() for i in range(len(c))})
    roots = message_check(tree, cycles, residual, inner)
    assert all(set(r['available']) == U-palettes[r['side']] for r in roots)
    return tree, dict(vertices=n, edges=edges, cycles=cycles,
                      critical_edges=critical, directed_interfaces=roots)


def shorten(n, edges, cycles, palettes, tree, t, keep_slots):
    ring = cycles[t]
    assert len(ring) >= 5 and len(set(keep_slots)) == 3
    keep_slots = sorted(keep_slots)
    selected = {ring[i] for i in keep_slots}
    kept_tree = {t}
    for s in tree[t]:
        if selected & set(cycles[s]):
            cut = tree.copy()
            cut.remove_edge(t, s)
            kept_tree |= nx.node_connected_component(cut, s)
    kept_core = selected | {v for s in kept_tree-{t} for v in cycles[s]}
    all_core = {v for c in cycles.values() for v in c}
    graph = nx.Graph(edges)
    # The normalized graph has only singleton D-forcers outside its cycles.
    leaves = {v for v in range(5, n) if v not in all_core and set(graph[v]) & kept_core}
    keep_vertices = set(range(5)) | kept_core | leaves
    branches = {v: {v} for v in keep_vertices}
    for j, start in enumerate(keep_slots):
        stop = keep_slots[(j+1) % 3]
        i = (start+1) % len(ring)
        while i != stop:
            branches[ring[start]].add(ring[i])
            i = (i+1) % len(ring)
    surviving = sorted(branches)
    relabel = {v: i for i, v in enumerate(surviving)}
    target_edges = {edge(relabel[u], relabel[v]) for u, v in edges
                    if u in keep_vertices and v in keep_vertices}
    target_edges |= {edge(relabel[ring[keep_slots[i]]], relabel[ring[keep_slots[(i+1) % 3]]])
                     for i in range(3)}
    target_edges = sorted(target_edges)
    target_branches = [sorted(branches[v]) for v in surviving]
    minor = verify_minor(n, edges, target_edges, target_branches)
    target_cycles = {s: [relabel[v] for v in (sorted(selected, key=ring.index) if s == t else cycles[s])]
                     for s in sorted(kept_tree)}
    target_palettes = {s: palettes[s] for s in kept_tree}
    return (len(surviving), target_edges, target_cycles, target_palettes,
            dict(shortened_block=t, retained_slots=keep_slots,
                 removed_blocks=sorted(set(cycles)-kept_tree),
                 target_branch_sets=target_branches, **minor))


def sequential_control(name, tree, lengths, base, order, protected_path):
    palettes, cycles, residual, inner, slots = core(tree, lengths, base)
    n, edges, _ = normalized_graph(residual, inner)
    cycles = {t: [v+5 for v in c] for t, c in cycles.items()}
    tree, source = check_state(n, edges, cycles, palettes)
    original_n, original_edges = n, edges
    composed = [[v] for v in range(n)]
    steps = []
    for t in order:
        if t not in cycles:
            continue
        assert len(cycles[t]) > 3
        # Preserve the whole marked path; its endpoints can be the two long
        # cycles. Each cycle meets at most two marked path edges.
        required = set()
        for a, b in zip(protected_path, protected_path[1:]):
            if t in (a, b):
                other = b if t == a else a
                required |= set(cycles[t]) & set(cycles[other])
        if t not in protected_path:
            other = nx.shortest_path(tree, t, protected_path[0])[1]
            required |= set(cycles[t]) & set(cycles[other])
        keep = {cycles[t].index(v) for v in required}
        for i in list(range(0, len(cycles[t]), 2)) + list(range(len(cycles[t]))):
            if len(keep) == 3:
                break
            keep.add(i)
        n, edges, cycles, palettes, minor = shorten(n, edges, cycles, palettes, tree, t, keep)
        assert set(protected_path) <= set(cycles)
        tree, state = check_state(n, edges, cycles, palettes)
        composed = [sorted(v for old in bs for v in composed[old])
                    for bs in minor['target_branch_sets']]
        verify_minor(original_n, original_edges, edges, composed)
        steps.append(dict(**minor, target=state))
    assert all(len(c) == 3 for c in cycles.values()) and len(cycles) >= 2
    labels = {t: i for i, t in enumerate(sorted(tree))}
    reduced_tree = nx.relabel_nodes(tree, labels)
    final_base = palettes[min(tree)]
    canonical_palettes, _, _, _, ls, es = make_core(reduced_tree, final_base)
    cn, canonical, _ = normalized_graph(ls, es)
    assert cn == n

    def marked(es):
        g = nx.Graph(es)
        nx.set_node_attributes(g, {v: v if v < 5 else -1 for v in g}, 'boundary')
        return g

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        marked(canonical), marked(edges), node_match=lambda a, b: a['boundary'] == b['boundary'])
    assert matcher.is_isomorphic()
    mapping = matcher.mapping
    assert all(mapping[b] == b for b in range(5))
    assert {edge(mapping[u], mapping[v]) for u, v in canonical} == set(edges)
    center = next(t for t in sorted(reduced_tree) if 3 not in canonical_palettes[t])
    pruning = pruning_control(reduced_tree, final_base, center)
    assert pruning['source_edges'] == canonical
    composed_minor = verify_minor(original_n, original_edges, edges, composed)
    small_branches = [sorted(v for old in bs for v in composed[mapping[old]])
                      for bs in pruning['target_branch_sets']]
    small_minor = verify_minor(original_n, original_edges, pruning['target_edges'], small_branches)
    return dict(name=name, lengths=lengths, attachment_slots=slots, palette=sorted(base),
                order=order, protected_path=protected_path, source=source, steps=steps,
                composed_branch_sets=composed, composed_minor=composed_minor,
                small_target_branch_sets=small_branches, small_target_minor=small_minor,
                canonical_vertex_map=[mapping[v] for v in range(n)], triangle_pruning=pruning)


def build():
    cases = [
        ('adjacent_5_5', nx.path_graph(2), {0: 5, 1: 5}, [0, 1]),
        ('triangle_between', nx.path_graph(3), {0: 5, 1: 3, 2: 7}, [0, 1, 2]),
        ('two_with_arms', nx.Graph([(0, 1), (0, 2), (0, 3), (1, 4)]),
         {0: 7, 1: 9, 2: 3, 3: 3, 4: 3}, [0, 1]),
        ('three_long_chain', nx.path_graph(3), {0: 5, 1: 7, 2: 5}, [0, 1, 2]),
        ('delete_long_branch', nx.star_graph(5),
         {0: 5, 1: 5, 2: 7, 3: 3, 4: 3, 5: 3}, [0, 1]),
    ]
    controls = []
    for name, tree, lengths, path in cases:
        order = [t for t in sorted(tree) if lengths[t] > 3]
        for base in PAIRS:
            for sequence in (order, list(reversed(order))):
                controls.append(sequential_control(name, tree, lengths, base, sequence, path))
    assert any(any(len(s['removed_blocks']) > 0 for s in c['steps']) for c in controls)
    assert any(len(c['steps']) >= 3 for c in controls)
    dependencies = ['c5_odd_cycle_roots', 'c5_triangle_tree_palettes', 'c5_pentagon_branches']
    sources = {f'scripts/{Path(__file__).stem}.py'}
    for name in dependencies:
        prior = json.loads((ROOT/f'artifacts/{name}/observations.json').read_text())
        for path, digest in prior['source_sha256'].items():
            assert sha(ROOT/path) == digest, path
            sources.add(path)
        for path, digest in prior.get('dependency_sha256', {}).items():
            assert sha(ROOT/path) == digest, path
    return dict(schema=1, fixed_pattern=Q,
                scope='Eleven-state algebra and named sequential minors; arbitrary odd-cycle trees are a paper proof, not Lean.',
                local=local_controls(), nonpalette_controls=nonpalette_controls(),
                sequential_controls=controls,
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
    print(json.dumps(dict(rooted=[{k: r[k] for k in ('length', 'inputs', 'counts')}
                                 for r in result['local']['rooted']], joins=len(result['local']['joins']),
                          nonpalette_controls=len(result['nonpalette_controls']),
                          sequential_controls=len(result['sequential_controls']),
                          shortening_steps=sum(len(c['steps']) for c in result['sequential_controls'])), indent=2))


if __name__ == '__main__':
    main()
