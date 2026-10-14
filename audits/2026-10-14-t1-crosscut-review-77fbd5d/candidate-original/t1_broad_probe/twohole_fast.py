"""Bitset replay of exact support constraints; imports shell producer only."""
import json,time,sys,itertools
from pathlib import Path
from collections import Counter
from probe import QUERIES
from kempe_probe import ROWS,OPTIONS
from twohole_probe import shell,matrix,bits,ALL
RID={r:i for i,r in enumerate(ROWS)}
OP=[[[sum(1<<RID[x] for x in o) for _,o in OPTIONS[r,s]] for s in range(3)] for r in ROWS]

def prune_mask(S):
 while True:
  old=S
  for r in bits(S):
   if any(not any(o & ~S==0 for o in opts) for opts in OP[r]):
    S &= ~(1<<r)
  if S==old:return S

def check(M,tau,limit=2000000):
 N=[sum(1<<b for b in range(31) if not M[a][b]&~tau) for a in range(31)]
 domains={ALL}
 for na in N:
  domains|={b & na for b in domains}
  if len(domains)>limit:return {'incomplete':True,'intersections':len(domains)}
 cache={};records=[]
 for bb in sorted(domains):
  aa=sum(1<<i for i,na in enumerate(N) if not bb & ~na)
  if aa not in cache:cache[aa]=prune_mask(aa)
  if bb not in cache:cache[bb]=prune_mask(bb)
  ap,bp=cache[aa],cache[bb]
  possible=0
  for a in bits(ap):
   for b in bits(bp):possible|=M[a][b]
  records.append([aa,bb,ap,bp,possible,tau & ~possible])
  if possible==tau:
   return {'incomplete':False,'excluded':False,'intersections':len(domains),'witness':records[-1],
           'left_support':[ROWS[i] for i in bits(ap)],'right_support':[ROWS[i] for i in bits(bp)]}
 return {'incomplete':False,'excluded':True,'intersections':len(domains),'rectangles':records}

def run(kind,pair):
 start=time.monotonic(); R=[];cache={}
 for name,e,tau in QUERIES:
  if e not in cache:
   V,E,D=shell(kind,pair,e);M,cnt=matrix(V,E,D);cache[e]=(V,E,D,M,cnt)
  V,E,D,M,cnt=cache[e];res=check(M,tau)
  R.append({'kind':kind,'pair':pair,'query':name,'collar':e,'target':tau,'vertices':V,'edges':E,'interfaces':D,
            'matrix':M,'shell_lift_counts':cnt,**res})
  print(kind,pair,name,'excluded',res.get('excluded'),'rectangles',res.get('intersections'),'time',round(time.monotonic()-start,2),flush=True)
 Path(__file__).with_name(f'twohole_{kind}_{pair}.json').write_text(json.dumps({'rows':ROWS,'records':R},separators=(',',':')))
if __name__=='__main__':
 if len(sys.argv)>1: run(sys.argv[1],int(sys.argv[2]))
 else:
  for kind in ('PINCH','BRIDGE'):
   for pair in range(4):run(kind,pair)
