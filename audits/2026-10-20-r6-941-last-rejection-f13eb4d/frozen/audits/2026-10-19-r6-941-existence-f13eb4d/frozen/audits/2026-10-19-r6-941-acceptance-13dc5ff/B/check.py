#!/usr/bin/env python3
"""Exact replay of the original n=5,a=6 exclusion and its surviving n=5 control."""
import argparse, copy, hashlib, importlib.util, itertools, json, math
from pathlib import Path
D=Path(__file__).resolve().parent
ROOT=D.parents[2]
BASE='13dc5ff163045c85b5c82dde438eb5f275dab999'
PRIOR='audits/2026-10-19-r6-941-quotients-13dc5ff'
NEEDED=[PRIOR+'/A/model.py',PRIOR+'/A/PROOF.md',PRIOR+'/B/CHORDS.md',PRIOR+'/SOURCE_CONTRACT.md',
 'audits/2026-10-19-r6-941-leakage-b89c591/B/SOURCE_CONTRACT.md',
 'audits/2026-10-19-r6-941-leakage-b89c591/B/CORE.md']
PINS=('a','u','R','L','q','c','s','v','w','t')
LEFT_EDGES=(('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),('p','h'),('p','n'),
 ('h','q'),('h','L'),('h','R'),('h','n'),('n','a'),('n','R'),('n','u'))
RIGHT_EDGES=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),
 ('r','t'),('r','w'),('r','v'),('r','s'))

