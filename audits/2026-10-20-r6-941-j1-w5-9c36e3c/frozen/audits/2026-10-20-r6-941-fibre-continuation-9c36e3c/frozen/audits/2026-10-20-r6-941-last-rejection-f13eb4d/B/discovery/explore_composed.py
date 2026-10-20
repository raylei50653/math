#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json,gzip
from itertools import product
from math import factorial
HERE=Path(__file__).resolve().parent.parent
ROOT=HERE.parent/'frozen'
def load(p,n):
 s=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py','model')
o=load('audits/2026-10-19-r6-941-chains-13dc5ff/C/check.py','old')
bb=load('audits/2026-10-19-r6-941-existence-f13eb4d/B/check.py','bb')
ten,CM,caps=o.matrices(m);C,*Hs=CM
K=m.kempe(10,ten);cl=bb.Closure(K,len(ten))
seed=[i for i in range(len(ten)) if all(not C[r][i] for r in (1,4,6)) and not Hs[4][0][i]]
live,rounds=cl.close(seed)
print('base',len(live),bb.projection(C,live),flush=True)
ops=[(name,p,edges,j) for name,p,edges in o.OPS for j in range(4)]
Ms=[[[0]*len(ten) for _ in m.ROWS] for op in ops]
lsall=[]
for i,word in enumerate(ten):
 f=dict(zip(o.PINS,word));rights=[]
 for x,y,r in product(range(4),repeat=3):
  ff=dict(f,x=x,y=y,r=r)
  if all(ff[u]!=ff[v] for u,v in o.RIGHT):rights.append((x,y,r))
 cap=[[] for op in ops]
 for b in range(4):
  ff=dict(f,b=b)
  if b in (f['a'],f['q']):continue
  flags=(b==f['n'] and f['R']==f['q'],b==f['n']==f['L'],b==f['L'] and f['a']!=f['R'], f['a']!=f['L'] and f['a']!=f['R'] and b!=f['L'])
  for x,y,r in rights:
   ff=dict(ff,x=x,y=y,r=r)
   for j,(_,frame,edges,kind) in enumerate(ops):
    if not flags[kind] or not all(ff[u]!=ff[v] for u,v in edges):continue
    row=m.ROWS.index(''.join(map(str,m.canonical((x,y,f['a'],b,f[frame])))))
    Ms[j][row][i]+=1;cap[j].append((b,x,y,r))
 fac=factorial(4-len(set(word)))
 for M in Ms:
  for row in M:assert row[i]%fac==0;row[i]//=fac
 lsall.append(cap)
catalogue=sorted(map(int,json.loads((ROOT/'audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json').read_text())['cells']))
results=[]
for j,(op,M) in enumerate(zip(ops,Ms)):
 available=[]
 for support in catalogue:
  s=[i for i in live if all(not M[r][i] for r in range(10) if not support>>r&1)]
  ll,rr=cl.close(s)
  orig=bb.projection(C,ll);upp=bb.projection(M,ll)
  if orig==941 and not support&~upp:available.append(support)
 results.append({'operation':op,'support_upper':bb.projection(M,live),'available':available})
 print(j,op,bb.projection(M,live),available,flush=True)
print(json.dumps(results))
for j in range(16,20):
 ii=[i for i in live if Ms[j][0][i]]
 print('H4row0',j,len(ii),[ten[i] for i in ii],flush=True)
