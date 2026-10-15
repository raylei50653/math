#!/usr/bin/env python3
"""Independent cross-review of saved XOR controls; does not import their checker."""
import hashlib,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OTHER=HERE.parent/'2026-10-15-xor-batch-descent-6ddea32'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def edge_components(n,edges,selected):
    parent=list(range(n))
    def root(v):
        while parent[v]!=v:v=parent[v]
        return v
    touched=set()
    for k in selected:
        a,b=edges[k];touched|={a,b};parent[root(a)]=root(b)
    groups={}
    for k in selected:groups.setdefault(root(edges[k][0]),[]).append(k)
    return sorted(sorted(v) for v in groups.values())
def main():
    graphs=json.loads((OTHER/'graphs.json').read_text());saved=json.loads((OTHER/'certificate.json').read_text());out=[]
    for g,c in zip(graphs,saved['controls']):
        n,es,e,f=g['n'],g['edges'],g['e'],g['f'];all_edges=set(range(len(es)));ms=[set(m['edges']) for m in c['matchings']]
        incidence=[[] for _ in range(n)]
        for k,(u,v) in enumerate(es):incidence[u].append((v,k));incidence[v].append((u,k))
        # Different branching order: greatest remaining vertex, descending edge.
        complete=set()
        def dfs(free,chosen):
            if not free:complete.add(tuple(sorted(chosen)));return
            u=max(free)
            for v,k in reversed(incidence[u]):
                if v in free:dfs(free-{u,v},chosen+[k])
        dfs(set(range(n)),[])
        require(complete=={tuple(sorted(m)) for m in ms},'incomplete matching table')
        odd=[]
        for M,row in zip(ms,c['matchings']):
            require(all(sum(k in M for _,k in incidence[v])==1 for v in range(n)),'not a perfect matching')
            comps=edge_components(n,es,all_edges-M);o=sum(len(p)%2 for p in comps);odd.append(o)
            require(o==row['oddness'],'wrong oddness')
            lifts=row['full_tait_lifts'];require(len(lifts)==(0 if o else 2**len(comps)),'wrong full Tait fibre')
            require(len({tuple(r) for r in lifts})==len(lifts),'duplicate full lift')
            for r in lifts:
                require({i for i,a in enumerate(r) if a==0}==M,'lift uses different matching')
                require(all({r[k] for _,k in incidence[v]}=={0,1,2} for v in range(n)),'improper full lift')
        states=[i for i,M in enumerate(ms) if (e in M)!=(f in M)]
        require(states==c['admissible_states'],'wrong XOR state table');moves=[]
        for i,j in itertools.combinations(states,2):
            ps=edge_components(n,es,ms[i]^ms[j]);marked=[set(p)&{e,f} for p in ps]
            basic=(len(ps)==1 and len(marked[0]) in [0,2]) or (len(ps)==2 and sorted(map(sorted,marked))==[[e],[f]])
            if basic:moves.append([i,j,len(ps),odd[j]-odd[i]])
        require(moves==c['complete_primitive_moves'],'incomplete basic move table')
        for i,li,j,lj,changed in c['local_colour_involution']:
            old=c['matchings'][i]['full_tait_lifts'][li];new=c['matchings'][j]['full_tait_lifts'][lj]
            beta=old[f] if old[e]==0 else old[e]
            pc=edge_components(n,es,{k for k,a in enumerate(old) if a in [0,beta]})
            touched=[p for p in pc if e in p or f in p]
            wanted=sorted(k for p in touched for k in p)
            require(len(touched) in [1,2] and changed==wanted,'nonlocal colour switch')
            require(new==[beta-a if k in wanted else a for k,a in enumerate(old)],'wrong complete target lift')
        nonadd=[];start=c['start']
        for move in c['complete_start_moves']:
            j=move['to'];ps=edge_components(n,es,ms[start]^ms[j]);individual=[]
            for p in ps:
                co=edge_components(n,es,all_edges-(ms[start]^set(p)));individual.append(sum(len(q)%2 for q in co)-odd[start])
            require(individual==move['individual_deltas'],'wrong individual deltas')
            require(odd[j]-odd[start]==move['oddness_delta'],'wrong joint delta')
            if sum(individual)!=odd[j]-odd[start]:nonadd.append({'from':start,'to':j,'individual':individual,'joint':odd[j]-odd[start]})
        out.append({'name':g['name'],'matchings':len(ms),'all_basic_moves':len(moves),'full_colour_switches':len(c['local_colour_involution']),'nonadditive_start_batches':nonadd})
    record={'status':'PASS','inputs':{name:hashlib.sha256((OTHER/name).read_bytes()).hexdigest() for name in ['graphs.json','certificate.json','check.py','PROOF.md']},'controls':out}
    print(json.dumps(record,indent=2))
if __name__=='__main__':main()
