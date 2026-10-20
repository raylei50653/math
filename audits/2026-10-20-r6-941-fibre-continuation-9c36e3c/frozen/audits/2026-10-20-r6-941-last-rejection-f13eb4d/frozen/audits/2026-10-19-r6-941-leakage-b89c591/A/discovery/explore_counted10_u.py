#!/usr/bin/env python3
"""Discovery only: intersect C10 counted cone with full U319 source zeros."""
import itertools,json,pickle
from pathlib import Path
import numpy as np
from scipy.sparse import hstack,vstack,csr_matrix
from scipy.optimize import linprog
D=Path(__file__).resolve().parent;ROOT=D.parents[2];OLD=ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2'
with (D/'counted10-discovery.pickle').open('rb') as f:ten,rows,hist,columns,descriptions,T,A=pickle.load(f)
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
forbidden=[]
for i,(a,n,R,L,q,c,s,v,w,t) in enumerate(ten):
 if a!=c:continue
 row=''.join(map(str,canonical((a,s,v,w,t))))
 if row not in ROWS:continue
 if row not in ('01212','01213','01232'):continue
 lifts=[(p,h) for p,h in itertools.product(range(4),repeat=2) if p not in {a,q,h,n} and h not in {p,q,L,R,n}]
 if lifts:forbidden.append(i)
print('U319 forbidden',len(forbidden),flush=True)
bounds=[(0,0) if j in forbidden else (0,None) for j in range(len(ten))]+[(0,None)]*len(columns)
controls=json.loads((OLD/'A/941-counted-candidate-probes.json').read_text())
AA=vstack([A,hstack([T,csr_matrix((274,len(columns)))])]).tocsr()
for rec in controls['results']:
 z=rec['counts'];ans=linprog(np.zeros(A.shape[1]),A_eq=AA,b_eq=np.array([0]*len(rows)+z),bounds=bounds)
 print('OLD U319',rec['candidate'],ans.success,ans.message,flush=True)
 if ans.success:
  print('supportZ',sum(ans.x[:len(ten)]>1e-8),'supportW',sum(ans.x[len(ten):]>1e-8),'resid',max(abs(AA@ans.x-np.array([0]*len(rows)+z))),flush=True)
  with (D/('counted10-u-old-'+rec['candidate']+'.pickle')).open('wb') as f:pickle.dump(ans.x,f)
