#!/usr/bin/env python3
"""Finite SAME local graph calibration of complete rootless M/N swaps.
The swaps stand for full original components, including every exterior vertex;
this script records only restrictions to the predecessor ten named vertices.
"""
import itertools,json
from pathlib import Path
SRC=Path(__file__).resolve().parents[3]/'2026-10-23-941-gamma8-cells-6b09cd4/certificate.json'
if not SRC.is_file():
    SRC=Path('audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json')
x=json.loads(SRC.read_text())
PAIRS=list(itertools.combinations(range(4),2))
def require(condition,message):
    if not condition:raise ValueError(message)
def components(edges,col,pair):
    unseen={v for v,c in col.items() if c in pair};ans=[]
    while unseen:
        root=min(unseen);todo=[root];unseen.remove(root);found=[]
        while todo:
            a=todo.pop();found.append(a)
            for u,v in edges:
                b=v if u==a else u if v==a else None
                if b in unseen:
                    unseen.remove(b);todo.append(b)
        ans.append(sorted(found))
    return sorted(ans)
def path(edges,col,pair,a,b):
    if col[a] not in pair or col[b] not in pair:return None
    todo=[[a]];seen={a}
    while todo:
        p=todo.pop(0)
        if p[-1]==b:return p
        for u,v in edges:
            z=v if u==p[-1] else u if v==p[-1] else None
            if z is not None and z not in seen and col[z] in pair:
                seen.add(z);todo.append(p+[z])
    return None
out=[]
for c in x['candidates']:
    if c['classification']!='local_necessary_type':continue
    rows=[]
    for m,n,k in itertools.product(range(2),repeat=3):
        col=dict(x['original_colors'])
        for v,label in x['original_component_labels'].items():
            if (label=='M' and m) or (label=='K' and k):col[v]^=2
            if label=='N' and n:col[v]^=2
        require(all(col[u]!=col[v] for u,v in c['edges']), 'improper local orbit coloring')
        rows.append({'M02':bool(m),'N13':bool(n),'same_K02':bool(k),
                     'colors':col,'full_local_palette_components':{
                      ''.join(map(str,p)):components(c['edges'],col,p) for p in PAIRS},
                     'e_h_12_path':path(c['edges'],col,(1,2),'e','h'),
                     'd_h_12_path':path(c['edges'],col,(1,2),'d','h'),
                     'd_x_03_path':path(c['edges'],col,(0,3),'d','x')})
    # In every type, M then same K gives an actual local 12 path e to h.
    row=next(r for r in rows if r['M02'] and not r['N13'] and r['same_K02'])
    require(row['e_h_12_path'] and row['d_h_12_path'], 'missing full M/K path')
    # N then same K additionally gives e/h in the O core only.
    row=next(r for r in rows if not r['M02'] and r['N13'] and r['same_K02'])
    require(bool(row['e_h_12_path']) == (c['core']=='O'), 'N/K e-h path core mismatch')
    out.append({'id':c['id'],'core':c['core'],'rows':rows})
print(json.dumps({'scope':'restrictions of commuting COMPLETE rootless M/N and SAME K on one original graph; not full source realizations',
                  'candidate_count':len(out),'rows':out},ensure_ascii=False,sort_keys=True,indent=2))
