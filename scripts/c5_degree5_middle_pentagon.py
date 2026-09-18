#!/usr/bin/env python3
"""R29: C3-C5-C3 with two distinct contacts on the middle pentagon.

Generation discovers subdivisions; --check validates saved paths only.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

import networkx as nx
import c5_degree5_triangle_components as triangle
import c5_degree5_tree_components as tree
import c5_degree5_bridge_arms as arms
from c5_k4_blocks import CYCLE, Q, U, coloring
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_middle_pentagon/observations.json'
D, Z = 3, 5


def positions():
    # Rotate the first cut to slot zero. Contacts are ordered by slot;
    # ordered arm pairs retain every assignment. No reflection quotient.
    for second_cut in range(1, 5):
        for contacts in combinations([i for i in range(1, 5) if i != second_cut], 2):
            yield second_cut, contacts


def forms():
    for second_cut, contacts in positions():
        for s in tree.PAIRS:
            walks = [w for c in sorted(U-s) for w in triangle.simple_walks(c)]
            for left, right in product(walks, repeat=2):
                yield dict(second_cut=second_cut, contacts=contacts,
                           middle_palette=sorted(s), left=left, right=right)


def skeleton(form):
    s = set(form['middle_palette'])
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((Z, b) for b in (0, 1, 4))
    # Middle cycle slots 0..4 are vertices 6..10; terminal private points 11..14.
    cut = 6+form['second_cut']
    graph.add_edges_from((6+i, 6+(i+1)%5) for i in range(5))
    for block in ((6,11,12), (cut,13,14)):
        graph.add_edges_from(combinations(block, 2))
    bans = {v: set(U-s) for v in range(6,11)}
    bans[6], bans[cut] = set(), set()
    bans.update({v:set(s) for v in range(11,15)})
    nxt = 15
    for slot, side in zip(form['contacts'], ('left','right')):
        endpoint = 6+slot
        walk = form[side]
        bans[endpoint].remove(walk[-1])
        last = Z
        for a, b in zip(walk, walk[1:]):
            graph.add_edge(last, nxt)
            bans[nxt] = U-{a,b}
            last, nxt = nxt, nxt+1
        graph.add_edge(last, endpoint)
    return graph, bans


def make_graph(form, choices):
    graph, _ = skeleton(form)
    nxt = max(graph)+1
    for v, c, bs in choices:
        if c == D:
            graph.add_edge(v, nxt)
            graph.add_edges_from((nxt,b) for b in bs)
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
    assert len(cycles) == 3 and sorted(map(len, cycles)) == [3,3,5]
    assert sorted(len(set(a)&set(b)) for a,b in combinations(cycles,2)) == [0,1,1]
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z,b) for b in (0,1,4))
    ws = [coloring(relaxed,dict(enumerate(Q)) | {Z:a}) for a in range(4)]
    assert [a for a,w in enumerate(ws) if w is None] == [D]
    assert coloring(graph,dict(enumerate(Q))) is None
    deletions = []
    def verify(g,w,pins):
        assert w is not None and set(w) == set(g)
        assert all(c in U for c in w.values())
        assert all(w[v] == c for v,c in pins.items())
        assert all(w[u] != w[v] for u,v in g.edges())
    for a,w in enumerate(ws):
        if w is not None:
            verify(relaxed,w,dict(enumerate(Q)) | {Z:a})
    for e in tree.edges(graph):
        if e in CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        w = coloring(child,dict(enumerate(Q)))
        verify(child,w,dict(enumerate(Q)))
        deletions.append(dict(edge=e,coloring=[w[v] for v in sorted(graph)]))
    return dict(z_colorings=[None if w is None else [w[v] for v in sorted(graph)] for w in ws],
                q_deletions=deletions)


def topology_layout(form):
    base, bans = skeleton(form)
    options = triangle.attachment_options(bans)
    graph = make_graph(form, [opts[0] for opts in options])
    fixed, variables = set(tree.edges(graph)), []
    leaf = max(base)+1
    for oi, opts in enumerate(options):
        v, color, _ = opts[0]
        endpoint = leaf if color == D else v
        if len(opts) == 2:
            assert color in (1,D)
            pair = [(1,endpoint), (3,endpoint)]
            assert pair[0] in fixed and pair[1] not in fixed
            # Each variable is an independent same-color boundary-edge swap.
            alternate = [o[0] for o in options]
            alternate[oi] = opts[1]
            assert set(tree.edges(make_graph(form,alternate))) == (set(tree.edges(graph))-{pair[0]}) | {pair[1]}
            fixed.remove(pair[0])
            variables.append(pair)
        else:
            assert len(opts) == 1
        if color == D:
            leaf += 1
    fixed.update((b,max(graph)+1) for b in range(5))
    literals = {e:(i,bit) for i,pair in enumerate(variables) for bit,e in enumerate(pair)}
    assert len(literals) == 2*len(variables) and not fixed.intersection(literals)
    return fixed, variables, literals


def build(saved):
    pool = [] if saved is None else saved['subdivisions']
    pool_edges = [{tuple(sorted(e)) for p in w['paths'] for e in zip(p,p[1:])} for w in pool]
    rows, counts, digest = [], Counter(), sha256()
    cube_queries = arms.cube_controls()
    assert len(list(positions())) == 12
    for index,form in enumerate(forms()):
        _,bans = skeleton(form)
        options = triangle.attachment_options(bans)
        first = [opts[0] for opts in options]
        rep = make_graph(form,first)
        semantics = criticality(rep)
        fixed, variables, literals = topology_layout(form)
        pending, refs = [{}], []
        replay = iter(saved['records'][index]['subdivisions']) if saved is not None else None
        while pending:
            cube = pending[0]
            es = fixed | {pair[cube.get(i,0)] for i,pair in enumerate(variables)}
            if replay is not None:
                wi = next(replay)
                assert pool_edges[wi] <= es
            else:
                wi = next((i for i,edges in enumerate(pool_edges) if edges <= es),None)
                if wi is None:
                    witness = kuratowski_certificate(nx.Graph(sorted(es)))
                    wi = len(pool)
                    pool.append(witness)
                    pool_edges.append(tree.validate_subdivision(nx.Graph(sorted(es)),witness))
            required = {}
            for e in sorted(pool_edges[wi]-fixed):
                assert e in literals
                i,bit = literals[e]
                assert i not in required or required[i] == bit
                required[i] = bit
            tree.validate_subdivision(nx.Graph(sorted(fixed | pool_edges[wi])),pool[wi])
            pending = [part for old in pending for part in arms.subtract(old,required)]
            refs.append(wi)
        if replay is not None:
            assert next(replay,None) is None
        lifts = 2**len(variables)
        digest.update(json.dumps([form,sorted(fixed),variables,refs]).encode())
        rows.append(dict(form=form,lifts=lifts,binary_variables=len(variables),
                         subdivisions=refs,representative_choices=first,**semantics))
        counts['forms'] += 1
        counts['wirings'] += lifts
        counts['z_queries'] += 4
        counts['deletion_colorings'] += len(semantics['q_deletions'])
        counts['cover_cubes'] += len(refs)
        if (index+1)%400 == 0:
            print(f'forms={index+1} wirings={counts["wirings"]} subdivisions={len(pool)}',flush=True)
    assert len(rows) == 12*408
    if saved is not None:
        assert len(saved['records']) == len(rows)
    files = {Path(__file__).resolve()}
    files.update(Path(m.__file__).resolve() for m in list(sys.modules.values())
                 if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent == ROOT/'scripts')
    return dict(schema=1,scope='C3-C5-C3, two distinct middle private contacts; all 12 slot configurations and simple-arm necessary normal forms. No long-cycle source minor or full Sigma claim.',
        source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(files)},
        summary=dict(counts,positions=12,subdivisions=len(pool),cube_difference_queries=cube_queries),
        coverage_sha256=digest.hexdigest(),records=rows,subdivisions=pool)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    if args.check:
        def forbidden(*args,**kwargs):
            raise AssertionError('planarity oracle forbidden during replay')
        nx.check_planarity = nx.is_planar = forbidden
        nx.algorithms.planarity.check_planarity = forbidden
        nx.algorithms.planarity.get_counterexample = forbidden
    result = build(saved)
    data = json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'],indent=2))


if __name__ == '__main__':
    main()
