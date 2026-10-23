"""Bounded one-edge quotient library; diagnostic only."""
import itertools,json
from pathlib import Path
import explore_k8 as e
H=Path(__file__).resolve().parent
def quotient(cap,contract):
 a,b=contract
 if b in cap['boundary']:a,b=b,a
 mp={v:(a if v==b else v) for v in cap['inner']+cap['boundary']}
 edges={tuple(sorted((mp[x],mp[y]))) for x,y in cap['edges'] if mp[x]!=mp[y]}
 return dict(vertices=sorted(set(mp.values())),ordered_boundary=[mp[v] for v in cap['boundary']],ordered_inner=[v for v in cap['inner'] if v in mp.values() and v not in cap['boundary']],edges=sorted(edges))
def main():
 ws=e.words();rows=[]
 for a,b in [(0,0),(0,1),(0,2),(0,3)]:
  k=[0]*6;k[a]+=1;k[b]+=1;cap=e.m.wheel(k)
  original=dict(vertices=cap['inner']+cap['boundary'],ordered_inner=cap['inner'],ordered_boundary=cap['boundary'],edges=sorted(cap['edges']))
  ls=[e.m.complete_lifts(original,w) for w in ws];mask=sum(1<<i for i,x in enumerate(ls) if x)
  safe=[];union=0
  for edge in sorted(cap['edges']):
   if set(edge)<=set(cap['boundary']):continue
   q=quotient(cap,edge);qs=sum(1<<i for i,w in enumerate(ws) if e.m.complete_lifts(q,w))
   if qs&~mask==0:safe.append(dict(edge=edge,nonempty=qs.bit_count()));union|=qs
  print(k,'safe',safe,'missing',(mask&~union).bit_count(),flush=True)
  rows.append(dict(distribution=k,safe=safe,missing=[w for i,w in enumerate(ws) if mask>>i&1 and not union>>i&1]))
 with (H/'EXPLORATION_CONTRACT.json').open('x') as f:json.dump(rows,f,indent=2);f.write('\n')
if __name__=='__main__':main()
