import sys
sys.dont_write_bytecode=True
import importlib.util,itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2];spec=importlib.util.spec_from_file_location('r4',ROOT/'audits/2026-10-23-three-mask-round4-cb8f859/933/check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
src=json.loads((ROOT/m.SRC).read_text());E=[tuple(t) for t in src['tuples']];ei={t:i for i,t in enumerate(E)};live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933));D=list(m.properwords(10));di={t:i for i,t in enumerate(D)};bad={j for j,t in enumerate(D) if any(ei[m.canonical(e)] not in live for r,x,y,e in m.complete_cap(t))};zeroC={640,654,683,685};zeros=bad|zeroC
four=list(itertools.combinations(range(10),4));nc=[p for p in m.partitions(10) if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in four)]
for row in ('01012','01202'):
 A,s,v,w,t=map(int,row);targets=set()
 for n,L,q in itertools.product(range(4),repeat=3):
  d=(A,n,A,L,q,A,s,v,w,t)
  if all(d[i]!=d[(i+1)%10] for i in range(10)):
   did=di[m.canonical(d)]
   if did not in bad:targets.add(did)
 print('ROW',row,'targets',sorted(targets),flush=True)
 for j in sorted(targets):
  results=[]
  for split in (((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))):
   m.SPLIT=split;opts=m.options(D[j],nc);surv=[o for o in opts if not any(di[m.canonical(word)] in zeros for _,word in o['complete_literal_subset_lifts'])];results.append((len(opts),len(surv)))
  print(j,''.join(map(str,D[j])),results,flush=True)
