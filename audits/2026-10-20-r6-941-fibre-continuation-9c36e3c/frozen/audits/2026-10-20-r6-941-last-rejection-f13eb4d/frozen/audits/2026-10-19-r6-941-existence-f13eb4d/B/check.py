#!/usr/bin/env python3
"""Exact same-core c=5 comparisons; read-only stdlib replay by default."""
import argparse, copy, gzip, hashlib, importlib.util, json
from itertools import combinations, product
from math import factorial
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'frozen'
BASE='f13eb4d0887d962021992ae7afe3323af4d79cd3'
MODEL='audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
OLD='audits/2026-10-19-r6-941-chains-13dc5ff/C/check.py'
NEEDED=(MODEL,OLD,'artifacts/c5_cells/cells.json',
 'audits/2026-10-19-r6-941-chains-13dc5ff/SOURCE_CONTRACT.md',
 'audits/2026-10-19-r6-941-chains-13dc5ff/C/PROOF.md',
 'audits/2026-10-19-r6-941-chains-13dc5ff/PROOF.md',
 'audits/2026-10-19-r6-941-chains-13dc5ff/B/PROOF.md',
 'audits/2026-10-19-r6-941-acceptance-13dc5ff/D/PROOF.md',
 'audits/2026-10-19-r6-941-leakage-b89c591/B/SOURCE_CONTRACT.md')

