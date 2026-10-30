#!/usr/bin/env python3
"""Test the necessary triple-parity lift of one collapsed integer tensor.

For three distinct neighbour labels i<j<k, chi(rho) is zero when j is
encountered before k while traversing the cyclic order from i, and one
otherwise. The odd-degree m=3 star-parity condition is

    c_uv({i,j,k}) == 1 + chi(rho_u) + chi(rho_v) (mod 2).

Thus a root signature determines every other star signature. We enumerate
all (m-1)! oriented cyclic orders, fixing only their first label. Passing
would be necessary, not sufficient, for a drawing. The supplied tensor fails.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from zarankiewicz_integer_replay import DEFAULT, replay


def orientation_signature(order: tuple[int, ...], triples: list[tuple[int, ...]]) -> int:
    position = {v: i for i, v in enumerate(order)}
    n = len(order)
    return sum(int((position[j] - position[i]) % n >
                   (position[k] - position[i]) % n) << bit
               for bit, (i, j, k) in enumerate(triples))


def valid_signatures(labels: tuple[int, ...], triples: list[tuple[int, ...]]) -> dict[int, tuple[int, ...]]:
    orders = [(labels[0],) + tail for tail in itertools.permutations(labels[1:])]
    result = {orientation_signature(order, triples): order for order in orders}
    assert len(result) == len(orders)
    return result


def audit(certificate: Path) -> dict:
    integer_result = replay(certificate)
    source = json.loads(certificate.read_text())
    tensor = source["tensor"]
    pairs = [tuple(pair) for pair in source["pair_order"]]
    pair_index = {pair: i for i, pair in enumerate(pairs)}
    labels = tuple(range(7))
    all_triples = list(itertools.combinations(labels, 3))
    all_signatures = valid_signatures(labels, all_triples)
    assert len(all_signatures) == 720
    sides = []
    # Each obstruction is a restriction to four neighbours and four stars.
    local_specs = [((0, 1, 2, 4), (0, 1, 2, 3)),
                   ((0, 1, 4, 5), (0, 1, 2, 4))]
    for axis in (0, 1):
        def count(root: int, v: int, triple: tuple[int, ...]) -> int:
            star_pair = pair_index[tuple(sorted((root, v)))]
            neighbour_pairs = [pair_index[p] for p in itertools.combinations(triple, 2)]
            return sum(tensor[p][star_pair] if axis == 0 else tensor[star_pair][p]
                       for p in neighbour_pairs)

        def offset(root: int, v: int, triples: list[tuple[int, ...]]) -> int:
            return sum((1 ^ (count(root, v, triple) % 2)) << i
                       for i, triple in enumerate(triples))

        offsets = [0] + [offset(0, v, all_triples) for v in range(1, 7)]
        candidates = set(all_signatures)
        root_counts = [len(candidates)]
        for v in range(1, 7):
            candidates = {sig for sig in candidates if sig ^ offsets[v] in all_signatures}
            root_counts.append(len(candidates))
        assert not candidates

        local_labels, local_stars = local_specs[axis]
        local_triples = list(itertools.combinations(local_labels, 3))
        local_orders = valid_signatures(local_labels, local_triples)
        assert len(local_orders) == 6
        root = local_stars[0]
        local_offsets = [offset(root, v, local_triples) for v in local_stars[1:]]
        local_candidates = set(local_orders)
        local_steps = [{"star": root, "remaining_root_signatures": sorted(local_candidates)}]
        for v, change in zip(local_stars[1:], local_offsets):
            local_candidates = {sig for sig in local_candidates if sig ^ change in local_orders}
            local_steps.append({"star": v, "offset_signature": change,
                                "triple_crossing_counts": [count(root, v, triple) for triple in local_triples],
                                "remaining_root_signatures": sorted(local_candidates)})
        assert not local_candidates
        sides.append({"star_side": "B" if axis == 0 else "A",
                      "neighbour_side": "A" if axis == 0 else "B",
                      "root_star": 0,
                      "oriented_root_orders_exhausted": len(all_signatures),
                      "full_root_candidate_counts_after_stars_0_through_6": root_counts,
                      "compatible_full_rotation_assignments": 0,
                      "four_by_four_obstruction": {
                          "neighbours": list(local_labels), "stars": list(local_stars),
                          "ordered_triples": [list(triple) for triple in local_triples],
                          "bit_convention": "integer bit i is chi on ordered_triples[i]; least significant bit first",
                          "valid_signatures": sorted(local_orders),
                          "valid_oriented_cyclic_orders": [list(local_orders[sig]) for sig in sorted(local_orders)],
                          "root_elimination": local_steps}})
    return {"status": "INTEGER_PASS_ROTATION_LIFT_REJECTED",
            "certificate_sha256": integer_result["certificate_sha256"],
            "scope": "exact finite obstruction to necessary triple-parity rotation lift of this tensor only",
            "parity_relation": "c_uv(T) = 1 + chi(rho_u|T) + chi(rho_v|T) modulo 2",
            "sides": sides,
            "drawing_realization": False,
            "all_integer_tensors_excluded": False,
            "general_unavoidability": "OPEN"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=DEFAULT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(audit(args.certificate), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
