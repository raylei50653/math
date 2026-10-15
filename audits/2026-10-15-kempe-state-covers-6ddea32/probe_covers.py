from pathlib import Path
import json,itertools,time
H=Path(__file__).resolve().parent
exec((H/'probe_voltage.py').read_text().split("print('edge orbit vars'")[0])
def canon(s):
 d={};r=''.join('ABCD'[d.setdefault(c,len(d))] for c in s)
 for c in 'ABCD':d.setdefault(c,len(d))
 return r,tuple('ABCD'.index(c) for c,n in sorted(d.items(),key=lambda x:x[1]))
R=sorted({canon(s['literal_row'])[0] for s in S});frame={s['id']:(R.index(canon(s['literal_row'])[0]),canon(s['literal_row'])[1]) for s in S}
def add(bas,v):
 while v:
  p=v.bit_length()-1
  if p in bas:v^=bas[p]
  else:bas[p]=v;return True
 return False
hrows=[]
for s in S:
 if s['literal_row']!=canon(s['literal_row'])[0]:continue
 for j,part in enumerate(s['pairings']):
  offset=0
  for blocks in part['terminal_parts']:
   mask=0;current=s['id']
   for bit in range(offset,offset+len(blocks)):
    mask^=1<<index[edges[current,j,bit]];current=byid[current]['pairings'][j]['cube_targets_by_bitmask'][1<<bit]
   offset+=len(blocks);hrows.append(mask)
B={}
for mask in sorted(rows|set(hrows)):add(B,mask)
null=[]
for f in range(len(keys)):
 if f in B:continue
 v=1<<f
 for p in sorted(B):
  if (B[p]&v).bit_count()%2:v^=1<<p
 null.append(v)
G={}
for r in R:
 mask=sum(1<<i for i,(a,b) in enumerate(keys) if (canon(a)[0]==r)!=(canon(b)[0]==r));add(G,mask)
Q=[];span=dict(G)
for v in null:
 if add(span,v):Q.append(v)
print('quotientdim',len(Q),flush=True)

def run(voltage):
 cons={}
 for s in S:
  for e in range(2):
   u0,p=frame[s['id']];u=2*u0+e
   for j,part in enumerate(s['pairings']):
    bit=0
    for pair,blocks in zip(part['pairing'],part['terminal_parts']):
     for block in blocks:
      v0,q=frame[part['cube_targets_by_bitmask'][1<<bit]];v=2*v0+(e^((voltage>>index[edges[s['id'],j,bit]])&1));bit+=1
      a={(i,k) for i in range(4) for k in range(4) if p[i]==q[k] or p[i] in pair and q[k] in pair}
      if u>v:key=(v,u);a={(k,i) for i,k in a}
      else:key=(u,v)
      cons.setdefault(key,set(itertools.product(range(4),repeat=2))).intersection_update(a)
 sols=[];nodes=0;start=time.time()
 def search(ds):
  nonlocal nodes
  nodes+=1
  if nodes>100000 or time.time()-start>30:raise RuntimeError('limit')
  change=True
  while change:
   change=False
   for (u,v),a in cons.items():
    nu={c for c in ds[u] if ((c,c) in a if u==v else any((c,d) in a for d in ds[v]))};nv={d for d in ds[v] if ((d,d) in a if u==v else any((c,d) in a for c in ds[u]))}
    if not nu or not nv:return
    if nu!=ds[u]:ds[u]=nu;change=True
    if nv!=ds[v]:ds[v]=nv;change=True
  todo=[i for i,d in enumerate(ds) if len(d)>1]
  if not todo:sols.append([next(iter(d)) for d in ds]);return
  i=min(todo,key=lambda i:len(ds[i]))
  for a in sorted(ds[i]):
   child=[set(d) for d in ds];child[i]={a};search(child)
 search([set(range(4)) for _ in range(36)])
 F=[{(sid,e):p[f[2*i+e]] for sid,(i,p) in frame.items() for e in range(2)} for f in sols]
 E=[(i,j) for i,j in itertools.combinations(range(len(F)),2) if all(F[i][sid,e]!=F[j][sid,e] for sid in frame for e in range(2))]
 pins=[next(i for i,f in enumerate(F) if all(f[s['id'],e]=='ABCD'.index(s['literal_row'][v]) for s in S for e in range(2))) for v in range(7)];reach={pins[4]};change=True
 while change:
  old=set(reach)
  for a,b in E:
   if F[a][0,0] in(2,3) and F[b][0,0] in(2,3):
    if a in reach:reach.add(b)
    if b in reach:reach.add(a)
  change=old!=reach
 globals()['LAST']=(sols,F,E,pins)
 return {'voltage':voltage,'nodes':nodes,'functions':len(F),'edges':len(E),'pins':pins,'reached':sorted(reach),'q_reached':pins[6] in reach,'seconds':time.time()-start}
for v in [0,Q[0],Q[1]]:
 result=run(v);print(result,flush=True)
(H/'probe-covers-basis.json').write_text(json.dumps({'quotient':Q,'gauge':G}))
