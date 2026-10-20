#!/usr/bin/env python3
"""Independent reconstruction of C planar-span and literal projection evidence."""
import hashlib,itertools,json
from pathlib import Path
import sympy as sp
R=Path(__file__).resolve().parent
F=R.parent/'frozen/audits/2026-10-18-smaller-bad-e1617a2'
D=json.loads((F/'kempe-consistency.json').read_text())
E=json.loads((R.parent/'C/explore.json').read_text())
P=json.loads((R.parent/'C/projections.json').read_text())
A=json.loads((R/'triangulated-witnesses.json').read_text())
T=[tuple(t) for t in D['tuples']];idx={t:i for i,t in enumerate(T)}

def normalize(t):
 used=[];out=[]
 for c in t:
  if c not in used:used.append(c)
  out.append(used.index(c))
 return tuple(out)

# Build all partitions as tuples of blocks by insertions, not RGS recursion.
parts=[((0,),)]
for k in range(1,8):
 nxt=[]
 for blocks in parts:
  nxt.append(blocks+((k,),))
  for j in range(len(blocks)):
   nxt.append(blocks[:j]+(blocks[j]+(k,),)+blocks[j+1:])
 parts=nxt
assert len(parts)==4140
nc=[]
for blocks in parts:
 owner={v:j for j,block in enumerate(blocks) for v in block}
 if not any(owner[a]==owner[c] and owner[b]==owner[d] and owner[a]!=owner[b]
            for a,b,c,d in itertools.combinations(range(8),4)):
  nc.append(blocks)
assert len(nc)==1430
columns=[]
for blocks in nc:
 col=tuple(int(all(len({t[v] for v in block})==1 for block in blocks)) for t in T)
 if any(col):columns.append(col)
assert len(columns)==91 and len(set(columns))==91
expected=sp.Matrix(E['matrix'])
assert set(columns)=={tuple(expected[:,j]) for j in range(expected.cols)}
assert expected.rank()==91

# Reconstruct literal C5 count maps by enumerating all literal C8 assignments.
rows=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
lookup={tuple(map(int,r)):i for i,r in enumerate(rows)}
M={name:sp.zeros(10,274) for name in ('G','Q1','Q2','GB')}
for t in itertools.product(range(4),repeat=8):
 if any(t[i]==t[(i+1)%8] for i in range(8)):continue
 a,n,right,left,q,c,x,y=t
 i=idx[normalize(t)]
 for b in range(4):
  boundary=(x,y,a,b,c)
  if boundary not in lookup or b==a or b==c or b==q:continue
  j=lookup[boundary]
  for p,h in itertools.product(range(4),repeat=2):
   values={'a':a,'b':b,'q':q,'n':n,'L':left,'R':right,'p':p,'h':h}
   edges=(('p','a'),('p','b'),('p','q'),('p','h'),('p','n'),
          ('h','q'),('h','L'),('h','R'),('h','n'))
   if all(values[u]!=values[v] for u,v in edges):M['G'][j,i]+=1
  if n==b and right==q:M['Q1'][j,i]+=1
  if n==b and left==b:M['Q2'][j,i]+=1
  if all(b!=v for v in (n,left,right)):M['GB'][j,i]+=1
for name,m in M.items():assert m==sp.Matrix(P['projection_matrices'][name])

checks=[]
for prior in D['results']:
 mask=prior['source_mask']
 rec=next(x for x in E['results'] if x['mask']==mask and x['kind']=='surviving_ids')
 B=sp.Matrix(rec['basis']);N=sp.Matrix(rec['n_basis'])
 banned=sorted(set(range(274))-set(prior['surviving_ids']))
 constraint=expected[banned,:]
 assert constraint*N==sp.zeros(len(banned),N.cols)
 assert B==expected*N and N.rank()==N.cols
 assert N.cols==91-constraint.rank()
 if mask in (932,933):
  for name,k in (('Q1',2),('Q2',2),('GB',4)):
   residual=4*M[name][6,:]-M[name][9,:]
   residual[17]-=k
   assert residual*B==sp.zeros(1,B.cols)
 count=sp.Matrix(next(r['counts'] for r in A['results'] if r['source_mask']==mask))
 coeff,params=B.gauss_jordan_solve(count)
 assert params.rows==0 and B*coeff==count
 checks.append({'mask':mask,'residual_dimension':B.cols,'independent_kernel_complete':True,
                'literal_projections_exact':True,'A_count_witness_in_planar_span':True,
                'A_witness_coordinates':[str(v) for v in coeff]})

rays=sp.Matrix(P['rays'])
assert rays.shape==(274,3) and all(v>=0 for v in rays)
assert rays[[11,17,132],:]==sp.eye(3)
B932=sp.Matrix(next(r['basis'] for r in E['results'] if r['mask']==932 and r['kind']=='surviving_ids'))
assert B932.row_join(rays).rank()==3
for name,m in M.items():assert m*rays==sp.Matrix(P['projected_rays'][name])
assert list(M['G'][9,:]*rays)==[8,4,4]
assert list(M['Q1'][9,:]*rays)==[4,2,4]
assert list(M['Q1'][6,:]*rays)==[1,1,1]
assert list(M['Q2'][9,:]*rays)==[4,2,0]
assert list(M['Q2'][6,:]*rays)==[1,1,0]
assert list(M['GB'][9,:]*rays)==[8,4,4]
assert list(M['GB'][6,:]*rays)==[2,2,1]
result={'noncrossing_partition_count':1430,'nonzero_equality_columns':91,
        'span_rank':91,'exact_932_rays':True,'exact_932_933_leak_identities':True,
        'results':checks,'input_sha256':{str(p.relative_to(R.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (R.parent/'C/explore.json',R.parent/'C/projections.json',R/'triangulated-witnesses.json')}}
with (R/'REVIEW-C.json').open('x') as f:
 f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('input_sha256','results')}),flush=True)
print(json.dumps([{k:v for k,v in r.items() if k!='A_witness_coordinates'} for r in checks]),flush=True)
