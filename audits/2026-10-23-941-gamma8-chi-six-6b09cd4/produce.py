#!/usr/bin/env python3
"""Exclusive-create paper tables; checker independently reconstructs actual graphs."""
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
KB=['d','p_d','U','p_x','x','zeta'];INNER=['r','T','s','tau','a','y','b']

def read(p):return json.loads((HERE/'frozen'/p).read_text())

def canonical(w):
    d={};return tuple(d.setdefault(c,len(d)) for c in w)

def main():
    cells=read('audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json')['candidates']
    old=read('audits/2026-10-23-941-types-wrong-side-round2-6b09cd4/reduction-certificate.json')
    caps=read('audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json')['caps']
    ys=[['a','T','b',*tail] for tail in [['U','p_d'],['p_d','U'],['U','p_x'],['p_x','U'],['p_d','U','p_x'],['p_x','U','p_d']]]
    templates=dict(L=dict(y=['a','T','b','U','p_d'],a=['r','T','y','p_d','d'],b=['s','T','y','U','p_x'],cap='L'),
        R=dict(y=['a','T','b','p_x','U'],a=['r','T','y','U','p_d'],b=['s','T','y','p_x','x'],cap='R'))
    stars=[]
    for cell in cells:
        if cell['classification']!='local_necessary_type':continue
        for chi,alias in product((2,3),(False,True)):
            joins=[templates[cell['core']]] if cell['core'] in templates and not alias else []
            stars.append(dict(cell=cell['id'],core=cell['core'],chi_color=chi,U_equals_d=alias,
                complete_y_links=[] if alias else ys,joint_star_rows=joins,
                status='sealed_K6_required' if joins else 'excluded_star_join'))
    caprows=[]
    for cap in caps:
        caprows.append(dict(core=cap['core'],ordered_boundary=KB,ordered_inner=INNER,
            normalized_rows=[dict(word=r['word'],full_lifts=r['complete_original_lifts'][cap['core']]) for r in old['relation']],
            vertices=cap['vertices'],original_edges=cap['edges'],oriented_actual_faces=cap['oriented_actual_faces']))
    graphs=[]
    for parity in (0,1):
        p=list(range(parity,6,2));tag='even' if parity==0 else 'odd'
        for kind in ('triangle','identify'):
            previous=next(g for g in old['candidates'] if g['id']==tag+'_'+kind)
            relation=set()
            for w in product(range(4),repeat=6):
                proper=all(w[i]!=w[(i+1)%6] for i in range(6))
                color_count=len({w[i] for i in p})
                if proper and color_count==(3 if kind=='triangle' else 1):relation.add(w)
            graphs.append(dict(id=kind+'_'+tag,port_map=previous['vertex_map'],edges=previous['edges'],
                k_drop=previous['completed_interior_saving'],
                normalized_support=[list(w) for w in sorted({canonical(w) for w in relation})],
                complete_literal_relation=''.join('1' if w in relation else '0' for w in product(range(4),repeat=6))))
    result=dict(schema='941-gamma8-chi-six-v1',base=BASE,
        paper_contract=dict(Gamma_interior_points=2,full_M2_empty=True,T_degree=6,exterior_private_points=6,
            chi_original_color_options=[2,3],chi_anticomplete_full_rootless_J_minus_K_branch=True,
            same_original_graph_rotation_and_literal_frame=True,U_F_link_is_not_complete_cyclic_star=True),
        complete_star_cases=stars,exact_K6_caps=caprows,four_reduction_graphs=graphs,
        authority_boundaries=dict(finite_control='triggered and holds',source_realizability='not triggered',
            paper_excluded_branch='empty_M2_T6_X6',paper_empty_M2_minimum_exterior=7,
            paper_all_eleven_minimum_exterior=7,eleven_entire_type_exclusions=0,common_k_lower_bound=23,
            empty_M2_seven_exterior='OPEN',general_wrong_side='OPEN',new_Lean=False,new_LP=False))
    with (HERE/'certificate.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(dict(status='CREATED',star_cases=len(stars),caps=2,reduction_graphs=4)))

if __name__=='__main__':main()
