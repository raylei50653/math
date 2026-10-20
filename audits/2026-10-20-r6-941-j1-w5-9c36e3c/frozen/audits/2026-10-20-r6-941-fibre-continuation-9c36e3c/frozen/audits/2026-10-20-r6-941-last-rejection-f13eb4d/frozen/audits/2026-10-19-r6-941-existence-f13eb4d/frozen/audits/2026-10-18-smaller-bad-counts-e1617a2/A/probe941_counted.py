#!/usr/bin/env python3
import json,itertools
from fractions import Fraction
from functools import reduce
from math import gcd,lcm
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
R=Path(__file__).resolve().parent
F=R.parent/'frozen/audits/2026-10-18-smaller-bad-e1617a2'
c=json.loads((R/'cone-triangulated.json').read_text())
d=json.loads((F/'kempe-consistency.json').read_text())
p=json.loads((F/'candidate-projections.json').read_text())['complete_local_records']
results=[]
for name in ('Q1','Q2','GB'):
 live=[i for i in d['results'][2]['surviving_ids'] if not (p[i]['local_candidate_masks'][name] & ((1<<1)|(1<<4)|(1<<6)))]
 allowed=[j for j,col in enumerate(c['columns']) if all(c['rows'][r]['tuple_id'] in live for r,v in col['entries'])]
 A=lil_matrix((821,274+len(allowed)))
 for r,row in enumerate(c['rows']):A[r,row['tuple_id']]=-row['orbit_size']
 for k,j in enumerate(allowed):
  for r,v in c['columns'][j]['entries']:A[r,274+k]=v
 A=A.tocsr();nv=A.shape[1]
 target=np.array([int(bool(p[i]['local_candidate_masks'][name]&512)) for i in range(274)]+[0]*len(allowed))
 ans=linprog(-target,A_eq=A,b_eq=np.zeros(821),A_ub=np.array([[1]*274+[0]*len(allowed)]),b_ub=[1],bounds=[(0,None) if i in live else (0,0) for i in range(274)]+[(0,None)]*len(allowed))
 print(name,'live',len(live),'columns',len(allowed),'max accept',-ans.fun,flush=True)
 rec={'candidate':name,'allowed_ids':live,'allowed_columns':allowed}
 if ans.fun< -1e-9:
  rat=[Fraction(float(x)).limit_denominator(1000000) for x in ans.x]
  mul=lcm(*(v.denominator for v in rat));vec=[int(v*mul) for v in rat];div=reduce(gcd,vec);vec=[v//div for v in vec]
  residual=[-row['orbit_size']*vec[row['tuple_id']] for row in c['rows']]
  for k,j in enumerate(allowed):
   for r,v in c['columns'][j]['entries']:residual[r]+=v*vec[274+k]
  assert not any(residual)
  original=0;candidate=0
  for i,v in enumerate(vec[:274]):
   if v:original|=d['old_lift_masks'][i];candidate|=p[i]['local_candidate_masks'][name]
  rec.update({'feasible':True,'counts':vec[:274],'orbit_weights':[[j,vec[274+k]] for k,j in enumerate(allowed) if vec[274+k]],'original_mask':original,'candidate_mask':candidate})
  print('exact support',sum(bool(v) for v in vec[:274]),'masks',original,candidate,flush=True)
 else:
  indices=live+list(range(274,nv))
  ans=linprog(np.zeros(821),A_ub=-A[:,indices].T,b_ub=-target[indices],bounds=[(None,None)]*821)
  assert ans.success
  rat=[Fraction(float(x)).limit_denominator(1000000) for x in ans.x]
  mul=lcm(*(v.denominator for v in rat));y=[int(v*mul) for v in rat]
  for i in indices:
   col=A[:,i].tocoo();value=sum(y[r]*int(v) for r,v in zip(col.row,col.data))
   assert value>=target[i]*mul,(i,value,target[i]*mul)
  rec.update({'feasible':False,'scale':mul,'dual':y})
 results.append(rec)
with (R/'941-counted-candidate-probes.json').open('x') as f:f.write(json.dumps({'scope':'necessary counted cone only, not realizability','results':results},indent=2)+'\n')
