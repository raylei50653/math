#!/usr/bin/env python3
"""Exclusive-create a finite contract certificate; never enumerate source disks."""
from copy import deepcopy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = 'audits/2026-10-23-three-mask-round2-cb8f859/941/certificate.json'
B14 = ['a','z1','z2','z3','z4','V','U','HL_0','q','c','s','v','w','t']
BASE = 'cb8f8593e273a7426ecadd59797a6e643cc4768e'


def make():
    prior = json.loads((HERE/'frozen'/PREV).read_text())
    rows = []
    for old in prior['source_rows']:
        e0,e1 = (0,1) if old['target']==44459 else (1,0)
        initial = dict(zip(B14,[0,3,0,3,0,1,0,1,3,1,2,e0,e1,2]))
        successor = {**initial,'U':2}
        blocks = old['full_03_successor_boundary_contacts']
        named = {label:next(b for b in blocks if contact in b)
                 for label,contact in [('A03','a'),('C12','U'),('Q03','q'),('D12','c')]}
        bridges = []
        for gate in old['complete_initial_01_gate']:
            big = next(b for b in gate if 'U' in b)
            former = [v for v in B14 if initial[v]==0 and v!='U' and v in big]
            last = [v for v in former if v in named['Q03']]
            bridges.append(dict(complete_initial_01_contacts=gate,
                predecessor_first_bridge_boundary_candidates=former,
                last_C_bridge_boundary_candidates=last,
                canonical_last_bridge_forced_private=(not last)))
        rows.append(dict(target=old['target'],initial_02_type=old['initial_02_type'],
            initial_03_type_choices=old['initial_03_type_choices'],
            complete_predecessor_record=deepcopy(old),original_boundary_colors=initial,
            whole_K_successor_boundary_colors=successor,complete_successor_boundary_components=named,
            forced_tree_path=['A03','C12','Q03','D12'],
            original_edges_for_tree_path=[['z4','V'],['HL_0','q'],['q','c']],
            full_A_D_anticomplete=True,
            last_bridge=dict(quantifier='last C vertex on each shortest actual original01 U-to-c path',
                original_color=0,outside_complete_K=True,actual_successor_03_component='Q03',
                old_first_bridge_is_not_reidentified=True,all_original_2_neighbors_outside_K=True,
                all_original_3_neighbors_in_complete_Q=True,private_degree5_multiset=[1,1,2,3,3],
                private_degree_at_least6_retained=True,boundary_classification=bridges),
            type4_only_joint_X=dict(requires_initial_03_type=4,private_X_color=3,
                X_in_complete_original_B13=True,X_in_actual_successor_A03=True,
                X_T_nonedge=True,X_anticomplete_to_full_D12=True,
                any_actual_original_B13_X_to_q_path_visits=['A03','C12','Q03'],
                selected_R_color=1,selected_R_in_complete_B13_and_C12=True,
                R_may_be_V_or_Y=True,R_is_not_identified_with_01_bridge_neighbors=True,
                T_original_02_component_is_not_identified_with_L=True),pair_excluded=False))
    return dict(schema='941-round3-certificate-v1',base=BASE,
        scope='same F ordinary short Type-I; initial02 13/36; complete whole-K successor',
        full_component_trees_include_all_rootless_components=True,
        arbitrary_private_size_bound=None,degree5_sides_both_retained=True,degree_at_least6_retained=True,
        source_realized=False,new_pair_exclusions=0,new_smaller_bad=False,new_Lean=False,
        original_941_source_control='not triggered',finite_disk_survival_controls_added=0,
        paper_status='conditional arbitrary-size same-source lemmas; not Lean formalized',
        source_rows=rows,upstream_complete_fibre_custody=deepcopy(prior['upstream_complete_fibre_custody']))


if __name__=='__main__':
    with (HERE/'certificate.json').open('x') as stream:
        json.dump(make(),stream,sort_keys=True,separators=(',',':'))
        stream.write('\n')
