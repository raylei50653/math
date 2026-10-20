from fractions import Fraction as F
from math import lcm,gcd
from functools import reduce
from pathlib import Path
import pickle,json,numpy as np
D=Path(__file__).resolve().parent
with (D/'counted10-discovery.pickle').open('rb') as f:ten,rows,hist,columns,descriptions,T,A=pickle.load(f)
with (D/'combined-matrix.pickle').open('rb') as f:AA,B,bounds=pickle.load(f)
for name in ('Q1','Q2','GB','tau','allk'):
 path=D/('combined-old-'+name+'.pickle') if name in ('Q1','Q2','GB') else D/('combined-'+name+'.pickle')
 if not path.exists():continue
 with path.open('rb') as f:x=pickle.load(f)
 for lim in (100,1000,10000,1000000):
  rat=[F(float(v)).limit_denominator(lim) for v in x]
  mul=lcm(*(v.denominator for v in rat));vec=[int(v*mul) for v in rat]
  # Zero equations exclude final274 fixed E target, to allow uniform scaling.
  cc=AA[:-274,:].tocoo();res=[0]*cc.shape[0]
  for r,c,v in zip(cc.row,cc.col,cc.data):res[r]+=int(v)*vec[c]
  if not any(res):
   div=reduce(gcd,vec);vec=[v//div for v in vec]
   print(name,'exact','denmax',max(v.denominator for v in rat),'scale',mul//div,'maxdigits',len(str(max(map(abs,vec)))),'nz',sum(bool(v) for v in vec),flush=True)
   with (D/('exact-'+name+'.pickle')).open('wb') as f:pickle.dump(vec,f)
   break
 else:print(name,'not exact',flush=True)
