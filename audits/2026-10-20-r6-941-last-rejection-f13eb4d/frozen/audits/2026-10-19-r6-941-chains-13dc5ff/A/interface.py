#!/usr/bin/env python3
"""Exact stdlib eleven-point component interface; no source realizability inference."""
import importlib.util,itertools
from collections import Counter,defaultdict
from pathlib import Path
D=Path(__file__).resolve().parent
ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('m',ROOT/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def ncgrowth(n,t=(0,)):
 if len(t)==n:yield t;return
 d=len(t)
 for x in range(max(t)+2):
  if any(t[a]==t[c] and t[b]==x and t[a]!=x for a,b,c in itertools.combinations(range(d),3)):continue
  yield from ncgrowth(n,t+(x,))

def kempe(n,states):
 lits=[t for t in itertools.product(range(4),repeat=n) if m.proper(t)]
 hcanon={t:m.hc(t) for t in lits};hist=Counter(hcanon.values());hrows=sorted(hist);hi={t:i for i,t in enumerate(hrows)}
 literal_index={t:hi[hcanon[t]] for t in lits};index={t:i for i,t in enumerate(states)}
 sideparts=defaultdict(list);nc=0
 for p in ncgrowth(n):
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
   col=tuple(sorted(Counter(literal_index[x] for x in orbit).items()))
   columns.setdefault(col,(t,p))
 cols=sorted(columns)
 return {'n':n,'states':states,'hrows':hrows,'hsize':[hist[t] for t in hrows], 'rowids':[index[m.canonical(t)] for t in hrows], 'columns':cols,'descriptions':[columns[c] for c in cols],'noncrossing_count':nc,'literal_count':len(lits)}

def cap(t,which):
 # L fan: a,n,R,U,V,q,c,s,v,w,t; R fan: a,n,U,V,L,q,c,s,v,w,t.
 if which=='L':a,n,R,U,V,q,c,s,v,w,T=t
 else:a,n,U,V,L,q,c,s,v,w,T=t
 out={g:[0]*10 for g in ('G','Q1','Q2')};da=0
 for f in range(4):
  if which=='L':L=f
  else:R=f
  if f in ({R,U,V,q} if which=='L' else {n,U,V,L}):continue
  left=[(b,p,h) for b,p,h in itertools.product(range(4),repeat=3) if b not in {a,c,q,p} and p not in {a,q,n,h} and h not in {q,L,R,n}]
  right=[(x,y,r) for x,y,r in itertools.product(range(4),repeat=3) if r not in {s,v,w,T,x,y} and x not in {c,s,y} and y not in {a,T}]
  for x,y,r in right:
   for b,p,h in left:
    row=''.join(map(str,m.canonical((x,y,a,b,c))));out['G'][m.ROWS.index(row)]+=1
    if row=='01232' and h==a:da+=1
   for b in range(4):
    if b in {a,c,q}:continue
    row=''.join(map(str,m.canonical((x,y,a,b,c))));j=m.ROWS.index(row)
    if b==n and R==q:out['Q1'][j]+=1
    if b==n==L:out['Q2'][j]+=1
 return out,da
