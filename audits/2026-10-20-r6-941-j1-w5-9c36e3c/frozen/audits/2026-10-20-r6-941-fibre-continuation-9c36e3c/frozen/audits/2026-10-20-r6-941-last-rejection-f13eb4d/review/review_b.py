"""Independent quotient-graph full cap enumeration for all twenty B candidates."""
import gzip,itertools,json
from pathlib import Path
from math import factorial
D=Path(__file__).resolve().parent.parent
C=json.loads(gzip.decompress((D/'B/certificate.json.gz').read_bytes()))
pins=('a','n','R','L','q','u','s','v','w','t');caps=('b','x','y','r')
vertices=pins+caps
right=(('x','y'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','t'),('r','w'),('r','v'),('r','s'))
base=[(pins[i],pins[(i+1)%10]) for i in range(10)]+[('a','b'),('b','q')]+list(right)
rows=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
def canon(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
for j,op in enumerate(C['operations']):
 parent={v:v for v in vertices}
 def root(x):
  while parent[x]!=x:x=parent[x]
  return x
 for a,b in op['left_equalities']:parent[root(a)]=root(b)
 edges={tuple(sorted((root(a),root(b)))) for a,b in base+op['H_added_edges']+op['left_added_edges']}
 assert all(a!=b for a,b in edges)
 adj={root(v):set() for v in vertices}
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 matrix=[[0]*2461 for _ in rows]
 for i,t in enumerate(C['core_states']):
  fixed={};good=True
  for v,col in zip(pins,t):
   r=root(v)
   if r in fixed and fixed[r]!=col:good=False;break
   fixed[r]=col
  if not good or any(a in fixed and b in fixed and fixed[a]==fixed[b] for a,b in edges):continue
  missing=sorted(set(adj)-fixed.keys())
  def visit(k):
   if k==len(missing):
    word=''.join(map(str,canon(tuple(fixed[root(v)] for v in op['boundary']))))
    matrix[rows.index(word)][i]+=1;return
   v=missing[k];used={fixed[w] for w in adj[v] if w in fixed}
   for col in range(4):
    if col not in used:fixed[v]=col;visit(k+1)
   fixed.pop(v,None)
  visit(0)
  stabilizer=factorial(4-len(set(t)))
  for row in matrix:assert row[i]%stabilizer==0;row[i]//=stabilizer
 assert matrix==C['matrices'][j],op['name']
print(json.dumps({'pass':True,'independent_quotient_graphs':20,'core_rows':2461,'complete_ten_fibres':True,'source_realized':False},sort_keys=True))
