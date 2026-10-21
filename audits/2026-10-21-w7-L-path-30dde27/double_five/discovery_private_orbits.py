import importlib.util,gzip,json,time
from itertools import product
from collections import Counter
from functools import lru_cache

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
collar=mod('audits/2026-10-21-w7-profile0-13e51db/check.py','collar');cap=mod('audits/2026-10-21-w7-k1-mixed-30dde27/transport/check.py','cap')
P=cap.P;rim=cap.RIM;F=['a','z1','z2','z3','z4','V','U','HL_0','q','c','s','v','w','t']
b='audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/'
c=json.load(gzip.open(b+'caps.json.gz'));o=json.load(gzip.open(b+'orbits.json.gz'));state={tuple(t):i for i,t in enumerate(c['states'])};live=set(o['live'])
_,g=collar.collar(0,[0,0,0,0,0,1],True);g={v:adj-{'p','h','R'}for v,adj in g.items()if v not in{'p','h','R'}}
for i,a in enumerate(rim):bb=rim[(i+1)%13];g.setdefault(a,set()).add(bb);g.setdefault(bb,set()).add(a)
for a,bb in [('HL_0','U'),('U','V'),('V','z4'),*[( 'K',z)for z in ['HL_0','U','V','z4','z5']]]:g.setdefault(a,set()).add(bb);g.setdefault(bb,set()).add(a)
inner=P+['z5','K']
@lru_cache(None)
def kernel(eword):
 fixed=dict(zip(F,eword));out=[]
 def go(assign):
  rem=set(inner)-assign.keys()
  if not rem:
   full=fixed|assign;rr=tuple(full[v]for v in rim);sid=state[cap.canonical(rr)];out.append((tuple(full[v]for v in inner),sid));return
  allc=fixed|assign;ds={v:set(range(4))-{allc[w]for w in g[v]if w in allc}for v in rem};v=min(rem,key=lambda x:(len(ds[x]),x))
  for co in sorted(ds[v]):go(assign|{v:co})
 go({});return out

def parts(side):
 trans=sum(side[i]!=side[(i+1)%len(side)]for i in range(len(side)));want=trans//2+1
 def go(t,stack,ps):
  i=len(t)
  if len(ps)>want:return
  if i==len(side):
   if len(ps)==want and(side[0]!=side[-1]or t[0]==t[-1]):yield t
   return
  if side[i]==side[i-1]:yield from go(t+(t[-1],),stack,ps);return
  for j,x in enumerate(stack):
   if ps[x]==side[i]:yield from go(t+(x,),stack[:j+1],ps)
  if len(ps)<want:yield from go(t+(len(ps),),stack+(len(ps),),ps+(side[i],))
 yield from go((0,),(0,),(side[0],))
start=time.time();summary=[]
for target in [44459,44466]:
 orig=(0,3,0,3,0,1,0,1,3,1,2,0,1,2)if target==44459 else(0,3,0,3,0,1,0,1,3,1,2,1,0,2)
 for mate in [1,2,3]:
  pairs=[(0,mate),tuple(x for x in range(4)if x not in(0,mate))];side=tuple(0 if x in pairs[0]else 1 for x in orig);n=0;surv=[];zero=Counter()
  for part in parts(side):
   n+=1;bad=None;bb=max(part)+1
   for mask in range(1<<bb):
    word=tuple((pairs[side[i]][0]^pairs[side[i]][1]^co)if mask>>part[i]&1 else co for i,co in enumerate(orig))
    rows=kernel(word)
    hit=next(((col,sid)for col,sid in rows if sid not in live),None)
    if hit:bad=(mask,word,hit);zero['oldD']+=1;break
   if bad is None:surv.append(part)
  print(target,mate,'all',n,'survive',len(surv),'cache',kernel.cache_info(),'sec',time.time()-start,flush=True)
  summary.append({'target':target,'mate':mate,'all':n,'survivors':surv})
open('audits/2026-10-21-w7-L-path-30dde27/double_five/discovery-private-orbits.json','w').write(json.dumps(summary,indent=2))
