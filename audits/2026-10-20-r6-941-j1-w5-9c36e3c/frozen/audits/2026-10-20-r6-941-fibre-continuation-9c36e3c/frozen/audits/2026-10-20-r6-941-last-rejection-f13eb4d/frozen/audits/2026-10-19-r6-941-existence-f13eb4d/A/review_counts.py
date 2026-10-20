#!/usr/bin/env python3
"""Independent named-edge transfers and rational signed-span identity audit."""
import gzip,hashlib,itertools,json
from fractions import Fraction
from pathlib import Path
D=Path(__file__).resolve().parent;P=D.parent
c=json.loads(gzip.decompress((P/'counts.json.gz').read_bytes()))
old=json.loads((P/'frozen/audits/2026-10-19-r6-941-quotients-13dc5ff/A/certificate.json').read_text())
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
def growth(n,t=(0,)):
 if len(t)==n:yield t;return
 for v in range(max(t)+2):yield from growth(n,t+(v,))
states=sorted({canonical(t) for t in itertools.product(range(4),repeat=8) if proper(t)})
assert [list(t) for t in states]==c['E_states'];index={t:i for i,t in enumerate(states)}
order=('a','n','R','L','q','c','x','y');rim=list(zip(order,order[1:]+order[:1]));common=rim+[('b','a'),('b','c'),('b','q')]
original=common+[('p','a'),('p','b'),('p','q'),('p','n'),('p','h'),('h','q'),('h','L'),('h','R'),('h','n')]
M=[[[0]*274 for _ in range(10)] for _ in range(2)];G=[[0]*274 for _ in range(10)];Aa=[0]*274
for ri,word in enumerate(c['rows']):
 x,y,a,b,cc=map(int,word)
 for n,R,L,q in itertools.product(range(4),repeat=4):
  f=dict(x=x,y=y,a=a,b=b,c=cc,n=n,R=R,L=L,q=q);t=tuple(f[k] for k in order)
  if not proper(t):continue
  i=index[canonical(t)]
  # Full graph tests: quotient b=L plus aR, or the three added diagonals.
  if b==L and all(f[u]!=f[v] for u,v in common+[('a','R')]):M[0][ri][i]+=1
  if all(f[u]!=f[v] for u,v in common+[('a','L'),('a','R'),('b','L')]):M[1][ri][i]+=1
  for p,h in itertools.product(range(4),repeat=2):
   ff=dict(f,p=p,h=h)
   if all(ff[u]!=ff[v] for u,v in original):
    G[ri][i]+=1
    if ri==9 and h==a:Aa[i]+=1
assert M==c['J_matrices'] and G==old['literal_E_count_matrices']['G'] and Aa==old['original_alpha_sectors']['Aa']
other=json.loads((P/'C/comparisons.json').read_text())
assert M==[other['matrices'][name]['E'] for name in ('J1','J2')]
parts=[p for p in growth(8) if proper(p) and not any(p[a]==p[cc] and p[b]==p[d] and p[a]!=p[b] for a,b,cc,d in itertools.combinations(range(8),4))]
assert [list(p) for p in parts]==c['planar_partitions'] and len(parts)==91
S=[[int(all(p[a]!=p[b] or t[a]==t[b] for a in range(8) for b in range(a))) for p in parts] for t in states]
def reduce(A):
 A=[[Fraction(v) for v in row] for row in A];piv=[]
 for j in range(len(A[0])):
  k=next((k for k in range(len(piv),len(A)) if A[k][j]),None)
  if k is None:continue
  r=len(piv);A[r],A[k]=A[k],A[r];v=A[r][j];A[r]=[x/v for x in A[r]]
  for k in range(len(A)):
   if k==r or not A[k][j]:continue
   v=A[k][j];A[k]=[x-v*y for x,y in zip(A[k],A[r])]
  piv.append(j)
  if len(piv)==len(A):break
 return A,piv
assert len(reduce(S)[1])==91
live=set(c['source_E_live']);assert c['source_E_live']==old['source_E_closure']['live'] and len(live)==225
R,piv=reduce([row for i,row in enumerate(S) if i not in live]);free=[j for j in range(91) if j not in piv];assert len(free)==44
own=[]
for j in free:
 v=[Fraction(0)]*91;v[j]=1
 for k,p in enumerate(piv):v[p]=-R[k][j]
 own.append([sum(a*b for a,b in zip(row,v)) for row in S])
saved=[[Fraction(v) for v in row] for row in c['basis']]
assert len(saved)==44 and len(reduce(own+saved)[1])==44
forms=[[x-u-v for x,u,v in zip(M[0][9],M[1][4],M[1][6])],
       [x-u-v for x,u,v in zip(M[1][9],M[0][4],M[0][6])],
       [x+y-z for x,y,z in zip(M[0][9],M[1][9],Aa)]]
assert forms==c['identity_forms']
assert all(sum(a*b for a,b in zip(row,vec))==0 for row in forms for vec in own+saved)
wrong=[x+u+v for x,u,v in zip(M[0][9],M[1][4],M[1][6])]
assert any(sum(a*b for a,b in zip(wrong,vec)) for vec in own)
print(json.dumps({'pass':True,'counts_certificate_sha256':hashlib.sha256((P/'counts.json.gz').read_bytes()).hexdigest(),'edge_generated_J_and_original_matrices_match':True,'C_independent_E_matrices_match':True,'noncrossing_columns':91,'full_signed_span_rank':91,'zero_restricted_rank':44,'reconstructed_basis_and_saved_joint_rank':44,'identity_residuals_checked':264,'wrong_sign_nonzero':True,'source_existence_claimed':False},sort_keys=True))
