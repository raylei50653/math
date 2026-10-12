#!/usr/bin/env python3
import json
from pathlib import Path
from hashlib import sha256
path=Path(__file__).with_name('cap_probe.json')
p=json.loads(path.read_text());patterns=p['pattern_order'];queries=0
for strmask,d in p['relations'].items():
 n=d['actual_cap_vertex_count'];edges=d['actual_cap_edges'];adj=[[] for _ in range(n)]
 for u,v in edges:adj[u].append(v);adj[v].append(u)
 mask=0
 for pi,b in enumerate(patterns):
  queries+=1
  if any(b[u]==b[v] for u,v in edges if u<7 and v<7):continue
  colors=list(b)+[-1]*(n-7)
  def extend():
   opts=[]
   for v in range(7,n):
    if colors[v]!=-1:continue
    av=set(range(4))-{colors[u] for u in adj[v] if colors[u]!=-1}
    if not av:return False
    opts.append((len(av),v,av))
   if not opts:return True
   _,v,av=min(opts,key=lambda o:o[0])
   for c in av:
    colors[v]=c
    if extend():colors[v]=-1;return True
   colors[v]=-1
   return False
  if extend():mask|=1<<pi
 assert mask==int(strmask),(strmask,mask,d)
 assert mask&p['inner_mask'],('disjoint',strmask)
result=dict(literal_cap_graphs=len(p['relations']),full_row_queries=queries,
            mismatches=0,disjoint_hits=0,certificate_sha256=sha256(path.read_bytes()).hexdigest())
print(json.dumps(result,sort_keys=True))
