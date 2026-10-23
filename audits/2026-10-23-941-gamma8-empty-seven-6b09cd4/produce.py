#!/usr/bin/env python3
"""Exclusive-create a narrow empty-seven paper contract and frozen inputs."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
SOURCES=[
 'audits/2026-10-23-941-types-wrong-side-round5-6b09cd4/REPORT.md',
 'audits/2026-10-23-941-types-wrong-side-round5-6b09cd4/PROOF.md',
 'audits/2026-10-23-941-gamma8-empty-resource-stars-6b09cd4/PROOF.md',
 'audits/2026-10-23-941-gamma8-empty-k-stars-6b09cd4/PROOF.md',
 'audits/2026-10-23-941-gamma8-empty-k-stars-6b09cd4/certificate.json',
 'audits/2026-10-23-941-gamma8-chi-six-6b09cd4/PROOF.md',
 'audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json',
 'audits/2026-10-23-941-types-wrong-side-6b09cd4/CAP_RELATION-v2.json',
 'audits/2026-10-23-941-gamma8-k6-exterior-6b09cd4/PROOF.md',
 'audits/2026-10-21-w7-I-joint-2c38d1d/geometry/PROOF.md',
]
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as f:json.dump(value,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
def main():
 rows=[]
 for name in SOURCES:
  raw=(ROOT/name).read_bytes();target=HERE/'frozen'/name;target.parent.mkdir(parents=True,exist_ok=True)
  with target.open('xb') as f:f.write(raw)
  rows.append(dict(path=name,snapshot=str(target.relative_to(HERE)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 write(HERE/'INPUTS.json',dict(schema='941-empty-seven-inputs-v1',base=BASE,authority=rows))
 relation=json.loads((HERE/'frozen'/SOURCES[7]).read_text())
 certificate=dict(
  schema='941-empty-seven-v1',base=BASE,
  source_contract=dict(M2_empty=True,same_original_graph=True,same_rotation=True,same_literal_frame=True,complete_original_components=True,all_attachments_retained=True,arbitrary_spectators=True,K_sole_frame_contact='U'),
  rim_faces=dict(every_rim_edge_has_actual_opposite_face=True,q_original_colors=[0,2],q_pairwise_distinct=True,no_T_q_edge=True,no_K_assumption_for_general_q=True,available_non_Z_02=['d','x','zeta','U'],outside_T_link_N_count='D-3'),
  all_D_bound=dict(minimum_even_D=6,resource_lower_bound='2*D-7',alias_d_U_resource_lower_bound='2*D-6',spectator_lower_bound=1,D8_min_resource=9,D8_min_exterior=10,D8_alias_min_resource=10,D8_alias_min_exterior=11),
  seven_resource_D6=dict(extra_resources=2,forbidden_extra_02_outside_K=True,extra_02_max_rim_neighbors=2,extra_02_max_other_neighbors=1,extra_02_degree_upper_bound=3,minimum_original_degree=5,remaining_extra_identities=['K0','K2','N1','N3'],no_new_13_component=True),
  both_K=dict(maximum_actual_K=8,possible_collar_lengths=[6,8],collar6='excluded by frozen same-H four-candidate reduction',remaining_collar_length=8,remaining_alias_d_U=False,remaining_extra_colors=[0,2],all_actual_K_on_collar=True,N_degree_patterns=[[5,5,5,5,5,7],[5,5,5,5,6,6]],sealed_inner_vertices=7,K8_edges=34,K8_faces=20),
  same_candidate=dict(choose_once_from_actual_01232=True,all_three_rejected_rows_one_H=True,rejected_rows=['01021','01202','01212'],all_same_original_exterior=True,quotient_pullback=True,k6_k_drops=[7,7,9,9]),
  complete_retained_K6_relation=relation,
  boundaries=dict(finite_control='triggered and holds',full_source_realizability='not triggered',paper_D8_Z7_and_Z8='excluded',paper_D6_extra_other_02='excluded',paper_D6_bothK_same_color_or_d_equals_U='excluded',paper_D6_mixed_or_twoN='OPEN',paper_D6_bothK_K8='OPEN',empty_M2_min_exterior=8,full_eleven_types='OPEN',general_wrong_side='OPEN',common_k=23,new_Lean=False,new_matching=False,new_K8_replacement=False))
 write(HERE/'certificate.json',certificate)
if __name__=='__main__':main()
