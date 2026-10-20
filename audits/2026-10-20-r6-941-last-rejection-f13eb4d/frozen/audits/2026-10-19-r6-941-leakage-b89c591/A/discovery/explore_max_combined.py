import itertools,json,pickle,numpy as np
from pathlib import Path
from scipy.optimize import linprog
D=Path(__file__).resolve().parent;ROOT=D.parents[2];OLD=ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2'
with (D/'counted10-discovery.pickle').open('rb') as f:ten,rows,hist,columns,descriptions,T,A=pickle.load(f)
with (D/'combined-matrix.pickle').open('rb') as f:AA,B,bounds=pickle.load(f)
cert=json.loads((OLD/'A/triangulated-witnesses.json').read_text());rec=next(r for r in cert['results'] if r['source_mask']==941);z=rec['counts'];n=len(ten);k=len(columns);m=B.shape[1]
bb=np.array([0]*(len(rows)+n)+z)
ans=linprog(np.zeros(n+k+m),A_eq=AA,b_eq=bb,bounds=bounds)
print('MAX OLD',ans.success,ans.message,flush=True)
if ans.success:
 with (D/'combined-max.pickle').open('wb') as f:pickle.dump(ans.x,f)
 u=json.loads((D.parent/'C/u319-core.json').read_text());M=np.array(u['literal_U_count_matrix']);y=M@ans.x[:n]
 print('supportZ',sum(ans.x[:n]>1e-8),'supportW',sum(ans.x[n:n+k]>1e-8),'Csupport',sum(abs(ans.x[n+k:])>1e-8),'maxresid',max(abs(AA@ans.x-bb)),'Ucounts',list(y),flush=True)
