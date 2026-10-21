#!/usr/bin/env python3
"""Read-only audit of the named Type-I initial 02/03 obligations.

This table records conditional necessary geometry, not jointly realizable sources.
The geometric implications are proved in geometry/PROOF.md.
"""
from copy import deepcopy
import argparse
import gzip
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PARENT = 'audits/2026-10-21-w7-L-path-30dde27/six_degree/'
BASE = '2c38d1dcb4490017312467deb19d9da02b7bb2a6'
Y = 'HL_0'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'BASE changed')
    for row in manifest['inputs']:
        data = (HERE / 'frozen' / row['path']).read_bytes()
        require(len(data) == row['bytes'] and sha256(data).hexdigest() == row['sha256'],
                'frozen authority drift: ' + row['path'])
    return json.loads(gzip.decompress((HERE / 'frozen' / PARENT / 'certificate-v2.json.gz').read_bytes()))


def survivors(case):
    return [(i, row) for i, row in enumerate(case['complete_specific_F_types'])
            if row['same_initial_E_residual_gate'] and not row['forbidden_action_masks']]


def block(row, vertex):
    return next(set(b) for b in row['complete_F_boundary_contacts'] if vertex in b)


def build():
    parent = inputs()
    cases = {(c['target'], c['split_containing_0'][1]): c for c in parent['ordinary_C14_cases']}
    rows = []
    for target in (44459, 44466):
        c02, c03 = cases[target, 2], cases[target, 3]
        s02, s03 = survivors(c02), survivors(c03)
        require([i for i, _ in s02] == [12, 13, 35, 36], '02 four full types changed')
        require([i for i, _ in s03] == [4, 9], '03 two full types changed')
        boundary = c02['ordered_F_boundary']
        require(boundary == c03['ordered_F_boundary'], 'different ordered F boundaries')
        require(c02['literal_F_boundary_colors'] == c03['literal_F_boundary_colors'],
                'different literal frames')
        colors = dict(zip(boundary, c02['literal_F_boundary_colors']))
        endpoints = ['z4', 'V', 'U', Y]
        require([boundary.index(v) for v in endpoints] == sorted(boundary.index(v) for v in endpoints),
                'alternating original endpoint order changed')
        for (i03, r03), (i02, r02) in product(s03, s02):
            u03 = 'z4' in block(r03, 'U')
            v03 = Y in block(r03, 'V')
            u02 = 'z4' in block(r02, 'U')
            v02 = Y in block(r02, 'V')
            require(u03 != v03 and u02 != v02, 'full fork lost exclusivity')
            p03 = ('U', 'z4', [0, 3]) if u03 else ('V', Y, [1, 2])
            p02 = ('U', 'z4', [0, 2]) if u02 else ('V', Y, [1, 3])
            for start, end, palette in (p03, p02):
                require(colors[start] == colors[end] and colors[start] in palette,
                        'replacement path must have even length')
            crossing = None
            if u03 != u02:
                contacts03 = block(r03, p03[0])
                contacts02 = block(r02, p02[0])
                require(not contacts03 & contacts02, 'claimed crossing is not forced private')
                common = set(p03[2]) & set(p02[2])
                require(len(common) == 1, 'crossing palette not unique')
                color = common.pop()
                require(color in (2, 3), 'wrong forced crossing color')
                crossing = {'color': color, 'original_F_private': True,
                            'alternating_branch_neighbor_colors': [0, 1, 0, 1],
                            'if_original_degree_5_fifth_neighbor_color': 5 - color,
                            'if_no_fifth_color_neighbor_degree_is_even_and_at_least': 6}
            rows.append({'target': target, 'F03_type_index': i03, 'F02_type_index': i02,
                         'complete_F03_boundary_contacts': r03['complete_F_boundary_contacts'],
                         'complete_F02_boundary_contacts': r02['complete_F_boundary_contacts'],
                         'required_F_paths': [dict(start=p[0], end=p[1], palette=p[2],
                                                   minimum_even_length=4) for p in (p03, p02)],
                         'forced_private_transverse_intersection': crossing,
                         'joint_source_status': 'OPEN', 'pair_excluded': False})
    return {'base': BASE, 'scope': 'ordinary Type I, U/V original E-private, initial literal F only',
            'all_16_conditional_initial_pairs': rows,
            'complete_common_neighbors_in_original_F': [
                {'pair': ['U', 'z4'], 'common_neighbors': ['V']},
                {'pair': ['V', Y], 'common_neighbors': ['U']}],
            'geometric_source_exclusion': False, 'joint_source_realized': False,
            'independent_palette_survivors_used_as_joint_witness': False,
            'V_equals_w_pinched_alias_covered': False, 'new_Lean': False,
            'pair_table_is_conditional_necessary_geometry': True}


def validate(certificate, expected):
    require(certificate == expected, 'certificate differs from full frozen reconstruction')


def negative_controls(expected):
    bad = []
    c = deepcopy(expected); c['joint_source_realized'] = True; bad.append(c)
    c = deepcopy(expected); c['geometric_source_exclusion'] = True; bad.append(c)
    c = deepcopy(expected); c['all_16_conditional_initial_pairs'].pop(); bad.append(c)
    c = deepcopy(expected); c['all_16_conditional_initial_pairs'][0]['required_F_paths'][0]['minimum_even_length'] = 2; bad.append(c)
    c = deepcopy(expected)
    cross = next(row for row in c['all_16_conditional_initial_pairs'] if row['forced_private_transverse_intersection'])
    cross['forced_private_transverse_intersection']['color'] = 0; bad.append(c)
    for c in bad:
        try:
            validate(c, expected)
        except ValueError:
            continue
        raise ValueError('corrupted certificate accepted')
    return len(bad)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json')
    args = parser.parse_args()
    expected = build()
    if args.build:
        with args.certificate.open('xb') as f:
            f.write(packed(expected))
    validate(json.loads(args.certificate.read_text()), expected)
    print(json.dumps({'result': 'PASS', 'base': BASE, 'complete_initial_pairs': 16,
                      'mixed_pairs_with_private_crossing': 8,
                      'all_required_replacement_paths_have_even_length_at_least': 4,
                      'pairs_excluded': 0, 'joint_sources_realized': 0,
                      'negative_controls': negative_controls(expected)}, sort_keys=True))


if __name__ == '__main__':
    main()
