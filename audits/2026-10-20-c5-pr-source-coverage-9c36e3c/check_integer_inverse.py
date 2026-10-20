#!/usr/bin/env python3
"""Read-only exact algebra replay; --write exclusively creates a certificate."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "frozen/docs/sources/2026-10-19-c5-grammar-v02/certificate_v02.json"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(row):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in row)


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    result = Fraction(1)
    for col in range(len(a)):
        pivot = next(row for row in range(col, len(a)) if a[row][col])
        if pivot != col:
            a[pivot], a[col] = a[col], a[pivot]
            result = -result
        scale = a[col][col]
        result *= scale
        for row in range(col + 1, len(a)):
            ratio = a[row][col] / scale
            a[row] = [x - ratio * y for x, y in zip(a[row], a[col])]
    require(result.denominator == 1, "nonintegral determinant")
    return result.numerator


def build():
    source = json.loads(SOURCE.read_text())
    model = source["model"]
    rows = sorted({canonical(row) for row in product(range(4), repeat=5)
                   if all(row[i] != row[(i + 1) % 5] for i in range(5))})
    require(["".join(map(str, r)) for r in rows] == model["rows"], "row order drift")
    index = {row: i for i, row in enumerate(rows)}
    # Compile from literal old b0 colours and the three new edges.
    p = [[0] * 10 for _ in rows]
    for j, beta in enumerate(rows):
        for old_b0 in range(4):
            if old_b0 not in {beta[0], beta[1], beta[4]}:
                p[j][index[canonical((old_b0,) + beta[1:])]] += 1
    require(p == model["operators"]["P"], "local P compilation differs")
    # Q = 2 P^{-1}. The three non-permutation coordinates are triangle sums.
    q = [[0] * 10 for _ in rows]
    for original, new in [(0, 7), (2, 5), (4, 9), (5, 2),
                          (6, 6), (7, 0), (9, 4)]:
        q[original][new] = 2
    for original, positives, negative in [
        (1, (3, 8), 1), (3, (1, 8), 3), (8, (1, 3), 8)
    ]:
        for j in positives:
            q[original][j] = 1
        q[original][negative] = -1
    identity2 = [[2 * (i == j) for j in range(10)] for i in range(10)]
    require(multiply(q, p) == identity2, "left inverse failed")
    require(multiply(p, q) == identity2, "right inverse failed")
    preimages = {}
    for mask in range(1024):
        target = sum(1 << i for i in range(10)
                     if any(value and mask >> j & 1 for j, value in enumerate(p[i])))
        preimages.setdefault(target, []).append(mask)
    histogram = Counter(map(len, preimages.values()))
    require(histogram == {1: 512, 4: 128}, "Boolean preimage classification failed")
    # Triangle block: 000 and the three one-hot patterns have unique images;
    # all four patterns with at least two positive coordinates have image 111.
    block = []
    for x, y, z in product(range(2), repeat=3):
        block.append({"source_n1_n3_n8": [x, y, z],
                      "integer_m1_m3_m8": [y + z, x + z, x + y],
                      "support_m1_m3_m8": [int(y or z), int(x or z), int(x or y)]})
    return {
        "schema": "c5-pr-integer-inverse/v1",
        "scope": "Exact local algebra on all nonnegative integer vectors; not source realizability",
        "rows": model["rows"],
        "P": p,
        "twice_inverse_P": q,
        "determinant_P": determinant(p),
        "left_and_right_products": identity2,
        "integer_image_conditions": {
            "nonnegative_coordinates": list(range(10)),
            "even_sum_coordinates": [1, 3, 8],
            "triangle_coordinates": [1, 3, 8],
        },
        "support_image_count": len(preimages),
        "support_preimage_size_histogram": dict(sorted(histogram.items())),
        "triangle_block": block,
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "integer_inverse.json")
    args = parser.parse_args()
    expected = json.loads(json.dumps(build()))
    if args.write:
        with args.certificate.open("x") as stream:
            json.dump(expected, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
    else:
        require(json.loads(args.certificate.read_text()) == expected, "certificate mismatch")
    print(json.dumps({"status": "PASS", "determinant": expected["determinant_P"],
                      "support_images": expected["support_image_count"],
                      "preimage_histogram": expected["support_preimage_size_histogram"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()
