#!/usr/bin/env python3
"""Exclusive-create the paper-derived finite link table, independently of check.py."""
from itertools import permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV = 'audits/2026-10-23-941-gamma8-rootless-stars-6b09cd4'


def links(left, middle, right):
    result = []
    for p in ('p_d', 'p_x'):
        result += [[left, middle, right, p, 'U'], [left, middle, right, 'U', p]]
    result += [[left, middle, right, *p] for p in permutations(['p_d', 'U', 'p_x'])
               if p[1] == 'U']
    return sorted(result)


def main():
    prior = json.loads((HERE / 'frozen' / PREV / 'certificate-v2.json').read_text())
    c = prior
    for _ in range(3):
        c = c['complete_predecessor_certificate']
    actual = [r for r in c['candidates'] if r['classification'] == 'local_necessary_type']
    equality, aliases, empty = [], [], []
    for cell in actual:
        for side, endpoint in [('C', 'r'), ('E', 's')]:
            for uc, vc in [(0, 3), (1, 0), (1, 3)]:
                if uc == 0:
                    target, allowed, cycles = 'u', ['m', 'n', 'v'], []
                elif vc == 0:
                    target, allowed, cycles = 'v', sorted(['m', 'u', endpoint]), []
                else:
                    target = 'u'
                    allowed = sorted(['m', 'n', 'v', 'p_d', 'p_x'] + (['U'] if side == 'C' else []))
                    cycles = links('n', 'm', 'v') if side == 'C' else []
                equality.append(dict(cell=cell['id'], core=cell['core'], side=side,
                    u_color=uc, v_color=vc, tested_vertex=target,
                    allowed_neighbors=allowed, complete_u_links=cycles))
            aliases.append(dict(cell=cell['id'], side=side, U_equals_d=True,
                allowed_neighbors=['m', 'n', 'p_d', 'p_x', 'v'], complete_u_links=[]))
        for alias in (False, True):
            empty.append(dict(cell=cell['id'], core=cell['core'], U_equals_d=alias,
                allowed_neighbors=sorted(['T','a','b','p_d','p_x'] + ([] if alias else ['U'])),
                complete_y_links=[] if alias else links('a', 'T', 'b'),
                O_already_excluded=cell['core'] == 'O'))
    result = dict(schema='941-gamma8-six-equality-v1', base=BASE,
        complete_predecessor_certificate=prior, six_point_cases=equality,
        d_U_alias_cases=aliases, empty_M2_five_point_cases=empty,
        paper_contract=dict(j=2, same_original_graph_and_frame=True,
            all_source_stars_complete=True, rootless_neighbors_have_only_U_frame_exception=True,
            C_not_equal_E=True, E_may_be_rootless=True, full_M2_retained=True,
            six_point_M2_singleton=True, six_point_M_equals_T_m=True,
            six_point_side='C', six_point_d_not_U=True, six_point_u_degree_options=[5, 6],
            empty_M2_five_points_requires_U_y=True, empty_M2_five_points_d_not_U=True,
            minimum_when_M2_empty_T6_d_U=6),
        authority_boundaries=dict(finite_control='triggered and holds',
            source_realizability='not triggered',
            excluded_conditional_branches=['six_points_m_in_E', 'six_points_d_U',
                                           'empty_M2_T6_five_points_d_U'],
            six_point_C_completion='OPEN', empty_M2_L_R_completion='OPEN',
            eleven_type_exclusions=0, general_wrong_side='OPEN', common_k_lower_bound=23,
            new_Lean=False, new_LP=False, smaller_bad=False))
    with (HERE / 'certificate.json').open('x') as out:
        json.dump(result, out, indent=2, sort_keys=True)
        out.write('\n')
    print(json.dumps(dict(status='CREATED', color_cases=len(equality), aliases=len(aliases), empty_cases=len(empty))))


if __name__ == '__main__':
    main()
