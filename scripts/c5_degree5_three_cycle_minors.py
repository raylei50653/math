#!/usr/bin/env python3
"""R27: three shared odd cycles, repeated-arm source minors, saved R26 topology."""
import argparse
from collections import Counter
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

import networkx as nx
import c5_degree5_three_triangles as normal
import c5_degree5_odd_cycle_components as odd

triangle, tree = normal.triangle, normal.tree
Q, U, Z, D = normal.Q, normal.U, normal.Z, normal.D
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_three_cycle_minors/observations.json'
CYCLES = ([6, 8, 9], [6, 7, 10], [7, 11, 12])


def paths(form):
    result, nxt = {}, 13
    for side in ('left', 'right'):
        n = len(form[side])-1
        result[side] = [Z, *range(nxt, nxt+n)]
        nxt += n
    return result


def shorten(form, choices, side):
    walk = form[side]
    pair = next(((i,j) for i in range(len(walk)) for j in range(i+1,len(walk))
                 if walk[i] == walk[j]), None)
    if pair is None:
        return None
    i,j = pair
    new = dict(form, **{side:walk[:i]+walk[j:]})
    source = normal.make_graph(form,choices)
    sg,_ = normal.skeleton(form)
    tg,_ = normal.skeleton(new)
    old_paths,new_paths = paths(form),paths(new)
    mapping = {v:v for v in range(13)}
    branches = {v:[v] for v in range(13)}
    for name in ('left','right'):
        old = old_paths[name]
        retained = old[:i+1]+old[j+1:] if name == side else old
        for x,v in zip(retained[1:],new_paths[name][1:]):
            mapping[x] = v
            branches[v] = [x]
    branches[new_paths[side][i]].extend(old_paths[side][i+1:j+1])
    new_choices = []
    old_leaf,new_leaf = max(sg)+1,max(tg)+1
    for v,c,bs in choices:
        if v in mapping:
            new_choices.append((mapping[v],c,bs))
            if c == D:
                branches[new_leaf] = [old_leaf]
                new_leaf += 1
        if c == D:
            old_leaf += 1
    target = normal.make_graph(new,new_choices)
    return new,new_choices,target,branches,tree.validate_minor(source,target,branches)


def graph_check(graph,lengths):
    assert graph.degree(Z) == 5
    assert set(graph[Z]) & set(range(5)) == {0,1,4}
    assert all(graph.degree(v) == 4 for v in graph if v > Z)
    inner = graph.subgraph([v for v in graph if v > Z])
    cycles = nx.cycle_basis(inner)
    assert nx.is_connected(inner) and sorted(map(len,cycles)) == sorted(lengths)
    assert sorted(len(set(a)&set(b)) for a,b in combinations(cycles,2)) == [0,1,1]
    assert {next(iter(set(a)&set(b))) for a,b in combinations(cycles,2)
            if set(a)&set(b)} == {6,7}
    vertices = sorted(graph)
    def witness(g,pins):
        w = normal.coloring(g,pins)
        if w is None:
            return None
        assert set(w) == set(g) and set(w.values()) <= U
        assert all(w[v] == c for v,c in pins.items())
        assert all(w[u] != w[v] for u,v in g.edges())
        return [w[v] for v in vertices]
    relaxed = graph.copy()
    relaxed.remove_edges_from((Z,b) for b in (0,1,4))
    rows = [witness(relaxed,dict(enumerate(Q)) | {Z:a}) for a in range(4)]
    assert [a for a,w in enumerate(rows) if w is None] == [D]
    assert witness(graph,dict(enumerate(Q))) is None
    deletions = []
    for e in tree.edges(graph):
        if e in tree.CYCLE:
            continue
        child = graph.copy()
        child.remove_edge(*e)
        w = witness(child,dict(enumerate(Q)))
        assert w is not None,e
        deletions.append(dict(edge=e,colors=w))
    return dict(vertices=vertices,edges=tree.edges(graph),degrees=[[v,graph.degree(v)] for v in vertices],
                lengths=lengths,z_colors=rows,deletions=deletions)


def selected(saved):
    buckets = {}
    for i,row in enumerate(saved['records']):
        f = row['form']
        key = (tuple(f['middle_palette']),f['left'][-1],f['right'][-1])
        buckets.setdefault(key,[]).append(i)
    assert len(buckets) == 24
    for key,indices in sorted(buckets.items()):
        indices.sort(key=lambda i:(len(saved['records'][i]['form']['left'])+
                                   len(saved['records'][i]['form']['right']),i))
        for size,i in zip(('short','long'),(indices[0],indices[-1])):
            yield size,i


