#!/usr/bin/env python3
"""All five c=5 changed frames, complete lifts and joint exact supports; stdlib."""
import argparse, copy, gzip, hashlib, importlib.util, json
from itertools import combinations, product
from math import factorial
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='13dc5ff163045c85b5c82dde438eb5f275dab999'
MODEL='audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
NEEDED=[MODEL,'artifacts/c5_cells/cells.json',
 'audits/2026-10-19-r6-941-quotients-13dc5ff/SOURCE_CONTRACT.md',
 'audits/2026-10-19-r6-941-acceptance-13dc5ff/SOURCE_CONTRACT.md',
 'audits/2026-10-19-r6-941-acceptance-13dc5ff/D/PROOF.md']
PINS=('a','n','R','L','q','u','s','v','w','t')
OPS=(('H0','q',(('q','s'),('q','x'))),
 ('H1','q',(('q','x'),('u','x'))),
 ('H2','u',(('b','u'),('u','x'))),
 ('H3','s',(('b','s'),('b','u'))),
 ('H4','s',(('b','s'),('q','s'))))
LEFT=(('b','a'),('b','q'),('b','p'),('p','a'),('p','q'),('p','n'),('p','h'),
 ('h','q'),('h','L'),('h','R'),('h','n'))
RIGHT=(('x','y'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),
 ('r','t'),('r','w'),('r','v'),('r','s'))

def packed(obj):return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(obj):return hashlib.sha256(packed(obj)).hexdigest()
def authority():
 seal=json.loads((HERE.parent/'INPUTS.json').read_text());assert seal['base']==BASE
 entries={v['path']:v for v in seal['files']};result={}
 for path in NEEDED:
  got=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
  assert got==entries[path]['sha256'],('frozen input drift',path)
  result[path]=got
 return result

def model():
 spec=importlib.util.spec_from_file_location('frozen_c5_interface',ROOT/MODEL)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def matrices(m):
 ten=[t for t in m.growth(10,four=True) if m.proper(t)]
 allmat=[[[0]*len(ten) for _ in m.ROWS] for _ in range(6)];caps=[]
 for i,word in enumerate(ten):
  f=dict(zip(PINS,word));left=[];right=[]
  for b,p,h in product(range(4),repeat=3):
   ff=dict(f,b=b,p=p,h=h)
   if all(ff[j]!=ff[k] for j,k in LEFT):left.append((b,p,h))
  for x,y,r in product(range(4),repeat=3):
   ff=dict(f,x=x,y=y,r=r)
   if all(ff[j]!=ff[k] for j,k in RIGHT):right.append((x,y,r))
  entry={'original_by_c':[],'candidates':[],'core':word}
  for c in range(4):
   good=c not in (f['q'],f['u'],f['s'])
   ls=[z for z in left if z[0]!=c] if good else []
   rs=[z for z in right if z[0]!=c] if good else []
   entry['original_by_c'].append({'c':c,'left':ls,'right':rs})
   for b,p,h in ls:
    for x,y,r in rs:
     row=m.ROWS.index(''.join(map(str,m.canonical((x,y,f['a'],b,c)))))
     allmat[0][row][i]+=1
  for hindex,(name,frame,edges) in enumerate(OPS):
   # Every new edge is wholly on core+left or core+right. Thus the full
   # lifts factor over this one complete core colouring, with empties retained.
   le=[e for e in edges if 'x' not in e];re=[e for e in edges if 'x' in e]
   ls=[z for z in left if all(dict(f,b=z[0],p=z[1],h=z[2])[j]!=dict(f,b=z[0],p=z[1],h=z[2])[k] for j,k in le)]
   rs=[z for z in right if all(dict(f,x=z[0],y=z[1],r=z[2])[j]!=dict(f,x=z[0],y=z[1],r=z[2])[k] for j,k in re)]
   entry['candidates'].append({'name':name,'left':ls,'right':rs})
   for b,p,h in ls:
    for x,y,r in rs:
     ff=dict(f,b=b,p=p,h=h,x=x,y=y,r=r)
     assert all(ff[j]!=ff[k] for j,k in LEFT+RIGHT+edges)
     row=m.ROWS.index(''.join(map(str,m.canonical((x,y,f['a'],b,f[frame])))))
     allmat[hindex+1][row][i]+=1
  fac=factorial(4-len(set(word)))
  for M in allmat:
   for row in M:assert row[i]%fac==0;row[i]//=fac
  caps.append(entry)
 return ten,allmat,caps

def projection(m,M,live):return m.mask([sum(row[i] for i in live) for row in M])
def closed(m,K,seed,C,matrices):
 live,rounds=m.close(K,seed)
 return {'initial':len(seed),'round_sizes':[len(r) for r in rounds],
  'rounds_sha256':digest(rounds),'live':live,'original_support_upper':projection(m,C,live),
  'candidate_support_uppers':[projection(m,N,live) for N in matrices]}

