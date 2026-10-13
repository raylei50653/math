#!/usr/bin/env python3
"""Exact literal full-lift control for the W8 simultaneous-equalities boundary."""

import json
from itertools import combinations, product


def main():
    pairs = ((0, 3), (1, 5), (2, 7), (4, 6))
    counts = [0] * len(pairs)
    witnesses = [None] * len(pairs)
    total = joint = 0
    for rim in product(range(4), repeat=8):
        if any(rim[i] == rim[(i + 1) % 8] for i in range(8)):
            continue
        for hub in range(4):
            if hub in rim:
                continue
            total += 1
            accepted = [rim[a] == rim[b] for a, b in pairs]
            joint += all(accepted)
            for j, ok in enumerate(accepted):
                if ok:
                    counts[j] += 1
                    if witnesses[j] is None:
                        witnesses[j] = {"rim": list(rim), "hub": hub}

    # Four quotient classes preserve every original inequality edge.
    classes = [0, 1, 2, 0, 3, 1, 3, 2]
    rim_edges = {
        tuple(sorted((classes[i], classes[(i + 1) % 8])))
        for i in range(8)
    }
    quotient_edges = rim_edges | {(i, 4) for i in range(4)}
    assert quotient_edges == set(combinations(range(5), 2))
    assert (total, counts, joint) == (1032, [240, 432, 240, 528], 0)
    for (a, b), witness in zip(pairs, witnesses):
        assert witness["rim"][a] == witness["rim"][b]
        assert witness["hub"] not in witness["rim"]

    print(json.dumps({
        "status": "PASS",
        "domain": "all literal proper full colourings of one named W8",
        "full_lifts": total,
        "equal_pairs": pairs,
        "single_pair_full_lifts": counts,
        "joint_full_lifts": joint,
        "single_pair_witnesses": witnesses,
        "simultaneous_quotient_edges": sorted(quotient_edges),
        "simultaneous_quotient": "K5",
        "source_minimal_outside_catalogue": "not triggered",
        "uses_four_colour_theorem": False,
    }, indent=2))


if __name__ == "__main__":
    main()
