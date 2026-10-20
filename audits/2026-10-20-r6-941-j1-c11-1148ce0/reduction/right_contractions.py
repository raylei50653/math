#!/usr/bin/env python3
"""Both original holes: exact local contraction/replacement relations."""
from pathlib import Path
from itertools import product,combinations
from collections import defaultdict
import importlib.util,gzip,json,time,sys
D=Path(__file__).resolve().parent
OLD=D.parent/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c'
sys.path.insert(0,str(OLD/'replacement'))
import probe as p
import combined as co

def triangulations(n,k):
 fs=[(0,j,j+1) for j in range(1,n-1)]
 for v in range(n,n+k):
  f=fs.pop(0);fs.extend(tuple(sorted((v,*e))) for e in combinations(f,2))
 initial=tuple(sorted(tuple(sorted(f)) for f in fs));seen={initial};queue=[initial]
 for faces in queue:
  yield faces
  ef=defaultdict(list)
  for f in faces:
   for e in combinations(f,2):ef[e].append(f)
  for e,fl in ef.items():
   if len(fl)!=2:continue
   a=next(v for v in fl[0] if v not in e);b=next(v for v in fl[1] if v not in e)
   if tuple(sorted((a,b))) in ef:continue
   new=tuple(sorted(set(faces)-set(fl)|{tuple(sorted((a,b,e[0]))),tuple(sorted((a,b,e[1])))}))
   if new not in seen:seen.add(new);queue.append(new)

def classes(n,k,es,sig):
 par=list(range(n+k))
 def find(x):
  while par[x]!=x:x=par[x]
  return x
 for j,(u,v) in enumerate(es):
  if sig&(1<<j):par[find(u)]=find(v)
 return tuple(tuple(i for i in range(n+k) if find(i)==r) for r in sorted({find(i) for i in range(n+k)}))

def right_relations(maxk=1):
 n=6;bound={tuple(sorted((i,(i+1)%n))) for i in range(n)}
 states=[t for t in p.growth(n) if all(t[i]!=t[(i+1)%n] for i in range(n))]
 idx={t:i for i,t in enumerate(states)}
 alphas={(v,w):set(idx[p.canonical((1,x,y,1,w,v))] for x,y in ((2,3),(3,2))) for v,w in ((2,3),(3,2))}
 ans={};counts={}
 for k in range(maxk+1):
  counts[k]=0
  for fs in triangulations(n,k):
   counts[k]+=1
   es=sorted({e for f in fs for e in combinations(f,2)}-bound);sigs=defaultdict(int)
   for i,t in enumerate(states):
    for ex in product(range(4),repeat=k):
     c=t+ex;sig=sum(1<<j for j,(u,v) in enumerate(es) if c[u]==c[v]);sigs[sig]|=1<<i
   for sig,sup in sigs.items():
    vw=[vw for vw,als in alphas.items() if any(sup&(1<<i) for i in als)]
    if not vw:continue
    cl=classes(n,k,es,sig)
    if any(1 in g and 2 in g for g in cl):continue
    delta=len(cl)-n-1
    if sup in ans and ans[sup]['delta']<=delta:continue
    ans[sup]={'interior':k,'faces':fs,'new_edges':es,'equal_signature':sig,'classes':cl,'delta':delta,'vw':vw,'support_ids':[i for i in range(len(states)) if sup&(1<<i)]}
 return states,idx,ans,counts

def compute():
 start=time.monotonic();inter=json.load(gzip.open(OLD/'interface/certificate-v4.json.gz','rt'))
 cache=D/'left-relations.json.gz'
 if cache.exists():left={int(k):v for k,v in json.load(gzip.open(cache,'rt')).items()}
 else:
  left=co.relations()
  with gzip.open(cache,'wt') as f:json.dump(left,f,sort_keys=True)
 print('left',len(left),flush=True)
 rstates,ridx,right,counts=right_relations(2);print('right',len(right),counts,flush=True)
 # Each exact negative cap lift couples one full left orbit and one right orbit.
 pairs=defaultdict(set)
 for i in inter['live']:
  a,n,u2,u1,L,q,c,s,v,w,t=inter['caps'][i]['core']
  for x,y in product(range(4),repeat=2):
   if x in (c,s,y) or y in (a,t):continue
   rj=ridx[p.canonical((s,x,y,t,w,v))]
   for b in range(4):
    if b in (a,c,q):continue
    row=''.join(map(str,p.canonical((x,y,a,b,c))))
    if row not in co.ROWS:continue
    lj=p.INDEX[p.canonical((a,b,q,L,u1,u2,n))]
    pairs[rj].add(lj)
 forb={rj:sum(1<<i for i in ls) for rj,ls in pairs.items()}
 hits=[];near=[];coverage=set()
 for rs,rc in right.items():
  bad=0
  for rj in rc['support_ids']:bad|=forb.get(rj,0)
  for ls,lc in left.items():
   # co.relations delta includes -1 original r; replace that with actual right delta.
   delta=lc['completed_delta']+1+rc['delta']
   if delta>=0:continue
   remaining=ls&bad
   if remaining:
    score=(remaining.bit_count(),delta)
    if len(near)<10 or score<near[-1][0]:
     near.append((score,len(near),{'left':lc,'right':rc,'delta':delta,'remaining_left_ids':[i for i in range(91) if remaining&(1<<i)]}));near.sort(key=lambda z:z[:2]);near=near[:10]
    continue
   hits.append({'left':lc,'right':rc,'delta':delta})
   for al in lc['alpha_ids']:
    for vw in rc['vw']:coverage.add((al,*vw))
 return {'source_live':len(inter['live']),'left_relations':len(left),'right_relations':len(right),'right_triangulations':counts,'hits':hits,'coverage':sorted(coverage),'near':[c for _,_,c in near],'seconds':time.monotonic()-start}
if __name__=='__main__':
 out=compute()
 with (D/'right-contractions.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('hits','near')}))
 print(json.dumps(out['hits'][:5] or out['near'][:2]))
