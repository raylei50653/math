#!/usr/bin/env python3
"""Independent residual/barrier review from original Q edges, no checker import."""
import itertools,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;OTHER=HERE.parent/'2026-10-15-three-edge-matchings-6ddea32'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def comps(vertices,adj):
    unseen=set(vertices);out=[]
    while unseen:
        v=max(unseen);unseen.remove(v);part={v};todo=[v]
        while todo:
            for w in adj[todo.pop()]&unseen:unseen.remove(w);part.add(w);todo.append(w)
        out.append(part)
    return out

def enumerate_pm(vertices,edges,banned=()):
    incident={v:[] for v in vertices}
    for k,(a,b) in enumerate(edges):
        if k in banned or a not in incident or b not in incident:continue
        incident[a].append((b,k));incident[b].append((a,k))
    out=[]
    def search(free,picked):
        if not free:out.append(tuple(sorted(picked)));return
        v=max(free)
        for w,k in reversed(incident[v]):
            if w in free:search(free-{v,w},picked+[k])
    search(set(vertices),[]);return sorted(out)

def main():
    cert=json.loads((OTHER/'certificate.json').read_text());result=[]
    for c in cert['controls']:
        n,edges=c['Q_n'],c['Q_edges'];allv=set(range(n));allpm=enumerate_pm(allv,edges)
        require(allpm==[tuple(m['edges']) for m in c['matchings']],'complete PM mismatch');weights=[]
        for M,m in zip(allpm,c['matchings']):
            adj=[set() for _ in range(n)]
            for k,(a,b) in enumerate(edges):
                if k not in M:adj[a].add(b);adj[b].add(a)
            factors=comps(allv,adj);weight=0 if any(len(p)%2 for p in factors) else 2**len(factors);weights.append(weight)
            require(weight==len(m['all_tait_lifts']),'full/empty Tait fibre count')
        families=[]
        for pattern,fam in c['families'].items():
            forced,banned=fam['forced'],fam['forbidden'];X=set().union(*(set(edges[k]) for k in forced));live=allv-X
            residual=enumerate_pm(live,edges,{banned});require(residual==list(map(tuple,fam['all_residual_matchings'])),'residual PM table')
            indices=[i for i,M in enumerate(allpm) if set(forced)<=set(M) and banned not in M]
            require(indices==fam['family_indices'],'two-in one-out family');require([tuple(sorted(set(allpm[i])-set(forced))) for i in indices]==residual,'residual bijection')
            require(sum(weights[i] for i in indices)==c['weights'][pattern],'weighted family')
            adj=[set() for _ in range(n)]
            for k,(a,b) in enumerate(edges):
                if k!=banned and a in live and b in live:adj[a].add(b);adj[b].add(a)
            observed={};max_def=-n;subsets=0
            for size in range(len(live)+1):
                for S0 in itertools.combinations(sorted(live),size):
                    S=set(S0);parts=comps(live-S,adj);q=sum(len(p)%2 for p in parts);d=q-size;max_def=max(max_def,d);subsets+=1
                    if d>0:observed[frozenset(S)]={frozenset(p) for p in parts}
            saved={frozenset(b['S']):{frozenset(p) for p in b['components']} for b in fam['all_barriers']}
            require(observed==saved,'missing or incorrect Tutte barrier')
            require(max_def==fam['maximum_deficiency'],'maximum deficiency')
            require(bool(residual)==(not observed),'Tutte equivalence')
            for barrier in fam['maximum_cardinality_barriers']:
                S=set(barrier['S']);parts=list(map(set,barrier['components']));require(all(len(p)%2 for p in parts),'even maximal-barrier component')
                mu=[]
                for C in parts:
                    cut=sum((a in C)!=(b in C) for a,b in edges);mu.append((cut-3)//2)
                    for v in C:require(bool(enumerate_pm(C-{v},edges,{banned})),'factor-critical deletion fails')
                a,b=edges[banned];tau=int(any(a in C for C in parts) and any(b in C for C in parts) and not any({a,b}<=C for C in parts))
                internal=sum(a in S and b in S for a,b in edges);sx=sum((a in S and b in X) or(a in X and b in S) for a,b in edges);xx=sum({a,b}<=X for a,b in edges)
                if c['no_nontrivial_3cut']:require(sum(mu)+internal+sx==3-xx+tau,'cut budget identity')
            families.append({'pattern':pattern,'PM':len(residual),'weight':c['weights'][pattern],'subsets':subsets,'barriers':len(observed),'maximum_deficiency':max_def})
        result.append({'name':c['name'],'all_PM':len(allpm),'families':families})
    print(json.dumps({'status':'PASS','inputs':{f:hashlib.sha256((OTHER/f).read_bytes()).hexdigest() for f in ['PROOF.md','check.py','certificate.json','graphs.json']},'controls':result},indent=2))
if __name__=='__main__':main()
