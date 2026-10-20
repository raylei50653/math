#!/usr/bin/env python3
"""Numerical orbit-only ray discovery, followed by exact integer verification."""
from pathlib import Path
import gzip
import json
import pickle
from fractions import Fraction
from math import gcd, lcm
from functools import reduce
import numpy as np
from scipy.optimize._highspy import _core as h
from scipy.sparse import vstack

D = Path(__file__).resolve().parent
with (D.parent / "counting/discovery.pickle").open("rb") as f:
    K, parts, E, U, M, sectors, old = pickle.load(f)
with (D / "orbit-only-discovery.pickle").open("rb") as f:
    variables, hr, ans = pickle.load(f)
I = json.load(gzip.open(D.parent / "frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c/interface/certificate-v4.json.gz", "rt"))
live = I["live"]
n = len(K["states"])
nh = len(K["hrows"])
nc = len(K["columns"])
AA = vstack([E[hr], U])[:, variables].tocsc()
lp = h.HighsLp()
lp.num_col_ = AA.shape[1]
lp.num_row_ = AA.shape[0]
lp.col_cost_ = np.r_[np.ones(len(live)), np.zeros(len(variables) - len(live))]
lp.col_lower_ = np.zeros(AA.shape[1])
lp.col_upper_ = np.full(AA.shape[1], h.kHighsInf)
lp.row_lower_ = np.r_[np.zeros(len(hr)), np.full(U.shape[0], -h.kHighsInf)]
lp.row_upper_ = np.r_[np.zeros(len(hr)), -np.ones(U.shape[0])]
lp.a_matrix_.format_ = h.MatrixFormat.kColwise
lp.a_matrix_.start_ = AA.indptr
lp.a_matrix_.index_ = AA.indices
lp.a_matrix_.value_ = AA.data
solver = h._Highs()
solver.setOptionValue("time_limit", 180.0)
solver.passModel(lp)
solver.run()
print("model status", solver.getModelStatus(), flush=True)
status, exists, ray = solver.getDualRay()
assert exists, (status, exists)
with (D / "orbit-only-dual-ray.pickle").open("xb") as f:
    pickle.dump((variables, hr, ray), f)
for bound in (1, 2, 4, 8, 16, 32, 128, 1024, 1000000):
    rat = [Fraction(float(v)).limit_denominator(bound) for v in ray]
    mul = lcm(*(v.denominator for v in rat))
    vec = [int(v * mul) for v in rat]
    div = reduce(gcd, vec)
    if not div:
        continue
    vec = [v // div for v in vec]
    if sum(vec[len(hr):]) > 0:
        vec = [-v for v in vec]
    weights = [-v for v in vec[len(hr):]]
    if min(weights) < 0 or sum(weights) <= 0:
        continue
    lam = [0] * E.shape[0]
    for r, value in zip(hr, vec[:len(hr)]):
        lam[r] = value
    sums = [0] * E.shape[1]
    coo = E.tocoo()
    for r, c, value in zip(coo.row, coo.col, coo.data):
        sums[c] += int(value) * lam[r]
    coo = U.tocoo()
    for r, c, value in zip(coo.row, coo.col, coo.data):
        sums[c] -= int(value) * weights[r]
    if max(sums[i] for i in variables) > 0:
        print("rational bound failed", bound, flush=True)
        continue
    # Every discarded orbit column has a dead half-row. Raising its multiplier
    # lowers that orbit coefficient and affects only a source-zero count.
    deadhr = sorted(set(range(nh)) - set(hr))
    adjustment = max([0] + sums[n:n + nc])
    if adjustment:
        for r in deadhr:
            lam[r] = adjustment
        sums = [0] * E.shape[1]
        coo = E.tocoo()
        for r, c, value in zip(coo.row, coo.col, coo.data):
            sums[c] += int(value) * lam[r]
        coo = U.tocoo()
        for r, c, value in zip(coo.row, coo.col, coo.data):
            sums[c] -= int(value) * weights[r]
    assert max(sums[i] for i in live) <= 0
    assert max(sums[n:n + nc]) <= 0
    assert not any(sums[n + nc:])
    cert = {
        "status": "exact integer Farkas certificate",
        "equality_multipliers": [[i, v] for i, v in enumerate(lam) if v],
        "positive_row_multipliers": [[i, v] for i, v in enumerate(weights) if v],
        "nonnegative_slacks": [[i, -sums[i]] for i in sorted(live) if sums[i]]
                              + [[i, -sums[i]] for i in range(n, n + nc) if sums[i]],
        "positive_weight_sum": sum(weights),
    }
    with (D / "orbit-farkas-certificate.json").open("x") as f:
        json.dump(cert, f, separators=(",", ":"))
        f.write("\n")
    print({"exact": True, "weights": weights, "bound": bound,
           "dead_half_row_adjustment": adjustment,
           "nonzero_equalities": len(cert["equality_multipliers"]),
           "nonzero_slacks": len(cert["nonnegative_slacks"])}, flush=True)
    break
else:
    raise AssertionError("no exact rationalization found")
