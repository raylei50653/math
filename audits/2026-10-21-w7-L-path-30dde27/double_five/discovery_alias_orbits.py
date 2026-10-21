import importlib.util,gzip,json,time
from itertools import product
from collections import Counter,defaultdict
from functools import lru_cache

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
collar=mod('audits/2026-10-21-w7-profile0-13e51db/check.py','collar');cap=mod('audits/2026-10-21-w7-k1-mixed-30dde27/transport/check.py','cap')
P=cap.P;rim=cap.RIM;F=['a','z1','z2','z3','z4','V','U','HL_0','q','c','s','v','w','t'];ER=['a','z1','z2','z3','z4','z5','HL_0','q','c','s','v','w','t']
b='audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/';c=json.load(gzip.open(b+'caps.json.gz'));o=json.load(gzip.open(b+'orbits.json.gz'));index={tuple(t):i for i,t in enumerate(c['states'])};live=set(o['live']);res=json.load(gzip.open('audits/2026-10-21-w7-k1-mixed-30dde27/full-exterior-v3.json.gz'))['L_complete_residual']
def norm(groups):return sorted(sorted(row)for row in groups)
def allparts(n,t=(0,),m=1):
 if n==0:yield ();return
 if len(t)==n:yield t;return
 for x in range(m+1):yield from allparts(n,t+(x,),max(m,x+1))
start=time.time()
for target,uname,vname in [(44459,'U','w'),(44459,'v','V'),(44459,'v','w'),(44466,'w','V')]:
 word=(0,3,0,3,0,1,0,1,3,1,2,0,1,2)if target==44459 else(0,3,0,3,0,1,0,1,3,1,2,1,0,2)
 names=[uname if v=='U'else vname if v=='V'else v for v in F]
 _,g=collar.collar(0,[0,0,0,0,0,1],True);g={v:adj-{'p','h','R'}for v,adj in g.items()if v not in{'p','h','R'}}
 for i,a in enumerate(rim):bb=rim[(i+1)%13];g.setdefault(a,set()).add(bb);g.setdefault(bb,set()).add(a)
 rep={'U':uname,'V':vname}
 for a,bb in [('HL_0','U'),('U','V'),('V','z4'),*[( 'K',z)for z in ['HL_0','U','V','z4','z5']]]:
  a=rep.get(a,a);bb=rep.get(bb,bb);g.setdefault(a,set()).add(bb);g.setdefault(bb,set()).add(a)
 inner=P+['z5','K']
 @lru_cache(None)
 def kernel(eword):
  fixed=dict(zip(names,eword));out=[]
  def go(assign):
   rem=set(inner)-assign.keys()
   if not rem:
    full=fixed|assign;sid=index[cap.canonical(tuple(full[v]for v in rim))];out.append((tuple(full[v]for v in inner),sid));return
   allc=fixed|assign;ds={v:set(range(4))-{allc[w]for w in g[v]if w in allc}for v in rem};v=min(rem,key=lambda x:(len(ds[x]),x))
   for co in sorted(ds[v]):go(assign|{v:co})
  go({});return out
 for mate in [1,2,3]:
  pairs=[(0,mate),tuple(x for x in range(4)if x not in(0,mate))];side=[0 if x in pairs[0]else 1 for x in word];par={v:v for v in names}
  def find(v):
   while par[v]!=v:v=par[v]
   return v
  def union(a,bb):par[find(a)]=find(bb)
  for i,a in enumerate(names):
   j=(i+1)%14
   if side[i]==side[j]:union(a,names[j])
  base=[sorted({find(names[i])for i in range(14)if side[i]==p})for p in [0,1]]
  rr=next(r for r in res if r['E_state']==(560 if target==44459 else 572)and r['split_containing_0']==[0,mate]);expected=[norm(r['component_blocks'])for r in rr['complete_surviving_columns']]
  total=0;sourcegood=0;surv=0
  for p0,p1 in product(allparts(len(base[0])),allparts(len(base[1]))):
   parts={root:(p0[k]if pp==0 else max(p0)+1+p1[k])for pp,roots in enumerate(base)for k,root in enumerate(roots)};part=tuple(parts[find(v)]for v in names);canon={};part=tuple(canon.setdefault(x,len(canon))for x in part);total+=1
   # Exact reattachment join on this same original F partition.
   allnames=set(names)|{'z5','K'};pp={v:v for v in allnames}
   def ff(v):
    while pp[v]!=v:v=pp[v]
    return v
   def uu(a,bb):pp[ff(a)]=ff(bb)
   for label in set(part):
    group=[names[i]for i,x in enumerate(part)if x==label]
    for v in group[1:]:uu(group[0],v)
   colors=dict(zip(names,word))|{'z5':3,'K':2}
   for a,bb in [('z4','z5'),('z5','HL_0'),*[( 'K',rep.get(z,z))for z in ['HL_0','U','V','z4','z5']]]:
    if any(colors[a]in pair and colors[bb]in pair for pair in pairs):uu(a,bb)
   groups={}
   for v in ER:groups.setdefault(ff(v),[]).append(v)
   if norm(groups.values())not in expected:continue
   sourcegood+=1;bad=False
   for mask in range(1<<(max(part)+1)):
    out=tuple((pairs[side[i]][0]^pairs[side[i]][1]^co)if mask>>part[i]&1 else co for i,co in enumerate(word))
    if any(sid not in live for _,sid in kernel(out)):bad=True;break
   surv+=not bad
  print(target,uname,vname,mate,'initial',total,'sourceE',sourcegood,'survive',surv,'kernels',kernel.cache_info().currsize,'sec',time.time()-start,flush=True)
