#!/usr/bin/env python3
"""Original nine-boundary disk, all original five-vertex reconstruction lifts."""
from pathlib import Path
src=Path(__file__).with_name('explore_shared_caps.py').read_text()
exec(compile(src.split('upper={')[0],str(Path(__file__).with_name('explore_shared_caps.py')),'exec'))
# nine pins c,s,j,i,w,t,a,p,q; original added vertices v,r,x,y,b.
EDGES=tuple((k,(k+1)%9) for k in range(9))
@lru_cache(None)
def optsF(row,pairing):
 pp=[]
 for pair in pairing:
  vv=tuple(i for i,c in enumerate(row) if c in pair);good=[]
  for pa in parts(vv):
   lab={u:k for k,bb in enumerate(pa) for u in bb}
   if all(lab[a]==lab[b] for a,b in EDGES if a in lab and b in lab):good.append(pa)
  pp.append(good)
 result=set()
 for p0,p1 in product(*pp):
  blocks=p0+p1;lab={u:k for k,bb in enumerate(blocks) for u in bb}
  if any(lab[a]==lab[c] and lab[b]==lab[d] and lab[a]!=lab[b] for a,b,c,d in combinations(range(9),4)):continue
  bp=[(bb,pair) for pa,pair in zip((p0,p1),pairing) for bb in pa];orbit=set()
  for flag in range(1<<len(bp)):
   rr=list(row)
   for k,(bb,pair) in enumerate(bp):
    if flag>>k&1:
     for u in bb:rr[u]=pair[0] if rr[u]==pair[1] else pair[1]
   orbit.add(canon(rr))
  result.add(frozenset(orbit))
 return tuple(result)
def fixedF(rows):
 live=set(rows);rounds=[]
 while True:
  dead={rr for rr in live if any(not any(o<=live for o in optsF(rr,pairing)) for pairing in PAIRINGS)}
  rounds.append({'live':len(live),'removed':len(dead)})
  if not dead:return live,rounds
  live-=dead
@lru_cache(None)
def lifts(row):
 c,s,j,i,w,t,a,p,q=row;out=[]
 for v in COL:
  if v in(s,j,i,w):continue
  for r in COL:
   if r in(s,v,w,t):continue
   for x in COL:
    if x in(c,r,s):continue
    for y in COL:
     if y in(x,a,r,t):continue
     for b in COL:
      if b in(a,c,p,q):continue
      out.append((v,r,x,y,b,bit((x,y,a,b,c))))
 return tuple(out)
def smask(rows):
 m=0
 for rr in rows:
  for ll in lifts(rr):m|=ll[-1]
 return m
def umask(rows):
 m=0
 for rr in rows:
  c,s,j,i,w,t,a,p,q=rr
  if c!=a:continue
  for v in COL:
   if v not in(s,j,i,w):m|=bit((c,s,v,w,t))
 return m
properrows={canon(r) for r in product(COL,repeat=9) if all(r[a]!=r[b] for a,b in EDGES)}
print('properrows',len(properrows),flush=True)
results=[]
for S in (932,933,941):
 upper={rr for rr in properrows if all(ll[-1]&S for ll in lifts(rr))}
 print('source',S,'upper',len(upper),'s/u',smask(upper),umask(upper),flush=True)
 live,rounds=fixedF(upper)
 print('source',S,'fixed',len(live),'s/u',smask(live),umask(live),'rounds',rounds,flush=True)
 results.append({'source_mask':S,'upper_rows':[name(r) for r in sorted(upper)],'fixed_rows':[name(r) for r in sorted(live)],'source_lift_support':smask(live),'U_lift_support':umask(live),'rounds':rounds})
out={'pins':['c','s','j','i','w','t','a','p','q'],'added':['v','r','x','y','b'],'results':results}
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--check',type=Path);ap.add_argument('--output',type=Path)
a=ap.parse_args()
if a.check:
 if json.loads(a.check.read_text())!=json.loads(json.dumps(out)):raise ValueError('certificate differs from exhaustive recomputation')
 print('certificate verified')
elif a.output:
 with a.output.open('x') as f:f.write(json.dumps(out,indent=2)+'\n')

