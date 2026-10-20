#!/usr/bin/env python3
# Discovery only; no graph realizability is inferred.
from pathlib import Path
exec((Path(__file__).parent/'explore_composed.py').read_text().split('catalogue=')[0])
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix,csr_matrix,hstack,vstack,eye
parts=[p for p in m.growth(10) if m.proper(p) and m.noncrossing(p)]
assert len(parts)==603
n=len(ten);k=len(K['columns']);ns=len(parts)
A=lil_matrix((len(K['hrows']),n+k),dtype=np.int64)
for r,i in enumerate(K['rowids']):A[r,i]=-K['hsize'][r]
for j,col in enumerate(K['columns']):
 for r,v in col:A[r,n+j]=v
P=np.ones((n,ns),dtype=np.int64);ts=np.array(ten)
for j,p in enumerate(parts):
 for i in range(10):
  for q in range(i):
   if p[i]==p[q]:P[:,j]*=(ts[:,i]==ts[:,q])
E=vstack([hstack([A.tocsr(),csr_matrix((A.shape[0],ns))]),hstack([eye(n),csr_matrix((n,k)),-csr_matrix(P)])]).tocsr()
bounds=[(0,None) if i in set(live) else (0,0) for i in range(n)]+[(0,None)]*k+[(None,None)]*ns
pos=[C[r] for r in range(10) if 941>>r&1]
pos += [M[r] for M in Hs for r in range(1,10)]
pos += [M[r] for j,M in enumerate(Ms) for r in range(10) if not(j in range(12,16) and r==0)]
U=hstack([-csr_matrix(np.array(pos)),csr_matrix((len(pos),k+ns))]).tocsr()
print('LP size',E.shape,U.shape,flush=True)
a=linprog(np.r_[np.ones(n),np.zeros(k+ns)],A_eq=E,b_eq=np.zeros(E.shape[0]),A_ub=U,b_ub=-np.ones(len(pos)),bounds=bounds)
print('LP',a.success,a.message,flush=True)
if a.success:
 print('residual',max(abs(E@a.x)),'support',sum(a.x[:n]>1e-7),flush=True)
 np.savez(Path(__file__).parent/'counted-discovery.npz',x=a.x)
 print('core denominators',sorted({str(__import__('fractions').Fraction(float(v)).limit_denominator(10000).denominator) for v in a.x[:n]}),flush=True)
