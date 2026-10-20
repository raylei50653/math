#!/usr/bin/env python3
"""Discovery-only reduced orbit-cone dual; exact full lift before certification."""
from pathlib import Path
from fractions import Fraction
from functools import reduce
from math import lcm,gcd
import pickle,json,gzip,time
import numpy as np
from scipy.sparse import csr_matrix,hstack,vstack
from scipy.optimize import linprog
D=Path(__file__).resolve().parent
with (D.parent/'counting/discovery.pickle').open('rb') as src:K,parts,E,U,M,sectors,old=pickle.load(src)
I=json.load(gzip.open(D.parent/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c/interface/certificate-v4.json.gz','rt'))
n=len(K['states']);nh=len(K['hrows']);nc=len(K['columns']);live=set(I['live'])
good=[j for j,col in enumerate(K['columns']) if all(K['rowids'][r] in live for r,v in col)]
hlive=[r for r,i in enumerate(K['rowids']) if i in live]
eqrows=hlive+list(range(nh,nh+n));nnvars=sorted(live)+[n+j for j in good]
Er=E[eqrows,:]
positive=-U[:,:n].toarray()
Aub=hstack([Er[:,nnvars].T,csr_matrix(np.hstack([positive[:,sorted(live)],np.zeros((10,len(good)))]).T)]).tocsr()
Aeq=vstack([hstack([Er[:,n+nc:].T,csr_matrix((len(parts),10))]),csr_matrix(([1]*10,([0]*10,range(len(eqrows),len(eqrows)+10))),shape=(1,len(eqrows)+10))]).tocsr()
b=np.r_[np.zeros(len(parts)),1]
print(json.dumps({'good_orbits':len(good),'removed_orbits':nc-len(good),'halfrows':len(hlive),'dual_vars':len(eqrows)+10,'inequalities':Aub.shape[0],'equalities':Aeq.shape[0]}),flush=True)
start=time.monotonic();ans=linprog(np.zeros(len(eqrows)+10),A_ub=Aub,b_ub=np.zeros(Aub.shape[0]),A_eq=Aeq,b_eq=b,bounds=[(None,None)]*len(eqrows)+[(0,None)]*10,method='highs-ds',options={'time_limit':240,'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
print(json.dumps({'status':ans.message,'elapsed':time.monotonic()-start}),flush=True)
with (D/'reduced-dual-discovery.pickle').open('xb') as dst:pickle.dump((eqrows,good,ans),dst)
assert ans.success,ans.message
rat=[Fraction(float(v)).limit_denominator(1000000) for v in ans.x]
mul=lcm(*(v.denominator for v in rat));vv=[int(v*mul) for v in rat];div=reduce(gcd,vv);vv=[v//div for v in vv]
eq=[0]*E.shape[0]
for r,v in zip(eqrows,vv):eq[r]=v
weights=vv[len(eqrows):]
assert all(w>=0 for w in weights) and sum(weights)>0
# Each discarded orbit meets a zero core. Add one common positive multiplier
# to every deleted zero-core halfrow to make all discarded orbit slacks valid.
need=0
for j in range(nc):
 col=K['columns'][j];value=sum(eq[r]*v for r,v in col)
 if j not in good and value<0:
  denom=sum(v for r,v in col if K['rowids'][r] not in live)
  assert denom>0;need=max(need,(-value+denom-1)//denom)
for r,i in enumerate(K['rowids']):
 if i not in live:eq[r]=need
full=E.tocoo();sums=[0]*E.shape[1]
for r,c,v in zip(full.row,full.col,full.data):sums[c]+=int(v)*eq[r]
for j,w in enumerate(weights):
 if w:
  for i in live:sums[i]+=w*int(positive[j,i])
assert all(sums[i]<=0 for i in live)
assert all(sums[n+j]<=0 for j in range(nc))
assert not any(sums[n+nc:])
out={'status':'exact integer Farkas certificate','equality_multipliers':[[i,v] for i,v in enumerate(eq) if v],'positive_row_multipliers':[[i,v] for i,v in enumerate(weights) if v],'nonnegative_slacks':[[i,-sums[i]] for i in sorted(live)+list(range(n,n+nc)) if sums[i]],'positive_weight_sum':sum(weights)}
with (D/'reduced-farkas-certificate.json').open('x') as dst:json.dump(out,dst,separators=(',',':'));dst.write('\n')
print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in out.items()}),flush=True)
