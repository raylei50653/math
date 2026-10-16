#!/usr/bin/env python3
"""Complete W5 fibres and joint square membership; no source enumeration."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def compute():
    # 0 is the centre; 1,...,5 are the cyclic rim.
    rim_edges = [(i + 1, (i + 1) % 5 + 1) for i in range(5)]
    spokes = [(0, i) for i in range(1, 6)]
    edges = spokes + rim_edges
    faces = [(0, a, b) for a, b in rim_edges]
    colours = [row for row in itertools.product(range(4), repeat=6)
               if all(row[a] != row[b] for a, b in edges)]
    assert len(colours) == 120
    rows, cut_counts = [], Counter()
    for bits in itertools.product(range(2), repeat=6):
        valid = all(len({bits[v] for v in face}) == 2 for face in faces)
        fibre = [row for row in colours
                 if all((row[v] >> 1) == bits[v] for v in range(6))]
        cut = [i for i, (a, b) in enumerate(rim_edges) if bits[a] == bits[b]]
        internal = [i for i in range(5) if bits[0] == bits[i + 1]]
        odd_rim = len(set(bits[1:])) == 1 and bits[0] != bits[1]
        if valid:
            # At a dual wheel-face exactly one matching incidence is selected.
            for i in range(5):
                assert ((i in cut) + (i in internal) +
                        ((i + 1) % 5 in internal)) == 1
            assert len(cut) in (1, 3, 5)
            assert len(internal) == (5 - len(cut)) // 2
            assert bool(fibre) != odd_rim
            assert (len(cut) == 5) == odd_rim
            cut_counts[len(cut)] += 1
        else:
            assert not fibre
        rows.append({'bits': bits, 'valid_partial_matching': valid,
                     'selected_cut_positions': cut,
                     'selected_internal_positions': internal,
                     'odd_rim': odd_rim, 'complete_colour_fibre': fibre})
    assert dict(cut_counts) == {5: 2, 3: 10, 1: 10}

    # All F_e starting mark memberships, each of the four possible square
    # locations, and the one permitted second marked change at g.
    square_rows = []
    for start in ((1, 1, 0), (1, 0, 1)):
        for primal_face, changed_mark in (('v', 0), ('w', 0), ('p', 1), ('q', 1)):
            after = list(start)
            after[changed_mark] ^= 1
            joint_after = after[0] == 1 and after[1] != after[2]
            assert not joint_after
            paired = after.copy()
            paired[2] ^= 1
            joint_paired = paired[0] == 1 and paired[1] != paired[2]
            assert joint_paired == (changed_mark == 1)
            square_rows.append({'before': start, 'square_face': primal_face,
                                'after_square': after, 'joint_after_square': joint_after,
                                'after_additional_g_switch': paired,
                                'joint_after_paired_switch': joint_paired})

    return {'scope': 'complete local W5 fibres and mark membership only; source not triggered',
            'paper_proofs': 'C/PROOF.md, C1-C3',
            'wheel_vertices': list(range(6)), 'wheel_edges': edges,
            'bit_assignment_count': len(rows), 'full_colour_count': len(colours),
            'valid_partial_matching_count': sum(row['valid_partial_matching'] for row in rows),
            'selected_cut_count_distribution': dict(sorted(cut_counts.items())),
            'empty_fibre_count': sum(not row['complete_colour_fibre'] for row in rows),
            'valid_empty_fibre_count': sum(row['valid_partial_matching'] and
                                         not row['complete_colour_fibre'] for row in rows),
            'all_wheel_rows': rows, 'all_square_rows': square_rows}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--check', type=Path)
    args = parser.parse_args()
    expected = json.loads(json.dumps(compute()))
    if args.check:
        if json.loads(args.check.read_text()) != expected:
            raise SystemExit('FAIL: candidate differs from complete independent reconstruction')
    else:
        with args.output.open('x') as stream:
            json.dump(expected, stream, indent=2, sort_keys=True)
            stream.write('\n')
    print(json.dumps({key: expected[key] for key in (
        'scope', 'bit_assignment_count', 'full_colour_count',
        'valid_partial_matching_count', 'selected_cut_count_distribution',
        'empty_fibre_count', 'valid_empty_fibre_count')}, sort_keys=True))


if __name__ == '__main__':
    main()
