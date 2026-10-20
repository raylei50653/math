#!/usr/bin/env python3
"""Exact, stdlib-only interfaces; no graph-realizability inference."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product, permutations, combinations

ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
NAMES=('G','Q1','Q2','GB')
PERMS=tuple(p for p in permutations(range(4)) if p[0]//2==p[1]//2 and p[2]//2==p[3]//2)

def canonical(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
def growth(n,t=(0,),four=False):
 if len(t)==n:yield t;return
 for x in range(min(3,max(t)+1)+1 if four else max(t)+2):yield from growth(n,t+(x,),four)
def hc(t):return min(tuple(p[c] for c in t) for p in PERMS)
def mv(matrix,v):return [sum(a*b for a,b in zip(row,v)) for row in matrix]
def mask(v):return sum(1<<i for i,n in enumerate(v) if n>0)
def noncrossing(p):return not any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b] for a,b,c,d in combinations(range(len(p)),4))
def rref(a):
 a=[[Fraction(x) for x in r] for r in a];piv=[]
 for col in range(len(a[0])):
  k=next((i for i in range(len(piv),len(a)) if a[i][col]),None)
  if k is None:continue
  r=len(piv);a[r],a[k]=a[k],a[r];q=a[r][col];a[r]=[x/q for x in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][col]:
    q=a[i][col];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
  piv.append(col)
 return a,piv

def interfaces():
 eight=[t for t in growth(8,four=True) if proper(t)];ten=[t for t in growth(10,four=True) if proper(t)]
 i8={t:i for i,t in enumerate(eight)};i10={t:i for i,t in enumerate(ten)}
 joint=[];M={name:[[0]*274 for _ in ROWS] for name in NAMES};sectors={s:[0]*274 for s in ('Aa','Ab')}
 for j,row in enumerate(ROWS):
  x,y,a,b,c=map(int,row)
  for n,R,L,q in product(range(4),repeat=4):
   t=(a,n,R,L,q,c,x,y);good=proper(t) and b not in {a,c,q};lifts=[]
   if good:lifts=[(p,h) for p,h in product(range(4),repeat=2) if p not in {a,b,q,n,h} and h not in {p,q,L,R,n}]
   flags=(int(good and n==b and R==q),int(good and n==b and L==b),int(good and b not in {n,R,L}))
   i=i8[canonical(t)] if proper(t) else -1
   joint.append([j,n,R,L,q,i,int(good),[list(v) for v in lifts],list(flags)])
   if good:
    M['G'][j][i]+=len(lifts)
    for name,f in zip(NAMES[1:],flags):M[name][j][i]+=f
    if j==9:
     sectors['Aa'][i]+=sum(h==a for p,h in lifts);sectors['Ab'][i]+=sum(h==b for p,h in lifts)
    if flags[0]:assert bool(lifts)==(L!=a)
    if flags[1]:assert bool(lifts)==(a==q or R!=a)
 T=[]
 for a,n,R,L,q,c,x,y in eight:
  counter=Counter()
  for s,v,w,t,r in product(range(4),repeat=5):
   core=(a,n,R,L,q,c,s,v,w,t)
   if proper(core) and x not in {s,r} and y not in {t,r} and r not in {s,v,w,t}:counter[i10[canonical(core)]]+=1
  T.append(sorted(counter.items()))
 core_caps=[]
 for a,n,R,L,q,c,s,v,w,t in ten:
  left=[(b,p,h) for b,p,h in product(range(4),repeat=3) if b not in {a,c,q,p} and p not in {a,q,n,h} and h not in {q,R,L,n}]
  right=[(x,y,r) for x,y,r in product(range(4),repeat=3) if r not in {s,v,w,t,x,y} and x not in {c,s,y} and y not in {a,t}]
  q1=[b for b in range(4) if b==n and R==q and b not in {a,c,q}]
  q2=[b for b in range(4) if b==n==L and b not in {a,c,q}]
  gb=[b for b in range(4) if b not in {a,c,q,n,R,L}]
  core_caps.append({'left':[list(v) for v in left],'right':[list(v) for v in right],'Q1':q1,'Q2':q2,'GB':gb})
 C={name:[[0]*2461 for _ in ROWS] for name in NAMES}
 for name in NAMES:
  for j,row in enumerate(M[name]):
   for e,value in enumerate(row):
    if value:
     for i,mult in T[e]:C[name][j][i]+=value*mult
 return {'eight':eight,'ten':ten,'joint':joint,'M':M,'sectors':sectors,'T':T,'C':C,'core_caps':core_caps}

def kempe(n,states):
 """All noncrossing, triangulated complementary-pair component orbits."""
 lits=[t for t in product(range(4),repeat=n) if proper(t)]
 hcanon={t:hc(t) for t in lits};hist=Counter(hcanon.values());hrows=sorted(hist);hi={t:i for i,t in enumerate(hrows)}
 literal_index={t:hi[hcanon[t]] for t in lits};index={t:i for i,t in enumerate(states)}
 sideparts=defaultdict(list);nc=0
 for p in growth(n):
  if not noncrossing(p):continue
  nc+=1;b=max(p)+1
  if sum(p[i]!=p[(i+1)%n] for i in range(n))!=2*(b-1):continue
  adjacency=[set() for _ in range(b)]
  for i in range(n):
   a,c=p[i],p[(i+1)%n]
   if a!=c:adjacency[a].add(c);adjacency[c].add(a)
  val=[None]*b;val[0]=0;stack=[0];okay=True
  while stack:
   a=stack.pop()
   for c in adjacency[a]:
    if val[c] is None:val[c]=1-val[a];stack.append(c)
    elif val[c]==val[a]:okay=False
  if not okay:continue
  assert all(v is not None for v in val)
  side=tuple(val[x] for x in p);sideparts[side].append(p);sideparts[tuple(1-x for x in side)].append(p)
 columns={}
 for t in hrows:
  for p in sideparts[tuple(c//2 for c in t)]:
   orbit=[tuple(c^1 if chosen&(1<<p[i]) else c for i,c in enumerate(t)) for chosen in range(1<<(max(p)+1))]
   assert len(set(orbit))==len(orbit)
   col=tuple(sorted(Counter(literal_index[x] for x in orbit).items()))
   columns.setdefault(col,(t,p))
 cols=sorted(columns)
 return {'n':n,'states':states,'hrows':hrows,'hsize':[hist[t] for t in hrows], 'rowids':[index[canonical(t)] for t in hrows], 'columns':cols,'descriptions':[columns[c] for c in cols],'noncrossing_count':nc,'literal_count':len(lits)}

def close(K,initial):
 rowids=K['rowids'];cols=K['columns'];live=set(initial);rounds=[]
 while True:
  good=[j for j,col in enumerate(cols) if all(rowids[r] in live for r,v in col)]
  covered={r for j in good for r,v in cols[j]};bad={}
  for r,i in enumerate(rowids):
   if i in live and r not in covered:bad.setdefault(i,r)
  if not bad:return sorted(live),rounds
  rounds.append([[i,bad[i]] for i in sorted(bad)]);live-=bad.keys()

def planar_basis(eight,live):
 parts=[p for p in growth(8) if proper(p) and noncrossing(p)]
 A=[[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for p in parts] for t in eight]
 assert len(rref(A)[1])==91
 reduced,piv=rref([r for i,r in enumerate(A) if i not in set(live)]);free=[i for i in range(len(parts)) if i not in piv];basis=[]
 for f in free:
  v=[Fraction(0)]*len(parts);v[f]=1
  for k,p in enumerate(piv):v[p]=-reduced[k][f]
  basis.append(mv(A,v))
 return parts,A,basis
