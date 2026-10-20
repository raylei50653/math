"""Find an exact rational separating functional; solver only discovers it."""
from pathlib import Path
import pickle
import gzip
import json
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction
from math import lcm, gcd
from functools import reduce

D=Path(__file__).resolve().parent
with (D/"discovery.pickle").open("rb") as f:
    K,parts,E,U,M,sectors,old_result=pickle.load(f)
n=len(K["states"]); nc=len(K["columns"])
OLD=D.parent/"frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c"
I=json.load(gzip.open(OLD/"interface/certificate-v4.json.gz","rt"))
live=set(I["live"])
livevars=sorted(live)+list(range(n,E.shape[1]))
EE=E[:,livevars].tocsr()
zvars=len(live)
bounds=[(0,None)]*(zvars+nc)+[(None,None)]*len(parts)
w=-U.toarray()[-1,:]
obj=-w[livevars]
print("start homogeneous dual", EE.shape,flush=True)
ans=linprog(obj,A_eq=EE,b_eq=np.zeros(EE.shape[0]),bounds=bounds,
            options={"time_limit":240})
print(ans.message,ans.fun,flush=True)
with (D/"homogeneous-dual.pickle").open("xb") as f:
    pickle.dump((livevars,ans),f)
if not ans.success:
    raise SystemExit("No certificate extracted; the solver status above is not a theorem.")
rat=[Fraction(float(v)).limit_denominator(1000000) for v in ans.eqlin.marginals]
mult=lcm(*(v.denominator for v in rat))
vec=[int(v*mult) for v in rat]
div=reduce(gcd,vec+[mult]);vec=[v//div for v in vec];mult//=div
coo=EE.tocoo();sums=[0]*EE.shape[1]
for r,c,v in zip(coo.row,coo.col,coo.data):
    sums[c]+=int(v)*vec[r]
target=[int(v)*mult for v in obj]
assert all(v<=t for v,t in zip(sums[:zvars+nc],target[:zvars+nc]))
assert sums[zvars+nc:]==target[zvars+nc:]
data={"status":"exact rational separating functional",
      "target":"sum of the two short-witness canonical core fibres",
      "witness_ids":[r["canonical_id"] for r in I["witnesses"]],
      "multiplier":mult,
      "equality_multipliers":[[i,v] for i,v in enumerate(vec) if v],
      "nonnegative_slacks":[[livevars[i],target[i]-sums[i]] for i in range(zvars+nc) if target[i]!=sums[i]],
      "source_excluded":True}
with (D/"dual-certificate.json").open("x") as f:
    json.dump(data,f,separators=(",",":"));f.write("\n")
print(json.dumps({"multipliers":len(data["equality_multipliers"]),
                  "scale":mult,"slacks":len(data["nonnegative_slacks"])}),flush=True)
