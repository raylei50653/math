#!/usr/bin/env python3
"""Discovery only: strongest joint C10 necessary model under consideration."""
import itertools,json,pickle,time
from pathlib import Path
import numpy as np
from scipy.sparse import hstack,vstack,csr_matrix,eye
from scipy.optimize import linprog
D=Path(__file__).resolve().parent;ROOT=D.parents[2];OLD=ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2'
with (D/'counted10-discovery.pickle').open('rb') as f:ten,rows,hist,columns,descriptions,T,A=pickle.load(f)
u=json.loads((D.parent/'C/u319-core.json').read_text());print(u.keys(),flush=True)
forbidden=u['forbidden_ids']
def growth(n,p=(0,)):
 if len(p)==n:yield p;return
 for x in range(max(p)+2):yield from growth(n,p+(x,))
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
fours=list(itertools.combinations(range(10),4))
parts=[p for p in growth(10) if proper(p) and not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in fours)]
B=np.ones((len(ten),len(parts)),dtype=np.int64);ts=np.array(ten)
for j,p in enumerate(parts):
 for i in range(10):
  old=next((k for k in range(i) if p[k]==p[i]),None)
  if old is not None:B[:,j]&=ts[:,i]==ts[:,old]
B=csr_matrix(B);n=len(ten);k=len(columns);m=len(parts)
print('planar columns',m,flush=True)
AA=vstack([hstack([A,csr_matrix((len(rows),m))]),hstack([eye(n),csr_matrix((n,k)),-B]),hstack([T,csr_matrix((274,k+m))])]).tocsr()
bounds=[(0,0) if j in forbidden else (0,None) for j in range(n)]+[(0,None)]*k+[(None,None)]*m
controls=json.loads((OLD/'A/941-counted-candidate-probes.json').read_text())
for rec in controls['results']:
 z=rec['counts'];bb=np.array([0]*(len(rows)+n)+z)
 fit=linprog(np.zeros(n+k+m),A_eq=AA,b_eq=bb,bounds=bounds)
 print('COMBINED',rec['candidate'],fit.success,fit.message,flush=True)
 if fit.success:
  print('Zsupport',sum(fit.x[:n]>1e-8),'Wsupport',sum(fit.x[n:n+k]>1e-8),'Csupport',sum(abs(fit.x[n+k:])>1e-8),'maxresidual',max(abs(AA@fit.x-bb)),flush=True)
  with (D/('combined-old-'+rec['candidate']+'.pickle')).open('wb') as f:pickle.dump(fit.x,f)
with (D/'combined-matrix.pickle').open('wb') as f:pickle.dump((AA,B,bounds),f)
