#!/usr/bin/env python3
"""Replay a collapsed common integer tensor using exact integer arithmetic.

Each tensor entry is indexed by one unordered pair on each bipartition side.
The two possible independent-edge matchings on those four endpoints are not
distinguished. A passing replay certifies the listed counting relaxation only;
it supplies no rotations, per-edge crossing order, or planar embedding.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "audits/2026-10-30-zarankiewicz-rotation-excess/integer_tensor.json"


def z_axis(n: int) -> int:
    return (n // 2) * ((n - 1) // 2)


def replay(certificate: Path) -> dict:
    raw = certificate.read_bytes()
    source = json.loads(raw)
    assert source["schema"] == "zarankiewicz-collapsed-integer-tensor-v1"
    assert source["m"] == source["n"] == 7
    n = 7
    a = b = 3
    pairs = list(itertools.combinations(range(n), 2))
    assert source["pair_order"] == [list(pair) for pair in pairs]
    tensor = source["tensor"]
    assert len(tensor) == len(pairs)
    assert all(len(row) == len(pairs) for row in tensor)
    assert all(type(v) is int and v in (0, 1) for row in tensor for v in row)
    total = sum(map(sum, tensor))
    assert total == source["crossing_total"] == 79
    target = z_axis(n) ** 2
    deficit = target - total
    assert deficit == 2

    # One shared tensor supplies every subset and both side projections.
    # No independently selected side marginals enter the verification.
    subsets = [tuple(v for v in range(n) if mask & (1 << v))
               for mask in range(1 << n)]
    inside = {subset: [i for i, pair in enumerate(pairs)
                       if set(pair) <= set(subset)] for subset in subsets}
    lower_checks = odd_checks = k33_checks = 0
    odd_size_counts: dict[str, int] = {}
    for left in subsets:
        for right in subsets:
            count = sum(tensor[i][j] for i in inside[left] for j in inside[right])
            lower = z_axis(len(left)) * z_axis(len(right))
            if len(left) != n or len(right) != n:
                assert count >= lower, ("subset lower bound", left, right, count, lower)
                lower_checks += 1
            if len(left) % 2 and len(right) % 2:
                assert (count - lower) % 2 == 0, ("odd subset parity", left, right)
                odd_checks += 1
                key = f"{len(left)}x{len(right)}"
                odd_size_counts[key] = odd_size_counts.get(key, 0) + 1
            if len(left) == len(right) == 3:
                assert count % 2 == 1
                k33_checks += 1

    lookup = {pair: i for i, pair in enumerate(pairs)}
    sides = []
    for side in ("A", "B"):
        pair_counts = ([sum(row) for row in tensor] if side == "A" else
                       [sum(row[j] for row in tensor) for j in range(len(pairs))])
        c = lambda u, v: pair_counts[lookup[tuple(sorted((u, v)))]]
        q = [sum(c(u, v) for u in range(n) if u != v) for v in range(n)]
        slack = [a * a * b - deficit - qv for qv in q]
        assert all(s >= 0 for s in slack)
        assert sum(q) == 2 * total
        assert sum(slack) == a * a * b - (2 * b - 1) * deficit
        p_checks = n2_checks = n3_checks = rt_checks = h_rows = 0
        for u, v in pairs:
            su, sv = slack[u], slack[v]
            assert max(0, a * a - deficit - su - sv) <= c(u, v)
            assert c(u, v) <= a * a - abs(su - sv)
            assert (c(u, v) + su + sv - a) % 2 == 0
            p_checks += 1
            assert c(u, v) + abs(q[u] - q[v]) <= a * a
            n2_checks += 1
        for v in range(n):
            hs = []
            for u in range(n):
                if u == v:
                    continue
                numerator = a * a - c(u, v) - slack[u] - slack[v]
                assert numerator % 2 == 0
                h = numerator // 2
                assert -min(slack[u], slack[v]) <= h <= deficit // 2
                hs.append(h)
            assert sum(hs) == b * deficit - (b - 1) * slack[v]
            h_rows += 1
        minimum_rt = None
        minimum_by_t: dict[str, int] = {}
        for u in range(n):
            others = [v for v in range(n) if v != u]
            for t in range(1, n):
                for replaced in itertools.combinations(others, t):
                    delta = (-sum(q[v] for v in replaced)
                             + sum(c(v, w) for v, w in itertools.combinations(replaced, 2))
                             + t * (q[u] - sum(c(u, v) for v in replaced))
                             + comb(t + 1, 2) * a * a)
                    assert delta >= 0, ("Rt", side, u, replaced, delta)
                    rt_checks += 1
                    minimum_rt = delta if minimum_rt is None else min(minimum_rt, delta)
                    key = str(t)
                    minimum_by_t[key] = min(minimum_by_t.get(key, delta), delta)
                    if t == 2:
                        v, w = replaced
                        assert q[v] + q[w] - 2 * q[u] + 2 * c(u, v) + 2 * c(u, w) - c(v, w) <= 3 * a * a
                        n3_checks += 1
        sides.append({"side": side, "pair_counts": pair_counts, "q": q, "s": slack,
                      "S_sum": sum(slack), "P_pair_checks": p_checks,
                      "H_row_checks": h_rows, "N2_pair_checks": n2_checks,
                      "N3_anchor_pair_checks": n3_checks,
                      "Rt_anchor_subset_checks": rt_checks,
                      "minimum_Rt_upper_bound": minimum_rt,
                      "minimum_Rt_upper_bound_by_t": minimum_by_t})

    # Binary entries mean every retained collapsed four-endpoint label occurs
    # at most once. They do not select which two actual edges cross.
    labels = [(pairs[i], pairs[j]) for i in range(len(pairs))
              for j in range(len(pairs)) if tensor[i][j]]
    assert len(labels) == len(set(labels)) == total
    return {"status": "PASS", "scope": "finite collapsed integer counting relaxation; no drawing realization",
            "certificate_sha256": hashlib.sha256(raw).hexdigest(),
            "m": n, "n": n, "C": total, "Z": target, "d": deficit,
            "binary_tensor_entries": len(pairs) ** 2,
            "unique_retained_four_endpoint_labels": len(labels),
            "proper_labelled_subset_lower_bound_checks": lower_checks,
            "induced_K33_odd_parity_checks": k33_checks,
            "induced_odd_by_odd_parity_checks_including_full": odd_checks,
            "odd_by_odd_parity_checks_by_size": odd_size_counts,
            "sides": sides,
            "rotations_supplied": False, "independent_edge_matchings_supplied": False,
            "per_edge_crossing_orders_supplied": False,
            "planarization_embedding_supplied": False,
            "geometric_counterexample": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=DEFAULT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = replay(args.certificate)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
