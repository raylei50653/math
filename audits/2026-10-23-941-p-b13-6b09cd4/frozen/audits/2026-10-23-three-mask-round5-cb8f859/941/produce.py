#!/usr/bin/env python3
"""Exclusive certificate: eight local rotations and twenty bounded patch schemas."""
from copy import deepcopy
from itertools import combinations,product
import json
from pathlib import Path
P=Path(__file__).resolve().parent
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
PREV='audits/2026-10-23-three-mask-round4-cb8f859/941/certificate.json'
ORDER=(0,2,3,1)
DIAG=((0,3),(2,1))


def rotations():
    out=[]
    for edge in ((0,3),(2,1)):
        rest=sorted(set(range(4))-set(edge))
        for left,right in product(rest,repeat=2):
            arms={}
            for color,offset in ((left,0),(right,2)):
                if offset==0:j,h=(0,1) if color%2==0 else (1,0)
                else:j,h=(3,2) if color%2==0 else (2,3)
                arms[j]='J';arms[h]='H'
            out.append(dict(center_original_colors=list(edge),third_original_colors=[left,right],
                cyclic_zero_arm_labels=[arms[i] for i in range(4)],
                transverse=(left!=right),four_role_patch=(left!=right)))
    return out


def schemas():
    result=[]
    for split in (None,0,1,2,3):
        a={c:f'{c}a' for c in ORDER};b={c:f'{c}b' if c==split else f'{c}a' for c in ORDER}
        for d0,d1 in product(range(2),repeat=2):
            es=set();centers=[];faces=[]
            for vertices,d in ((a,d0),(b,d1)):
                es|={tuple(sorted((vertices[x],vertices[y]))) for x,y in zip(ORDER,ORDER[1:]+ORDER[:1])}
                center=tuple(sorted(vertices[c] for c in DIAG[d]));centers.append(list(center));es.add(center)
                colors=((0,2,3),(0,3,1)) if d==0 else ((0,2,1),(2,3,1))
                faces.extend([[vertices[c] for c in f] for f in colors])
            vs=sorted(set(a.values())|set(b.values()));four=next((list(s) for s in combinations(vs,4) if all(tuple(sorted(e)) in es for e in combinations(s,2))),None)
            blocker=None
            if centers[0]==centers[1]:kind='not_two_distinct_centers'
            elif four is not None:kind='forbidden_original_K4';blocker=dict(vertices=four)
            else:
                kind='forbidden_original_C4_without_diagonals';i=ORDER.index(split)
                p,n=ORDER[(i-1)%4],ORDER[(i+1)%4]
                blocker=dict(cycle=[a[split],a[p],b[split],a[n]],
                    same_color_diagonal=[a[split],b[split]],
                    other_diagonal=[a[p],a[n]],other_diagonal_forbidden_by='would complete original K4')
            result.append(dict(split_original_color=split,diagonal_choices=[d0,d1],
                first_roles={str(c):a[c] for c in ORDER},second_roles={str(c):b[c] for c in ORDER},
                centers=centers,original_edges=[list(e) for e in sorted(es)],
                original_faces=faces,classification=kind,blocker=blocker))
    return result


def main():
    previous=json.loads((P/'frozen'/PREV).read_text());rows=[]
    for r in previous['source_rows']:
        target=r['target']
        rows.append(dict(target=target,initial_02_type=r['initial_02_type'],
            complete_predecessor_record=deepcopy(r),
            applies_initial03_types=[4,9],premise='M02(T) outside B component of J minus K',
            alpha_boundary_edges=[['U','V'],['U','HL_0']],
            beta_boundary_edges=[['HL_0','q'],['v','w'] if target==44459 else ['w','t']],
            marked_K_internal_C_Q_edge=True,beta_ends_outside_alpha_U_side=True,
            at_least_two_transverse_crossings=True,
            patch_roles={'0':'K intersect C','2':'K intersect Q','1':'B intersect C','3':'B intersect Q'},
            patch_cycle_original_colors=[0,2,3,1],patch_center_options=[[0,3],[2,1]],
            center_has_two_original_facial_triangles=True,other_diagonal_original_nonedge=True,
            two_distinct_center_patches_need_at_least_original_vertices=6,
            only_K2_role_forced_private=True,K0_may_equal_U=True,B3_may_equal_q=True,
            patch_K2_not_identified_with_marked_Z=True,patch_B1_not_identified_with_R_or_r=True,
            R_and_r_may_equal_or_differ=True,M_not_identified_with_L=True,
            same_P_last_K_exit_b_in_B_outside_C=True,
            same_B_last_C_bridge_W_in_Q=True,bridge_W_may_be_boundary_q=True,
            X_R_lemmas_require_initial03_type4=True,pair_excluded=False))
    cert=dict(schema='941-round5-certificate-v1',base=BASE,
        scope='ordinary short Type-I initial02 13/36; wrong original T side forces two coupled interface patches',
        source_rows=rows,upstream_complete_fibre_custody=deepcopy(previous['upstream_complete_fibre_custody']),
        local_rotations=rotations(),small_patch_gluings=schemas(),
        source_control='not triggered',finite_calibrations='triggered and holds',
        no_private_size_or_degree_upper_bound=True,original_degree5_sides_and_high_degree_retained=True,
        rootless_and_boundary_tip_retained=True,new_initial_pair_exclusions=0,
        new_smaller_bad=False,new_Lean=False,source_realized=False,finite_source_survival_search=False)
    with (P/'certificate.json').open('x') as f:json.dump(cert,f,sort_keys=True,separators=(',',':'));f.write('\n')


if __name__=='__main__':main()
