#!/usr/bin/env python3
"""Replay actual component normal forms, short-path pockets, and C11 controls."""
import argparse,copy,hashlib,importlib.util,itertools,json
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
s=importlib.util.spec_from_file_location('interface',D/'interface.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
m=f.m
BASE='13dc5ff163045c85b5c82dde438eb5f275dab999'
PINS=['a','n','R','L','q','c','s','v','w','t']
G_ZERO=(1,4,6)
assert sum(1<<j for j in range(10) if j not in G_ZERO)==941
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def partitions(t,pair):
 side=tuple(int(c in pair) for c in t);out=[]
 for p in f.ncgrowth(10):
  if any(side[i]!=side[j] for i in range(10) for j in range(i) if p[i]==p[j]):continue
  if any(side[i]==side[(i+1)%10] and p[i]!=p[(i+1)%10] for i in range(10)):continue
  if sum(p[i]!=p[(i+1)%10] for i in range(10))!=2*max(p):continue
  out.append(p)
 return out
def normal_forms():
 records=[]
 for name,R,L,pair in [('Q1',3,1,{2,3}),('Q2',2,3,{1,3})]:
  for v,w in [(2,3),(3,2)]:
   t=(0,1,R,L,2,0,1,v,w,1)
   allp=partitions(t,pair)
   forms=[p for p in allp if (p[2]==p[4] if name=='Q1' else p[3] in (p[1],p[9]))]
   if name=='Q1':
    assert len(forms)==2
    for p in forms:
     assert [i for i,x in enumerate(p) if x==p[3]]==[3], 'L complementary component rim singleton'
     assert (p[0]==p[5]) == (p[2]!=p[7]), 'same-colouring complementary dichotomy'
   else:
    assert len(forms)==7
    for p in forms:
     if p[3]==p[1]:assert [i for i,x in enumerate(p) if x==p[2]]==[2], 'Ln path isolates R complementary component'
     if p[3]!=p[1]:assert p[0]==p[2], 'Lt-only component forces aR complementary connection'
   records.append({'zero_acceptance_candidate':name,'literal_core':t,'pair':sorted(pair),'all_triangulated_partition_count':len(allp),'normal_forms':forms})
 return records
def short_pockets():
 # Cycle (endpoint, middle rim point, endpoint, second private, first private).
 # All five triangulations, plus the single-centre W5 exception, are retained.
 chords=[(i,j) for i in range(5) for j in range(i+1,5) if (j-i) not in (1,4)]
 tris=[]
 for es in itertools.combinations(chords,2):
  if any(a<c<b<d or c<a<d<b for (a,b),(c,d) in itertools.combinations(es,2)):continue
  tris.append(es)
 assert len(tris)==5
 records=[]
 for name,colours in [('Q1',(3,1,2,3,2)),('Q2',(3,2,1,3,1))]:
  data=[]
  for es in tris:
   proper=all(colours[i]!=colours[j] for i,j in es)
   induced_ok=(0,2) not in es
   middle_degree=2+sum(1 in e for e in es)
   data.append({'diagonals':es,'proper':proper,'induced_old_rim':induced_ok,'middle_core_degree':middle_degree,'allowed':proper and induced_ok and middle_degree>=4})
  good=[r for r in data if r['allowed']]
  assert len(good)==1 and good[0]['diagonals']==((1,3),(1,4))
  records.append({'branch':name,'cycle_colours':colours,'empty_fillings':data,'W5':{'center_colours':[c for c in range(4) if c not in colours],'middle_core_degree':3,'allowed':False},'forced_middle_original_degree':5,'short_path_private_points':2,'induced_wheel':True})
 return records
def c11():
 states=[t for t in m.growth(11,four=True) if m.proper(t)];K=f.kempe(11,states);ix={t:i for i,t in enumerate(states)}
 records=[]
 for fan,name in [('L','Q1'),('R','Q2')]:
  caps=[f.cap(t,fan) for t in states]
  initial=[i for i,(out,da) in enumerate(caps) if not any(out['G'][j] for j in G_ZERO) and not out[name][9]]
  live,rounds=m.close(K,initial);ls=set(live);short=[]
  for v,w in [(2,3),(3,2)]:
   t=(0,1,3,2,3,2,0,1,v,w,1) if fan=='L' else (0,1,3,1,3,2,0,1,v,w,1)
   i=ix[m.canonical(t)];assert i in ls,'short path boundary survives necessary interface'
   short.append({'literal_C11':t,'canonical_id':i,'survives':True})
  records.append({'fan_center':fan,'zero_acceptance_candidate':name,'cap_counts_sha256':digest(caps),'initial':initial,'rounds':rounds,'live':live,'source_alpha_projection_units':sum(caps[i][0]['G'][9] for i in live),'short_path_boundary_controls':short,'source_realized':False,'branch_excluded':False})
 assert [len(r['live']) for r in records]==[5975,5987]
 return {'source_mask':941,'source_zero_indices':G_ZERO,'source_zero_rows':[m.ROWS[j] for j in G_ZERO],'states':len(states),'literal_states':K['literal_count'],'H_rows':len(K['hrows']),'noncrossing_partitions':K['noncrossing_count'],'columns':len(K['columns']),'columns_sha256':digest(K['columns']),'records':records,'authority':'necessary component support interface only'}
def reconstruct():
 deps=[D/'interface.py',ROOT/'audits/2026-10-19-r6-941-acceptance-13dc5ff/A/PROOF.md',ROOT/'audits/2026-10-19-r6-941-acceptance-13dc5ff/SOURCE_CONTRACT.md',ROOT/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/PROOF.md',ROOT/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py',D.parent/'INPUTS.json']
 return {'base':BASE,'literal_pin_order':PINS,'inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in deps},'actual_component_normal_forms':normal_forms(),'actual_short_path_pockets':short_pockets(),'C11_necessary_interface':c11(),'same_accepting_candidate_three_rejections':'OPEN','strictly_smaller_bad_constructed':False}
def validate(a,e):
 assert a['base']==BASE and a['literal_pin_order']==PINS,'literal source and frame'
 assert a['inputs_sha256']==e['inputs_sha256'],'exact frozen source inputs'
 assert a['actual_component_normal_forms']==e['actual_component_normal_forms'],'complete simultaneous complementary components'
 assert a['actual_short_path_pockets']==e['actual_short_path_pockets'],'all five fillings and W5 exception'
 for r in a['C11_necessary_interface']['records']:
  assert r['source_realized'] is False and r['branch_excluded'] is False,'necessary interface is not source exclusion'
 assert a['C11_necessary_interface']==e['C11_necessary_interface'],'full C11 cap and component closure'
 assert a['same_accepting_candidate_three_rejections']=='OPEN' and not a['strictly_smaller_bad_constructed'],'main authority boundary'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--negative-controls',action='store_true');args=ap.parse_args()
 e=json.loads(json.dumps(reconstruct()));path=D/'certificate.json'
 if args.build:
  with path.open('x') as z:json.dump(e,z,indent=2);z.write('\n')
 a=json.loads(path.read_text());validate(a,e);negative=[]
 if args.negative_controls:
  cases=[('omit-complementary-normal-form',lambda x:x['actual_component_normal_forms'][0]['normal_forms'].pop()),('drop-empty-fan',lambda x:x['actual_short_path_pockets'][0]['empty_fillings'].pop()),('admit-W5-middle-degree3',lambda x:x['actual_short_path_pockets'][0]['W5'].__setitem__('allowed',True)),('false-short-path-at-least-five',lambda x:x['C11_necessary_interface']['records'][0]['short_path_boundary_controls'][0].__setitem__('survives',False)),('truncate-complete-closure',lambda x:x['C11_necessary_interface']['records'][1]['rounds'].pop()),('claim-source-excluded',lambda x:x['C11_necessary_interface']['records'][0].__setitem__('branch_excluded',True)),('change-literal-frame',lambda x:x['literal_pin_order'].reverse()),('wrong-source-zero-indices',lambda x:x['C11_necessary_interface'].__setitem__('source_zero_indices',[0,3,5]))]
  for name,mutate in cases:
   bad=copy.deepcopy(a);mutate(bad)
   try:validate(bad,e)
   except AssertionError as err:negative.append({'name':name,'rejected':True,'reason':str(err)})
   else:raise AssertionError('negative control accepted: '+name)
 print(json.dumps({'pass':True,'actual_normal_form_counts':[len(r['normal_forms']) for r in a['actual_component_normal_forms']],'short_path_forces_original_degree_five_wheel':True,'C11_columns':a['C11_necessary_interface']['columns'],'C11_surviving_counts':[len(r['live']) for r in a['C11_necessary_interface']['records']],'negative_controls':negative,'main_target':'OPEN'},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
