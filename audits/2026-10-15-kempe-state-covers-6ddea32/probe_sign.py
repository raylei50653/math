from pathlib import Path
import json,itertools,time
H=Path(__file__).resolve().parent
S=[s for s in json.load(open(H/'frozen/audits/2026-10-15-kempe-compatibility-6ddea32/certificate.json'))['states'] if s['layer']==0]
def frame(s):
 order=''.join(dict.fromkeys(s));order+=''.join(c for c in 'ABCD' if c not in order);p=tuple('ABCD'.index(c) for c in order);return ''.join('ABCD'[order.index(c)] for c in s),p,sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
R=sorted({frame(s['literal_row'])[0] for s in S});D={(s['id'],e):(2*R.index(frame(s['literal_row'])[0])+(e^frame(s['literal_row'])[2]),frame(s['literal_row'])[1]) for s in S for e in range(2)}
cons={}
for s in S:
 for e in range(2):
  u,p=D[s['id'],e]
  for part in s['pairings']:
   bit=0
   for pair,blocks in zip(part['pairing'],part['terminal_parts']):
    for block in blocks:
     v,q=D[part['cube_targets_by_bitmask'][1<<bit],e];bit+=1
     a={(i,j) for i in range(4) for j in range(4) if p[i]==q[j] or p[i] in pair and q[j] in pair}
     if u>v:key=(v,u);a={(j,i) for i,j in a}
     else:key=(u,v)
     cons.setdefault(key,set(itertools.product(range(4),repeat=2))).intersection_update(a)
sol=[];nodes=0
def search(ds):
 global nodes
 nodes+=1
 if nodes>1000000:raise RuntimeError('node budget')
 change=True
 while change:
  change=False
  for (u,v),a in cons.items():
   nu={c for c in ds[u] if ((c,c) in a if u==v else any((c,d) in a for d in ds[v]))};nv={d for d in ds[v] if ((d,d) in a if u==v else any((c,d) in a for c in ds[u]))}
   if not nu or not nv:return
   if nu!=ds[u]:ds[u]=nu;change=True
   if nv!=ds[v]:ds[v]=nv;change=True
 todo=[i for i,d in enumerate(ds) if len(d)>1]
 if not todo:sol.append([next(iter(d)) for d in ds]);return
 i=min(todo,key=lambda i:len(ds[i]))
 for a in sorted(ds[i]):
  child=[set(d) for d in ds];child[i]={a};search(child)
t=time.time();search([set(range(4)) for i in range(36)]);print('nodes',nodes,'sol',len(sol),'sec',time.time()-t,flush=True)
F=[{x:p[f[i]] for x,(i,p) in D.items()} for f in sol];E=[(i,j) for i,j in itertools.combinations(range(len(F)),2) if all(F[i][x]!=F[j][x] for x in D)];pins=[next(i for i,f in enumerate(F) if all(f[s['id'],e]=='ABCD'.index(s['literal_row'][v]) for s in S for e in range(2))) for v in range(7)];reach={pins[4]};change=True
while change:
 old=set(reach)
 for a,b in E:
  if F[a][0,0] in(2,3) and F[b][0,0] in(2,3):
   if a in reach:reach.add(b)
   if b in reach:reach.add(a)
 change=old!=reach
print('edges',len(E),'pins',pins,'reach',sorted(reach),'q',pins[6]);(H/'probe-sign.json').write_text(json.dumps({'variables':36,'nodes':nodes,'functions':sol,'edges':E,'pins':pins,'reach':sorted(reach)}))