def compute():
 inputs=authority();m=model();ten,matrices_all,caps=matrices(m)
 C,*Ns=matrices_all;K=m.kempe(10,ten)
 initial=[i for i in range(len(ten)) if all(not C[r][i] for r in (1,4,6))]
 general=closed(m,K,initial,C,Ns);live=general['live']
 assert len(initial)==2141 and len(live)==1881 and general['original_support_upper']==941
 catalogue=sorted(map(int,json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())['cells']))
 individual=[]
 for j,N in enumerate(Ns):
  records=[];compatible=[]
  for support in catalogue:
   seed=[i for i in live if all(not N[r][i] for r in range(10) if not(support>>r&1))]
   rec=closed(m,K,seed,C,[N]);upper=rec['candidate_support_uppers'][0]
   possible=rec['original_support_upper']==941 and support&~upper==0
   rec.update(allowed_catalogue_support=support,not_excluded_by_zero_closure=possible)
   if possible:compatible.append(support)
   records.append(rec)
  assert compatible==([1022] if j==1 else [1022,1023])
  individual.append({'candidate':OPS[j][0],'compatible_catalogue_supports':compatible,'comparisons':records})
 joint=[];survivors=[]
 for zero_bits in range(32):
  supports=[1022 if zero_bits>>j&1 else 1023 for j in range(5)]
  seed=[i for i in live if all(not Ns[j][0][i] for j in range(5) if zero_bits>>j&1)]
  rec=closed(m,K,seed,C,Ns)
  possible=rec['original_support_upper']==941 and all(s&~u==0 for s,u in zip(supports,rec['candidate_support_uppers']))
  rec.update(zero_bits=zero_bits,exact_supports_hypothesis=supports,not_excluded_by_zero_closure=possible)
  if possible:survivors.append(zero_bits)
  joint.append(rec)
 assert survivors==[2,6,10,11,14,26,27,30]
 # Exhaustive pentagon triangulations: noncrossing pairs of its five diagonals.
 poly=('b','q','u','s','x');diag=((0,2),(0,3),(1,3),(1,4),(2,4));tri=[]
 for ds in combinations(diag,2):
  (i,j),(k,l)=ds
  if i<k<j<l or k<i<l<j:continue
  tri.append(tuple(sorted(tuple(sorted((poly[i],poly[j]))) for i,j in ds)))
 assert sorted(tri)==sorted(tuple(sorted(tuple(sorted(e)) for e in edges)) for name,frame,edges in OPS)
 cert={'base':BASE,'inputs':inputs,'source_contract':'same original G, full support941, c=5',
  'core_order':PINS,'literal_rows':m.ROWS,'original_boundary':('x','y','a','b','c'),
  'operations':[{'name':name,'deleted':['c'],'added_edges':edges,
   'boundary':('x','y','a','b',frame),'completed_inner_delta':-1} for name,frame,edges in OPS],
  'all_pentagon_triangulations':tri,'core_states':ten,'original_matrix':C,'candidate_matrices':Ns,
  'complete_caps_sha256':digest(caps),'component_columns':len(K['columns']),
  'component_columns_sha256':digest(K['columns']),'general_c5':general,
  'individual_comparisons':individual,'joint_comparisons':joint,
  'joint_support_zero_bit_patterns_not_excluded':survivors,
  'source_realization_supplied':False,'strict_smaller_bad_constructed':False}
 return cert,caps

def verify(got,want):assert got==want,'complete lifts, literal frames, joint core or support comparison mismatch'
def negatives(cert,caps):
 out=[]
 mutations=[('lose_one_actual_triangulation',lambda z:z['operations'].pop()),
  ('omit_boundary_promotion_cost',lambda z:z['operations'][0].__setitem__('completed_inner_delta',0)),
  ('keep_old_frame_after_deleting_c',lambda z:z['operations'][1].__setitem__('boundary',z['original_boundary'])),
  ('admit_all_five_full_supports',lambda z:z['joint_support_zero_bit_patterns_not_excluded'].insert(0,0)),
  ('claim_independent_marginals_are_joint',lambda z:z['joint_support_zero_bit_patterns_not_excluded'].__setitem__(0,3)),
  ('lose_source_positive_row',lambda z:z['joint_comparisons'][31].__setitem__('original_support_upper',941)),
  ('surviving_pattern_as_realization',lambda z:z.__setitem__('source_realization_supplied',True))]
 for name,mutate in mutations:
  wrong=copy.deepcopy(cert);mutate(wrong)
  try:verify(wrong,cert)
  except AssertionError:out.append(name)
  else:raise AssertionError('accepted negative '+name)
 wrong=copy.deepcopy(caps);entry=next(e for e in wrong if e['candidates'][0]['left']);entry['candidates'][0]['left'].pop()
 try:verify(wrong,caps)
 except AssertionError:out.append('drop_complete_cap_lift')
 else:raise AssertionError('accepted incomplete cap')
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
 cert,caps=compute()
 if args.build:
  for name,value in (('certificate.json',cert),('cap-lifts.json',caps)):
   with (HERE/(name+'.gz')).open('xb') as out:out.write(gzip.compress(packed(value),mtime=0))
 verify(json.loads(gzip.decompress((HERE/'certificate.json.gz').read_bytes())),json.loads(packed(cert)))
 assert gzip.decompress((HERE/'cap-lifts.json.gz').read_bytes())==packed(caps)
 print(json.dumps({'pass':True,'base':BASE,'all_five_completed_inner_delta':-1,
  'H1_support_exactly':1022,'joint_zero_bit_patterns_not_excluded':cert['joint_support_zero_bit_patterns_not_excluded'],
  'joint_patterns_tested':32,'source_realization_supplied':False,'strict_smaller_bad_constructed':False,
  'negative_controls_rejected':negatives(json.loads(packed(cert)),json.loads(packed(caps)))},sort_keys=True))
if __name__=='__main__':main()
