"""Discovery only. Exact extraction checked below, no graph realization."""
import importlib.util,json,pickle,numpy as np
from pathlib import Path
from scipy.sparse import csr_matrix,hstack,vstack
from scipy.optimize import linprog
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
D=Path(__file__).resolve().parent;F=D.parent/'frozen';OLD=F/'audits/2026-10-19-r6-941-existence-f13eb4d';L=F/'audits/2026-10-19-r6-941-leakage-b89c591/A'
s=importlib.util.spec_from_file_location('o',L/'model.py');o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
eight,ten,index,transfer,hrows,hi,hist,parts,M,U=o.build()
with (L/'discovery/counted10-discovery.pickle').open('rb') as f:ten0,rows0,hist0,columns,desc,T,A=pickle.load(f)
with (L/'discovery/combined-matrix.pickle').open('rb') as f:AA,B,bounds=pickle.load(f)
assert ten==ten0 and hrows==rows0
n=len(ten);nc=len(columns);npart=len(parts)
J=json.loads((OLD/'C/comparisons.json').read_text())['matrices']
for g in J:M[g]=J[g]['E']
c=json.loads((OLD/'C/certificate.json').read_text());unique={v['signature_id']:v for v in c['candidates']}
for k,v in unique.items():
 E=[[0]*274 for _ in range(10)];sig=list(map(len,v['lifts']))
 for j,nn,R,Lq,q,ei,ri,good in c['exterior_records']:
  if good:E[j][ei]+=sig[ri]
 M['P'+str(k)]=E
C={g:np.asarray(np.array(mat)@T) for g,mat in M.items()}
cat=set(map(int,json.loads((OLD/'frozen/artifacts/c5_cells/cells.json').read_text())['cells']))
records=[]
for branch in json.loads((D/'joint90_discovery.json').read_text()):
 name=branch['branch'];q='Q1' if name=='a1' else 'Q2';live=set(branch['live'])
 masks={g:reduce(lambda x,y:x|y,ds,0) for g,ds in branch['domains'].items()}
 assert all(v in cat for v in masks.values()),[(g,v) for g,v in masks.items() if v not in cat]
 pos=[C['G'][j] for j in range(10) if 941>>j&1]+[np.array(U[j]) for j in range(10) if 319>>j&1]
 pos += [np.array([int(i in ids) for i in range(n)]) for ids in o.source_positive_subsets(index).values()]
 pos += [C['J1' if q=='Q1' else 'J2'][1]]
 ub=hstack([-csr_matrix(np.array(pos)),csr_matrix((len(pos),nc+npart))]).tocsr()
 bd=list(bounds)
 for i in range(n):
  if i not in live:bd[i]=(0,0)
 ans=linprog(np.r_[np.ones(n),np.zeros(nc+npart)],A_eq=AA[:-274,:],b_eq=np.zeros(AA.shape[0]-274),A_ub=ub,b_ub=-np.ones(len(pos)),bounds=bd)
 print(name,ans.success,ans.message,flush=True)
 if not ans.success:continue
 rat=[Fraction(float(v)).limit_denominator(1000000) for v in ans.x];mul=lcm(*(v.denominator for v in rat));vec=[int(v*mul) for v in rat];div=reduce(gcd,vec);vec=[v//div for v in vec]
 coo=AA[:-274,:].tocoo();res=[0]*coo.shape[0]
 for r,co,v in zip(coo.row,coo.col,coo.data):res[r]+=int(v)*vec[co]
 assert not any(res)
 assert min(vec[:n+nc])>=0 and all(vec[i]==0 for i in range(n) if i not in live)
 counts={g:[sum(int(x)*v for x,v in zip(row,vec[:n])) for row in mat] for g,mat in C.items()}
 assert o.mask(counts['G'])==941 and counts[q][9]==0
 print('actual masks',{g:o.mask(counts[g]) for g in ('Q1','Q2','GB','J1','J2')},flush=True)
 assert all(sum(int(x)*v for x,v in zip(row,vec[:n]))>0 for row in pos)
 rec={'branch':name,'core_counts':vec[:n],'planar_coefficients':[[i,v] for i,v in enumerate(vec[n+nc:]) if v],
 'orbits':[{'start':desc[tuple(columns[j])][0],'partition':desc[tuple(columns[j])][1],'weight':v} for j,v in enumerate(vec[n:n+nc]) if v],
 'graph_counts':counts,'masks':{g:o.mask(v) for g,v in counts.items()},'source_realized':False}
 records.append(rec)
 print(name,'exact',max(map(abs,vec)),sum(v>0 for v in vec[:n]),'J1/J2',counts['J1'],counts['J2'],flush=True)
with (D/'counted_T_controls.json').open('x') as f:json.dump({'status':'necessary common count control, not graph realization','source_realized':False,'records':records},f,separators=(',',':'));f.write('\n')
