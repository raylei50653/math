import itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent.parent
cat=json.loads((P/'frozen/artifacts/c5_cells/cells.json').read_text())
PAIRS=tuple(itertools.combinations(range(4),2))
def adj(n,E):
 a=[set() for _ in range(n)]
 for u,v in E:a[u].add(v);a[v].add(u)
 return a

def lifts(a,b):
 c=list(b)+[-1]*(len(a)-len(b))
 if any(c[u]==c[v] for u in range(len(b)) for v in a[u] if v<len(b)):return
 def rec():
  unseen=[u for u,x in enumerate(c) if x<0]
  if not unseen:
   yield tuple(c);return
  u=max(unseen,key=lambda u:(len({c[v] for v in a[u] if c[v]>=0}),len(a[u]),-u))
  used={c[v] for v in a[u]}
  for x in range(4):
   if x not in used:
    c[u]=x;yield from rec()
  c[u]=-1
 yield from rec()

def comps(a,c,p):
 un={i for i,x in enumerate(c) if x in p};out=[]
 while un:
  r=min(un);un.remove(r);q=[r]
  for u in q:
   for v in sorted(a[u]&un):un.remove(v);q.append(v)
  out.append(tuple(sorted(q)))
 return tuple(out)

def sig(a,c):
 return c[:5],tuple(tuple(tuple(v for v in q if v<5) for q in comps(a,c,p) if any(v<5 for v in q)) for p in PAIRS)

def run(n,E,bs,name):
 a=adj(n,E);seen={};N=0;S=set();counts=[]
 for b in bs:
  C=sorted(lifts(a,b));counts.append(len(C))
  for c in C:
   N+=1;s=sig(a,c);S.add(s)
   for p in PAIRS:
    for q in comps(a,c,p):
     for r in q:
      if r>=5:continue
      t=tuple(sum(p)-x if v in q else x for v,x in enumerate(c));ts=sig(a,t);key=(s,p,r)
      if key in seen and seen[key][0]!=ts:
       old=seen[key];w=dict(name=name,n=n,edges=E,pair=p,root=r,source1=old[1],source2=c,target1=old[2],target2=t,source_signature=s,target_signature1=old[0],target_signature2=ts)
       (P/'experiment/first_collision.json').write_text(json.dumps(w,indent=2)+'\n');print('COLLISION',name,N,flush=True);return True
      seen[key]=(ts,c,t)
 print(name,N,len(S),counts,flush=True)
 return False
if __name__=='__main__':
 for name,row in sorted(cat['cells'].items(),key=lambda kv:int(kv[0])):
  E=sorted(set(tuple(sorted(e)) for e in row['edges']+[[i,(i+1)%5] for i in range(5)]))
  if run(5+row['k_eff'],E,cat['pattern_order'],name):break
 else:
  eq=json.loads((P/'frozen/artifacts/c5_cells/equal_cut_witness.json').read_text());run(eq['graph']['n'],eq['graph']['edges'],cat['pattern_order'],'survivor-811')
