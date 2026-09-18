#!/usr/bin/env python3
"""K4 residual lists and explicit K5 minors, without a planarity oracle.

The arbitrary-branch exclusion and degree-four synthesis are paper proofs.
This certificate checks local algebra, all normalized lifts, and named branches.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_k4_blocks/observations.json'
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)
CYCLE = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
CLIQUE = tuple(range(5, 9))
TRIPLES = [U-{c} for c in sorted(U)]


def edge(u, v):
    return tuple(sorted((u, v)))


def coloring(graph, fixed):
    """Independent backtracking on the complete concrete graph."""
    colors = dict(fixed)
    if any(u in colors and v in colors and colors[u] == colors[v]
           for u, v in graph.edges()):
        return None

    def visit():
        if len(colors) == len(graph):
            return dict(colors)
        choices = {v: U-{colors[u] for u in graph[v] if u in colors}
                   for v in graph if v not in colors}
        v = min(choices, key=lambda x: (len(choices[x]), x))
        for c in sorted(choices[v]):
            colors[v] = c
            result = visit()
            if result is not None:
                return result
            del colors[v]
        return None

    return visit()


def local_controls():
    unrooted, rooted = [], []
    for lists in product(TRIPLES, repeat=4):
        actual = any(len(set(cs)) == 4 for cs in product(*lists))
        assert actual == (len(set(lists)) != 1)
        unrooted.append(dict(lists=list(map(sorted, lists)), colorable=actual))
    for lists in product(TRIPLES, repeat=3):
        actual = {r for r in U if any(len({r, *cs}) == 4 for cs in product(*lists))}
        expected = U-lists[0] if len(set(lists)) == 1 else U
        assert actual == expected
        rooted.append(dict(lists=list(map(sorted, lists)), available=sorted(actual)))
    return dict(unrooted=unrooted, rooted=rooted)


def base():
    graph = nx.Graph()
    graph.add_edges_from(sorted(CYCLE))
    graph.add_edges_from(combinations(CLIQUE, 2))
    return graph


def spoke(graph, v, c, b=None):
    if b is None:
        b = Q.index(c)
    assert Q[b] == c
    graph.add_edge(v, b)


def d_leaf(graph, parent, contacts=None):
    v = max(graph)+1
    graph.add_edge(parent, v)
    for c in range(3):
        spoke(graph, v, c, None if contacts is None else contacts[c])
    return v


def even_path_forcer(graph, parent, c, length):
    assert c != 3 and length >= 2 and length % 2 == 0
    path = list(range(max(graph)+1, max(graph)+1+length))
    graph.add_edges_from(zip([parent]+path, path))
    for v in path[:-1]:
        for bcolor in sorted(U-{3, c}):
            spoke(graph, v, bcolor)
    for bcolor in range(3):
        spoke(graph, path[-1], bcolor)


def clique_forcer(graph, parent, c):
    vertices = list(range(max(graph)+1, max(graph)+5))
    graph.add_edges_from(combinations(vertices, 2))
    graph.add_edge(parent, vertices[0])
    for v in vertices[1:]:
        if c == 3:
            d_leaf(graph, v)
        else:
            spoke(graph, v, c)


def verify(graph, name, forbidden):
    fixed = dict(enumerate(Q))
    inner = set(graph)-set(range(5))
    assert all(graph.degree(v) == 4 for v in inner)
    assert nx.is_connected(graph.subgraph(inner))
    assert set(CLIQUE) in list(nx.biconnected_components(graph.subgraph(inner)))
    for v in inner:
        cs = [Q[b] for b in graph[v] if b < 5]
        assert len(cs) == len(set(cs))
    assert coloring(graph, fixed) is None
    deletion_witnesses = []
    for u, v in sorted(edge(*e) for e in graph.edges() if edge(*e) not in CYCLE):
        relaxed = graph.copy()
        relaxed.remove_edge(u, v)
        witness = coloring(relaxed, fixed)
        assert witness is not None
        deletion_witnesses.append(dict(edge=[u, v], coloring=[witness[x] for x in sorted(graph)]))

    # A concrete path from each outside neighbor to its first boundary contact.
    # Root components in H-K4 are disjoint because K4 is a block.
    paths, bridge_interfaces = [], []
    outside = graph.subgraph(inner-set(CLIQUE))
    used = set()
    for v in CLIQUE:
        neighbor, = set(graph[v])-set(CLIQUE)
        if neighbor < 5:
            assert Q[neighbor] == forbidden
            paths.append([v, neighbor])
            continue
        component = set(nx.node_connected_component(outside, neighbor))
        assert not (component & used)
        used |= component
        side = graph.subgraph(component | set(range(5))).copy()
        contacts = sorted((u, b) for u in component for b in graph[u] if b < 5)
        assert contacts
        available = [c for c in sorted(U)
                     if coloring(side, {**fixed, neighbor: c}) is not None]
        assert available == [forbidden]
        retained = graph.subgraph(set(graph)-component).copy()
        opposite = [c for c in sorted(U)
                    if coloring(retained, {**fixed, v: c}) is not None]
        assert opposite == available
        u, b = contacts[0]
        path = [v]+nx.shortest_path(outside.subgraph(component), neighbor, u)+[b]
        paths.append(path)
        bridge_interfaces.append(dict(edge=[v, neighbor], available=available,
                                      opposite_available=opposite, component=sorted(component)))

    # First keep all five boundary vertices distinct, and contract only paths.
    branches = [[b] for b in range(5)]+[path[:-1] for path in paths]
    flat = [v for bs in branches for v in bs]
    assert len(flat) == len(set(flat))
    assert all(nx.is_connected(graph.subgraph(bs)) for bs in branches)
    target = sorted(CYCLE | set(combinations(CLIQUE, 2))
                    | {edge(v, path[-1]) for v, path in zip(CLIQUE, paths)})
    contacts = []
    for u, v in target:
        source = sorted(edge(a, b) for a in branches[u] for b in branches[v]
                        if graph.has_edge(a, b))
        assert source
        contacts.append(dict(target=[u, v], source=list(source[0])))

    # Independent K5 branch-set certificate in the ORIGINAL graph. The hub
    # merges boundary vertices only at this final nonplanarity step.
    hub = sorted(set(range(5)) | {x for p in paths for x in p[1:-1]})
    k5 = [hub]+[[v] for v in CLIQUE]
    assert len(set(x for bs in k5 for x in bs)) == sum(map(len, k5))
    assert all(nx.is_connected(graph.subgraph(bs)) for bs in k5)
    k5_edges = []
    for i, j in combinations(range(5), 2):
        witnesses = sorted(edge(a, b) for a in k5[i] for b in k5[j] if graph.has_edge(a, b))
        assert witnesses
        k5_edges.append(dict(target=[i, j], source=list(witnesses[0])))
    return dict(name=name, forbidden=forbidden, vertices=sorted(graph),
                edges=sorted(edge(*e) for e in graph.edges()),
                deletion_witnesses=deletion_witnesses, bridge_interfaces=bridge_interfaces,
                paths=paths, boundary_fixed_minor=dict(branch_sets=branches, edges=contacts),
                k5_minor=dict(branch_sets=k5, edges=k5_edges))


def build():
    local = local_controls()
    normalized = []
    for c in range(4):
        options = ([(b,) for b in range(5) if Q[b] == c] if c != 3 else
                   list(product(*[[b for b in range(5) if Q[b] == s] for s in range(3)])))
        for i, attachments in enumerate(product(options, repeat=4)):
            graph = base()
            for v, contacts in zip(CLIQUE, attachments):
                if c == 3:
                    d_leaf(graph, v, contacts)
                else:
                    spoke(graph, v, c, contacts[0])
            normalized.append(verify(graph, f'normalized_{c}_{i}', c))
    named = []
    for c in range(4):
        graph = base()
        for v in CLIQUE:
            clique_forcer(graph, v, c)
        named.append(verify(graph, f'four_k4_branches_{c}', c))
        if c != 3:
            graph = base()
            for v, length in zip(CLIQUE, (2, 4, 6, 8)):
                even_path_forcer(graph, v, c, length)
            named.append(verify(graph, f'four_even_paths_{c}', c))
            graph = base()
            spoke(graph, CLIQUE[0], c)
            even_path_forcer(graph, CLIQUE[1], c, 2)
            even_path_forcer(graph, CLIQUE[2], c, 4)
            clique_forcer(graph, CLIQUE[3], c)
            named.append(verify(graph, f'mixed_spoke_path_k4_{c}', c))
    assert len(normalized) == 289 and len(named) == 10
    return dict(schema=1, fixed_pattern=Q,
                scope='Local exact lists and concrete minors; arbitrary branches and degree-four synthesis remain paper proofs.',
                source_sha256={str(Path(__file__).relative_to(ROOT)): sha256(Path(__file__).read_bytes()).hexdigest()},
                local=local, normalized=normalized, named=named)


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
    print(json.dumps(dict(unrooted=len(result['local']['unrooted']),
                          uncolorable=sum(not r['colorable'] for r in result['local']['unrooted']),
                          rooted_sizes=dict(Counter(len(r['available']) for r in result['local']['rooted'])),
                          normalized=len(result['normalized']), named=len(result['named']),
                          checked_minors=len(result['normalized'])+len(result['named'])), indent=2))


if __name__ == '__main__':
    main()
