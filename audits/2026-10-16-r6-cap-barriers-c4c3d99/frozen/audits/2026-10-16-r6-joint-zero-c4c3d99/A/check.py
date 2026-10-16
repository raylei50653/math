#!/usr/bin/env python3
"""Independent replay of existing labelled controls for the new parity obstruction.
No third-party dependencies; no source graphs are generated or asserted.
"""
import argparse
from collections import Counter, deque
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'frozen/audits/2026-10-15-three-edge-matchings-6ddea32/graphs.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def primal_dual(g):
    vertices, edges, triangles = g['J_vertices'], g['J_edges'], g['J_faces']
    require(len(vertices) == len(set(vertices)), 'duplicate primal vertex')
    require(len(edges) == len({tuple(sorted(e)) for e in edges}), 'duplicate primal edge')
    require(all(len(t) == len(set(t)) == 3 for t in triangles), 'nontriangle')
    incidence = {tuple(sorted(e)): [] for e in edges}
    for i, t in enumerate(triangles):
        for j in range(3):
            incidence[tuple(sorted((t[j], t[(j+1) % 3])))].append(i)
    require(all(len(fs) == 2 for fs in incidence.values()), 'not a closed triangulation')
    qedges = [incidence[tuple(sorted(e))] for e in edges]
    require(len(vertices)-len(edges)+len(triangles) == 2, 'not sphere Euler')
    qfaces = {}
    for u in vertices:
        faces = {i for i,t in enumerate(triangles) if u in t}
        around = {i: [] for i in faces}
        for k, edge in enumerate(edges):
            if u in edge:
                i,j = qedges[k]; around[i].append(j); around[j].append(i)
        require(all(len(vs) == 2 for vs in around.values()), 'nonmanifold primal link')
        root = min(faces); cycle=[root]; previous=None; current=root
        while True:
            nxt = next(v for v in around[current] if v != previous)
            if nxt == root: break
            require(nxt not in cycle, 'premature link cycle')
            cycle.append(nxt); previous,current=current,nxt
        require(set(cycle) == faces, 'disconnected primal link')
        qfaces[u]=cycle
    # Orient all triangles consistently across every edge. Together with
    # connected vertex links and Euler=2 this checks the supplied sphere.
    oriented = {0: 1}; todo=deque([0])
    while todo:
        i=todo.popleft(); tri=triangles[i]
        for j in range(3):
            uv=(tri[j],tri[(j+1)%3]); fs=incidence[tuple(sorted(uv))]
            other=next(k for k in fs if k != i); ot=triangles[other]
            same=any((ot[k],ot[(k+1)%3]) == uv for k in range(3))
            sign=-oriented[i] if same else oriented[i]
            if other in oriented: require(oriented[other] == sign, 'nonorientable')
            else: oriented[other]=sign; todo.append(other)
    require(len(oriented) == len(triangles), 'disconnected surface')
    degrees=Counter(u for e in edges for u in e)
    marks=[next(i for i,e in enumerate(edges) if set(e) == set(mark))
           for mark in g['marked_original_edges']]
    return len(triangles), qedges, qfaces, degrees, marks


def matching_count(vertices, edges):
    neighbours={v: [] for v in vertices}
    for u,v in edges:
        if u in neighbours and v in neighbours:
            neighbours[u].append(v); neighbours[v].append(u)
    def visit(free):
        if not free: return 1
        u=min(free)
        return sum(visit(free-{u,v}) for v in neighbours[u] if v in free)
    return visit(set(vertices))


def residual_rows(n, edges, forced, forbidden):
    X={v for i in forced for v in edges[i]}
    V=sorted(set(range(n))-X)
    hedges=[(u,v) for i,(u,v) in enumerate(edges)
            if i != forbidden and u not in X and v not in X]
    adj={u:set() for u in V}
    for u,v in hedges: adj[u].add(v); adj[v].add(u)
    barriers=[]; maximum=-1
    for mask in range(1 << len(V)):
        S={v for i,v in enumerate(V) if mask >> i & 1}
        unseen=set(V)-S; components=[]
        while unseen:
            root=min(unseen); unseen.remove(root); comp={root}; todo=[root]
            while todo:
                for v in adj[todo.pop()] & unseen:
                    unseen.remove(v); comp.add(v); todo.append(v)
            components.append(sorted(comp))
        deficiency=sum(len(c)%2 for c in components)-len(S)
        if deficiency > 0:
            maximum=max(maximum,len(S))
            barriers.append({'S':sorted(S),'components':components,'deficiency':deficiency})
    pm=matching_count(V,hedges)
    require((pm == 0) == bool(barriers), 'independent PM/Tutte mismatch')
    return X, pm, [b for b in barriers if len(b['S']) == maximum], len(barriers), 1 << len(V)


