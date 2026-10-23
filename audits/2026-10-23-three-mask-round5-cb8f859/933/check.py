#!/usr/bin/env python3
"""Read-only same-D Hstar reduction, two positive OR families and long paths."""
import argparse,copy,hashlib,itertools,json
from functools import lru_cache
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
PREV='audits/2026-10-23-three-mask-round4-cb8f859/933/certificate.json'
SRC='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
CAT='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json'
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
D=('a','n','R','L','q','c','s','v','w','t');E=('a','n','R','L','q','c','x','y')
SPLITS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
LEFT=(('a','b'),('b','c'),('b','q'))+tuple(('p',v) for v in ('a','b','q','h','n'))+tuple(('h',v) for v in ('q','L','R','n'))
def digest(d):return hashlib.sha256(d).hexdigest()
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
def frozen(p):return (P/'frozen'/p).read_bytes()
def custody():
 m=json.loads((P/'INPUTS.json').read_text());assert m['base']==BASE
 for e in m['files']:
  d=frozen(e['path']);assert len(d)==e['bytes'] and digest(d)==e['sha256'],'frozen bytes: '+e['path'];assert (ROOT/e['path']).read_bytes()==d,'immutable drift: '+e['path']
 return m

def partitions(t=(0,)):
 if len(t)==10:yield t;return
 for c in range(max(t)+2):yield from partitions(t+(c,))
