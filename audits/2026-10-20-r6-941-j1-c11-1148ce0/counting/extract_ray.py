"""Discover a Farkas ray and verify it with exact integers before saving."""
from pathlib import Path
from scipy.optimize._highspy import _core as h
from scipy.sparse import vstack
import numpy as np
import json,gzip,pickle
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
D=Path(__file__).resolve().parent
with (D/"discovery.pickle").open("rb") as f:
    K,parts,E,U,M,sectors,old=pickle.load(f)
n=len(K["states"]);nc=len(K["columns"])
OLD=D.parent/"frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c"
I=json.load(gzip.open(OLD/"interface/certificate-v4.json.gz","rt"))
live=sorted(I["live"])
variables=live+list(range(n,E.shape[1]))
AA=vstack([E,U])[:,variables].tocsc()
lp=h.HighsLp()
lp.num_col_=AA.shape[1];lp.num_row_=AA.shape[0]
lp.col_cost_=np.r_[np.ones(len(live)),np.zeros(nc+len(parts))]
lp.col_lower_=np.r_[np.zeros(len(live)+nc),np.full(len(parts),-h.kHighsInf)]
lp.col_upper_=np.full(AA.shape[1],h.kHighsInf)
lp.row_lower_=np.r_[np.zeros(E.shape[0]),np.full(U.shape[0],-h.kHighsInf)]
lp.row_upper_=np.r_[np.zeros(E.shape[0]),-np.ones(U.shape[0])]
lp.a_matrix_.format_=h.MatrixFormat.kColwise
lp.a_matrix_.start_=AA.indptr
lp.a_matrix_.index_=AA.indices
lp.a_matrix_.value_=AA.data
solver=h._Highs()
solver.setOptionValue("time_limit",240.0)
solver.passModel(lp)
solver.run()
print("status",solver.getModelStatus(),flush=True)
status,exists,ray=solver.getDualRay()
assert exists,(status,exists)
with (D/"dual-ray.pickle").open("xb") as f:
    pickle.dump((variables,ray),f)
rat=[Fraction(float(v)).limit_denominator(1000000) for v in ray]
mul=lcm(*(v.denominator for v in rat))
vec=[int(v*mul) for v in rat];div=reduce(gcd,vec);vec=[v//div for v in vec]
coo=AA.tocoo();sums=[0]*AA.shape[1]
for r,c,v in zip(coo.row,coo.col,coo.data):sums[c]+=int(v)*vec[r]
if sum(vec[E.shape[0]:])>0:
    vec=[-v for v in vec];sums=[-v for v in sums]
assert all(v<=0 for v in vec[E.shape[0]:]) and sum(vec[E.shape[0]:])<0
assert all(v<=0 for v in sums[:len(live)+nc])
assert not any(sums[len(live)+nc:])
out={"status":"exact integer Farkas certificate",
     "equality_multipliers":[[i,v] for i,v in enumerate(vec[:E.shape[0]]) if v],
     "positive_row_multipliers":[[i,-v] for i,v in enumerate(vec[E.shape[0]:]) if v],
     "nonnegative_slacks":[[variables[i],-v] for i,v in enumerate(sums[:len(live)+nc]) if v],
     "positive_weight_sum":-sum(vec[E.shape[0]:])}
with (D/"farkas-certificate.json").open("x") as f:
    json.dump(out,f,separators=(",",":"));f.write("\n")
print({k:(len(v) if isinstance(v,list) else v) for k,v in out.items()},flush=True)
