#!/usr/bin/env python3
"""Rank bounded exact patch relations by complete surviving negative fibres."""
import probe as p
from itertools import product
from collections import defaultdict,Counter
import json,gzip,hashlib,time
D=p.ROOT
ROWS=('01021','01202','01212')
with gzip.open(D.parent/'interface/certificate.json.gz','rt') as f:inter=json.load(f)
inc=[defaultdict(set) for _ in ROWS]
# Store FULL literal C11 fibres: global frame normalization uniquely fixes
# the unused fourth colour because a proper C5 uses at least three colours.
for i in inter['live']:
 cap=inter['caps'][i];a,n,u2,u1,L,q,c,s,v,w,t=cap['core']
 for b in range(4):
  if b in (a,c,q):continue
  rimid=p.INDEX[p.canonical((a,b,q,L,u1,u2,n))]
  for x,y,r in cap['right_xyr']:
   frame=(x,y,a,b,c);z=''.join(map(str,p.canonical(frame)))
   if z not in ROWS:continue
   perm=dict(zip(frame,map(int,z)))
   assert len(perm)>=3
   for missing,target in zip(set(range(4))-set(perm),set(range(4))-set(perm.values())):perm[missing]=target
   literal=tuple(perm[vv] for vv in cap['core'])
   inc[ROWS.index(z)][rimid].add(literal)
fibre_ids=[{t:i for i,t in enumerate(sorted(set().union(*d.values())))} for d in inc]
bits=[{j:sum(1<<ids[t] for t in ts) for j,ts in d.items()} for d,ids in zip(inc,fibre_ids)]
def residual(support):
 out=[]
 for d in bits:
  b=0
  for j,v in d.items():
   if support&(1<<j):b|=v
  out.append(b)
 return tuple(out)
def classes(k,newedges,sig):
 par=list(range(7+k))
 def find(x):
  while par[x]!=x:x=par[x]
  return x
 for j,(u,v) in enumerate(newedges):
  if sig&(1<<j):par[find(u)]=find(v)
 return tuple(tuple(i for i in range(7+k) if find(i)==r) for r in sorted({find(i) for i in range(7+k)}))
seen={};best={};counts=Counter();start=time.monotonic()
for k in range(3):
 for faces in p.all_triangulations(k):
  newedges=sorted({e for f in faces for e in p.combinations(f,2)}-p.BOUND)
  signatures=defaultdict(int)
  for i,t in enumerate(p.STATES):
   for extra in product(range(4),repeat=k):
    c=t+extra
    sig=sum(1<<j for j,(u,v) in enumerate(newedges) if c[u]==c[v])
    signatures[sig]|=1<<i
  for sig,support in signatures.items():
   alpha=[a for a in p.ALPHA_IDS if support&(1<<a)]
   if not alpha:continue
   cl=classes(k,newedges,sig)
   # Geometry allows the exterior chord a-u2. Avoid its contraction.
   if any(0 in g and 5 in g for g in cl):continue
   delta=len(cl)-10
   if support in seen and seen[support]<=delta:continue
   seen[support]=delta
   rs=residual(support);sizes=tuple(b.bit_count() for b in rs)
   counts[(sum(n>0 for n in sizes),)]+=1
   cand={'interior':k,'faces':faces,'new_edges':newedges,'equal_signature':sig,'classes':cl,'completed_delta':delta,'alpha_ids':alpha,'support_ids':[i for i in range(91) if support&(1<<i)],'negative_fibre_counts':dict(zip(ROWS,sizes))}
   score=(sum(n>0 for n in sizes),sum(sizes),delta,k)
   old=best.get(sizes)
   if old is None or score<old[0]:best[sizes]=(score,cand,rs)
   # Keep individual negative masks sorted too in final output.
ranked=sorted(best.values(),key=lambda z:z[0])[:25]
for score,cand,rs in ranked:
 cand['complete_negative_literal_fibres']={row:[t for t,j in ids.items() if b&(1<<j)] for row,ids,b in zip(ROWS,fibre_ids,rs)}
data={'status':'bounded necessary-interface comparison, no source realization','interface_sha256':hashlib.sha256((D.parent/'interface/certificate.json.gz').read_bytes()).hexdigest(),'negative_rows':ROWS,'literal_fibres_in_interface':[len(ids) for ids in fibre_ids],'distinct_relations_seen':len(seen),'best_candidates':[c for s,c,r in ranked],'seconds':time.monotonic()-start}
with (D/'rank.json').open('x') as f:json.dump(data,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in data.items() if k not in ('best_candidates',)}))
for score,cand,rs in ranked[:8]:print(json.dumps({k:v for k,v in cand.items() if k!='complete_negative_literal_fibres'}))
