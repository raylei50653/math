"""Exploratory broadening of T1, fixed immutable repository baseline.
Own reconstruction from the published source contract. Support-only probe;
not a full-fibre source-exclusion certificate.
"""
import json, time, itertools
from collections import Counter
from pathlib import Path
BASE = '77fbd5da7ba273f0af7c75175dc08376d2282f46'
BROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
QUERIES = (
 ('c15-933',(0,1,2,0,0),933),('c18-933',(0,2,1,0,0),933),
 ('c04-941',(0,0,1,0,2),941),('c07-941',(0,0,2,0,1),941),
 ('c15-941',(0,1,2,0,0),941),('c18-941',(0,2,1,0,0),941),
 ('c20-941',(1,0,0,0,2),941),('c30-941',(2,0,0,0,1),941))

def canon(word):
 d={}; out=[]
 for c in word:
  if c not in d: d[c]=len(d)
  out.append(str(d[c]))
 return ''.join(out)

def outer(kind, pair, side, collar):
 """Cut along e,c_a,...,c_(a+4), absorbing the entire variable half into L.
 Fixed half remains the original empty-s terminal (rim5 + center).
 """
 E=set()
 def edge(a,b):
  assert a != b
  E.add(tuple(sorted((a,b))))
 def cycle(vs):
  for a,b in zip(vs,vs[1:]+vs[:1]): edge(a,b)
 B=['b'+str(i) for i in range(5)]
 C=['c'+str(i) for i in range(8)]
 cycle(B); cycle(C)
 orig=['a0']
 for i in range(1,5):
  orig += ['y%d_%d'%(i,j) for j in range(1,collar[i]+1)]+['a'+str(i)]
 orig += ['y0_'+str(j) for j in range(1,collar[0]+1)]
 assert len(orig)==8
 image=dict(zip(orig,C))
 for i in range(5):
  edge(B[i],image['a'+str(i)]); edge(B[(i+1)%5],image['a'+str(i)])
  for j in range(1,collar[i]+1): edge(B[i],image['y%d_%d'%(i,j)])
 ends=['x'] if kind=='PINCH' else ['x','y']
 for x in ends:
  edge(x,C[pair]);edge(x,C[(pair+4)%8])
 if kind=='BRIDGE': edge('x','y')
 a=(pair+4*side)%8; f=(a+4)%8
 ep=ends[side] if kind=='BRIDGE' else 'x'
 fp=ends[1-side] if kind=='BRIDGE' else 'x'
 T=['t'+str((f+i)%8) for i in range(4)]
 for i,t in enumerate(T):
  edge(t,C[(f+i)%8]);edge(t,C[(f+i+1)%8])
 ring=[fp]+T; cycle(ring)
 for t in ring: edge('zF',t)
 D=[ep]+[C[(a+i)%8] for i in range(5)]
 cycle(D)
 V=B+C+T+ends+['zF']
 return V,sorted(E),D

def colouring(V,E,D,beta):
 index={v:i for i,v in enumerate(V)}; n=len(V)
 adj=[[] for _ in V]
 for a,b in E:
  a,b=index[a],index[b];adj[a].append(b);adj[b].append(a)
 cols=[-1]*n; dom=[15]*n
 for i,c in enumerate(map(int,beta)):cols[i]=c;dom[i]=0
 for v in range(5):
  for u in adj[v]:
   if cols[u]>=0: assert cols[u]!=cols[v]
   else:dom[u]&=~(1<<cols[v])
 di=[index[d] for d in D]; support=set(); counts=Counter()
 free=set(range(5,n))
 def visit():
  if not free:
   row=tuple(cols[i] for i in di)
   counts[row]+=1
   support.add(canon(row)); return
  v=min(free,key=lambda u:(dom[u].bit_count(),-len(adj[u]),u))
  opts=dom[v]
  if not opts:return
  free.remove(v)
  while opts:
   bit=opts&-opts;opts-=bit;cols[v]=bit.bit_length()-1
   changed=[];ok=True
   for u in adj[v]:
    if u in free and dom[u]&bit:
     changed.append((u,dom[u]));dom[u]^=bit
     if not dom[u]:ok=False
   if ok:visit()
   for u,d in changed:dom[u]=d
  cols[v]=-1;free.add(v)
 visit()
 return support,counts

def masks_for(V,E,D):
 masks={}; literal=[]
 for i,beta in enumerate(BROWS):
  support,counts=colouring(V,E,D,beta)
  literal.append({''.join(map(str,g)):v for g,v in counts.items()})
  for q in support:masks[q]=masks.get(q,0)|(1<<i)
 return masks,literal

def safe_result(masks,tau):
 safe={q:m for q,m in masks.items() if m & ~tau==0}
 possible=0
 for m in safe.values():possible|=m
 return {'safe':safe,'possible':possible,'missing':tau & ~possible,'excluded':possible!=tau}

def run():
 records=[]; start=time.monotonic()
 for kind in ('PINCH','BRIDGE'):
  for pair in range(4):
   for side in range(2):
    cache={}
    for name,collar,tau in QUERIES:
     if collar not in cache:
      V,E,D=outer(kind,pair,side,collar)
      masks,literal=masks_for(V,E,D)
      cache[collar]=(V,E,D,masks,literal)
     V,E,D,masks,literal=cache[collar]
     r={'query':name,'kind':kind,'pair':pair,'side':side,'collar':collar,
        'target':tau,'vertices':V,'edges':E,'interface':D,'masks':masks,
        'literal_fibre_counts_sparse':literal,**safe_result(masks,tau)}
     records.append(r)
    print(kind,pair,side,'excluded',sum(r['excluded'] for r in records),'of',len(records),'time',round(time.monotonic()-start,2),flush=True)
 Path(__file__).with_name('outer_cut_results.json').write_text(json.dumps({'baseline':BASE,'scope':'outer-cut one fixed W5 terminal, arbitrary other half relation','records':records},indent=2))
 print('SUMMARY',Counter((r['kind'],r['excluded']) for r in records),flush=True)
if __name__=='__main__': run()
