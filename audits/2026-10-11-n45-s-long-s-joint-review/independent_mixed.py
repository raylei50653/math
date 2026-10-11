import json,time
from pathlib import Path
from itertools import product
from collections import Counter
start=time.monotonic(); d=Path('audits/2026-10-11-n45-s-long-s-joint'); z=json.loads((d/'certificate.json').read_bytes()); n=Counter()
def enum(V,E,B):
    neighbours={v:set() for v in V}
    for v,w in E: neighbours[v].add(w); neighbours[w].add(v)
    order=sorted(set(V)-set(range(5)),reverse=True); f=dict(enumerate(B)); result=[]
    def visit(k):
        if k==len(order): result.append(tuple(f[v] for v in V)); return
        v=order[k]
        for colour in range(4):
            if all(f.get(w,-1)!=colour for w in neighbours[v]):
                f[v]=colour;visit(k+1);del f[v]
    visit(0);return sorted(result)
for g in z['graphs']:
    r,s=g['root_order']; C=g['C_vertices']; E=g['original_edges']; pieces={p['id']:p for p in g['pieces']}
    for case in g['cases']:
        for row in case['rows']:
            B=tuple(map(int,row['literal'])); independent=[]
            for rec in row['mixed']:
                p=pieces[rec['id']]; verts=p['vertices']; dom=set(range(5))|set(verts); fs=[f[5:] for f in enum(list(range(5))+verts,[e for e in E if set(e)<=dom],B)]
                assert fs==[tuple(f) for f in rec['assignments']]
                for a in range(4):
                    want=[i for i,f in enumerate(fs) if all(f[verts.index(v)]!=a for v in p['contacts'][str(r)])]
                    assert want==rec['all_r_fibres'][a]['assignment_indices']
                for cell in rec['all_16_original_root_pin_fibres']:
                    a,b=cell['pins_r_s']; want=[i for i,f in enumerate(fs) if all(f[verts.index(v)]!=a for v in p['contacts'][str(r)]) and all(f[verts.index(v)]!=b for v in p['contacts'][str(s)])]
                    assert want==cell['assignment_indices'];n['mixed_pin_cells']+=1
                independent.append((verts,fs));n['mixed_records']+=1
            assembled=[]
            for i,origin in enumerate(row['C_from_mixed_indices']):
                a,pi,qi=origin; f={r:a}
                for (verts,fs),j in zip(independent,(pi,qi)): f.update(zip(verts,fs[j]))
                full=tuple(f[v] for v in C); assert full==tuple(row['C_assignments'][i]);assert all(f[v]!=f[w] for v,w in case['X_edges'] if v in f and w in f)
                assert all(a!=B[b] for b in case['retained_r_spokes']);assembled.append(full);n['mixed_join_provenance']+=1
            assert len(assembled)==len(set(assembled))
            assert g['whole_root_transport_to_prior']==[g['root_order'].index(v) for v in g['original_root_order']]
            for cell in row['all_16_root_pin_cells']:
                assert cell['prior_pins']==[cell['pins_r_s'][g['root_order'].index(v)] for v in g['original_root_order']];n['root_transports']+=1
print(json.dumps({'result':'PASS','counts':dict(n),'elapsed_seconds':round(time.monotonic()-start,3)},sort_keys=True))