def sha(v):
 return hashlib.sha256(json.dumps(v,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def authority():
 seal=json.loads((D.parent/'INPUTS.json').read_text());assert seal['base']==BASE
 entries={v['path']:v for v in seal['files']}
 result={}
 for path in NEEDED:
  got=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
  assert got==entries[path]['sha256'],('frozen input drift',path)
  result[path]=got
 return result

def load_model():
 spec=importlib.util.spec_from_file_location('frozen_source_model',ROOT/NEEDED[0]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def interfaces(m):
 ten=[t for t in m.growth(10,four=True) if m.proper(t)];assert len(ten)==2461
 rows={tuple(map(int,w)):j for j,w in enumerate(m.ROWS)}
 M=[[0]*len(ten) for _ in m.ROWS];caps=[]
 for i,word in enumerate(ten):
  f=dict(zip(PINS,word));a,u,R,L,q,c,s,v,w,t=word
  left=[]
  for b,p,h,n in itertools.product(range(4),repeat=4):
   ff=dict(f,b=b,p=p,h=h,n=n)
   direct=all(ff[vv]!=ff[ww] for vv,ww in LEFT_EDGES)
   factor=b not in {a,c,q,p} and p not in {a,q,n,h} and h not in {q,R,L,n} and n not in {a,R,u}
   assert direct==factor
   if direct:left.append([b,p,h,n])
  right=[]
  for x,y,r in itertools.product(range(4),repeat=3):
   ff=dict(f,x=x,y=y,r=r)
   direct=all(ff[vv]!=ff[ww] for vv,ww in RIGHT_EDGES)
   factor=r not in {s,v,w,t,x,y} and x not in {c,s,y} and y not in {a,t}
   assert direct==factor
   if direct:right.append([x,y,r])
  for b,p,h,n in left:
   for x,y,r in right:
    ff=dict(f,b=b,p=p,h=h,n=n,x=x,y=y,r=r)
    assert all(ff[vv]!=ff[ww] for vv,ww in LEFT_EDGES+RIGHT_EDGES)
    frame=m.canonical((x,y,a,b,c));M[rows[frame]][i]+=1
  # A proper C5 word uses at least 3 colours and has trivial S4 stabilizer.
  # Each fixed canonical-core fibre has the (4-d)! permutations of unused
  # core colours acting freely on its complete cap assignments.
  divisor=math.factorial(4-len(set(word)))
  for row in M:
   assert row[i]%divisor==0
   row[i]//=divisor
  caps.append({'core':list(word),'left':left,'right':right,'unused_core_stabilizer':divisor})
 return ten,M,caps

def verify_rounds(K,initial,rounds,live):
 current=set(initial);ri=K['rowids'];columns=K['columns']
 for block in rounds:
  assert len({i for i,r in block})==len(block)
  for i,r in block:
   assert i in current and ri[r]==i
   relevant=[col for col in columns if any(rr==r for rr,v in col)]
   assert relevant
   assert all(any(ri[rr] not in current for rr,v in col) for col in relevant)
  current-={i for i,r in block}
 assert sorted(current)==live
 cover={r for col in columns if all(ri[rr] in current for rr,v in col) for r,v in col}
 assert all(r in cover for r,i in enumerate(ri) if i in current)

def closure(m,K,ten,M,extra_edge):
 source_zero=[i for i in range(len(ten)) if any(M[j][i]>0 for j in (1,4,6))]
 edge_zero=[i for i,t in enumerate(ten) if t[1]==t[9]] if extra_edge else []
 initial=sorted(set(range(len(ten)))-set(source_zero)-set(edge_zero))
 live,rounds=m.close(K,initial);verify_rounds(K,initial,rounds,live)
 upper=[sum(M[j][i] for i in live) for j in range(10)]
 return {'extra_original_edge':['u','t'] if extra_edge else None,'source_reject_zero_core_ids':source_zero,
 'edge_zero_core_ids':edge_zero,'initial':initial,'rounds':rounds,'live':live,
 'source_projection_upper_mask':m.mask(upper),'source_fixed_row_upper_counts':upper,
 'source_alpha_positive_core_ids':[i for i in live if M[9][i]>0],
 'source_alpha_zero':not any(M[9][i] for i in live)}

def reconstruct():
 inputs=authority();m=load_model();ten,M,caps=interfaces(m);K=m.kempe(10,ten)
 assert len(K['columns'])==10798 and len(K['hrows'])==7382
 general=closure(m,K,ten,M,False);branch=closure(m,K,ten,M,True)
 assert [len(v) for v in general['rounds']]==[128,42,8] and len(general['live'])==2005
 assert general['source_projection_upper_mask']==941 and len(general['source_alpha_positive_core_ids'])==36
 assert [len(v) for v in branch['rounds']]==[322,178,81,49,40,26]
 assert len(branch['live'])==756 and branch['source_projection_upper_mask']==429 and branch['source_alpha_zero']
 # Exactly all five empty C5 fillings; only the fan at z avoids a C10 chord.
 polygon=('t','a','n','R','z');possible=((0,2),(0,3),(1,3),(1,4),(2,4))
 triangulations=[]
 for ds in itertools.combinations(possible,2):
  if any(i<k<j<l or k<i<l<j for (i,j),(k,l) in itertools.combinations(ds,2)):continue
  forbidden=[list(e) for e in ds if e not in ((1,4),(2,4))]
  deg=[2]*5
  for i,j in ds:deg[i]+=1;deg[j]+=1
  triangulations.append({'diagonals':[list(e) for e in ds],'forbidden_old_C10_chords':forbidden,'degrees':deg})
 assert len(triangulations)==5
 valid=[x for x in triangulations if not x['forbidden_old_C10_chords']]
 assert len(valid)==1 and valid[0]['degrees'][1:3]==[3,3]
 pocket={'cycle':list(polygon),'empty_fillings':triangulations,'W5_boundary_degrees':[3]*5,
 'both_cases_force_original_degrees':{'a':6,'n':5},'common_neighbour_branch_excluded':True,
 'distance_lower_bound_in_original_G':3,'original_pair':['t','R']}
 cert={'base':BASE,'inputs_sha256':inputs,'scope':'full original r6, p=h=5, support exactly 941',
 'core_order':list(PINS),'source_frame':['x','y','a','b','c'],'words':list(m.ROWS),
 'complete_left_cap_vertices':['b','p','h','n'],'complete_left_cap_edges':[list(e) for e in LEFT_EDGES],
 'complete_right_cap_vertices':['x','y','r'],'complete_right_cap_edges':[list(e) for e in RIGHT_EDGES],
 'literal_source_count_matrix':M,'caps':{'file':'cap-lifts.json','entries':len(caps),'canonical_sha256':sha(caps)},
 'complementary_partition_family':{'H_rows':len(K['hrows']),'columns':len(K['columns']),
 'noncrossing_partitions':K['noncrossing_count'],'literal_rows':K['literal_count'],'columns_sha256':sha(K['columns'])},
 'n5_control':general,'n5_a6_exclusion':branch,'short_pocket':pocket,
 'derived_original_theorems':['n=5 implies a>=7','dist_G(t,R)>=3'],
 'core_interior_count':'k-12','completed_smaller_bad_constructed':False,'main_Q1_Q2_target_proved':False,
 'arbitrary_graph_source_realization_supplied':False}
 return cert,caps

def reject_controls(cert,caps):
 checks=[]
 def reject(name,wrong,right):
  try:assert wrong==right
  except AssertionError:checks.append(name)
  else:raise AssertionError('negative control accepted '+name)
 r=copy.deepcopy(cert);r['complete_left_cap_edges'].remove(['n','u']);reject('omit-original-n-u-edge',r,cert)
 r=copy.deepcopy(caps);i=next(i for i,c in enumerate(r) if c['left']);r[i]['left'].pop();reject('lose-complete-left-lift',r,caps)
 r=copy.deepcopy(cert);r['n5_a6_exclusion']['edge_zero_core_ids']=[];reject('omit-required-original-u-t-edge',r,cert)
 r=copy.deepcopy(cert);r['n5_a6_exclusion']['rounds'][0].pop();reject('truncate-component-deletion-round',r,cert)
 r=copy.deepcopy(cert);r['short_pocket']['W5_boundary_degrees']=[2]*5;reject('forget-original-W5-exception',r,cert)
 r=copy.deepcopy(cert);r['n5_control']['source_alpha_zero']=True;reject('claim-n5-alone-excluded',r,cert)
 r=copy.deepcopy(cert);r['core_interior_count']='k-11';reject('omit-private-n-deletion-cost',r,cert)
 r=copy.deepcopy(cert);r['main_Q1_Q2_target_proved']=True;reject('promote-distance-bound-to-smaller-bad',r,cert)
 return checks

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'certificate.json');args=ap.parse_args()
 cert,caps=reconstruct()
 if args.build:
  for path,value in ((D/'cap-lifts.json',caps),(args.certificate,cert)):
   with path.open('x') as out:json.dump(value,out,ensure_ascii=False,separators=(',',':'));out.write('\n')
 assert json.loads((D/'cap-lifts.json').read_text())==caps,'all complete cap lifts'
 assert json.loads(args.certificate.read_text())==cert,'source matrix, exact zero witnesses, short pockets'
 negative=reject_controls(cert,caps)
 print(json.dumps({'pass':True,'base':BASE,'n5_surviving_core_cells':len(cert['n5_control']['live']),
 'n5_a6_removed_by_round':[len(v) for v in cert['n5_a6_exclusion']['rounds']],
 'n5_a6_source_alpha_zero':True,'derived_original_theorems':cert['derived_original_theorems'],
 'negative_controls_rejected':negative,'main_Q1_Q2_target':'OPEN'},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