def build():
    data=json.loads(INPUT.read_text()); controls=[]
    for g in data:
        planar='J_vertices' in g
        if planar:
            n,edges,qfaces,degrees,marks=primal_dual(g)
            pins=g['pins']; T=set(pins.values())
            require(len(T) == 6, 'pins are not six distinct original vertices')
            unmarked_odd=sorted(u for u in g['J_vertices'] if u not in T and degrees[u]%2)
            unmarked_five=sorted(u for u in g['J_vertices'] if u not in T and degrees[u] == 5)
            degree_domain=(degrees[pins['m']] >= 7 and degrees[pins['z']] >= 6
                           and all(degrees[pins[s]] >= 4 for s in ['v','w','p','q'])
                           and all(degrees[u] >= 5 for u in g['J_vertices'] if u not in T))
            require(sum(6-degrees[u] for u in g['J_vertices']) == 12, 'curvature failed')
            if degree_domain:
                t4=sum(degrees[pins[s]] == 4 for s in ['v','w','p','q'])
                t5=sum(degrees[pins[s]] == 5 for s in ['v','w','p','q'])
                excess=sum(max(degrees[u]-6,0) for u in g['J_vertices'])
                require(len(unmarked_five) == 12+excess-2*t4-t5, 'source curvature identity')
                require(len(unmarked_five) >= 5, 'source curvature lower bound')
        else:
            n,edges,marks=g['Q_n'],g['Q_edges'],g['marks']
            degree_domain=False; unmarked_odd=unmarked_five=None
        families={}
        for label,forced,forbidden in [('110',marks[:2],marks[2]),('101',[marks[0],marks[2]],marks[1])]:
            X,pm,barriers,total,subsets=residual_rows(n,edges,forced,forbidden)
            Xedges=[i for i,(u,v) in enumerate(edges) if u in X and v in X]
            induced=set(Xedges) == set(forced) and len(X) == 4
            singles=[]
            for b in barriers:
                if not all(len(c) == 1 for c in b['components']): continue
                S=set(b['S']); I=set(range(n))-X-S
                tau=int(all(v in I for v in edges[forbidden]))
                B=[i for i,(u,v) in enumerate(edges)
                   if (u in S and v in S) or (u in S and v in X) or (v in S and u in X)]
                mono=[i for i,(u,v) in enumerate(edges) if (u in I) == (v in I)]
                expected=set(Xedges)|set(B)|({forbidden} if tau else set())
                require(set(mono) == expected, 'monochromatic decomposition failed')
                require(b['deficiency'] == 2, 'singleton deficiency not two')
                require(len(B) == 3-len(Xedges)+tau, 'exact singleton budget failed')
                row={**b,'tau':tau,'B':B,'monochromatic_edges':mono}
                if planar:
                    fdegree=Counter(u for i in mono for u in g['J_edges'][i])
                    require(all(fdegree[u]%2 == degrees[u]%2 for u in g['J_vertices']), 'face parity failed')
                    outside_endpoints=sorted({u for i in B for u in g['J_edges'][i] if u not in T})
                    require(set(unmarked_odd) <= set(outside_endpoints), 'unmarked odd coverage failed')
                    row.update({'unmarked_odd_vertices':unmarked_odd,'exceptional_endpoints_outside_T':outside_endpoints})
                    if induced: require(len(unmarked_odd) <= 4, 'new singleton exclusion violated')
                singles.append(row)
            lemma_domain=planar and induced and len(unmarked_odd) >= 5
            require(not (lemma_domain and singles), 'singleton barrier in new lemma domain')
            families[label]={'ordinary_matching_count':pm,'subsets_checked':subsets,
                             'total_Tutte_violating_sets':total,'maximum_barrier_count':len(barriers),
                             'induced_forced_pair':induced,'new_general_lemma_domain':lemma_domain,
                             'maximum_singleton_barriers':singles}
        controls.append({'name':g['name'],'sphere_embedding_supplied':planar,
                         'source_degree_premises':degree_domain,'actual_source_status':'not triggered',
                         'unmarked_degree_five_vertices':unmarked_five,
                         'unmarked_odd_vertices':unmarked_odd,'families':families})
    return {'schema':'r6-joint-zero-A-v1','input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),
            'theorem':'No all-singleton Tutte obstruction in either prescribed family under full source premises',
            'actual_sources_supplied':0,'controls':controls}


def main():
    parser=argparse.ArgumentParser(); group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path); group.add_argument('--check',type=Path)
    args=parser.parse_args(); expected=build()
    if args.output:
        with args.output.open('x') as stream: json.dump(expected,stream,indent=2); stream.write('\n')
        print('PASS independent control reconstruction; output exclusive-created')
    else:
        actual=json.loads(args.check.read_text())
        require(actual == expected, 'certificate differs from independently reconstructed full result')
        print('PASS independent full-certificate replay')
    print(json.dumps({'controls':len(expected['controls']), 'source_status':'not triggered',
                      'singleton_barriers':[len(f['maximum_singleton_barriers']) for c in expected['controls'] for f in c['families'].values()]}))

if __name__ == '__main__': main()
