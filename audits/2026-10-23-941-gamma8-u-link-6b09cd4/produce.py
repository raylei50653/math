#!/usr/bin/env python3
"""Exclusive-create the paper's complete-star restrictions; no disk search."""
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = 'audits/2026-10-23-941-gamma8-six-equality-6b09cd4/certificate.json'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'


def rows(cells):
    result = []
    for cell in cells:
        core = cell['core']
        ri = ['d','zeta','tau','T'] if core == 'L' else ['d','tau','T']
        si = ['T','tau','zeta','x'] if core == 'R' else ['T','tau','x']
        for family in ['A-short-v','A-long-v','B','C']:
            for nx in ([False,True] if core == 'R' else [False]):
                ul = {'A-short-v':['n','m','v','U','p_x'],
                      'A-long-v':['n','m','v','U','p_x'],
                      'B':['n','m','v','p_d','U'],
                      'C':['n','m','v','p_d','U','p_x']}[family]
                nl = ['s','T','m','u'] + (['U'] if family == 'B' else []) + ['p_x'] + (['x'] if nx else [])
                vl = {'A-short-v':['r','m','u','U','p_d'],
                      'A-long-v':['r','m','u','U','p_d','d'],
                      'B':['r','m','u','p_d','d'],
                      'C':['r','m','u','p_d','d']}[family]
                rl = ri + ['m','v'] + (['p_d'] if family == 'A-short-v' else [])
                sl = si + ([] if nx else ['p_x']) + ['n']
                pd = {'A-short-v':['d','r','v','U'],
                      'A-long-v':['d','v','U'],
                      'B':['d','v','u','U'],
                      'C':['d','v','u','U']}[family]
                px = ['x'] + ([] if nx else ['s']) + ['n'] + ([] if family == 'B' else ['u']) + ['U']
                un = {'A-short-v':['p_d','v','u','p_x'],
                      'A-long-v':['p_d','v','u','p_x'],
                      'B':['p_d','u','n','p_x'],
                      'C':['p_d','u','p_x']}[family]
                result.append(dict(cell=cell['id'],core=core,family=family,n_x_edge=nx,
                    full_links=dict(u=ul,n=nl,v=vl,r=rl,s=sl),
                    exit_N_arcs=dict(p_d=pd,p_x=px),U_N_arc=un))
    return sorted(result,key=lambda r:(r['cell'],r['full_links']['u'],r['full_links']['n'],r['full_links']['v']))


def b_models():
    out=[]
    for ev,hc in product([False,True],repeat=2):
        if ev and hc: continue  # missing opposite full M2 separator
        e='V' if ev else 'e';h='c' if hc else 'h'
        choices=['c'] if hc else (['h','c'] if ev else ['e','h','c'])
        for z in choices:
            edges={tuple(sorted(p)) for p in [('W','V'),('W',e),('W',h),('q','Y'),('q','c'),('W',z),('q',z)]}
            out.append(dict(e_equals_V=ev,h_equals_c=hc,bridge=z,
                vertices=sorted({'V','Y','q','c','W',e,h}),edges=sorted([list(p) for p in edges]),
                shortest_V_Y_path=['V','W',z,'q','Y']))
    return out


def main():
    previous=json.loads((HERE/'frozen'/PREV).read_text())
    c=previous['complete_predecessor_certificate']
    for _ in range(3):c=c['complete_predecessor_certificate']
    cells=[r for r in c['candidates'] if r['classification']=='local_necessary_type']
    result=dict(schema='941-gamma8-u-link-v1',base=BASE,
        complete_predecessor_certificate=previous,star_restrictions=rows(cells),B_models=b_models(),
        U_F_link_contract=dict(endpoints=['V','Y'],
            permitted_V_arms=[['V'],['V','W'],['V','W','e']],
            Y_arm=['Y'],exit_orders=[['p_d','p_x'],['p_x','p_d']],
            e_V_alias_drops_third_arm=True,exit_other_arcs_are_paths_in_same_B_model=True,
            exit_original_degrees_at_least_five=True,unknown_B_paths_not_claimed_feasible=True),
        paper_contract=dict(same_original_graph_and_literal_frame=True,j=2,
            M2_nonempty=True,exterior_private_count=6,M_equals=['T','m'],
            m_side='C',d_not_U=True,W_not_q=True,e_not_Y=True,
            complete_original_B_has_only_W_q_color3=True,
            E_may_be_rootless=True,full_fibres_and_lifts_preserved=True),
        authority_boundaries=dict(finite_control='triggered and holds',
            source_realizability='not triggered',eleven_type_exclusions=0,
            full_exterior_disk='OPEN',general_wrong_side='OPEN',
            common_k_lower_bound=23,new_Lean=False,new_LP=False,smaller_bad=False))
    with (HERE/'certificate.json').open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(dict(status='CREATED',complete_star_restrictions=len(result['star_restrictions']),B_models=len(result['B_models']))))


if __name__=='__main__':main()
