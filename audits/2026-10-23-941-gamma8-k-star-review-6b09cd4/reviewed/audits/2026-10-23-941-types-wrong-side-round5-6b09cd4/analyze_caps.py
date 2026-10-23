#!/usr/bin/env python3
"""Exploratory independent union-of-faces analysis; no source-coverage verdict."""
import collections,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def edge(a,b):return tuple(sorted((a,b)))
def inspect(row):
 es={tuple(e) for e in row['edges']};links=row['full_links'];centers=set(links)|{'tau'}
 faces={tuple(sorted((v,a,b))) for v,lk in links.items() for a,b in zip(lk,lk[1:]+lk[:1])}
 tn={b if a=='tau' else a for a,b in es if 'tau' in (a,b)}
 faces|={tuple(sorted(('tau',a,b))) for a,b in itertools.combinations(tn,2) if edge(a,b) in es}
 fe=collections.defaultdict(list)
 for i,f in enumerate(sorted(faces)):
  for a,b in itertools.combinations(f,2):fe[edge(a,b)].append(i)
 if any(len(v)>2 for v in fe.values()):return dict(status='overused_edge')
 vertices=set().union(*map(set,faces));bd={e for e,fs in fe.items() if len(fs)==1};ba=collections.defaultdict(set)
 for a,b in bd:ba[a].add(b);ba[b].add(a)
 if any(len(v)!=2 for v in ba.values()):return dict(status='nonsimple_boundary')
 if set(ba)&centers:return dict(status='unsealed_center')
 if len(vertices)-len(fe)+len(faces)!=1:return dict(status='non_disk_euler')
 start=min(ba);cycle=[start];prev=None;cur=start
 while True:
  nex=min(ba[cur]-({prev} if prev else set()))
  if nex==start:break
  if nex in cycle:return dict(status='boundary_repeat')
  cycle.append(nex);prev,cur=cur,nex
 if len(cycle)!=len(ba):return dict(status='multiple_boundary')
 # Orient actual faces by the shared-edge constraint, allowing each input star
 # one joint reflection only insofar as the union has a global orientation.
 fs=sorted(faces);orientation={0:1};todo=[0]
 def sign(f,a,b):
  return 1 if any((f[j],f[(j+1)%3])==(a,b) for j in range(3)) else -1
 while todo:
  i=todo.pop();f=fs[i]
  for a,b in itertools.combinations(f,2):
   for j in fe[edge(a,b)]:
    if j==i:continue
    want=-orientation[i]*sign(f,a,b)*sign(fs[j],a,b)
    if j in orientation and orientation[j]!=want:return dict(status='nonorientable')
    if j not in orientation:orientation[j]=want;todo.append(j)
 if len(orientation)!=len(fs):return dict(status='disconnected_faces')
 for v in vertices:
  le={edge(a,b) for f in faces if v in f for a,b in [tuple(x for x in f if x!=v)]}
  adj=collections.defaultdict(set)
  for a,b in le:adj[a].add(b);adj[b].add(a)
  if any(len(n)>2 for n in adj.values()):return dict(status='branched_vertex_link')
  unseen=set(adj);todo=[next(iter(unseen))];seen=set(todo)
  while todo:
   for w in adj[todo.pop()]-seen:seen.add(w);todo.append(w)
  if seen!=unseen:return dict(status='disconnected_vertex_link')
  ds=sorted(map(len,adj.values()))
  if v in centers and ds!=[2]*len(adj):return dict(status='center_not_cyclic')
  if v not in centers and ds!=[1,1]+[2]*(len(adj)-2):return dict(status='boundary_not_path')
 return dict(status='disk',boundary=cycle,centers=sorted(centers),edges=[list(e) for e in sorted(fe)],faces=[list(f) for f in fs],vertices=sorted(vertices))
def main():
 p=ROOT/'audits/2026-10-23-941-gamma8-nonempty-k-stars-6b09cd4/explore.json'
 rows=json.loads(p.read_text());out=[]
 for i,r in enumerate(rows):out.append(dict(index=i,cell=r['cell'],omega_type=r['omega_type'],m_side=r['m_side'],**inspect(r)))
 dest=HERE/'explore-cap-unions.json'
 with dest.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps(dict(count=len(out),status=dict(collections.Counter(x['status'] for x in out)),collars=dict(collections.Counter((x['omega_type']+':'+str(len(x['boundary']))) for x in out if x['status']=='disk')))))
if __name__=='__main__':main()
