#!/usr/bin/env python3
"""Exact six-source ray, cut-sector ranks, and four-pole reduction witnesses.

The certificate checks finite target data. The accompanying paper reduction
quantifies over all planar sources and scales; no graph search or 4CT oracle
is used here.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
from functools import reduce

from ck_bernhart_marked_separation import complete_colorings, determinant
from four_color_counts_cone_verification import compatible, signatures

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'audits/2026-10-29-bernhart-endpoint-ray/r2-support-actions.json'
DEFAULT = ROOT / 'audits/2026-10-30-bernhart-universal-marking/six-source-reductions.json'
PAIRS = ((1, 2), (1, 3), (2, 3))


def xor(values):
    return reduce(int.__xor__, values, 0)


def det_or_zero(matrix):
    try:
        return determinant(matrix)
    except StopIteration:
        return 0


def row_rank_minor(rows, width):
    echelon, chosen, columns = [], [], []
    for index, original in enumerate(rows):
        row = list(map(Fraction, original))
        for pivot, basis in echelon:
            value = row[pivot]
            if value:
                row = [a - value * b for a, b in zip(row, basis)]
        pivot = next((j for j, value in enumerate(row) if value), None)
        if pivot is None:
            continue
        value = row[pivot]
        row = [a / value for a in row]
        echelon.append((pivot, row))
        chosen.append(index)
        columns.append(pivot)
    minor = [[rows[i][j] for j in columns] for i in chosen]
    det = determinant(minor)
    assert det
    return dict(rank=len(chosen), selected_rows=chosen,
                selected_columns=columns, minor=minor, determinant=det)


def report():
    source = json.loads(SOURCE.read_text())
    words = tuple(product((1, 2, 3), repeat=6))
    h = {tuple(row['six_word']): row['three_cap_colors'][0]
         for row in source['word_factorization']['rows']}
    six_sigs = tuple(signatures(6))
    positive = sorted(row['six_signature_index']
                      for row in source['signature_factorization']['pairs'])
    assert len(words) == len(h) == 729
    assert len(six_sigs) == 191 and len(positive) == 23
    exclusions, eligible = [], []
    for index, sig in enumerate(six_sigs):
        witness = next(((word, pair) for word in words if not h[word]
                        for pair in PAIRS if compatible(word, pair, sig)), None)
        if witness is None:
            eligible.append(index)
        else:
            word, pair = witness
            exclusions.append(dict(signature_index=index, signature=sig,
                                   zero_word=word, pair=pair))
    assert eligible == positive and len(exclusions) == 168
    equations, metadata = [], []
    for word in words:
        incidence = [[int(compatible(word, pair, six_sigs[index]))
                      for index in eligible] for pair in PAIRS]
        for other in (1, 2):
            row = [a - b for a, b in zip(incidence[0], incidence[other])]
            assert sum(row) == 0
            equations.append(row)
            metadata.append(dict(word=word, first_pair=PAIRS[0], second_pair=PAIRS[other]))
        assert all(sum(row) == h[word] for row in incidence)
    rank = row_rank_minor(equations, 23)
    assert rank['rank'] == 22
    rank['selected_row_equations'] = [metadata[i] for i in rank['selected_rows']]
    rank['all_1458_equations_annihilate_ones'] = True
    rank['kernel_basis'] = [1] * 23
    rank['reason_upper_bound_22'] = 'Every row has sum zero.'

    # These are complete count representatives, with actual edge identities.
    four_words = ((1, 1, 1, 1), (1, 1, 2, 2), (1, 2, 1, 2), (1, 2, 2, 1))
    four_reps = [
        ('wire_01_23', [(0, 1), (2, 3)], ((0, 1, -1), (2, 3, -1)), (1, 1, 0, 0)),
        ('wire_03_12', [(0, 3), (1, 2)], ((0, 3, -1), (1, 2, -1)), (1, 0, 0, 1)),
        ('H_01_23', [(0, 4), (1, 4), (4, 5), (2, 5), (3, 5)],
         ((0, 1, 1), (2, 3, 1)), (0, 0, 1, 1)),
        ('H_03_12', [(0, 4), (3, 4), (4, 5), (1, 5), (2, 5)],
         ((0, 3, 1), (1, 2, 1)), (0, 1, 1, 0)),
    ]
    representatives = []
    for name, edges, sig, expected in four_reps:
        full = complete_colorings(edges)
        counts = []
        for word in four_words:
            counts.append(sum(all(phi[next(e for e, uv in enumerate(edges) if v in uv)] == word[v]
                                  for v in range(4)) for phi in full))
        assert tuple(counts) == expected
        assert counts == [int(compatible(word, (1, 2), sig)) for word in four_words]
        representatives.append(dict(name=name, edges=edges,
                                    all_complete_colorings=full, counts=counts,
                                    full_12_signature_weight=sig))
    four_sigs = tuple(signatures(4))
    assert all(tuple(sig) in four_sigs for _, _, sig, _ in four_reps)
    for word in four_words:
        active = [sig for sig in four_sigs if compatible(word, (1, 2), sig)]
        assert set(active) == {sig for _, _, sig, _ in four_reps
                               if compatible(word, (1, 2), sig)}
    triangle_witnesses = []
    unequal_leaf_pair_witnesses = []
    for left, right in combinations(range(6), 2):
        different_word = ((1, 1, 2, 3, 2, 3) if (right - left) == 3
                          else (1, 2, 3, 1, 2, 3))
        assert h[different_word] > 0 and different_word[left] != different_word[right]
        unequal_leaf_pair_witnesses.append(dict(leaf_pair=[left, right],
                                                positive_word=different_word,
                                                h=h[different_word]))
        rest = [i for i in range(6) if i not in (left, right)]
        witnesses = []
        for suffix in product((1, 2, 3), repeat=4):
            triple, full_words = [], []
            for color in (1, 2, 3):
                word = [0] * 6
                word[left] = word[right] = color
                for index, value in zip(rest, suffix):
                    word[index] = value
                word = tuple(word)
                full_words.append(word)
                triple.append(h[word])
            negative = [sum(triple) - 2 * value for value in triple]
            if min(negative) < 0:
                witnesses.append(dict(rest_word=suffix, full_words=full_words,
                                      target_counts=triple, twice_inverse_counts=negative))
        assert len(witnesses) in (6, 9, 15, 21)
        triangle_witnesses.append(dict(leaf_pair=[left, right],
                                       rest_positions=rest, witnesses=witnesses))

    bridge_rows = []
    for mask in range(64):
        subset = [i for i in range(6) if mask >> i & 1]
        zero_word = next((word for word in words if h[word] and
                          xor(word[i] for i in subset) == 0), None)
        bridge_rows.append(dict(leaf_subset=subset,
                                bridge_flow_not_excluded=zero_word is None,
                                positive_word_with_zero_boundary_xor=zero_word))
    possible = [row['leaf_subset'] for row in bridge_rows if row['bridge_flow_not_excluded']]
    assert len(possible) == 12 and all(len(row) in (1, 5) for row in possible)

    # Three-leaf XOR-zero sectors have six literal row/column words each.
    # Two cut edges must have equal colors, hence at most three separating states.
    sectors = []
    triples = tuple(permutations((1, 2, 3)))
    for subset in combinations(range(6), 3):
        complement = tuple(i for i in range(6) if i not in subset)
        matrix = []
        for left in triples:
            row = []
            for right in triples:
                word = [0] * 6
                for i, value in zip(subset, left):
                    word[i] = value
                for i, value in zip(complement, right):
                    word[i] = value
                row.append(h[tuple(word)])
            matrix.append(row)
        witness = next((dict(rows=ri, columns=ci,
                             matrix=[[matrix[i][j] for j in ci] for i in ri],
                             determinant=determinant([[matrix[i][j] for j in ci] for i in ri]))
                        for ri in combinations(range(6), 4)
                        for ci in combinations(range(6), 4)
                        if det_or_zero([[matrix[i][j] for j in ci] for i in ri])), None)
        assert witness is not None
        sectors.append(dict(leaf_subset=subset, complement=complement,
                            xor_sector=0, row_words=triples, column_words=triples,
                            target_matrix=matrix, nonzero_four_by_four_minor=witness,
                            two_edge_cut_rank_upper_bound=3))
    assert len(sectors) == 20

    return json.loads(json.dumps(dict(
        source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
        scope='Exact finite target-data witnesses for general paper reductions; no all-size graph enumeration.',
        zero_signature_exclusions=exclusions,
        zero_word_eligible_signature_indices=eligible,
        projective_kernel=rank,
        full_729_word_incidence_checked=True,
        conclusions=dict(
            count_only_target_forces_full_lift=True,
            target_count_ray_extreme_in_B6=True,
            bridge_leaf_sides='Only one leaf versus five leaves can occur.',
            two_edge_cut_three_three='Excluded by rank >=4 versus interface capacity 3 in XOR-zero sector.',
            two_leaf_side_reduction='In a vertex-minimal unmarked target source, no two-edge bond has a two-leaf side; four-pole decomposition leaves only direct wires.',
            actual_source_existence='OPEN', r2_exclusion='OPEN', new_forced_zero_coordinates=0),
        four_pole=dict(representative_words=four_words, representatives=representatives,
                       exact_count_decomposition='(a,b,c,d)=(alpha+beta,alpha+delta,gamma+delta,beta+gamma), with nonnegative actual full-12-signature weights.',
                       original_leaf_port_cases=[
                           dict(original_leaf_ports=[0, 1], direct_wires=['wire_03_12'],
                                equal_only=['wire_01_23'], different_only=['H_01_23'],
                                cross_H=['H_03_12']),
                           dict(original_leaf_ports=[0, 2], direct_wires=['wire_01_23', 'wire_03_12'],
                                equal_only=[], different_only=[],
                                cross_H=['H_01_23', 'H_03_12'])],
                       target_positive_unequal_leaf_pair_witnesses=unequal_leaf_pair_witnesses,
                       target_cross_H_triangle_witnesses=triangle_witnesses),
        bridge_flow_rows=bridge_rows,
        three_leaf_cut_sectors=sectors,
    ), sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    if args.check:
        assert json.loads(args.check.read_text()) == result
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(zero_signature_exclusions=168, eligible_signatures=23,
                         projective_rank=22, projective_minor_determinant=result['projective_kernel']['determinant'],
                         four_pole_representatives=4, cross_H_leaf_pair_exclusions=15,
                         bridge_compatible_leaf_subsets=12,
                         three_three_cut_exclusions=20,
                         actual_source_existence='OPEN', new_forced_zero_coordinates=0), sort_keys=True))


if __name__ == '__main__':
    main()
