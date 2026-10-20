#!/usr/bin/env python3
"""Compact support obstruction for the bounded left family, not a source theorem."""
import combined as c
from pathlib import Path
import json
D=c.D
rel=c.relations();d=json.loads((D/'interface-search-2.json').read_text());T=sum(1<<i for i in d['forbidden_ids']);allrows=[]
for a in c.p.ALPHA_IDS:
 sups=[s for s in rel if s&(1<<a)];minimal=[s for s in sups if not any(t!=s and (t&s)==t for t in sups)]
 intersections=T
 for s in sups:intersections &=s
 badsets=sorted({s&T for s in sups},key=int.bit_count)
 badminimal=[s for s in badsets if not any(t!=s and (t&s)==t for t in badsets)]
 # Exact branch-and-bound smallest hitting set; branch on smallest uncovered set.
 best=[T]
 def hit(chosen,left):
  if not left:
   if chosen.bit_count()<best[0].bit_count():best[0]=chosen
   return
  if chosen.bit_count()>=best[0].bit_count():return
  b=min(left,key=int.bit_count)
  while b:
   v=b&-b;b-=v
   hit(chosen|v,[s for s in left if not s&v])
 hit(0,badminimal)
 rec={'alpha_id':a,'relations':len(sups),'minimal_support_relations':[rel[s] for s in minimal],'common_forbidden_ids':[i for i in range(91) if intersections&(1<<i)],'minimal_forbidden_sets':[[i for i in range(91) if s&(1<<i)] for s in badminimal],'minimum_hitting_set':[i for i in range(91) if best[0]&(1<<i)]}
 allrows.append(rec)
with (D/'obstruction.json').open('x') as f:json.dump({'scope':'bounded<=2-interior left replacement relation obstruction','by_alpha':allrows},f,sort_keys=True,indent=2);f.write('\n')
for row in allrows:print(json.dumps({k:v for k,v in row.items() if k!='minimal_support_relations'}))
