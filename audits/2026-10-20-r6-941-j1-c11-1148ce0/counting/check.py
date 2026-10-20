#!/usr/bin/env python3
"""Rebuild and check an integer C11 separating identity; no numeric solver."""
from pathlib import Path
from collections import Counter
import argparse
import gzip
import hashlib
import importlib.util
import json

D = Path(__file__).resolve().parent
OLD = D.parent / "frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c"
spec = importlib.util.spec_from_file_location("frozen_c11", OLD / "interface/check.py")
o = importlib.util.module_from_spec(spec)
spec.loader.exec_module(o)


def packed(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


def sparse(items, length):
    ans = [0] * length
    used = set()
    for i, v in items:
        assert type(i) is int and type(v) is int and v
        assert 0 <= i < length and i not in used
        used.add(i)
        ans[i] = v
    return ans


def check(certificate):
    inter = json.load(gzip.open(OLD / "interface/certificate-v4.json.gz", "rt"))
    states = [tuple(c["core"]) for c in inter["caps"]]
    assert states == [t for t in o.m.growth(11, four=True) if o.m.proper(t)]
    K = o.old.kempe(11, states)
    assert hashlib.sha256(packed(K["columns"])).hexdigest() == inter["kempe"]["columns_sha256"]
    assert len(states) == 7381 and len(K["hrows"]) == 22143
    assert len(K["columns"]) == 36487 and set(K["hsize"]) == {8}
    n, nh = len(states), len(K["hrows"])
    lam = sparse(certificate["equality_multipliers"], nh + n)
    weights = sparse(certificate["positive_row_multipliers"], 10)
    assert min(weights) >= 0 and sum(weights) > 0
    assert sum(weights) == certificate["positive_weight_sum"]
    pos = [[0] * n for _ in range(10)]
    source_rows = (0, 2, 3, 5, 7, 8, 9)
    for i, cap in enumerate(inter["caps"]):
        a, _, _, _, _, _, c, *_ = cap["core"]
        for b, p, h, R in cap["original_left_bphR"]:
            for x, y, r in cap["right_xyr"]:
                row = o.m.ROWS.index("".join(map(str, o.m.canonical((x, y, a, b, c)))))
                if row in source_rows:
                    pos[source_rows.index(row)][i] += 1
                if row == 9:
                    pos[7][i] += h == a
                    pos[8][i] += h == b
    for w in inter["witnesses"]:
        pos[9][w["canonical_id"]] = 1
    core = lam[nh:]
    for r, i in enumerate(K["rowids"]):
        core[i] += K["hsize"][r] * lam[r]
    for j, weight in enumerate(weights):
        for i, value in enumerate(pos[j]):
            core[i] += weight * value
    orbits = [-sum(lam[r] * v for r, v in col) for col in K["columns"]]
    parts = [p for p in o.old.ncgrowth(11) if o.m.proper(p)]
    assert len(parts) == 1585
    nonzero_span = [(i, lam[nh+i]) for i in range(n) if lam[nh+i]]
    for p in parts:
        pairs = [(i, j) for i in range(11) for j in range(i) if p[i] == p[j]]
        value = sum(v for i, v in nonzero_span
                    if all(states[i][a] == states[i][b] for a, b in pairs))
        assert value == 0, ("signed planar column does not cancel", p, value)
    live = sorted(inter["live"])
    assert all(core[i] <= 0 for i in live), "positive coefficient on possible core fibre"
    assert max(orbits) <= 0, "positive coefficient on possible complete Kempe orbit"
    slacks = [[i, -core[i]] for i in live if core[i]]
    slacks += [[n+j, -v] for j, v in enumerate(orbits) if v]
    assert slacks == certificate["nonnegative_slacks"], "incomplete or changed slack vector"
    return {
        "status": "PASS exact integer separating identity",
        "states": n, "half_rows": nh, "complete_kempe_columns": len(orbits),
        "signed_planar_columns": len(parts),
        "inherited_zero_fibres": n-len(live),
        "positive_rows": ["G:"+o.m.ROWS[j] for j in source_rows]+["A_a", "A_b", "short_W5"],
        "positive_row_weights": weights,
        "nonzero_equality_multipliers": len(certificate["equality_multipliers"]),
        "nonzero_nonnegative_slacks": len(slacks),
        "short_fibres_forced_zero_by_identity": weights[9] > 0,
        "identity": "weighted source positive counts plus nonnegative slack counts equals zero",
        "source_excluded_under_inherited_contract": True,
        "new_Lean": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, default=D.parent/"geometry/orbit-farkas-certificate.json")
    args = ap.parse_args()
    print(json.dumps(check(json.loads(args.certificate.read_text())), sort_keys=True))


if __name__ == "__main__":
    main()
