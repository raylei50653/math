from pathlib import Path
import importlib.util,json
from itertools import product
ROOT=Path(__file__).resolve().parents[3]
OLD=ROOT/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
spec=importlib.util.spec_from_file_location('oldmodel',OLD);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ten=[t for t in m.growth(10,four=True) if m.proper(t)]
C=[[0]*len(ten) for _ in m.ROWS]
for i,(a,n,R,L,q,u,s,v,w,t) in enumerate(ten):
 for c in range(4):
  if c in (q,u,s):continue
  left=[(b,p,h) for b,p,h in product(range(4),repeat=3) if b not in (a,c,q,p) and p not in (a,q,n,h) and h not in (q,R,L,n)]
  right=[(x,y,r) for x,y,r in product(range(4),repeat=3) if r not in (s,v,w,t,x,y) and x not in (c,s,y) and y not in (a,t)]
  for b,p,h in left:
   for x,y,r in right:
    row=''.join(map(str,m.canonical((x,y,a,b,c))))
    C[m.ROWS.index(row)][i]+=1
K=m.kempe(10,ten)
initial=[i for i in range(len(ten)) if not any(C[r][i] for r in (1,4,6))]
live,rounds=m.close(K,initial)
print(json.dumps({'initial':len(initial),'rounds':[len(r) for r in rounds],'live':len(live),'G_upper':m.mask([sum(row[i] for i in live) for row in C]),'alpha_cells':sum(C[9][i]>0 for i in live),'alpha_caps':sum(C[9][i] for i in live)}))
from math import factorial
N=[[0]*len(ten) for _ in m.ROWS]
for i,(a,n,R,L,q,u,s,v,w,t) in enumerate(ten):
 left=[(b,p,h) for b,p,h in product(range(4),repeat=3) if b not in (a,u,q,p) and p not in (a,q,n,h) and h not in (q,R,L,n)]
 right=[(x,y,r) for x,y,r in product(range(4),repeat=3) if r not in (s,v,w,t,x,y) and x not in (u,s,y) and y not in (a,t)]
 for b,p,h in left:
  for x,y,r in right:
   row=''.join(map(str,m.canonical((x,y,a,b,u))))
   N[m.ROWS.index(row)][i]+=1
upper=m.mask([sum(row[i] for i in live) for row in N])
print('new candidate upper',upper,'counts',[sum(row[i] for i in live) for row in N])
# test whether a proposed K132 mask can retain original941 and be closed under true Kempe swaps
catalogue=set(map(int,json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())['cells']))
result=[]
for mask in sorted(catalogue):
 initial2=[i for i in initial if all(not N[r][i] for r in range(10) if not(mask>>r&1))]
 l,rs=m.close(K,initial2)
 gmask=m.mask([sum(row[i] for i in l) for row in C]);nmask=m.mask([sum(row[i] for i in l) for row in N])
 if gmask==941:result.append((mask,nmask,len(l)))
print('catalogue-compatible',len(result),result)
for uv in ((3,5),):
 l,rs=m.close(K,[i for i in initial if ten[i][uv[0]]!=ten[i][uv[1]]])
 print('c5 plus L-u',len(l),[len(r) for r in rs],m.mask([sum(row[i] for i in l) for row in C]),sum(C[9][i] for i in l))
remaining=[]
for mask in sorted(catalogue):
 if mask in (1022,1023):continue
 l,rs=m.close(K,[i for i in initial if all(not N[r][i] for r in range(10) if not(mask>>r&1))])
 if any(C[9][i] for i in l):remaining.append((mask,m.mask([sum(row[i] for i in l) for row in C])))
print('noncompatible but alpha remaining',remaining)
