#!/usr/bin/env python3
"""Exclusive-create the seven-point conditional sealed-cap inheritance record."""
from copy import deepcopy
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PREV='audits/2026-10-23-941-gamma8-u-link-6b09cd4/certificate.json'
CAPS='audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/EXACT_CAPS.json'


def main():
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    exact=json.loads((HERE/'frozen'/CAPS).read_text())
    cases=[]
    for chi in [2,3]:
        reasons=({0:'different_complete_02',1:'rootless_component_would_be_rooted',2:'same_color',3:'rootless_component_would_be_rooted'}
                 if chi==2 else {0:'rootless_component_would_be_rooted',1:'different_complete_13',2:'rootless_component_would_be_rooted',3:'same_color'})
        for color in range(4):
            cases.append(dict(chi_color=chi,rootless_color=color,adjacency_allowed=False,reason=reasons[color]))
    caps=deepcopy(exact['caps'])
    for cap in caps:
        for rel in cap['relations']:rel['full_lifts'].sort()
    result=dict(schema='941-gamma8-chi-seven-sealed-caps-v1',base=(HERE/'BASE').read_text().strip(),
        paper_domain=dict(j=2,M2_nonempty=True,exterior_private_count=7,same_original_graph=True,literal_frame=True,E_may_be_rootless=True),
        chi_options=[dict(original_color=2,original_component='L02(z4)',successor_component='C12(U)'),dict(original_color=3,original_component='B13(V)',successor_component='A03(a)')],
        entire_rootless_branch_anticompleteness=cases,
        equality_consequences=dict(M2=['m'],M=['T','m'],degree_T=5,degree_m=5,bGamma_m=2,m_side='C',d_not_U=True,U_u_edge=True,
            exterior_private_vertices=['m','n','u','v','p_d','p_x','chi'],
            chi_strictly_outside_sealed_cap=True,chi_anticomplete_cap_interior=True),
        inherited_star_restrictions=deepcopy(prior['star_restrictions']),
        boundary=exact['boundary'],inner=exact['inner'],proper_S4_words=exact['proper_S4_words'],caps=caps,
        predecessor_preservation=dict(complete_fibres_including_empty=True,all_full_lifts=True,frozen_certificate=PREV,
            inherited_scopes=['60_rootless_complete_star_rows','fixed_K2_N_side_arcs','16_sealed_K6_caps'],
            exterior_B_and_full_U_F_link='requires_fresh_join_when_chi3'),
        authority_boundaries=dict(finite_control='triggered and holds',source_realizability='not triggered',paper_result='conditional_sealed_cap_inheritance',
            seven_point_exclusion='requires_separate_safe_replacement',eleven_type_exclusions=0,common_k_lower_bound=23,
            general_wrong_side='OPEN',new_Lean=False,new_LP=False,smaller_bad=False))
    with (HERE/'certificate.json').open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(dict(status='CREATED',chi_adjacency_cases=len(cases),inherited_stars=len(result['inherited_star_restrictions']),caps=len(caps))))

if __name__=='__main__':main()
