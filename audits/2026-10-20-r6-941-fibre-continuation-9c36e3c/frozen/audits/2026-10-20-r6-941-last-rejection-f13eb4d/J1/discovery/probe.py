from pathlib import Path
import importlib.util,json
from itertools import product,permutations
D=Path(__file__).resolve().parent.parent;F=D.parent/'frozen'
s=importlib.util.spec_from_file_location('m',F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
I=m.interfaces();K=m.kempe(10,I['ten']); ix={t:i for i,t in enumerate(I['ten'])}
d=json.loads((F/'audits/2026-10-19-r6-941-existence-f13eb4d/C/comparisons.json').read_text())
live=set(next(e['live'] for e in d['records'][0]['survivors'] if e['mask']==943))
print('LIVE',len(live),flush=True)
patterns=[]
for n,R,q in ((1,3,0),(1,3,3),(3,1,0)):
 for r in (2,3):
  for v,w in ((0,1),(1,0)):
   t=(0,n,R,2,q,1,5-r,v,w,5-r);i=ix[m.canonical(t)]
   patterns.append((t,r,i,i in live))
print('T',patterns,flush=True)
parts=m.kempe
byh={}
for j,col in enumerate(K['columns']):
 if all(K['rowids'][rr] in live for rr,_ in col):
  for rr,v in col:byh.setdefault(rr,[]).append(j)
hi={t:j for j,t in enumerate(K['hrows'])}
names=('a','n','R','L','q','c','s','v','w','t')
for t,r,i,okay in patterns:
 if not okay:continue
 print('PATTERN',t,'r',r,flush=True)
 for sep in ((0,1,2,3),(0,2,1,3),(0,2,3,1)):
  q=tuple(sep[c] for c in t);h=m.hc(q);rr=hi[h];js=byh[rr]
  ps=[]
  for j in js:
   # descriptions row has same color side pattern up to swap, enough for partition
   ps.append(K['descriptions'][j][1])
  together=[(names[a],names[b]) for a in range(10) for b in range(a+1,10) if all(p[a]==p[b] for p in ps)]
  apart=[(names[a],names[b]) for a in range(10) for b in range(a+1,10) if q[a]//2==q[b]//2 and all(p[a]!=p[b] for p in ps)]
  print('  split',sep,'nparts',len(ps),'together',together,'apart',apart,flush=True)
t=patterns[4][0];sep=(0,2,3,1);h=m.hc(tuple(sep[c] for c in t));rr=hi[h]
print('Q3_EXACT')
for j in byh[rr]:
 p=K['descriptions'][j][1];print(j,[[names[i] for i,v in enumerate(p) if v==b] for b in range(max(p)+1)])
