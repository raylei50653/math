#!/usr/bin/env python3
"""Paper-formula producer for a four-candidate same-source K6 reduction."""
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV='audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/certificate.json'
REL='audits/2026-10-23-941-types-wrong-side-6b09cd4/CAP_RELATION-v2.json'


def canonical(word):
    labels={}
    return [labels.setdefault(c,len(labels)) for c in word]


def models():
    cycle=[[i,(i+1)%6] for i in range(6)]
    return [dict(id='triangle_even',port_map=list(range(6)),vertices=list(range(6)),
                 edges=cycle+[[0,2],[2,4],[4,0]],kind='add_three_internal_chords',k_drop=7),
            dict(id='triangle_odd',port_map=list(range(6)),vertices=list(range(6)),
                 edges=cycle+[[1,3],[3,5],[5,1]],kind='add_three_internal_chords',k_drop=7),
            dict(id='identify_even',port_map=[0,1,0,3,0,5],vertices=[0,1,3,5],
                 edges=[[0,1],[0,3],[0,5]],kind='contract_empty_disk_Y_tree',k_drop=9),
            dict(id='identify_odd',port_map=[0,1,2,1,4,1],vertices=[0,1,2,4],
                 edges=[[0,1],[1,2],[1,4]],kind='contract_empty_disk_Y_tree',k_drop=9)]


def main():
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    relation=json.loads((HERE/'frozen'/REL).read_text())
    words=[list(w) for w in product(range(4),repeat=6)
           if canonical(w)==list(w) and all(w[i]!=w[(i+1)%6] for i in range(6))]
    rows=[];masks=[[] for _ in range(4)]
    for w in product(range(4),repeat=6):
        proper=all(w[i]!=w[(i+1)%6] for i in range(6))
        values=[proper and len(set(w[0::2]))==3,proper and len(set(w[1::2]))==3,
                proper and len(set(w[0::2]))==1,proper and len(set(w[1::2]))==1]
        for i,b in enumerate(values):masks[i].append('1' if b else '0')
        if list(w) in words:
            rows.append(dict(word=list(w),candidate_acceptance=values))
    candidates=models()
    for i,row in enumerate(candidates):row['complete_literal_port_relation']=''.join(masks[i])
    certificate=dict(schema='941-gamma8-k6-exterior-reduction-v1',base=BASE,
        complete_predecessor_certificate=prior,complete_predecessor_K6_fibres=relation,
        candidates=candidates,normalized_boundary_rows=rows,
        paper_contract=dict(same_original_graph_and_literal_C5=True,j=2,full_M2_empty=True,
            original_T_degree=6,exterior_private_points=5,all_six_K6_ports_original_C5_private=True,
            sealed_seven_private_vertices=True,choose_candidate_once_from_one_actual_01232_witness=True,
            quotient_coloring_pulled_back_to_same_exterior=True,all_three_rejected_rows_share_same_candidate=True,
            planar_Y_contraction_before_simplifying_parallel_edges=True,no_original_target_target_edge=True,
            no_completion_vertices=True,E_rootless_retained=True,U_only_F_side_link=True,
            normalised_candidate_need_not_preserve_r6_or_degrees=True),
        authority_boundaries=dict(finite_cover='triggered and holds',source_instance_control='not triggered',
            paper_minimal_source_five_point_branch='excluded',minimum_exterior_private_points=6,
            all_eleven_j2_types_minimum_exterior_private_points=6,eleven_type_exclusions=0,
            general_wrong_side='OPEN',common_k_lower_bound=23,new_Lean=False,new_LP=False))
    with (HERE/'certificate.json').open('x') as f:json.dump(certificate,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(dict(status='CREATED',candidates=4,normalized_boundary_words=len(rows))))


if __name__=='__main__':main()
