from pathlib import Path
import json,time
H=Path(__file__).resolve().parent;g=json.load(open(H/'probe-realization-101.json'));n=len(g['functions']);adj=[set() for _ in range(n)]
for a,b in g['edges']:adj[a].add(b);adj[b].add(a)
start=time.time();nodes=0;solutions=[];complete=True
initial=[15]*n
for v,c in zip([g['pins'][i] for i in (0,5,6)],(0,1,2)):initial[v]=1<<c

def search(ds):
 global nodes
 nodes+=1
 if nodes%1000==0 and time.time()-start>30:raise TimeoutError
 change=True
 while change:
  change=False
  for u in range(n):
   if ds[u].bit_count()!=1:continue
   for v in adj[u]:
    if ds[v]&ds[u]:
     ds[v]&=~ds[u];change=True
     if not ds[v]:return
 todo=[v for v in range(n) if ds[v].bit_count()>1]
 if not todo:
  solutions.append([d.bit_length()-1 for d in ds]);return
 v=min(todo,key=lambda v:(ds[v].bit_count(),-len(adj[v]),v));mask=ds[v]
 for c in range(4):
  if mask>>c&1:
   child=ds[:];child[v]=1<<c;search(child)
try:search(initial)
except TimeoutError:complete=False
out={'vertices':n,'edges':len(g['edges']),'fixed_triangle_pins':[0,5,6],'fixed_colours':[0,1,2],'complete':complete,'nodes':nodes,'seconds':time.time()-start,'solutions':solutions};(H/'probe-graph-colourings-101.json').write_text(json.dumps(out)+'\n');print({k:v if k!='solutions' else len(v) for k,v in out.items()})
