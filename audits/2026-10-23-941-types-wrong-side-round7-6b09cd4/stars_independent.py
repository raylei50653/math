"""Independent cycle-catalog Cartesian join; no use of the DFS star compiler."""
from itertools import combinations,permutations
def edge(a,b):return tuple(sorted((a,b)))
def audit(contract,cell,kinds,alias):
 color=dict(contract['original_colors'],a=3,b=3,y=1,p_d=2,p_x=2,U=0,omega=int(kinds[0][1]),eta=int(kinds[1][1]))
 owner=dict(contract['original_component_labels'],a='N',b='N',y='N',p_d='K',p_x='K',U='K',omega=kinds[0][0],eta=kinds[1][0])
 if alias:del color['U'];del owner['U']
 original=set(contract['original_colors']);old={edge(*e) for e in cell['edges']}
 base=old|{edge(a,b) for a,b in [('T','a'),('T','y'),('T','b'),('r','a'),('a','y'),('y','b'),('b','s'),('d','p_d'),('x','p_x')]}
 verts=sorted(color);pairs=list(combinations(verts,2))
 fixed={'T':('r','tau','s','b','y','a')}
 for v in ['tau','zeta']:fixed[v]=tuple(b if a==v else a for a,b in old if v in (a,b))
 forbidden=set()
 for a,b in pairs:
  bad=(color[a]==color[b] or ({a,b}<=original and edge(a,b) not in old)
   or (bool({a,b}&{'tau','zeta'}) and edge(a,b) not in old)
   or ({color[a],color[b]}<={0,2} and owner[a]!=owner[b])
   or ({color[a],color[b]}<={1,3} and owner[a]!=owner[b])
   or (owner[a]!='K' and owner[b]!='K' and ((owner[a] in ('M','N'))!=(owner[b] in ('M','N')))))
  if bad:forbidden.add(edge(a,b))
 for v,lk in fixed.items():
  forbidden|={edge(v,w) for w in verts if w!=v and w not in lk}
  if v=='T':forbidden|={edge(a,b) for a,b in combinations(lk,2) if abs(lk.index(a)-lk.index(b)) not in (1,len(lk)-1)}
 psi={v:(c^2 if owner[v]=='K' else c) for v,c in color.items()}
 sideC={'r','d','e'}|({'U'} if not alias else set());sideE={'s','x','h'}
 def valid(es,sealed):
  if es&forbidden:return False
  adj={v:set() for v in verts}
  for a,b in es:adj[a].add(b);adj[b].add(a)
  if any(len(adj[a]&adj[b])>2 for a,b in pairs):return False
  if ((adj['r']&adj['s'])|(adj['d']&adj['x']))-original:return False
  for v,lk in {**fixed,**sealed}.items():
   if adj[v]!=set(lk):return False
   if v not in ('tau','zeta') and any(edge(a,b) in es for a,b in combinations(lk,2) if abs(lk.index(a)-lk.index(b)) not in (1,len(lk)-1)):return False
  # Independent connected-component calculation in the common literal psi.
  pending={v for v in verts if psi[v] in (1,2)}
  while pending:
   component={min(pending)}
   while True:
    enlarged=component|set().union(*(adj[v]&pending for v in component))
    if enlarged==component:break
    component=enlarged
   pending-=component
   if component&sideC and component&sideE:return False
  return True
 def inner(center,start,end):
  faces=[set(f)-{center} for f in cell['faces'] if center in f];arc=[start]
  while arc[-1]!=end:
   nxt=next(v for f in faces if arc[-1] in f for v in f if v!=arc[-1] and (len(arc)<2 or v!=arc[-2]));arc.append(nxt)
  return arc
 arcs={'a':['r','T','y'],'b':['s','T','y'],'y':['a','T','b'],'r':inner('r','d','T')+['a'],'s':['b']+inner('s','T','x')}
 centers=['a','b','y','r','s','omega']+(['eta'] if kinds[1][0]=='N' else [])
 catalogs={}
 for v in centers:
  allowed=[w for w in verts if w!=v and edge(v,w) not in forbidden]
  arc=arcs.get(v,[]);extra=[w for w in allowed if w not in arc];catalog=[]
  for size in range(max(0,5-len(arc)),len(extra)+1):
   for subset in combinations(extra,size):
    if not arc and not any(owner[w]=='N' for w in subset):continue
    for perm in permutations(subset if arc else subset[1:]):
     lk=tuple(arc)+perm if arc else (subset[0],)+perm
     if not arc and lk[1]>lk[-1]:continue
     cycle={edge(a,b) for a,b in zip(lk,lk[1:]+lk[:1])}
     es=cycle|{edge(v,w) for w in lk}
     if es&forbidden:continue
     if valid(base|es,{v:lk}):catalog.append((lk,es))
  catalogs[v]=catalog
 counts=[0]*(len(centers)+1)
 def join(i,es,sealed):
  counts[i]+=1
  if i==len(centers):return
  v=centers[i]
  for lk,edges in catalogs[v]:
   nextsealed={**sealed,v:lk};combined=es|edges
   if valid(combined,nextsealed):join(i+1,combined,nextsealed)
 if valid(base,{}):join(0,base,{})
 return dict(cell=cell['id'],kinds=list(kinds),d_equals_U=alias,catalog_counts={v:len(catalogs[v]) for v in centers},stage_counts=counts,complete_join_count=counts[-1])
