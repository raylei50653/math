import networkx as nx, sys,random,json,time
from collections import Counter
from pathlib import Path
sys.path.insert(0,'scripts')
import four_color_three_step_kempe_escape as k
import four_color_three_step_cross_split_exclusion as old

rng=random.Random(9173)
G=nx.icosahedral_graph(); x,y=0,1
z,w=sorted(set(G[x])&set(G[y]));A=set(G[x])-{y,z,w}; D=set(G[y])-{x,z,w}
a=next(v for v in A if G.has_edge(z,v)); b=next(iter(A-{a}));d=next(v for v in D if G.has_edge(z,v)); c=next(iter(D-{d}))
labels={x:0,y:1,z:2,a:3,b:4,c:5,d:6,w:7}
for v in sorted(set(G)-labels.keys()):labels[v]=len(labels)
G=nx.relabel_nodes(G,labels)
frame=set(old.INNER_EDGES)
seen=set(); summary=Counter(); examples=[];start=time.time()
for n in range(12,19):
 if n>12:
  # Insert in a triangle wholly outside the protected center stars.
  planar,em=nx.check_planarity(G);seen_darts=set();faces=[]
  for u,v in em.edges():
   if (u,v) not in seen_darts:
    f=em.traverse_face(u,v,seen_darts)
    if not set(f)&{0,1}:faces.append(f)
  f=rng.choice(faces)
  G.add_node(n-1)
  for v in f:G.add_edge(n-1,v)
 for trial in range(900):
  planar,em=nx.check_planarity(G); assert planar
  seen_darts=set();faces=[];inc={}
  for u,v in em.edges():
   if (u,v) not in seen_darts:
    f=em.traverse_face(u,v,seen_darts);assert len(f)==3;faces.append(f)
    for u,v in zip(f,f[1:]+f[:1]):inc.setdefault(tuple(sorted((u,v))),[]).append(next(x for x in f if x not in (u,v)))
  options=[]
  for (u,v),ends in inc.items():
   if (u,v) in frame or len(ends)!=2:continue
   a,b=ends
   if a in (0,1) or b in (0,1) or G.has_edge(a,b):continue
   # Allow min4 at all vertices except protected 5-centers; this keeps enumeration small.
   if G.degree(u)<=4 or G.degree(v)<=4:continue
   options.append((u,v,a,b))
  if options:
   u,v,a,b=rng.choice(options);G.remove_edge(u,v);G.add_edge(a,b)
  edgekey=tuple(sorted(tuple(sorted(e)) for e in G.edges))
  if edgekey in seen:continue
  seen.add(edgekey)
  edges=tuple(e for e in edgekey if e[0]>=2 and e[1]>=2)
  states=k.enumerate_normalized(n-2,edges)
  supports={k.normalize(k.boundary(f)) for f in states}
  summary['graphs']+=1
  if not k.D16<=supports:summary['support_filter_rejected']+=1;continue
  lookup={f:i for i,f in enumerate(states)};adj=k.adjacency(n-2,edges);actions=[]
  for f in states:
   actions.append([[p,sum(1<<v for v in block),lookup[k.normalize(k.swapped(f,k.PAIRS[p],block))]] for p,blocks in enumerate(k.components(f,adj)) for block in blocks])
  dist,rec=k.distances(actions,states)
  summary['full_class_checks']+=1
  if len(rec['connected_component_sizes'])>1:
   summary['disconnected']+=1
   if len(examples)<5:examples.append({'n':n,'edges':edges,'summary':rec})
  if rec['d16_closed_state_orbits']:
   print('FOUND',n,trial,rec,flush=True)
   Path('scratch/2026-10-30-d16-closed-class/found.json').write_text(json.dumps({'n':n,'edges':edges,'summary':rec,'states':states,'actions':actions}))
   raise SystemExit
  if summary['graphs']%100==0:print(n,trial,summary,'last',len(states),'secs',round(time.time()-start,1),flush=True)
 print('END N',n,summary,'secs',round(time.time()-start,1),flush=True)
Path('scratch/2026-10-30-d16-closed-class/search-results.json').write_text(json.dumps({'seed':9173,'summary':dict(summary),'examples':examples},indent=2))
