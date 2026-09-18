#!/usr/bin/env python3
"""Disjoint triangles, distinct entry/exit vertices, and arbitrary outer arms.

Paper length reduction; finite topology certificate uses exact Boolean cubes.
--check verifies saved subdivisions and cube coverage, without planarity calls.
"""
import argparse
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

import networkx as nx

import c5_degree5_bridge_triangles as direct
import c5_degree5_triangle_components as triangle
import c5_degree5_tree_components as tree
from c5_k4_blocks import CYCLE, Q, U
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_bridge_arms/observations.json'
D, Z = 3, 5


def forms():
    for s, t in product(tree.PAIRS, repeat=2):
        left = [list(w) for d in sorted(U-s) for w in triangle.simple_walks(d)]
        right = [list(w) for d in sorted(U-t) for w in triangle.simple_walks(d)]
        for n in range(1, 5):
            for word in permutations(range(4), n):
                if word[0] in s or word[-1] in t:
                    continue
                for a, b in product(left, right):
                    yield dict(left=sorted(s), right=sorted(t), word=list(word), a=a, b=b)


def skeleton(form):
    s, t, word = set(form['left']), set(form['right']), form['word']
    assert word[0] not in s and word[-1] not in t
    assert all(a != b for a, b in zip(word, word[1:]))
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((Z, b) for b in (0, 1, 4))
    graph.add_edges_from(((6, 7), (7, 8), (8, 6), (9, 10), (10, 11), (11, 9)))
    paths = {'word': [6]+list(range(12, 11+len(word)))+[9]}
    graph.add_edges_from(zip(paths['word'], paths['word'][1:]))
    lists = {6: s | {word[0]}, 7: s | {form['a'][-1]}, 8: s,
             9: t | {word[-1]}, 10: t | {form['b'][-1]}, 11: t}
    lists.update({v: {a, b} for v, a, b in zip(paths['word'][1:-1], word, word[1:])})
    nxt = max(graph)+1
    for side, endpoint, palette in (('a', 7, s), ('b', 10, t)):
        walk = form[side]
        assert walk[0] == D and walk[-1] not in palette
        assert all(a != b for a, b in zip(walk, walk[1:]))
        inner = list(range(nxt, nxt+len(walk)-1))
        nxt += len(inner)
        paths[side] = [Z]+inner+[endpoint]
        graph.add_edges_from(zip(paths[side], paths[side][1:]))
        lists.update({v: {a, b} for v, a, b in zip(inner, walk, walk[1:])})
    return graph, {v: U-cs for v, cs in lists.items()}, paths


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


def message(walk, a):
    available = {a}
    for x, y in zip(walk, walk[1:]):
        available = {c for c in (x, y) if any(c != old for old in available)}
    return available


def root_message(s, c, walk, a):
    m = message(walk, a)
    private = {v for v in s | {walk[-1]} if any(v != x for x in m)}
    return {r for r, p, u in product(s | {c}, private, s) if len({r, p, u}) == 3}


def semantics(form):
    s, t = set(form['left']), set(form['right'])
    word = form['word']
    forbidden = []
    for a in range(4):
        left = root_message(s, word[0], form['a'], a)
        right = root_message(t, word[-1], form['b'], a)
        assert left == ({word[0]} if a == D else s | {word[0]})
        assert right == ({word[-1]} if a == D else t | {word[-1]})
        for x, y in zip(word, word[1:]):
            left = {c for c in (x, y) if any(c != old for old in left)}
        if not any(x != y for x, y in product(left, right)):
            forbidden.append(a)
    assert forbidden == [D]


def local_controls():
    count, fingerprint = 0, sha256()
    for s in tree.PAIRS:
        for d in sorted(U-s):
            for base in triangle.simple_walks(d):
                # Simple arms plus prefix and internal repeated-color controls.
                walks = [base, (D, (D+1) % 4, D)+base[1:]]
                if len(base) > 1:
                    walks.append(base[:1]+(base[1], base[0])+base[1:])
                for walk in walks:
                    for c, a in product(sorted(U-s), range(4)):
                        actual = set()
                        # Full tuples on the arm and triangle, not root elimination.
                        lists = [{x, y} for x, y in zip(walk, walk[1:])]
                        for colors in product(*lists, s | {c}, s | {d}, s):
                            arm, r, p, u = colors[:-3], *colors[-3:]
                            chain = (a,)+arm+(p,)
                            if all(x != y for x, y in zip(chain, chain[1:])) and len({r, p, u}) == 3:
                                actual.add(r)
                        expected = {c} if a == D else s | {c}
                        assert actual == expected == root_message(s, c, walk, a)
                        fingerprint.update(json.dumps([sorted(s), c, walk, a, sorted(actual)]).encode())
                        count += 1
    return dict(full_tuple_queries=count, sha256=fingerprint.hexdigest())


