#!/usr/bin/env python3
"""Exact colour-permutation gluing across at most five cut incidences.

The two ordered incidence tuples are literal colour observations from two
actual side colourings. Only one common permutation of the entire second side
is permitted. This finite lemma does not splice marginal side supports, assert
that side tuples are realizable, or authorize arbitrary swaps under fixed/list
domains. No production solver or external package is imported.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path


AUDIT = Path(__file__).resolve().parent
PALETTE = tuple(range(4))
PERMUTATIONS = tuple(permutations(PALETTE))


def normalize(row):
    labels = {}
    return tuple(labels.setdefault(colour, len(labels)) for colour in row)


def canonical_patterns(length):
    """Restricted-growth words representing S4-orbits, at most four blocks."""
    def visit(prefix, maximum):
        if len(prefix) == length:
            yield tuple(prefix)
            return
        for value in range(min(maximum + 1, 3) + 1):
            yield from visit(prefix + [value], max(maximum, value))
    return tuple(visit([], -1))


def partition_type(row):
    return tuple(sorted(Counter(row).values(), reverse=True))


def compatible_permutations(left, right):
    return tuple(permutation for permutation in PERMUTATIONS
                 if all(a != permutation[b] for a, b in zip(left, right)))


def inclusion_exclusion_count(left, right):
    """Count allowed bijections independently through collision events.

    The collision event for a distinct cell (a,b) is pi(b)=a. An intersection
    contributes (4-k)! precisely when its k cells use distinct rows/columns;
    inconsistent event intersections contribute zero.
    """
    cells = tuple(sorted(set(zip(left, right))))
    result = 0
    for size in range(len(cells) + 1):
        for chosen in combinations(cells, size):
            if len({a for a, _ in chosen}) != size or len({b for _, b in chosen}) != size:
                continue
            result += (-1) ** size * factorial(4 - size)
    return result


def four_position_obstructions(left, right):
    records = []
    for positions in combinations(range(len(left)), 4):
        a = {left[i] for i in positions}
        b = {right[i] for i in positions}
        if len(a) == 1 and len(b) == 4:
            records.append(dict(positions=list(positions),
                                orientation="left_constant_right_rainbow"))
        if len(a) == 4 and len(b) == 1:
            records.append(dict(positions=list(positions),
                                orientation="left_rainbow_right_constant"))
    return records


def forbidden_lines(left, right):
    cells = set(zip(left, right))
    full_rows = [a for a in PALETTE if all((a, b) in cells for b in PALETTE)]
    full_columns = [b for b in PALETTE if all((a, b) in cells for a in PALETTE)]
    return cells, full_rows, full_columns


def hall_witnesses(left, right):
    """Enumerate all Hall failures of the independent 4x4 allowed matrix."""
    forbidden = set(zip(left, right))
    result = []
    for size in range(1, 5):
        for rows in combinations(PALETTE, size):
            neighbours = sorted(b for b in PALETTE
                                if any((a, b) not in forbidden for a in rows))
            if len(neighbours) < size:
                result.append(dict(rows=list(rows), allowed_columns=neighbours))
    return result


def audit_length(length):
    patterns = canonical_patterns(length)
    literal_patterns = {normalize(row) for row in product(PALETTE, repeat=length)}
    assert set(patterns) == literal_patterns
    assert len(patterns) == (1, 1, 2, 5, 15, 51)[length]
    incompatible = []
    legal_count_histogram = Counter()
    oriented_type_histogram = Counter()
    for left_index, left in enumerate(patterns):
        for right_index, right in enumerate(patterns):
            choices = compatible_permutations(left, right)
            count = inclusion_exclusion_count(left, right)
            assert count == len(choices)
            legal_count_histogram[count] += 1
            cells, full_rows, full_columns = forbidden_lines(left, right)
            obstructions = four_position_obstructions(left, right)
            hall = hall_witnesses(left, right)
            assert bool(choices) == (not hall)
            assert bool(choices) == (not (full_rows or full_columns))
            assert bool(choices) == (not obstructions)
            if length <= 3:
                assert choices
            if length == 4:
                predicted = ((partition_type(left) == (4,) and partition_type(right) == (1, 1, 1, 1))
                             or (partition_type(right) == (4,) and partition_type(left) == (1, 1, 1, 1)))
                assert (not choices) == predicted
            if not choices:
                left_type, right_type = partition_type(left), partition_type(right)
                if length == 5:
                    left_family = left_type in ((5,), (4, 1))
                    right_family = right_type in ((5,), (4, 1))
                    assert ((left_family and right_type == (2, 1, 1, 1))
                            or (right_family and left_type == (2, 1, 1, 1)))
                type_key = "+".join(map(str, left_type)) + " / " + "+".join(map(str, right_type))
                oriented_type_histogram[type_key] += 1
                incompatible.append(dict(left_index=left_index, right_index=right_index,
                                         left=list(left), right=list(right),
                                         left_type=list(left_type), right_type=list(right_type),
                                         forbidden_cells=[list(cell) for cell in sorted(cells)],
                                         full_forbidden_rows=full_rows,
                                         full_forbidden_columns=full_columns,
                                         four_position_obstructions=obstructions,
                                         hall_witnesses=hall,
                                         legal_permutation_count=count))
    assert len(incompatible) == (0, 0, 0, 0, 2, 60)[length]
    return dict(length=length, patterns=[list(p) for p in patterns],
                pattern_count=len(patterns), ordered_pattern_pairs=len(patterns) ** 2,
                incompatible_count=len(incompatible), compatible_count=len(patterns) ** 2 - len(incompatible),
                incompatible_pairs=incompatible,
                legal_permutation_count_histogram={str(k): v for k, v in sorted(legal_count_histogram.items())},
                incompatible_oriented_type_histogram=dict(sorted(oriented_type_histogram.items())),
                literal_tuple_universe=4 ** length,
                canonical_patterns_independently_match_all_literal_tuples=True,
                all_permutation_counts_match_independent_inclusion_exclusion=True,
                all_pair_decisions_match_independent_Hall_enumeration=True,
                all_pair_decisions_match_four_position_criterion=True)


def positional_negative_control():
    # The same L/R partition types can be compatible or incompatible: whether
    # the four constant positions see all four opposite colours matters.
    left = (0, 0, 0, 0, 1)
    bad_right = (0, 1, 2, 3, 0)
    good_right = (0, 0, 1, 2, 3)
    assert partition_type(bad_right) == partition_type(good_right) == (2, 1, 1, 1)
    assert not compatible_permutations(left, bad_right)
    good = compatible_permutations(left, good_right)
    assert good
    return dict(left=list(left), left_type=list(partition_type(left)),
                incompatible_right=list(bad_right), compatible_right=list(good_right),
                common_right_type=list(partition_type(good_right)),
                compatible_witness_permutation=list(good[0]),
                compatible_permutation_count=len(good),
                assertion="L/R type membership alone is not sufficient; the same four positions are required.")


def six_incidence_control():
    """One sharp boundary example, not a classification of six incidences."""
    left = (0, 0, 0, 1, 1, 1)
    right = (0, 1, 2, 0, 1, 2)
    choices = compatible_permutations(left, right)
    count = inclusion_exclusion_count(left, right)
    hall = hall_witnesses(left, right)
    cells, full_rows, full_columns = forbidden_lines(left, right)
    obstructions = four_position_obstructions(left, right)
    assert not choices and count == 0 and hall
    assert cells == set(product(range(2), range(3)))
    assert not full_rows and not full_columns and not obstructions
    assert hall == [dict(rows=[0, 1], allowed_columns=[3])]
    assert len(set(left)) == 2 and len(set(right)) == 3
    # K5 split into a K2 and K3 has exactly these six crossing incidences.
    # This example is not a planar source: 10 edges exceed 3*5-6 = 9.
    edges = [list(edge) for edge in combinations(range(5), 2)]
    crossing_edges = [[x, y] for x in (0, 1) for y in (2, 3, 4)]
    assert [x for x, _ in crossing_edges] == list(left)
    assert [y - 2 for _, y in crossing_edges] == list(right)
    return dict(name="six_incidence_two_by_three_forbidden_rectangle",
                left=list(left), right=list(right), left_type=list(partition_type(left)),
                right_type=list(partition_type(right)), side_colour_counts=[2, 3],
                forbidden_cells=[list(cell) for cell in sorted(cells)],
                forbidden_rectangle=dict(rows=[0, 1], columns=[0, 1, 2]),
                full_forbidden_rows=full_rows, full_forbidden_columns=full_columns,
                four_position_obstructions=obstructions, hall_witnesses=hall,
                legal_permutation_count=len(choices), independent_inclusion_exclusion_count=count,
                permutation_trials=len(PERMUTATIONS),
                abstract_graph_control=dict(name="K5 split into K2 and K3",
                                            vertices=list(range(5)), edges=edges,
                                            left_vertices=[0, 1], right_vertices=[2, 3, 4],
                                            crossing_edges=crossing_edges,
                                            planar_edge_bound_failed=len(edges) > 3 * 5 - 6,
                                            planar_realization=False),
                assertions=dict(all_24_permutations_fail=True,
                                independent_inclusion_exclusion_also_zero=True,
                                independent_Hall_failure_is_two_rows_one_allowed_column=True,
                                forbidden_cells_are_exactly_two_by_three_rectangle=True,
                                no_full_forbidden_row_or_column=True,
                                neither_side_is_rainbow=True,
                                six_incidence_global_enumeration_performed=False),
                scope="One named t=6 sharp-boundary control only; no classification of all six-incidence pairs or planar six-cuts.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=AUDIT / "cut_report.json")
    args = parser.parse_args()
    records = [audit_length(length) for length in range(6)]
    report = dict(source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  permutations=[list(p) for p in PERMUTATIONS], lengths=records,
                  positional_negative_control=positional_negative_control(),
                  named_six_incidence_control=six_incidence_control(),
                  proof=dict(forbidden_cell="(a,b) forbids pi(b)=a; at most t distinct forbidden cells.",
                             Hall_rectangle_sizes=[dict(rows=k, columns=5-k, forbidden_cells=k*(5-k))
                                                   for k in range(1, 5)],
                             at_most_five_cells="A Hall failure with 2 or 3 rows needs at least 6 forbidden cells. With at most 5, failure is exactly a full forbidden row or column.",
                             four_position_form="A full forbidden row/column is equivalent to four incidence positions that are constant on one side and use all four colours on the other."),
                  assertions=dict(all_lengths_zero_through_five_exhausted=True,
                                  canonical_pattern_counts=[r["pattern_count"] for r in records],
                                  ordered_pattern_pairs=sum(r["ordered_pattern_pairs"] for r in records),
                                  no_incompatible_pairs_for_at_most_three_incidences=True,
                                  length_four_only_mono_rainbow_in_both_orientations=True,
                                  length_five_exact_four_position_obstruction=True,
                                  length_five_type_families_necessary_but_not_sufficient=True,
                                  all_legal_counts_independently_checked_by_inclusion_exclusion=True,
                                  every_decision_independently_checked_by_Hall=True,
                                  one_named_six_incidence_sharp_boundary_control_checked=True),
                  scope="Complete enumeration for two actual ordered side-incidence colour tuples, one common S4 permutation of the entire second side, and at most five cut incidences. One named t=6 control is separately marked; there is no t=6 classification. No side realizability oracle, marginal splicing, list/fixed-domain permutation permission, larger-cut theorem, planar 4CT, or 932 exclusion claim.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(report, sort_keys=True, indent=2) + "\n"
    args.out.write_text(encoded)
    for record in records:
        print(json.dumps({key: record[key] for key in ("length", "pattern_count", "ordered_pattern_pairs",
                                                      "compatible_count", "incompatible_count")}, sort_keys=True))
    print(json.dumps(dict(output=str(args.out), sha256=sha256(encoded.encode()).hexdigest())))


if __name__ == "__main__":
    main()
