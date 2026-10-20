"""Solve the separating-functional feasibility problem directly, then exact-check."""
from pathlib import Path
from scipy.sparse import hstack,vstack,csr_matrix
from scipy.optimize import linprog
import numpy as np
import pickle,json,gzip
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
D=Path(__file__).resolve().parent
with (D/"discovery.pickle").open("rb") as f:
    K,parts,E,U,M,sectors,old=pickle.load(f)
n=len(K["states"]);nc=len(K["columns"]);nh=len(K["hrows"])
OLD=D.parent/"frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c"
I=json.load(gzip.open(OLD/"interface/certificate-v4.json.gz","rt"))
live=sorted(I["live"]);variables=live+list(range(n,E.shape[1]))
EE=E[:,variables].tocsr();P=-U[:,variables].tocsr()
nn=len(live)+nc
ineq=hstack([EE.T[:nn],P.T[:nn]]).tocsr()
eq=vstack([hstack([EE.T[nn:],P.T[nn:]]),
           csr_matrix([[0]*E.shape[0]+[1]*U.shape[0]])]).tocsr()
print("direct dual",ineq.shape,eq.shape,flush=True)
ans=linprog(np.zeros(E.shape[0]+U.shape[0]),A_ub=ineq,b_ub=np.zeros(nn),
            A_eq=eq,b_eq=np.r_[np.zeros(len(parts)),1],
            bounds=[(None,None)]*E.shape[0]+[(0,None)]*U.shape[0],
            method="highs-ipm",options={"time_limit":480})
print(ans.message,flush=True)
with (D/"direct-dual.pickle").open("xb") as f:
    pickle.dump(ans,f)
assert ans.success
rat=[Fraction(float(v)).limit_denominator(1000000) for v in ans.x]
mul=lcm(*(v.denominator for v in rat))
vec=[int(v*mul) for v in rat];div=reduce(gcd,vec);vec=[v//div for v in vec]
y,weights=vec[:E.shape[0]],vec[E.shape[0]:]
sums=[0]*EE.shape[1];coo=EE.tocoo()
for r,c,v in zip(coo.row,coo.col,coo.data):sums[c]+=int(v)*y[r]
coo=P.tocoo()
for r,c,v in zip(coo.row,coo.col,coo.data):sums[c]+=int(v)*weights[r]
assert min(weights)>=0 and sum(weights)>0
assert max(sums[:nn])<=0 and not any(sums[nn:])
out={"status":"exact integer Farkas certificate",
     "equality_multipliers":[[i,v] for i,v in enumerate(y) if v],
     "positive_row_multipliers":[[i,v] for i,v in enumerate(weights) if v],
     "nonnegative_slacks":[[variables[i],-v] for i,v in enumerate(sums[:nn]) if v],
     "positive_weight_sum":sum(weights)}
with (D/"farkas-certificate.json").open("x") as f:
    json.dump(out,f,separators=(",",":"));f.write("\n")
print({k:(len(v) if isinstance(v,list) else v) for k,v in out.items()},flush=True)