def topology_layout(form):
    """Every binary variable changes exactly one B-colored boundary edge."""
    _, bans, _ = skeleton(form)
    options = triangle.attachment_options(bans)
    first = [opts[0] for opts in options]
    graph = make_graph(form, first)
    assert graph.degree(Z) == 5 and all(graph.degree(v) == 4 for v in graph if v > Z)
    fixed = set(tree.edges(graph))
    variables = []
    leaf = max(skeleton(form)[0])+1
    for opts in options:
        v, color, _ = opts[0]
        endpoint = leaf if color == D else v
        if len(opts) == 2:
            assert color in (1, D)
            pair = [(1, endpoint), (3, endpoint)]
            assert pair[0] in fixed and pair[1] not in fixed
            fixed.remove(pair[0])
            variables.append(pair)
        if color == D:
            leaf += 1
    apex = max(graph)+1
    fixed.update((b, apex) for b in range(5))
    edge_literals = {edge: (i, bit) for i, pair in enumerate(variables) for bit, edge in enumerate(pair)}
    assert len(edge_literals) == 2*len(variables) and not fixed.intersection(edge_literals)
    return fixed, variables, edge_literals


def subtract(cube, covered):
    """Disjoint cubes partition cube minus covered; dictionaries fix Boolean bits."""
    if any(i in cube and cube[i] != bit for i, bit in covered.items()):
        return [cube]
    remainder, intersection = [], dict(cube)
    for i, bit in sorted(covered.items()):
        if i not in intersection:
            remainder.append(intersection | {i: 1-bit})
            intersection[i] = bit
    return remainder


def cube_controls():
    # Independent truth-table audit of the symbolic coverage operation.
    cubes = [dict((i, x) for i, x in enumerate(values) if x != 2)
             for values in product(range(3), repeat=4)]
    assignments = list(product(range(2), repeat=4))
    def points(cube):
        return {bits for bits in assignments if all(bits[i] == x for i, x in cube.items())}
    for a, b in product(cubes, repeat=2):
        pieces = list(map(points, subtract(a, b)))
        assert set().union(*pieces) == points(a)-points(b)
        assert sum(map(len, pieces)) == len(set().union(*pieces))
    return len(cubes)**2


def templates(saved):
    pool = [] if saved is None else saved['subdivisions']
    pool_edges = [{tuple(sorted(e)) for p in w['paths'] for e in zip(p, p[1:])} for w in pool]
    # A subdivision may omit the apex and the highest numbered leaf.
    # Its maximum label is only a lower bound on the source apex label.
    by_apex = {}
    for i, es in enumerate(pool_edges):
        by_apex.setdefault(max(v for e in es for v in e), []).append(i)
    rows, fingerprint, total, used_cubes = [], sha256(), 0, 0
    for index, form in enumerate(forms()):
        semantics(form)
        fixed, variables, literals = topology_layout(form)
        universe = fixed | set(literals)
        apex = max(v for e in universe for v in e)
        pending, refs = [{}], []
        replay = iter(saved['templates'][index]['subdivisions']) if saved is not None else None
        while pending:
            cube = pending[0]
            es = fixed | {pair[cube.get(i, 0)] for i, pair in enumerate(variables)}
            if replay is not None:
                wi = next(replay)
                assert pool_edges[wi] <= es
            else:
                wi = next((i for highest, indices in by_apex.items() if highest <= apex
                           for i in indices if pool_edges[i] <= es), None)
                if wi is None:
                    witness = kuratowski_certificate(nx.Graph(sorted(es)))
                    wi = len(pool)
                    pool.append(witness)
                    pool_edges.append(tree.validate_subdivision(nx.Graph(sorted(es)), witness))
                    by_apex.setdefault(max(v for e in pool_edges[-1] for v in e), []).append(wi)
            required = {}
            for e in pool_edges[wi]-fixed:
                assert e in literals
                i, bit = literals[e]
                assert i not in required or required[i] == bit
                required[i] = bit
            tree.validate_subdivision(nx.Graph(sorted(fixed | pool_edges[wi])), pool[wi])
            pending = [part for old in pending for part in subtract(old, required)]
            refs.append(wi)
        if replay is not None:
            assert next(replay, None) is None
        lifts = 2**len(variables)
        row = dict(form=form, binary_variables=len(variables), lifts=lifts, subdivisions=refs)
        if saved is not None:
            assert row == saved['templates'][index]
        rows.append(row)
        total += lifts
        used_cubes += len(refs)
        fingerprint.update(json.dumps([form, sorted(fixed), variables, refs]).encode())
        if (index+1) % 2000 == 0:
            print(f'forms={index+1} lifts={total} cubes={used_cubes} subdivisions={len(pool)}', flush=True)
    if saved is not None:
        assert len(rows) == len(saved['templates'])
    return rows, pool, total, used_cubes, fingerprint.hexdigest()


