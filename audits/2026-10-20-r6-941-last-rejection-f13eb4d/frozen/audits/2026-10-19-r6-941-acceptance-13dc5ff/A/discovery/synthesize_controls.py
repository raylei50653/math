"""Discovery only: synthesize small rational acceptance-zero controls."""
from pathlib import Path
import pickle,numpy as np
D=Path(__file__).resolve().parent;ROOT=D.parents[3]
P=ROOT/"audits/2026-10-19-r6-941-quotients-13dc5ff/A/discovery/explore_acceptance.py"
task_D=D
exec(P.read_text().split("for name in ('Q1','Q2'):")[0])
D=task_D
for name in ("Q1","Q2"):
 acc=np.asarray(np.array(original[name][9])@T).ravel()
 eq2=vstack([eq,hstack([csr_matrix(acc.reshape(1,-1)),csr_matrix((1,k+m))])]).tocsr()
 obj=np.r_[np.ones(n),np.zeros(k+m)]
 ans=linprog(obj,A_eq=eq2,b_eq=np.zeros(eq2.shape[0]),A_ub=ub,b_ub=-np.ones(len(pos)),bounds=bounds)
 print(name,ans.success,ans.fun,flush=True)
 if ans.success:
  with (D/(name+"-minimal-accept-zero.pickle")).open("xb") as f:pickle.dump(ans.x,f)
