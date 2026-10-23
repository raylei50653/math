#!/usr/bin/env python3
"""Read-only round4 933 audit: one true C10, complete rxy lifts and bridges."""
import argparse,copy,hashlib,itertools,json
from functools import lru_cache
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
R3='audits/2026-10-23-three-mask-round3-cb8f859/933/certificate.json'
SRC='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
E=('a','n','R','L','q','c','x','y');D=('a','n','R','L','q','c','s','v','w','t')
FACES=(('x','y','r'),('y','t','r'),('t','w','r'),('w','v','r'),('v','s','r'),('s','x','r'),('x','s','c'),('y','a','t'))
EDGES=tuple(sorted({tuple(sorted((u,v))) for f in FACES for u,v in zip(f,f[1:]+f[:1])}))
SPLIT=((0,2),(1,3))
TAILS=((2,1,3,2),(2,3,1,2),(3,0,3,1),(3,1,0,1),(1,0,1,3),(1,3,0,3))

def digest(d):return hashlib.sha256(d).hexdigest()
def canonical(t):
 m={};return tuple(m.setdefault(c,len(m)) for c in t)
def frozen(p):return (P/'frozen'/p).read_bytes()
def custody():
 m=json.loads((P/'INPUTS.json').read_text());assert m['base']==BASE
 for e in m['files']:
  d=frozen(e['path']);assert len(d)==e['bytes'] and digest(d)==e['sha256'],'frozen bytes: '+e['path']
  assert (ROOT/e['path']).read_bytes()==d,'immutable drift: '+e['path']
 return m

def properwords(n,t=(0,)):
 if len(t)==n:
  if t[-1]!=t[0]:yield t
  return
 for c in range(min(4,max(t)+2)):
  if c!=t[-1]:yield from properwords(n,t+(c,))
def partitions(n,t=(0,)):
 if len(t)==n:yield t;return
 for c in range(max(t)+2):yield from partitions(n,t+(c,))
def proper(c,edges):return all(c[u]!=c[v] for u,v in edges)

@lru_cache(None)
def complete_cap(t):
 colors=dict(zip(D,t));out=[]
 if any(t[i]==t[(i+1)%10] for i in range(10)):return ()
 for r,x,y in itertools.product(range(4),repeat=3):
  c=dict(colors,r=r,x=x,y=y)
  if proper(c,EDGES):out.append((r,x,y,tuple(c[v] for v in E)))
 return tuple(out)

def options(t,nc):
 side={c:j for j,pair in enumerate(SPLIT) for c in pair};flip={c:pair[1-k] for pair in SPLIT for k,c in enumerate(pair)};out=[]
 for p in nc:
  blocks=[[i for i,v in enumerate(p) if v==b] for b in range(max(p)+1)]
  if any(len({side[t[i]] for i in block})>1 for block in blocks):continue
  if any(side[t[i]]==side[t[(i+1)%10]] and p[i]!=p[(i+1)%10] for i in range(10)):continue
  lifts=[]
  for subset in range(1<<len(blocks)):
   word=tuple(flip[c] if subset>>p[i]&1 else c for i,c in enumerate(t));assert all(word[i]!=word[(i+1)%10] for i in range(10));lifts.append([subset,list(word)])
  out.append({'partition':list(p),'complete_literal_subset_lifts':lifts})
 return out

