"""Bounded independent signed-span discovery; exact dual if optimum zero."""
from pathlib import Path
import gzip,json,pickle,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import vstack,csr_matrix
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
D=Path(__file__).resolve().parent;C=D.parent/'counting';O=D.parent/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c'
with (C/'discovery.pickle').open('rb') as f:K,parts,E,U,M,sectors,orig=pickle.load(f)
I=json.load(gzip.open(O/'interface/certificate-v4.json.gz','rt'));n=len(K['states']);nc=len(K['columns']);live=sorted(I['live']);vs=live+list(range(n+nc,E.shape[1]));mat=E[-n:,vs].tocsr();norm=csr_matrix(np.r_[np.ones(len(live)),np.zeros(len(parts))]);mat=vstack([mat,norm]).tocsr();obj=U.toarray()[-1,vs];rhs=np.r_[np.zeros(n),1.]
print('span normalized',mat.shape,mat.nnz,flush=True);start=time.monotonic()
ans=linprog(obj,A_eq=mat,b_eq=rhs,bounds=[(0,None)]*len(live)+[(None,None)]*len(parts),method='highs-ipm',options={'time_limit':240})
print(ans.message,ans.fun,time.monotonic()-start,flush=True)
with (D/'span-normalized-result.pickle').open('xb') as f:pickle.dump((vs,ans),f)
out={'solver_message':ans.message,'solver_status':int(ans.status),'fun':ans.fun,'seconds':time.monotonic()-start,'source_excluded':False}
if ans.success:
 out['witness_sum']=-float(ans.fun)
 if ans.fun==0:
  rat=[Fraction(float(x)).limit_denominator(1000000) for x in ans.eqlin.marginals];scale=lcm(*(x.denominator for x in rat));vec=[int(x*scale) for x in rat];div=reduce(gcd,vec+[scale]);vec=[x//div for x in vec];scale//=div
  sums=[0]*len(vs);coo=mat.tocoo()
  for r,c,v in zip(coo.row,coo.col,coo.data):sums[c]+=int(v)*vec[r]
  targets=[int(x)*scale for x in obj]
  assert all(s<=t for s,t in zip(sums[:len(live)],targets[:len(live)]));assert sums[len(live):]==targets[len(live):];assert vec[-1]==0
  out.update({'scale':scale,'equality_multipliers':[[i,x] for i,x in enumerate(vec[:-1]) if x],'nonnegative_slacks':[[vs[i],targets[i]-sums[i]] for i in range(len(live)) if targets[i]!=sums[i]],'exact_valid':True})
with (D/'span-normalized.json').open('x') as f:json.dump(out,f,sort_keys=True);f.write('\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('equality_multipliers','nonnegative_slacks')}),flush=True)
