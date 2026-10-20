#!/usr/bin/env python3
"""Discovery only: exact r6 collar transfer and nonnegative core relaxation."""
import itertools,json
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
D=Path(__file__).resolve().parent
ROOT=D.parents[2]
OLD=ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2'
src=json.loads((OLD/'frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json').read_text())
controls=json.loads((OLD/'A/941-counted-candidate-probes.json').read_text())
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
def rgss(n,t=(0,)):
 if len(t)==n:
  if t[-1]!=t[0]:yield t
  return
 for c in range(min(3,max(t)+1)+1):
  if c!=t[-1]:yield from rgss(n,t+(c,))
eight=list(map(tuple,src['tuples']));ten=list(rgss(10));ind={t:i for i,t in enumerate(ten)}
assert ten==sorted(ten)
T=lil_matrix((274,len(ten)),dtype=np.int64)
for i,e in enumerate(eight):
 a,n,R,L,q,c,x,y=e
 for s,v,w,t,r in itertools.product(range(4),repeat=5):
  f=(a,n,R,L,q,c,s,v,w,t)
  if any(f[j]==f[(j+1)%10] for j in range(10)):continue
  if x in {s,r} or y in {t,r} or r in {s,v,w,t}:continue
  T[i,ind[canonical(f)]]+=1
T=T.tocsr()
print('T',T.shape,T.nnz,flush=True)
results=[]
for rec in controls['results']:
 z=rec['counts'];ans=linprog(np.zeros(len(ten)),A_eq=T,b_eq=z,bounds=(0,None))
 print(rec['candidate'],ans.success,ans.message,flush=True)
 if ans.success:
  print('support',sum(ans.x>1e-8),'maxresidual',max(abs(T@ans.x-z)),flush=True)
 results.append((rec['candidate'],ans))
# Maximal old count-control and accepted one-candidate all-three reject LP in core cone.
live=set(src['results'][2]['surviving_ids'])
zero=[i for i in range(274) if i not in live]
allowed=[j for j in range(len(ten)) if not any(T[i,j] for i in zero)]
print('941 cap-allowed columns',len(allowed),flush=True)
for name in ('Q1','Q2','GB'):
 p=json.loads((OLD/'frozen/audits/2026-10-18-smaller-bad-e1617a2/candidate-projections.json').read_text())['complete_local_records']
 forbidden=[i for i in live if p[i]['local_candidate_masks'][name]&82]
 cols=[j for j in allowed if not any(T[i,j] for i in forbidden)]
 target=np.array([int(bool(p[i]['local_candidate_masks'][name]&512)) for i in range(274)])@T[:,cols]
 ans=linprog(-target,A_ub=np.array([np.asarray(T[:,cols].sum(axis=0)).ravel()]),b_ub=[1],bounds=(0,None))
 print('candidate',name,'corecols',len(cols),'maxacc',None if not ans.success else -ans.fun,flush=True)
