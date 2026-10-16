#!/usr/bin/env python3
"""Original c/a split nine-boundary partitions, then glue components to H."""
from pathlib import Path
src=Path(__file__).with_name('explore_shared_caps.py').read_text()
exec(compile(src.split('upper={')[0],str(Path(__file__).with_name('explore_shared_caps.py')),'exec'))
H_EDGES=EDGES
EDGES9=tuple((k,(k+1)%9) for k in range(9))
MAP=(0,1,2,3,4,5,0,6,7)
@lru_cache(None)
def opts9(row,pairing):
 r9=tuple(row[i] for i in MAP)
 pp=[]
 for pair in pairing:
  v=tuple(i for i,c in enumerate(r9) if c in pair)
  good=[]
  for p in parts(v):
   lab={u:k for k,b in enumerate(p) for u in b}
   if all(lab[a]==lab[b] for a,b in EDGES9 if a in lab and b in lab):good.append(p)
  pp.append(good)
 result=set()
 for p0,p1 in product(*pp):
  blocks=p0+p1;lab={u:k for k,b in enumerate(blocks) for u in b}
  if any(lab[a]==lab[c] and lab[b]==lab[d] and lab[a]!=lab[b] for a,b,c,d in combinations(range(9),4)):continue
  bp=[]
  for p,pair in zip((p0,p1),pairing):
   glued=[];hub=[]
   for b in p:
    b8=set(MAP[u] for u in b)
    if 0 in b8:hub.extend(b8)
    else:glued.append(tuple(sorted(b8)))
   if hub:glued.append(tuple(sorted(set(hub))))
   bp.extend((b,pair) for b in glued)
  orbit=set()
  for flag in range(1<<len(bp)):
   r=list(row)
   for k,(b,pair) in enumerate(bp):
    if flag>>k&1:
     for u in b:r[u]=pair[0] if r[u]==pair[1] else pair[1]
   orbit.add(canon(r))
  result.add(frozenset(orbit))
 return tuple(result)
def fixed9(rows):
 live=set(rows);rounds=[]
 while True:
  dead={r for r in live if any(not any(o<=live for o in opts9(r,pairing)) for pairing in PAIRINGS)}
  rounds.append({'live':len(live),'removed':[name(r) for r in sorted(dead)]})
  if not dead:return live,rounds
  live-=dead
base=json.loads((P/'shared-caps-exploration.json').read_text())
upper={tuple('ABCD'.index(c) for c in r) for r in base['upper_rows']}
live,rounds=fixed9(upper)
print('ninefixed',len(live),[support(live,w) for w in ('i','j','u')],[(d['live'],len(d['removed'])) for d in rounds],flush=True)
ci=base['cap_candidates'][0];cj=base['cap_candidates'][1]
result=[]
for mi,mj in product(ci,cj):
 rows={r for r in live if projection(r,'i')&~mi==0 and projection(r,'j')&~mj==0}
 good,rr=fixed9(rows);ss=[support(good,w) for w in ('i','j','u')]
 if ss==[mi,mj,319]:result.append({'caps':[mi,mj],'rows':[name(r) for r in sorted(good)]})
print('survivors',[(d['caps'],len(d['rows'])) for d in result],flush=True)
out={'original_split_boundary':['c','s','j','i','w','t','a','p','q'],'split_colours':'c=a=z','split_vertices_need_not_be_connected':True,'full_H_component_glue':MAP,'upper_rows':base['upper_rows'],'fixed_rows':[name(r) for r in sorted(live)],'rounds':rounds,'survivors':result,'source_coverage':'not triggered'}
(P/'split-nine-exploration.json').write_text(json.dumps(out,indent=2)+'\n')