def packed(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(packed(x)).hexdigest()
def authority():
 seal=json.loads((HERE.parent/'INPUTS.json').read_text());assert seal['base']==BASE
 entries={v['path']:v for v in seal['files']};out={}
 for p in NEEDED:
  data=(ROOT/p).read_bytes();h=hashlib.sha256(data).hexdigest()
  assert len(data)==entries[p]['bytes'] and h==entries[p]['sha256'],('frozen drift',p)
  out[p]=h
 return out

def load(path,name):
 s=importlib.util.spec_from_file_location(name,ROOT/path)
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def operations():
 poly=('x','y','a','b','q','u','s');ops=[]
 for keep in combinations(range(7),5):
  gaps=[]
  for k,start in enumerate(keep):
   end=keep[(k+1)%5]
   gap=tuple(poly[v%7] for v in range(start,start+(end-start)%7+1))
   if len(gap)>2:gaps.append(gap)
  if len(gaps)==2:edgepairs=[tuple((g[0],g[-1]) for g in gaps)]
  else:
   g=gaps[0];assert len(g)==4
   edgepairs=[((g[0],g[-1]),d) for d in ((g[0],g[2]),(g[1],g[3]))]
  for edges in edgepairs:
   ops.append({'name':'S'+str(len(ops)),'deleted':['c'],'boundary':[poly[j] for j in keep],
    'added_edges':edges,'completed_inner_delta':-1})
 assert len(ops)==28
 assert len({(tuple(o['boundary']),tuple(sorted(tuple(sorted(e)) for e in o['added_edges']))) for o in ops})==28
 return ops

def matrices(m,old):
 ten,alls,oldcaps=old.matrices(m);C,*Hs=alls
 ops=operations();Ss=[[[0]*len(ten) for _ in range(10)] for _ in ops]
 Qs=[[[0]*len(ten) for _ in range(10)] for _ in range(2)];caps=[]
 for i,word in enumerate(ten):
  f=dict(zip(old.PINS,word));left=[];right=[]
  for b,p,h in product(range(4),repeat=3):
   ff=dict(f,b=b,p=p,h=h)
   if all(ff[v]!=ff[w] for v,w in old.LEFT):left.append((b,p,h))
  for x,y,r in product(range(4),repeat=3):
   ff=dict(f,x=x,y=y,r=r)
   if all(ff[v]!=ff[w] for v,w in old.RIGHT):right.append((x,y,r))
  item={'core':word,'Q_by_c':[],'S_complete_lifts':[[] for _ in ops]}
  for c in range(4):
   good=c not in (f['q'],f['u'],f['s'])
   rs=[z for z in right if z[0]!=c] if good else []
   bs=[[f['n']] if good and f['n'] not in (f['a'],c,f['q']) and flag else []
       for flag in (f['R']==f['q'],f['L']==f['n'])]
   item['Q_by_c'].append({'c':c,'right':rs,'Q1_b':bs[0],'Q2_b':bs[1]})
   for j in range(2):
    for b in bs[j]:
     for x,y,r in rs:
      row=m.ROWS.index(''.join(map(str,m.canonical((x,y,f['a'],b,c)))))
      Qs[j][row][i]+=1
  for b,p,h in left:
   for x,y,r in right:
    ff=dict(f,b=b,p=p,h=h,x=x,y=y,r=r)
    for j,op in enumerate(ops):
     if not all(ff[v]!=ff[w] for v,w in op['added_edges']):continue
     item['S_complete_lifts'][j].append((b,p,h,x,y,r))
     row=m.ROWS.index(''.join(map(str,m.canonical(tuple(ff[v] for v in op['boundary'])))))
     Ss[j][row][i]+=1
  fac=factorial(4-len(set(word)))
  for M in Qs+Ss:
   for row in M:assert row[i]%fac==0;row[i]//=fac
  caps.append(item)
 # First five seven-rim completions must exactly reproduce the old H frames.
 assert Ss[:5]==Hs
 return ten,C,Hs,Qs,Ss,ops,{'original_and_H_caps':oldcaps,'Q_and_S_caps':caps}

class Closure:
 def __init__(self,K,size):
  self.K=K;self.size=size;self.full=(1<<size)-1;self.rowbits=[0]*size
  for r,i in enumerate(K['rowids']):self.rowbits[i]|=1<<r
  self.cols=[(sum(1<<i for i in {K['rowids'][r] for r,v in col}),
              sum(1<<r for r,v in col)) for col in K['columns']]
 def close(self,seed):
  live=sum(1<<i for i in seed);rounds=[]
  while True:
   dead=self.full^live;covered=0
   for cb,rb in self.cols:
    if not cb&dead:covered|=rb
   bad=[]
   for i in range(self.size):
    if not live>>i&1:continue
    missing=self.rowbits[i]&~covered
    if missing:bad.append([i,(missing&-missing).bit_length()-1])
   if not bad:return [i for i in range(self.size) if live>>i&1],rounds
   rounds.append(bad);live^=sum(1<<i for i,r in bad)

def projection(M,live):return sum(1<<r for r,row in enumerate(M) if any(row[i] for i in live))
def record(cl,seed,C,Hs,Qs,Ss):
 live,rounds=cl.close(seed)
 return {'initial':len(seed),'live':live,'rounds':rounds,'original_upper':projection(C,live),
         'H_uppers':[projection(M,live) for M in Hs],
         'Q_uppers':[projection(M,live) for M in Qs],
         'S_uppers':[projection(M,live) for M in Ss]}
def support_possible(rec,supports):
 return rec['original_upper']==941 and all(not(s&~u) for s,u in zip(supports,rec['H_uppers']))

def compute():
 inputs=authority();m=load(MODEL,'frozen_model');old=load(OLD,'frozen_five_caps')
 ten,C,Hs,Qs,Ss,ops,caps=matrices(m,old);K=m.kempe(10,ten);cl=Closure(K,len(ten))
 initial=[i for i in range(len(ten)) if all(not C[r][i] for r in (1,4,6))]
 general=record(cl,initial,C,Hs,Qs,Ss);live=general['live']
 assert len(initial)==2141 and len(live)==1881
 # Independent original list/set closure agreement checks the optimized bitset replay.
 assert (live,general['rounds'])==m.close(K,initial)
 catalogue=sorted(map(int,json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())['cells']))
 joint=[]
 for zb in range(32):
  supports=[1022 if zb>>j&1 else 1023 for j in range(5)]
  seed=[i for i in live if all(not Hs[j][0][i] for j in range(5) if zb>>j&1)]
  rec=record(cl,seed,C,Hs,Qs,Ss);rec.update(zero_bits=zb,supports=supports)
  rec['not_excluded']=support_possible(rec,supports);joint.append(rec)
 survivors=[r['zero_bits'] for r in joint if r['not_excluded']]
 assert survivors==[2,6,10,11,14,26,27,30]
 branches=[]
 for zb in (26,27,30):
  jr=joint[zb];base_live=jr['live'];accept_zero=[];comparisons=[]
  for j,N in enumerate(Qs):
   rec=record(cl,[i for i in base_live if not N[9][i]],C,Hs,Qs,Ss)
   assert rec['original_upper']==429
   # Independent list/set closure agreement for the actual acceptance-zero claim.
   assert (rec['live'],rec['rounds'])==m.close(K,[i for i in base_live if not N[9][i]])
   accept_zero.append(rec);allcases=[]
   for support in catalogue:
    seed=[i for i in base_live if all(not N[r][i] for r in range(10) if not support>>r&1)]
    rr=record(cl,seed,C,Hs,Qs,Ss)
    okay=support_possible(rr,jr['supports']) and not(support&~rr['Q_uppers'][j])
    rr.update(hypothesis=support,not_excluded=okay);allcases.append(rr)
   assert [r['hypothesis'] for r in allcases if r['not_excluded']]==[1021]
   comparisons.append(allcases)
  branches.append({'zero_bits':zb,'acceptance_zero':accept_zero,'Q_catalogue_comparisons':comparisons})
 # Stronger direct premise: only H4's literal row01012 is zero. Its closure
 # equals the branch26 closure, without assuming ANY other H positive fibre.
 assert joint[16]['live']==joint[26]['live']
 assert joint[16]['Q_uppers']==[1021,1021]
 for j,cases in enumerate(branches[0]['Q_catalogue_comparisons']):
  compatible=[r['hypothesis'] for r in cases if r['original_upper']==941
              and not(r['hypothesis']&~r['Q_uppers'][j])]
  assert compatible==[1021]
 # Each of the 28 new concrete graphs is compared with all 132 catalogue cells.
 seven=[]
 for j,N in enumerate(Ss):
  allcases=[]
  for support in catalogue:
   seed=[i for i in live if all(not N[r][i] for r in range(10) if not support>>r&1)]
   rr=record(cl,seed,C,[],[],[N]);okay=rr['original_upper']==941 and not(support&~rr['S_uppers'][0])
   rr.update(hypothesis=support,not_excluded=okay);allcases.append(rr)
  possible=[r['hypothesis'] for r in allcases if r['not_excluded']]
  assert possible
  seven.append({'candidate':j,'possible_catalogue_supports':possible,'comparisons':allcases})
 assert seven[24]['possible_catalogue_supports']==[511]
 assert seven[26]['possible_catalogue_supports']==[959]
 # Check whether any one new graph eliminates an old joint pattern. This does
 # not claim simultaneous feasibility of all 28 support choices.
 tests=[]
 for zb in survivors:
  jr=joint[zb];lists=[]
  for j,N in enumerate(Ss):
   possible=[]
   for support in seven[j]['possible_catalogue_supports']:
    seed=[i for i in jr['live'] if all(not N[r][i] for r in range(10) if not support>>r&1)]
    rr=record(cl,seed,C,Hs,[],[N])
    if support_possible(rr,jr['supports']) and not(support&~rr['S_uppers'][0]):possible.append(support)
   assert possible;lists.append(possible)
  tests.append({'zero_bits':zb,'individual_S_support_options':lists})
 # Apply ALL forced zero rows from the 28 support unions to ONE core at once.
 # Every mandatory positive row (intersection of each support option set) is
 # checked on the resulting common live set. No common realization is asserted.
 cases=[(general,[r['possible_catalogue_supports'] for r in seven])]
 cases += [(joint[t['zero_bits']],t['individual_S_support_options']) for t in tests]
 for jr,options in cases:
  unions=[];intersections=[]
  for choices in options:
   union=0;intersection=1023
   for mask in choices:union|=mask;intersection&=mask
   unions.append(union);intersections.append(intersection)
  seed=[i for i in jr['live'] if all(not Ss[j][r][i] for j,u in enumerate(unions)
                                   for r in range(10) if not u>>r&1)]
  jointly_closed,rounds=cl.close(seed)
  assert seed==jr['live'] and jointly_closed==jr['live'] and not rounds
  assert projection(C,jointly_closed)==941
  assert all(not(p&~projection(N,jointly_closed)) for p,N in zip(intersections,Ss))
 cert={'base':BASE,'inputs':inputs,'core_order':old.PINS,'literal_rows':m.ROWS,
  'original_boundary':['x','y','a','b','c'],'source_extra_hypothesis':'d_G(c)=5',
  'Q_operations':[{'candidate':j+1,'boundary':['x','y','a','b','c'],'completed_inner_delta':-4} for j in range(2)],
  'S_operations':ops,'core_states':ten,'original_matrix':C,'H_matrices':Hs,'Q_matrices':Qs,'S_matrices':Ss,
  'complete_caps_sha256':digest(caps),'kempe_columns_sha256':digest(K['columns']),
  'component_columns':len(K['columns']),'general_c5':general,'old_joint_comparisons':joint,
  'H4_zero_branches':branches,'seven_graph_comparisons':seven,'seven_vs_eight_tests':tests,
  'H4_zero_implies_Q_supports':[1021,1021],
  'source_realization_supplied':False,'c5_excluded':False,'strict_smaller_bad_constructed':False,
  'all_28_joint_feasibility_claimed':False}
 return cert,caps

