from pathlib import Path
import importlib.util,json
from itertools import product
H=Path(__file__).resolve().parent.parent;F=H.parent/'frozen'
def load(p,n):
 s=importlib.util.spec_from_file_location(n,F/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py','m');o=load('audits/2026-10-19-r6-941-leakage-b89c591/A/model.py','o')
ten=[t for t in m.growth(10,four=True) if m.proper(t)];idx={t:i for i,t in enumerate(ten)}
z=json.loads((H/'counted-control.json').read_text())['core_counts'];old=[];transfer=[]
for row in ten:
 a,n,R,L,q,c,s,v,w,t=row
 lifts=[idx[m.canonical((a,n,R,L,q,u,s,v,w,t))] for u in range(4) if u not in {q,c,s}]
 transfer.append(lifts);old.append(sum(z[i] for i in lifts))
U=[]
for row in m.ROWS:
 a,s,v,w,t=map(int,row);val=0
 for n,R,L,q in product(range(4),repeat=4):
  core=(a,n,R,L,q,a,s,v,w,t)
  if not m.proper(core):continue
  ph=sum(p not in {a,q,n,h} and h not in {p,q,L,R,n} for p,h in product(range(4),repeat=2))
  val+=ph*old[idx[m.canonical(core)]]
 U.append(val)
pos={name:sum(old[i] for i in ids) for name,ids in o.source_positive_subsets(idx).items()}
print('U',U,'mask',m.mask(U),'positive subsets',pos)
