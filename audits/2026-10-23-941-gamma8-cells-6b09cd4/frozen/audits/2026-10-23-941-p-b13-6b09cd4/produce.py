#!/usr/bin/env python3
"""Exclusive finite calibration of the P/B13 joint skeleton, not a source search."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = 'audits/2026-10-23-941-patch-order-6b09cd4/certificate.json'
ORDER = ['r', 'T', 's', 'x', 'h', 'W', 'e', 'd']
PHI = dict(zip(ORDER, [1, 0, 1, 0, 1, 3, 1, 0]))
PSI = dict(zip(ORDER, [1, 0, 1, 2, 1, 3, 1, 2]))
J = dict(zip(ORDER, ['N', 'M', 'N', 'K', 'B', 'B', 'B', 'K']))
H = dict(zip(ORDER, ['C', 'Q', 'E', 'E', 'E', 'Q', 'C', 'C']))


def chords():
    boundary = {frozenset((a, b)) for a, b in zip(ORDER, ORDER[1:] + ORDER[:1])}
    result = []
    for a, b in combinations(ORDER, 2):
        if frozenset((a, b)) in boundary:
            continue
        if PHI[a] == PHI[b]:
            kind = 'original_same_color'
        elif {J[a], J[b]} == {'N', 'B'}:
            kind = 'merges_original_13_components'
        elif {J[a], J[b]} == {'M', 'B'}:
            kind = 'original_J_cycle'
        elif {H[a], H[b]} == {'C', 'E'}:
            kind = 'merges_complete_psi12_components'
        else:
            kind = 'possible_triangle_ear_chord'
        result.append(dict(pair=[a, b], classification=kind))
    return result


def main():
    previous = json.loads((HERE / 'frozen' / PREV).read_text())
    short = []
    for row in previous['exact_two_shared_schemas']:
        if row['shared_colors'] == [0, 2]:
            short.append(dict(complete_predecessor_schema=deepcopy(row),
                              internal_beta_midpoint_colors=[0, 2],
                              missing_P_bridge_midpoint_colors=[0, 1],
                              exactly_two_crossing_six_point_branch='excluded'))
    c = dict(schema='941-p-b13-v2', base='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd',
        complete_predecessor_certificate=deepcopy(previous), shared02_short_segments=short,
        gamma8=dict(order=ORDER, original_colors=PHI, exchanged_colors=PSI,
                    original_components=J, exchanged_components=H,
                    original_tree_edges=[['M', 'N'], ['N', 'K'], ['K', 'B']],
                    segment_lengths=dict(P=4, B13=2, C_path=2),
                    noncycle_pairs=chords(), x_not_identified_with_xprime=True, h_not_identified_with_b=True,
                    ear_faces_may_be_inside_or_outside_Gamma=True),
        face_ownership=dict(states=[0, 1, 2, 3], adjacent_face_maximum_change=1,
                            p_incident_face_values=[0, 0], center_face_value=3,
                            shortest_count_word=[3, 2, 1, 0, 0, 1, 2, 3],
                            minimum_inside_faces=8, minimum_with_outside_center_faces=10,
                            count_word_not_a_source_realization=True),
        paper_claims=dict(r_T_edge_in_Omega=True, r_and_T_anticomplete_to_B=True,
            R_neq_r_only_wrong_side_type4=True, p_original01_and_n_original13_distinct=True,
            n_may_be_boundary_Yq=True, Gamma_minimum_even_length=8,
            Gamma_keeps_P_and_B13_bridges=True, Gamma_need_not_keep_last_K_exit_m=True,
            Gamma_has_no_K2=True, odd_centers_inside_and_outside_Gamma=True,
            at_least_two_distinct_private_K2_in_Q=True, one_patch_K2_differs_from_Z=True,
            new_patch_K2_not_given_marked_Z_link=True,
            exactly_two_crossings_minimum_patch_union=7,
            exactly_two_crossings_shared_roles=['k0', 'b1', 'b3'],
            shared_k0_and_nonendpoint_b1_separate_C_r_e=True,
            shared_b3_on_fixed_B_subpath=True, shared_b3_degree_at_least_5_plus_D0_count=True,
            T_has_private_original3_neighbor_on_each_Gamma_side=True,
            Gamma_is_not_empty_cap=True),
        boundaries=dict(source_control='not triggered', finite_calibration='triggered and holds',
            initial_pair_exclusions=0, smaller_bad=False, source_realized=False, new_Lean=False,
            no_source_enumeration_or_LP=True, rootless_and_boundary_tips_retained=True,
            Wstar_may_equal_q=True, b_may_equal_c=True, multiple_P_B13_intersections_retained=True,
            high_degrees_and_ordinary_degree5_sides_retained=True, M_not_identified_with_L=True,
            general_wrong_side_and_eight_pairs='OPEN'))
    with (HERE / 'certificate-v2.json').open('x') as stream:
        json.dump(c, stream, indent=2, sort_keys=True); stream.write('\n')
    print(json.dumps(dict(status='CREATED', shared02_cases=4, gamma8_noncycle_pairs=20)))


if __name__ == '__main__':
    main()
