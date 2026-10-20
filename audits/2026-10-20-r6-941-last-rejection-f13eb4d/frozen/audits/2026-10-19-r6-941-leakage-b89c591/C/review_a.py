#!/usr/bin/env python3
"""Independent direct-edge cap replay of A's two new same-source controls."""
import hashlib,itertools,json
from collections import Counter
from pathlib import Path
D=Path(__file__).resolve().parent
A=D.parent/'A'
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
EDGE_RIGHT=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','t'),('r','w'),('r','v'),('r','s'))
EDGE_LEFT=(('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),('p','h'),('p','n'),('h','q'),('h','L'),('h','R'),('h','n'))
def can(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
def generate(n,p=(0,)):
 if len(p)==n:
  if proper(p):yield p
 else:
  for x in range(min(3,max(p)+1)+1):yield from generate(n,p+(x,))
def ok(f,edges):return all(f[a]!=f[b] for a,b in edges)
def mv(m,z):return [sum(x*y for x,y in zip(row,z)) for row in m]
def support(v):return sum(1<<i for i,x in enumerate(v) if x)
eight=list(generate(8));ten=list(generate(10));index={t:i for i,t in enumerate(ten)}
transfer=[]
for e in eight:
 f=dict(zip(('a','n','R','L','q','c','x','y'),e));row=Counter()
 for s,v,w,t,r in itertools.product(range(4),repeat=5):
  g=dict(f,s=s,v=v,w=w,t=t,r=r);core=tuple(g[k] for k in ('a','n','R','L','q','c','s','v','w','t'))
  if proper(core) and ok(g,EDGE_RIGHT):row[index[can(core)]]+=1
 transfer.append(row)
subsets={}
for name,h,n in [('h_equals_a',0,1),('h_equals_b',1,2)]:
 ids=[]
 for R,L,v,w in itertools.product(range(4),repeat=4):
  f={'a':0,'c':0,'q':2,'b':1,'p':3,'h':h,'n':n,'s':1,'t':1,'r':0,'x':2,'y':3,'R':R,'L':L,'v':v,'w':w}
  core=tuple(f[k] for k in ('a','n','R','L','q','c','s','v','w','t'))
  if proper(core) and ok(f,EDGE_LEFT+EDGE_RIGHT):ids.append(index[can(core)])
 subsets[name]=sorted(set(ids))
J=json.loads((D/'joint-fibres.json').read_text());U=json.loads((D/'u319-core.json').read_text())['literal_U_count_matrix']
cert=json.loads((A/'source-positive-certificate.json').read_text());assert cert['source_positive_subset_ids']==subsets
summary=[]
for rec in cert['records']:
 z=rec['core_counts'];e=[sum(n*z[i] for i,n in row.items()) for row in transfer];assert e==rec['exterior_counts']
 projections={name:mv(m,e) for name,m in J['literal_count_matrices'].items()};assert projections==rec['graph_counts']
 u=mv(U,z);assert u==rec['U_counts'] and support(u)==319
 d={name:sum(z[i] for i in ids) for name,ids in subsets.items()};assert d==rec['source_positive_subset_counts'] and all(d.values())
 sectors={name:sum(a*b for a,b in zip(v,e)) for name,v in J['original_alpha_sector_count_rows'].items()}
 assert all(sectors[name]>=2*d[name] for name in sectors)
 assert 2*projections['GB'][6]==sectors['h_equals_a']+sum(e[i] for i in (17,118,179))
 summary.append({'name':rec['name'],'masks':{name:support(v) for name,v in projections.items()},'d':d,'actual_alpha_sectors':sectors})
print(json.dumps({'pass':True,'scope':'independent direct-edge cap transfer, complete U and candidate projections, exact source-positive subsets; planar+component replay separately by A checker',
 'reviewed_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (A/'model.py',A/'check.py',A/'source-positive-certificate.json')},'results':summary},sort_keys=True))
