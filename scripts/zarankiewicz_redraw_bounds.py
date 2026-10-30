#!/usr/bin/env python3
"""Exact arithmetic controls for the local-redrawing research note.

This does not enumerate or certify plane drawings. The uniform tensor is a
fractional relaxation control, not a geometric counterexample.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb


def axis_pairs(n: int) -> int:
    return (n // 2) * ((n - 1) // 2) if n else 0


def z(m: int, n: int) -> int:
    return axis_pairs(m) * axis_pairs(n)


def check() -> dict:
    sector_checks = 0
    for m in range(1, 101):
        costs = [comb(k, 2) + comb(m - k, 2) for k in range(m + 1)]
        assert min(costs) == axis_pairs(m)
        sector_checks += 1

    even_deletion_checks = 0
    for m in range(1, 101):
        for n in range(4, 101, 2):
            assert n * z(m, n - 1) == (n - 2) * z(m, n)
            even_deletion_checks += 1

    parity_checks = 0
    for m in range(3, 102, 2):
        for n in range(3, 102, 2):
            assert (comb(m, 3) * comb(n, 3) - z(m, n)) % 2 == 0
            parity_checks += 1

    # Realized standard duplication models check the new pair/row identities.
    # These arithmetic matrices do not encode all geometric data themselves.
    pair_checks = row_checks = 0
    for a in range(1, 10):
        for b in range(1, 10):
            n = 2 * b + 1
            pair = [[0 if i == j else a * a * int((i < b) == (j < b))
                     for j in range(n)] for i in range(n)]
            qvals = [sum(row) for row in pair]
            slacks = [a * a * b - q for q in qvals]
            assert sum(slacks) == a * a * b
            for v in range(n):
                hsum = 0
                for u in range(n):
                    if u == v:
                        continue
                    c, su, sv = pair[u][v], slacks[u], slacks[v]
                    assert max(0, a * a - su - sv) <= c <= a * a - abs(su - sv)
                    assert (c + su + sv - a) % 2 == 0
                    h = (a * a - c - su - sv) // 2
                    assert -min(su, sv) <= h <= 0
                    hsum += h
                    pair_checks += 1
                assert hsum == -(b - 1) * slacks[v]
                row_checks += 1

    # One common fractional endpoint-pair tensor, not spliced marginals.
    m = n = 7
    crossing_total = 79
    weight = Fraction(crossing_total, comb(m, 2) * comb(n, 2))
    subset_checks = 0
    for p in range(m + 1):
        for q in range(n + 1):
            if (p, q) == (m, n):
                continue
            assert weight * comb(p, 2) * comb(q, 2) >= z(p, q)
            subset_checks += 1
    pair_weight = weight * comb(m, 2)
    star_weight = (n - 1) * pair_weight
    assert comb(n, 2) * pair_weight == crossing_total
    assert star_weight <= crossing_total - z(m, n - 1)
    assert crossing_total % 2 == z(m, n) % 2
    clone_deltas = []
    for k in range(1, n):
        # All stars have equal q, and all same-side pairs have equal c.
        delta = comb(k + 1, 2) * (axis_pairs(m) - pair_weight)
        assert delta > 0
        clone_deltas.append(str(delta))
    local_k33_weight = 9 * weight
    assert local_k33_weight.denominator != 1

    deficit_examples = []
    for m, n in ((7, 7), (7, 9), (9, 9), (9, 11)):
        a, b = m // 2, n // 2
        cap = min(a * a * b // (2 * b - 1), a * b * b // (2 * a - 1))
        deficit_examples.append({
            "m": m, "n": n, "deletion_cap": cap,
            "positive_even_deficits_not_excluded_by_cap": list(range(2, cap + 1, 2)),
        })

    return {
        "scope": "finite exact arithmetic; no drawing realization or topology proof",
        "sector_minimum_checks": sector_checks,
        "even_deletion_identity_checks": even_deletion_checks,
        "odd_parity_formula_checks": parity_checks,
        "standard_model_ordered_pair_checks": pair_checks,
        "standard_model_row_identity_checks": row_checks,
        "fractional_control": {
            "m": 7, "n": 7, "C": crossing_total, "Z": z(7, 7),
            "endpoint_pair_weight": str(weight),
            "same_side_pair_weight": str(pair_weight),
            "star_weight": str(star_weight),
            "proper_subset_size_checks": subset_checks,
            "clone_delta_by_number_replaced": clone_deltas,
            "local_K33_weight": str(local_k33_weight),
            "local_K33_parity_satisfied": False,
            "geometric_counterexample": False,
        },
        "conditional_deficit_examples": deficit_examples,
    }


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False, indent=2))
