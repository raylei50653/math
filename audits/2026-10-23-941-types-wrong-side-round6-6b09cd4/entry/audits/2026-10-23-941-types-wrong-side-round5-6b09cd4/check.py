#!/usr/bin/env python3
"""Read-only custody and connection check for the fifth-round source proof."""
import argparse,copy,hashlib,json
from pathlib import Path
import transfer_caps
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def custody():
 inputs=load(HERE/'INPUTS.json');require(inputs['base']==BASE,'BASE')
 routing={r['path']:r for r in inputs['inputs'] if r['authority']=='routing-entry'}
 for r in inputs['inputs']:
  paths=[HERE/r['snapshot']]+([] if r['authority']=='routing-entry' else [ROOT/r['path']])
  for p in paths:
   b=p.read_bytes();require((len(b),hashlib.sha256(b).hexdigest())==(r['bytes'],r['sha256']),'entry authority drift '+str(p))
 prior=load(HERE/'entry/audits/2026-10-23-941-types-wrong-side-round4-6b09cd4/FINAL_MANIFEST.json')
 for r in prior['entries']:
  p=HERE/routing[r['path']]['snapshot'] if r['path'] in routing else ROOT/r['path'];b=p.read_bytes()
  require((len(b),hashlib.sha256(b).hexdigest())==(r['bytes'],r['sha256']),'round4 artifact drift '+r['path'])
 transfer_caps.custody()
 return dict(round4_entries=len(prior['entries']),entry_authorities=len(inputs['inputs']),immutable_drift=0)
def expected():
 transfer=load(HERE/'cap-transfer-certificate.json');out=transfer_caps.reconstruct();transfer_caps.verify(transfer,out)
 c=load(ROOT/'audits/2026-10-23-941-gamma8-nonempty-k-stars-6b09cd4/certificate.json')
 require(c['relaxed_complete_N_star_rows']==transfer_caps.read(transfer_caps.NEW),'same literal shared star table')
 actual=set(c['necessary_complete_N_star_row_ids']);covered={r['row'] for r in out if r['kind']=='old_cap'}
 require(len(actual)==480 and actual<=covered,'all refined source rows have old-cap transfer')
 e=load(ROOT/'audits/2026-10-23-941-gamma8-empty-k-stars-6b09cd4/certificate.json')
 require(e['boundaries']['empty_M2_min_resource']==7 and e['boundaries']['empty_M2_min_exterior']==8,'empty branch source boundary')
 return dict(schema='941-k-collar-round5-v1',base=BASE,
  source_domain='original_G_F_Gamma8_j2_eleven_necessary_types',
  empty=dict(M2_empty=True,resource_lower_bound=7,exterior_lower_bound=8,reduction='old_sealed_seven_inner_K6_four_candidate',arbitrary_spectators=True),
  nonempty=dict(resource_seven_omega_remaining=['N1','N3'],K0_K2_excluded=True,relaxed_star_rows=563,child_source_necessary_rows=480,independent_transfer_superdomain=513,exterior_lower_bound=8),
  common_eleven_type_exterior_lower_bound=8,non_single_M2_exterior_lower_bound=10,
  same_candidate=dict(one_actual_accepted_witness=True,one_H_for_all_three_rejections=True,complete_fibres_and_full_lifts_preserved=True),
  authority=dict(finite_control='triggered and holds',source_realizability='not triggered',eleven_types='OPEN',general_wrong_side='OPEN',common_k=23,W7_excluded_profiles=38,W7_total_profiles=40,new_Lean=False,new_LP=False,new_matching=False,general_smaller_bad='OPEN'))
def verify(c,e):require(c==e,'integrated source contract mismatch')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--produce',action='store_true');ap.add_argument('--negative',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');a=ap.parse_args();frozen=custody();e=expected()
 if a.produce:
  with a.certificate.open('x') as f:json.dump(e,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
 c=load(a.certificate);verify(c,e);neg=[]
 if a.negative:
  for name,mutate in [('drop_N3_remaining',lambda x:x['nonempty']['resource_seven_omega_remaining'].pop()),('claim_entire_11_exclusion',lambda x:x['authority'].update(eleven_types='excluded')),('change_common_k',lambda x:x['authority'].update(common_k=24)),('rowwise_candidates',lambda x:x['same_candidate'].update(one_H_for_all_three_rejections=False)),('forget_spectators',lambda x:x['empty'].update(arbitrary_spectators=False)),('weaken_new_common_bound',lambda x:x.update(common_eleven_type_exterior_lower_bound=7))]:
   bad=copy.deepcopy(c);mutate(bad)
   try:verify(bad,e)
   except ValueError:neg.append(name)
   else:raise ValueError('negative accepted '+name)
 print(json.dumps(dict(status='PASS',custody=frozen,empty_resource=7,empty_exterior=8,common_eleven_exterior=8,nonempty_remaining=['N1','N3'],child480_covered_by_independent513=True,negative_rejected=neg),sort_keys=True))
if __name__=='__main__':main()
