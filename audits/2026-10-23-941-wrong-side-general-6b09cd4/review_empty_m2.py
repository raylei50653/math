#!/usr/bin/env python3
"""Independent actual-triangle complex checks for the sibling K6 cap."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
TARGET=ROOT/'audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json'
raw=TARGET.read_bytes();c=json.loads(raw)
rows=[]
for cap in c['caps']:
    vs=set(cap['vertices']);es={frozenset(e) for e in cap['edges']}
    adj={v:set() for v in vs}
    for a,b in cap['edges']:adj[a].add(b);adj[b].add(a)
    triangles=[tuple(t) for t in combinations(sorted(vs),3) if all(frozenset(e) in es for e in combinations(t,2))]
    incidence=Counter(frozenset(e) for t in triangles for e in combinations(t,2))
    boundary={e for e,n in incidence.items() if n==1}
    K=cap['ordered_boundary'];want={frozenset((a,b)) for a,b in zip(K,K[1:]+K[:1])}
    assert len(triangles)==18 and boundary==want and all(n in (1,2) for n in incidence.values())
    assert len(vs)-len(es)+len(triangles)==1
    # Every claimed inner star really has one connected cyclic link.
    degree={}
    for v in cap['ordered_inner']:
        ns=adj[v];le={e for e in es if e<=ns};la={u:{w for w in ns if frozenset((u,w)) in le} for u in ns}
        assert all(len(n)==2 for n in la.values())
        seen=set();todo=[next(iter(ns))]
        while todo:
            u=todo.pop()
            if u in seen:continue
            seen.add(u);todo.extend(la[u]-seen)
        assert seen==ns
        degree[v]=len(ns)
    assert degree['T']==6 and all(d==5 for v,d in degree.items() if v!='T')
    # Connect and orient the actual triangles by shared interior edges.
    owners=defaultdict(list)
    for i,t in enumerate(triangles):
        for a,b in zip(t,t[1:]+t[:1]):owners[frozenset((a,b))].append((i,a,b))
    sign={0:1};todo=[0]
    while todo:
        i=todo.pop();t=triangles[i]
        for a,b in zip(t,t[1:]+t[:1]):
            for j,x,y in owners[frozenset((a,b))]:
                if j==i:continue
                wanted=-sign[i] if (x,y)==(a,b) else sign[i]
                if j in sign:assert sign[j]==wanted
                else:sign[j]=wanted;todo.append(j)
    assert len(sign)==18
    # Rootless N and the full original K induced graphs are precisely cycles.
    N={'r','s','tau','a','y','b'}
    assert all(len(adj[v]&N)==2 for v in N)
    assert {e for e in es if e<=set(K)}==want
    rows.append(dict(core=cap['core'],vertices=len(vs),edges=len(es),actual_triangle_candidates=len(triangles),single_boundary=K,inner_degrees=degree,connected_oriented_triangle_complex=True))
print(json.dumps(dict(status='PASS',target=str(TARGET.relative_to(ROOT)),sha256=sha256(raw).hexdigest(),statistics=rows,interpretation='finite complex calibration; actual-plane face premise and source completeness audited in REVIEW_EMPTY_M2.md'),sort_keys=True))
