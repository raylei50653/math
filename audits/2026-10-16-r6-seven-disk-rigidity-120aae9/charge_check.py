#!/usr/bin/env python3
"""Finite algebra calibration of the general excess cancellation; no sources."""
import argparse
import copy
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def add(*terms):
    result = {}
    for term in terms:
        for variable, coefficient in term.items():
            result[variable] = result.get(variable, 0) + coefficient
    return {key: value for key, value in sorted(result.items()) if value}


def certificate():
    local = []
    for beta in (0, 1):
        for excess in range(0, 22, 2):
            for kind in ('ordinary', 'pin', 'z'):
                degree = {'ordinary': 6-beta, 'pin': 5-beta, 'z': 7-beta}[kind] + excess
                for inward in range(1, degree-1):
                    if inward % 2 != beta:
                        continue
                    difference = degree - 2 - inward
                    if kind == 'z' and degree-inward-1 < 3:
                        continue
                    ear = int(kind == 'ordinary' and difference == 0)
                    bound = 2-beta+excess+2*ear
                    require(inward <= bound, 'local boundary inequality')
                    local.append([kind, beta, excess, degree, inward, ear, bound])
    m_sector = []
    for containing in range(6, 35):
        for other in range(7, 35, 2):
            degree = containing+other-5
            for inward in range(1, containing-4):
                if (containing-inward-5) % 2:
                    continue
                beta = inward % 2
                excess = degree-(7+beta)
                require(excess >= 0 and excess % 2 == 0, 'm parity excess')
                bound = 2-beta+excess-2*(1-beta)
                require(inward <= bound, 'm sector inequality')
                m_sector.append([containing, other, inward, excess, bound])
    absent = []
    for left in range(7, 35, 2):
        for right in range(7, 35, 2):
            excess = left+right-5-7
            require(excess >= 2, 'absent m compulsory excess')
            absent.append([left, right, excess])
    delta = {'I': 1, 'B': 1, 'epsilon': -2, 'constant': -10}
    summed = add({'constant': 14, 'B': -1}, delta,
                 {'Delta_i': -1}, {'constant': -2, 'epsilon': 2}, {'h': 2})
    euler = {'constant': 8, 'I': 1, 'Delta_i': -1}
    residual = add(euler, {key: -value for key, value in summed.items()})
    require(summed == {'Delta_i': -1, 'I': 1, 'constant': 2, 'h': 2}, 'exact affine cancellation')
    require(residual == {'constant': 6, 'h': -2}, 'three-ear inequality')
    independent = []
    for mask in range(128):
        vertices = [i for i in range(7) if mask & (1 << i)]
        if all((i+1) % 7 not in vertices for i in vertices):
            independent.append(vertices)
    require(max(map(len, independent)) == 3, 'seven-cycle independent set size')
    return {'schema': 'seven-disk-general-charge-v1',
            'domain': {'kind': 'finite local arithmetic and exact affine coefficient control',
                       'degree_excess_samples': '0,2,...,20',
                       'original_sector_degree_samples': '6,...,34',
                       'arbitrary_size_proof': 'PROOF.md sections 2-4, independently reviewed',
                       'actual_source_instances': 0, 'actual_source_status': 'not triggered'},
            'local_boundary_rows': local, 'm_sector_rows': m_sector,
            'm_absent_rows': absent, 'delta_coefficients': delta,
            'summed_boundary_coefficients': summed, 'euler_coefficients': euler,
            'euler_minus_upper_bound': residual,
            'all_independent_subsets_of_C7': independent}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('charge_certificate.json'))
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--negative', choices=('missing-interior-excess', 'missing-m-cost', 'z-two-exterior-faces'))
    args = parser.parse_args()
    expected = certificate()
    if args.write:
        require(args.negative is None, 'negative comparison only')
        with args.certificate.open('x') as stream:
            json.dump(expected, stream, indent=2, sort_keys=True)
            stream.write('\n')
    actual = json.loads(args.certificate.read_text())
    if args.negative:
        actual = copy.deepcopy(actual)
        if args.negative == 'missing-interior-excess':
            actual['summed_boundary_coefficients'].pop('Delta_i')
        elif args.negative == 'missing-m-cost':
            actual['summed_boundary_coefficients']['constant'] += 2
        else:
            # beta=1, z degree six, t=3 would pass a false two-outside-face premise.
            actual['local_boundary_rows'].append(['z', 1, 0, 6, 3, 0, 1])
    require(actual == expected, 'complete arithmetic certificate mismatch')
    print(json.dumps({'status': 'PASS', 'local_boundary_rows': len(expected['local_boundary_rows']),
                      'm_sector_rows': len(expected['m_sector_rows']),
                      'm_absent_rows': len(expected['m_absent_rows']),
                      'exact_residual': expected['euler_minus_upper_bound'],
                      'source_instances': 0, 'source_status': 'not triggered'}, sort_keys=True))


if __name__ == '__main__':
    main()
