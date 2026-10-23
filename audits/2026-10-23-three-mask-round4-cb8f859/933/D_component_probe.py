exec((__import__('pathlib').Path(__file__).parent/'probe.py').read_text().split('for j in (73,76,196,198,257,259):')[0])
D=('a','n','R','L','q','c','s','v','w','t');cap_edges=[('x','y'),('x','c'),('x','s'),('x','r'),('y','a'),('y','t'),('y','r')]+[('r',v) for v in ('s','v','w','t')]+[('s','v'),('v','w'),('w','t'),('s','c'),('t','a')]
def parts(t=(0,)):
 if len(t)==10:yield t;return
 for c in range(max(t)+2):yield from parts(t+(c,))
four=list(itertools.combinations(range(10),4));nc10=[p for p in parts() if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in four)]
def properwords(t=(0,)):
 if len(t)==10:
  if t[-1]!=t[0]:yield t
  return
 for c in range(min(4,max(t)+2)):
  if c!=t[-1]:yield from properwords(t+(c,))
ds=list(properwords());di={t:i for i,t in enumerate(ds)};bad=set();reason={}
for j,tup in enumerate(ds):
 colors=dict(zip(D,tup))
 for r,x,y in itertools.product(range(4),repeat=3):
  cs=dict(colors,r=r,x=x,y=y)
  if all(cs[u]!=cs[v] for u,v in cap_edges):
   eid=index[m.canonical(tuple(cs[v] for v in m.PIN))]
   if eid in zeros:bad.add(j);reason[j]=[r,x,y,eid];break
print('Dwords',len(ds),'NC',len(nc10),'bad',len(bad),flush=True)
def options(t,split):
 side={c:k for k,pair in enumerate(split) for c in pair};flip={c:pair[1-k] for pair in split for k,c in enumerate(pair)};out=[]
 for p in nc10:
  blocks=[[i for i,k in enumerate(p) if k==b] for b in range(max(p)+1)]
  if any(len({side[t[i]] for i in bl})>1 for bl in blocks):continue
  if any(side[t[i]]==side[t[(i+1)%10]] and p[i]!=p[(i+1)%10] for i in range(10)):continue
  orbit=set()
  for subset in range(1<<len(blocks)):
   word=tuple(flip[c] if subset>>p[i]&1 else c for i,c in enumerate(t));orbit.add(di[m.canonical(word)])
  out.append((p,sorted(orbit)))
 return out
rows=[(2,1,3,2),(2,3,1,2),(3,0,3,1),(3,1,0,1),(1,0,1,3),(1,3,0,3)]
for row in rows:
 t=(0,1,0,2,3,0)+row;j=di[t]
 print('TARGET',row,'id',j,flush=True)
 for si,split in enumerate(m.SPLITS):
  opts=options(t,split);surv=[(p,orb) for p,orb in opts if not set(orb)&bad]
  print(' split',si,'opts',len(opts),'survive',len(surv),'parts',[p for p,orb in surv],flush=True)
