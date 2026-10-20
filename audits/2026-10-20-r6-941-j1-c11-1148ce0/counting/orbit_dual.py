"""Find and exactly verify a separator using only complete orbit counts."""
from pathlib import Path
import pickle,gzip,json
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
import numpy as np
from scipy.optimize import linprog
D=Path(__file__).resolve().parent
with (D/"discovery.pickle").open("rb") as f:
    K,parts,E,U,M,sectors,old=pickle.load(f)
n=len(K["states"]);nh=len(K["hrows"]);nc=len(K["columns"])
OLD=D.parent/"frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c"
I=json.load(gzip.open(OLD/"interface/certificate-v4.json.gz","rt"))
live=sorted(I["live"]);ls=set(live)
rows=[r for r,i in enumerate(K["rowids"]) if i in ls]
good=[j for j,col in enumerate(K["columns"]) if all(K["rowids"][r] in ls for r,v in col)]
variables=live+[n+j for j in good]
T=E[rows,:n+nc][:,variables].tocsr()
w=(-U[-1,:n+nc]).toarray()[0]
print("orbit only",T.shape,flush=True)
ans=linprog(-w[variables],A_eq=T,b_eq=np.zeros(len(rows)),bounds=(0,None),
            options={"time_limit":240})
print(ans.message,ans.fun,flush=True)
with (D/"orbit-dual.pickle").open("xb") as f:pickle.dump((rows,good,ans),f)
assert ans.success and abs(ans.fun)<1e-8
rat=[Fraction(float(v)).limit_denominator(1000000) for v in ans.eqlin.marginals]
scale=lcm(*(v.denominator for v in rat))
y=[0]*nh
for r,v in zip(rows,rat):y[r]=int(v*scale)
div=reduce(gcd,y+[scale]);y=[v//div for v in y];scale//=div
# Extend the reduced dual to every original column: deleted halfrows refer
# only to already-proved zero core fibres, so their coefficients are free.
dead=set(range(nh))-set(rows)
extension=0
for col in K["columns"]:
    den=sum(v for r,v in col if r in dead)
    if den:
        need=-sum(y[r]*v for r,v in col)
        extension=max(extension,-(-need//den))
for r in dead:y[r]=extension
core=[0]*n
for r,i in enumerate(K["rowids"]):core[i]+=K["hsize"][r]*y[r]
for rec in I["witnesses"]:core[rec["canonical_id"]]+=scale
orb=[-sum(y[r]*v for r,v in col) for col in K["columns"]]
assert all(core[i]<=0 for i in live)
assert max(orb)<=0
slacks=[[i,-core[i]] for i in live if core[i]]
slacks += [[n+j,-v] for j,v in enumerate(orb) if v]
out={"status":"exact integer Farkas certificate",
     "equality_multipliers":[[i,v] for i,v in enumerate(y) if v],
     "positive_row_multipliers":[[9,scale]],
     "nonnegative_slacks":slacks,
     "positive_weight_sum":scale}
with (D/"orbit-farkas-certificate.json").open("x") as f:
    json.dump(out,f,separators=(",",":"));f.write("\n")
print({"scale":scale,"extension":extension,"nonzero_multipliers":len(out["equality_multipliers"]),
       "nonzero_slacks":len(slacks),"max_coefficient":max(map(abs,y))},flush=True)
