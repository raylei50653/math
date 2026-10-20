#!/usr/bin/env python3
"""Independent direct literal-C10 projection review of right-hole comparisons."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_caps',HERE/'check.py')
cap=importlib.util.module_from_spec(spec);spec.loader.exec_module(cap)
RIM=('x','y','t','w','v','s')

def polygon(poly):
    if len(poly)<=3:
        return {()}
    out=set()
    for i in range(1,len(poly)-1):
        for left in polygon(poly[:i+1]):
            for right in polygon(poly[i:]):
                diagonals=set(left)|set(right)
                if i>1:diagonals.add(tuple(sorted((poly[0],poly[i]))))
                if i<len(poly)-2:diagonals.add(tuple(sorted((poly[i],poly[-1]))))
                out.add(tuple(sorted(diagonals)))
    return out

def main():
    source=json.loads((HERE.parent/'right-minimality.json').read_text())
    tris=sorted(polygon(tuple(range(6))))
    assert len(tris)==14
    quotient=[(i,j) for i in range(6) for j in range(i+1,6) if j-i not in (1,5)]
    operations=[('quotient',pair) for pair in quotient]+[('triangulation',t) for t in tris]
    controls=json.loads((cap.OLD/'A/source-positive-certificate.json').read_text())['records']
    ten=sorted({cap.canonical(t) for t in cap.literal_cycle(10)})
    index={t:i for i,t in enumerate(ten)}
    results={}
    for kind,operation in operations:
        names=('G','Q1','Q2','GB')+(tuple('left_tri_'+str(i) for i in range(14)) if kind=='triangulation' else ())
        results[(kind,operation)]={c['name']:{n:[0]*10 for n in names} for c in controls}
    rowindex={tuple(map(int,r)):i for i,r in enumerate(cap.ROWS)}
    for t in cap.literal_cycle(10):
        a,n,R,L,q,c,s,v,w,tt=t
        # Fixed first two boundary letters; the remaining cap is independent.
        if 0 in (c,s) or 1 in (a,tt):continue
        rim=(0,1,tt,w,v,s)
        choices=[]
        for kind,operation in operations:
            good=(rim[operation[0]]==rim[operation[1]]) if kind=='quotient' else all(rim[i]!=rim[j] for i,j in operation)
            if good:choices.append((kind,operation))
        if not choices:continue
        j=index[cap.canonical(t)]
        cc=cap.caps(t)
        left={name:cc[name] for name in ('G','Q1','Q2','GB')}
        for i,tri in enumerate(tris):
            left['left_tri_'+str(i)]=[[b] for b in range(4) if b not in (a,c,q) and all((a,b,q,L,R,n)[u]!=(a,b,q,L,R,n)[v0] for u,v0 in tri)]
        for key in choices:
            for name,lifts in left.items():
                if name not in results[key][controls[0]['name']]:continue
                for lift in lifts:
                    ri=rowindex.get((0,1,a,lift[0],c))
                    if ri is None:continue
                    for control in controls:
                        results[key][control['name']][name][ri]+=control['core_counts'][j]
    by_key={}
    for record in source['records']:
        op=tuple(record['operation']) if record['kind']=='quotient' else tuple(map(tuple,record['operation']))
        if record['kind']=='quotient':op=tuple(RIM.index(x) for x in op)
        by_key[(record['kind'],op)]=record
    assert set(by_key)==set(results)
    compared=0
    for key,got in results.items():
        for projection in by_key[key]['projections']:
            assert got[projection['name']]==projection['counts'],(key,projection['name'])
            compared+=len(got[projection['name']])
    result={'status':'PASS','method':'direct literal C10 assignments and independent Catalan triangulations; no old matrix or B/minimality import',
            'right_quotients':9,'right_triangulations':14,'double_triangulations':196,
            'exact_control_query_comparisons':compared,
            'reviewed_sha256':hashlib.sha256((HERE.parent/'right-minimality.json').read_bytes()).hexdigest(),
            'source_realizations':0}
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
