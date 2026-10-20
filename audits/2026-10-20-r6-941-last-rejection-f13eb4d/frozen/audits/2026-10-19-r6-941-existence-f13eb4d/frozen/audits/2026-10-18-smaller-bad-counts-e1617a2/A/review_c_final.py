#!/usr/bin/env python3
"""Independent reconstruction of C planar-span and literal projection evidence."""
import hashlib,itertools,json
from pathlib import Path
import sympy as sp
R=Path(__file__).resolve().parent
F=R.parent/'frozen/audits/2026-10-18-smaller-bad-e1617a2'
D=json.loads((F/'kempe-consistency.json').read_text())
CERT_PATH=R.parent/'C/certificate.json'
CERT=json.loads(CERT_PATH.read_text())
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
def owners(blocks):
 return tuple(next(j for j,block in enumerate(blocks) if v in block) for v in range(8))
nc.sort(key=owners)
columns=[]
for blocks in nc:
 col=tuple(int(all(len({t[v] for v in block})==1 for block in blocks)) for t in T)
 if any(col):columns.append(col)
assert len(columns)==91 and len(set(columns))==91
expected=sp.Matrix(columns).T
assert expected.rank()==CERT['rank']==91
assert CERT['noncrossing_partitions']==1430 and CERT['nonzero_columns']==91

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
assert CERT['rows']==list(rows)

checks=[]
for prior in D['results']:
 mask=prior['source_mask']
 banned=sorted(set(range(274))-set(prior['surviving_ids']))
 constraint=expected[banned,:]
 N=sp.Matrix.hstack(*constraint.nullspace());B=expected*N
 rec=next(x for x in CERT['maximal_support_witnesses'] if x['source_mask']==mask)
 assert rec['dimension']==B.cols
 assert len(rec['coefficient_vector'])==91 and len(rec['exterior_counts'])==274
 assert expected*sp.Matrix(rec['coefficient_vector'])==sp.Matrix(rec['exterior_counts'])
 assert all(x>=0 for x in rec['exterior_counts'])
 assert sorted(i for i in prior['surviving_ids'] if not any(B[i,:]))==rec['extra_zero_ids']
 assert set(i for i,x in enumerate(rec['exterior_counts']) if x)==set(prior['surviving_ids'])-set(rec['extra_zero_ids'])
 assert M['G']*sp.Matrix(rec['exterior_counts'])==sp.Matrix(rec['source_counts'])
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

rays=sp.Matrix(CERT['source932']['exterior_rays'])
assert expected*sp.Matrix(CERT['source932']['coefficient_rays'])==rays
assert rays.shape==(274,3) and all(v>=0 for v in rays)
assert rays[[11,17,132],:]==sp.eye(3)
bad932=sorted(set(range(274))-set(D['results'][0]['surviving_ids']))
B932=expected*sp.Matrix.hstack(*expected[bad932,:].nullspace())
assert B932.row_join(rays).rank()==3
for name,m in M.items():assert m*rays==sp.Matrix(CERT['source932']['projected_rays'][name])
assert list(M['G'][9,:]*rays)==[8,4,4]
assert list(M['Q1'][9,:]*rays)==[4,2,4]
assert list(M['Q1'][6,:]*rays)==[1,1,1]
assert list(M['Q2'][9,:]*rays)==[4,2,0]
assert list(M['Q2'][6,:]*rays)==[1,1,0]
assert list(M['GB'][9,:]*rays)==[8,4,4]
assert list(M['GB'][6,:]*rays)==[2,2,1]
assert len(CERT['maximal_support_witnesses'])==3
assert {r['source_mask'] for r in CERT['maximal_support_witnesses']}=={932,933,941}
assert len(CERT['identities'])==6
assert {(r['source_mask'],r['candidate']) for r in CERT['identities']}==set(itertools.product((932,933),('Q1','Q2','GB')))
for claim in CERT['identities']:
 assert (claim['factor'],claim['residual_exterior_id'],claim['residual_factor'])==(4,17,4 if claim['candidate']=='GB' else 2)
 assert (claim['acceptance_row'],claim['rejection_row'])==('01232','01212')
assert len(CERT['source941_separate_candidate_controls'])==3
assert {r['name'] for r in CERT['source941_separate_candidate_controls']}=={'Q1','Q2','GB'}
for control in CERT['source941_separate_candidate_controls']:
 assert len(control['coefficient_vector'])==91 and len(control['exterior_counts'])==274
 z=expected*sp.Matrix(control['coefficient_vector'])
 assert z==sp.Matrix(control['exterior_counts']) and all(v>=0 for v in z)
 assert all(z[i]==0 for i in set(range(274))-set(D['results'][2]['surviving_ids']))
 g=M['G']*z;q=M[control['name']]*z
 assert g==sp.Matrix(control['source_counts'])
 assert sum(1<<i for i,v in enumerate(g) if v)>0
 assert sum(1<<i for i,v in enumerate(g) if v)==941
 assert q==sp.Matrix(control['candidate_counts']) and q[9]>0 and all(q[i]==0 for i in (1,4,6))
result={'noncrossing_partition_count':1430,'nonzero_equality_columns':91,
        'span_rank':91,'exact_932_rays':True,'exact_932_933_leak_identities':True,
        'results':checks,'input_sha256':{str(p.relative_to(R.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (CERT_PATH,R/'triangulated-witnesses.json')}}
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
output=R/'REVIEW-C-FINAL.json'
if args.write:
 with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
else:
 assert json.loads(output.read_text())==result
print(json.dumps({k:v for k,v in result.items() if k not in ('input_sha256','results')}),flush=True)
print(json.dumps([{k:v for k,v in r.items() if k!='A_witness_coordinates'} for r in checks]),flush=True)
