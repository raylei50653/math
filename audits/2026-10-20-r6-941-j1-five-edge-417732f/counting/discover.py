#!/usr/bin/env python3
"""Numerical common orbit cone discovery; optimizer output is not a proof."""
from pathlib import Path
import argparse,gzip,json,pickle,time
import numpy as np
from scipy.sparse import coo_matrix,hstack,csr_matrix
from scipy.optimize import linprog
D=Path(__file__).resolve().parent;start=time.monotonic()
ap=argparse.ArgumentParser()
ap.add_argument('--output-prefix',type=Path,default=D/'exploration')
args=ap.parse_args()
result_path=Path(str(args.output_prefix)+'.json')
pickle_path=Path(str(args.output_prefix)+'.pickle')
assert not result_path.exists() and not pickle_path.exists(), 'exploration output already exists'
I=json.load(gzip.open(D/'caps.json.gz','rt'))
K=json.load(gzip.open(D/'orbits.json.gz','rt'));K['rowids']=dict(K['rowids'])
live=K['live'];li={i:j for j,i in enumerate(live)}
rows=sorted(r for r,i in K['rowids'].items() if i in li);ri={r:j for j,r in enumerate(rows)}
rr=list(range(len(rows)));cc=[li[K['rowids'][r]] for r in rows];vv=[2]*len(rows)
n=len(live);q=len(K['columns'])
for j,col in enumerate(K['columns']):
    for r in col:rr.append(ri[r]);cc.append(n+j);vv.append(-1)
E=coo_matrix((vv,(rr,cc)),shape=(len(rows),n+q)).tocsr()
pos=[np.array([I['matrices']['G'][j][i] for i in live],dtype=int) for j in (0,2,3,5,7,8,9)]
pos += [np.array([row[i] for i in live],dtype=int) for row in I['sectors']]
w=np.zeros(n,dtype=int)
for rec in I['witnesses']:w[li[rec['canonical_id']]]=1
pos.append(w)
U=hstack([-csr_matrix(np.stack(pos)),csr_matrix((len(pos),q))]).tocsr()
print('LP',E.shape,E.nnz,'seconds',time.monotonic()-start,flush=True)
ans=linprog(np.r_[np.ones(n),np.zeros(q)],A_eq=E,b_eq=np.zeros(E.shape[0]),
            A_ub=U,b_ub=-np.ones(len(pos)),bounds=(0,None),
            options={'time_limit':120})
out={'status':ans.status,'success':bool(ans.success),'message':ans.message,
     'seconds':time.monotonic()-start,'source_excluded':False,'source_realized':False}
if ans.success:
    out.update({'nonzero_z':int(np.count_nonzero(ans.x[:n])),
                'nonzero_orbits':int(np.count_nonzero(ans.x[n:])),
                'positive_quantities':(np.stack(pos)@ans.x[:n]).tolist()})
with pickle_path.open('xb') as f:pickle.dump((live,rows,ans),f)
with result_path.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out),flush=True)
