#!/usr/bin/env python3
"""Same-H necessary screen joining both actual C5 completions; not realizability."""
from functools import lru_cache
from itertools import combinations,product
import json
from pathlib import Path
P=Path(__file__).resolve().parent
COL=tuple(range(4))
PAIRINGS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
# H literal ordered pins z,s,j,i,w,t,p,q.
EDGES=((0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(6,7),(7,0))
PATTERNS=('ABABC','ABACB','ABACD','ABCAB','ABCAC','ABCAD','ABCBC','ABCBD','ABCDB','ABCDC')
def canon(r):
 d={};return tuple(d.setdefault(x,len(d)) for x in r)
def name(r):return ''.join('ABCD'[x] for x in r)
def bit(r):return 1<<PATTERNS.index(name(canon(r)))
def projection(row,which):
 z,s,j,i,w,t,p,q=row
 if which=='i':return bit((z,s,i,w,t)) if s!=i else 0
 if which=='j':return bit((z,s,j,w,t)) if j!=w else 0
 return sum({bit((z,s,v,w,t)) for v in COL if v not in(s,j,i,w)})
def support(rows,which):
 ans=0
 for r in rows:ans|=projection(r,which)
 return ans
def proper(r):return all(r[a]!=r[b] for a,b in EDGES)
def old_rule(z,s,r,t,p,q):
 if z==r:return s==t and {p,q}==set(COL)-{z,s}
 if s==t:return bool({p,q}&(set(COL)-{z,s,r}))
 return {p,q}=={s,t}
def allowed(row):
 if not proper(row):return False
 z,s,j,i,w,t,p,q=row
 return all(old_rule(z,s,r,t,p,q) for v in COL if v not in (s,j,i,w) for r in COL if r not in(s,v,w,t))
@lru_cache(None)
def parts(items):
 if not items:return ((),)
 ans=[]
 for p in parts(items[1:]):
  ans.append(((items[0],),)+p)
  for i,b in enumerate(p):ans.append(p[:i]+((items[0],)+b,)+p[i+1:])
 return tuple(ans)
@lru_cache(None)
def opts(row,pairing):
 pp=[]
 for pair in pairing:
  v=tuple(i for i,c in enumerate(row) if c in pair)
  good=[]
  for p in parts(v):
   lab={u:k for k,b in enumerate(p) for u in b}
   if all(lab[a]==lab[b] for a,b in EDGES if a in lab and b in lab):good.append(p)
  pp.append(good)
 result=[]
 for p0,p1 in product(*pp):
  blocks=p0+p1;lab={u:k for k,b in enumerate(blocks) for u in b}
  if any(lab[a]==lab[c] and lab[b]==lab[d] and lab[a]!=lab[b] for a,b,c,d in combinations(range(6),4)):continue
  bp=[(b,pair) for p,pair in zip((p0,p1),pairing) for b in p]
  orbit=set()
  for flag in range(1<<len(bp)):
   r=list(row)
   for k,(b,pair) in enumerate(bp):
    if flag>>k&1:
     for u in b:r[u]=pair[0] if r[u]==pair[1] else pair[1]
   orbit.add(canon(r))
  result.append(frozenset(orbit))
 return tuple(result)
def fixed(rows):
 live=set(rows);rounds=[]
 while True:
  dead={r for r in live if any(not any(o<=live for o in opts(r,pairing)) for pairing in PAIRINGS)}
  rounds.append({'live':len(live),'removed':len(dead)})
  if not dead:return live,rounds
  live-=dead
upper={canon(r) for r in product(COL,repeat=8) if allowed(r)}
print('upper',len(upper),[support(upper,w) for w in ('i','j','u')],flush=True)
live,rounds=fixed(upper)
print('fixed',len(live),[support(live,w) for w in ('i','j','u')],rounds,flush=True)
cells=json.loads((P/'cells.json').read_text())
ci=sorted(int(m) for m in cells['cells'] if int(m)&~support(live,'i')==0)
cj=sorted(int(m) for m in cells['cells'] if int(m)&~support(live,'j')==0)
result=[];survivors=[]
for mi,mj in product(ci,cj):
 rows={r for r in live if projection(r,'i')&~mi==0 and projection(r,'j')&~mj==0}
 good,rr=fixed(rows)
 ss=[support(good,w) for w in ('i','j','u')]
 d={'cap_masks':[mi,mj],'stable_supports':ss,'stable_rows':len(good),'necessary_possible':ss==[mi,mj,319],'rounds':rr}
 result.append(d)
 if d['necessary_possible']:
  d['rows']=[name(r) for r in sorted(good)];survivors.append(d)
print('pairs',len(result),'survivors',len(survivors),[(d['cap_masks'],d['stable_rows']) for d in survivors],flush=True)
out={'pins':['z','s','j','i','w','t','p','q'],'edges':EDGES,'authority':'same-H necessary finite Kempe screen, not source realizability','upper_rows':[name(r) for r in sorted(upper)],'fixed_rows':[name(r) for r in sorted(live)],'fixed_rounds':rounds,'cap_candidates':[ci,cj],'pairs':result,'survivors':survivors,'source_instances':0,'source_coverage':'not triggered'}
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--check',type=Path);ap.add_argument('--output',type=Path)
a=ap.parse_args()
if a.check:
 if json.loads(a.check.read_text())!=json.loads(json.dumps(out)):raise ValueError('certificate differs from exhaustive recomputation')
 print('certificate verified')
elif a.output:
 with a.output.open('x') as f:f.write(json.dumps(out,indent=2)+'\n')

