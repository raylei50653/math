#!/usr/bin/env python3
"""Independent raw-stream/aggregate audit; no parent checker imports.

This verifies saved full-lift validity and coverage metadata, not exhaustive
coloring-search completeness. The parent's two solvers supply that obligation.
"""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'2026-10-13-k15-sphere-6cafdfb'

def parse(path):
    data=path.read_bytes()
    assert data.startswith(b'>>planar_code<<')
    i=15; spheres=[]
    while i<len(data):
        n=data[i];i+=1;assert n==21
        a=[]
        for _ in range(n):
            j=data.index(0,i);a.append([v-1 for v in data[i:j]]);i=j+1
        assert sum(map(len,a))==114 and min(map(len,a))>=5
        for u,vs in enumerate(a):
            assert len(vs)==len(set(vs)) and u not in vs
            assert all(0<=v<n and u in a[v] for v in vs)
        spheres.append(a)
    return spheres

p=parse(SOURCE/'generation/spheres21.pc')
s=parse(SOURCE/'generation/spheres21_from_min4.pc')
data=json.loads(gzip.decompress((SOURCE/'certificate.json.gz').read_bytes()))
rows=['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232']
assert data['pattern_order']==rows
assert data['base']=='6cafdfb02fe5892a49eee21f92aea2369a25c022'
expected={}
hist=Counter()
for sid,a in enumerate(p):
    for z,vs in enumerate(a):
        if len(vs)!=5: continue
        mapping=vs+sorted(set(range(21))-set(vs)-{z})
        inverse={v:i for i,v in enumerate(mapping)}
        rot=[[inverse[v] for v in a[u] if v!=z] for u in mapping]
        edges=sorted([u,v] for u,ns in enumerate(rot) for v in ns if u<v)
        assert len(edges)==52
        h=sum(len(a[v])-1 for v in vs)-20
        hist[h]+=1
        expected[(sid,z)]=(mapping,rot,edges,h)
actual={(r['sphere'],r['root']):r for r in data['records']}
assert len(actual)==len(data['records']) and set(actual)==set(expected)
count=0; masks=Counter()
for key,(mapping,rot,edges,h) in expected.items():
    r=actual[key]
    assert r['canonical_to_original']==mapping
    assert r['rotation']==rot and r['edges']==edges and r['h']==h
    assert r['degree']==list(map(len,rot))
    assert len(r['rows'])==10
    mask=0
    for i,(word,row) in enumerate(zip(rows,r['rows'],strict=True)):
        assert row['pattern']==word
        fs=row['lifts'];assert len(fs)==row['count']==len(set(fs))
        assert fs==sorted(fs)
        for f in fs:
            assert len(f)==20 and f[:5]==word and set(f)<=set('0123')
            assert all(f[u]!=f[v] for u,v in edges)
        count+=len(fs)
        if fs: mask|=1<<i
    assert mask==r['mask'];masks[mask]+=1
summary=data['summary']
assert len(p)==len(s)==summary['spheres']
assert len(expected)==summary['rooted_disks']
assert count==summary['full_lifts']
assert summary['literal_rows']==10*len(expected)
assert summary['h_histogram']=={str(k):v for k,v in sorted(hist.items())}
assert summary['mask_histogram']=={str(k):v for k,v in sorted(masks.items())}
assert masks=={1023:len(expected)}
result={'status':'PASS','review_scope':'source-domain proof, exact derivative, raw-root coverage, saved full-lift validity and aggregates; search completeness by parent independent solvers',
        'spheres_each_stream':len(p),'degree_five_roots':len(expected),'literal_rows':len(expected)*10,'full_lifts_validated':count,
        'h_histogram':dict(sorted(hist.items())),'mask_histogram':dict(masks),
        'certificate_sha256':hashlib.sha256((SOURCE/'certificate.json.gz').read_bytes()).hexdigest(),
        'payload_sha256':hashlib.sha256(gzip.decompress((SOURCE/'certificate.json.gz').read_bytes())).hexdigest()}
if '--write' in sys.argv:
    with (HERE/'RESULT.json').open('x') as out:json.dump(result,out,indent=2,sort_keys=True);out.write('\n')
else:
    assert result==json.loads((HERE/'RESULT.json').read_text()) or json.loads(json.dumps(result))==json.loads((HERE/'RESULT.json').read_text())
print(json.dumps(result,sort_keys=True))
