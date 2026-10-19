#!/usr/bin/env python3
"""Read-only replay of the two-cap fibre algebra; --build creates new bytes only."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = range(4)
ORDER = ("a", "n", "R", "L", "q", "c", "s", "v", "w", "t")
LEFT_EDGES = tuple("ba bc bq bp pa pq ph pn hq hL hR hn".split())
RIGHT_EDGES = tuple("xy xc xr xs ya yr yt rt rw rv rs".split())
FULL_EDGES = LEFT_EDGES + RIGHT_EDGES


def canonical_rows():
    def visit(prefix):
        if len(prefix) == 10:
            if prefix[-1] != prefix[0]:
                yield tuple(prefix)
            return
        for color in range(min(3, max(prefix) + 1) + 1):
            if color != prefix[-1]:
                yield from visit(prefix + [color])

    return list(visit([0]))


def edge_lifts(row, names, edges):
    fixed = dict(zip(ORDER, row))
    answer = []
    for assignment in itertools.product(COLORS, repeat=len(names)):
        f = fixed | dict(zip(names, assignment))
        if all(f[u] != f[v] for u, v in edges):
            answer.append(assignment)
    return answer


def formula_lifts(row):
    a, n, u, v, q, c, s, i, j, t = row
    left = [(b, p, h) for b, p, h in itertools.product(COLORS, repeat=3)
            if b not in {a, c, q, p} and p not in {a, q, n, h}
            and h not in {q, u, v, n}]
    right = [(x, y, r) for x, y, r in itertools.product(COLORS, repeat=3)
             if r not in {s, i, j, t, x, y}
             and x not in {c, s, y} and y not in {a, t}]
    candidates = {
        "Q1": [b for b in COLORS if b == n and u == q and b not in {a, c, q}],
        "Q2": [b for b in COLORS if b == n == v and b not in {a, c, q}],
        "GB": [b for b in COLORS if b not in {a, c, q, n, u, v}],
    }
    return left, right, candidates


def old_quotient_lifts(row, candidate, b):
    fixed = dict(zip(ORDER, row)) | {"b": b}
    # Direct check against the whole original left cap, not simplified tests.
    return [(p, h) for p, h in itertools.product(COLORS, repeat=2)
            if all((fixed | {"p": p, "h": h})[u]
                   != (fixed | {"p": p, "h": h})[v]
                   for u, v in LEFT_EDGES)]


def compute():
    rows = canonical_rows()
    assert len(rows) == 2461
    saved = []
    q2_branch = None
    omitted_right = None
    omitted_left = None
    left_only = None
    right_only = None
    for row in rows:
        left, right, candidates = formula_lifts(row)
        assert left == edge_lifts(row, "bph", LEFT_EDGES)
        assert right == edge_lifts(row, "xyr", RIGHT_EDGES)
        fixed = dict(zip(ORDER, row))
        # Check the Cartesian construction against all 23 edges, retaining
        # every private cap colour. These are complete cap assignments.
        for lft, rgt in itertools.product(left, right):
            f = fixed | dict(zip("bph", lft)) | dict(zip("xyr", rgt))
            assert all(f[u] != f[v] for u, v in FULL_EDGES)
        if left and not right and left_only is None:
            left_only = list(row)
        if right and not left and right_only is None:
            right_only = list(row)
        # Quotient formula must preserve the omitted a=q branch.
        for candidate in ("Q1", "Q2"):
            for b in candidates[candidate]:
                lifts = old_quotient_lifts(row, candidate, b)
                expected = row[3] != row[0] if candidate == "Q1" else (
                    row[0] == row[4] or row[2] != row[0])
                assert bool(lifts) == expected
                if (candidate == "Q2" and row[0] == row[2] == row[4]
                        and q2_branch is None):
                    assert lifts
                    q2_branch = {"row": row, "b": b, "old_ph": lifts}
        if omitted_right is None:
            broken = edge_lifts(row, "xyr", tuple(e for e in RIGHT_EDGES if e != "rw"))
            extra = sorted(set(broken) - set(right))
            if extra:
                omitted_right = {"row": row, "missing_edge": "rw", "false_lifts": extra}
        if omitted_left is None:
            broken = edge_lifts(row, "bph", tuple(e for e in LEFT_EDGES if e != "pn"))
            extra = sorted(set(broken) - set(left))
            if extra:
                omitted_left = {"row": row, "missing_edge": "pn", "false_lifts": extra}
        saved.append({"core_row": row, "left": left, "right": right,
                      "candidate_b": candidates})
    assert all(x is not None for x in
               (q2_branch, omitted_right, omitted_left, left_only, right_only))
    return {
        "authority": "finite complete cap algebra; no source realization",
        "base": "b89c5913cea9df2305845be0f65fa6f1c1aaf55f",
        "core_order": ORDER,
        "left_order": list("bph"), "right_order": list("xyr"),
        "left_edges": LEFT_EDGES, "right_edges": RIGHT_EDGES,
        "all_core_orbits": saved,
        "full_lifts": "For each fixed complete core coloring, exactly left x right; no factors omitted.",
        "negative_controls": {
            "q2_a_equals_q_equals_R_is_liftable": q2_branch,
            "omitted_rw": omitted_right,
            "omitted_pn": omitted_left,
            "cross_row_product_is_invalid": {
                "left_nonempty_right_empty_row": left_only,
                "right_nonempty_left_empty_row": right_only,
            },
        },
        "totals": {
            "proper_core_color_orbits": len(saved),
            "empty_left": sum(not r["left"] for r in saved),
            "empty_right": sum(not r["right"] for r in saved),
            "cap_products": sum(len(r["left"]) * len(r["right"]) for r in saved),
        },
    }


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "core-certificate.json")
    args = parser.parse_args()
    root = HERE.parents[2]
    sources = json.loads((HERE / "additional-inputs.json").read_text())
    for item in sources["files"]:
        source_bytes = (root / item["path"]).read_bytes()
        assert len(source_bytes) == item["bytes"]
        assert hashlib.sha256(source_bytes).hexdigest() == item["sha256"], item["path"]
    data = compute()
    payload = canonical_bytes(data)
    certificate = args.certificate
    if args.build:
        with certificate.open("xb") as stream:
            stream.write(payload)
    else:
        assert certificate.read_bytes() == payload, "complete core/cap fibre certificate mismatch"
    print(json.dumps({"status": "PASS", "certificate_sha256": hashlib.sha256(payload).hexdigest(),
                      **data["totals"], "negative_controls": "4 checked"}, sort_keys=True))


if __name__ == "__main__":
    main()
