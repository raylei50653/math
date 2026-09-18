#!/usr/bin/env python3
"""One odd-cycle two-port reduction; fixed-q semantics and explicit minors.

Unbounded coverage is proved in the report. No planarity search or graph catalog.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

import c5_degree5_triangle_components as triangle
import c5_degree5_tree_components as tree
from c5_k4_blocks import CYCLE, Q, U, coloring

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_odd_cycle_components/observations.json'
TRIANGLE = triangle.OUT
D, Z = 3, 5


def cycle_witness(lists):
    """Exact path dynamic programming with a fixed first color, then close."""
    for first in sorted(lists[0]):
        paths = {first: [first]}
        for allowed in lists[1:]:
            paths = {c: path + [c] for c in sorted(allowed)
                     if (path := next((p for d, p in sorted(paths.items()) if d != c), None))}
        for last, path in sorted(paths.items()):
            if last != first:
                assert all(c in allowed for c, allowed in zip(path, lists))
                assert all(a != b for a, b in zip(path, path[1:] + path[:1]))
                return path
    return None


def restriction(message):
    return set(message) if len(message) == 1 else set()


def local_controls():
    digest, counts = sha256(), Counter()
    lists_ge_two = [frozenset(cs) for n in (2, 3, 4) for cs in combinations(range(4), n)]
    for n, options in ((3, lists_ge_two), (4, lists_ge_two), (5, tree.PAIRS)):
        for lists in product(options, repeat=n):
            actual = cycle_witness(lists) is not None
            expected = not (n % 2 and len(set(lists)) == 1 and len(lists[0]) == 2)
            assert actual == expected
            # Independent full tuples for the complete short-list domain.
            brute = any(all(a != b for a, b in zip(cs, cs[1:] + cs[:1]))
                        for cs in product(*map(sorted, lists)))
            assert actual == brute
            counts['cycle_list_assignments'] += 1
            digest.update(json.dumps([list(map(sorted, lists)), actual]).encode())
    messages = [{a} for a in range(4)] + [set(U)]
    # Non-singleton arm messages impose no restriction on their cycle endpoint.
    for palette in tree.PAIRS:
        for n in (3, 5, 7, 9):
            available = [a for a in range(4)
                         if cycle_witness([{a}] + [palette] * (n-1)) is not None]
            assert set(available) == U-palette
            for left, right in product(messages, repeat=2):
                lists = [U-restriction(left)-restriction(right)] + [palette] * (n-1)
                actual = cycle_witness(lists) is not None
                expected = bool((U-palette)-restriction(left)-restriction(right))
                assert actual == expected
                counts['shared_message_queries'] += 1
                digest.update(json.dumps([sorted(palette), n, sorted(left), sorted(right), actual]).encode())
            for cu, cv in product(sorted(U-palette), repeat=2):
                for position in range(1, n):
                    for left, right in product(messages, repeat=2):
                        lu = (palette | {cu}) - restriction(left)
                        lv = (palette | {cv}) - restriction(right)
                        lists = [palette] * n
                        lists[0], lists[position] = lu, lv
                        actual = cycle_witness(lists) is not None
                        reduced = cycle_witness([lu, lv, palette]) is not None
                        assert actual == reduced == (not (lu == lv == palette))
                        counts['distinct_message_queries'] += 1
                        digest.update(json.dumps([sorted(palette), n, position, cu, cv,
                                                  sorted(left), sorted(right), actual]).encode())
    # Full two-port relations are NOT preserved: two nonadjacent marked vertices
    # can share an outside color in C5, whereas their triangle images are adjacent.
    control_lists = [{2}, {0, 1}, {2}, {0, 1}, {0, 1}]
    witness = cycle_witness(control_lists)
    assert witness is not None and cycle_witness([{2}, {2}, {0, 1}]) is None
    return dict(**counts, sha256=digest.hexdigest(), relation_negative_control=dict(
        cycle_lists=list(map(sorted, control_lists)), marked_positions=[0, 2],
        source_coloring=witness, triangle_lists=[[2], [2], [0, 1]], triangle_colorable=False))


def criticality(graph, cycle_length):
    assert graph.degree(Z) == 5
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    inner = graph.subgraph([v for v in graph if v > Z])
    assert nx.is_connected(inner)
    cycles = nx.cycle_basis(inner)
    assert len(cycles) == 1 and len(cycles[0]) == cycle_length
    assert len(set(graph[Z]) - set(range(5))) == 2
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z, b) for b in (0, 1, 4))
    witnesses = [coloring(relaxed, dict(enumerate(Q)) | {Z: a}) for a in range(4)]
    assert [a for a, w in enumerate(witnesses) if w is None] == [D]
    deletions = []
    for e in tree.edges(graph):
        if e in CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        witness = coloring(child, dict(enumerate(Q)))
        assert witness is not None, e
        deletions.append(dict(edge=e, coloring=[witness[v] for v in sorted(graph)]))
    return dict(z_colorings=[None if w is None else [w[v] for v in sorted(graph)] for w in witnesses],
                q_deletions=deletions)


def expand_cycle(target, retained, palette, lengths, variant):
    """Expand three arcs; contracting each arc into its initial retained vertex
    deletes only the inserted vertices' attachments. All retained attachments stay.
    """
    assert len(retained) == 3 and sum(lengths) % 2 == 1 and min(lengths) >= 1
    source = target.copy()
    branches = {v: [v] for v in sorted(target)}
    nxt, paths = max(source)+1, []
    for i, (u, v) in enumerate(zip(retained, retained[1:] + retained[:1])):
        source.remove_edge(u, v)
        inserted = list(range(nxt, nxt+lengths[i]-1))
        nxt += lengths[i]-1
        path = [u, *inserted, v]
        source.add_edges_from(zip(path, path[1:]))
        branches[u].extend(inserted)
        paths.append(path)
        for vertex in inserted:
            for c in sorted(U-palette):
                if c == D:
                    source.add_edge(vertex, nxt)
                    source.add_edges_from((nxt, b) for b in (2, 1+2*((vertex+variant) % 2), 4))
                    nxt += 1
                else:
                    options = [b for b in triangle.ARC if Q[b] == c]
                    source.add_edge(vertex, options[(vertex+variant) % len(options)])
    return source, branches, paths


def subdivision_for(graph, pool):
    augmented = graph.copy()
    augmented.add_edges_from((max(graph)+1, b) for b in range(5))
    es = set(tree.edges(augmented))
    witness = next(w for w in pool if {tuple(sorted(e)) for p in w['paths']
                                      for e in zip(p, p[1:])} <= es)
    tree.validate_subdivision(augmented, witness)
    return witness


def graph_controls(saved, tree_saved):
    selected, seen = [], set()
    for i, row in enumerate(saved['templates']):
        form = row['form']
        key = ((form['kind'], tuple(form['palette']), form['left'][-1], form['right'][-1])
               if form['kind'] == 'distinct' else (form['kind'], form['motif'], form['mark']))
        if key not in seen:
            selected.append((i, row))
            seen.add(key)
    records, counts = [], Counter()
    # Includes two even arcs, hence not merely even subdivisions of each edge.
    arc_lengths = ((1, 2, 2), (2, 1, 4), (3, 4, 2))
    for i, row in selected:
        form = row['form']
        target = triangle.make_graph(form, row['representative_choices'])
        target_check = triangle.criticality(target)
        if form['kind'] == 'distinct':
            retained, palette = [6, 7, 8], set(form['palette'])
        else:
            n, mark = len(form['walk'])-1, form['mark']
            retained = [6+mark, 6+n, 7+n]
            palette = U-{form['walk'][mark], form['walk'][mark+1]}
        witness = subdivision_for(target, saved['subdivisions'])
        for variant, lengths in enumerate(arc_lengths):
            source, branches, paths = expand_cycle(target, retained, palette, lengths, variant)
            check = criticality(source, sum(lengths))
            minor = tree.validate_minor(source, target, branches)
            assert branches[Z] == [Z]
            counts[form['kind']] += 1
            records.append(dict(kind=form['kind'], template=i, form=form, palette=sorted(palette),
                                cycle_paths=paths, source_edges=tree.edges(source), **check,
                                target_edges=tree.edges(target), target_check=target_check, minor=minor,
                                source_obstruction=tree.topology_on_source(source, target, branches, witness)))
    for old in saved['cyclic_branch_controls']:
        target = nx.Graph(old['source_edges'])
        cycle = sorted(nx.cycle_basis(target.subgraph([v for v in target if v > Z]))[0])
        # The root (least cycle label) has one spoke and one parent bridge.
        x = cycle[1]
        palette = U-{Q[b] for b in target[x] if b < 5}
        assert len(palette) == 2
        normalized, walk, choices, next_branches, forcers = tree.normalize_tree(target)
        tree.criticality(normalized)
        witness = subdivision_for(normalized, tree_saved['subdivisions'])
        for variant, lengths in enumerate(arc_lengths):
            source, branches, paths = expand_cycle(target, cycle, palette, lengths, variant)
            check = criticality(source, sum(lengths))
            composed = tree.compose_minor(branches, next_branches)
            counts['side'] += 1
            records.append(dict(kind='side', motif=old['kind'], palette=sorted(palette),
                                cycle_paths=paths, source_edges=tree.edges(source), **check,
                                target_edges=tree.edges(target), minor=tree.validate_minor(source, target, branches),
                                forcers=forcers, tree_walk=walk, tree_choices=choices,
                                tree_minor=tree.validate_minor(source, normalized, composed),
                                source_obstruction=tree.topology_on_source(source, normalized, composed, witness)))
    assert counts == dict(distinct=72, shared=60, side=15), counts
    return records, dict(counts)


def build():
    saved, tree_saved = json.loads(TRIANGLE.read_text()), json.loads(triangle.TREE.read_text())
    controls, counts = graph_controls(saved, tree_saved)
    local = local_controls()
    names = ('c5_degree5_odd_cycle_components', 'c5_degree5_triangle_components',
             'c5_degree5_tree_components', 'c5_k4_blocks', 'c5_odd_join_cores',
             'c5_disk_deletions', 'c5_cell_enumerator', 'local_closure', 'boundary_relations')
    return dict(schema=1, scope='One odd-cycle plus bridges, three-spoke two-port components; paper reduction, no Lean theorem.',
                source_sha256={f'scripts/{name}.py': tree.digest(ROOT/'scripts'/f'{name}.py') for name in names},
                input_sha256={str(p.relative_to(ROOT)): tree.digest(p) for p in (TRIANGLE, triangle.TREE)},
                local=local, controls=controls,
                summary=dict(graph_controls=counts, cycle_lengths=[5, 7, 9],
                             **{k: v for k, v in local.items() if k.endswith('queries') or k.endswith('assignments')}))


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
