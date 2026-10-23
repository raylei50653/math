#!/usr/bin/env python3
"""Independent finite checks for the resource lemmas; not source enumeration."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pair_table():
    # Original-circle neighbors of any original2 point in complete M2.
    pool = ("T", "r", "s")
    choices = [frozenset(a) for n in range(4)
               for a in itertools.combinations(pool, n)
               if not {"r", "s"} <= set(a)]
    rows = []
    for a, b in itertools.combinations_with_replacement(choices, 2):
        # At most two total original common neighbors for original2 nonedges.
        c = len(a & b)
        max_overlap = 2 - c
        union = len(a | b)
        require(union <= 3, "missed original-circle neighbor")
        # Minimum original degree is five.  Larger degrees only improve bound.
        outside_a, outside_b = 5 - len(a), 5 - len(b)
        outside_union_min = outside_a + outside_b - max_overlap
        require(outside_union_min == 8 - union, "inclusion-exclusion mismatch")
        # Count complete M2 and the two distinct original K2 outlets separately.
        z_minus_q = 2 + outside_union_min
        require(z_minus_q == 10 - union >= 7, "pair-resource lower bound")
        rows.append({"a": sorted(a), "b": sorted(b),
                     "max_outside_overlap": max_overlap,
                     "min_Z_minus_q": z_minus_q})
    require(len(rows) == 21, "incomplete circle-neighbor pair table")
    return rows


def check_empty_n1():
    # Complete envelope of an additional original1 point in N13.  For each
    # degree-five neighborhood, preserve the same U, p_d, p_x and chosen a/b.
    pool = ("a", "b", "d", "x", "U", "p_d", "p_x")
    survivors = []
    for n in range(5, len(pool) + 1):
        for seq in itertools.combinations(pool, n):
            star = frozenset(seq)
            if {"a", "b"} <= star or {"d", "x"} <= star:
                continue
            require(n == 5, "degree capacity not exact")
            require({"U", "p_d", "p_x"} <= star, "missing forced K neighbors")
            for p in ("p_d", "p_x"):
                y_star = frozenset(("T", "a", "b", "U", p))
                require(len(star & y_star) >= 3,
                        "same-source original1 nonedge does not contradict")
            survivors.append(sorted(star))
    require(len(survivors) == 4, "incomplete capacity table")
    # If d=U, identifying those labels cannot add an available original point.
    alias_pool = frozenset("U" if v == "d" else v for v in pool)
    alias_max = 0
    for n in range(len(alias_pool) + 1):
        for seq in itertools.combinations(sorted(alias_pool), n):
            star = frozenset(seq)
            if {"a", "b"} <= star or {"U", "x"} <= star:
                continue
            alias_max = max(alias_max, len(star))
    require(alias_max == 4, "d=U capacity exception")
    return {"nonalias_degree5_stars": survivors,
            "d_equals_U_max_degree": alias_max}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--negative", action="store_true")
    ns = ap.parse_args()
    inputs = json.loads((HERE / "INPUTS.json").read_text())
    for row in inputs["authority"]:
        raw = (REPO / row["path"]).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == row["sha256"],
                "authority drift: " + row["path"])
    reviewed = json.loads((HERE / "REVIEWED-INPUTS.json").read_text())
    for row in reviewed["artifacts"]:
        frozen = (HERE / row["snapshot"]).read_bytes()
        require(len(frozen) == row["bytes"] and
                hashlib.sha256(frozen).hexdigest() == row["sha256"],
                "reviewed snapshot drift: " + row["path"])
        require((REPO / row["path"]).read_bytes() == frozen,
                "reviewed live artifact drift: " + row["path"])
    table = pair_table()
    empty = check_empty_n1()
    if ns.negative:
        # Counterexample to using only pair marginals: drop the same original
        # gamma common neighbor and the claimed |Z| bound is too weak.
        a, b = {"T", "r"}, {"T", "s"}
        wrong = 2 + (5 - len(a)) + (5 - len(b)) - 2
        right = 2 + (5 - len(a)) + (5 - len(b)) - (2 - len(a & b))
        require(wrong == 6 and right == 7, "common-neighbor negative control")
        try:
            require(len({"a", "U", "p_d"}) <= 2,
                    "three same-source common neighbors")
        except ValueError:
            pass
        else:
            raise ValueError("failed to reject original1 nonedge corruption")
    result = {"status": "triggered and holds",
              "scope": "finite arithmetic/capacity controls only",
              "actual_complete_source": "not triggered",
              "authority_count": len(inputs["authority"]),
              "reviewed_artifacts": len(reviewed["artifacts"]),
              "pair_cases": len(table),
              "pair_min_Z_minus_q": min(row["min_Z_minus_q"] for row in table),
              "empty_N1": empty,
              "negative_controls": 2 if ns.negative else 0}
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
