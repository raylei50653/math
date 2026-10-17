#!/usr/bin/env python3
"""Explore all six actual ear caps, keeping the same H relation."""
from pathlib import Path
src=Path(__file__).with_name('explore_shared_caps.py').read_text()
exec(compile(src.split('upper={')[0],str(Path(__file__).with_name('explore_shared_caps.py')),'exec'))
base=json.loads((P/'shared-caps-exploration.json').read_text())
live={tuple('ABCD'.index(c) for c in r) for r in base['fixed_rows']}
K=set(map(int,json.loads((P/'cells.json').read_text())['cells']))
def earbit(r,d):
 return bit(r[:d]+r[d+1:6]) if r[(d-1)%6]!=r[(d+1)%6] else 0
def earmask(rows,d):
 ans=0
 for r in rows:ans|=earbit(r,d)
 return ans
result=[]
for d in range(6):
 mask=earmask(live,d);surv=[]
 for m in sorted(k for k in K if k&~mask==0):
  gg,rr=fixed({r for r in live if earbit(r,d)&~m==0})
  ss=[support(gg,w) for w in ('i','j','u')]
  if ss==[1022,1022,319] and earmask(gg,d)==m:surv.append({'mask':m,'rows':len(gg)})
 result.append({'drop':d,'upper':mask,'survivors':surv})
print(json.dumps(result,indent=2))
(P/'six-caps-exploration.json').write_text(json.dumps(result,indent=2)+'\n')
