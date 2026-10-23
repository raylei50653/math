import sys
sys.dont_write_bytecode=True
import importlib.util,itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[2]
spec=importlib.util.spec_from_file_location('old',ROOT/'audits/2026-10-23-three-mask-methods-cb8f859/933/check.py');o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
src=json.loads((ROOT/o.SOURCE).read_text());ts=[tuple(t) for t in src['tuples']];index={t:i for i,t in enumerate(ts)}
ps=[p for p in o.partitions() if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in itertools.combinations(range(8),4))]
cols=[[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in ts] for p in ps];A=list(map(list,zip(*(c for c in cols if any(c)))))
live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933));B=o.mm(A,o.kernel([r for j,r in enumerate(A) if j not in live],91))
E=('a','n','R','L','q','c','x','y');H=('a','n','R','L','q','b');rim=[(E[i],E[(i+1)%8]) for i in range(8)];base=rim+[('a','b'),('b','c'),('b','q')]
def triang(v):
 if len(v)<=3:return [set()]
 out=[]
 for j in range(1,len(v)-1):
  for a in triang(v[:j+1]):
   for b in triang(v[j:]):
    es=a|b
    for edge in ((v[0],v[j]),(v[j],v[-1])):
     if abs(v.index(edge[0])-v.index(edge[1]))>1:es.add(tuple(sorted(edge)))
    out.append(es)
 return out
trs=sorted({tuple(sorted(t)) for t in triang(H)});print(len(trs))
old=json.loads((ROOT/o.OLD).read_text());control=next(w for w in old['maximal_support_witnesses'] if w['source_mask']==933);z=control['exterior_counts']
for j,ds in enumerate(trs):
 M=[[0]*274 for _ in range(10)]
 for r,word in enumerate(o.ROWS):
  x,y,a,b,c=map(int,word)
  for n,R,L,q in itertools.product(range(4),repeat=4):
   colors=dict(zip(E,(a,n,R,L,q,c,x,y)),b=b)
   if all(colors[u]!=colors[v] for u,v in base+list(ds)):
    M[r][index[o.canonical(tuple(colors[v] for v in E))]]+=1
 S=o.mm(M,B);cs=o.mv(M,z)
 print(j,ds,'zero', [o.ROWS[i] for i,r in enumerate(S) if not any(r)],'control',cs,'mask',sum(1<<i for i,c in enumerate(cs) if c),'alpha terms',[i for i,c in enumerate(M[9]) if c and any(B[i])])
 print('raw-alpha-in-reject', {o.ROWS[i]:all(not c or not any(B[k]) or M[i][k] for k,c in enumerate(M[9])) for i in (1,4,6)})
 for absent in ((6,),(4,8),(2,6),(1,4,6)):
  initial=[k for k in range(274) if any(M[i][k] for i in absent)]
  S,steps,zeros=o.close_zeros(B,initial)
  red=o.mm(M,S) if S else [[] for _ in o.ROWS]
  orig=o.mm(o.local_relations(ts)[0]['G'],S) if S else [[] for _ in o.ROWS]
  print('absent',absent,'dim',len(S[0]) if S else 0,'alpha-zero',not any(red[9]),'original-933-rows-killed',[o.ROWS[i] for i,r in enumerate(orig) if (933>>i&1) and not any(r)])
 if j in (0,1):
  spec2=importlib.util.spec_from_file_location('r2',ROOT/'audits/2026-10-23-three-mask-round2-cb8f859/933/check.py');r2=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(r2)
  initial=[k for k in range(274) if any(M[i][k] for i in (1,4,6))];S,steps,zeros=o.close_zeros(B,initial);zeros=set(zeros)|{k for k,r in enumerate(S) if not any(r)}
  for target in (30,131,257,259):
   for split in (((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))):
    r2.SPLIT=split;opts=r2.all_actual_component_options(ts[target],ps,index)
    surv=[op for op in opts if not set(op['orbit'])&zeros]
    print('target',target,'word',ts[target],'split',split,'opts',len(opts),'surv',len(surv),'hits',sorted({min(set(op['orbit'])&zeros) for op in opts if set(op['orbit'])&zeros}))
