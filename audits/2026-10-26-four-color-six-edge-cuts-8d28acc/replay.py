#!/usr/bin/env python3
"""Independent six-incidence colour-permutation audit and planar controls.

This script uses only the standard library. It does not import the production
solver, a planar graph catalogue, or a Four Colour Theorem oracle. A side row
is an ordered observation from one complete side colouring, not six
independent choices. Side-pattern enumeration does not assert realizability.
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
COLOURS = tuple(range(4))
PERMUTATIONS = tuple(permutations(COLOURS))


def normalize(row):
    labels = {}
    return tuple(labels.setdefault(value, len(labels)) for value in row)


def patterns(length):
    def visit(prefix, maximum):
        if len(prefix) == length:
            yield tuple(prefix)
            return
        for value in range(min(maximum + 1, 3) + 1):
            yield from visit(prefix + [value], max(maximum, value))
    rows = tuple(visit([], -1))
    assert set(rows) == {normalize(row) for row in product(COLOURS, repeat=length)}
    return rows


def allowed_permutations(left, right):
    return tuple(p for p in PERMUTATIONS
                 if all(a != p[b] for a, b in zip(left, right)))


def inclusion_exclusion_count(forbidden):
    """Independent collision-event count, including repeated-cell handling."""
    result = 0
    cells = sorted(forbidden)
    for size in range(len(cells) + 1):
        for chosen in combinations(cells, size):
            if (len({a for a, _ in chosen}) != size
                    or len({b for _, b in chosen}) != size):
                continue
            result += (-1) ** size * factorial(4 - size)
    return result


def hall_failures(forbidden):
    failures = []
    for size in range(1, 5):
        for rows in combinations(COLOURS, size):
            allowed = [b for b in COLOURS
                       if any((a, b) not in forbidden for a in rows)]
            if len(allowed) < size:
                failures.append(dict(rows=list(rows), allowed_columns=allowed))
    return failures


def full_lines(forbidden):
    rows = [a for a in COLOURS if all((a, b) in forbidden for b in COLOURS)]
    columns = [b for b in COLOURS if all((a, b) in forbidden for a in COLOURS)]
    return rows, columns


def rectangles(forbidden):
    result = []
    for size in (2, 3):
        for rows in combinations(COLOURS, size):
            for columns in combinations(COLOURS, 5 - size):
                if all((a, b) in forbidden for a in rows for b in columns):
                    result.append(dict(rows=list(rows), columns=list(columns)))
    return result


def audit_patterns():
    rows = patterns(6)
    assert len(rows) == 187
    counts = Counter()
    legal_histogram = Counter()
    rectangle_records = []
    incompatible_indices = []
    for li, left in enumerate(rows):
        for ri, right in enumerate(rows):
            forbidden = set(zip(left, right))
            choices = allowed_permutations(left, right)
            independent_count = inclusion_exclusion_count(forbidden)
            hall = hall_failures(forbidden)
            full_rows, full_columns = full_lines(forbidden)
            rectangle_list = rectangles(forbidden)
            star = bool(full_rows or full_columns)
            assert independent_count == len(choices)
            assert bool(choices) == (not hall)
            assert bool(choices) == (not (star or rectangle_list))
            counts["ordered_pairs"] += 1
            legal_histogram[len(choices)] += 1
            if choices:
                counts["compatible_pairs"] += 1
                continue
            counts["incompatible_pairs"] += 1
            incompatible_indices.append([li, ri])
            if star:
                counts["star_pairs"] += 1
                assert not rectangle_list
                continue
            counts["nonstar_rectangle_pairs"] += 1
            assert len(forbidden) == 6 and len(rectangle_list) == 1
            assert sorted((len(set(left)), len(set(right)))) == [2, 3]
            orientation = f"{len(set(left))}_by_{len(set(right))}"
            counts[orientation] += 1
            left_blocks = sorted(Counter(left).values())
            right_blocks = sorted(Counter(right).values())
            assert sorted((left_blocks, right_blocks)) == [[2, 2, 2], [3, 3]]
            rectangle_records.append(dict(
                left_index=li, right_index=ri, left=list(left), right=list(right),
                left_colour_count=len(set(left)), right_colour_count=len(set(right)),
                forbidden_cells=[list(cell) for cell in sorted(forbidden)],
                rectangle=rectangle_list[0], hall_failures=hall,
                colour_pair_multiplicities=[dict(left=a, right=b, count=n)
                                           for (a, b), n in sorted(Counter(zip(left, right)).items())],
                legal_permutation_count=0))
    assert counts == Counter(ordered_pairs=34969, compatible_pairs=33279,
                             incompatible_pairs=1690, star_pairs=1570,
                             nonstar_rectangle_pairs=120,
                             **{"2_by_3": 60, "3_by_2": 60})
    return dict(
        length=6, canonical_pattern_count=len(rows),
        canonical_patterns=[list(row) for row in rows],
        literal_tuple_universe=4 ** 6,
        counts=dict(sorted(counts.items())),
        legal_permutation_histogram={str(k): v for k, v in sorted(legal_histogram.items())},
        incompatible_pattern_indices=incompatible_indices,
        nonstar_rectangle_records=rectangle_records,
        assertions=dict(
            canonical_patterns_match_independent_literal_enumeration=True,
            all_24_permutations_checked_for_every_ordered_pair=True,
            all_counts_match_independent_inclusion_exclusion=True,
            all_decisions_match_independent_Hall_enumeration=True,
            all_failures_are_stars_or_exact_six_cell_rectangles=True,
            all_nonstar_failures_have_each_colour_pair_exactly_once=True))


def valid_colouring(vertices, edges, colouring):
    return (set(colouring) == set(vertices)
            and all(colouring[v] in COLOURS for v in vertices)
            and all(colouring[a] != colouring[b] for a, b in edges))


def component(vertices, edges, colouring, colours, root):
    allowed = {v for v in vertices if colouring[v] in colours}
    assert root in allowed
    neighbours = {v: [] for v in allowed}
    for a, b in edges:
        if a in allowed and b in allowed:
            neighbours[a].append(b)
            neighbours[b].append(a)
    reached = {root}
    queue = [root]
    for v in queue:
        for w in neighbours[v]:
            if w not in reached:
                reached.add(w)
                queue.append(w)
    return sorted(reached)


def orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segments_intersect(a, b, c, d):
    if (max(a[0], b[0]) < min(c[0], d[0])
            or max(c[0], d[0]) < min(a[0], b[0])
            or max(a[1], b[1]) < min(c[1], d[1])
            or max(c[1], d[1]) < min(a[1], b[1])):
        return False
    return (orientation(a, b, c) * orientation(a, b, d) <= 0
            and orientation(c, d, a) * orientation(c, d, b) <= 0)


def planar_source_control():
    """A subdivided ladder: a bad selected pair, but a colourable source."""
    top = [f"x{i}" for i in range(6)]
    bottom = [f"y{i}" for i in range(6)]
    subdivisions = [f"s{i}" for i in (0, 1, 3, 4)]
    left_vertices = top + subdivisions
    left_edges = []
    coordinates = {v: [2 * i, 2] for i, v in enumerate(top)}
    coordinates.update({v: [2 * i, 0] for i, v in enumerate(bottom)})
    for i in range(5):
        if i == 2:
            left_edges.append([top[i], top[i + 1]])
        else:
            middle = f"s{i}"
            coordinates[middle] = [2 * i + 1, 2]
            left_edges.extend([[top[i], middle], [middle, top[i + 1]]])
    right_edges = [[bottom[i], bottom[i + 1]] for i in range(5)]
    cut = [[top[i], bottom[i]] for i in range(6)]
    vertices = left_vertices + bottom
    edges = left_edges + right_edges + cut
    for a, b in edges:
        for v in vertices:
            if v not in (a, b):
                assert not (orientation(coordinates[a], coordinates[b], coordinates[v]) == 0
                            and min(coordinates[a][0], coordinates[b][0]) <= coordinates[v][0] <= max(coordinates[a][0], coordinates[b][0])
                            and min(coordinates[a][1], coordinates[b][1]) <= coordinates[v][1] <= max(coordinates[a][1], coordinates[b][1]))
    for first, second in combinations(edges, 2):
        if set(first).isdisjoint(second):
            assert not segments_intersect(*(coordinates[v] for v in first + second))
    left = {v: (0 if i < 3 else 1) for i, v in enumerate(top)}
    left.update({v: 2 for v in subdivisions})
    right = {v: i % 3 for i, v in enumerate(bottom)}
    assert valid_colouring(left_vertices, left_edges, left)
    assert valid_colouring(bottom, right_edges, right)
    a, b = tuple(left[v] for v in top), tuple(right[v] for v in bottom)
    assert a == (0, 0, 0, 1, 1, 1) and b == (0, 1, 2, 0, 1, 2)
    assert not allowed_permutations(a, b)
    repaired_right = dict(zip(bottom, (1, 2, 1, 0, 2, 0)))
    complete = left | repaired_right
    assert valid_colouring(vertices, edges, complete)
    # Unused boundary colour 3 has no vertices in this selected left colouring.
    # Its {0,3} component at x0 contains a proper subset of the 0-terminals.
    kempe_component = component(left_vertices, left_edges, left, {0, 3}, "x0")
    assert kempe_component == ["x0"]
    changed_left = dict(left)
    for v in kempe_component:
        changed_left[v] = 3 if left[v] == 0 else 0
    assert valid_colouring(left_vertices, left_edges, changed_left)
    changed_row = tuple(changed_left[v] for v in top)
    assert len(set(changed_row)) == 3
    choices = allowed_permutations(changed_row, b)
    assert choices
    changed_complete = changed_left | {v: choices[0][right[v]] for v in bottom}
    assert valid_colouring(vertices, edges, changed_complete)
    return dict(
        name="subdivided_ladder_selected_rectangle_is_not_uncolourability",
        vertices=vertices, edges=edges, left_vertices=left_vertices,
        right_vertices=bottom, crossing_edges=cut, coordinates=coordinates,
        left_side_colouring=left, right_side_colouring=right,
        selected_left_row=list(a), selected_right_row=list(b),
        selected_pair_legal_permutation_count=0,
        complete_three_colouring=complete,
        kempe_repair=dict(colour_pair=[0, 3], component=kempe_component,
                          changed_left_colouring=changed_left,
                          changed_boundary_row=list(changed_row),
                          compatible_whole_right_permutation=list(choices[0]),
                          complete_colouring=changed_complete),
        assertions=dict(
            both_sides_connected_paths=True,
            six_crossing_edges=True,
            integer_straight_line_drawing_has_no_crossings_or_vertex_on_edge=True,
            selected_side_colourings_are_complete_and_proper=True,
            selected_rectangle_pair_fails_all_common_permutations=True,
            whole_graph_has_verified_three_colouring=True,
            one_actual_Kempe_component_breaks_two_colour_boundary_lock=True),
        scope="A source-level negative control, not a minimal counterexample.")


def positional_control():
    left = (0, 0, 0, 1, 1, 1)
    bad = (0, 1, 2, 0, 1, 2)
    good = (0, 0, 1, 1, 2, 2)
    assert Counter(bad) == Counter(good)
    assert not allowed_permutations(left, bad)
    choices = allowed_permutations(left, good)
    assert len(choices) == 6
    return dict(left=list(left), incompatible_right=list(bad),
                compatible_right=list(good),
                right_multiplicities=[2, 2, 2],
                legal_permutation_count=len(choices),
                witness_permutation=list(choices[0]))


def fixed_colour_control():
    choices = allowed_permutations((0,), (0,))
    preserving = [p for p in PERMUTATIONS if p[0] == 0]
    assert choices and not [p for p in preserving if 0 != p[0]]
    return dict(vertices=["x", "y"], edges=[["x", "y"]],
                fixed_colours={"x": 0, "y": 0},
                unrestricted_permutation_count=len(choices),
                domain_preserving_legal_permutation_count=0,
                assertion="The naked-colour permutation theorem does not apply to arbitrary fixed/list domains.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=AUDIT / "report.json")
    args = parser.parse_args()
    report = dict(
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        permutations=[list(p) for p in PERMUTATIONS],
        six_incidence_audit=audit_patterns(),
        positional_negative_control=positional_control(),
        planar_source_negative_control=planar_source_control(),
        fixed_colour_negative_control=fixed_colour_control(),
        proof_scope=dict(
            finite_audit="All 187^2 six-incidence equality-pattern pairs and all 24 whole-side permutations.",
            conditional_planar_theorem="Paper proof only: a hypothetical vertex-minimal naked planar counterexample has nonempty compressed side-colouring families, fixed 2/3 orientation, and the stated two-colour-side Kempe connectivity.",
            not_claimed=["a realization of a planar uncolourable source", "six-edge-cut exclusion", "932 exclusion", "a Four Colour Theorem proof", "Lean formalization", "production solver modification"]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["six_incidence_audit"]["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
