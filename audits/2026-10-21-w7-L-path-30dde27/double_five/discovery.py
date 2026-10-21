import importlib.util,json
from itertools import product
from collections import defaultdict

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
collar=mod('audits/2026-10-21-w7-profile0-13e51db/check.py','collar');caps=mod('audits/2026-10-21-w7-k1-mixed-30dde27/transport/check.py','caps')
P=caps.P;rim=caps.RIM
for target in [44459,44466]:
 z0='v'if target==44459 else'w';tip='w'if target==44459 else'v'
 for uname,vname in product(['U',z0],['V','c',tip]):
  if uname==z0 and vname=='c':continue
  _,g=collar.collar(0,[0,0,0,0,0,1],True);g={v:adj-{'p','h','R'}for v,adj in g.items()if v not in{'p','h','R'}}
  for i,a in enumerate(rim):b=rim[(i+1)%13];g.setdefault(a,set()).add(b);g.setdefault(b,set()).add(a)
  replace={'U':uname,'V':vname}
  for a,b in [('Y','U'),('U','V'),('V','z4'),*[( 'K',z)for z in ['Y','U','V','z4','z5']]]:
   a=replace.get(a,a);b=replace.get(b,b);a='HL_0'if a=='Y'else a;b='HL_0'if b=='Y'else b
   g.setdefault(a,set()).add(b);g.setdefault(b,set()).add(a)
  orig=dict(zip(rim,[0,1,2,1,2,1,2,3,1,2,0,1,2]if target==44459 else[0,1,2,1,2,1,2,3,1,2,1,0,2]))|{'z1':3,'z2':0,'z3':3,'z4':0,'z5':3,'HL_0':1,uname:0,vname:1,'K':2}
  assert all(orig[a]!=orig[b]for a in g for b in g[a])
  inner=P+['z5','K'];fixed={v:co for v,co in orig.items()if v not in inner};lifts=[];badrows=[]
  def go(assign):
   rem=set(inner)-assign.keys()
   if not rem:
    full=fixed|assign;cap=caps.full_caps(tuple(full[v]for v in rim));lifts.append((dict(assign),cap['all_bad_full_cap_lifts']))
    if cap['all_bad_full_cap_lifts']:badrows.append(lifts[-1])
    return
   domains={v:set(range(4))-{(fixed|assign)[w]for w in g[v]if w in fixed or w in assign}for v in rem};v=min(rem,key=lambda x:(len(domains[x]),x))
   for co in sorted(domains[v]):go(assign|{v:co})
  go({})
  print(target,uname,vname,'lifts',len(lifts),'bad',len(badrows),'sample',badrows[:1])
