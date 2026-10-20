#!/usr/bin/env python3
"""Discovery of the exact C10 counted necessary cone; no source realization."""
from collections import Counter,defaultdict
import itertools,json,time,pickle
from pathlib import Path
import numpy as np
from scipy.sparse import lil_matrix,hstack,vstack,csr_matrix
from scipy.optimize import linprog
D=Path(__file__).resolve().parent
ROOT=D.parents[2]
OLD=ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2'
src=json.loads((OLD/'frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json').read_text())
controls=json.loads((OLD/'A/941-counted-candidate-probes.json').read_text())
perms=[p for p in itertools.permutations(range(4)) if p[0]//2==p[1]//2 and p[2]//2==p[3]//2]
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
def rgss(n,t=(0,)):
 if len(t)==n:
  if t[-1]!=t[0]:yield t
  return
 for c in range(min(3,max(t)+1)+1):
  if c!=t[-1]:yield from rgss(n,t+(c,))
def partitions(n,t=(0,)):
 if len(t)==n:yield t;return
 for c in range(max(t)+2):yield from partitions(n,t+(c,))
def literal(n,t=()):
 if len(t)==n:
  if t[-1]!=t[0]:yield t
  return
 for c in range(4):
  if not t or c!=t[-1]:yield from literal(n,t+(c,))
def hc(t):return min(tuple(p[x] for x in t) for p in perms)
eight=list(map(tuple,src['tuples']));ten=list(rgss(10));ind={t:i for i,t in enumerate(ten)}
T=lil_matrix((274,len(ten)),dtype=np.int64)
for i,e in enumerate(eight):
 a,n,R,L,q,c,x,y=e
 for s,v,w,t,r in itertools.product(range(4),repeat=5):
  f=(a,n,R,L,q,c,s,v,w,t)
  if any(f[j]==f[(j+1)%10] for j in range(10)):continue
  if x in {s,r} or y in {t,r} or r in {s,v,w,t}:continue
  T[i,ind[canonical(f)]]+=1
T=T.tocsr()
now=time.time()
lits=list(literal(10));hist=Counter(hc(t) for t in lits);rows=sorted(hist);ri={t:i for i,t in enumerate(rows)}
li={t:ri[hc(t)] for t in lits}
print('rows',len(rows),'time',time.time()-now,flush=True)
sideparts=defaultdict(list);nc=0;eligible=0
fours=list(itertools.combinations(range(10),4))
for p in partitions(10):
 if any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b] for a,b,c,d in fours):continue
 nc+=1;b=max(p)+1
 if sum(p[i]!=p[(i+1)%10] for i in range(10))!=2*(b-1):continue
 adjacency=[set() for _ in range(b)]
 for a,c in zip(p,p[1:]+p[:1]):
  if a!=c:adjacency[a].add(c);adjacency[c].add(a)
 val=[None]*b;val[0]=0;stack=[0];okay=True
 while stack:
  a=stack.pop()
  for c in adjacency[a]:
   if val[c] is None:val[c]=1-val[a];stack.append(c)
   elif val[c]==val[a]:okay=False
 if not okay:continue
 assert all(x is not None for x in val)
 side=tuple(val[x] for x in p)
 sideparts[side].append(p);sideparts[tuple(1-x for x in side)].append(p);eligible+=1
print('nc',nc,'eligible',eligible,'time',time.time()-now,flush=True)
cols={}
for t in rows:
 for p in sideparts[tuple(c//2 for c in t)]:
  b=max(p)+1
  orbit=[tuple(c^1 if subset&(1<<p[i]) else c for i,c in enumerate(t)) for subset in range(1<<b)]
  col=tuple(sorted(Counter(li[x] for x in orbit).items()))
  cols.setdefault(col,(t,p))
print('columns',len(cols),'time',time.time()-now,flush=True)
columns=sorted(cols)
A=lil_matrix((len(rows),len(ten)+len(cols)),dtype=np.int64)
for r,t in enumerate(rows):A[r,ind[canonical(t)]]=-hist[t]
for j,col in enumerate(columns):
 for r,v in col:A[r,len(ten)+j]=v
A=A.tocsr();print('matrix',A.shape,A.nnz,flush=True)
# Save temporary discovery matrix for root/research only; no replay authority.
with (D/'counted10-discovery.pickle').open('wb') as f:pickle.dump((ten,rows,hist,columns,cols,T,A),f)
for rec in controls['results']:
 z=rec['counts'];AA=vstack([A,hstack([T,csr_matrix((274,len(cols)))])]).tocsr()
 ans=linprog(np.zeros(A.shape[1]),A_eq=AA,b_eq=np.array([0]*len(rows)+z),bounds=(0,None))
 print('OLD',rec['candidate'],ans.success,ans.message,flush=True)
 if ans.success:
  print('supportZ',sum(ans.x[:len(ten)]>1e-8),'supportW',sum(ans.x[len(ten):]>1e-8),'resid',max(abs(AA@ans.x-np.array([0]*len(rows)+z))),flush=True)
  with (D/('counted10-old-'+rec['candidate']+'.pickle')).open('wb') as f:pickle.dump(ans.x,f)
