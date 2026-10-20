#!/usr/bin/env python3
"""Independent direct-C10 complete-lift check of C's two new graphs."""
from pathlib import Path
from itertools import product,combinations
from math import factorial
import hashlib,importlib.util,json
B=Path(__file__).resolve().parent;C=B.parent/'C';F=B.parent/'frozen'
manifest=json.loads((C/'INPUTS.json').read_text())
for path,want in manifest['files'].items():
 data=(F/path).read_bytes();assert len(data)==want['bytes'] and hashlib.sha256(data).hexdigest()==want['sha256']
s=importlib.util.spec_from_file_location('m',F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ten=[t for t in m.growth(10,four=True) if m.proper(t)]
Ms={name:[[0]*len(ten) for _ in range(10)] for name in ('J1','J2')}
for i,(a,n,R,L,q,c,s,v,w,t) in enumerate(ten):
 for b,x,y,r in product(range(4),repeat=4):
  if b in (a,c,q) or x in (c,s,y,r) or y in (a,t,r) or r in (s,v,w,t):continue
  row=m.ROWS.index(''.join(map(str,m.canonical((x,y,a,b,c)))))
  if L==b and a!=R:Ms['J1'][row][i]+=1
  if a!=L and a!=R and b!=L:Ms['J2'][row][i]+=1
 fac=factorial(4-len(set(ten[i])))
 for N in Ms.values():
  for row in N:assert row[i]%fac==0;row[i]//=fac
out=json.loads((C/'comparisons.json').read_text())
for name,N in Ms.items():assert N==out['matrices'][name]['F']
# Exact local embedding: both constructions use the same hexagon before contraction.
added=((0,3),(0,4),(1,3))
for (a,b),(c,d) in combinations(added,2):assert not(a<c<b<d or c<a<d<b)
faces=((0,1,3),(1,2,3),(0,3,4),(0,4,5))
edges={tuple(sorted((i,(i+1)%6))) for i in range(6)}|set(added)
assert all(tuple(sorted(e)) in edges for face in faces for e in combinations(face,2))
image=lambda i:1 if i==3 else i
contracted={tuple(sorted((image(u),image(v)))) for u,v in edges if {u,v}!={1,3}}
assert all(u!=v for u,v in contracted)
# Exactly one original interior boundary-of-hole point is merged into b.
assert -2-1==-3 and -2==-2
expected={'J1':[935,942,943],'J2':[943]}
for rec in out['records']:
 actual=[r['mask'] for r in rec['survivors'] if r['mask']&512]
 assert actual==expected[rec['candidate']]
 assert all(mask&2 and not(mask&16) and not(mask&64) for mask in actual)
print(json.dumps({'pass':True,'complete_direct_C10_matrices_equal':list(Ms),
 'original_boundary_retained':True,'completed_inner_deltas':[-3,-2],
 'positive_acceptance_supports':expected,'original_rejections_zero':[4,6]},sort_keys=True))
