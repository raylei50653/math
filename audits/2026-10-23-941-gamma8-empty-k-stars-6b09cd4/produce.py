#!/usr/bin/env python3
"""Exclusive paper-list producer; does not perform the checker's search."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
AUTH=[
 'audits/2026-10-23-941-types-wrong-side-round4-6b09cd4/REPORT.md',
 'audits/2026-10-23-941-gamma8-empty-resource-stars-6b09cd4/PROOF.md',
 'audits/2026-10-23-941-gamma8-empty-resource-stars-6b09cd4/certificate.json',
 'audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json',
 'audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/PROOF.md',
 'audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json',
 'audits/2026-10-23-941-gamma8-k6-exterior-6b09cd4/PROOF.md',
 'audits/2026-10-23-941-types-wrong-side-6b09cd4/CAP_RELATION-v2.json',
 'audits/2026-10-21-w7-I-joint-2c38d1d/geometry/PROOF.md',
 'audits/2026-10-23-941-gamma8-chi-six-6b09cd4/PROOF.md',
]
def write(p,v):
 with p.open('x') as f:json.dump(v,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
def main():
 inputs=[]
 for name in AUTH:
  raw=(ROOT/name).read_bytes();snap=HERE/'frozen'/name;snap.parent.mkdir(parents=True,exist_ok=True)
  with snap.open('xb') as f:f.write(raw)
  inputs.append(dict(path=name,snapshot=str(snap.relative_to(HERE)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 write(HERE/'INPUTS.json',dict(base=BASE,schema='941-empty-k-inputs-v1',authority=inputs))
 rows=[]
 for core in ['L','R']:
  for color,alias,substitutions in [
   (0,False,[{},dict(U='omega')]),(0,True,[dict(U='omega')]),
   (2,False,[{},dict(p_d='omega'),dict(p_x='omega')]),(2,True,[])]:
   for sub in substitutions:
    rows.append(dict(core=core,omega_color=color,U_equals_d=alias,substitution=sub))
 write(HERE/'certificate.json',dict(schema='941-empty-k-collar-v1',base=BASE,
  source_contract=dict(M2_empty=True,T_degree=6,resource_size=6,arbitrary_spectators=True,
   same_original_graph=True,same_rotation=True,same_literal_frame=True,K_sole_frame_contact='U',
   N_cycle=['r','tau','s','b','y','a'],K_available=['d','x','zeta','U','p_d','p_x','omega']),
  wheel_lemma=dict(exterior_edge_face_vertices=6,maximum_actual_K_vertices=7,
   no_K_two_nonconsecutive_N_contacts=True,extra_K_touches_at_most_one_N=True,
   collar_is_simple=True,bipartite_collar=True,collar_length=6,all_N_degrees=5),
  cap_substitutions=rows,
  retained_complete_K6_relation=json.loads((ROOT/AUTH[7]).read_text()),
  same_candidate_reduction=dict(candidates=['Q_even','Q_odd','J_even','J_odd'],
   k_drops=[7,7,9,9],choose_once_from_actual_01232=True,
   rejected_rows=['01021','01202','01212'],all_rows_one_graph_and_frame=True,
   all_exterior_and_attachments_retained=True,quotient_pullback=True),
  boundaries=dict(finite_control='triggered and holds',source_realizability='not triggered',
   paper_empty_M2_D6_Z6='excluded',empty_M2_min_resource=7,empty_M2_min_exterior=8,
   full_eleven_types='OPEN',general_wrong_side='OPEN',common_k=23,new_Lean=False,new_matching=False)))
 print('exclusive paper certificate generated')
if __name__=='__main__':main()