def compute():
 custody();src=json.loads(frozen(SRC));prior=json.loads(frozen(R3));ts=[tuple(t) for t in src['tuples']];ei={t:i for i,t in enumerate(ts)}
 assert list(properwords(8))==ts and len(ts)==274
 live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933));forbidden=set(range(274))-live
 assert len(live)==191 and {72,74}<=forbidden
 ds=list(properwords(10));di={t:i for i,t in enumerate(ds)};assert len(ds)==2461
 @lru_cache(None)
 def refill_zero(t):
  for r,x,y,e in complete_cap(tuple(t)):
   eid=ei[canonical(e)]
   if eid in forbidden:return {'rxy':[r,x,y],'literal_E':list(e),'E_id':eid}
  return None
 # Complete generic r lift kernel, retaining each of 274*256 empty/full fibres.
 kernel=[];all_fibres=[]
 for eid,t in enumerate(ts):
  row={};fibres=[]
  for tail in itertools.product(range(4),repeat=4):
   d=t[:6]+tail;did=di.get(canonical(d)) if all(d[i]!=d[(i+1)%10] for i in range(10)) else None
   c=dict(zip(D,d),x=t[6],y=t[7]);lifts=[r for r in range(4) if proper(dict(c,r=r),EDGES)] if did is not None else []
   fibres.append([did,lifts])
   if lifts:row[did]=row.get(did,0)+len(lifts)
  kernel.append(row);all_fibres.append(fibres)
 composed={}
 for name,M in [('G',prior['original_count_matrix']),('T0',prior['candidate_count_matrices'][0]),('T1',prior['candidate_count_matrices'][1])]:
  rows=[]
  for r in M:
   out={}
   for j,c in enumerate(r):
    if c:
     for k,v in kernel[j].items():out[k]=out.get(k,0)+c*v
   rows.append({str(k):v for k,v in sorted(out.items())})
  composed[name]=rows
 # One fixed D prefix, complete all-rxy fibres including the irrelevant empties.
 local=[];relevant=[]
 for tail in itertools.product(range(4),repeat=4):
  t=(0,1,0,2,3,0)+tail;cap=complete_cap(t);records=[[r,x,y,ei[canonical(e)],list(e)] for r,x,y,e in cap];u=sum(x==1 and y==3 for r,x,y,e in cap);v=sum(x==3 and y==1 for r,x,y,e in cap)
  rec={'svwt':list(tail),'all_rxy_lifts':records,'U_lift_count':u,'V_lift_count':v,'zero_refill':refill_zero(t)};local.append(rec)
  if u or v:relevant.append(rec)
 assert len(local)==256 and len(relevant)==24
 killed=[r for r in relevant if r['zero_refill']];survive=[r for r in relevant if not r['zero_refill']]
 assert len(killed)==18 and all(r['zero_refill']['E_id'] in (72,74) for r in killed)
 assert {tuple(r['svwt']) for r in survive}==set(TAILS)
 for i,tail in enumerate(TAILS):
  rec=next(r for r in survive if tuple(r['svwt'])==tail)
  assert (rec['U_lift_count'],rec['V_lift_count'])==((1,1) if i<2 else (1,0) if i<4 else (0,1))
  assert {r[0] for r in rec['all_rxy_lifts']}==({0} if i<2 else {2})
 uid=ei[(0,1,0,2,3,0,1,3)];vid=ei[(0,1,0,2,3,0,3,1)];assert (uid,vid)==(73,76)
 for eid,indices in [(uid,(0,1,2,3)),(vid,(0,1,4,5))]:
  surviving_projection={k:v for k,v in kernel[eid].items() if not refill_zero(ds[k])};assert surviving_projection=={di[(0,1,0,2,3,0)+TAILS[i]]:1 for i in indices}
 # True D complementary components: one actual partition, all its subset swaps.
 four=list(itertools.combinations(range(10),4));nc=[p for p in partitions(10) if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in four)];assert len(nc)==16796
 lemmas=[]
 for i,tail in enumerate(TAILS):
  t=(0,1,0,2,3,0)+tail;opts=options(t,nc);good=[]
  for op in opts:
   blockers=[{'subset':subset,'literal_D':word,'zero_refill':z} for subset,word in op['complete_literal_subset_lifts'] if (z:=refill_zero(tuple(word))) is not None]
   op['one_blocking_complete_refill']=blockers[0] if blockers else None
   if not blockers:good.append(op['partition'])
  expected=(3,3,5,5,6,6)[i];assert len(good)==expected
  if i>=2:
   assert all(p[6]!=p[9] for p in good),'D13 s/t cannot connect'
   for p in good:
    if i in (2,3):assert p[1]==p[4],'U private n/q must be in one D13 component'
    else:assert p[1]==p[4] or (p[1]==p[9] and p[4]==p[6]),'only one V crossed attachment'
    assert not (p[1]==p[4]==p[6]==p[9])
   classes=sorted({('separate' if p[1]==p[4] and p[1] not in (p[6],p[9]) else 's-side' if p[1]==p[4]==p[6] else 't-side' if p[1]==p[4]==p[9] else 'crossed-n-t-q-s') for p in good})
   assert classes==(['s-side','separate','t-side'] if i in (2,3) else ['crossed-n-t-q-s','s-side','separate','t-side'])
  else:classes=[]
  lemmas.append({'target':i,'literal_D':list(t),'all_compatible_component_options':opts,'surviving_necessary_partitions':good,'attachment_classes':classes,'status':'necessary structural conclusion; no realization claim'})
 # The paired A map fixes D pointwise. The free private map flips the one E13
 # component through x,y, i.e. both actual D components of s and t, in full.
 maps=[]
 for i in range(2):
  tail=TAILS[i];colors=dict(zip(D,(0,1,0,2,3,0)+tail),r=0,x=1,y=3);assert {v for v in ('y','c','r','s') if colors[v] in (1,3)}=={'y'};assert {v for v in ('x','a','r','t') if colors[v] in (1,3)}=={'x'}
  maps.append({'kind':'A-pair','target':i,'source_rxy':[0,1,3],'destination_rxy':[0,3,1],'fixed_entire_D_colouring':True,'actual_switched_E13_component':['x','y']})
 for u,v in ((2,4),(3,5)):
  t=(0,1,0,2,3,0)+TAILS[u];target=(0,1,0,2,3,0)+TAILS[v]
  for part in lemmas[u]['surviving_necessary_partitions']:
   if part[1] in (part[6],part[9]) or part[4] in (part[6],part[9]):continue
   changed=tuple(4-c if c in (1,3) and part[i] in (part[6],part[9]) else c for i,c in enumerate(t));assert changed==target
  maps.append({'kind':'free-private-pair','U_target':u,'V_target':v,'premise':'n and q avoid both complete D13 components of s,t','same_actual_D':True,'switch_entire_D13_components_rooted_at':['s','t'],'switch_x_y':True,'private_and_rootless_attachments':'whole actual components included; all other components fixed'})
 return {'base':BASE,'manifest_sha256':digest((P/'INPUTS.json').read_bytes()),'original_E_order':list(E),'actual_D_order':list(D),'actual_D_induced_claimed':False,'original_r_rotation':['x','y','t','w','v','s'],'cap_oriented_faces':[list(f) for f in FACES],'cap_edges':[list(e) for e in EDGES],'source_E_forbidden_ids':sorted(forbidden),'D_words':[list(d) for d in ds],'generic_E_to_D_sparse_kernel':[{str(k):v for k,v in sorted(row.items())} for row in kernel],'complete_274_by_256_tail_fibres':all_fibres,'composed_complete_ten_row_D_matrices':composed,'inherited_full_ph_cap_fibres':prior['complete_local_fibres'],'fixed_prefix_complete_256_tail_fibres':local,'related_D_tuple_count':24,'forced_zero_related_D_tuple_count':18,'six_surviving_necessary_D_tails':[list(t) for t in TAILS],'U_D_targets':[0,1,2,3],'V_D_targets':[0,1,4,5],'D_component_lemmas':lemmas,'complete_component_bijections':maps,'positive_branch':'minimum source: 2A+CU1+CU2+CV1+CV2>0; paired A or free C implies both U,V positive; unilateral leakage requires attached private C','s_x_y_t_E13_edges_all_bridges_on_private_C':True,'conditional_smaller_bad':'only if all six actual complete D fibres vanish','six_D_fibres_realized':False,'necessary_support_feasibility_claimed':False,'general_933_exclusion':False,'smaller_bad_constructed':False,'new_Lean':False,'controls':{'complete_cap_and_original_rotation':'triggered and holds','six_fibre_zero_refill_exclusions':'triggered and holds','actual_component_conditional_bijections':'triggered and holds','full_original_r6_933_source_graph':'not triggered','surviving_D_partitions_realizability':'not triggered'}}

