#!/usr/bin/env python3
"""Finite calibration of the two closed stars and mixed fork contacts.

PROOF.md supplies the all-source Jordan and C3/C4 implications. This checker
does not enumerate source disks or certify joint source realizability.
"""
from copy import deepcopy
import gzip
from itertools import product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / 'frozen/audits/2026-10-21-w7-L-path-30dde27/six_degree/certificate-v2.json.gz'
Y = 'HL_0'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def closed_star(center, faces):
    """All four claimed faces must close one complete cyclic link."""
    link = {}
    for face in faces:
        require(center in face and len(set(face)) == 3, 'not an incident triangle')
        left, right = (v for v in face if v != center)
        link.setdefault(left, set()).add(right)
        link.setdefault(right, set()).add(left)
    require(len(link) == 4 and all(len(n) == 2 for n in link.values()),
            'four faces do not close the original degree-four star')
    seen, todo = set(), [next(iter(link))]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(link[v] - seen)
    require(seen == set(link), 'cyclic link disconnected')
    return sorted(link)


def block(row, vertex):
    return next(set(b) for b in row['complete_F_boundary_contacts'] if vertex in b)


def build():
    data = json.loads(gzip.decompress(PARENT.read_bytes()))
    cases = {(c['target'], c['split_containing_0'][1]): c for c in data['ordinary_C14_cases']}
    stars = [
        dict(center='V', faces=[['z5', 'V', 'U'], ['z5', 'V', 'z4'],
                                ['U', 'V', 'X'], ['V', 'z4', 'X']],
             required_degree=5, closed_degree=4),
        dict(center='U', faces=[['z5', 'U', Y], ['z5', 'U', 'V'],
                                [Y, 'U', 'X'], ['U', 'V', 'X']],
             required_degree=5, closed_degree=4),
    ]
    for star in stars:
        star['complete_neighbors'] = closed_star(star['center'], star['faces'])
        require(star['closed_degree'] < star['required_degree'], 'lost degree contradiction')
    pairs = []
    for target in (44459, 44466):
        two, three = cases[target, 2], cases[target, 3]
        s02 = [(i, r) for i, r in enumerate(two['complete_specific_F_types'])
               if r['same_initial_E_residual_gate']]
        s03 = [(i, r) for i, r in enumerate(three['complete_specific_F_types'])
               if r['same_initial_E_residual_gate']]
        require([i for i, _ in s02] == [12, 13, 35, 36], '02 full types changed')
        require([i for i, _ in s03] == [4, 9], '03 full types changed')
        for (i03, r03), (i02, r02) in product(s03, s02):
            first = ('U', 'z4', [0, 3]) if 'z4' in block(r03, 'U') else ('V', Y, [1, 2])
            second = ('U', 'z4', [0, 2]) if 'z4' in block(r02, 'U') else ('V', Y, [1, 3])
            row = dict(target=target, type03=i03, type02=i02,
                       required_paths=[list(first), list(second)], minimum_even_lengths=[4, 4],
                       joint_source_realized=False, pair_excluded=False, private_crossing=None)
            if first[:2] != second[:2]:
                a, b = block(r03, first[0]), block(r02, second[0])
                require(not a & b, 'mixed path boundary contacts overlap')
                boundary = two['ordered_F_boundary']
                endpoints = ['z4', 'V', 'U', Y]
                require(sorted(endpoints, key=boundary.index) == endpoints,
                        'path endpoints no longer alternate')
                shared = set(first[2]) & set(second[2])
                require(len(shared) == 1 and shared <= {2, 3}, 'wrong mixed crossing color')
                color = next(iter(shared))
                row['private_crossing'] = dict(color=color, degree_five_extra_color=5-color,
                                               missing_extra_color_forces_even_degree_at_least=6)
            pairs.append(row)
    require(len(pairs) == 16 and sum(r['private_crossing'] is not None for r in pairs) == 8,
            'conditional pair table lost rows')
    return dict(star_calibrations=stars, conditional_pairs=pairs,
                common_F_neighbors=[dict(pair=['U', 'z4'], exactly=['V']),
                                    dict(pair=['V', Y], exactly=['U'])],
                original_source_excluded=False, original_source_realized=False)


def validate(value, expected):
    require(value == expected, 'finite calibration or source boundary changed')


def main():
    expected = build()
    negatives = []
    for key in ('original_source_excluded', 'original_source_realized'):
        damaged = deepcopy(expected)
        damaged[key] = True
        negatives.append(damaged)
    damaged = deepcopy(expected)
    damaged['conditional_pairs'][0]['minimum_even_lengths'][0] = 2
    negatives.append(damaged)
    damaged = deepcopy(expected)
    damaged['common_F_neighbors'][0]['exactly'] = []
    negatives.append(damaged)
    for damaged in negatives:
        try:
            validate(damaged, expected)
        except ValueError:
            pass
        else:
            raise ValueError('negative control accepted')
    try:
        closed_star('V', expected['star_calibrations'][0]['faces'][:-1])
    except ValueError:
        pass
    else:
        raise ValueError('incomplete star accepted as complete')
    print(json.dumps(dict(result='PASS', closed_degree_four_star_calibrations=2,
                          conditional_pairs=16, private_crossing_pairs=8,
                          all_required_path_lower_bounds=4, pair_exclusions=0,
                          source_realizations=0, negative_controls=len(negatives)+1), sort_keys=True))


if __name__ == '__main__':
    main()
