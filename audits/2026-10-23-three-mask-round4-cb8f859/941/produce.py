#!/usr/bin/env python3
"""Exclusive certificate creation; no source graph enumeration."""
from copy import deepcopy
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PREV='audits/2026-10-23-three-mask-round3-cb8f859/941/certificate.json'
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'


def negative_graph():
    return dict(name='K0_not_one_successor12_component',
        colors=dict(U=0,r=1,q=3,s=1,x=0,z=2,h=3,j=1),
        boundary=['U','r','q','s','h','j'],
        faces=[['z','U','r'],['z','r','q'],['z','q','s'],['z','s','x'],
               ['s','h','x'],['x','h','z'],['h','j','z'],['z','j','U']],
        complete_K=['U','x','z'],complete_K_boundary_contacts=['U'],
        successor12_component_of_U=['U','j','r'],K0_outside_that_component=['x'],
        original941_source_control='not triggered',
        purpose='counterexample to inferring one successor12 component from full original02 connectivity')


def main():
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    rows=[]
    for original in prior['source_rows']:
        rows.append(dict(target=original['target'],initial_02_type=original['initial_02_type'],
            complete_predecessor_record=deepcopy(original),
            initial03_choices=deepcopy(original['initial_03_type_choices']),
            all_boundary_components_in_JminusK_B_side=True,
            rootless_branches_retained=True,T_original02_component_not_assumed_L=True,
            last_original_K_exit=dict(next_original1_in_complete_B=True,
                next_original1_successor12_component='actual E_prime, not assumed C'),
            branch_implication=dict(premise='M02(T) outside B component of J minus K',
                wrong_side_T_private=True,original01_tail_returns_K0=True,
                return_K0_in_Q_side_of_HminusC=True,
                canonical_Z=dict(quantifier='last C exit on an actual K02 path from U to a tail-return x',
                    original_color=2,private=True,in_complete_K=True,in_actual_successor_Q=True,
                    two_path_neighbors_original0_in_K=True,
                    first_path_neighbor_in_C=True,second_path_neighbor_outside_C=True,
                    all_original0_neighbors_in_K=True,all_original3_neighbors_in_complete_Q=True,
                    at_least_two_original0_and_two_original3_neighbors=True,
                    degree5_neighbor_multiset=[0,0,1,3,3],
                    unique_original1_successor12_sides=['C','outside_C'],
                    degree_at_least6_retained=True,no_original1_even_degree_at_least6_retained=True)),
            type4_joint=dict(requires_initial03_type=4,requires_wrong_original_T_side=True,
                X_T_Z_distinct_private=True,three_original_nonedges=[['X','T'],['X','Z'],['T','Z']],
                original_B13_path_R_still_in_C=True,R_not_identified_with_r_or_s=True,
                R_distinct_from_u_and_s=True),
            pair_excluded=False))
    c=dict(schema='941-round4-certificate-v1',base=BASE,
        scope='same F ordinary short Type-I; initial02 13/36; original T branch versus marked private insertion Z',
        source_rows=rows,upstream_complete_fibre_custody=deepcopy(prior['upstream_complete_fibre_custody']),
        arbitrary_private_size_bound=None,all_original_X_T_degree_sides_retained=True,
        initial03_type9_has_no_X_R_triple_lemma=True,new_pair_exclusions=0,
        source_realized=False,new_smaller_bad=False,new_Lean=False,
        full941_source_and_wrong_side_trigger='not triggered',
        finite_disk_survival_controls_added=0,negative_graph_control=negative_graph())
    with (HERE/'certificate.json').open('x') as f:
        json.dump(c,f,sort_keys=True,separators=(',',':'));f.write('\n')


if __name__=='__main__':main()