def verify(c,e):assert c==e,'complete exact semantic mismatch'
def negatives(c,e):
 out=[]
 def bad(name,change):
  d=copy.deepcopy(c);change(d)
  try:verify(d,e)
  except AssertionError:out.append({'name':name,'status':'counterexample rejected'})
  else:raise AssertionError('corruption accepted: '+name)
 bad('change_original_r_rotation',lambda d:d['original_r_rotation'].reverse())
 bad('invent_induced_D',lambda d:d.__setitem__('actual_D_induced_claimed',True))
 bad('omit_cap_face',lambda d:d['cap_oriented_faces'].pop())
 bad('retain_only_one_rxy_lift',lambda d:next(r['all_rxy_lifts'] for r in d['fixed_prefix_complete_256_tail_fibres'] if len(r['all_rxy_lifts'])>1).pop())
 bad('omit_empty_tail_fibre',lambda d:d['complete_274_by_256_tail_fibres'][0].pop())
 bad('drop_original_ph_full_lift',lambda d:next(r[6] for r in d['inherited_full_ph_cap_fibres'] if r[6]).pop())
 bad('truncate_ten_row_projection',lambda d:d['composed_complete_ten_row_D_matrices']['T0'].pop())
 bad('drop_whole_D_zero_refill',lambda d:next(r for r in d['fixed_prefix_complete_256_tail_fibres'] if r['zero_refill']).__setitem__('zero_refill',None))
 bad('forget_one_Kempe_subset',lambda d:d['D_component_lemmas'][2]['all_compatible_component_options'][0]['complete_literal_subset_lifts'].pop())
 bad('claim_all_private_U_maps_without_premise',lambda d:d['complete_component_bijections'][2].__setitem__('premise','none'))
 bad('omit_private_or_rootless_attachments',lambda d:d['complete_component_bijections'][2].__setitem__('private_and_rootless_attachments','boundary vertices only'))
 bad('erase_V_crossed_attachment',lambda d:d['D_component_lemmas'][4]['attachment_classes'].remove('crossed-n-t-q-s'))
 bad('call_survivors_realized_sources',lambda d:d.__setitem__('six_D_fibres_realized',True))
 bad('claim_necessary_feasibility',lambda d:d.__setitem__('necessary_support_feasibility_claimed',True))
 bad('claim_smaller_bad',lambda d:d.__setitem__('smaller_bad_constructed',True))
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--negative',action='store_true');args=p.parse_args();e=compute();path=P/'certificate.json'
 if args.build:
  with path.open('x') as f:json.dump(e,f,separators=(',',':'));f.write('\n')
 c=json.loads(path.read_text());verify(c,e);result={'status':'PASS','base':BASE,'complete_generic_tail_fibres':274*256,'related_D_tuples':24,'forced_zero':18,'remaining_necessary_D_fibres':6,'C13_bridge_lemma':True,'unilateral_leakage_requires_attached_private_C':True,'immutable_drift':0,'actual_source_control':'not triggered','certificate_sha256':digest(path.read_bytes())}
 if args.negative:result['semantic_negative_controls']=negatives(c,e)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
