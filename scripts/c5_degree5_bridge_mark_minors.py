#!/usr/bin/env python3
"""Boundary-fixed marked-path minors and complete non-disk wiring covers.

Extends R18 without changing its artifacts. --check is read-only and verifies
saved subdivisions; it never calls a planarity oracle.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import networkx as nx

import c5_degree5_bridge_arms as arms
import c5_degree5_bridge_marks as marks
import c5_degree5_triangle_components as tri
import c5_degree5_tree_components as tree
from c5_k4_blocks import Q, U, coloring
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_bridge_mark_minors/observations.json'
INPUTS = [marks.OUT, tri.OUT, tree.OUT]
D, Z = 3, 5


def make_graph(form, choices):
    graph, bans = marks.skeleton(form)
    options = tri.attachment_options(bans)
    assert len(choices) == len(options)
    assert all((v, c, tuple(bs)) in opts for (v, c, bs), opts in zip(choices, options))
    nxt = max(graph)+1
    for v, c, bs in choices:
        if c == D:
            graph.add_edge(v, nxt)
            graph.add_edges_from((nxt, b) for b in bs)
            nxt += 1
        else:
            graph.add_edge(v, bs[0])
    return graph


def criticality(form, graph):
    assert graph.degree(Z) == 5
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    inner = graph.subgraph([v for v in graph if v > Z])
    cycles = nx.cycle_basis(inner)
    assert nx.is_connected(inner)
    assert len(cycles) == len(form['marks']) + (form['kind'] == 'one')
    assert all(len(c) == 3 for c in cycles)
    assert all(not set(a) & set(b) for a, b in combinations(cycles, 2))
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z, b) for b in (0, 1, 4))
    ws = [coloring(relaxed, dict(enumerate(Q)) | {Z: a}) for a in range(4)]
    assert [a for a, w in enumerate(ws) if w is None] == [D]
    deletions = []
    for e in tree.edges(graph):
        if e in tree.CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        w = coloring(child, dict(enumerate(Q)))
        assert w is not None, e
        deletions.append(dict(edge=e, colors=[w[v] for v in sorted(graph)]))
    return dict(z_colors=[None if w is None else [w[v] for v in sorted(graph)] for w in ws],
                deletions=deletions)


def topology_layout(form):
    skeleton, bans = marks.skeleton(form)
    options = tri.attachment_options(bans)
    graph = make_graph(form, [opts[0] for opts in options])
    assert graph.degree(Z) == 5 and all(graph.degree(v) == 4 for v in graph if v > Z)
    fixed, variables = set(tree.edges(graph)), []
    leaf = max(skeleton)+1
    for opts in options:
        v, color, _ = opts[0]
        endpoint = leaf if color == D else v
        if len(opts) == 2:
            assert color in (1, D)
            pair = [(1, endpoint), (3, endpoint)]
            assert pair[0] in fixed and pair[1] not in fixed
            fixed.remove(pair[0])
            variables.append(pair)
        else:
            assert len(opts) == 1
        if color == D:
            leaf += 1
    fixed.update((b, max(graph)+1) for b in range(5))
    literals = {e: (i, bit) for i, pair in enumerate(variables) for bit, e in enumerate(pair)}
    assert len(literals) == 2*len(variables) and not fixed.intersection(literals)
    return fixed, variables, literals


def witness_edges(witness):
    return {tuple(sorted(e)) for p in witness['paths'] for e in zip(p, p[1:])}


def templates(saved, semantic_rows):
    pool = [] if saved is None else saved['subdivisions']
    pool_edges = list(map(witness_edges, pool))
    rows, fingerprint, totals = [], sha256(), Counter()
    for index, form in enumerate(marks.forms()):
        assert form == semantic_rows[index]['form']
        representative, choices = marks.make_graph(form)
        assert tree.edges(representative) == [tuple(e) for e in semantic_rows[index]['edges']]
        assert representative.edges == make_graph(form, choices).edges
        semantic = marks.semantics(representative)
        assert json.dumps(semantic, sort_keys=True) == json.dumps(
            {key: semantic_rows[index][key] for key in semantic}, sort_keys=True)
        fixed, variables, literals = topology_layout(form)
        pending, refs = [{}], []
        replay = iter(saved['templates'][index]['subdivisions']) if saved is not None else None
        while pending:
            cube = pending[0]
            es = fixed | {pair[cube.get(i, 0)] for i, pair in enumerate(variables)}
            if replay is not None:
                wi = next(replay)
                assert pool_edges[wi] <= es
            else:
                wi = next((i for i, edges in enumerate(pool_edges) if edges <= es), None)
                if wi is None:
                    witness = kuratowski_certificate(nx.Graph(sorted(es)))
                    wi = len(pool)
                    pool.append(witness)
                    pool_edges.append(tree.validate_subdivision(nx.Graph(sorted(es)), witness))
            required = {}
            for e in pool_edges[wi]-fixed:
                assert e in literals
                i, bit = literals[e]
                assert i not in required or required[i] == bit
                required[i] = bit
            tree.validate_subdivision(nx.Graph(sorted(fixed | pool_edges[wi])), pool[wi])
            pending = [part for old in pending for part in arms.subtract(old, required)]
            refs.append(wi)
        if replay is not None:
            assert next(replay, None) is None
        row = dict(form=form, binary_variables=len(variables), lifts=2**len(variables), subdivisions=refs)
        if saved is not None:
            assert row == saved['templates'][index]
        rows.append(row)
        totals[form['kind']+'_forms'] += 1
        totals[form['kind']+'_lifts'] += row['lifts']
        totals['cubes'] += len(refs)
        fingerprint.update(json.dumps([form, sorted(fixed), variables, refs]).encode())
        if (index+1) % 200 == 0:
            print(f'forms={index+1} subdivisions={len(pool)}', flush=True)
    assert len(rows) == len(semantic_rows) == 1044
    if saved is not None:
        assert len(rows) == len(saved['templates'])
    return rows, pool, dict(totals), fingerprint.hexdigest()


def paths_and_gadgets(form):
    if form['kind'] == 'one':
        n, m = len(form['left'])-1, len(form['right'])-1
        paths = dict(left=list(range(9, 9+n)), right=list(range(9+n, 9+n+m)))
        first_private = 9+n+m
    else:
        n = len(form['walk'])-1
        paths = dict(walk=list(range(6, 6+n)))
        first_private = 6+n
    gadgets = {mark: [first_private+2*i, first_private+2*i+1]
               for i, mark in enumerate(form['marks'])}
    return paths, gadgets


def shortening(walk, closed):
    if closed:
        step = tree.reduction(walk)
        return None if step is None else (list(step[0]), step[1], step[2])
    interval = next(((i, j) for i in range(len(walk)) for j in range(i+1, len(walk))
                     if walk[i] == walk[j]), None)
    if interval is None:
        return None
    i, j = interval
    return walk[:i]+walk[j:], list(range(i))+list(range(j, len(walk)-1)), interval


def shorten(form, choices, side):
    step = shortening(form[side], side == 'walk')
    if step is None:
        return None
    walk, retained, interval = step
    marked_side = 'left' if form['kind'] == 'one' else 'walk'
    new_marks = ([k for k, i in enumerate(retained) if i in form['marks']]
                 if side == marked_side else form['marks'])
    new = dict(form, **{side: walk, 'marks': new_marks})
    if side == 'walk':
        new['motif'] = tree.MOTIFS.get(tuple(walk), 'long')
    source = make_graph(form, choices)
    old_paths, old_gadgets = paths_and_gadgets(form)
    new_paths, new_gadgets = paths_and_gadgets(new)
    branches = {v: [v] for v in range(9 if form['kind'] == 'one' else 6)}
    mapping = {v: v for v in branches}
    for name, old in old_paths.items():
        kept = retained if name == side else list(range(len(old)))
        for k, i in enumerate(kept):
            v = new_paths[name][k]
            mapping[old[i]] = v
            end = kept[k+1] if k+1 < len(kept) else len(old)
            branches[v] = old[i:end]
        branches[Z].extend(old[:kept[0]] if kept else old)
    kept_marks = retained if side == marked_side else list(range(len(form[marked_side])-1))
    for new_mark in new_marks:
        old_mark = kept_marks[new_mark]
        for old_v, v in zip(old_gadgets[old_mark], new_gadgets[new_mark]):
            mapping[old_v] = v
            branches[v] = [old_v]
    new_choices = []
    old_leaf, new_leaf = max(marks.skeleton(form)[0])+1, max(marks.skeleton(new)[0])+1
    for v, c, bs in choices:
        if v in mapping:
            new_choices.append((mapping[v], c, bs))
            if c == D:
                branches[new_leaf] = [old_leaf]
                new_leaf += 1
        if c == D:
            old_leaf += 1
    target = make_graph(new, new_choices)
    for name in old_paths:
        kept = retained if name == side else range(len(form[name])-1)
        assert all({new[name][k], new[name][k+1]} == {form[name][i], form[name][i+1]}
                   for k, i in enumerate(kept))
    cert = tree.validate_minor(source, target, branches)
    removed_marks = sorted(set(form['marks'])-set(kept_marks))
    assert all(v in cert['deleted_vertices'] for mark in removed_marks for v in old_gadgets[mark])
    return new, new_choices, target, branches, dict(side=side, interval=interval,
           removed_marks=removed_marks, minor=cert)


def long_forms():
    # Six palettes, every marked step in a seven-step left arm, and a long right arm.
    for palette in tree.PAIRS:
        end = min(U-palette-{D})
        base = list(max(tri.simple_walks(end), key=len))
        left = [D, base[1], D]+base[1:]
        left = left[:3]+[left[3], left[2]]+left[3:]
        right = [D, base[1], D]+base[1:]
        for mark in range(len(left)-1):
            yield dict(kind='one', palette=sorted(palette), left=left, right=right, marks=[mark])
        if D not in palette:
            # The whole marked arm disappears into z; the surviving triangle
            # becomes directly adjacent to z, with no arm vertex left.
            for mark in (0, 1):
                yield dict(kind='one', palette=sorted(palette), left=[D, end, D],
                           right=base, marks=[mark])
    # All thirty colored motifs, with prefix/internal/suffix contractions.
    # Select marks by their actual step identity, exercising 0/1/2 survivors.
    for name, motif in tree.motifs():
        a = motif[1]
        walk = [D, a, D]+list(motif[1:])+[a, D]
        b = next(c for c in range(3) if c != a)
        walk = walk[:2]+[b, a]+walk[2:]
        current, retained = walk, list(range(len(walk)-1))
        while step := shortening(current, True):
            current, kept, _ = step
            retained = [retained[i] for i in kept]
        removed = sorted(set(range(len(walk)-1))-set(retained))
        adjacent = next(((i, i+1) for i in retained if i+1 in retained), (0, 1))
        pairs = {tuple(sorted(p)) for p in ((retained[0], retained[-1]),
                 (removed[0], retained[0]), (removed[0], removed[1]),
                 (removed[0], removed[-1]), adjacent)}
        for pair in sorted(pairs):
            yield dict(kind='two', motif=name, walk=walk, marks=list(pair))


def long_controls(pool, lower_pools):
    controls, outcomes, events = [], Counter(), Counter()
    available = pool + lower_pools
    available_edges = list(map(witness_edges, available))
    for index, form in enumerate(long_forms()):
        _, bans = marks.skeleton(form)
        choices = [opts[(index+i) % len(opts)] for i, opts in enumerate(tri.attachment_options(bans))]
        source = make_graph(form, choices)
        source_check = criticality(form, source)
        current, ch, target = form, choices, source
        composed, steps = {v: [v] for v in source}, []
        for side in (('left', 'right') if form['kind'] == 'one' else ('walk',)):
            while step := shorten(current, ch, side):
                previous_marks = current['marks']
                current, ch, target, branches, cert = step
                check = criticality(current, target)
                composed = tree.compose_minor(composed, branches)
                events['removed_'+str(len(cert['removed_marks']))+'_marks'] += 1
                events['prefix_into_z' if cert['interval'][0] == 0 else 'internal_or_suffix'] += 1
                if any(b == a+1 for a, b in zip(previous_marks, previous_marks[1:])):
                    events['adjacent_marks_at_source'] += 1
                if side != 'walk' and len(current[side]) == 1:
                    events['whole_arm_into_z'] += 1
                steps.append(dict(form=current, choices=ch, edges=tree.edges(target), **cert, **check))
        augmented = target.copy()
        augmented.add_edges_from((b, max(target)+1) for b in range(5))
        es = set(tree.edges(augmented))
        wi = next(i for i, edges in enumerate(available_edges) if edges <= es)
        tree.validate_subdivision(augmented, available[wi])
        outcomes[form['kind']+'_remaining_'+str(len(current['marks']))] += 1
        controls.append(dict(form=form, choices=choices, source_edges=tree.edges(source), **source_check,
                             steps=steps, target_form=current,
                             composed_minor=tree.validate_minor(source, target, composed),
                             source_obstruction=tree.topology_on_source(source, target, composed, available[wi])))
    assert set(outcomes) == {'one_remaining_0', 'one_remaining_1', 'two_remaining_0',
                             'two_remaining_1', 'two_remaining_2'}
    assert all(events['removed_'+str(n)+'_marks'] for n in range(3))
    assert events['prefix_into_z'] and events['adjacent_marks_at_source'] and events['whole_arm_into_z']
    return controls, dict(outcomes), dict(events)


def build(saved):
    inputs = [json.loads(p.read_text()) for p in INPUTS]
    # Check the R18 code provenance before independently recomputing its rows.
    for source, digest in inputs[0]['source_sha256'].items():
        assert tree.digest(ROOT/source) == digest
    cube_queries = arms.cube_controls()
    rows, pool, totals, fingerprint = templates(saved, inputs[0]['templates'])
    controls, outcomes, events = long_controls(pool, inputs[1]['subdivisions']+inputs[2]['subdivisions'])
    names = ('c5_degree5_bridge_mark_minors', 'c5_degree5_bridge_marks', 'c5_degree5_bridge_arms',
             'c5_degree5_bridge_triangles', 'c5_degree5_triangle_components', 'c5_degree5_tree_components',
             'c5_k4_blocks', 'c5_odd_join_cores', 'c5_disk_deletions', 'c5_cell_enumerator',
             'local_closure', 'boundary_relations')
    return dict(schema=1, scope='Disjoint triangle blocks with at least one coincident arm/bridge root; fixed q and specified boundary arc.',
                source_sha256={f'scripts/{n}.py': tree.digest(ROOT/'scripts'/f'{n}.py') for n in names},
                input_sha256={str(p.relative_to(ROOT)): tree.digest(p) for p in INPUTS},
                networkx_version=nx.__version__, cube_difference_queries=cube_queries,
                templates=rows, subdivisions=pool, ordered_cover_sha256=fingerprint, long_controls=controls,
                summary=dict(**totals, subdivisions=len(pool), long_sources=len(controls),
                             shortening_steps=sum(len(r['steps']) for r in controls),
                             outcomes=outcomes, events=events, disk=0))


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
