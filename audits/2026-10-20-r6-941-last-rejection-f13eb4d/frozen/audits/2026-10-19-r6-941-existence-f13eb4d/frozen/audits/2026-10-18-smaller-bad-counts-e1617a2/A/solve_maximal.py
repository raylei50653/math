#!/usr/bin/env python3
"""Find and certify maximal support in the triangulated count cone."""
import hashlib
import json
from pathlib import Path
from fractions import Fraction
from math import gcd,lcm
from functools import reduce
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix,hstack,vstack,eye
R=Path(__file__).resolve().parent
cone=json.loads((R/'cone-triangulated.json').read_text())
F=R.parent/'frozen/audits/2026-10-18-smaller-bad-e1617a2'
data=json.loads((F/'kempe-consistency.json').read_text())
proj=json.loads((F/'candidate-projections.json').read_text())['complete_local_records']
results=[]
for prior in data['results']:
 mask=prior['source_mask'];live=prior['surviving_ids'];nl=len(live)
 allowed=[j for j,col in enumerate(cone['columns']) if all(cone['rows'][r]['tuple_id'] in live for r,v in col['entries'])]
 A=lil_matrix((821,274+len(allowed)))
 for r,row in enumerate(cone['rows']):A[r,row['tuple_id']]=-row['orbit_size']
 for k,j in enumerate(allowed):
  for r,v in cone['columns'][j]['entries']:A[r,274+k]=v
 A=A.tocsr();nv=A.shape[1]
 U=lil_matrix((nl,nv+nl))
 for k,i in enumerate(live):U[k,i]=-1;U[k,nv+k]=1
 bounds=[(0,None) if i in live else (0,0) for i in range(274)]+[(0,None)]*len(allowed)+[(0,1)]*nl
 ans=linprog([0]*nv+[-1]*nl,A_eq=hstack([A,lil_matrix((821,nl))]).tocsr(),b_eq=np.zeros(821),A_ub=U.tocsr(),b_ub=np.zeros(nl),bounds=bounds)
 assert ans.success
 support=[i for k,i in enumerate(live) if ans.x[nv+k]>0.5]
 forced=sorted(set(live)-set(support))
 print(mask,'maxsupport',len(support),'forced',forced,flush=True)
 # Choose a small exact rational witness positive throughout this support.
 bs=[(1,None) if i in support else (0,0) for i in range(274)]+[(0,None)]*len(allowed)
 ans=linprog(np.ones(nv),A_eq=A,b_eq=np.zeros(821),bounds=bs)
 assert ans.success
 rats=[Fraction(float(v)).limit_denominator(1000000) for v in ans.x]
 scale=lcm(*(v.denominator for v in rats));ints=[int(v*scale) for v in rats]
 div=reduce(gcd,ints);ints=[v//div for v in ints]
 residual=[0]*821
 for r,row in enumerate(cone['rows']):residual[r]-=row['orbit_size']*ints[row['tuple_id']]
 for k,j in enumerate(allowed):
  for r,v in cone['columns'][j]['entries']:residual[r]+=v*ints[274+k]
 assert not any(residual)
 original=0;candidates=dict.fromkeys(('GA','GB','H','S','Q1','Q2'),0)
 for i in support:
  original|=data['old_lift_masks'][i]
  for name,v in proj[i]['local_candidate_masks'].items():candidates[name]|=v
 rec={'source_mask':mask,'boolean_live_ids':live,'maximal_support':support,'forced_zero_ids':forced,'counts':ints[:274],
      'positive_orbit_weights':[[j,ints[274+k]] for k,j in enumerate(allowed) if ints[274+k]],
      'original_projection':original,'candidate_masks':candidates,'allowed_columns':allowed}
 print('witness',max(ints[:274]),len(rec['positive_orbit_weights']),original,candidates,flush=True)
 if forced:
  indices=live+list(range(274,nv));c=np.array([int(i in forced) for i in range(274)]+[0]*len(allowed))
  d=linprog(np.zeros(821),A_ub=-A[:,indices].T,b_ub=-c[indices],bounds=[(None,None)]*821)
  assert d.success
  y=[Fraction(float(v)).limit_denominator(1000000) for v in d.x]
  scale=lcm(*(v.denominator for v in y));yy=[int(v*scale) for v in y]
  for i in indices:
   col=A[:,i].tocoo();val=sum(yy[r]*int(v) for r,v in zip(col.row,col.data))
   assert val>=c[i]*scale,(i,val,c[i]*scale)
  rec['forced_zero_dual']={'scale':scale,'row_values':yy}
  print('exact dual',scale,'max',max(map(abs,yy)),'nonzero',sum(bool(v) for v in yy),flush=True)
 results.append(rec)
out={'scope':'necessary maximal triangulated count cone; not source realizability',
     'cone_sha256':hashlib.sha256((R/'cone-triangulated.json').read_bytes()).hexdigest(),
     'solver':'scipy 1.18.1 linprog highs; all output checked as exact integers',
     'results':results}
with (R/'triangulated-witnesses.json').open('x') as f:
 f.write(json.dumps(out,indent=2)+'\n')
