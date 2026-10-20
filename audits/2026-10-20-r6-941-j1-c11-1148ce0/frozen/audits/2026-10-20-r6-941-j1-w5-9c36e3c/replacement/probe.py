#!/usr/bin/env python3
"""Narrow exact seven-rim replacement search. No source-realization inference."""
from itertools import product, combinations
from collections import defaultdict, Counter
from pathlib import Path
import json, hashlib, argparse, time
ROOT=Path(__file__).resolve().parent
RIM=('a','b','q','L','u1','u2','n')
FACES=('abp','bpq','pqh','phn','pna','hqL','hLR','hRn','Rnu2','Ru2u1','Ru1L')
# Explicit tuples avoid parsing multi-character names.
OFACES=[('a','b','p'),('b','p','q'),('p','q','h'),('p','h','n'),('p','n','a'),('h','q','L'),('h','L','R'),('h','R','n'),('R','n','u2'),('R','u2','u1'),('R','u1','L')]
BOUND={tuple(sorted((i,(i+1)%7))) for i in range(7)}
def growth(n,t=(0,)):
 if len(t)==n:
  yield t;return
 for c in range(min(3,max(t)+1)+1):yield from growth(n,t+(c,))
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
def proper(t):return all(t[i]!=t[(i+1)%7] for i in range(7))
STATES=[t for t in growth(7) if proper(t)];INDEX={t:i for i,t in enumerate(STATES)}
OE={tuple(sorted(e)) for f in OFACES for e in combinations(f,2)}
OLIFTS=[]
for t in STATES:
 c=dict(zip(RIM,t));li=[]
 for phR in product(range(4),repeat=3):
  c.update(zip(('p','h','R'),phR))
  if all(c[u]!=c[v] for u,v in OE):li.append(phR)
 OLIFTS.append(li)
ORIGINAL=sum((1<<i) for i,li in enumerate(OLIFTS) if li)
ALPHA=[(0,1,2,1,0,2,1),(0,1,2,1,2,0,1)]
ALPHA_IDS=[INDEX[canonical(t)] for t in ALPHA]
def all_triangulations(k):
 # Flip-connected enumeration of simple triangulations of this topological disk.
 fs=[(0,j,j+1) for j in range(1,6)]
 for v in range(7,7+k):
  f=fs.pop(0);fs.extend(tuple(sorted((v,*e))) for e in combinations(f,2))
 initial=tuple(sorted(tuple(sorted(f)) for f in fs));seen={initial};queue=[initial]
 for faces in queue:
  yield faces
  edge_faces=defaultdict(list)
  for f in faces:
   for e in combinations(f,2):edge_faces[e].append(f)
  for e,fl in edge_faces.items():
   if len(fl)!=2:continue
   a=next(v for v in fl[0] if v not in e);b=next(v for v in fl[1] if v not in e)
   if tuple(sorted((a,b))) in edge_faces:continue
   new=tuple(sorted(set(faces)-set(fl)|{tuple(sorted((a,b,e[0]))),tuple(sorted((a,b,e[1])))}))
   if new not in seen:seen.add(new);queue.append(new)
