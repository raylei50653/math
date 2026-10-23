"""Bounded octagon library: triangulate, then contract selected diagonals."""
import importlib.util,itertools,json
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('prior',HERE/'entry/audits/2026-10-23-941-gamma8-empty-seven-6b09cd4/check.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
@lru_cache(None)
def triangulations(poly):
 if len(poly)<3:return (frozenset(),)
 out=set();a,b=poly[0],poly[-1]
 for k in range(1,len(poly)-1):
  c=poly[k]
  for left in triangulations(poly[:k+1]):
   for right in triangulations(poly[k:]):
    es=left|right|{tuple(sorted((a,c))),tuple(sorted((c,b)))}
    out.add(frozenset(e for e in es if (e[1]-e[0]) not in (1,7)))
 return tuple(sorted(out,key=lambda x:sorted(x)))
def words():
 return sorted({m.canonical(w) for w in itertools.product(range(4),repeat=8) if all(w[i]!=w[(i+1)%8] for i in range(8))})
def models(ws):
 out={}
 for tri in triangulations(tuple(range(8))):
  tri=sorted(tri)
  for bits in itertools.product([False,True],repeat=len(tri)):
   equal=[e for e,b in zip(tri,bits) if b];diff=[e for e,b in zip(tri,bits) if not b]
   mask=sum(1<<i for i,w in enumerate(ws) if all(w[a]==w[b] for a,b in equal) and all(w[a]!=w[b] for a,b in diff))
   if mask and mask not in out:out[mask]=dict(equal=equal,different=diff)
 return out
def main():
 ws=words();qs=models(ws);rows=[]
 for a in range(6):
  for b in range(a,6):
   k=[0]*6;k[a]+=1;k[b]+=1;cap=m.wheel(k)
   old=dict(vertices=cap['inner']+cap['boundary'],ordered_inner=cap['inner'],ordered_boundary=cap['boundary'],edges=sorted(cap['edges']))
   lifts=[m.complete_lifts(old,w) for w in ws];support=sum(1<<i for i,l in enumerate(lifts) if l)
   safe=[(mask,q) for mask,q in qs.items() if mask&~support==0]
   union=0
   for mask,q in safe:union|=mask
   missing=[list(w) for i,w in enumerate(ws) if support>>i&1 and not union>>i&1]
   print(k,'support',support.bit_count(),'lifts',sum(map(len,lifts)),'safe',len(safe),'miss',len(missing),flush=True)
   rows.append(dict(distribution=k,nonempty=support.bit_count(),safe=len(safe),missing=missing))
 with (HERE/'EXPLORATION_K8.json').open('x') as f:json.dump(dict(words=len(ws),models=len(qs),triangulations=len(triangulations(tuple(range(8)))),caps=rows),f,indent=2);f.write('\n')
if __name__=='__main__':main()
