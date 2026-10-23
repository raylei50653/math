#!/usr/bin/env python3
"""Exclusive-create a calibration of forced exits and original full-star budgets."""
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = 'audits/2026-10-23-941-gamma8-m2-stars-6b09cd4/certificate.json'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'


def main():
    prior = json.loads((HERE / 'frozen' / PREV).read_text())
    cells = prior['complete_predecessor_certificate']['complete_predecessor_certificate']
    boundary = set(cells['boundary'])
    obligations = []
    for cell in cells['candidates']:
        if cell['classification'] != 'local_necessary_type':
            continue
        obligations.append(dict(id=cell['id'], core=cell['core'],
            blocked_exterior_common_neighbor_pair=['d', 'x'],
            K2_exit_centers=['d', 'x'], T_interior_neighbors=['tau'],
            boundary_without_color2=True))
    prefixes = []
    for row in prior['prefix_rows']:
        names = {r: 'out_' + min(g) for g in row['partition'] for r in g}
        m = names['a' if row['T_M2_side'] == 'C' else 'b']
        neighbors = sorted({v if u == m else u for u, v in row['edges'] if m in (u, v)})
        k2 = sorted({names[r] for r, kind in row['kinds'].items() if kind == 'K2'})
        prefixes.append(dict(id=row['id'], core=row['core'], T_M2_side=row['T_M2_side'],
            m_vertex=m, Gamma_neighbors=sorted(boundary & set(neighbors)),
            known_prefix_neighbors=neighbors, private_K2_face_vertices=k2,
            minimum_external_vertices=6, opposite_cut_bound=8))
    trials = []
    for old, new in product(['N1', 'N3'], ['N1', 'N3', 'Other1', 'Other3', 'K2', 'Other2']):
        same_color = int(old[-1]) == int(new[-1])
        allowed = not same_color and (new == 'K2' or new.startswith('N'))
        trials.append(dict(from_kind=old, next_kind=new, allowed=allowed))
    result = dict(schema='941-gamma8-rootless-stars-v1', base=BASE,
        complete_predecessor_certificate=prior, cell_obligations=obligations,
        prefix_audits=prefixes, first_departure_trials=trials,
        m_boundary_audit=[dict(side=s, allowed_Gamma_neighbors=sorted(['T', p]))
                          for s, p in [('C', 'r'), ('E', 's')]],
        algebra_contract=dict(b_means='all original Gamma neighbors', max_b=2, min_degree=5,
            protected_bound='degree+3-b', full_M2_bound='degree+M2_size+2-b',
            minimum_if_M2_nonempty=6,
            adjacent_two_star_bound='T_degree+degree-4',
            nonadjacent_two_star_bound='T_degree+degree-2',
            minimum_if_T_degree5_and_M2_not_singleton=8,
            minimum_if_T_degree_at_least_6_and_M2_nonempty=7,
            six_vertex_residual=dict(M2_size=1, m_degree=5, Gamma_neighbors=2, T_degree=5),
            M2_empty=dict(M_singleton_T=True, T_degree_even=True)),
        paper_contract=dict(j=2, same_original_exterior=True, full_original_stars=True,
            full_M2_set_retained=True, E_may_be_rootless=True,
            first_departure_K2_from_d_and_x=True,
            first_departure_stays_in_F_when_d_is_U=True,
            distinct_exterior_K2_exits=True, private_M_star_degree_at_least=5,
            protected_exterior_bound=6, opposite_separator_exterior_bound=8,
            six_vertex_residual_uses_C3_faces=True,
            prefix_rows_are_not_complete_stars_or_disk_completions=True),
        authority_boundaries=dict(finite_control='triggered and holds',
            original_source_control='not triggered', general_wrong_side='OPEN',
            eleven_type_exclusions=0, initial_pair_exclusions=0,
            common_k_lower_bound=23, smaller_bad=False, new_Lean=False, new_LP=False))
    with (HERE / 'certificate-v2.json').open('x') as out:
        json.dump(result, out, indent=2, sort_keys=True)
        out.write('\n')
    print(json.dumps(dict(status='CREATED', cells=len(obligations), prefixes=len(prefixes),
                         first_departure_trials=len(trials))))


if __name__ == '__main__':
    main()