def build():
    saved = json.loads(normal.OUT.read_text())
    for name,digest in saved['source_sha256'].items():
        assert tree.digest(ROOT/name) == digest,name
    records,counts = [],Counter()
    for size,index in selected(saved):
        for variant in range(2):
            form = dict(saved['records'][index]['form'])
            # Prefix, interior/suffix loops, including a whole D-to-D arm.
            for side in ('left','right'):
                w = list(form[side])
                i = 0 if variant == 0 else len(w)-1
                c = (w[i]+1+variant)%4
                w = w[:i]+[w[i],c]+w[i:]
                if variant == 1:
                    w = [D,(D+1)%4]+w
                form[side] = w
            _,bans = normal.skeleton(form)
            choices = [opts[(k+variant)%len(opts)] for k,opts in enumerate(triangle.attachment_options(bans))]
            base = normal.make_graph(form,choices)
            s = set(form['middle_palette'])
            palettes = (U-s,s,U-s)
            arcs = ((1,2,2),(2,1,4),(3,4,2))
            source = base
            expansions = []
            for k in range(3):
                arc = arcs[(k+variant)%3]
                expanded,_,cycle_paths = odd.expand_cycle(source,CYCLES[k],palettes[k],arc,variant+k)
                expansions.append(dict(vertices=sorted(set(expanded)-set(source)),paths=cycle_paths,length=sum(arc)))
                source = expanded
            graphs,checks = {},{}
            for mask in range(8):
                vertices = set(base)
                for k,e in enumerate(expansions):
                    if mask & (1<<k):
                        vertices.update(e['vertices'])
                graph = source.subgraph(vertices).copy()
                for k,cycle in enumerate(CYCLES):
                    if not mask & (1<<k):
                        graph.add_edges_from(zip(cycle,cycle[1:]+cycle[:1]))
                graphs[mask] = graph
                lengths = [e['length'] if mask & (1<<k) else 3 for k,e in enumerate(expansions)]
                checks[mask] = graph_check(graph,lengths)
            assert tree.edges(graphs[0]) == tree.edges(base)
            steps,branch_maps = [],{}
            for mask in range(1,8):
                for k,e in enumerate(expansions):
                    if not mask & (1<<k):
                        continue
                    child = mask ^ (1<<k)
                    branches = {v:[v] for v in graphs[child]}
                    for path in e['paths']:
                        branches[path[0]].extend(path[1:-1])
                    branch_maps[mask,k] = branches
                    steps.append(dict(before=mask,after=child,cycle=k,
                        minor=tree.validate_minor(graphs[mask],graphs[child],branches)))
            cycle_composed = None
            for order in permutations(range(3)):
                mask,composed = 7,{v:[v] for v in source}
                for k in order:
                    composed = tree.compose_minor(composed,branch_maps[mask,k])
                    mask ^= 1<<k
                assert cycle_composed is None or composed == cycle_composed
                cycle_composed = composed
            assert cycle_composed[Z] == [Z]
            assert all(set(cycle_composed[v]) & set(base) == {v} for v in base)
            current,current_choices,target = form,choices,base
            composed = cycle_composed
            arm_steps = []
            for side in ('left','right'):
                while step := shorten(current,current_choices,side):
                    current,current_choices,target,branches,cert = step
                    composed = tree.compose_minor(composed,branches)
                    arm_steps.append(dict(side=side,form=current,choices=current_choices,minor=cert,
                                          graph=graph_check(target,[3,3,3])))
            target_index = next(i for i,row in enumerate(saved['records']) if row['form'] == current)
            _,target_bans = normal.skeleton(current)
            options = triangle.attachment_options(target_bans)
            assert len(current_choices) == len(options)
            assert all(choice in opts for choice,opts in zip(current_choices,options))
            witness = odd.subdivision_for(target,saved['subdivisions'])
            records.append(dict(seed_template=index,target_template=target_index,size=size,variant=variant,form=form,choices=choices,
                expansions=expansions,graphs=[dict(mask=m,**checks[m]) for m in range(8)],
                cycle_steps=steps,cycle_orders=[list(p) for p in permutations(range(3))],
                cycle_composed=tree.validate_minor(source,base,cycle_composed),
                arm_steps=arm_steps,target_form=current,target_choices=current_choices,
                composed_minor=tree.validate_minor(source,target,composed),target_subdivision=witness,
                source_obstruction=tree.topology_on_source(source,target,composed,witness)))
            counts['sources'] += 1
            counts['cycle_step_minors'] += len(steps)
            counts['cycle_orders'] += 6
            counts['arm_step_minors'] += len(arm_steps)
            all_checks = list(checks.values())+[step['graph'] for step in arm_steps]
            counts['graph_stages'] += len(all_checks)
            counts['z_queries'] += 4*len(all_checks)
            counts['deletion_colorings'] += sum(len(c['deletions']) for c in all_checks)
            if len(records)%12 == 0:
                print(f'sources={len(records)}',flush=True)
    files = {Path(__file__).resolve()}
    files.update(Path(m.__file__).resolve() for m in list(sys.modules.values())
                 if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent == ROOT/'scripts')
    return dict(schema=1,scope='Three shared odd-cycle chain with terminal private arms; fixed-q source minors. Paper plus finite certificates, not general three-cycle exclusion or Lean/full Sigma.',
        source_sha256={str(p.relative_to(ROOT)):tree.digest(p) for p in sorted(files)},
        input_sha256={str(normal.OUT.relative_to(ROOT)):tree.digest(normal.OUT)},
        networkx_version=nx.__version__,summary=dict(counts,selected_seeds=48),records=records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    def forbidden(*args,**kwargs):
        raise AssertionError('planarity oracle forbidden')
    nx.check_planarity = nx.is_planar = forbidden
    nx.algorithms.planarity.check_planarity = forbidden
    nx.algorithms.planarity.get_counterexample = forbidden
    result = build()
    data = json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n'
    if args.check:
        assert OUT.read_text() == data,'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'],indent=2))


if __name__ == '__main__':
    main()
