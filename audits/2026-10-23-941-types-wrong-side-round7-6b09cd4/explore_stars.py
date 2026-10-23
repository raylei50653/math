"""Full same-graph stars in the seven-resource envelope, no source realization."""
import itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def edge(a,b):return tuple(sorted((a,b)))
def reconstruct(contract):
 result=[]
 for cell in contract['candidates']:
  if cell['classification']!='local_necessary_type':continue
  for kinds in [('N1','N1'),('N1','N3'),('N3','N3'),('N1','K0'),('N1','K2'),('N3','K0'),('N3','K2')]:
   for alias in [False,True]:
    co=dict(contract['original_colors'],a=3,y=1,b=3,p_d=2,p_x=2,U=0,omega=int(kinds[0][1]),eta=int(kinds[1][1]))
    la=dict(contract['original_component_labels'],a='N',y='N',b='N',p_d='K',p_x='K',U='K',omega=kinds[0][0],eta=kinds[1][0])
    im=lambda v:'d' if alias and v=='U' else v
    if alias:del co['U'];del la['U']
    es={edge(*e) for e in cell['edges']}|{edge(im(a),im(b)) for a,b in [('T','a'),('T','y'),('T','b'),('r','a'),('a','y'),('y','b'),('b','s'),('d','p_d'),('x','p_x')]}
    adj={v:set() for v in co}
    for a,b in es:adj[a].add(b);adj[b].add(a)
    original=set(contract['original_colors']);old={edge(*e) for e in cell['edges']}
    links=dict(T=['r','tau','s','b','y','a'])
    for v in ['tau','zeta']:links[v]=sorted(adj[v])
    psi={v:c^2 if la[v]=='K' else c for v,c in co.items()}
    sides={'r':'C','d':'C','e':'C','s':'E','x':'E','h':'E'}
    if not alias:sides['U']='C'
    def basic(a,b):
     if a==b or co[a]==co[b]:return False
     if {a,b}<=original and edge(a,b) not in old:return False
     if {a,b}&{'tau','zeta'} and edge(a,b) not in old:return False
     if {co[a],co[b]}<={0,2} and la[a]!=la[b]:return False
     if {co[a],co[b]}<={1,3} and la[a]!=la[b]:return False
     if la[a]!='K' and la[b]!='K' and ((la[a] in {'M','N'})!=(la[b] in {'M','N'})):return False
     if {psi[a],psi[b]}=={1,2} and a in sides and b in sides and sides[a]!=sides[b]:return False
     for v,lk in links.items():
      if a==v and b not in lk or b==v and a not in lk:return False
      if v not in ('tau','zeta') and a in lk and b in lk and (lk.index(a)-lk.index(b))%len(lk) not in (1,len(lk)-1):return False
     return True
    def valid(g):
     if any(not basic(a,b) for a in g for b in g[a]):return False
     if any(len(g[a]&g[b])>2 for a,b in itertools.combinations(co,2)):return False
     if (g['r']&g['s']|g['d']&g['x'])-original:return False
     unseen={v for v in co if psi[v] in (1,2)}
     while unseen:
      v=min(unseen);todo=[v];seen=set()
      while todo:
       v=todo.pop()
       if v in seen:continue
       seen.add(v);todo.extend(g[v]&unseen-seen)
      unseen-=seen
      if {sides.get(v) for v in seen}>={'C','E'}:return False
     return all(g[v]==set(lk) for v,lk in links.items())
    def options(center,arc,g):
     pool=sorted(v for v in co if basic(center,v) and v not in arc)
     def walk(seq,left):
      lk=arc+seq
      if len(lk)>=5 and g[center]<=set(lk) and basic(lk[-1],lk[0]):
       ng={v:set(nb) for v,nb in g.items()}
       for a,b in [(center,v) for v in lk]+list(zip(lk,lk[1:]+lk[:1])):ng[a].add(b);ng[b].add(a)
       if valid(ng) and all(edge(a,b) not in {edge(x,y) for x,y in itertools.combinations(lk,2) if (lk.index(x)-lk.index(y))%len(lk) not in (1,len(lk)-1)} for a in ng for b in ng[a] if a in lk and b in lk):yield lk,ng
      for v in left:
       if not basic(lk[-1],v):continue
       if any(v in g[x] for x in lk[:-1] if x!=lk[0]):continue
       yield from walk(seq+[v],[w for w in left if w!=v])
     yield from walk([],pool)
    def inner_arc(center,start,end):
     g={v:set() for v in original if v!=center}
     for f in cell['faces']:
      if center in f:
       a,b=[v for v in f if v!=center];g[a].add(b);g[b].add(a)
     path=[start]
     while path[-1]!=end:path.append(next(v for v in g[path[-1]] if len(path)<2 or v!=path[-2]))
     return path
    centers=['a','b','y','r','s','omega']+(['eta'] if kinds[1][0]=='N' else [])
    counts=[0]*(len(centers)+1);rows=[]
    def visit(i,g):
     counts[i]+=1
     if i==len(centers):
      rows.append(dict(full_links={v:lk for v,lk in links.items() if v not in ('tau','zeta')},edges=[list(e) for e in sorted({edge(a,b) for a in g for b in g[a]})]));return
     v=centers[i]
     arc={'a':['r','T','y'],'b':['s','T','y'],'y':['a','T','b']}.get(v)
     if v=='r':arc=inner_arc('r','d','T')+['a']
     if v=='s':arc=inner_arc('s','T','x');arc=['b']+arc
     arcs=[arc] if arc else [[a] for a in sorted(g[v])[:1]]
     if not arcs:arcs=[[a] for a in sorted(co) if la[a]=='N' and co[a]!=co[v] and basic(v,a)]
     for start in arcs:
      for lk,ng in options(v,start,g):
       links[v]=lk;visit(i+1,ng);del links[v]
    if valid(adj):visit(0,adj)
    result.append(dict(cell=cell['id'],core=cell['core'],kinds=kinds,d_equals_U=alias,centers=centers,stage_counts=counts,rows=rows))
 return result
if __name__=='__main__':
 contract=json.loads((HERE/'entry/audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json').read_text())
 rows=reconstruct(contract)
 with (HERE/'EXPLORATION_STARS.json').open('x') as f:json.dump(rows,f,indent=2);f.write('\n')
 for kinds in [('N1','N1'),('N1','N3'),('N3','N3'),('N1','K0'),('N1','K2'),('N3','K0'),('N3','K2')]:
  rr=[r for r in rows if tuple(r['kinds'])==kinds];print(kinds,'contexts',len(rr),'partial',sum(r['stage_counts'][-2] for r in rr),'full',sum(len(r['rows']) for r in rr),flush=True)