def verify(got,want):
 assert got==want,'complete same-core certificate mismatch'

def negatives(cert,caps):
 mutations=[('cross_candidate_acceptance',lambda z:z['H4_zero_implies_Q_supports'].__setitem__(0,509)),
  ('invent_success',lambda z:z.__setitem__('strict_smaller_bad_constructed',True)),
  ('keep_original_frame',lambda z:z['S_operations'][24].__setitem__('boundary',z['original_boundary'])),
  ('omit_promotion_cost',lambda z:z['S_operations'][24].__setitem__('completed_inner_delta',0)),
  ('claim_source_realization',lambda z:z.__setitem__('source_realization_supplied',True)),
  ('claim_full_joint_feasibility',lambda z:z.__setitem__('all_28_joint_feasibility_claimed',True)),
  ('omit_catalogue_cell',lambda z:z['H4_zero_branches'][0]['Q_catalogue_comparisons'][0].pop()),
  ('drop_zero_closure_round',lambda z:z['H4_zero_branches'][0]['acceptance_zero'][0]['rounds'].pop())]
 out=[]
 for name,mutate in mutations:
  z=copy.deepcopy(cert);mutate(z)
  try:verify(z,cert)
  except AssertionError:out.append(name)
  else:raise AssertionError('negative accepted '+name)
 z=copy.deepcopy(caps)
 e=next(e for e in z['Q_and_S_caps'] if any(r['Q1_b'] for r in e['Q_by_c']))
 next(r for r in e['Q_by_c'] if r['Q1_b'])['Q1_b'].pop()
 try:verify(z,caps)
 except AssertionError:out.append('drop_complete_quotient_lift')
 else:raise AssertionError('incomplete quotient lift accepted')
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
 cert,caps=compute()
 if args.build:
  for name,obj in (('certificate.json.gz',cert),('cap-lifts.json.gz',caps)):
   with (HERE/name).open('xb') as f:f.write(gzip.compress(packed(obj),mtime=0))
 assert gzip.decompress((HERE/'certificate.json.gz').read_bytes())==packed(cert)
 assert gzip.decompress((HERE/'cap-lifts.json.gz').read_bytes())==packed(caps)
 print(json.dumps({'pass':True,'base':BASE,'H4_zero_implies_Q_supports':cert['H4_zero_implies_Q_supports'],
  'H4_literal_01012_zero_suffices':True,
  'accept_zero_original_uppers':[[r['original_upper'] for r in b['acceptance_zero']] for b in cert['H4_zero_branches']],
  'seven_completions':28,'S24_support_exactly':511,'S26_support_exactly':959,
  'joint_forced_zero_closures_tested':9,'new_zeros_from_joint_forced_rows':0,
  'c5_excluded':False,'strict_smaller_bad_constructed':False,
  'negative_controls_rejected':negatives(cert,caps)},sort_keys=True))
if __name__=='__main__':main()