def search(k, forbidden=None):
 start=time.monotonic();stats=Counter();hits=[];best=[];alphacover=Counter()
 for faces in all_triangulations(k):
  stats['triangulations']+=1
  edges=sorted({e for f in faces for e in combinations(f,2)})
  newedges=[e for e in edges if e not in BOUND]
  assert len(newedges)==3*k+4
  signatures=defaultdict(int)
  # All labels (= contractions or != retained edges) at once. Each whole
  # assignment belongs to one complete signature, no per-vertex marginals.
  for i,t in enumerate(STATES):
   bit=1<<i
   for extra in product(range(4),repeat=k):
    c=t+extra
    sig=sum(1<<j for j,(u,v) in enumerate(newedges) if c[u]==c[v])
    signatures[sig]|=bit
  stats['nonempty_labelled_relations']+=len(signatures)
  for sig,support in signatures.items():
   alpha=[a for a in ALPHA_IDS if support&(1<<a)]
   if not alpha:continue
   stats['alpha_relations']+=1
   bad=support&(~ORIGINAL if forbidden is None else forbidden)
   for a in alpha:alphacover[(a,bad.bit_count())]+=1
   if bad:
    if len(best)<10 or bad.bit_count()<best[-1][0]:
     best.append((bad.bit_count(),len(best),{'faces':faces,'new_edges':newedges,'equal_signature':sig,'alpha_ids':alpha,'unsupported_rim_ids':[i for i in range(91) if bad&(1<<i)]}));best.sort(key=lambda z:z[:2]);best=best[:10]
    continue
   # The quotient is colourable, hence no retained edge becomes a loop.
   # Completed cost must count actual equivalence classes, including centers.
   par=list(range(7+k))
   def find(x):
    while par[x]!=x:x=par[x]
    return x
   for j,(u,v) in enumerate(newedges):
    if sig&(1<<j):par[find(u)]=find(v)
   classes=tuple(tuple(i for i in range(7+k) if find(i)==r) for r in sorted({find(i) for i in range(7+k)}))
   delta=len(classes)-7-3
   if delta>=0:continue
   hits.append({'faces':faces,'new_edges':newedges,'equal_signature':sig,'classes':classes,'alpha_ids':alpha,'support_ids':[i for i in range(91) if support&(1<<i)],'completed_delta':delta})
 stats['hits']=len(hits)
 return {'interior':k,'stats':dict(stats),'seconds':round(time.monotonic()-start,3),'hits':hits,'best_near_misses':[x[2] for x in best],'alpha_bad_histogram':[[a,b,n] for (a,b),n in sorted(alphacover.items())]}
def main():
 p=argparse.ArgumentParser();p.add_argument('--max-interior',type=int,default=1);p.add_argument('--build',action='store_true');p.add_argument('--interface',action='store_true');a=p.parse_args()
 forbidden=None
 if a.interface:
  import gzip
  with gzip.open(ROOT.parent/'interface/certificate.json.gz','rt') as f:interface=json.load(f)
  forbidden=0
  for i in interface['live']:
   cap=interface['caps'][i];aa,n,u2,u1,L,q,c,ss,v,w,tt=cap['core']
   for b in range(4):
    if b in (aa,c,q):continue
    if any(''.join(map(str,canonical((x,y,aa,b,c)))) in ('01021','01202','01212') for x,y,r in cap['right_xyr']):
     forbidden |= 1<<INDEX[canonical((aa,b,q,L,u1,u2,n))]
  print(json.dumps({'forbidden_ids':[i for i in range(91) if forbidden&(1<<i)],'alpha_forbidden':[bool(forbidden&(1<<i)) for i in ALPHA_IDS]}))
 result={'rim':RIM,'states':STATES,'original_lifts':OLIFTS,'alpha_ids':ALPHA_IDS,'forbidden_ids':None if forbidden is None else [i for i in range(91) if forbidden&(1<<i)],'search':[search(k,forbidden) for k in range(a.max_interior+1)],'limit':'Universal original-patch-sound seven-rim replacements with 0 through max-interior new vertices, formed by a simple triangulation and marking every new edge =/!=. Exterior-edge legality of rim contractions still requires a source geometry proof. No actual source realization asserted.'}
 if a.build:
  with (ROOT/f'{"interface-" if a.interface else ""}search-{a.max_interior}.json').open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k in ('rim','alpha_ids')}))
 for r in result['search']:print(json.dumps({k:v for k,v in r.items() if k not in ('hits','best_near_misses','alpha_bad_histogram')}))
 if result['search'][-1]['hits']:print(json.dumps(result['search'][-1]['hits'][:5]))
if __name__=='__main__':main()
