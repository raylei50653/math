#!/usr/bin/env python3
"""Finite-set/bitmask replay; Python evidence, not Lean extraction or a graph search."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'artifacts/c5_cells/bitmask_check.json'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def encode(selected):
    # Independent arithmetic encoding, with no shifts or bitwise operators.
    return sum(2 ** e for e in selected)


def decode(width, mask):
    return {e for e in range(width) if (mask // (2 ** e)) % 2}


def check_state(width, selected):
    mask = encode(selected)
    require(decode(width, mask) == selected, 'round trip')
    require(0 <= mask < 2 ** width, 'width bound')
    for cut in range(width + 2):
        prefix = {e for e in selected if e < cut}
        shifted = {e - cut for e in selected if e >= cut}
        require(encode(prefix) == mask & ((1 << cut) - 1), 'prefix')
        require(encode(shifted) == mask >> cut, 'shift')
        require(len(shifted) == bin(mask >> cut).count('1'), 'suffix count')
        require(encode(selected | {cut}) == mask | (1 << cut), 'insert')
        window = {i for i in range(5) if cut + i in selected}
        require(encode(window) == (mask >> cut) & 31, 'attachment window')
    return width + 2


def negative_controls():
    cases = [
        ('xor_instead_of_or', lambda: require(encode({2}) == (4 ^ (1 << 2)), 'insert')),
        ('shift_off_by_one', lambda: require(encode({0}) == (4 >> 3), 'shift')),
        ('unbounded_round_trip', lambda: require(encode(decode(3, 8)) == 8, 'round trip')),
        ('attachment_bit_order', lambda: require(encode({0}) == 16, 'attachment window')),
    ]
    result = {}
    for name, action in cases:
        try:
            action()
        except AssertionError:
            result[name] = 'rejected'
        else:
            raise AssertionError(f'negative control accepted: {name}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    paths = ['scripts/c5_bitmask_check.py', 'Math/EdgeMask.lean', 'Math/ReducedDFS.lean',
             'scripts/c5_cell_reduced.py', 'artifacts/c5_cells/cells.json']
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    states = cuts = pairs = 0
    for width in range(11):
        for mask in range(2 ** width):
            cuts += check_state(width, decode(width, mask))
            states += 1
    for width in range(7):
        subsets = [decode(width, mask) for mask in range(2 ** width)]
        for left in subsets:
            for right in subsets:
                require(encode(left & right) == encode(left) & encode(right), 'intersection')
                pairs += 1
    high_states = 0
    for width in (64, 65, 128, 257):
        for selected in (set(), {0}, {width - 1}, {0, width // 2, width - 1}, set(range(width))):
            check_state(width, selected)
            high_states += 1
    report = dict(scope='all masks width 0..10; all intersection pairs width 0..6; '
                        '20 sparse/dense cases at widths 64/65/128/257; no graph search',
                  source_sha256=hashes, exhaustive_states=states, cut_observations=cuts,
                  intersection_pairs=pairs, high_width_states=high_states,
                  mismatches=0, negative_controls=negative_controls())
    require(all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h for p, h in hashes.items()),
            'source changed during audit')
    payload = json.dumps(report, sort_keys=True, indent=2) + '\n'
    if args.check:
        require(REPORT.read_text() == payload, 'report replay differs')
        print('bitmask replay: PASS')
    else:
        REPORT.write_text(payload)
        print(payload, end='')


if __name__ == '__main__':
    main()
