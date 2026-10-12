#!/usr/bin/env python3
"""Limited exterior controls for the surviving C7 upper bound; not exhaustive."""
import argparse
from itertools import product, combinations
import json
from hashlib import sha256
from pathlib import Path
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
mode=parser.add_mutually_exclusive_group(required=True)
mode.add_argument('--check',action='store_true')
mode.add_argument('--write',action='store_true')
parser.add_argument('--certificate',type=Path,default=HERE/'cap_probe.json')
args=parser.parse_args()
CATALOGUE=HERE/'frozen/artifacts/c5_cells/cells.json'
S=755425272170557940120206052

def norm(p):
 d={};return tuple(d.setdefault(c,len(d)) for c in p)
P=sorted({norm(p) for p in product(range(4),repeat=7) if all(p[i]!=p[(i+1)%7] for i in range(7))})
P5=sorted({norm(p) for p in product(range(4),repeat=5) if all(p[i]!=p[(i+1)%5] for i in range(5))});I5={p:i for i,p in enumerate(P5)}
k=json.loads(CATALOGUE.read_text())['cells']
C5=[(i,(i+1)%5) for i in range(5)]
relations={};templates=[];tested=0;hits=[]
for first in range(5):
 b=list(range(5));u,v=b[first],b[(first+1)%5];b.insert(first+1,5);es=C5+[(u,5),(v,5)]
 for second in range(6):
  c=b[:];u,v=c[second],c[(second+1)%6];c.insert(second+1,6);edges=es+[(u,6),(v,6)]
  for rot in range(7):
   for refl in [False,True]:
    # canonical outer index j refers to literal original vertex c[rot +/- j]
    outer=[c[(rot+(-j if refl else j))%7] for j in range(7)];pos={v:j for j,v in enumerate(outer)}
    mapped=[(pos[u],pos[v]) for u,v in edges];old=[pos[j] for j in range(5)]
    pullback=[]
    for p in P:
     pullback.append(I5[norm(tuple(p[j] for j in old))] if all(p[u]!=p[v] for u,v in mapped) else -1)
    for r in map(int,k):
     mask=sum(1<<i for i,j in enumerate(pullback) if j>=0 and r>>j&1)
     tested+=1
     relations.setdefault(mask,dict(kind='C5-two-ears',source_mask=r,first=first,second=second,outer=outer,template_edges=edges))
     if not mask&S:hits.append((mask,relations[mask]));break
    if hits:break
   if hits:break
  if hits:break
 if hits:break
print('C5-ears',tested,'distinct',len(relations),'hits',hits[:1])
# Every subset of seven spokes is a literal planar hub patch.
cycle=[(i,(i+1)%7) for i in range(7)]
hub_relations={}
for spoke_mask in range(128):
 mask=0
 for i,p in enumerate(P):
  if len({p[j] for j in range(7) if spoke_mask>>j&1})<4:mask|=1<<i
 hub_relations.setdefault(mask,dict(kind='partial-7-hub',spoke_mask=spoke_mask))
 if not mask&S:hits.append((mask,hub_relations[mask]))
print('hub',128,'distinct',len(hub_relations),'hits',hits[:1])
# Every triangulation via recursive polygon dissection.
def triangulations(poly):
 if len(poly)<=3:return [set()]
 out=[]
 for j in range(1,len(poly)-1):
  left=poly[:j+1];right=poly[j:]
  fixed={tuple(sorted(e)) for e in [(poly[0],poly[j]),(poly[j],poly[-1])] if (e[0]-e[1])%7 not in (1,6)}
  for a in triangulations(left):
   for b in triangulations(right):out.append(a|b|fixed)
 return out
tris={tuple(sorted(e)) for e in triangulations(tuple(range(7)))}
trirels={}
for edges in sorted(tris):
 mask=sum(1<<i for i,p in enumerate(P) if all(p[u]!=p[v] for u,v in edges))
 trirels.setdefault(mask,dict(kind='7-outerplanar-triangulation',chords=edges))
 if not mask&S:hits.append((mask,trirels[mask]))
print('triangulations',len(tris),'distinct',len(trirels),'hits',hits[:1])
allrels={**relations,**hub_relations,**trirels}
for mask, desc in allrels.items():
 if desc['kind']=='C5-two-ears':
  source=k[str(desc['source_mask'])]
  # Source interiors 5,... become 7,...; newly introduced boundary ears are 5,6.
  rename=lambda v:v if v<5 else v+2
  pos={v:j for j,v in enumerate(desc['outer'])}
  frame=lambda v:pos[v] if v<7 else v
  es=desc['template_edges']+[(rename(u),rename(v)) for u,v in source['edges']]
  desc['actual_cap_vertex_count']=7+source['k_eff']
  desc['actual_cap_edges']=sorted({tuple(sorted((frame(u),frame(v)))) for u,v in es})
 elif desc['kind']=='partial-7-hub':
  desc['actual_cap_vertex_count']=8
  desc['actual_cap_edges']=cycle+[(i,7) for i in range(7) if desc['spoke_mask']>>i&1]
 else:
  desc['actual_cap_vertex_count']=7
  desc['actual_cap_edges']=cycle+list(desc['chords'])
out=dict(source_catalogue_sha256=sha256(CATALOGUE.read_bytes()).hexdigest(),inner_mask=S,pattern_order=P,c5_two_ear_cases=tested,c5_two_ear_distinct=len(relations),hub_cases=128,hub_distinct=len(hub_relations),triangulation_cases=len(tris),triangulation_distinct=len(trirels),combined_distinct=len(allrels),disjoint_hits=hits,relations={str(r):d for r,d in sorted(allrels.items())})
assert tested==55440 and len(relations)==3318 and len(allrels)==3383 and not hits
if args.write:
 with args.certificate.open('x') as f:
  json.dump(out,f,separators=(',',':'),sort_keys=True);f.write('\n')
else:
 assert json.loads(args.certificate.read_text())==json.loads(json.dumps(out)), 'certificate mismatch'
print('PASS combined',len(allrels),'disjoint hits',len(hits))
