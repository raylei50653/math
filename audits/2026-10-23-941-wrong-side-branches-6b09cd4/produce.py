#!/usr/bin/env python3
"""Exclusive fixed branch/cyclic-link controls, never source enumeration."""
from itertools import product
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'

def first_word(kind,n,m):
    for degree in range(2,12):
        for tail in product(range(3),repeat=degree-1):
            word=(1,)+tail
            if any(a==b for a,b in zip(word,word[1:])):continue
            if kind=='cyclic' and word[-1]==word[0]:continue
            if kind=='path' and word[-1]!=1:continue
            pairs=list(zip(word,word[1:]))+([(word[-1],word[0])] if kind=='cyclic' else [])
            if word.count(1)>=n and sum(a!=1 and b!=1 for a,b in pairs)>=m:return degree,list(word)
    raise ValueError('control bound too short')
links=[]
for kind,n in [('cyclic',3),('path',3),('path',4),('path',5)]:
 for m in range(3):
  degree,word=first_word(kind,n,m)
  center=0 if kind=='path' and n==3 else 3
  if center==0:word=[3 if col==0 else col for col in word]
  links.append(dict(kind=kind,original_center_color=center,minimum_color1_neighbors=n,required_distinct_non1_edges=m,minimum_degree=degree,witness_color_word=word,word_is_not_a_source=True))
common=dict(Y=1,q=3,c=1,V=1,a=3,u=1,d=3)
root=[['Y','q'],['q','c'],['Y','a'],['a','u'],['u','d'],['d','V']]
B=[
 dict(name='private_cut_unframed_b_branch',colors=dict(common,f=1,cut=3,b=1),edges=root+[['q','f'],['f','cut'],['cut','b']],cut='cut',C_in_B=['V','Y'],b_component=['b'],c_in_b_component=False,corner_trigger=False,special_Y_q_c_path=None),
 dict(name='q_cut_c_side_now_excluded_conditionally',colors=dict(common,t=3,b=1),edges=root+[['c','t'],['t','b']],cut='q',C_in_B=['V','Y'],b_component=['b','c','t'],c_in_b_component=True,corner_trigger=True,special_Y_q_c_path=['Y','q','c','t','b']),
 dict(name='q_cut_unframed_b_branch_still_necessary',colors=dict(common,b=1),edges=root+[['q','b']],cut='q',C_in_B=['V','Y'],b_component=['b'],c_in_b_component=False,corner_trigger=False,special_Y_q_c_path=None),
]
C=[
 dict(name='U_two_boundary_neighbor_branches_excluded_conditionally',colors=dict(r=1,a=2,V=1,U=2,Y=1,b=2,e=1),edges=[['r','a'],['a','V'],['V','U'],['U','Y'],['Y','b'],['b','e']],r_branch=['V','a','r'],e_branch=['Y','b','e'],corner_trigger=True,special_r_e_path=['r','a','V','U','Y','b','e']),
 dict(name='U_both_branches_avoid_neighbor_frames',colors=dict(r=1,U=2,V=1,Y=1,e=1),edges=[['U','r'],['U','e'],['U','V'],['U','Y']],r_branch=['r'],e_branch=['e'],corner_trigger=False,special_r_e_path=None),
]
record=dict(schema='941-wrong-side-branches-v2',base=BASE,link_controls=links,B13_controls=B,C12_controls=C,
    escape_control=dict(colors=dict(b=1,x=0,c=1,q=3),original_edges=[['b','q'],['c','q'],['b','x'],['x','c'],['q','x']],same_P_tail=['b','x','c'],B13_vertices=['b','c','q'],original_K_vertices=[],root02_label='L0',not_a_source=True),
    paper_claims=['exact_two_shared_b3_b_branch_has_no_B14_contact_including_q_case','private_shared_b3_degree_at_least_6_plus_D0','q_shared_b3_F_degree_at_least_7_plus_D0','q_both_patch_b1_not_Y_F_degree_at_least_9_plus_D0','same_P_tail_has_B_free_01_escape_in_nonK_J_minus_B_branch','opposite_patches_shared_U_r_e_branches_cannot_split_V_Y','opposite_patches_shared_U_F_degree_at_least_5_plus_D0','opposite_patches_shared_U_G_degree_at_least_6_plus_D0'],
    boundaries=dict(source_control='not triggered',finite_calibration='triggered and holds',source_realized=False,general_wrong_side='OPEN',initial_pair_exclusions=0,common_k_lower_bound=23,new_Lean=False,smaller_bad=False,Wstar_may_equal_q=True,E_may_be_rootless=True,U_and_q_use_F_link_paths=True,P_tail_not_assumed_inside_B=True))
with (HERE/'certificate-v2.json').open('x') as f:json.dump(record,f,indent=2,sort_keys=True);f.write('\n')
print('created bounded branch and link calibration')
