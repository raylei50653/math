"""Exploratory full PINCH/BRIDGE source test using two fixed C6 interfaces.
Two unknown planar disks are arbitrary. Their common original contact colors
are synchronized by one literal coloring of the shell.
"""
import itertools,json,time
from pathlib import Path
from collections import Counter
from probe import BROWS,QUERIES,canon,colouring
from kempe_probe import ROWS,prune
RID={r:i for i,r in enumerate(ROWS)}
ALL=(1<<len(ROWS))-1

def shell(kind,pair,collar):
 E=set()
 def edge(a,b):
  assert a!=b;E.add(tuple(sorted((a,b))))
 def cyc(L):
  for a,b in zip(L,L[1:]+L[:1]):edge(a,b)
 B=['b'+str(i) for i in range(5)];C=['c'+str(i) for i in range(8)]
 cyc(B);cyc(C)
 old=['a0']
 for i in range(1,5):old+=['y%d_%d'%(i,j) for j in range(1,collar[i]+1)]+['a'+str(i)]
 old+=['y0_'+str(j) for j in range(1,collar[0]+1)]
 image=dict(zip(old,C))
 for i in range(5):
  edge(B[i],image['a'+str(i)]);edge(B[(i+1)%5],image['a'+str(i)])
  for j in range(1,collar[i]+1):edge(B[i],image['y%d_%d'%(i,j)])
 ep=['x'] if kind=='PINCH' else ['x','y']
 for v in ep:
  edge(v,C[pair]);edge(v,C[(pair+4)%8])
 if kind=='BRIDGE':edge('x','y')
 D=[]
 for s in range(2):
  a=(pair+4*s)%8;e=ep[s] if kind=='BRIDGE' else 'x'
  D.append([e]+[C[(a+i)%8] for i in range(5)])
 return B+C+ep,sorted(E),D

def matrix(V,E,D):
 S=V[5:];idx={v:i for i,v in enumerate(S)}
 di=[[idx[v] for v in d] for d in D]
 M=[[0]*len(ROWS) for _ in ROWS];cnt=[]
 for bi,beta in enumerate(BROWS):
  _,literal=colouring(V,E,S,beta)
  for row,n in literal.items():
   a,b=[RID[canon([row[i] for i in js])] for js in di]
   M[a][b]|=1<<bi
  cnt.append(sum(literal.values()))
 return M,cnt

def bits(n):
 while n:
  x=n&-n;n-=x;yield x.bit_length()-1

def check(M,tau,limit=1000000):
 N=[sum(1<<b for b in range(31) if not M[a][b]&~tau) for a in range(31)]
 # Every maximal safe rectangle is (A(B),B), with B an intersection of N(a).
 domains={ALL}
 for na in N:
  domains|={b & na for b in list(domains)}
  if len(domains)>limit:return {'incomplete':True,'intersections':len(domains)}
 records=[]; cache={}
 def kp(mask):
  if mask not in cache:
   S,steps=prune({ROWS[i] for i in bits(mask)})
   cache[mask]=(sum(1<<RID[s] for s in S),steps)
  return cache[mask]
 for bb in sorted(domains):
  aa=sum(1<<i for i,na in enumerate(N) if not bb & ~na)
  # Formal closure of all common neighbours must return bb (including empties).
  test=ALL
  for i in bits(aa):test &= N[i]
  assert test==bb
  ap,asteps=kp(aa);bp,bsteps=kp(bb)
  possible=0
  for a in bits(ap):
   for b in bits(bp):possible|=M[a][b]
  records.append({'A':aa,'B':bb,'A_pruned':ap,'B_pruned':bp,'possible':possible,'missing':tau & ~possible})
  if possible==tau:
   return {'incomplete':False,'excluded':False,'intersections':len(domains),'witness':records[-1],
           'left_support':[ROWS[i] for i in bits(ap)],'right_support':[ROWS[i] for i in bits(bp)]}
 return {'incomplete':False,'excluded':True,'intersections':len(domains),'rectangles':records,
         'pruning':{str(k):{'final':v[0],'steps':v[1]} for k,v in cache.items()}}

def run():
 R=[];start=time.monotonic()
 for kind in ('PINCH','BRIDGE'):
  for pair in range(4):
   cache={}
   for name,e,tau in QUERIES:
    if e not in cache:
     V,E,D=shell(kind,pair,e);M,cnt=matrix(V,E,D);cache[e]=(V,E,D,M,cnt)
    V,E,D,M,cnt=cache[e];res=check(M,tau)
    R.append({'kind':kind,'pair':pair,'query':name,'target':tau,'vertices':V,'edges':E,'interfaces':D,
              'matrix':M,'shell_lift_counts':cnt,**res})
    print(kind,pair,name,'excluded',res.get('excluded'),'rectangles',res.get('intersections'),'elapsed',round(time.monotonic()-start,2),flush=True)
 Path(__file__).with_name('twohole_results.json').write_text(json.dumps({'rows':ROWS,'records':R},indent=2))
 print('SUMMARY',Counter((r['kind'],r.get('excluded')) for r in R))
if __name__=='__main__':run()
