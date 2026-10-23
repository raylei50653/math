#!/usr/bin/env python3
"""Exclusive-create paper-derived complete-star restrictions; no disk search."""
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
SIX = 'audits/2026-10-23-941-gamma8-six-equality-6b09cd4/certificate.json'
CELLS = 'audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json'
INNER = ['r', 'T', 's', 'tau', 'a', 'y', 'b']
KBOUND = ['d', 'p_d', 'U', 'p_x', 'x', 'zeta']


def paper_links(core):
    common = dict(T=['r', 'tau', 's', 'b', 'y', 'a'])
    if core == 'L':
        return dict(common, a=['r','T','y','p_d','d'], b=['s','T','y','U','p_x'],
                    y=['a','T','b','U','p_d'], r=['d','zeta','tau','T','a'],
                    s=['T','tau','x','p_x','b'])
    return dict(common, a=['r','T','y','U','p_d'], b=['s','T','y','p_x','x'],
                y=['a','T','b','p_x','U'], r=['T','tau','d','p_d','a'],
                s=['x','zeta','tau','T','b'])


def fibres():
    lifts = [[ring, center, ring, other, other, ring, other]
             for ring, other in [(1,3),(3,1)] for center in (0,2)]
    mask = ['0'] * 4**7
    for lift in lifts:
        index = 0
        for color in lift:
            index = 4 * index + color
        mask[index] = '1'
    return [dict(ordered_boundary=KBOUND, literal_boundary_word=word,
                 ordered_inner=INNER, complete_assignment_mask=''.join(mask),
                 full_lifts=sorted(lifts), empty_assignments=4**7-4)
            for word in ([0,2,0,2,0,2], [2,0,2,0,2,0])]


def main():
    prior = json.loads((HERE/'frozen'/SIX).read_text())
    cells = json.loads((HERE/'frozen'/CELLS).read_text())
    actual = [c for c in cells['candidates'] if c['classification']=='local_necessary_type']
    cases, survivors, b_rows = [], [], []
    for cell in actual:
        row = next(r for r in prior['empty_M2_five_point_cases']
                   if r['cell']==cell['id'] and not r['U_equals_d'])
        links = paper_links(cell['core']) if cell['core']!='O' else None
        for ylink in row['complete_y_links']:
            keep = links is not None and ylink == links['y']
            cases.append(dict(cell=cell['id'], core=cell['core'], complete_y_link=ylink,
                complete_a_b_links=[dict(a=links['a'],b=links['b'])] if keep else [],
                classification='necessary_joint_star_row' if keep else
                    ('O_previously_excluded' if cell['core']=='O' else 'excluded_complete_star_join')))
        if links is None:
            continue
        survivors.append(dict(cell=cell['id'], core=cell['core'], complete_stars=links,
            complete_original_M=['T'], complete_original_N=['a','b','r','s','tau','y'],
            complete_original_K_cycle=KBOUND,
            required_U_F_link_arc=['p_d','y','b','p_x'] if cell['core']=='L' else ['p_d','a','y','p_x'],
            U_arc_allows_reversal=True, U_F_link_is_not_cyclic=True,
            literal_K6_fibres=fibres()))
        for e_identity, connector in product(('private','V'), ('c','e','h')):
            if e_identity=='V' and connector=='e':
                continue
            b_rows.append(dict(cell=cell['id'], e_identity=e_identity, unique_W_q_connector=connector,
                shortest_original_B13_V_Y_path=['V','W',connector,'q','Y'],
                classification='necessary_B13_tree_row'))
    certificate = dict(schema='941-gamma8-empty-m2-v1', base=BASE,
        complete_predecessor_certificate=prior, joint_link_cases=cases,
        complete_star_survivors=survivors, necessary_B13_tree_rows=b_rows,
        paper_contract=dict(j=2, full_M2_empty=True, original_T_degree=6,
            exterior_private_points=5, same_original_graph_and_literal_frame=True,
            E_may_be_rootless=True, full_stars_and_rotation_retained=True,
            U_is_only_rootless_star_frame_exception=True,
            d_not_U=True, h_not_c=True, W_not_q=True, original_V_W_edge=True,
            e_not_Y=True, E_rootless=True, exact_B13_connector=True,
            no_complete_U_cyclic_star_assumption=True),
        authority_boundaries=dict(finite_control='triggered and holds', source_realizability='not triggered',
            conditional_L_R_complete_star_rows=8, eleven_type_exclusions=0,
            remaining_exterior_completion='OPEN', general_wrong_side='OPEN',
            common_k_lower_bound=23, new_Lean=False, new_LP=False, smaller_bad=False))
    with (HERE/'certificate.json').open('x') as f:
        json.dump(certificate,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(dict(status='CREATED',joint_link_cases=len(cases),complete_star_rows=len(survivors),B13_tree_rows=len(b_rows))))


if __name__=='__main__':
    main()
