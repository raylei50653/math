"""One-time exact extraction from local discovery; no optimization."""
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
from pathlib import Path
import importlib.util,pickle,json,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parents[3]
OLD=ROOT/"audits/2026-10-19-r6-941-leakage-b89c591/A"
Q=ROOT/"audits/2026-10-19-r6-941-quotients-13dc5ff/A"
s=importlib.util.spec_from_file_location("oldmodel",OLD/"model.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
with (OLD/"discovery/counted10-discovery.pickle").open("rb") as f:ten,rows,hist,columns,descriptions,T,AA=pickle.load(f)
with (OLD/"discovery/combined-matrix.pickle").open("rb") as f:A,B,bounds=pickle.load(f)
eight,ten2,index,transfer,hrows,hi,hhist,parts,M,MU=m.build();assert ten==ten2 and rows==hrows
n=len(ten);k=len(columns);rec=[]
for name in ("Q1","Q2"):
 with (D/(name+"-minimal-accept-zero.pickle")).open("rb") as f:x=pickle.load(f)
 for lim in (100,1000,10000,1000000):
  rat=[Fraction(float(v)).limit_denominator(lim) for v in x];mul=lcm(*(v.denominator for v in rat));vec=[int(v*mul) for v in rat]
  coo=A[:-274,:].tocoo();res=[0]*coo.shape[0]
  for r,c,v in zip(coo.row,coo.col,coo.data):res[r]+=int(v)*vec[c]
  if not any(res):
   div=reduce(gcd,vec);vec=[v//div for v in vec];break
 else:raise AssertionError("cannot exactify")
 z=vec[:n];e=[sum(z[i]*v for i,v in r) for r in transfer];counts={g:m.mv(mat,e) for g,mat in M.items()}
 assert counts[name][9]==0
 orbits=[]
 for j,v in enumerate(vec[n:n+k]):
  if v:
   t,p=descriptions[columns[j]];orbits.append({"start":list(t),"partition":list(p),"weight":v})
 coeff=[[j,v] for j,v in enumerate(vec[n+k:]) if v]
 subsets=m.source_positive_subsets(index)
 rec.append({"name":name+"_accept_zero","zero_acceptance_candidate":name,"core_counts":z,"exterior_counts":e,"orbits":orbits,"planar_coefficients":coeff,"graph_counts":counts,"U_counts":m.mv(MU,z),"source_positive_subset_counts":{s:sum(z[i] for i in ids) for s,ids in subsets.items()}})
 print(name,"exact",lim,"max",max(map(abs,vec)),"core",sum(v>0 for v in z),"orbits",len(orbits),"graphs",counts,"subsets",rec[-1]["source_positive_subset_counts"],flush=True)
cert={"base":"13dc5ff163045c85b5c82dde438eb5f275dab999","scope":"acceptance-zero necessary common-core controls only","source_realized":False,"smaller_bad_source_constructed":False,"records":rec,"pin_order":["a","n","R","L","q","c","s","v","w","t"],"rows":list(m.ROWS),"source_positive_subset_ids":subsets,"inputs_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (OLD/"model.py",Q/"model.py",Q.parent/"SOURCE_CONTRACT.md",D.parents[1]/"INPUTS.json",ROOT/"audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json")}}
with (D.parent/"acceptance-zero-controls.json").open("x") as f:json.dump(cert,f,indent=2);f.write("\n")
