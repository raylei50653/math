#!/usr/bin/env python3
"""Two-port tree reduction to five palette walks; saved non-disk subdivisions.

Unbounded coverage is a paper proof. --check never runs a planarity search.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

from c5_k4_blocks import CYCLE, Q, U, coloring
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_tree_components/observations.json'
SECTORS = ROOT / 'artifacts/c5_degree5_sectors/observations.json'
D, Z = 3, 5
ARC = (1, 2, 3, 4)
PAIRS = tuple(frozenset(p) for p in combinations(range(4), 2))


def edges(graph):
    return sorted(tuple(sorted(e)) for e in graph.edges())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def root_bans(lists):
    result = set()
    for a in U:
        possible = set(lists[0]) - {a}
        for pair in lists[1:]:
            possible = {c for c in pair if any(c != d for d in possible)}
        if not (possible - {a}):
            result.add(a)
    return result


def trace(lists, a):
    colors = [a]
    for pair in lists:
        if colors[-1] not in pair:
            return None
        colors.append(next(iter(set(pair) - {colors[-1]})))
    return colors


def motifs():
    for a, b in permutations(range(3), 2):
        yield 'triangle', (D, a, b, D)
        yield 'split', (D, a, D, b, D)
        yield 'nested', (D, a, b, a, D)
    for a, b, c in permutations(range(3)):
        yield 'square', (D, a, b, c, D)
        yield 'lollipop', (D, a, b, c, a, D)


MOTIFS = {walk: name for name, walk in motifs()}


def reduction(walk):
    """Delete a closed subwalk only when at least three colors remain."""
    for i in range(len(walk)-1):
        for j in range(i+1, len(walk)):
            if walk[i] != walk[j]:
                continue
            target = tuple(walk[:i]) + tuple(walk[j:])
            if len(set(target)) >= 3:
                retained = list(range(i)) + list(range(j, len(walk)-1))
                return target, retained, (i, j)
    assert tuple(walk) in MOTIFS, walk
    return None


def local_controls():
    assignment_hash, counts = sha256(), Counter()
    for n in range(1, 6):
        for lists in product(PAIRS, repeat=n):
            bans = root_bans(lists)
            valid = [cs for cs in product(*map(sorted, lists))
                     if all(a != b for a, b in zip(cs, cs[1:]))]
            brute = {a for a in U if not any(cs[0] != a and cs[-1] != a for cs in valid)}
            assert bans == brute
            traced = {a for a in U if (t := trace(lists, a)) is not None and t[-1] == a}
            assert bans == traced
            assert len(bans) <= 1 or len(set(lists)) == 1
            if D in bans:
                assert (bans == {D}) == (len(set(lists)) >= 2)
            counts['pair_assignments'] += 1
            assignment_hash.update(json.dumps([list(map(sorted, lists)), sorted(bans)]).encode())
    reduced_counts, walk_hash = Counter(), sha256()
    def visit(walk):
        if len(walk) >= 3 and walk[-1] == D and len(set(walk)) >= 3:
            current = tuple(walk)
            while step := reduction(current):
                current = step[0]
            reduced_counts[MOTIFS[current]] += 1
            walk_hash.update(json.dumps([walk, current]).encode())
        if len(walk) == 11:
            return
        for c in sorted(U - {walk[-1]}):
            visit(walk + [c])
    visit([D])
    return dict(**counts, pair_sha256=assignment_hash.hexdigest(),
                closed_walks=sum(reduced_counts.values()), reduction_counts=dict(sorted(reduced_counts.items())),
                walk_sha256=walk_hash.hexdigest(), maximum_walk_edges=10)


def attachment_options(walk):
    options = []
    for a, b in zip(walk, walk[1:]):
        pair = {a, b}
        boundary = product(*[[v for v in ARC if Q[v] == c]
                             for c in range(3) if c not in pair])
        options.append([(tuple(ns), leaf) for ns in boundary
                        for leaf in (((2, 1, 4), (2, 3, 4)) if D not in pair else (None,))])
    return options


def make_graph(walk, choices):
    n = len(walk)-1
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((Z, b) for b in (0, 1, 4, 6, 5+n))
    graph.add_edges_from((v, v+1) for v in range(6, 5+n))
    leaves, next_vertex = {}, 6+n
    for i, (ns, contacts) in enumerate(choices):
        v = 6+i
        graph.add_edges_from((v, b) for b in ns)
        if contacts is not None:
            leaves[i] = next_vertex
            graph.add_edge(v, next_vertex)
            graph.add_edges_from((next_vertex, b) for b in contacts)
            next_vertex += 1
    return graph, leaves


def criticality(graph):
    assert graph.degree(Z) == 5
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    assert nx.is_tree(graph.subgraph([v for v in graph if v > Z]))
    component_graph = graph.copy()
    component_graph.remove_edges_from((Z, b) for b in (0, 1, 4))
    witnesses = [coloring(component_graph, dict(enumerate(Q)) | {Z: a}) for a in sorted(U)]
    assert [a for a, w in enumerate(witnesses) if w is None] == [D]
    assert coloring(graph, dict(enumerate(Q))) is None
    deleted = []
    for e in edges(graph):
        if e in CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        witness = coloring(child, dict(enumerate(Q)))
        assert witness is not None, e
        deleted.append(dict(edge=e, coloring=[witness[v] for v in sorted(graph)]))
    return dict(z_color_witnesses=[None if w is None else [w[v] for v in sorted(graph)] for w in witnesses],
                q_deletions=deleted)


def validate_subdivision(graph, witness):
    branch = set(witness['branch_vertices'])
    used, links, interiors = set(), set(), set()
    for path in witness['paths']:
        assert len(path) == len(set(path)) and len(path) >= 2
        assert path[0] in branch and path[-1] in branch
        assert not (set(path[1:-1]) & (branch | interiors))
        interiors.update(path[1:-1])
        link = tuple(sorted((path[0], path[-1])))
        assert link not in links
        links.add(link)
        for u, v in zip(path, path[1:]):
            e = tuple(sorted((u, v)))
            assert graph.has_edge(u, v) and e not in used
            used.add(e)
    model = nx.Graph(sorted(links))
    if witness['model'] == 'K5':
        assert len(branch) == 5 and links == set(combinations(sorted(branch), 2))
    else:
        assert witness['model'] == 'K3,3' and len(branch) == 6
        assert nx.is_bipartite(model) and all(d == 3 for _, d in model.degree())
    return used


def validate_minor(source, target, branches, boundary_fixed=True):
    assert set(branches) == set(target)
    used, provenance = set(), []
    for v, bs in sorted(branches.items()):
        assert bs and set(bs) <= set(source) and len(bs) == len(set(bs))
        assert not (used & set(bs)) and nx.is_connected(source.subgraph(bs))
        used.update(bs)
        if boundary_fixed and v < 5:
            assert bs == [v]
    for u, v in edges(target):
        candidates = sorted(tuple(sorted((a, b))) for a in branches[u] for b in branches[v]
                            if source.has_edge(a, b))
        assert candidates, (u, v)
        provenance.append(dict(target=[u, v], source=candidates[0]))
    return dict(branch_sets=[dict(target=v, source=bs) for v, bs in sorted(branches.items())],
                edges=provenance, deleted_vertices=sorted(set(source)-used))


def templates(saved):
    rows, pool, pool_edges, counts = [], [], [], Counter()
    if saved is not None:
        pool = saved['subdivisions']
        pool_edges = [{tuple(sorted((u, v))) for path in w['paths'] for u, v in zip(path, path[1:])}
                      for w in pool]
    for kind, walk in motifs():
        for choices in product(*attachment_options(walk)):
            graph, _ = make_graph(walk, choices)
            check = criticality(graph)
            apex = max(graph)+1
            augmented = graph.copy()
            augmented.add_edges_from((apex, b) for b in range(5))
            if saved is None:
                es = set(edges(augmented))
                wi = next((i for i, wes in enumerate(pool_edges) if wes <= es), None)
                if wi is None:
                    witness = kuratowski_certificate(augmented)
                    wi = len(pool)
                    pool.append(witness)
                    pool_edges.append(validate_subdivision(augmented, witness))
            else:
                wi = saved['templates'][len(rows)]['subdivision']
            validate_subdivision(augmented, pool[wi])
            rows.append(dict(kind=kind, walk=walk, choices=choices, edges=edges(graph),
                             apex=apex, subdivision=wi, **check))
            counts[kind] += 1
    assert counts == dict(triangle=48, split=48, nested=168, square=96, lollipop=288)
    return rows, pool, counts


def short_minor(walk, choices, retained):
    source, old_leaves = make_graph(walk, choices)
    new_choices = [choices[i] for i in retained]
    new_walk = tuple([walk[retained[0]]] + [walk[i+1] for i in retained])
    target, new_leaves = make_graph(new_walk, new_choices)
    branches = {v: [v] for v in range(5)}
    branches[Z] = sorted([Z] + [6+i for i in range(retained[0])] +
                         [6+i for i in range(retained[-1]+1, len(walk)-1)])
    for j, i in enumerate(retained):
        end = retained[j+1] if j+1 < len(retained) else i+1
        branches[6+j] = list(range(6+i, 6+end))
        if j in new_leaves:
            branches[new_leaves[j]] = [old_leaves[i]]
    certificate = validate_minor(source, target, branches)
    return new_walk, new_choices, target, branches, certificate


def compose_minor(outer, inner):
    return {v: sorted({u for x in bs for u in outer[x]}) for v, bs in inner.items()}


def topology_on_source(source, target, composed, witness):
    sa, ta = max(source)+1, max(target)+1
    source_apex = source.copy()
    source_apex.add_edges_from((sa, b) for b in range(5))
    composed = dict(composed) | {ta: [sa]}
    contracted = {v: [v] for v in witness['branch_vertices']}
    model = nx.Graph()
    for path in witness['paths']:
        contracted[path[0]].extend(path[1:-1])
        model.add_edge(path[0], path[-1])
    lifted = compose_minor(composed, contracted)
    return dict(apex=sa, model=witness['model'],
                **validate_minor(source_apex, model, lifted, boundary_fixed=False))


def long_controls(rows, pool):
    lookup = {json.dumps([r['walk'], r['choices']]): i for i, r in enumerate(rows)}
    records = []
    for index, (_, motif) in enumerate(motifs()):
        # Prefix, suffix and internal loops exercise both root absorption and interior contraction.
        a = motif[1]
        walk = (D, a, D) + motif[1:] + (a, D)
        insert = (walk[1]+1) % 3
        if insert == walk[1]:
            insert = (insert+1) % 3
        walk = walk[:2] + (insert, walk[1]) + walk[2:]
        choices = [opts[(index+i) % len(opts)] for i, opts in enumerate(attachment_options(walk))]
        source, _ = make_graph(walk, choices)
        source_check = criticality(source)
        current, current_choices = walk, choices
        composed = {v: [v] for v in source}
        steps = []
        target = source
        while step := reduction(current):
            expected, retained, interval = step
            new_walk, new_choices, target, branches, cert = short_minor(current, current_choices, retained)
            assert new_walk == expected
            criticality(target)
            composed = compose_minor(composed, branches)
            steps.append(dict(deleted_walk_interval=interval, retained=retained,
                              target_walk=new_walk, minor=cert))
            current, current_choices = new_walk, new_choices
        ti = lookup[json.dumps([current, current_choices])]
        witness = pool[rows[ti]['subdivision']]
        records.append(dict(walk=walk, choices=choices, source_edges=edges(source),
                            **source_check, steps=steps, template=ti,
                            composed_minor=validate_minor(source, target, composed),
                            source_obstruction=topology_on_source(source, target, composed, witness)))
    return records


def expand_tree(graph, leaves, fork):
    """Named source trees: replace a spoke by a non-D forcer and each D leaf by a tree."""
    graph = graph.copy()
    next_vertex = max(graph)+1
    parent, contact = next((v, b) for v in sorted(graph) if v > Z and v not in leaves.values()
                           for b in sorted(graph[v]) if b < 5)
    c = Q[contact]
    root, leaf = next_vertex, next_vertex+1
    next_vertex += 2
    graph.remove_edge(parent, contact)
    graph.add_edges_from(((parent, root), (root, leaf)))
    graph.add_edges_from((root, next(b for b in ARC if Q[b] == color)) for color in range(3) if color != c)
    graph.add_edges_from((leaf, contact if color == c else next(b for b in ARC if Q[b] == color))
                         for color in range(3))
    for v in leaves.values():
        contacts = {Q[b]: b for b in graph[v] if b < 5}
        graph.remove_edges_from((v, b) for b in contacts.values())
        if not fork:
            x, y = next_vertex, next_vertex+1
            next_vertex += 2
            graph.add_edges_from(((v, x), (x, y)))
            graph.add_edges_from((u, contacts[c]) for u in (v, x) for c in (1, 2))
            graph.add_edges_from((y, b) for b in contacts.values())
        else:
            graph.add_edge(v, contacts[2])
            for color in (0, 1):
                x, y = next_vertex, next_vertex+1
                next_vertex += 2
                graph.add_edges_from(((v, x), (x, y)))
                graph.add_edges_from((x, contacts[c]) for c in range(3) if c != color)
                graph.add_edges_from((y, b) for b in contacts.values())
    return graph


def normalize_tree(source):
    inner = source.subgraph([v for v in source if v > Z])
    ports = sorted(set(source[Z]) & set(inner))
    path = nx.shortest_path(inner, *ports)
    target = nx.Graph(sorted(CYCLE))
    target.add_edges_from((Z, b) for b in (0, 1, 4, 6, 5+len(path)))
    target.add_edges_from((v, v+1) for v in range(6, 5+len(path)))
    labels = {v: 6+i for i, v in enumerate(path)}
    branches = {v: [v] for v in range(6)} | {labels[v]: [v] for v in path}
    for v in path:
        target.add_edges_from((labels[v], b) for b in source[v] if b < 5)
    forcers = []
    for vs in sorted(sorted(c) for c in nx.connected_components(inner.subgraph(set(inner)-set(path)))):
        root, parent = next((v, p) for v in vs for p in source[v] if p in labels)
        assert sum(p in labels for v in vs for p in source[v]) == 1
        side = source.subgraph(set(range(5)) | set(vs)).copy()
        available = [a for a in sorted(U) if coloring(side, dict(enumerate(Q)) | {root: a}) is not None]
        assert len(available) == 1
        color = available[0]
        contacts = sorted((v, b) for v in vs for b in source[v] if b < 5)
        if color == D:
            new = max(target)+1
            target.add_edge(labels[parent], new)
            selected = [next((v, b) for v, b in contacts if Q[b] == c) for c in range(3)]
            target.add_edges_from((new, b) for _, b in selected)
            branches[new] = vs
        else:
            selected = [next((v, b) for v, b in contacts if Q[b] == color)]
            target.add_edge(labels[parent], selected[0][1])
            branches[labels[parent]] += vs
            branches[labels[parent]].sort()
        forcers.append(dict(vertices=vs, root=root, parent=parent, forced=color, contacts=selected))
    lists, choices = [], []
    for v in range(6, 6+len(path)):
        bs = sorted(b for b in target[v] if b < 5)
        leaf = [w for w in target[v] if w >= 6+len(path)]
        assert len(leaf) <= 1
        leaf_contacts = (tuple(next(b for b in target[leaf[0]] if b < 5 and Q[b] == c)
                               for c in range(3)) if leaf else None)
        lists.append(U - {Q[b] for b in bs} - ({D} if leaf else set()))
        # Canonical color order, shared with attachment_options.
        choices.append((tuple(sorted(bs, key=lambda b: Q[b])), leaf_contacts))
    walk = tuple(trace(lists, D))
    canonical, _ = make_graph(walk, choices)
    # Relabel the leaf IDs created in component order into path order.
    mapping = {v: v for v in range(6+len(path))}
    next_leaf = 6+len(path)
    for v in range(6, 6+len(path)):
        for w in target[v]:
            if w >= 6+len(path):
                mapping[w] = next_leaf
                next_leaf += 1
    branches = {mapping[v]: bs for v, bs in branches.items()}
    assert edges(nx.relabel_nodes(target, mapping)) == edges(canonical)
    return canonical, walk, choices, branches, forcers


def tree_controls(rows, pool):
    lookup = {json.dumps([r['walk'], r['choices']]): i for i, r in enumerate(rows)}
    controls = []
    for kind in ('triangle', 'split', 'nested', 'square', 'lollipop'):
        row = next(r for r in rows if r['kind'] == kind)
        base, leaves = make_graph(row['walk'], row['choices'])
        for fork in (False, True):
            source = expand_tree(base, leaves, fork)
            check = criticality(source)
            target, walk, choices, branches, forcers = normalize_tree(source)
            criticality(target)
            ti = lookup[json.dumps([walk, choices])]
            controls.append(dict(kind=kind, fork=fork, source_edges=edges(source), **check,
                                 forcers=forcers, target_walk=walk, template=ti,
                                 minor=validate_minor(source, target, branches),
                                 source_obstruction=topology_on_source(source, target, branches,
                                                                      pool[rows[ti]['subdivision']])))
    return controls


def k4_control():
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((Z, v) for v in (0, 1, 4, 6, 7))
    graph.add_edges_from(combinations(range(6, 10), 2))
    for v, leaf in ((8, 10), (9, 11)):
        graph.add_edge(v, leaf)
        graph.add_edges_from((leaf, b) for b in (1, 2, 4))
    assert all(graph.degree(v) == 4 for v in range(6, 12)) and graph.degree(Z) == 5
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z, b) for b in (0, 1, 4))
    bans = [a for a in sorted(U) if coloring(relaxed, dict(enumerate(Q)) | {Z: a}) is None]
    assert bans == [D]
    deletions = []
    for e in edges(graph):
        if e in CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        w = coloring(child, dict(enumerate(Q)))
        assert w is not None
        deletions.append(dict(edge=e, coloring=[w[v] for v in sorted(graph)]))
    branches = {0: list(range(6)) + [10, 11]} | {i+1: [v] for i, v in enumerate(range(6, 10))}
    return dict(edges=edges(graph), q_deletions=deletions,
                k5_minor=validate_minor(graph, nx.complete_graph(5), branches, boundary_fixed=False))


def build(saved):
    local = local_controls()
    rows, pool, counts = templates(saved)
    long = long_controls(rows, pool)
    trees = tree_controls(rows, pool)
    k4 = k4_control()
    names = ('c5_degree5_tree_components', 'c5_k4_blocks', 'c5_odd_join_cores',
             'c5_disk_deletions', 'c5_cell_enumerator', 'local_closure', 'boundary_relations')
    return dict(schema=1, scope='Paper arbitrary-tree reduction; five finite walk forms; no general degree-five theorem or Lean proof.',
                source_sha256={f'scripts/{n}.py': digest(ROOT/'scripts'/f'{n}.py') for n in names},
                input_sha256={str(SECTORS.relative_to(ROOT)): digest(SECTORS)},
                local=local, templates=rows, subdivisions=pool, long_controls=long,
                tree_controls=trees, k4_control=k4,
                summary=dict(pair_assignments=local['pair_assignments'], closed_walks=local['closed_walks'],
                             motif_palettes=len(MOTIFS), lifts=dict(sorted(counts.items())),
                             subdivisions=len(pool), long_controls=len(long),
                             shortening_steps=sum(len(r['steps']) for r in long),
                             tree_controls=len(trees), k4_controls=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    result = build(saved)
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
