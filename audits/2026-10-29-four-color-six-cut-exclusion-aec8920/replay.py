#!/usr/bin/env python3
"""Finite controls for the conditional six-edge-cut exclusion argument.

Standard library only.  This checks rim colourings, compressed incidence
patterns, and explicit planar source controls.  It does not enumerate planar
sources, prove the arbitrary-source topological argument, invoke a Four Colour
Theorem oracle, or import the production solver.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parent.parent
COLOURS = tuple(range(4))
PERMUTATIONS = tuple(permutations(COLOURS))


def normalize(row):
    labels = {}
    return tuple(labels.setdefault(value, len(labels)) for value in row)


def patterns(length):
    def visit(prefix):
        if len(prefix) == length:
            yield prefix
            return
        for value in range(min(2, max(prefix, default=-1) + 1) + 1):
            yield from visit(prefix + (value,))
    result = tuple(visit(()))
    literal_normalizations = {
        normalize(row) for row in product(COLOURS, repeat=length)
        if len(set(row)) <= 3
    }
    assert set(result) == literal_normalizations
    return result


def legal_permutations(left, right):
    cells = set(zip(left, right))
    return tuple(p for p in PERMUTATIONS
                 if all(a != p[b] for a, b in cells))


def forbidden_rectangles(left, right):
    cells = set(zip(left, right))
    result = []
    for height, width in ((2, 3), (3, 2)):
        for rows in combinations(sorted(set(left)), height):
            for columns in combinations(sorted(set(right)), width):
                rectangle = {(a, b) for a in rows for b in columns}
                if rectangle <= cells:
                    result.append((rectangle, rows, columns))
    return result


def audit_compressed_pairs(length):
    rows = patterns(length)
    counts = Counter()
    classes = Counter()
    histogram = Counter()
    incompatible_indices = []
    for li, left in enumerate(rows):
        for ri, right in enumerate(rows):
            choices = legal_permutations(left, right)
            rectangles = forbidden_rectangles(left, right)
            assert bool(choices) == (not rectangles)
            counts["ordered_pairs"] += 1
            histogram[len(choices)] += 1
            if choices:
                counts["compatible_pairs"] += 1
                continue
            counts["incompatible_pairs"] += 1
            incompatible_indices.append([li, ri])
            left_rank, right_rank = len(set(left)), len(set(right))
            orientation = f"{left_rank}_by_{right_rank}"
            counts[orientation] += 1
            left_multiplicities = sorted(Counter(left).values(), reverse=True)
            right_multiplicities = sorted(Counter(right).values(), reverse=True)
            label = ("".join(map(str, left_multiplicities)) + "_by_"
                     + "".join(map(str, right_multiplicities)))
            classes[label] += 1
            cells = set(zip(left, right))
            assert len(rectangles) == 1
            rectangle, rectangle_rows, rectangle_columns = rectangles[0]
            if length == 6:
                assert cells == rectangle
                assert sorted((left_rank, right_rank)) == [2, 3]
            elif sorted((left_rank, right_rank)) == [2, 3]:
                assert cells == rectangle and len(cells) == 6
                assert sorted(Counter(zip(left, right)).values()) == [1, 1, 1, 1, 1, 2]
            else:
                assert (left_rank, right_rank) == (3, 3)
                assert len(cells) == 7 and len(cells - rectangle) == 1
                extra = next(iter(cells - rectangle))
                if len(rectangle_rows) == 2:
                    assert extra[0] not in rectangle_rows
                    assert extra[1] in rectangle_columns
                else:
                    assert extra[0] in rectangle_rows
                    assert extra[1] not in rectangle_columns
    expected = {
        6: dict(ordered_pairs=14884, compatible_pairs=14764,
                incompatible_pairs=120, **{"2_by_3": 60, "3_by_2": 60}),
        7: dict(ordered_pairs=133225, compatible_pairs=128185,
                incompatible_pairs=5040,
                **{"2_by_3": 1260, "3_by_2": 1260, "3_by_3": 2520}),
    }
    assert counts == Counter(expected[length])
    return dict(
        incidence_count=length,
        boundary_colour_limit=3,
        canonical_pattern_count=len(rows),
        canonical_patterns=[list(row) for row in rows],
        counts=dict(sorted(counts.items())),
        incompatible_multiplicity_classes=dict(sorted(classes.items())),
        legal_permutation_histogram={str(k): v for k, v in sorted(histogram.items())},
        incompatible_pattern_indices=incompatible_indices,
        assertions=dict(
            canonical_rows_match_independent_literal_normalization=True,
            every_pair_checked_against_all_24_permutations=True,
            direct_permutation_decisions_match_rectangle_test=True,
            every_failure_has_exactly_one_Hall_rectangle=True,
            all_failed_supports_and_multiplicities_classified=True,
        ),
    )


def audit_rim_wheels():
    records = []
    for size in range(3, 7):
        counts = Counter()
        for colours in product(COLOURS, repeat=size + 1):
            hub, rim = colours[0], colours[1:]
            if hub in rim or any(rim[i] == rim[(i + 1) % size]
                                 for i in range(size)):
                continue
            rank = len(set(rim))
            counts["proper_wheel_colourings"] += 1
            counts[f"rim_rank_{rank}"] += 1
            assert rank in (2, 3)
            if rank == 2:
                assert size % 2 == 0
                assert all(rim[i] == rim[i % 2] for i in range(size))
                i, j, k, ell = 0, 1, 2, 3
                assert rim[i] == rim[k] and rim[j] == rim[ell]
                assert rim[i] != rim[j]
                counts["rank_two_has_four_distinct_alternating_terminals"] += 1
        assert counts["proper_wheel_colourings"] == 4 * (2 ** size + (-1) ** size * 2)
        assert counts["rim_rank_2"] == (24 if size % 2 == 0 else 0)
        records.append(dict(
            distinct_rim_vertices=size,
            literal_assignments_checked=4 ** (size + 1),
            counts=dict(sorted(counts.items())),
        ))
    return dict(
        records=records,
        scope="Literal colourings of wheels with 3..6 distinct rim vertices; no planar-source enumeration.",
        topological_crossing_assertion="Paper proof only: not discharged by this finite wheel enumeration.",
    )


def adjacency(vertex_count, edges):
    result = [set() for _ in range(vertex_count)]
    for u, v in edges:
        assert 0 <= u < vertex_count and 0 <= v < vertex_count and u != v
        result[u].add(v)
        result[v].add(u)
    return result


def proper(colours, edges):
    return all(colours[u] != colours[v] for u, v in edges)


def component(adj, colours, start, pair):
    assert colours[start] in pair
    found, pending = {start}, [start]
    while pending:
        u = pending.pop()
        for v in sorted(adj[u]):
            if v not in found and colours[v] in pair:
                found.add(v)
                pending.append(v)
    return sorted(found)


def audit_operational_swaps():
    records = []
    for size in (4, 6):
        edges = [(i, (i + 1) % size) for i in range(size)]
        before = [i % 2 for i in range(size)]
        adj = adjacency(size, edges)
        changed = component(adj, before, 0, (0, 2))
        assert changed == [0]
        after = before.copy()
        for vertex in changed:
            after[vertex] = 2 if before[vertex] == 0 else 0
        assert proper(before, edges) and proper(after, edges)
        assert len(set(before)) == 2 and len(set(after)) == 3
        assert before[2] == after[2] == 0
        records.append(dict(
            original_vertex_count=size,
            original_edges=[list(edge) for edge in edges],
            complete_side_colouring_before=before,
            literal_colour_pair=[0, 2],
            actual_component_swapped=changed,
            complete_side_colouring_after=after,
            boundary_rank_before=2,
            boundary_rank_after=3,
            assertions=dict(original_edges_proper_before_and_after=True,
                            one_actual_component_of_same_colouring_swapped=True),
        ))
    return records


def cross(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))


def on_segment(a, b, c):
    return (cross(a, b, c) == 0
            and min(a[0], b[0]) <= c[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))


def intersects(a, b, c, d):
    x1, x2, x3, x4 = cross(a, b, c), cross(a, b, d), cross(c, d, a), cross(c, d, b)
    return ((x1 * x2 < 0 and x3 * x4 < 0)
            or (x1 == 0 and on_segment(a, b, c))
            or (x2 == 0 and on_segment(a, b, d))
            or (x3 == 0 and on_segment(c, d, a))
            or (x4 == 0 and on_segment(c, d, b)))


def verify_straight_embedding(coordinates, edges):
    assert len(set(map(tuple, coordinates))) == len(coordinates)
    for u, v in edges:
        assert coordinates[u] != coordinates[v]
        for w in range(len(coordinates)):
            if w not in (u, v):
                assert not on_segment(coordinates[u], coordinates[v], coordinates[w])
    for first, second in combinations(edges, 2):
        if set(first) & set(second):
            continue
        assert not intersects(coordinates[first[0]], coordinates[first[1]],
                              coordinates[second[0]], coordinates[second[1]])


def audit_seven_planar_control():
    left = [0, 0, 0, 1, 1, 1, 2]
    right = [0, 1, 2, 0, 1, 2, 0]
    repaired_right = [1, 2, 1, 0, 2, 0, 1]
    coordinates = [[2 * i, 2] for i in range(7)]
    coordinates += [[2 * i, 0] for i in range(7)]
    edges, left_edges = [], []
    complete_left = left.copy()
    inserted_vertices = []
    for i in range(6):
        if left[i] == left[i + 1]:
            vertex = len(coordinates)
            coordinates.append([2 * i + 1, 2])
            inserted_vertices.append(vertex)
            left_edges.extend([(i, vertex), (vertex, i + 1)])
            complete_left.append(2)
        else:
            left_edges.append((i, i + 1))
    right_edges = [(7 + i, 8 + i) for i in range(6)]
    cross_edges = [(i, 7 + i) for i in range(7)]
    edges = left_edges + right_edges + cross_edges
    assert len(coordinates) == 18 and len(edges) == 23
    assert len(set(tuple(sorted(edge)) for edge in edges)) == len(edges)
    verify_straight_embedding(coordinates, edges)
    initial_colours = left + right + [2] * 4
    repaired_colours = left + repaired_right + [2] * 4
    assert proper(initial_colours, left_edges + right_edges)
    assert proper(repaired_colours, edges) and len(set(repaired_colours)) == 3
    assert not legal_permutations(left, right)
    forbidden = sorted(set(zip(left, right)))
    assert forbidden == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0)]
    return dict(
        vertex_count=len(coordinates),
        edge_count=len(edges),
        coordinates=coordinates,
        original_edges=[list(edge) for edge in edges],
        left_vertices=list(range(7)) + inserted_vertices,
        right_vertices=list(range(7, 14)),
        ordered_cross_edges=[list(edge) for edge in cross_edges],
        left_complete_side_colouring=dict(zip(map(str, list(range(7)) + inserted_vertices), complete_left)),
        right_complete_side_colouring={str(i + 7): colour for i, colour in enumerate(right)},
        ordered_left_incidence_colours=left,
        ordered_right_incidence_colours=right,
        forbidden_cells=[list(cell) for cell in forbidden],
        legal_whole_side_permutation_count=0,
        full_original_graph_three_colouring=repaired_colours,
        assertions=dict(
            integer_straight_line_embedding_verified_without_crossings=True,
            both_initial_side_colourings_complete_and_proper=True,
            seven_forbidden_cells_are_rectangle_plus_one_third_row_cell=True,
            both_boundary_colour_ranks_equal_three=True,
            all_24_whole_side_permutations_fail=True,
            repaired_colouring_checked_against_every_original_edge=True,
        ),
        scope="One pair of complete side colourings in a colourable planar source; not a minimal counterexample or all-family lock.",
    )


def source_hashes():
    paths = [Path(__file__).resolve(),
             ROOT / "docs/four_color_six_cut_exclusion.md",
             ROOT / "docs/four_color_six_edge_cuts.md",
             ROOT / "audits/2026-10-26-four-color-six-edge-cuts-8d28acc/replay.py"]
    return {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in paths}


def build_report():
    return dict(
        schema="four-colour-six-cut-exclusion-finite-controls-v1",
        source_sha256=source_hashes(),
        evidence_layer="Python finite enumeration and explicit original-edge controls; arbitrary planar-source exclusion remains a paper proof.",
        production_solver_imported=False,
        four_colour_theorem_oracle_used=False,
        rim_wheels=audit_rim_wheels(),
        same_witness_cycle_component_swaps=audit_operational_swaps(),
        six_compressed_incidence_pairs=audit_compressed_pairs(6),
        seven_compressed_incidence_pairs=audit_compressed_pairs(7),
        seven_edge_planar_negative_control=audit_seven_planar_control(),
        boundaries=dict(
            arbitrary_planar_sources_enumerated=False,
            topological_rim_crossing_argument_formally_verified=False,
            two_separator_planar_gluing_argument_formally_verified=False,
            Lean_theorems_added=False,
            seven_cut_excluded=False,
            mask_932_excluded=False,
        ),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = build_report()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(dict(
        output=str(args.out),
        six_counts=report["six_compressed_incidence_pairs"]["counts"],
        seven_counts=report["seven_compressed_incidence_pairs"]["counts"],
        wheel_counts=[record["counts"] for record in report["rim_wheels"]["records"]],
        planar_control_vertices=report["seven_edge_planar_negative_control"]["vertex_count"],
        planar_control_edges=report["seven_edge_planar_negative_control"]["edge_count"],
    ), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
