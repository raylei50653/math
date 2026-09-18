#!/usr/bin/env python3
"""One-triangle two-port components: finite minors after paper reductions.

--check replays saved subdivisions and never invokes a planarity oracle.
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
import c5_degree5_tree_components as tree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_triangle_components/observations.json'
TREE = ROOT / 'artifacts/c5_degree5_tree_components/observations.json'
D, Z, ARC = 3, 5, (1, 2, 3, 4)


def simple_walks(end):
    if end == D:
        return [(D,)]
    return [(D, *middle, end) for n in range(3)
            for middle in permutations(sorted(U-{D, end}), n)]


def forms():
    for palette in tree.PAIRS:
        walks = [w for c in sorted(U-palette) for w in simple_walks(c)]
        for left, right in product(walks, repeat=2):
            yield dict(kind='distinct', palette=sorted(palette), left=left, right=right)
    for motif, walk in tree.motifs():
        for mark in range(len(walk)-1):
            yield dict(kind='shared', motif=motif, walk=walk, mark=mark)


def skeleton(form):
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((Z, b) for b in (0, 1, 4))
    if form['kind'] == 'distinct':
        palette = set(form['palette'])
        left, right = form['left'], form['right']
        graph.add_edges_from(combinations((6, 7, 8), 2))
        bans = {6: U-palette-{left[-1]}, 7: U-palette-{right[-1]}, 8: U-palette}
        nxt = 9
        for root, walk in ((6, left), (7, right)):
            last = Z
            for a, b in zip(walk, walk[1:]):
                graph.add_edge(last, nxt)
                bans[nxt] = U-{a, b}
                last, nxt = nxt, nxt+1
            graph.add_edge(last, root)
    else:
        walk = form['walk']
        n = len(walk)-1
        graph.add_edges_from((v, v+1) for v in range(6, 5+n))
        graph.add_edges_from(((Z, 6), (Z, 5+n)))
        bans = {6+i: U-{a, b} for i, (a, b) in enumerate(zip(walk, walk[1:]))}
        if form['kind'] == 'shared':
            mark = form['mark']
            root, x, y = 6+mark, 6+n, 7+n
            pair = {walk[mark], walk[mark+1]}
            bans[root], bans[x], bans[y] = set(), pair, pair
            graph.add_edges_from(((root, x), (root, y), (x, y)))
    return graph, bans


def attachment_options(bans):
    return [[(v, c, (b,)) for b in ARC if Q[b] == c] if c != D else
            [(v, c, (2, b, 4)) for b in (1, 3)]
            for v, cs in sorted(bans.items()) for c in sorted(cs)]


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
    assert len(cycles) == 1 and len(cycles[0]) == 3
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z, b) for b in (0, 1, 4))
    witnesses = [coloring(relaxed, dict(enumerate(Q)) | {Z: a}) for a in sorted(U)]
    assert [a for a, w in enumerate(witnesses) if w is None] == [D]
    deletions = []
    for e in tree.edges(graph):
        if e in CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        w = coloring(child, dict(enumerate(Q)))
        assert w is not None, e
        deletions.append(dict(edge=e, coloring=[w[v] for v in sorted(graph)]))
    return dict(z_colorings=[None if w is None else [w[v] for v in sorted(graph)] for w in witnesses],
                q_deletions=deletions)


def arm_message(lists, a):
    possible = {a}
    for pair in lists:
        possible = {c for c in pair if any(c != d for d in possible)}
    return possible


def local_controls():
    count, fingerprint = 0, sha256()
    for n in range(5):
        for lists in product(tree.PAIRS, repeat=n):
            outputs = []
            for a in sorted(U):
                actual = {a} if not lists else {
                    cs[-1] for cs in product(*map(sorted, lists))
                    if cs[0] != a and all(x != y for x, y in zip(cs, cs[1:]))}
                expected = arm_message(lists, a)
                assert actual == expected
                outputs.append(sorted(actual))
            # A prescribed singleton output has at most one input color.
            for c in U:
                assert sum(x == [c] for x in outputs) <= 1
            fingerprint.update(json.dumps([list(map(sorted, lists)), outputs]).encode())
            count += 1
    return dict(arm_list_assignments=count, max_arm_vertices=4, sha256=fingerprint.hexdigest())


def templates(saved):
    pool = [] if saved is None else saved['subdivisions']
    pool_edges = [{tuple(sorted(e)) for path in w['paths'] for e in zip(path, path[1:])} for w in pool]
    counts, records, cover = Counter(), [], sha256()
    for index, form in enumerate(forms()):
        base, bans = skeleton(form)
        options = attachment_options(bans)
        first = [opts[0] for opts in options]
        representative = make_graph(form, first)
        semantics = criticality(representative)
        # Changing a boundary endpoint to another vertex of the same q color
        # preserves the complete labelled interior constraint problem, including
        # each single-edge deletion (edges correspond by attachment role).
        n = 0
        for choices in product(*options):
            graph = make_graph(form, choices)
            assert graph.degree(Z) == 5 and all(graph.degree(v) == 4 for v in graph if v > Z)
            assert len(graph) == len(representative) and len(graph.edges()) == len(representative.edges())
            assert set(graph.subgraph(range(5, len(graph))).edges()) == set(representative.subgraph(range(5, len(graph))).edges())
            for v in range(5, len(graph)):
                assert sorted(Q[b] for b in graph[v] if b < 5) == sorted(Q[b] for b in representative[v] if b < 5)
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
    assert counts == dict(distinct=81992, shared=7232)
    return records, pool, dict(counts), cover.hexdigest()


def shorten_distinct(form, choices, side):
    walk = form[side]
    interval = next(((i, j) for i in range(len(walk)) for j in range(i+1, len(walk))
                     if walk[i] == walk[j]), None)
    if interval is None:
        return None
    i, j = interval
    new = dict(form) | {side: tuple(walk[:i])+tuple(walk[j:])}
    source = make_graph(form, choices)
    target_base, _ = skeleton(new)
    old_paths = {'left': list(range(9, 8+len(form['left']))),
                 'right': list(range(8+len(form['left']), 7+len(form['left'])+len(form['right'])))}
    retained = {s: list(range(len(form[s])-1)) for s in ('left', 'right')}
    retained[side] = list(range(i))+list(range(j, len(walk)-1))
    branches = {v: [v] for v in range(9)}
    mapping, nxt = {}, 9
    for s in ('left', 'right'):
        path = old_paths[s]
        for k in retained[s]:
            mapping[path[k]] = nxt
            branches[nxt] = [path[k]]
            nxt += 1
    removed = old_paths[side][i:j]
    recipient = Z if i == 0 else mapping[old_paths[side][i-1]]
    branches[recipient] += removed
    new_choices = []
    old_leaf, new_leaf = max(skeleton(form)[0])+1, max(target_base)+1
    for v, c, bs in choices:
        new_v = v if v < 9 else mapping.get(v)
        if new_v is not None:
            new_choices.append((new_v, c, bs))
            if c == D:
                branches[new_leaf] = [old_leaf]
                new_leaf += 1
        if c == D:
            old_leaf += 1
    target = make_graph(new, new_choices)
    return new, new_choices, target, branches, tree.validate_minor(source, target, branches)


def long_controls(records, pool):
    lookup = {json.dumps(r['form'], sort_keys=True): i for i, r in enumerate(records)}
    result = []
    distinct = [r for r in records if r['form']['kind'] == 'distinct']
    for index in range(0, len(distinct), 17):
        form = dict(distinct[index]['form'])
        for side in ('left', 'right'):
            w = tuple(form[side])
            # A removable prefix loop; also covers an arm shortened to zero.
            form[side] = (D, (index//17) % 3, D) + w[1:]
        _, bans = skeleton(form)
        choices = [opts[0] for opts in attachment_options(bans)]
        source = make_graph(form, choices)
        check = criticality(source)
        current, ch = form, choices
        composed = {v: [v] for v in source}
        steps, target = [], source
        for side in ('left', 'right'):
            while step := shorten_distinct(current, ch, side):
                current, ch, target, branches, cert = step
                criticality(target)
                composed = tree.compose_minor(composed, branches)
                steps.append(dict(side=side, form=current, minor=cert))
        ti = lookup[json.dumps(current, sort_keys=True)]
        augmented = target.copy()
        augmented.add_edges_from((max(target)+1, b) for b in range(5))
        es = set(tree.edges(augmented))
        witness = next(w for w in pool if {tuple(sorted(e)) for p in w['paths'] for e in zip(p,p[1:])} <= es)
        result.append(dict(form=form, choices=choices, source_edges=tree.edges(source), **check,
                           steps=steps, template=ti, composed_minor=tree.validate_minor(source,target,composed),
                           source_obstruction=tree.topology_on_source(source,target,composed,witness)))
    return result


def cyclic_branch_controls(tree_saved):
    controls = []
    for kind in ('triangle', 'split', 'nested', 'square', 'lollipop'):
        row = next(r for r in tree_saved['templates'] if r['kind'] == kind)
        source, _ = tree.make_graph(row['walk'], row['choices'])
        parent, b = next((v,b) for v in sorted(source) if v > Z for b in sorted(source[v]) if b < 5)
        c, h = Q[b], next(x for x in range(3) if x != Q[b])
        hb = next(x for x in ARC if Q[x] == h)
        root, x, y = range(max(source)+1, max(source)+4)
        source.remove_edge(parent,b)
        source.add_edges_from(((parent,root),(root,x),(root,y),(x,y),(root,hb)))
        source.add_edges_from((v,contact) for v in (x,y) for contact in (b,hb))
        check = criticality(source)
        target, walk, choices, branches, forcers = tree.normalize_tree(source)
        tree.criticality(target)
        ti = next(i for i,r in enumerate(tree_saved['templates']) if tuple(r['walk']) == walk and
                  json.dumps(r['choices']) == json.dumps(choices))
        witness = tree_saved['subdivisions'][tree_saved['templates'][ti]['subdivision']]
        controls.append(dict(kind=kind, source_edges=tree.edges(source), **check, forcers=forcers,
                             target_walk=walk, template=ti, minor=tree.validate_minor(source,target,branches),
                             source_obstruction=tree.topology_on_source(source,target,branches,witness)))
    return controls


def shorten_shared(form, choices):
    walk = form['walk']
    step = tree.reduction(walk)
    if step is None:
        return None
    new_walk, retained, interval = step
    mark = form.get('mark')
    new = dict(kind='shared', walk=new_walk, mark=retained.index(mark)) if mark in retained else dict(kind='tree', walk=new_walk)
    source = make_graph(form, choices)
    mapping = {6+i: 6+j for j, i in enumerate(retained)}
    branches = {v: [v] for v in range(5)}
    branches[Z] = [Z] + [6+i for i in range(retained[0])] + [6+i for i in range(retained[-1]+1, len(walk)-1)]
    for j, i in enumerate(retained):
        end = retained[j+1] if j+1 < len(retained) else i+1
        branches[6+j] = list(range(6+i, 6+end))
    if new['kind'] == 'shared':
        for k in (0, 1):
            old_v, new_v = 5+len(walk)+k, 5+len(new_walk)+k
            mapping[old_v] = new_v
            branches[new_v] = [old_v]
    new_choices = []
    old_leaf, new_leaf = max(skeleton(form)[0])+1, max(skeleton(new)[0])+1
    for v, c, bs in choices:
        if v in mapping:
            new_choices.append((mapping[v], c, bs))
            if c == D:
                branches[new_leaf] = [old_leaf]
                new_leaf += 1
        if c == D:
            old_leaf += 1
    target = make_graph(new, new_choices)
    return new, new_choices, target, branches, dict(interval=interval, minor=tree.validate_minor(source,target,branches))


def shared_controls(records, pool, tree_saved):
    controls, outcomes = [], Counter()
    for kind in ('triangle', 'split', 'nested', 'square', 'lollipop'):
        motif = next(w for k,w in tree.motifs() if k == kind)
        a = motif[1]
        walk = (D,a,D) + motif[1:] + (a,D)
        for mark in (0, 2+(len(motif)-2)//2):
            form = dict(kind='shared', walk=walk, mark=mark)
            _, bans = skeleton(form)
            choices = [opts[0] for opts in attachment_options(bans)]
            source = make_graph(form, choices)
            check = criticality(source)
            current, ch, target = form, choices, source
            composed = {v:[v] for v in source}
            steps = []
            while step := shorten_shared(current, ch):
                current, ch, target, branches, cert = step
                (criticality if current['kind'] == 'shared' else tree.criticality)(target)
                composed = tree.compose_minor(composed, branches)
                steps.append(dict(form=current, **cert))
            available = pool if current['kind'] == 'shared' else tree_saved['subdivisions']
            augmented = target.copy()
            augmented.add_edges_from((max(target)+1,b) for b in range(5))
            es = set(tree.edges(augmented))
            witness = next(w for w in available if {tuple(sorted(e)) for p in w['paths'] for e in zip(p,p[1:])} <= es)
            outcomes[current['kind']] += 1
            controls.append(dict(motif=kind, form=form, choices=choices, source_edges=tree.edges(source), **check,
                                 steps=steps, final_form=current, composed_minor=tree.validate_minor(source,target,composed),
                                 source_obstruction=tree.topology_on_source(source,target,composed,witness)))
    assert outcomes == dict(shared=4, tree=6), outcomes
    return controls


def build(saved):
    records, pool, counts, coverage = templates(saved)
    old = json.loads(TREE.read_text())
    long = long_controls(records, pool)
    cyclic = cyclic_branch_controls(old)
    shared = shared_controls(records, pool, old)
    names = ('c5_degree5_triangle_components', 'c5_degree5_tree_components', 'c5_k4_blocks',
             'c5_odd_join_cores', 'c5_disk_deletions', 'c5_cell_enumerator', 'local_closure', 'boundary_relations')
    local = local_controls()
    return dict(schema=1, scope='Paper one-triangle reduction; finite necessary lifts, no general degree-five or Lean theorem.',
                source_sha256={f'scripts/{n}.py':tree.digest(ROOT/'scripts'/f'{n}.py') for n in names},
                input_sha256={str(TREE.relative_to(ROOT)):tree.digest(TREE)}, local=local,
                templates=records, subdivisions=pool, coverage_sha256=coverage,
                long_controls=long, shared_controls=shared, cyclic_branch_controls=cyclic,
                summary=dict(forms=len(records), lifts=counts, subdivisions=len(pool),
                             arm_list_assignments=local['arm_list_assignments'], long_controls=len(long),
                             shortening_steps=sum(len(r['steps']) for r in long), cyclic_branch_controls=len(cyclic),
                             shared_controls=len(shared), shared_shortening_steps=sum(len(r['steps']) for r in shared)))


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
