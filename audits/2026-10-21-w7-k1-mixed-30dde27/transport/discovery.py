from collections import defaultdict,Counter
from itertools import product
from pathlib import Path
import gzip,json,importlib.util

def mod(path,name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
old=mod('audits/2026-10-21-w7-single-barrier-30dde27/transport/check.py','old')
cap=mod('audits/2026-10-21-w7-single-barrier-30dde27/independent_caps.py','cap')
collar=mod('audits/2026-10-21-w7-profile0-13e51db/check.py','collar')
b='audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/'
o=json.load(gzip.open(b+'orbits.json.gz'));c=json.load(gzip.open(b+'caps.json.gz'));rim=old.RIM;P=old.P;index={tuple(x):i for i,x in enumerate(c['states'])};rstate=dict(o['rowids']);inc=defaultdict(list)
for j,col in enumerate(o['columns']):
 for h in col:inc[h].append(j)

def components(g,col,pair):return old.graph_components(g,col,pair)
def kernel(g,col):
 fixed={v:x for v,x in col.items() if v not in P};domains=[sorted(set(range(4))-{fixed[z] for z in g[v] if z in fixed})for v in P];out=[]
 for path in product(*domains):
  if any(a==b for a,b in zip(path,path[1:])):continue
  colors=col|dict(zip(P,path));counts,bad=cap.direct_caps(tuple(colors[v] for v in rim));out.append((path,bad))
 return out
summary=Counter();surv=[];details=[]
for center_i in [2,4,5]:
 counts=[0]*6;counts[center_i]=1;data,g=collar.collar(0,counts,True);g={v:adj-{'p','h','R'} for v,adj in g.items() if v not in {'p','h','R'}}
 for i,v in enumerate(rim):u=rim[(i+1)%13];g.setdefault(v,set()).add(u);g.setdefault(u,set()).add(v)
 path=data['boundary'][1:];y=next(v for v in path if v.startswith('H'));pos=path.index(y);base=dict(zip(P,[1,2,1,2,1,2]))
 for i,v in enumerate(path):base[v]=[0,3][i%2] if i<pos else 3-base[P[center_i]] if i==pos else [3,0][(len(path)-1-i)%2]
 beta=base[path[pos-1]];x=3-beta;eta=base[y];pair=(eta,x);mate=1 # both remaining mixed splits 01|23
 for target,z0,j03 in old.TARGETS:
  original=base|dict(zip(rim,c['states'][target]));h=old.halfrow(c['states'][target],mate)
  for j in inc[h]:
   bbs=old.blocks(o['columns'][j]);lookup={v:k for k,bb in enumerate(bbs) for v in bb}
   # Original collar compatibility.
   okay=all(len({lookup[rim.index(v)] for v in comp if v in rim})<=1 for pp in [(0,1),(2,3)]for comp in components(g,original,pp))
   if not okay:continue
   for bb in bbs:
    if original[rim[bb[0]]] not in pair:continue
    names={rim[i] for i in bb};chosen=set(names)|{y}
    for zi in [f'z{i}'for i in range(1,6)]:
     if original[zi]==x:
      ends=[t for t in P if t in g[zi] and original[t]==eta];assert len(ends)==1
      if ends[0] in names:chosen.add(zi)
    colors={v:(eta^x^co if v in chosen else co)for v,co in original.items()}
    assert all(colors[a]!=colors[b]for a in g for b in g[a]),(center_i,target,j,names)
    kr=kernel(g,colors);bad=next(((pp,bad)for pp,bad in kr if bad),None)
    summary[(P[center_i],target,bad is None)]+=1
    row={'center':P[center_i],'target':target,'source_column':j,'marked_y_block':sorted(names),'new_rim':[colors[v]for v in rim],'canonical_state':index[tuple(old.canon([colors[v]for v in rim]))],'new_A':[(v,colors[v])for v in path],'lifts':len(kr),'bad':bad}
    details.append(row)
    if bad is None:surv.append(row)
print('summary',dict(summary),'survive',len(surv),'total',len(details))
for row in surv:print('SURVIVE',row)
Path('audits/2026-10-21-w7-k1-mixed-30dde27/transport/discovery.json').write_text(json.dumps(details,indent=2))
