exec((__import__('pathlib').Path(__file__).resolve().parent/'explore_allk_combined.py').read_text().split('ans=linprog')[0])
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
idx={t:i for i,t in enumerate(ten)}
idsB=sorted({idx[canonical((0,2,R,L,2,0,1,v,w,1))] for R,L in ((0,3),(3,0)) for v,w in ((2,3),(3,2))})
idsA=sorted({idx[canonical((0,1,R,L,2,0,1,v,w,1))] for R,L in ((2,1),(2,3),(3,1)) for v,w in ((2,3),(3,2))})
print('sectorB',idsB,'sectorA',idsA,flush=True)
for name in ('Q1','Q2','GB','tau','allK'):
 path=D/('exact-'+name+'.pickle')
 if name=='allK':
  with (D/'exact-Q1.pickle').open('rb') as f:x1=pickle.load(f)
  with (D/'exact-GB.pickle').open('rb') as f:x2=pickle.load(f)
  with (D/'exact-tau.pickle').open('rb') as f:x3=pickle.load(f)
  x=[a+b+c for a,b,c in zip(x1,x2,x3)]
 else:
  with path.open('rb') as f:x=pickle.load(f)
 print(name,'sectorA',sum(x[i] for i in idsA),'sectorB',sum(x[i] for i in idsB),flush=True)
# Full source941 and U319 positives, plus these exact mandatory sectors.
pos=[]
for ri in range(10):
 if (941>>ri)&1:pos.append(np.asarray(np.array([int(bool(mask&(1<<ri))) for mask in src['old_lift_masks']])@T).ravel())
for ri in range(10):
 if (319>>ri)&1:pos.append(MU[ri])
for ids in (idsA,idsB):pos.append(np.array([int(i in ids) for i in range(n)]))
for name in ('Q1','Q2','GB'):
 forbid=[i for i,p in enumerate(proj) if p['local_candidate_masks'][name]&82]
 eq2=vstack([eq,hstack([T[forbid,:],csr_matrix((len(forbid),k+m))])]).tocsr()
 acc=np.asarray(np.array([int(bool(p['local_candidate_masks'][name]&512)) for p in proj])@T).ravel()
 ub2=hstack([-csr_matrix(np.array(pos+[acc])),csr_matrix((len(pos)+1,k+m))]).tocsr()
 fit=linprog(np.array([1]*n+[0]*(k+m)),A_eq=eq2,b_eq=np.zeros(eq2.shape[0]),A_ub=ub2,b_ub=-np.ones(len(pos)+1),bounds=bounds)
 print('sector+fourcert',name,fit.success,fit.message,flush=True)
 if fit.success:
  with (D/('combined-sector-'+name+'.pickle')).open('wb') as f:pickle.dump(fit.x,f)
