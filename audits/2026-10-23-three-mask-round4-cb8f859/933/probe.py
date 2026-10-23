import sys
sys.dont_write_bytecode=True
import importlib.util,itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
s=importlib.util.spec_from_file_location('r3',ROOT/'audits/2026-10-23-three-mask-round3-cb8f859/933/check.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
src=json.loads((ROOT/m.SOURCE).read_text());ts=[tuple(t) for t in src['tuples']];index={t:i for i,t in enumerate(ts)}
nc=[p for p in m.partitions() if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in itertools.combinations(range(8),4))]
cols=[[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in ts] for p in nc];A=list(map(list,zip(*(c for c in cols if any(c)))))
live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933));B=m.mm(A,m.kernel([r for j,r in enumerate(A) if j not in live],91));zeros={j for j,r in enumerate(B) if not any(r)}
for j in (73,76,196,198,257,259):
 print('TARGET',j,ts[j])
 for si,split in enumerate(m.SPLITS):
  opts=m.component_options(ts[j],nc,index,split,True);surv=[o for o in opts if not set(o['orbit'])&zeros]
  print('split',si,'options',len(opts),'surv',len(surv))
  for o in surv:print(' partition',o['partition'],'orbit',o['orbit'])
cap_edges=[('x','y'),('x','c'),('x','s'),('x','r'),('y','a'),('y','t'),('y','r')]+[('r',v) for v in ('s','v','w','t')]+[('s','v'),('v','w'),('w','t'),('s','c'),('t','a')]
rows=set();original_lifts={}
for name,x,y in [('U',1,3),('V',3,1)]:
 opts=[]
 for s,v,w,t,r in itertools.product(range(4),repeat=5):
  colors={'a':0,'n':1,'R':0,'L':2,'q':3,'c':0,'s':s,'v':v,'w':w,'t':t,'x':x,'y':y,'r':r}
  if all(colors[a]!=colors[b] for a,b in cap_edges):opts.append((s,v,w,t,r));rows.add((s,v,w,t))
 print(name,'raw full lifts',len(opts),'Drows',len({o[:4] for o in opts}));original_lifts[name]=opts
Drows=[]
for s,v,w,t in sorted(rows):
 lifts=[]
 for x,y,r in itertools.product(range(4),repeat=3):
  colors={'a':0,'n':1,'R':0,'L':2,'q':3,'c':0,'s':s,'v':v,'w':w,'t':t,'x':x,'y':y,'r':r}
  if all(colors[a]!=colors[b] for a,b in cap_edges):
   eid=index[m.canonical(tuple(colors[k] for k in m.PIN))];lifts.append((x,y,r,eid,eid in zeros))
 Drows.append({'svwt':[s,v,w,t],'lifts':lifts,'forcedzero':any(l[-1] for l in lifts)})
 print('D',s,v,w,t,'lifts',lifts,'zero',any(l[-1] for l in lifts))
print('all rows',len(Drows),'survive',sum(not d['forcedzero'] for d in Drows))
with (P/'D-probe.json').open('x') as f:json.dump(Drows,f,indent=2)
