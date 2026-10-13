#!/usr/bin/env python3
"""Exploratory nonnegative fixed-split component-orbit count cone."""
from collections import Counter
from itertools import permutations, combinations
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack,csr_matrix
from count_feasibility import inputs,algebra,HERE

interface,queries=inputs()
words=list(map(tuple,interface['pattern_order']));wi={p:i for i,p in enumerate(words)}
literal=list(map(tuple,interface['literal_assignments']))
group=[p for p in permutations(range(4)) if (p[0]//2==p[1]//2 and p[2]//2==p[3]//2)]
def norm(p):
    d={};return tuple(d.setdefault(c,len(d)) for c in p)
def canon(p):return min(tuple(g[c] for c in p) for g in group)
canon_of={p:canon(p) for p in literal}
states=sorted(set(canon_of.values()));si={p:i for i,p in enumerate(states)}
state_of={p:si[canon_of[p]] for p in literal}
sizes=Counter(state_of.values());pattern_of=[wi[norm(p)] for p in states]
nc,active,rows=algebra(words)
orbits=set()
for idx,p in enumerate(states):
    side=[c//2 for c in p]
    for part in nc:
        if any(part[a]==part[b] and side[a]!=side[b] for a,b in combinations(range(8),2)):continue
        if any(side[a]==side[(a+1)%8] and part[a]!=part[(a+1)%8] for a in range(8)):continue
        count=Counter()
        for flip in range(1<<(max(part)+1)):
            q=tuple(c^1 if flip>>part[a]&1 else c for a,c in enumerate(p))
            count[state_of[q]]+=1
        # Incidence of the G8-averaged literal orbit; common multiplier 8.
        col=tuple((s,8*n//sizes[s]) for s,n in sorted(count.items()))
        assert all(8*n%sizes[s]==0 for s,n in count.items())
        orbits.add(col)
print('states',len(states),'orbit columns',len(orbits),flush=True)
orbits=sorted(orbits)
result={'schema':'c8-kempe-cone-discovery-v1','states':states,'state_pattern_indices':pattern_of,'state_orbit_sizes':[sizes[s] for s in range(len(states))],'columns':orbits,'queries':[]}
for query in queries:
    mask=query['support']; good=[j for j,col in enumerate(orbits) if all(mask>>pattern_of[s]&1 for s,_ in col)]
    ii=[];jj=[];vv=[]
    for j,colidx in enumerate(good):
        for s,v in orbits[colidx]:ii.append(s);jj.append(j);vv.append(v)
    M=coo_matrix((vv,(ii,jj)),shape=(len(states),len(good))).tocsr()
    E=np.array([rows[p] for p in pattern_of],float)
    Aeq=hstack([M,csr_matrix(-E)],format='csr')
    allowed=[p for p in range(274) if mask>>p&1]
    Aub=hstack([csr_matrix((len(allowed),len(good))),csr_matrix(-np.array([rows[p] for p in allowed],float))],format='csr')
    # all state rows include zeros since columns outside mask were removed.
    lp=linprog(np.zeros(len(good)+len(active)),A_eq=Aeq,b_eq=np.zeros(len(states)),A_ub=Aub,b_ub=-np.ones(len(allowed)),bounds=[(0,None)]*len(good)+[(None,None)]*len(active),method='highs')
    print(query['query_id'],'columns',len(good),'status',lp.status,lp.message,flush=True)
    result['queries'].append({'query_id':query['query_id'],'column_indices':good,'status':lp.status,'message':lp.message,'solution':lp.x.tolist() if lp.success else None})
with (HERE/'kempe_cone_discovery.json').open('w') as f:json.dump(result,f,separators=(',',':'));f.write('\n')