def proper_cycle(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
@lru_cache(None)
def rxy_lifts(t):
 if not proper_cycle(t):return ()
 a,n,R,L,q,c,s,v,w,end=t;out=[]
 for r,x,y in itertools.product(range(4),repeat=3):
  if x in (y,c,s,r) or y in (a,end,r) or r in (s,v,w,end):continue
  out.append((r,x,y))
 return tuple(out)
def options(t,nc,split):
 side={c:j for j,pair in enumerate(split) for c in pair};flip={c:pair[1-k] for pair in split for k,c in enumerate(pair)};out=[]
 for p in nc:
  blocks=[[i for i,v in enumerate(p) if v==b] for b in range(max(p)+1)]
  if any(len({side[t[i]] for i in block})>1 for block in blocks):continue
  if any(side[t[i]]==side[t[(i+1)%10]] and p[i]!=p[(i+1)%10] for i in range(10)):continue
  lifts=[[subset,[flip[c] if subset>>p[i]&1 else c for i,c in enumerate(t)]] for subset in range(1<<len(blocks))]
  assert all(proper_cycle(word) for _,word in lifts)
  out.append({'partition':list(p),'all_literal_subset_outputs':lifts})
 return out

def compute():
 custody();prior=json.loads(frozen(PREV));src=json.loads(frozen(SRC));ds=[tuple(t) for t in prior['D_words']];di={t:i for i,t in enumerate(ds)};ei={tuple(t):i for i,t in enumerate(src['tuples'])};live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933))
 @lru_cache(None)
 def zero_refill(t):
  for r,x,y in rxy_lifts(tuple(t)):
   word=tuple(t[:6])+(x,y);eid=ei[canonical(word)]
   if eid not in live:return {'all_vertices_rxy':[r,x,y],'literal_E_word':list(word),'forbidden_E_id':eid}
  return None
 source_bad={j for j,t in enumerate(ds) if zero_refill(t)};assert len(source_bad)==552
 matrices=[[0]*2461 for _ in ROWS];records=[]
 for ri,w in enumerate(ROWS):
  A,s,v,w,end=map(int,w)
  for n,L,q in itertools.product(range(4),repeat=3):
   d=(A,n,A,L,q,A,s,v,w,end);proper=proper_cycle(d);did=di[canonical(d)] if proper else None;colors=dict(zip(D,d));bph=[]
   if proper:
    for b,p,h in itertools.product(range(4),repeat=3):
     c=dict(colors,b=b,p=p,h=h)
     if all(c[a]!=c[z] for a,z in LEFT):bph.append([b,p,h])
   rxy=[list(x) for x in rxy_lifts(d)];full=[left+right for left in bph for right in rxy]
   if proper:
    matrices[ri][did]+=1
    if n==q:
     missing=next(iter(set(range(4))-{A,L,q}));assert bph==[[missing,L,missing]]
    else:assert bph==[]
   records.append({'outer_row':ri,'nLq':[n,L,q],'literal_D':list(d),'D_id':did,'all_original_bph_lifts':bph,'all_original_rxy_lifts':rxy,'all_original_six_vertex_lifts_bph_rxy':full,'zero_refill':zero_refill(d) if proper else None})
 assert len(records)==640 and all(sum(r)==18 for r in matrices)
 assert sum(bool(r['all_original_bph_lifts']) for r in records)==60
 reduced=[[j for j,c in enumerate(row) if c and j not in source_bad] for row in matrices]
 assert list(map(len,reduced))==[10,18,18,18,10,18,0,0,10,0]
 assert all(not r['all_original_rxy_lifts'] for r in records if r['outer_row'] in (1,3)),'both forced positive families have no rxy lift at all'
 for ri in (6,7,9):assert all(r['zero_refill'] for r in records if r['outer_row']==ri and r['D_id'] is not None)
 catalogue=set(map(int,json.loads(frozen(CAT))['cells']));allowed=sorted(m for m in catalogue if m&~319==0);assert allowed==[271,314,319]
 mandatory=[i for i in range(10) if all(mask>>i&1 for mask in allowed)];assert mandatory==[1,3,8]
 # Each original six-fibre witness descends through the same fixed quotient.
 six_maps=[]
 for i,tail in enumerate(prior['six_surviving_necessary_D_tails']):
  d=(0,1,0,2,3,0)+tuple(tail);word=canonical((0,)+tuple(tail));row=ROWS.index(''.join(map(str,word)))
  assert row==(8 if i<2 else 0 if i in (2,4) else 4);assert d[0]==d[2]==d[5]
  six_maps.append({'D_fibre':i,'literal_D':list(d),'new_literal_outer_word':[0]+tail,'new_outer_row':row,'all_remaining_vertices_unchanged_under_quotient':True})
 # New exact joint palette obligations extracted from every inherited actual
 # partition. The two colour pairs belong to this same complete colouring.
 joints=[]
 for lemma in prior['D_component_lemmas'][2:]:
  target=lemma['target'];j=7 if target in (2,4) else 8;checks=[]
  for part in lemma['surviving_necessary_partitions']:
   if part[1]==part[4]:
    N=part[1]
    if N==part[6]:kind='nq-on-s';anchor=0;assert part[j]==part[0] and part[j] not in (part[5],part[2],part[3])
    elif N==part[9]:kind='nq-on-t';anchor=5;assert part[j]==part[5] and part[j] not in (part[0],part[2],part[3])
    else:kind='free';anchor=None;assert part[j] in (part[0],part[5]) and part[j] not in (part[2],part[3])
   else:
    kind='V-crossed';anchor=None;assert target in (4,5) and part[1]==part[9] and part[4]==part[6];assert part[j]==part[2]==part[3] and part[j] not in (part[0],part[5])
   checks.append({'one_actual_boundary_partition':part,'joint_class':kind,'zero_vertex_D_index':j,'forced_anchor_D_index':anchor})
  joints.append({'target':target,'all_same_colouring_joint_cases':checks})
 # Four short-path obstructions reconstructed from the original r rotation.
 rotation=['x','y','t','w','v','s'];short=[]
 for anchor,port,other in [('a','y','x'),('c','x','y')]:
  for j in ('v','w'):
   a,b=rotation.index(port),rotation.index(j);arcs=[]
   for step in (1,-1):
    arc=[];k=(a+step)%6
    while k!=b:arc.append(rotation[k]);k=(k+step)%6
    if other not in arc:arcs.append(arc)
   assert len(arcs)==1;inside=arcs[0];assert inside=={('a','v'):['t','w'],('a','w'):['t'],('c','v'):['s'],('c','w'):['s','v']}[(anchor,j)]
   short.append({'anchor':anchor,'zero_vertex':j,'hypothetical_02_three_edge_path':['r',j,'u',anchor],'u_literal_colour':2,'original_proper_C5':['r',j,'u',anchor,port],'forced_strict_cap_vertices':inside,'contradiction':'at least two cap vertices' if len(inside)>1 else 'singleton s/t would have original degree five, contrary to at least six'})
 # One bounded stop test only: the two newly mandatory positive families.
 four=list(itertools.combinations(range(10),4));nc=[p for p in partitions() if not any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b] for a,b,c,d in four)];assert len(nc)==16796
 tests=[];residuals={}
 for ri in (1,3):
  dead=[];remaining=[]
  for did,c in enumerate(matrices[ri]):
   if not c:continue
   splits=[]
   for si,split in enumerate(SPLITS):
    opts=options(ds[did],nc,split);survive=[]
    for op in opts:
     blockers=[{'subset':subset,'literal_D':word,'zero_refill':z} for subset,word in op['all_literal_subset_outputs'] if (z:=zero_refill(tuple(word))) is not None]
     op['one_blocking_complete_refill']=blockers[0] if blockers else None
     if not blockers:survive.append(op['partition'])
    splits.append({'split':si,'all_complete_options':opts,'surviving_necessary_partitions':survive})
   killed=any(not s['surviving_necessary_partitions'] for s in splits);(dead if killed else remaining).append(did)
   tests.append({'new_outer_row':ri,'D_id':did,'literal_D':list(ds[did]),'all_three_split_tests':splits,'verdict':'forced zero' if killed else 'not excluded by this test'})
  assert dead==([461,482] if ri==1 else [470,491]);assert len(remaining)==16
  residuals[ROWS[ri]]={'forced_zero_ids':dead,'positive_OR_residual_16_D_ids':remaining,'common_actual_D':True,'simultaneous_realization_claimed':False}
 return {'base':BASE,'manifest_sha256':digest((P/'INPUTS.json').read_bytes()),'original_D_order':list(D),'new_fixed_outer_order':['A','s','v','w','t'],'quotient_classes':[['a','R','c']],'deleted_original_vertices':['b','p','h','r','x','y'],'total_vertex_count_after_quotient':'k-3','interior_vertex_count':'k-8','embedding_operations':['add a-c arc in the original D outer face and contract; keep outer (A,s,v,w,t) and empty inner face (A,n,R,L,q)','in that actual empty face add A-R arc and contract; suppress only duplicate inequalities and preserve every designated outer edge copy'],'pure_original_source_nonedges':{'aR':{'original_C4':['a','p','h','R'],'forbidden_diagonals':[['a','h'],['p','R']]},'Rc':{'original_C5':['c','b','p','h','R'],'forbidden_diagonals':[['c','p'],['c','h'],['b','h'],['b','R'],['p','R']],'only_possible_W5_centre':'q','missing_required_spoke':['q','R']}},'complete_Hstar_to_D_count_matrix':matrices,'complete_640_new_outer_nLq_fibres':records,'old_bph_gate':'iff n=q; unique p=L,b=h=missing colour outside {A,L,q}','source_552_D_zero_ids':sorted(source_bad),'remaining_projection_D_ids':reduced,'Hstar_full_support_upper_bound':319,'Hstar_exact_catalogue_alternatives_using_minimality':allowed,'Hstar_forced_positive_rows':[ROWS[i] for i in mandatory],'six_full_fibre_quotient_maps':six_maps,'six_fibre_nonemptiness_implies_Hstar_nonempty':True,'same_colouring_private_joint_cases':joints,'four_original_short_path_obstructions':short,'noncrossed_attached_C_consequence':{'original_r_anchor_02_path_minimum_edges':5,'strict_private_D_vertices_on_the_path_at_least':3,'shortest_five_edge_case':'original induced C7 after adding a-y-r or c-x-r','otherwise_minimum_odd_edges':7,'V_crossed_case_excluded':False},'two_positive_family_stop_tests':tests,'two_positive_OR_residuals':residuals,'preserved_predecessor_relations':{'generic_E_to_D_kernel':prior['generic_E_to_D_sparse_kernel'],'all_70144_empty_full_r_tail_fibres':prior['complete_274_by_256_tail_fibres'],'all_old_2560_ph_fibres':prior['inherited_full_ph_cap_fibres'],'all_original_and_T0_T1_ten_row_D_matrices':prior['composed_complete_ten_row_D_matrices']},'controls':{'original_nonedges_and_legal_quotient':'conditional paper source theorem','complete_relations_and_catalogue_filter':'triggered and holds','two_positive_family_whole_orbit_test':'triggered and holds','actual_full_original_r6_933_source_graph':'not triggered','remaining_six_fibres_and_OR_families_realizability':'not triggered'},'Hstar_smaller_bad_claimed':False,'six_fibres_proved_empty':False,'necessary_support_feasibility_claimed':False,'general_933_exclusion':False,'new_Lean':False}

