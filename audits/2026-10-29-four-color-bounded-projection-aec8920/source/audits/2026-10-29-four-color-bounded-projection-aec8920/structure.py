"""Independent finite support and structural cost audit (standard library only).

This module does not import the proposed bounded-projection implementation.
Its rows/cells are representation counts, not solver checks, time, or RSS.
Source contract: docs/four_color_mathematical_optimization.md:32-46;
current monolithic construction: scripts/four_color_constraints.py:1373-1511.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import reduce
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def _meet(masks):
    return reduce(int.__and__, masks, 15)


def _bounded_groups(family):
    return tuple(combinations(family, min(4, len(family))))


def _anchored_groups(family, anchor, cap=None):
    others = tuple(mask for mask in family if mask != anchor)
    width = min(anchor.bit_count() if cap is None else cap, len(others))
    return tuple((anchor,) + subset for subset in combinations(others, width))


def _support_audit():
    families = anchors = bounded_groups = anchored_groups = uniform_cap_cases = 0
    minimal_empty = []
    for size in range(6):
        for family in combinations(range(16), size):
            families += 1
            expected = _meet(family)
            groups = _bounded_groups(family)
            bounded_groups += len(groups)
            assert bool(expected) == all(_meet(group) != 0 for group in groups)
            assert expected == _meet(_meet(group) for group in groups)
            if family and not expected and all(
                _meet(family[:i] + family[i + 1 :]) for i in range(size)
            ):
                minimal_empty.append(family)
            for anchor in family:
                anchors += 1
                groups = _anchored_groups(family, anchor)
                anchored_groups += len(groups)
                assert bool(expected) == all(_meet(group) != 0 for group in groups)
                assert expected == _meet(_meet(group) for group in groups)
                # A table's uniform support cap can exceed this row's actual
                # support size. Check all such valid caps, not only tight ones.
                for cap in range(anchor.bit_count(), 5):
                    groups = _anchored_groups(family, anchor, cap)
                    uniform_cap_cases += 1
                    assert bool(expected) == all(_meet(group) != 0 for group in groups)
                    assert expected == _meet(_meet(group) for group in groups)
    assert len(minimal_empty) == 49
    assert Counter(map(len, minimal_empty)) == {1: 1, 2: 25, 3: 22, 4: 1}
    extremal = (7, 11, 13, 14)
    assert _meet(extremal) == 0
    assert all(_meet(subset) for subset in combinations(extremal, 3))
    return {
        "scope": "all distinct four-bit mask families of cardinality zero through five",
        "families": families,
        "anchor_cases": anchors,
        "bounded_subfamilies_checked": bounded_groups,
        "anchored_subfamilies_checked": anchored_groups,
        "valid_uniform_anchor_cap_cases": uniform_cap_cases,
        "complete_fibre_intersections_equal": True,
        "duplicate_masks": "redundant under intersection; not distinct additional cases",
        "minimal_empty_count": len(minimal_empty),
        "minimal_empty_by_size": {
            str(size): count for size, count in sorted(Counter(map(len, minimal_empty)).items())
        },
        "minimal_empty_families": [list(family) for family in minimal_empty],
        "four_factor_necessity": {
            "masks": list(extremal),
            "intersection": 0,
            "every_triple_nonempty": True,
            "graph_control": "K1,4; distinct leaf colours 0,1,2,3; no centre colour",
        },
    }


def _star_audit():
    direct = []
    for degree in range(9):
        rows = fibres = 0
        for boundary in product(range(4), repeat=degree):
            # Direct original-edge check, without mask compiler or projection code.
            choices = tuple(colour for colour in range(4)
                            if all(colour != leaf for leaf in boundary))
            rows += bool(choices)
            fibres += len(choices)
        expected_rows = 1 if degree == 0 else 4 * 3**degree - 6 * 2**degree + 4
        assert rows == expected_rows
        assert fibres == 4 * 3**degree
        direct.append({"degree": degree, "allowed_boundary_rows": rows,
                       "original_graph_solutions": fibres})
    no_rainbow = tuple(boundary for boundary in product(range(4), repeat=4)
                       if any(all(colour != leaf for leaf in boundary)
                              for colour in range(4)))
    assert len(no_rainbow) == 232
    costs = []
    for degree in range(4, 13):
        monolithic = 4 * 3**degree - 6 * 2**degree + 4
        bounded_count = comb(degree, 4)
        anchored_count = comb(degree - 1, 3)
        costs.append({
            "degree": degree,
            "monolithic_projection": {"factors": 1, "allowed_rows": monolithic,
                                       "boundary_cells": degree * monolithic},
            "all_four_subsets": {"factors": bounded_count,
                                 "allowed_rows": 232 * bounded_count,
                                 "boundary_cells": 4 * 232 * bounded_count},
            "anchored_four_subsets": {"factors": anchored_count,
                                      "allowed_rows": 232 * anchored_count,
                                      "boundary_cells": 4 * 232 * anchored_count},
        })
    return {
        "direct_original_edge_enumeration": direct,
        "four_leaf_factor_allowed_rows": 232,
        "degree_four_through_twelve": costs,
        "first_strict_allowed_row_saving": {"all_four_subsets": 8,
                                             "anchored_four_subsets": 6},
        "tautological_projection_degrees": [0, 1, 2, 3],
        "tautology_contract": "raw edge bucket; centre has all four colours; keep full history recipe",
        "cost_exclusions": ["history recipe", "factor metadata", "source snapshots",
                            "deduplication", "construction work", "later elimination", "RSS"],
        "order_caveat": "forced centre-first control; current min-fill selects star leaves first",
    }


def _shared_assignment_control():
    # The remaining two four-colour coordinates encode five different cases.
    # In case j, factor j alone removes colour 0. Other factors remove 1,2,3,1.
    # Every four-factor projection has a witness in its own case, while no
    # common boundary assignment satisfies all five projections together.
    boundaries = tuple(product(range(4), repeat=2))
    family_by_boundary = []
    for case, boundary in enumerate(boundaries):
        singleton_zero = case % 5
        forbidden = [None] * 5
        forbidden[singleton_zero] = 0
        for factor, colour in zip((i for i in range(5) if i != singleton_zero), (1, 2, 3, 1)):
            forbidden[factor] = colour
        family = tuple(15 ^ (1 << colour) for colour in forbidden)
        assert _meet(family) == 0
        family_by_boundary.append((boundary, family))
    projected = []
    for indices in combinations(range(5), 4):
        rows = tuple(boundary for boundary, family in family_by_boundary
                     if _meet(family[i] for i in indices))
        assert rows
        projected.append({"factor_indices": list(indices),
                          "allowed_boundary_rows": [list(row) for row in rows]})
    joint = set(boundaries)
    for factor in projected:
        joint &= {tuple(row) for row in factor["allowed_boundary_rows"]}
    assert not joint
    return {"variables": ["x", "u", "v"], "bucket_factors": 5,
            "four_factor_projections": projected,
            "each_projection_nonempty": True, "their_common_join_rows": 0,
            "lesson": "nonemptiness witnesses for different subprojections cannot use different boundary assignments"}


def _planar_two_step_growth():
    rows = []
    for degree in range(4, 13):
        first = comb(degree - 1, 3)
        next_width = min(3, first)
        second = comb(first, next_width)
        row = {"degree": degree, "first_generated_factors": first,
               "second_generated_candidate_factors": second,
               "second_max_scope_upper_bound": min(degree, 10)}
        if degree <= 8:
            first_scopes = tuple(combinations(range(1, degree), 3))
            histogram = Counter()
            scopes = set()
            for subset in combinations(first_scopes, next_width):
                scope = frozenset().union(*subset)
                # One additional coordinate is the surviving other hub z.
                histogram[len(scope) + 1] += 1
                scopes.add(scope)
            assert sum(histogram.values()) == second
            row["second_scope_size_histogram"] = {
                str(size): count for size, count in sorted(histogram.items())}
            row["second_distinct_scopes"] = len(scopes)
        rows.append(row)
    return {
        "original_graph": "planar K_(2,d), hubs x,z and leaves y0,...,y(d-1)",
        "forced_order": ["x", "y0"],
        "first_anchor": "original edge x-y0; conditional support size at most three",
        "second_anchor": "original edge y0-z; conditional support size at most three",
        "first_factors": "C(d-1,3) no-rainbow factors; every scope contains y0",
        "second_factors": "C(C(d-1,3), min(3,C(d-1,3))) unsimplified candidates",
        "counts": rows,
        "limits": "candidate counts before scope merging or relation deduplication; not unavoidable storage or runtime lower bounds",
    }


def run():
    return {"audit": "independent finite support and structural representation audit",
            "support": _support_audit(), "stars": _star_audit(),
            "shared_assignment_negative_control": _shared_assignment_control(),
            "planar_two_step_growth": _planar_two_step_growth()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = run()
    payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out:
        with args.out.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