def shorten(form, choices, side):
    walk = form[side]
    interval = next(((i, j) for i in range(len(walk)) for j in range(i+1, len(walk))
                     if walk[i] == walk[j]), None)
    if interval is None:
        return None
    i, j = interval
    new = dict(form, **{side: walk[:i]+walk[j:]})
    source = make_graph(form, choices)
    sg, _, old_paths = skeleton(form)
    tg, _, new_paths = skeleton(new)
    mapping = {v: v for v in range(12)}
    branches = {v: [v] for v in range(12)}
    for name in ('word', 'a', 'b'):
        old = old_paths[name]
        retained = old[:i+1]+old[j+1:] if name == side else old
        for x, v in zip(retained, new_paths[name]):
            mapping[x] = v
            branches[v] = [x]
    branches[new_paths[side][i]].extend(old_paths[side][i+1:j+1])
    new_choices = []
    old_leaf, new_leaf = max(sg)+1, max(tg)+1
    for v, c, bs in choices:
        if v in mapping:
            new_choices.append((mapping[v], c, bs))
            if c == D:
                branches[new_leaf] = [old_leaf]
                new_leaf += 1
        if c == D:
            old_leaf += 1
    target = make_graph(new, new_choices)
    return new, new_choices, target, branches, tree.validate_minor(source, target, branches)


def long_controls(rows, pool):
    result = []
    for s, t in product(tree.PAIRS, repeat=2):
        row = next(r for r in rows if r['form']['left'] == sorted(s)
                   and r['form']['right'] == sorted(t) and len(r['form']['word']) >= 2
                   and len(r['form']['a']) >= 2 and len(r['form']['b']) >= 2)
        for variant in range(2):
            form = dict(row['form'])
            for side in ('a', 'b', 'word'):
                w = form[side]
                i = min(variant, len(w)-1)
                c = next(c for c in range(4) if c != w[i])
                form[side] = w[:i]+[w[i], c]+w[i:]
            _, bans, _ = skeleton(form)
            choices = [opts[variant % len(opts)] for opts in triangle.attachment_options(bans)]
            source = make_graph(form, choices)
            check = direct.criticality(source)
            current, current_choices, target = form, choices, source
            composed = {v: [v] for v in source}
            steps = []
            for side in ('a', 'b', 'word'):
                while step := shorten(current, current_choices, side):
                    current, current_choices, target, branches, cert = step
                    semantics(current)
                    direct.criticality(target)
                    composed = tree.compose_minor(composed, branches)
                    steps.append(dict(side=side, form=current, minor=cert))
            augmented = target.copy()
            augmented.add_edges_from((max(target)+1, b) for b in range(5))
            es = set(tree.edges(augmented))
            witness = next(w for w in pool if {tuple(sorted(e)) for p in w['paths']
                                              for e in zip(p, p[1:])} <= es)
            result.append(dict(form=form, choices=choices, source_edges=tree.edges(source), **check,
                               steps=steps, target_form=current, target_choices=current_choices,
                               composed_minor=tree.validate_minor(source, target, composed),
                               source_obstruction=tree.topology_on_source(source, target, composed, witness)))
    return result


def build(saved):
    local = local_controls()
    local['cube_difference_queries'] = cube_controls()
    rows, pool, lifts, cubes, fingerprint = templates(saved)
    controls = long_controls(rows, pool)
    names = ('c5_degree5_bridge_arms', 'c5_degree5_bridge_triangles', 'c5_degree5_triangle_components',
             'c5_degree5_tree_components', 'c5_k4_blocks', 'c5_odd_join_cores',
             'c5_disk_deletions', 'c5_cell_enumerator', 'local_closure', 'boundary_relations')
    return dict(schema=1, scope='Disjoint triangles with distinct entry and exit vertices; arbitrary arms and bridge path.',
                source_sha256={f'scripts/{name}.py': tree.digest(ROOT/'scripts'/f'{name}.py') for name in names},
                networkx_version=nx.__version__, local=local, templates=rows,
                subdivisions=pool, ordered_cover_sha256=fingerprint, long_controls=controls,
                summary=dict(templates=len(rows), lifts=lifts, cubes=cubes, subdivisions=len(pool),
                             long_sources=len(controls), shortening_steps=sum(len(r['steps']) for r in controls), disk=0))


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
