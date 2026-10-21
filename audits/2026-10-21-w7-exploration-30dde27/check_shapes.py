#!/usr/bin/env python3
"""Exact local target-colour diagnostics, with no original-source realization."""
from collections import defaultdict
from hashlib import sha256
from itertools import product
from math import comb, prod
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '30dde27293b5d3ad63c75fae73cda5be96db705b'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'wrong frozen BASE')
    for row in manifest['inputs']:
        raw = (HERE / 'frozen' / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'frozen input drift: ' + row['path'])
        if row['role'] == 'mathematical-authority':
            require((ROOT / row['path']).read_bytes() == raw,
                    'live mathematical authority drift: ' + row['path'])
    return len(manifest['inputs'])


def compositions(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, width - 1):
                yield (first,) + tail


def independent_polynomial(k):
    return [comb(k + 1 - j, j) for j in range((k + 1) // 2 + 1)]


def convolve(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def A(k):
    return (2 ** (k + 2) + (-1) ** (k + 1)) // 3


def barrier_histogram(shape):
    polynomial = [1]
    for k in shape:
        polynomial = convolve(polynomial, independent_polynomial(k))
    return {str(b): coefficient * 2 ** (b - 1)
            for b, coefficient in enumerate(polynomial) if b and coefficient}


def path_dynamic_program(profile, shape):
    """Colour every vertex in the original ordered a--q local path.

    This does not use independent-set polynomials or the 504-wheel formula.
    The two target choices agree on this local graph; their exterior differs.
    """
    centers = ([1] if profile == 0 else []) + [2, 1, 2, 1, 2]
    require(len(shape) == len(centers), 'shape width changed')
    states = {(0, 0): 1}  # literal a=0, number of 12-coloured H points
    for index, (k, center) in enumerate(zip(shape, centers)):
        nodes = [((0, 3, 3 - center), True)] * k
        nodes.append(((3,) if index == len(shape) - 1 else (0, 3), False))
        for allowed, is_H in nodes:
            next_states = defaultdict(int)
            for (previous, barriers), multiplicity in states.items():
                for color in allowed:
                    if color != previous:
                        next_states[(color, barriers + int(is_H and color in (1, 2)))] += multiplicity
            states = next_states
    counts = defaultdict(int)
    for (last, barriers), count in states.items():
        require(last == 3, 'q literal colour changed')
        counts[barriers] += count
    return dict(sorted(counts.items()))


def partitions(total, width, ceiling=None):
    if width == 0:
        if total == 0:
            yield ()
        return
    ceiling = total if ceiling is None else min(ceiling, total)
    for first in range(ceiling, -1, -1):
        for tail in partitions(total - first, width - 1, first):
            yield (first,) + tail


def compute():
    records = []
    totals = []
    for profile, width in ((0, 6), (1, 5)):
        for K in range(6):
            group = []
            for shape in compositions(K, width):
                histogram = barrier_histogram(shape)
                dynamic = path_dynamic_program(profile, shape)
                require({str(b): n for b, n in dynamic.items() if b} == histogram,
                        'literal-path count disagrees with barrier formula')
                require(dynamic.get(0, 0) == int((K + width) % 2 == 1),
                        'all-03 path parity changed')
                count = sum(histogram.values())
                require(count == (prod(A(k) for k in shape) - 1) // 2,
                        'closed formula disagrees with complete histogram')
                row = {'profile': profile, 'K': K, 'H_lengths': list(shape),
                       'separated_local_colorings': count,
                       'barrier_histogram': histogram,
                       'all03_local_colorings_before_separation': dynamic.get(0, 0)}
                records.append(row)
                group.append(row)
            totals.append({'profile': profile, 'K': K, 'ordered_shapes': len(group),
                           'separated_local_colorings': sum(r['separated_local_colorings'] for r in group)})
    require(len(records) == 714, 'ordered shape coverage changed')

    # Fixed K repartition is a diagnostic across local collars, not a graph move.
    extrema = []
    for width in (5, 6):
        for K in range(1, 19):
            shapes = list(partitions(K, width))
            values = {s: (prod(A(k) for k in s) - 1) // 2 for s in shapes}
            lo, hi = min(values.values()), max(values.values())
            require(lo == (A(K) - 1) // 2, 'concentrated diagnostic minimum failed')
            spread_shape = tuple(sorted(([1] * K + [0] * (width - K)) if K <= width
                                       else ([K - width + 1] + [1] * (width - 1)), reverse=True))
            # Finite calibration of the arbitrary-K extremal proof in the report.
            require(values[spread_shape] == hi, 'finite diagnostic maximum pattern failed')
            extrema.append({'width': width, 'K': K, 'sorted_shapes': len(shapes),
                            'minimum': lo, 'maximum': hi,
                            'min_shapes': [list(s) for s in shapes if values[s] == lo],
                            'max_shapes': [list(s) for s in shapes if values[s] == hi]})

    # Independently enumerate barrier subsets on paths; no colouring formula here.
    for k in range(13):
        direct = [0] * (k + 1)
        for bits in product((0, 1), repeat=k):
            if not any(a == b == 1 for a, b in zip(bits, bits[1:])):
                direct[sum(bits)] += 1
        expected = independent_polynomial(k)
        require(direct[:len(expected)] == expected and not any(direct[len(expected):]),
                'path-independent-set coefficient failed')
        require(sum(n * 2 ** b for b, n in enumerate(direct)) == A(k),
                'A_k closed form failed')
    split_cases = 0
    consolidation_cases = 0
    for m, n in product(range(1, 19), repeat=2):
        require(A(m) * A(n) - A(m + n)
                == 4 * A(max(m - 2, 0)) * A(max(n - 2, 0)),
                'split-versus-concentrate identity failed')
        split_cases += 1
        if m >= 2 and n >= 2:
            require(9 * (3 * A(m + n - 1) - A(m) * A(n))
                    == 2 * (2 ** m + 2 * (-1) ** m) * (2 ** n + 2 * (-1) ** n),
                    'extremal consolidation identity failed')
            require(3 * A(m + n - 1) > A(m) * A(n), 'consolidation did not improve')
            consolidation_cases += 1
    return {'base': BASE, 'frozen_inputs': inputs(), 'ordered_shape_cases': records,
            'shape_totals': totals, 'finite_extrema_K1_to18': extrema,
            'independent_set_lengths_checked': list(range(13)), 'split_identity_checks': split_cases,
            'extremal_consolidation_identity_checks': consolidation_cases,
            'original_941_source_triggered': False, 'profile0_excluded': False,
            'profile1_excluded': False, 'original_count_cone_solved': False,
            'legal_smaller_patch_constructed': False, 'new_Lean': False}


def validate(result, expected):
    require(result == expected, 'certificate differs from exact recomputation or enlarges claims')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'shapes-v2.json')
    args = parser.parse_args()
    expected = compute()
    if args.build:
        with args.certificate.open('x') as stream:
            json.dump(expected, stream, sort_keys=True, indent=2)
            stream.write('\n')
    validate(json.loads(args.certificate.read_text()), expected)
    negative_controls = 0
    for key, bad in [('profile0_excluded', True), ('original_941_source_triggered', True),
                     ('legal_smaller_patch_constructed', True)]:
        try:
            validate(expected | {key: bad}, expected)
        except ValueError:
            negative_controls += 1
    require(negative_controls == 3, 'scope pollution negative controls failed')
    print(json.dumps({'result': 'PASS', 'ordered_shapes': len(expected['ordered_shape_cases']),
                      'shape_totals': expected['shape_totals'], 'finite_extrema_rows': 36,
                      'negative_controls': negative_controls, 'source_exclusions': []}, sort_keys=True))


if __name__ == '__main__':
    main()
