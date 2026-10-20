#!/usr/bin/env python3
"""Independent Q-edge lifts and list/set replay of B's six main comparisons."""
import gzip,hashlib,importlib.util,itertools,json,math
from pathlib import Path
D=Path(__file__).resolve().parent;B=D.parent/'B';F=D.parent/'frozen'
path=F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
s=importlib.util.spec_from_file_location('review_model',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
c=json.loads(gzip.decompress((B/'certificate.json.gz').read_bytes()))
states=[t for t in m.growth(10,four=True) if m.proper(t)];assert [list(t) for t in states]==c['core_states']
Q=[[[0]*len(states) for _ in range(10)] for _ in range(2)]
edges=[('c','q'),('c','u'),('c','s'),('c','x'),('c','b'),('b','a'),('b','q'),
 ('x','y'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),
 ('r','s'),('r','v'),('r','w'),('r','t')]
for i,t in enumerate(states):
 f=dict(zip(('a','n','R','L','q','u','s','v','w','t'),t))
 for cc,bb in itertools.product(range(4),repeat=2):
  if bb!=f['n']:continue
  for xx,yy,rr in itertools.product(range(4),repeat=3):
   z=dict(f,c=cc,b=bb,x=xx,y=yy,r=rr)
   if any(z[u]==z[v] for u,v in edges):continue
   j=m.ROWS.index(''.join(map(str,m.canonical((xx,yy,f['a'],bb,cc)))))
   if f['R']==f['q']:Q[0][j][i]+=1
   if bb==f['L']:Q[1][j][i]+=1
 fac=math.factorial(4-len(set(t)))
 for M in Q:
  for r in M:assert r[i]%fac==0;r[i]//=fac
assert Q==c['Q_matrices']
K=m.kempe(10,states);G=c['original_matrix'];Hs=c['H_matrices']
def support(M,live):return sum(1<<r for r,row in enumerate(M) if any(row[i] for i in live))
catalogue=sorted(map(int,json.loads((F/'artifacts/c5_cells/cells.json').read_text())['cells']))
initial=[i for i in range(len(states)) if all(not G[j][i] for j in (1,4,6))]
live,_=m.close(K,initial);assert live==c['general_c5']['live']
summary=[]
for branch in c['H4_zero_branches']:
 zb=branch['zero_bits'];supports=[1022 if zb>>j&1 else 1023 for j in range(5)]
 seed=[i for i in live if all(not Hs[j][0][i] for j in range(5) if zb>>j&1)]
 ls,_=m.close(K,seed)
 for qi,N in enumerate(Q):
  zz=[i for i in ls if not N[9][i]];dead,rounds=m.close(K,zz)
  got=branch['acceptance_zero'][qi]
  assert dead==got['live'] and rounds==got['rounds'] and support(G,dead)==429
  choices=[]
  assert [r['hypothesis'] for r in branch['Q_catalogue_comparisons'][qi]]==catalogue
  for mask,expected in zip(catalogue,branch['Q_catalogue_comparisons'][qi]):
   zz=[i for i in ls if all(not N[j][i] for j in range(10) if not(mask>>j&1))]
   surv,rs=m.close(K,zz)
   assert surv==expected['live'] and rs==expected['rounds']
   ok=support(G,surv)==941 and all(mm&~support(H,surv)==0 for mm,H in zip(supports,Hs)) and mask&~support(N,surv)==0
   assert ok==expected['not_excluded']
   if ok:choices.append(mask)
  assert choices==[1021];summary.append({'zero_bits':zb,'Q':qi+1,'only_support':1021,'accept_zero_source_upper':429})
print(json.dumps({'pass':True,'B_certificate_sha256':hashlib.sha256((B/'certificate.json.gz').read_bytes()).hexdigest(),'independent_edges':edges,'full_Q_matrix_match':True,'independent_list_set_comparisons':len(summary)*132,'main_result':summary},sort_keys=True))
