"""Search exact observables of J1/J2 in the frozen exterior planar span."""
import importlib.util,json,itertools
from pathlib import Path
HERE=Path(__file__).resolve().parent
F=HERE.parent/'frozen'
spec=importlib.util.spec_from_file_location('emodel',F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
old=json.loads((F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/certificate.json').read_text())
eight=[t for t in m.growth(8,four=True) if m.proper(t)];idx={t:i for i,t in enumerate(eight)}
J=[[[0]*len(eight) for _ in m.ROWS] for _ in range(2)]
for row,w in enumerate(m.ROWS):
 x,y,a,b,c=map(int,w)
 for n,R,L,q in itertools.product(range(4),repeat=4):
  t=(a,n,R,L,q,c,x,y)
  if not m.proper(t) or b in {a,c,q}:continue
  for j,flag in enumerate((b==L and a!=R,a!=L and a!=R and b!=L)):
   if flag:J[j][row][idx[m.canonical(t)]]+=1
_,_,basis=m.planar_basis(eight,old['source_E_closure']['live'])
M=old['literal_E_count_matrices']
forms={'a1':M['Q1'][9],'a2':M['Q2'][9]}
for j in range(2):
 for row in (1,4,6,9):forms[f'J{j+1}_{m.ROWS[row]}']=J[j][row]
vals={k:m.mv(basis,v) for k,v in forms.items()}
for j in range(2):
 for row in (4,6):
  v=vals[f'J{j+1}_{m.ROWS[row]}']
  for a in ('a1','a2'):
   z=vals[a];k=next(i for i,x in enumerate(z) if x);ratio=v[k]/z[k]
   if all(x==ratio*y for x,y in zip(v,z)):print(f'J{j+1}_{m.ROWS[row]} = {ratio} * {a}')
print('ranks',len(m.rref(list(vals.values()))[1]),len(vals))
names=list(vals)
red,piv=m.rref(list(map(list,zip(*vals.values()))))
for free in set(range(len(names)))-set(piv):
 relation={names[free]:'1'}
 for r,p in enumerate(piv):
  if red[r][free]:relation[names[p]]=str(-red[r][free])
 print(relation)
print('done')
