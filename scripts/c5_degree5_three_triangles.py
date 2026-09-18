#!/usr/bin/env python3
"""R26: three shared triangles with an arm on each terminal triangle.

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
from c5_k4_blocks import CYCLE, Q, U, coloring
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_three_triangles/observations.json'
D, Z = 3, 5


def forms():
    for s in tree.PAIRS:
        walks = [w for c in sorted(s) for w in triangle.simple_walks(c)]
        for left, right in product(walks, repeat=2):
            yield dict(middle_palette=sorted(s), left=left, right=right)


def skeleton(form):
    s = set(form['middle_palette'])
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((Z, b) for b in (0, 1, 4))
    # Cut vertices 6,7; terminal contacts 8,11; palette anchors 9,10,12.
    for block in ((6,8,9), (6,7,10), (7,11,12)):
        graph.add_edges_from(combinations(block, 2))
    bans = {6:set(), 7:set(), 8:set(s), 9:set(s), 10:U-s, 11:set(s), 12:set(s)}
    nxt = 13
    for endpoint, side in ((8,'left'), (11,'right')):
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
    assert len(cycles) == 3 and all(len(c) == 3 for c in cycles)
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


def build(saved):
    pool = [] if saved is None else saved['subdivisions']
    pool_edges = [{tuple(sorted(e)) for p in w['paths'] for e in zip(p,p[1:])} for w in pool]
    rows, counts, digest = [], Counter(), sha256()
    for index,form in enumerate(forms()):
        _,bans = skeleton(form)
        options = triangle.attachment_options(bans)
        first = [opts[0] for opts in options]
        rep = make_graph(form,first)
        semantics = criticality(rep)
        inner_edges = set(tree.edges(rep.subgraph([v for v in rep if v >= Z])))
        boundary_colors = {v:sorted(Q[b] for b in rep[v] if b < 5) for v in rep if v >= Z}
        lifts = 0
        for choices in product(*options):
            graph = make_graph(form,choices)
            assert set(graph) == set(rep)
            assert graph.degree(Z) == 5 and all(graph.degree(v) == 4 for v in graph if v > Z)
            assert set(tree.edges(graph.subgraph([v for v in graph if v >= Z]))) == inner_edges
            assert all(sorted(Q[b] for b in graph[v] if b < 5) == cs for v,cs in boundary_colors.items())
            apex = max(graph)+1
            graph.add_edges_from((apex,b) for b in range(5))
            es = set(tree.edges(graph))
            wi = next((i for i,edges in enumerate(pool_edges) if edges <= es),None)
            if wi is None:
                assert saved is None, ('missing subdivision',index,choices)
                witness = kuratowski_certificate(graph)
                wi = len(pool)
                pool.append(witness)
                pool_edges.append(tree.validate_subdivision(graph,witness))
            tree.validate_subdivision(graph,pool[wi])
            digest.update(json.dumps([index,choices,tree.edges(graph),wi]).encode())
            lifts += 1
        rows.append(dict(form=form,lifts=lifts,representative_choices=first,**semantics))
        counts['forms'] += 1
        counts['wirings'] += lifts
        counts['z_queries'] += 4
        counts['deletion_colorings'] += len(semantics['q_deletions'])
        if saved is None and (index+1)%50 == 0:
            print(f'forms={index+1} wirings={counts["wirings"]} subdivisions={len(pool)}',flush=True)
    files = {Path(__file__).resolve()}
    files.update(Path(m.__file__).resolve() for m in list(sys.modules.values())
                 if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent == ROOT/'scripts')
    return dict(schema=1,scope='Three shared triangles, one arm on each terminal private point; simple-arm necessary normal forms. No long-cycle source minor or full Sigma claim.',
        source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(files)},
        summary=dict(counts,subdivisions=len(pool)),coverage_sha256=digest.hexdigest(),
        records=rows,subdivisions=pool)


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
    data = json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'],indent=2))


if __name__ == '__main__':
    main()
