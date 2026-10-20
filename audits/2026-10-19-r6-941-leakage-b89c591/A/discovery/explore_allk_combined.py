import itertools,json,pickle,numpy as np
from pathlib import Path
from scipy.optimize import linprog
from scipy.sparse import vstack,hstack,csr_matrix
D=Path(__file__).resolve().parent;ROOT=D.parents[2];OLD=ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2'
with (D/'counted10-discovery.pickle').open('rb') as f:ten,rows,hist,columns,descriptions,T,A=pickle.load(f)
with (D/'combined-matrix.pickle').open('rb') as f:AA,B,bounds=pickle.load(f)
src=json.loads((OLD/'frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json').read_text());proj=json.loads((OLD/'frozen/audits/2026-10-18-smaller-bad-e1617a2/candidate-projections.json').read_text())['complete_local_records']
u=json.loads((D.parent/'C/u319-core.json').read_text());MU=np.array(u['literal_U_count_matrix'])
n=len(ten);k=len(columns);m=B.shape[1];zeroT=[i for i in range(274) if i not in src['results'][2]['surviving_ids']]
eq=vstack([AA[:-274,:],hstack([T[zeroT,:],csr_matrix((len(zeroT),k+m))])]).tocsr()
positives=[]
for ri in range(10):
 if (941>>ri)&1:positives.append(np.asarray(np.array([int(bool(mask&(1<<ri))) for mask in src['old_lift_masks']])@T).ravel())
for name in ('Q1','Q2','GB'):
 for ri in range(10):positives.append(np.asarray(np.array([int(bool(p['local_candidate_masks'][name]&(1<<ri))) for p in proj])@T).ravel())
for ri in range(10):
 if (319>>ri)&1:positives.append(MU[ri])
ub=hstack([-csr_matrix(np.array(positives)),csr_matrix((len(positives),k+m))]).tocsr()
ans=linprog(np.zeros(n+k+m),A_eq=eq,b_eq=np.zeros(eq.shape[0]),A_ub=ub,b_ub=-np.ones(len(positives)),bounds=bounds)
print('ALLK strongest',ans.success,ans.message,flush=True)
if ans.success:
 z=T@ans.x[:n];o=0;masks={name:0 for name in ('Q1','Q2','GB')}
 for i,v in enumerate(z):
  if v>1e-7:
   o|=src['old_lift_masks'][i]
   for name in masks:masks[name]|=proj[i]['local_candidate_masks'][name]
 print('Epositive',sum(z>1e-7),'source',o,'candidates',masks,'Zpositive',sum(ans.x[:n]>1e-7),'Wpositive',sum(ans.x[n:n+k]>1e-7),'Cpositive',sum(abs(ans.x[n+k:])>1e-7),flush=True)
 print('Ucounts',list(MU@ans.x[:n]),'resid',max(abs(eq@ans.x)),flush=True)
 with (D/'combined-allk.pickle').open('wb') as f:pickle.dump(ans.x,f)
