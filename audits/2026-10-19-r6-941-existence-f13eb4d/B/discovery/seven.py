import importlib.util,json,gzip,time
from pathlib import Path
from itertools import product,combinations
from math import factorial
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parent/'frozen'
def load(p,name):
 sp=importlib.util.spec_from_file_location(name,ROOT/p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
m=load('audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py','m')
a=load('audits/2026-10-19-r6-941-chains-13dc5ff/C/check.py','a')
cert=json.loads(gzip.decompress((ROOT/'audits/2026-10-19-r6-941-chains-13dc5ff/C/certificate.json.gz').read_bytes()))
ten=[tuple(t) for t in cert['core_states']];C=cert['original_matrix'];K=m.kempe(10,ten)
rowbits=[0]*len(ten)
for r,i in enumerate(K['rowids']):rowbits[i]|=1<<r
colbits=[(sum(1<<i for i in set(K['rowids'][r] for r,v in col)),sum(1<<r for r,v in col)) for col in K['columns']]
FULL=(1<<len(ten))-1

def close(seed):
 live=sum(1<<i for i in seed);rounds=[]
 while True:
  dead=FULL^live;covered=0
  for cb,rb in colbits:
   if not cb&dead:covered|=rb
  bad=[i for i in range(len(ten)) if live>>i&1 and rowbits[i]&covered!=rowbits[i]]
  if not bad:return [i for i in range(len(ten)) if live>>i&1],rounds
  rounds.append(bad);live^=sum(1<<i for i in bad)

def proj(N,live):return sum(1<<r for r,row in enumerate(N) if any(row[i] for i in live))
poly=('x','y','a','b','q','u','s')
ops=[]
for keep in combinations(range(7),5):
 gaps=[]
 for ii,st in enumerate(keep):
  en=keep[(ii+1)%5];gap=tuple(poly[v%7] for v in range(st,st+(en-st)%7+1))
  if len(gap)>2:gaps.append(gap)
 if len(gaps)==2:
  es=tuple((g[0],g[-1]) for g in gaps);ops.append({'frame':tuple(poly[j] for j in keep),'edges':es})
 else:
  g=gaps[0];assert len(g)==4
  for diag in ((g[0],g[2]),(g[1],g[3])):ops.append({'frame':tuple(poly[j] for j in keep),'edges':((g[0],g[-1]),diag)})
assert len(ops)==28
Ns=[[[0]*len(ten) for _ in range(10)] for op in ops]
for i,word in enumerate(ten):
 f=dict(zip(a.PINS,word))
 left=[];right=[]
 for b,p,h in product(range(4),repeat=3):
  ff=dict(f,b=b,p=p,h=h)
  if all(ff[j]!=ff[k] for j,k in a.LEFT):left.append((b,p,h))
 for x,y,r in product(range(4),repeat=3):
  ff=dict(f,x=x,y=y,r=r)
  if all(ff[j]!=ff[k] for j,k in a.RIGHT):right.append((x,y,r))
 for b,p,h in left:
  for x,y,r in right:
   ff=dict(f,b=b,p=p,h=h,x=x,y=y,r=r)
   for j,op in enumerate(ops):
    if not all(ff[v]!=ff[w] for v,w in op['edges']):continue
    row=m.ROWS.index(''.join(map(str,m.canonical(tuple(ff[v] for v in op['frame'])))))
    Ns[j][row][i]+=1
 fac=factorial(4-len(set(word)))
 for N in Ns:
  for row in N:assert row[i]%fac==0;row[i]//=fac
catalogue=sorted(map(int,json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())['cells']))
live=cert['general_c5']['live']
records=[]
for j,(op,N) in enumerate(zip(ops,Ns)):
 poss=[];recs=[]
 for support in catalogue:
  ll,rs=close([i for i in live if all(not N[r][i] for r in range(10) if not support>>r&1)])
  if proj(C,ll)!=941:continue
  if support&~proj(N,ll):continue
  poss.append(support);recs.append((support,ll))
 print(j,op,'upper',proj(N,live),'poss',poss,flush=True)
 records.append(recs)
json.dump({'ops':ops,'matrices':Ns,'compatible':records},open(HERE/'discovery/seven-results.json','w'))
