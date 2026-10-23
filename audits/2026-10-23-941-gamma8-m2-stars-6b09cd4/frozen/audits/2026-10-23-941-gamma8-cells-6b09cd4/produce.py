#!/usr/bin/env python3
"""Exclusive-create the twelve fixed Gamma8 two-interior-point candidates."""
from collections import Counter
from copy import deepcopy
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = 'audits/2026-10-23-941-p-b13-6b09cd4/certificate-v2.json'
BOUNDARY = ['r', 'T', 's', 'x', 'h', 'W', 'e', 'd']
VERTICES = BOUNDARY + ['tau', 'zeta']
PHI = dict(zip(VERTICES, [1, 0, 1, 0, 1, 3, 1, 0, 3, 2]))
J = dict(zip(VERTICES, ['N', 'M', 'N', 'K', 'B', 'B', 'B', 'K', 'N', 'K']))
H = dict(zip(VERTICES, ['C', 'Q', 'E', 'E', 'E', 'Q', 'C', 'C', 'Q', 'Q']))
PSI = {v: c ^ 2 if J[v] == 'K' else c for v, c in PHI.items()}


def fan(cycle):
    return [['tau', a, b] for a, b in zip(cycle, cycle[1:] + cycle[:1])]


def fibre(edges, boundary_colors):
    lifts, failures = [], []
    for assignment in product(range(4), repeat=2):
        colors = dict(zip(BOUNDARY, boundary_colors)); colors.update(zip(['tau', 'zeta'], assignment))
        (lifts if all(colors[a] != colors[b] for a, b in edges) else failures).append(list(assignment))
    return dict(boundary_word=boundary_colors, ordered_inner_vertices=['tau', 'zeta'],
                full_lifts=lifts, all_other_inner_assignments=failures)


def candidate(core, ix, id_):
    if core == 'L':
        faces = [['r', 'zeta', 'd']] + fan(['r', 'T', 's', 'x', 'zeta'])
    elif core == 'R':
        faces = [['s', 'x', 'zeta']] + fan(['r', 'T', 's', 'zeta', 'd'])
    else:
        faces = fan(['r', 'T', 's', 'x', 'zeta', 'd'])
    faces += ([['x', 'h', 'W'], ['x', 'W', 'zeta']] if ix else [['x', 'h', 'zeta'], ['h', 'W', 'zeta']])
    faces += ([['d', 'e', 'W'], ['d', 'W', 'zeta']] if id_ else [['d', 'e', 'zeta'], ['e', 'W', 'zeta']])
    faces = sorted([sorted(f) for f in faces])
    edges = sorted({tuple(sorted((a, b))) for f in faces for a, b in zip(f, f[1:] + f[:1])})
    degrees = Counter(v for e in edges for v in e)
    signature = [1 - id_, 1 - ix, int(core == 'L'), int(core == 'R')]
    return dict(id=f'{core}-x{ix}-d{id_}', core=core, inside_ears=dict(xW=ix, dW=id_),
        edges=[list(e) for e in edges], faces=faces,
        full_private_stars={v: sorted(b if a == v else a for a, b in edges if v in (a, b)) for v in ['tau', 'zeta']},
        full_private_degrees={v: degrees[v] for v in ['tau', 'zeta']},
        four_center_D1_signature=signature,
        four_centers=[['d', 'W'] if id_ else ['zeta', 'e'],
                      ['x', 'W'] if ix else ['zeta', 'h'],
                      ['zeta', 'r'] if core == 'L' else ['d', 'tau'],
                      ['zeta', 's'] if core == 'R' else ['x', 'tau']],
        literal_phi_boundary_fibre=fibre(edges, [PHI[v] for v in BOUNDARY]),
        literal_psi_boundary_fibre=fibre(edges, [PSI[v] for v in BOUNDARY]),
        classification='excluded_private_degree4_and_C4' if core == 'O' and ix and id_ else 'local_necessary_type')


def main():
    previous = json.loads((HERE / 'frozen' / PREV).read_text())
    candidates = [candidate(core, ix, id_) for core in ['L', 'R', 'O'] for ix, id_ in product(range(2), repeat=2)]
    c = dict(schema='941-gamma8-cells-v1', base='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd',
        complete_predecessor_certificate=deepcopy(previous), boundary=BOUNDARY,
        original_colors=PHI, exchanged_colors=PSI, original_component_labels=J, exchanged_component_labels=H,
        candidates=candidates,
        exterior_ear_load=dict(private_tip_minimum_degree=5, tip_boundary_neighbors=2,
            max_common_neighbors_of_nonedge=2, already_common_boundary_neighbors=1,
            T_private3_neighbor_not_adjacent_to_e_or_h=True,
            interior_lower_bounds_by_exterior_ears=[2, 4, 6], no_sharpness_claim=True),
        paper_contract=dict(scope='same original Gamma8; exactly two strict interior vertices for eleven types',
            two_interior_vertices_are_tau3_N_Q_and_zeta2_K_Q=True,
            exterior_ears_excluded_only_in_two_interior_branch=True,
            other_rootless_and_full_outer_stars_retained=True,
            four_joint_centers_each_once_only_for_two_interior_branch=True,
            global_alpha_beta_crossing_number_not_fixed=True,
            zeta_not_preidentified_with_Z=True, tau_not_preidentified_with_X=True,
            Wstar_may_equal_q=True, x_not_preidentified_with_xprime=True, h_not_preidentified_with_b=True,
            T_degree5_outer_link_color_words=[[1, 2, 3, 1], [1, 3, 2, 1]],
            zeta_degree5_C_and_E_sides_both_retained=True,
            named_local_fibres_are_not_original_complete_Sigma=True),
        authority_boundaries=dict(finite_control='triggered and holds', source_control='not triggered',
            local_types_not_full_source_realizations=True, initial_pair_exclusions=0,
            new_Lean=False, smaller_bad=False, no_LP_or_general_source_enumeration=True,
            Gamma8_two_interior_source_exclusion=False,
            general_wrong_side_and_eight_pairs='OPEN', common_k_lower_bound_unchanged=23))
    with (HERE / 'certificate.json').open('x') as f:
        json.dump(c, f, sort_keys=True, indent=2); f.write('\n')
    print(json.dumps(dict(status='CREATED', candidates=12, necessary_types=11)))


if __name__ == '__main__':
    main()
