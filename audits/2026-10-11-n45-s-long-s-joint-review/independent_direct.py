import json,time
from pathlib import Path
from itertools import product
from collections import Counter
start=time.monotonic(); d=Path('audits/2026-10-11-n45-s-long-s-joint'); z=json.loads((d/'certificate.json').read_bytes()); counts=Counter()

def enum(V,E,B):
    adj={v:set() for v in V}
    for v,w in E: adj[v].add(w); adj[w].add(v)
    free=sorted(set(V)-set(range(5)),key=lambda v:(-len(adj[v]),-v)); f=dict(enumerate(B)); out=[]
    assert all(f[v]!=f[w] for v,w in E if v in f and w in f)
    def go(k):
        if k==len(free): out.append(tuple(f[v] for v in V)); return
        v=free[k]; banned={f[w] for w in adj[v] if w in f}
        for colour in (3,2,1,0):
            if colour not in banned:
                f[v]=colour; go(k+1)
        f.pop(v,None)
    go(0); return sorted(out)

for g in z['graphs']:
    raw=json.loads((d/'frozen/artifacts/c5_excess_two_e4c/controls'/ (g['id']+'.json')).read_bytes()) if (d/'frozen/artifacts/c5_excess_two_e4c/controls'/ (g['id']+'.json')).is_file() else None
    if raw is None:
        raw=next(json.loads(p.read_bytes()) for p in (d/'frozen/artifacts/c5_excess_two_e4c/controls').glob('*.json') if json.loads(p.read_bytes())['id']==g['id'])
    original=json.loads((d/'frozen'/raw['source']).read_bytes()); E=original['canonical_edges']; V=raw['vertices']; assert E==g['original_edges']; r,s=g['root_order']; C=g['C_vertices']; U=g['U_vertices']; I=g['isolated_vertices']
    eligible=sorted(tuple(sorted((r,b))) for v,b in [] )
    assert sorted(tuple(c['omitted_edge']) for c in g['cases'])==sorted(tuple(sorted((r,w))) for v,w in E if v==r and w<5)+sorted(tuple(sorted((r,v))) for v,w in E if w==r and v<5)
    counts['graphs']+=1; counts['source_sigma_'+str(original['sigma_mask'])]+=1
    for case in g['cases']:
        xe=[e for e in E if e!=case['omitted_edge']]; assert xe==case['X_edges']; counts['cases']+=1
        for row in case['rows']:
            B=tuple(map(int,row['literal'])); X=enum(V,xe,B); G=enum(V,E,B); counts['rows']+=1
            expectedC=[f[5:] for f in enum(list(range(5))+C,[e for e in xe if set(e)<=set(range(5))|set(C)],B)]
            expectedU=[f[5:] for f in enum(list(range(5))+U,[e for e in xe if set(e)<=set(range(5))|set(U)],B)]
            assert expectedC==[tuple(f) for f in row['C_assignments']]; assert expectedU==[tuple(f) for f in row['U_assignments']]
            for verts,fs,order,relation,key,fkey in [(C,expectedC,g['C_s_contact_order'],row['R_C'],'all_ambient_C_r_tuple_fibres','C_assignment_indices'),(U,expectedU,g['U_s_contact_order'],row['R_U'],'all_ambient_U_tuple_fibres','U_assignment_indices')]:
                preimages={}
                for i,f in enumerate(fs): preimages.setdefault(tuple(f[verts.index(v)] for v in order),[]).append(i)
                assert {tuple(x['tuple']):x['assignment_indices'] for x in relation}==preimages
                ambient=row[key]
                expectedcoords=set(product(range(4),repeat=len(order)+(1 if verts is C else 0)))
                coords=set()
                for a in ambient:
                    t=tuple(a['C_contact_tuple'] if verts is C else a['U_contact_tuple']); coord=(a['r_colour'],)+t if verts is C else t; coords.add(coord)
                    expected=[i for i,f in enumerate(fs) if tuple(f[verts.index(v)] for v in order)==t and (verts is U or f[verts.index(r)]==a['r_colour'])]
                    assert expected==a[fkey]; counts['ambient_cells']+=1; counts['empty_ambient_cells']+=not expected
                assert coords==expectedcoords and len(coords)==len(ambient)
            for cell in row['all_16_root_pin_cells']:
                a,b=cell['pins_r_s']; joinX=[]; joinG=[]
                for source,target in [('X_lift_indices_C_U_isolated',joinX),('G_lift_indices_C_U_isolated',joinG)]:
                    for ci,ui,zi in cell[source]:
                        assignment=dict(enumerate(B))|{s:b}|dict(zip(C,row['C_assignments'][ci]))|dict(zip(U,row['U_assignments'][ui]))|dict(zip(I,g['isolated_assignments'][zi]))
                        target.append(tuple(assignment[v] for v in V))
                directX=[f for f in X if (f[V.index(r)],f[V.index(s)])==(a,b)]; directG=[f for f in G if (f[V.index(r)],f[V.index(s)])==(a,b)]
                assert sorted(joinX)==directX; assert sorted(joinG)==directG; assert len(joinX)==len(set(joinX)) and len(joinG)==len(set(joinG))
                counts['pins']+=1; counts['X_lifts']+=len(directX); counts['G_lifts']+=len(directG)
print(json.dumps({'result':'PASS','independent_algorithm':'fixed descending-degree vertex order, reversed colour order; no checker/prior imports','counts':dict(sorted(counts.items())),'elapsed_seconds':round(time.monotonic()-start,3)},sort_keys=True))
