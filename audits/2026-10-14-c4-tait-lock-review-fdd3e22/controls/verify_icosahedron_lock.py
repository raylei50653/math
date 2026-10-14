from itertools import combinations
from collections import defaultdict, deque
n=12
E=set()
for i in range(5):
 for u,v in [(0,1+i),(1+i,1+(i+1)%5),(11,6+i),(6+i,6+(i+1)%5),(1+i,6+i),(1+i,6+(i-1)%5)]:E.add(tuple(sorted((u,v))))
E=sorted(E);adj=[set()for _ in range(n)]
for u,v in E:adj[u].add(v);adj[v].add(u)
def comp(allowed):
 seen={next(iter(allowed))};todo=list(seen)
 while todo:
  v=todo.pop()
  for w in adj[v]&allowed-seen:seen.add(w);todo.append(w)
 return seen
for k in range(5):
 for r in combinations(range(n),k):
  allowed=set(range(n))-set(r);assert comp(allowed)==allowed
assert {len(a)for a in adj}=={5}
F=[t for t in combinations(range(n),3) if all(v in adj[u]for u,v in combinations(t,2))]
assert len(E)==30 and len(F)==20
inc=defaultdict(list)
for i,f in enumerate(F):
 for e in combinations(f,2):inc[e].append(i)
assert all(len(inc[e])==2 for e in E)
# Give all faces a compatible orientation, proving orientability. With Euler2 and all vertex links circles, this is a sphere.
ori={0:1};q=deque([0])
def direction(f,e):
 a,b=e
 return 1 if (f.index(a)+1)%3==f.index(b) else -1
while q:
 i=q.popleft()
 for e in combinations(F[i],2):
  j=next(j for j in inc[e]if j!=i)
  sj=-ori[i]*direction(F[i],e)*direction(F[j],e)
  if j in ori:assert ori[j]==sj
  else:ori[j]=sj;q.append(j)
assert len(ori)==20
for v in range(n):
 link=[(a,b)for a,b in combinations(adj[v],2)if a in adj[b]]
 assert len(link)==5 and all(sum(w in e for e in link)==2 for w in adj[v])
f=(0,1,2,1,2,3,3,0,3,0,2,1)
g=(0,1,2,1,3,2,0,3,0,1,3,2)
for c in [f,g]:assert all(c[u]!=c[v]for u,v in E)
z,x,y,b=0,2,3,5
assert tuple(sorted((z,x,y))) in F and b in adj[z]and b not in adj[x]|adj[y]
assert f[x]^f[y]==f[z]^f[b]==3
assert g[x]^g[y]==3 and g[z]^g[b]==2
for a,b in combinations((1,2,3),2):
 H=[set()for _ in F]
 for e in E:
  if f[e[0]]^f[e[1]]in(a,b):
   i,j=inc[e];H[i].add(j);H[j].add(i)
 assert {len(h)for h in H}=={2}
 seen={0};q=[0]
 while q:
  for j in H[q.pop()]-seen:seen.add(j);q.append(j)
 assert len(seen)==20
print('PASS: explicit icosahedron is a 5-connected sphere triangulation; all degrees5; zxy is facial; zb exists; b not adjacent x,y.')
print('PASS: coloring f locks xy,zb at difference3; each dual two-color subgraph is a Hamilton cycle; every Tait-Kempe move is a global color transposition.')
print('PASS: coloring g separates xy,zb, differences3 and2, so a different Tait-Kempe class provides the target.')
print('E=',E)
print('F=',F)
print('f=',f,'g=',g,'roles=',(z,x,y,5))
