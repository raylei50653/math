from pathlib import Path
src=Path(__file__).with_name('explore_shared_caps.py').read_text()
exec(compile(src.split('upper={')[0],str(Path(__file__).with_name('explore_shared_caps.py')),'exec'))
# K=J-v: pins m,j,i,w,z,p,q, actual boundary first4.
EDGES_K=((0,1),(1,2),(2,3),(3,0),(0,4),(4,5),(5,6),(6,4))
@lru_cache(None)
def optsK(row,pairing):
 pp=[]
 for pair in pairing:
  vv=tuple(i for i,c in enumerate(row) if c in pair);good=[]
  for pa in parts(vv):
   lab={u:k for k,bb in enumerate(pa) for u in bb}
   if all(lab[a]==lab[b] for a,b in EDGES_K if a in lab and b in lab):good.append(pa)
  pp.append(good)
 result=set()
 for p0,p1 in product(*pp):
  blocks=p0+p1;lab={u:k for k,bb in enumerate(blocks) for u in bb}
  if any(lab[a]==lab[c] and lab[b]==lab[d] and lab[a]!=lab[b] for a,b,c,d in combinations(range(4),4)):continue
  bp=[(bb,pair) for pa,pair in zip((p0,p1),pairing) for bb in pa];orbit=set()
  for flag in range(1<<len(bp)):
   rr=list(row)
   for k,(bb,pair) in enumerate(bp):
    if flag>>k&1:
     for u in bb:rr[u]=pair[0] if rr[u]==pair[1] else pair[1]
   orbit.add(canon(rr))
  result.add(frozenset(orbit))
 return tuple(result)
def fixedK(rows):
 live=set(rows);rounds=[]
 while True:
  dead={rr for rr in live if any(not any(o<=live for o in optsK(rr,pairing)) for pairing in PAIRINGS)}
  rounds.append({'live':len(live),'removed':len(dead)})
  if not dead:return live,rounds
  live-=dead
def toK(r):return canon((r[1],r[2],r[3],r[4],r[0],r[6],r[7]))
base=json.loads((P/'combined-source-exploration.json').read_text())[0]
live={tuple('ABCD'.index(c) for c in s) for s in base['H_fixed']}
rounds=[]
while True:
 before=set(live)
 kk={toK(r) for r in live if r[1]==r[5]}
 kl,kr=fixedK(kk)
 live={r for r in live if r[1]!=r[5] or toK(r) in kl}
 live,hr=fixed(live)
 rounds.append({'before_H':len(before),'K_upper':len(kk),'K_after':len(kl),'K_rounds':kr,'H_after':len(live),'H_rounds':hr})
 if live==before:break
print('quadrilateral',len(live),[support(live,w) for w in ('i','j','u')],rounds)
(P/'quadrilateral-exploration.json').write_text(json.dumps({'rows':[name(r) for r in sorted(live)],'rounds':rounds},indent=2)+'\n')
