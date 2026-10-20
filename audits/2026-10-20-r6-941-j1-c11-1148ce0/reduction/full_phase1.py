"""Bounded full cone phase1 independent numerical feasibility check."""
from pathlib import Path
import gzip,json,pickle,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import vstack,hstack,csr_matrix
D=Path(__file__).resolve().parent;C=D.parent/'counting';O=D.parent/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c'
with (C/'discovery.pickle').open('rb') as f:K,parts,E,U,M,sectors,orig=pickle.load(f)
I=json.load(gzip.open(O/'interface/certificate-v4.json.gz','rt'));n=len(K['states']);nc=len(K['columns']);live=sorted(I['live']);vs=live+list(range(n,E.shape[1]));nv=len(vs)
mat=hstack([E[:,vs],csr_matrix((E.shape[0],1))]);norm=csr_matrix(np.r_[np.ones(len(live)),np.zeros(nc+len(parts)+1)]);mat=vstack([mat,norm]).tocsr();ub=hstack([U[:,vs],csr_matrix(np.ones((U.shape[0],1)))]).tocsr();obj=np.r_[np.zeros(nv),-1.];rhs=np.r_[np.zeros(E.shape[0]),1.]
print('full phase1',mat.shape,mat.nnz,ub.shape,flush=True);start=time.monotonic()
ans=linprog(obj,A_eq=mat,b_eq=rhs,A_ub=ub,b_ub=np.zeros(U.shape[0]),bounds=[(0,None)]*(len(live)+nc)+[(None,None)]*len(parts)+[(0,None)],method='highs-ipm',options={'time_limit':360})
print(ans.message,ans.fun,time.monotonic()-start,flush=True)
with (D/'full-phase1-result.pickle').open('xb') as f:pickle.dump((vs,ans),f)
out={'solver_message':ans.message,'solver_status':int(ans.status),'fun':ans.fun,'seconds':time.monotonic()-start,'source_excluded':False}
if ans.success:
 out['minimum_positive_value']=-float(ans.fun)
 out['positive_values']=(-U[:,vs]@ans.x[:-1]).tolist();out['max_equation_residual']=float(max(abs(ans.eqlin.residual)));out['minimum_nonnegative_variable']=float(min(ans.x[:len(live)+nc]))
with (D/'full-phase1.json').open('x') as f:json.dump(out,f,sort_keys=True);f.write('\n')
print(json.dumps(out),flush=True)
