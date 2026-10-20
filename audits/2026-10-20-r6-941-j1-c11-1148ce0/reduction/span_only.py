"""Independent signed-span-only numerical dual discovery, then exact verification."""
from pathlib import Path
import gzip,json,pickle,time
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
D=Path(__file__).resolve().parent;C=D.parent/'counting';O=D.parent/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c'
with (C/'discovery.pickle').open('rb') as f:K,parts,E,U,M,sectors,orig=pickle.load(f)
I=json.load(gzip.open(O/'interface/certificate-v4.json.gz','rt'));n=len(K['states']);nc=len(K['columns']);live=sorted(I['live']);vars=live+list(range(n+nc,E.shape[1]));mat=E[-n:,vars].tocsr();obj=-U.toarray()[-1,vars];obj=-obj
print('span-only',mat.shape,mat.nnz,flush=True);start=time.monotonic()
ans=linprog(obj,A_eq=mat,b_eq=np.zeros(n),bounds=[(0,None)]*len(live)+[(None,None)]*len(parts),options={'time_limit':240})
print(ans.message,ans.fun,time.monotonic()-start,flush=True)
with (D/'span-only-result.pickle').open('xb') as f:pickle.dump((vars,ans),f)
out={'solver_message':ans.message,'solver_status':int(ans.status),'fun':ans.fun,'seconds':time.monotonic()-start,'source_excluded':False}
if ans.success:
 rat=[Fraction(float(x)).limit_denominator(1000000) for x in ans.eqlin.marginals];scale=lcm(*(x.denominator for x in rat));vec=[int(x*scale) for x in rat];div=reduce(gcd,vec+[scale]);vec=[x//div for x in vec];scale//=div
 sums=[0]*len(vars);coo=mat.tocoo()
 for r,c,v in zip(coo.row,coo.col,coo.data):sums[c]+=int(v)*vec[r]
 targets=[int(x)*scale for x in obj]
 assert all(s<=t for s,t in zip(sums[:len(live)],targets[:len(live)]))
 assert sums[len(live):]==targets[len(live):]
 out.update({'scale':scale,'equality_multipliers':[[i,x] for i,x in enumerate(vec) if x],'nonnegative_slacks':[[vars[i],targets[i]-sums[i]] for i in range(len(live)) if targets[i]!=sums[i]],'exact_valid':True})
with (D/'span-only.json').open('x') as f:json.dump(out,f,sort_keys=True);f.write('\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('equality_multipliers','nonnegative_slacks')}),flush=True)
