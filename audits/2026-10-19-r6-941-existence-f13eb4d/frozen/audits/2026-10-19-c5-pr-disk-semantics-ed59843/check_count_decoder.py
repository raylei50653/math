#!/usr/bin/env python3
"""Read-only replay of the integer count decoder; graph soundness is separate."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SOURCE = 'docs/sources/2026-10-19-c5-grammar-v02/certificate_v02.json'
PROBES = ('RR', 'PRR', 'RRR')
OBSERVATION = (9, 1, 4, 6)
DECODER = ((0, 2), (0, 3), (0, 0), (2, 3), (0, 1),
           (1, 0), (2, 1), (1, 2), (2, 0), (1, 1))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def multiply(left, right):
    return [[sum(a * b for a, b in zip(row, column)) for column in zip(*right)]
            for row in left]


def replay():
    base = json.loads((ROOT / 'BASE.json').read_bytes())
    for name, entry in base['inputs'].items():
        data = (ROOT / entry['frozen']).read_bytes()
        require(len(data) == entry['size'] and sha256(data).hexdigest() == entry['sha256'],
                'frozen input custody mismatch: ' + name)
    source = json.loads((ROOT / 'frozen' / SOURCE).read_bytes())
    matrices = source['model']['operators']
    require(source['model']['rows'] == [
        '01012', '01021', '01023', '01201', '01202',
        '01203', '01212', '01213', '01231', '01232'], 'ordered rows mismatch')
    identity = [[int(i == j) for j in range(10)] for i in range(10)]
    for letter in 'PR':
        matrix = matrices[letter]
        require(len(matrix) == 10 and all(len(row) == 10 for row in matrix), 'matrix shape')
        require(all(type(x) is int and x >= 0 for row in matrix for x in row),
                'nonnegative integer coefficients required')
    blocks = []
    for word in PROBES:
        action = identity
        for letter in word:
            action = multiply(matrices[letter], action)
        blocks.append([action[i] for i in OBSERVATION])
    observation_matrix = [row for block in blocks for row in block]
    decoder_matrix = [[int(i == 4 * p + q) for i in range(12)] for p, q in DECODER]
    require(multiply(decoder_matrix, observation_matrix) == identity,
            'integer decoder is not a left inverse')
    require(blocks[2][2] == blocks[0][3], 'c3=a4 identity failed')
    require(blocks[1][3] == [a + b for a, b in zip(blocks[2][3], blocks[2][0])],
            'b4=c4+c1 identity failed')
    # A symbolic check of the converse: E D fixes every output subject to those
    # two equations. Ten independent coordinates are left as formal variables.
    free_positions = [4 * p + q for p, q in DECODER]
    require(len(set(free_positions)) == 10, 'decoder repeats an independent coordinate')
    constrained = [[0] * 10 for _ in range(12)]
    for j, position in enumerate(free_positions):
        constrained[position][j] = 1
    constrained[10] = constrained[3][:]
    constrained[7] = [a + b for a, b in zip(constrained[11], constrained[8])]
    require(multiply(multiply(observation_matrix, decoder_matrix), constrained) == constrained,
            'exact nonnegative integer image identity failed')
    return {
        'schema': 'c5-pr-disk-semantics/count-decoder-v1',
        'domain': 'all nonnegative integer ten-vectors; actual disk use requires the paper fibre theorem',
        'probes': list(PROBES), 'observation_indices': list(OBSERVATION),
        'probe_integer_matrices': blocks, 'decoder_zero_based': [list(x) for x in DECODER],
        'decoder_times_observation': identity,
        'exact_image_equations': ['c3=a4', 'b4=c4+c1'],
        'claims_all_disk_supports_in_132': False,
        'new_Lean_theorem': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    parser.add_argument('--certificate', type=Path, default=ROOT / 'count_decoder.json')
    args = parser.parse_args()
    expected = encoded(replay())
    if args.write:
        with args.certificate.open('xb') as stream:
            stream.write(expected)
        print('WROTE integer count-decoder certificate (exclusive create)')
    else:
        require(args.certificate.read_bytes() == expected, 'count decoder certificate mismatch')
        print('PASS: integer D E = I; exact nonnegative integer image; frozen custody')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print('FAIL:', error, file=sys.stderr)
        raise SystemExit(1)