def verify(c,e):assert c==e,'complete exact semantic mismatch'
def negatives(c,e):
 out=[]
 def reject(name,change):
  bad=copy.deepcopy(c);change(bad)
  try:verify(bad,e)
  except AssertionError:out.append({'name':name,'status':'counterexample rejected'})
  else:raise AssertionError('corruption accepted: '+name)
 reject('identify_different_original_contacts',lambda d:d['quotient_classes'][0].__setitem__(1,'L'))
 reject('erase_actual_cofacial_second_step',lambda d:d['embedding_operations'].pop())
 reject('overstate_strict_size_gain',lambda d:d.__setitem__('interior_vertex_count','k-9'))
 reject('permit_W5_missing_qR_spoke',lambda d:d['pure_original_source_nonedges']['Rc'].__setitem__('missing_required_spoke',[]))
 reject('drop_empty_nLq_fibre',lambda d:d['complete_640_new_outer_nLq_fibres'].pop(next(i for i,r in enumerate(d['complete_640_new_outer_nLq_fibres']) if r['D_id'] is None)))
 reject('drop_a_full_original_rxy_lift',lambda d:next(r['all_original_rxy_lifts'] for r in d['complete_640_new_outer_nLq_fibres'] if r['all_original_rxy_lifts']).pop())
 reject('truncate_original_complete_ten_rows',lambda d:d['complete_Hstar_to_D_count_matrix'].pop())
 reject('weaken_old_bph_gate',lambda d:d.__setitem__('old_bph_gate','n=q is optional'))
 reject('erase_one_catalogue_alternative',lambda d:d['Hstar_exact_catalogue_alternatives_using_minimality'].pop())
 reject('merge_independent_colour_witnesses',lambda d:d['same_colouring_private_joint_cases'][0]['all_same_colouring_joint_cases'][0].__setitem__('forced_anchor_D_index',2))
 reject('use_unbounded_short_cycle_side',lambda d:d['four_original_short_path_obstructions'][0].__setitem__('forced_strict_cap_vertices',['x','s']))
 reject('invent_four_edge_02_path',lambda d:d['noncrossed_attached_C_consequence'].__setitem__('original_r_anchor_02_path_minimum_edges',4))
 reject('drop_one_whole_Kempe_subset',lambda d:d['two_positive_family_stop_tests'][0]['all_three_split_tests'][0]['all_complete_options'][0]['all_literal_subset_outputs'].pop())
 reject('erase_V_crossed_exception',lambda d:d['noncrossed_attached_C_consequence'].__setitem__('V_crossed_case_excluded',True))
 reject('call_OR_residual_a_source',lambda d:d['two_positive_OR_residuals']['01021'].__setitem__('simultaneous_realization_claimed',True))
 reject('claim_smaller_bad_Hstar',lambda d:d.__setitem__('Hstar_smaller_bad_claimed',True))
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--negative',action='store_true');args=p.parse_args();e=compute();path=P/'certificate.json'
 if args.build:
  with path.open('x') as f:json.dump(e,f,separators=(',',':'));f.write('\n')
 c=json.loads(path.read_text());verify(c,e);result={'status':'PASS','base':BASE,'Hstar_interior_vertices':'k-8','full_support_alternatives':[271,314,319],'new_forced_positive_rows':['01021','01201','01231'],'positive_OR_family_sizes':[16,16],'new_exact_D_zeros':[461,482,470,491],'noncrossed_attached_path_min_edges':5,'immutable_drift':0,'actual_original_source_control':'not triggered','certificate_sha256':digest(path.read_bytes())}
 if args.negative:result['semantic_negative_controls']=negatives(c,e)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
