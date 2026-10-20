exec((__import__('pathlib').Path(__file__).resolve().parent/'explore_allk_combined.py').read_text().split('ans=linprog')[0])
positives=[]
for name in ('Q1','Q2','GB'):
 positives.append(np.asarray(np.array([int(bool(p['local_candidate_masks'][name]&2)) for p in proj])@T).ravel())
ub=hstack([-csr_matrix(np.array(positives)),csr_matrix((len(positives),k+m))]).tocsr()
ans=linprog(np.array([1]*n+[0]*(k+m)),A_eq=eq,b_eq=np.zeros(eq.shape[0]),A_ub=ub,b_ub=-np.ones(len(positives)),bounds=bounds)
print('tau strongest',ans.success,ans.message,flush=True)
if ans.success:
 z=T@ans.x[:n];o=0;masks={name:0 for name in ('Q1','Q2','GB')}
 for i,v in enumerate(z):
  if v>1e-7:
   o|=src['old_lift_masks'][i]
   for name in masks:masks[name]|=proj[i]['local_candidate_masks'][name]
 print('Epositive',sum(z>1e-7),'source',o,'candidates',masks,'Zpositive',sum(ans.x[:n]>1e-7),'Wpositive',sum(ans.x[n:n+k]>1e-7),'Cpositive',sum(abs(ans.x[n+k:])>1e-7),flush=True)
 print('Ucounts',list(MU@ans.x[:n]),'resid',max(abs(eq@ans.x)),flush=True)
 with (D/'combined-tau.pickle').open('wb') as f:pickle.dump(ans.x,f)
