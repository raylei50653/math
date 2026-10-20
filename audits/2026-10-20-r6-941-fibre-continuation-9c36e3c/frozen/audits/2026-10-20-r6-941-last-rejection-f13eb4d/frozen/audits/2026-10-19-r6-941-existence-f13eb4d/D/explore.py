"""Explore complete n=5 comparisons on the same original core."""
import importlib.util, itertools, json, math, time
from pathlib import Path
D=Path(__file__).resolve().parent
ROOT=D.parents[2]
FROZEN=D.parent/'frozen'
def module(name,path):
 s=importlib.util.spec_from_file_location(name,FROZEN/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module('n5_model','audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py')
old=module('n5_prior','audits/2026-10-19-r6-941-acceptance-13dc5ff/B/check.py')
PINS=old.PINS
POLY=('a','p','h','R','u')
DIAG=((0,2),(0,3),(1,3),(1,4),(2,4))
TRI=[tuple((POLY[i],POLY[j]) for i,j in ds) for ds in itertools.combinations(DIAG,2)
 if not any(i<k<j<l or k<i<l<j for (i,j),(k,l) in itertools.combinations(ds,2))]
FOLD=[(POLY[i],POLY[j]) for i,j in DIAG]

def build():
 ten,C,caps=old.interfaces(m)
 Ms=[[[0]*len(ten) for _ in range(10)] for _ in range(12)]
 edge=[e for e in old.LEFT_EDGES if 'n' not in e]
 full=[]
 for i,t in enumerate(ten):
  f=dict(zip(PINS,t));left=[]
  for b,p,h in itertools.product(range(4),repeat=3):
   ff=dict(f,b=b,p=p,h=h)
   if all(ff[v]!=ff[w] for v,w in edge):left.append((b,p,h))
  rights=caps[i]['right'];lsall=[]
  for j in range(10):
   ls=[]
   for b,p,h in left:
    ff=dict(f,b=b,p=p,h=h)
    good=all(ff[v]!=ff[w] for v,w in TRI[j]) if j<5 else ff[FOLD[j-5][0]]==ff[FOLD[j-5][1]]
    if good:ls.append((b,p,h))
   lsall.append(ls)
   for b,p,h in ls:
    for x,y,r in rights:
     row=m.ROWS.index(''.join(map(str,m.canonical((x,y,f['a'],b,f['c'])))))
     Ms[j][row][i]+=1
  qcaps=[]
  for which in range(2):
   ls=[]
   for b,n in itertools.product(range(4),repeat=2):
    if n in {f['a'],f['R'],f['u']} or b in {f['a'],f['c'],f['q']}:continue
    if not (b==n and (f['R']==f['q'] if which==0 else n==f['L'])):continue
    ls.append((b,n))
    for x,y,r in rights:
     row=m.ROWS.index(''.join(map(str,m.canonical((x,y,f['a'],b,f['c'])))))
     Ms[10+which][row][i]+=1
   qcaps.append(ls)
  for M in Ms:
   for row in M:
    fac=math.factorial(4-len(set(t)));assert row[i]%fac==0;row[i]//=fac
  full.append({'core':t,'source':caps[i],'candidates':lsall,'quotients':qcaps})
 return ten,C,Ms,full

def main():
 ten,C,Ms,full=build();print('matrices ready',flush=True)
 K=m.kempe(10,ten);print('kempe ready',flush=True)
 initial=[i for i in range(len(ten)) if all(C[r][i]==0 for r in (1,4,6))]
 live,rounds=m.close(K,initial)
 cat=sorted(map(int,json.loads((FROZEN/'artifacts/c5_cells/cells.json').read_text())['cells']))
 results=[]
 for j,N in enumerate(Ms):
  good=[];recs=[]
  for support in cat:
   seed=[i for i in live if all(not N[r][i] for r in range(10) if not(support>>r&1))]
   cells,rs=m.close(K,seed)
   cu=m.mask([sum(row[i] for i in cells) for row in C]);nu=m.mask([sum(row[i] for i in cells) for row in N])
   okay=cu==941 and support&~nu==0
   if okay:good.append(support)
   recs.append({'support':support,'source_upper':cu,'candidate_upper':nu,'live':cells,'round_sizes':[len(r) for r in rs]})
  results.append({'name':f'T{j}' if j<5 else f'F{j-5}' if j<10 else f'Q{j-9}','supports':good,'comparisons':recs})
  print(results[-1]['name'],good,flush=True)
 with (D/'exploration.json').open('x') as f:json.dump({'tri':TRI,'fold':FOLD,'results':results},f,separators=(',',':'))

if __name__=='__main__':main()
