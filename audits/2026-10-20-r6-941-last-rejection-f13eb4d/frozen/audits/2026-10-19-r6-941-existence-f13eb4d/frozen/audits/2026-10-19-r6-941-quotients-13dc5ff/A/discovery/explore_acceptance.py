import importlib.util,pickle,json,itertools,numpy as np
from pathlib import Path
from scipy.sparse import vstack,hstack,csr_matrix
from scipy.optimize import linprog
ROOT=Path.cwd(); OLD=ROOT/'audits/2026-10-19-r6-941-leakage-b89c591'; D=OLD/'A/discovery'
spec=importlib.util.spec_from_file_location('oldmodel',OLD/'A/model.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
with (D/'counted10-discovery.pickle').open('rb') as f:ten,rows,hist,columns,descriptions,T,A=pickle.load(f)
with (D/'combined-matrix.pickle').open('rb') as f:AA,B,bounds=pickle.load(f)
eight,ten2,index,transfer,hrows,hi,hist2,parts,original,umatrix=mod.build()
n=len(ten);k=len(columns);m=B.shape[1]
src=json.loads((ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json').read_text())
zeroT=[i for i in range(274) if i not in next(r for r in src['results'] if r['source_mask']==941)['surviving_ids']]
eq=vstack([AA[:-274,:],hstack([T[zeroT,:],csr_matrix((len(zeroT),k+m))])]).tocsr()
pos=[]
for ri in range(10):
 if (941>>ri)&1:pos.append(np.asarray(np.array(original['G'][ri])@T).ravel())
for ri in range(10):
 if (319>>ri)&1:pos.append(np.array(umatrix[ri]))
for ids in mod.source_positive_subsets(index).values():pos.append(np.array([int(i in ids) for i in range(n)]))
ub=hstack([-csr_matrix(np.array(pos)),csr_matrix((len(pos),k+m))]).tocsr()
for name in ('Q1','Q2'):
 acc=np.asarray(np.array(original[name][9])@T).ravel()
 eq2=vstack([eq,hstack([csr_matrix(acc.reshape(1,-1)),csr_matrix((1,k+m))])]).tocsr()
 ans=linprog(np.zeros(n+k+m),A_eq=eq2,b_eq=np.zeros(eq2.shape[0]),A_ub=ub,b_ub=-np.ones(len(pos)),bounds=bounds)
 print(name,'acceptance_zero_feasible',ans.success,ans.message,flush=True)
 if ans.success:
  print('counts',{g:list(np.array(original[g])@T@ans.x[:n]) for g in ('G','Q1','Q2','GB')},flush=True)
  with (Path(__file__).parent/(name+'-accept-zero.pickle')).open('wb') as f:pickle.dump(ans.x,f)
