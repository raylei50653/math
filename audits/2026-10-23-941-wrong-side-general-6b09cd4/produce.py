#!/usr/bin/env python3
"""Write the one fixed control certificate once; no source enumeration."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
base='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
B=[
 dict(name='boundary_b_equals_c',endpoint_b='c',b_is_c=True,colors=dict(Y=1,q=3,c=1,a=3,u=1,d=3,V=1),edges=[['Y','q'],['q','c'],['Y','a'],['a','u'],['u','d'],['d','V']],unavoidable_Y_b_vertices=['q'],color3_unavoidable_vertices=['q']),
 dict(name='private_B_cutpoint_rootless_tail',endpoint_b='b',b_is_c=False,colors=dict(Y=1,q=3,c=1,V=1,a=3,u=1,d=3,t=1,w=3,b=1),edges=[['Y','q'],['q','c'],['Y','a'],['a','u'],['u','d'],['d','V'],['q','t'],['t','w'],['w','b']],unavoidable_Y_b_vertices=['q','t','w'],color3_unavoidable_vertices=['q','w']),
 dict(name='alternative_B_path_avoids_q',endpoint_b='b',b_is_c=False,colors=dict(Y=1,q=3,c=1,V=1,a=3,u=1,w=3,b=1),edges=[['Y','q'],['q','c'],['q','b'],['Y','a'],['a','u'],['u','w'],['w','b'],['w','V']],unavoidable_Y_b_vertices=[],color3_unavoidable_vertices=[]),
]
C=[
 dict(name='C_literal01_bridge',colors=dict(r=1,u=2,a=1,k0=2,b1=1,v=2,e=1),edges=[['r','u'],['u','a'],['a','k0'],['k0','b1'],['b1','v'],['v','e']],r_e_bridges=[['r','u'],['u','a'],['a','k0'],['k0','b1'],['b1','v'],['v','e']]),
 dict(name='C_cycle_has_no_r_e_bridge',colors=dict(r=1,u=2,e=1,v=2),edges=[['r','u'],['u','e'],['r','v'],['v','e']],r_e_bridges=[]),
]
W=[
 dict(name='boundary_q_all_F_faces_inside',q_is_boundary_corner=True,coordinates=dict(Y=[-3,0],q=[0,-3],c=[3,0],v=[3,4],t=[-3,4],w=[-1,1],x=[1,1]),colors=dict(Y=1,q=3,c=1,v=2,t=3,w=2,x=0),boundary=['Y','q','c','v','t'],Gamma=['Y','q','c','x','w'],actual_faces=[['q','Y','w'],['q','w','x'],['q','x','c'],['t','Y','w'],['t','w','x'],['t','x','c'],['t','c','v']],incident_q_face_inside_labels=[True,True,True]),
 dict(name='interior_q_requires_boundary_premise',q_is_boundary_corner=False,coordinates=dict(Y=[-2,0],q=[0,0],c=[2,0],top=[0,2],bottom=[0,-2]),colors=dict(Y=1,q=3,c=1,top=0,bottom=0),boundary=['Y','bottom','c','top'],Gamma=['Y','q','c','top'],actual_faces=[['q','Y','top'],['q','top','c'],['q','c','bottom'],['q','bottom','Y']],incident_q_face_inside_labels=[True,True,False,False]),
]
c=dict(schema='941-wrong-side-general-v1',base=base,scope=dict(finite_calibration='triggered and holds',source_control='not triggered',source_realized=False,initial_pair_exclusions=0,smaller_bad=False,new_Lean=False,Gamma_length_bound=None,E_may_be_rootless=True,Wstar_may_equal_q=True,repeated_P_S_meetings_retained=True,general_wrong_side='OPEN'),paper_claims=['fixed_S_inside_centers_independent_of_L','opposite_side_shared01_is_C_r_e_bridge','opposite_side_shared13_is_same_e_Wstar','exact_two_shared_b3_separates_all_B_intersection_C_from_b','exact_two_b_equals_c_excludes_shared_b3','h_equals_c_implies_b_equals_c_only'],B13_controls=B,C12_controls=C,wedge_controls=W)
with (HERE/'certificate.json').open('x') as f:json.dump(c,f,ensure_ascii=False,indent=2,sort_keys=True);f.write('\n')
print('created fixed calibration certificate; no source instance')
