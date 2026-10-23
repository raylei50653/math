#!/usr/bin/env python3
"""Exclusive-create the paper-derived face obstruction and exact cap relations."""
from copy import deepcopy
import json
from pathlib import Path
import explore_caps

HERE=Path(__file__).resolve().parent
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV='audits/2026-10-23-941-gamma8-u-link-6b09cd4/certificate.json'
SOURCE='audits/2026-10-23-three-mask-round3-cb8f859/941/certificate.json'


def tables(rows):
    out=[]
    for row in rows:
        contacts=row['complete_predecessor_record']['complete_initial_02_contacts']
        colors={('Y' if z=='HL_0' else z):v for z,v in row['original_boundary_colors'].items()}
        L=next(p for p in contacts if 'z4' in p)
        B=next(p for p in contacts if 'V' in p)
        for branch in ['nonempty_M2_six_points','empty_M2_five_points']:
            private={'zeta':(2,'K'),'p_d':(2,'K'),'p_x':(2,'K'),'W':(3,'B'),'tau':(3,'N')}
            private.update({'m':(2,'M'),'n':(3,'N'),'v':(3,'N')} if branch.startswith('nonempty') else {'a':(3,'N'),'b':(3,'N')})
            tested=[]
            for v,c in sorted(colors.items()):
                if c not in [2,3]:continue
                if c==2:
                    why='C_D_merge' if v=='s' else 'wrong_original_02_component'
                else:why='fixed_V_Y_common_neighbor' if v=='q' else 'wrong_original_13_component'
                tested.append(dict(vertex=v,ownership='frame',original_color=c,rejection=why))
            for v,(c,owner) in sorted(private.items()):
                why=('wrong_original_02_component' if c==2 else 'A_Q_merge' if owner=='B' else 'wrong_original_13_component')
                tested.append(dict(vertex=v,ownership=owner,original_color=c,rejection=why))
            out.append(dict(target=row['target'],type02=row['initial_02_type'],branch=branch,
                complete_L_contacts=deepcopy(L),complete_B_contacts=deepcopy(B),
                frame_L2=['s'],frame_B3=['q'],tested_third_points=tested,admissible_third_points=[]))
    return out


def main():
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    rows=json.loads((HERE/'frozen'/SOURCE).read_text())['source_rows']
    caps=explore_caps.caps();words=explore_caps.words()
    for i,cap in enumerate(caps):
        cap['id']=i
        cap['relations']=[dict(word=w,full_lifts=sorted(explore_caps.lifts(cap,w))) for w in words]
        cap['statistics']=dict(vertices=14,edges=33,faces=20,
            nonempty=sum(bool(r['full_lifts']) for r in cap['relations']),
            total_lifts=sum(len(r['full_lifts']) for r in cap['relations']))
    result=dict(schema='941-gamma8-joint-bpaths-v1',base=BASE,
        complete_predecessor_certificate=prior,face_tables=tables(rows),
        forced_face=dict(edge=['z4','V'],original_colors=[0,1],third_color_options=[2,3],
            new_private_options=[dict(color=2,original_component='L02(z4)',successor_component='C12(U)'),
                                 dict(color=3,original_component='B13(V)',successor_component='A03(a)')],
            strict_exterior=True,holds_for_arbitrary_Gamma8_interior=True,E_may_be_rootless=True,
            disjoint_from_all_M2_and_rootless_full_stars_and_K2_exits=True),
        j2_bounds=dict(M2_nonempty_minimum=7,M2_empty_T6_minimum=6,
            full_M2_degree_bound='|M2|+3+d(m)-bGamma(m)',
            adjacent_T_m_bound='D+d(m)-3',nonadjacent_T_v_bound='D+d(v)-1',
            T5_nonsingleton_M2_minimum=9,empty_M2_bound='D',empty_M2_D_even=True),
        exact_K6_caps=caps,proper_S4_boundary_words=words,
        authority_boundaries=dict(finite_control='triggered and holds',source_realizability='not triggered',
            paper_excluded_branches=['M2_nonempty_X6','M2_empty_T6_X5'],
            eleven_type_exclusions=0,general_wrong_side='OPEN',common_k_lower_bound=23,
            partial_B_path_interfaces_are_not_sources=True,new_Lean=False,new_LP=False,smaller_bad=False))
    with (HERE/'certificate.json').open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(dict(status='CREATED',face_tables=len(result['face_tables']),caps=len(caps))))


if __name__=='__main__':main()
