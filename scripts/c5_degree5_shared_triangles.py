#!/usr/bin/env python3
"""Two triangles sharing a cut vertex: two-port normal forms and minors.

Unbounded coverage is a paper proof. --check only replays subdivisions.
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
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_shared_triangles/observations.json'
D, Z = 3, 5


def forms():
    for palette in tree.PAIRS:
        for kind in ('same', 'opposite'):
            other = palette if kind == 'same' else U-palette
            left = [w for c in sorted(U-palette) for w in triangle.simple_walks(c)]
            right = [w for c in sorted(U-other) for w in triangle.simple_walks(c)]
            for a, b in product(left, right):
                yield dict(kind=kind, palette=sorted(palette), left=a, right=b)
    for motif, walk in tree.motifs():
        for mark in range(len(walk)-1):
            yield dict(kind='marked', motif=motif, walk=walk, mark=mark)


def skeleton(form):
    if form['kind'] == 'tree':
        return triangle.skeleton(form)
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((Z, b) for b in (0, 1, 4))
    if form['kind'] in ('same', 'opposite'):
        # Shared vertex 6; private vertices 7,8 and 9,10.
        palette = set(form['palette'])
        graph.add_edges_from(combinations((6, 7, 8), 2))
        graph.add_edges_from(combinations((6, 9, 10), 2))
        bans = {6: set(), 7: U-palette, 8: U-palette, 9: palette, 10: palette}
        endpoints = (7, 8 if form['kind'] == 'same' else 9)
        nxt = 11
        for endpoint, side in zip(endpoints, ('left', 'right')):
            walk = form[side]
            bans[endpoint] = bans[endpoint]-{walk[-1]}
            last = Z
            for a, b in zip(walk, walk[1:]):
                graph.add_edge(last, nxt)
                bans[nxt] = U-{a, b}
                last, nxt = nxt, nxt+1
            graph.add_edge(last, endpoint)
    else:
        assert form['kind'] == 'marked'
        walk, mark = form['walk'], form['mark']
        n = len(walk)-1
        graph.add_edges_from((v, v+1) for v in range(6, 5+n))
        graph.add_edges_from(((Z, 6), (Z, 5+n)))
        bans = {6+i: U-{a, b} for i, (a, b) in enumerate(zip(walk, walk[1:]))}
        root, shared, private, x, y = 6+mark, 6+n, 7+n, 8+n, 9+n
        pair = {walk[mark], walk[mark+1]}
        graph.add_edges_from(combinations((root, shared, private), 2))
        graph.add_edges_from(combinations((shared, x, y), 2))
        bans.update({root: set(), shared: set(), private: pair, x: U-pair, y: U-pair})
    return graph, bans


def make_graph(form, choices):
    graph, _ = skeleton(form)
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
    assert len(set(cycles[0]) & set(cycles[1])) == 1
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


def root_available(a, b):
    return {r for r in U if any(len({r, x, y}) == 3 for x, y in product(a, b))}


def local_controls():
    options = [frozenset(cs) for n in (2, 3, 4) for cs in combinations(range(4), n)]
    fingerprint = sha256()
    root_count, joint_count = 0, 0
    for a, b in product(options, repeat=2):
        actual = root_available(a, b)
        expected = U-a if a == b and len(a) == 2 else U
        assert actual == expected
        fingerprint.update(json.dumps([sorted(a), sorted(b), sorted(actual)]).encode())
        root_count += 1
    for lists in product(options, repeat=4):
        left, right = root_available(*lists[:2]), root_available(*lists[2:])
        # Full five-vertex tuples, without separately rechoosing shared root.
        actual = {r for r in U if any(len({r, a, b}) == 3 and len({r, c, d}) == 3
                                    for a, b, c, d in product(*lists))}
        assert actual == left & right
        bad = lists[0] == lists[1] and lists[2] == lists[3] and len(lists[0]) == 2 and lists[2] == U-lists[0]
        assert (not actual) == bad
        fingerprint.update(json.dumps([list(map(sorted, lists)), sorted(actual)]).encode())
        joint_count += 1
    return dict(root_queries=root_count, shared_root_queries=joint_count, sha256=fingerprint.hexdigest())


def templates(saved):
    pool = [] if saved is None else saved['subdivisions']
    pool_edges = [{tuple(sorted(e)) for p in w['paths'] for e in zip(p, p[1:])} for w in pool]
    records, counts, cover = [], Counter(), sha256()
    for index, form in enumerate(forms()):
        _, bans = skeleton(form)
        options = triangle.attachment_options(bans)
        first = [opts[0] for opts in options]
        representative = make_graph(form, first)
        semantics = criticality(representative)
        interior_edges = set(representative.subgraph([v for v in representative if v >= Z]).edges())
        boundary_colors = {v: sorted(Q[b] for b in representative[v] if b < 5)
                           for v in representative if v >= Z}
        n = 0
        for choices in product(*options):
            graph = make_graph(form, choices)
            assert graph.degree(Z) == 5 and all(graph.degree(v) == 4 for v in graph if v > Z)
            assert set(graph) == set(representative)
            assert set(graph.subgraph([v for v in graph if v >= Z]).edges()) == interior_edges
            assert all(sorted(Q[b] for b in graph[v] if b < 5) == cs for v, cs in boundary_colors.items())
            apex = max(graph)+1
            graph.add_edges_from((apex, b) for b in range(5))
            es = set(tree.edges(graph))
            wi = next((i for i, wes in enumerate(pool_edges) if wes <= es), None)
            if wi is None:
                assert saved is None, ('missing saved subdivision', index, choices)
                witness = kuratowski_certificate(graph)
                wi = len(pool)
                pool.append(witness)
                pool_edges.append(tree.validate_subdivision(graph, witness))
            tree.validate_subdivision(graph, pool[wi])
            cover.update(json.dumps([index, choices, tree.edges(graph), wi]).encode())
            n += 1
        records.append(dict(form=form, lifts=n, representative_choices=first, **semantics))
        counts[form['kind']] += n
        if saved is None and (index+1) % 100 == 0:
            print(f'forms={index+1} lifts={sum(counts.values())} subdivisions={len(pool)}', flush=True)
    return records, pool, dict(counts), cover.hexdigest()


def transfer_choices(form, choices, new, mapping, branches):
    """Keep attachments of retained skeleton vertices; delete the others."""
    old_leaf, new_leaf = max(skeleton(form)[0])+1, max(skeleton(new)[0])+1
    result = []
    for v, c, bs in choices:
        if v in mapping:
            result.append((mapping[v], c, bs))
            if c == D:
                branches[new_leaf] = [old_leaf]
                new_leaf += 1
        if c == D:
            old_leaf += 1
    return result


def shorten_arm(form, choices, side):
    walk = form[side]
    interval = next(((i, j) for i in range(len(walk)) for j in range(i+1, len(walk))
                     if walk[i] == walk[j]), None)
    if interval is None:
        return None
    i, j = interval
    new = dict(form) | {side: tuple(walk[:i])+tuple(walk[j:])}
    paths = {'left': list(range(11, 10+len(form['left']))),
             'right': list(range(10+len(form['left']), 9+len(form['left'])+len(form['right'])))}
    retained = {s: list(range(len(form[s])-1)) for s in ('left', 'right')}
    retained[side] = list(range(i))+list(range(j, len(walk)-1))
    branches, mapping, nxt = {v: [v] for v in range(11)}, {v: v for v in range(11)}, 11
    for s in ('left', 'right'):
        for k in retained[s]:
            mapping[paths[s][k]] = nxt
            branches[nxt] = [paths[s][k]]
            nxt += 1
    recipient = Z if i == 0 else mapping[paths[side][i-1]]
    branches[recipient] += paths[side][i:j]
    ch = transfer_choices(form, choices, new, mapping, branches)
    source, target = make_graph(form, choices), make_graph(new, ch)
    return new, ch, target, branches, tree.validate_minor(source, target, branches)


def shorten_marked(form, choices):
    walk = form['walk']
    step = tree.reduction(walk)
    if step is None:
        return None
    new_walk, retained, interval = step
    mark = form.get('mark')
    new = (dict(kind='marked', walk=new_walk, mark=retained.index(mark)) if mark in retained
           else dict(kind='tree', walk=new_walk))
    mapping = {6+i: 6+j for j, i in enumerate(retained)}
    branches = {v: [v] for v in range(5)}
    branches[Z] = [Z]+[6+i for i in range(retained[0])]+[6+i for i in range(retained[-1]+1, len(walk)-1)]
    for j, i in enumerate(retained):
        end = retained[j+1] if j+1 < len(retained) else i+1
        branches[6+j] = list(range(6+i, 6+end))
    if new['kind'] == 'marked':
        for k in range(4):
            old_v, new_v = 5+len(walk)+k, 5+len(new_walk)+k
            mapping[old_v] = new_v
            branches[new_v] = [old_v]
    ch = transfer_choices(form, choices, new, mapping, branches)
    source, target = make_graph(form, choices), make_graph(new, ch)
    return new, ch, target, branches, dict(interval=interval, minor=tree.validate_minor(source, target, branches))


def subdivision_for(graph, pool):
    augmented = graph.copy()
    augmented.add_edges_from((max(graph)+1, b) for b in range(5))
    es = set(tree.edges(augmented))
    witness = next(w for w in pool if {tuple(sorted(e)) for p in w['paths'] for e in zip(p, p[1:])} <= es)
    tree.validate_subdivision(augmented, witness)
    return witness


def long_controls(records, pool, old):
    selected, seen = [], set()
    for row in records:
        f = row['form']
        if f['kind'] == 'marked':
            continue
        key = (f['kind'], tuple(f['palette']), f['left'][-1], f['right'][-1])
        if key not in seen:
            selected.append(f)
            seen.add(key)
    result, counts = [], Counter()
    for index, f in enumerate(selected):
        form = dict(f)
        for side in ('left', 'right'):
            w = tuple(form[side])
            # Prefix loops include arms whose final normal form has zero length.
            form[side] = (D, index % 3, D)+w[1:]
        _, bans = skeleton(form)
        choices = [opts[index % len(opts)] for opts in triangle.attachment_options(bans)]
        source = make_graph(form, choices)
        check = criticality(source)
        current, ch, target = form, choices, source
        composed, steps = {v: [v] for v in source}, []
        for side in ('left', 'right'):
            while step := shorten_arm(current, ch, side):
                current, ch, target, branches, cert = step
                criticality(target)
                composed = tree.compose_minor(composed, branches)
                steps.append(dict(side=side, form=current, minor=cert))
        witness = subdivision_for(target, pool)
        counts[form['kind']] += 1
        result.append(dict(form=form, choices=choices, source_edges=tree.edges(source), **check,
                           steps=steps, final_form=current,
                           composed_minor=tree.validate_minor(source, target, composed),
                           source_obstruction=tree.topology_on_source(source, target, composed, witness)))
    for kind in ('triangle', 'split', 'nested', 'square', 'lollipop'):
        motif = next(w for k, w in tree.motifs() if k == kind)
        a = motif[1]
        walk = (D, a, D)+motif[1:]+(a, D)
        for mark in (0, 2+(len(motif)-2)//2):
            form = dict(kind='marked', walk=walk, mark=mark)
            _, bans = skeleton(form)
            choices = [opts[0] for opts in triangle.attachment_options(bans)]
            source = make_graph(form, choices)
            check = criticality(source)
            current, ch, target = form, choices, source
            composed, steps = {v: [v] for v in source}, []
            while step := shorten_marked(current, ch):
                current, ch, target, branches, cert = step
                (criticality if current['kind'] == 'marked' else tree.criticality)(target)
                composed = tree.compose_minor(composed, branches)
                steps.append(dict(form=current, **cert))
            witness = subdivision_for(target, pool if current['kind'] == 'marked' else old['subdivisions'])
            counts['marked_to_'+current['kind']] += 1
            result.append(dict(form=form, choices=choices, source_edges=tree.edges(source), **check,
                               steps=steps, final_form=current,
                               composed_minor=tree.validate_minor(source, target, composed),
                               source_obstruction=tree.topology_on_source(source, target, composed, witness)))
    return result, dict(counts)


def side_controls(old):
    result = []
    for kind in ('triangle', 'split', 'nested', 'square', 'lollipop'):
        row = next(r for r in old['templates'] if r['kind'] == kind)
        source, _ = tree.make_graph(row['walk'], row['choices'])
        parent, b = next((v, b) for v in sorted(source) if v > Z for b in sorted(source[v]) if b < 5)
        c, h = Q[b], next(x for x in range(3) if x != Q[b])
        root, shared, private, x, y = range(max(source)+1, max(source)+6)
        source.remove_edge(parent, b)
        source.add_edge(parent, root)
        source.add_edges_from(combinations((root, shared, private), 2))
        source.add_edges_from(combinations((shared, x, y), 2))
        pair = {c, h}
        bans = {root: {h}, shared: set(), private: pair, x: U-pair, y: U-pair}
        nxt = max(source)+1
        for opts in triangle.attachment_options(bans):
            v, color, bs = opts[0]
            if color == D:
                source.add_edge(v, nxt)
                source.add_edges_from((nxt, contact) for contact in bs)
                nxt += 1
            else:
                source.add_edge(v, bs[0])
        check = criticality(source)
        target, walk, choices, branches, forcers = tree.normalize_tree(source)
        tree.criticality(target)
        witness = subdivision_for(target, old['subdivisions'])
        result.append(dict(kind=kind, source_edges=tree.edges(source), **check, forcers=forcers,
                           target_walk=walk, target_choices=choices,
                           minor=tree.validate_minor(source, target, branches),
                           source_obstruction=tree.topology_on_source(source, target, branches, witness)))
    # A two-color closed walk is rejected at two z colors, hence not minimal.
    form = dict(kind='marked', walk=(D, 0, D), mark=0)
    _, bans = skeleton(form)
    choices = [opts[0] for opts in triangle.attachment_options(bans)]
    graph = make_graph(form, choices)
    graph.remove_edges_from((Z, b) for b in (0, 1, 4))
    forbidden = [a for a in range(4) if coloring(graph, dict(enumerate(Q)) | {Z: a}) is None]
    assert forbidden == [0, D]
    negative = dict(form=form, choices=choices, relaxed_edges=tree.edges(graph), forbidden=forbidden)
    return result, negative


def build(saved):
    records, pool, counts, coverage = templates(saved)
    old = json.loads(tree.OUT.read_text())
    long, outcomes = long_controls(records, pool, old)
    side, negative = side_controls(old)
    names = ('c5_degree5_shared_triangles', 'c5_degree5_triangle_components',
             'c5_degree5_tree_components', 'c5_k4_blocks', 'c5_odd_join_cores',
             'c5_disk_deletions', 'c5_cell_enumerator', 'local_closure', 'boundary_relations')
    return dict(schema=1, scope='Two shared triangles only; paper coverage and finite certificates, no Lean theorem.',
                source_sha256={f'scripts/{n}.py': tree.digest(ROOT/'scripts'/f'{n}.py') for n in names},
                input_sha256={str(p.relative_to(ROOT)): tree.digest(p) for p in (triangle.OUT, tree.OUT)},
                local=local_controls(), templates=records, subdivisions=pool, coverage_sha256=coverage,
                long_controls=long, side_controls=side, minimality_negative_control=negative,
                summary=dict(forms=len(records), lifts=counts, subdivisions=len(pool),
                             long_controls=outcomes, shortening_steps=sum(len(r['steps']) for r in long),
                             side_controls=len(side)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    result = build(saved)
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
