#!/usr/bin/env python3
"""Can y = alpha*y13 + beta*y0 (alpha, beta of free sign) be a dual certificate?

Checker form (independent/README.md), target-only lambda_9 > 0:
  2 w_s(y) >= 0 for every live non-target s,  2 w_t(y) > 0 for t = 44459, 44466,
  col_j(y) <= 0 for every one of the 307,197 columns.
y13 = frozen 13-term half-row weights (sparse/warm2-44459), y0 = C11 deletion
pullback (c11_mismatch.py).  Every constraint is a closed half-plane through 0 in
(alpha, beta), so the feasible set is a cone whose extreme rays are perpendicular to
some constraint normal: test those rays and their pairwise sums, exactly in integers.
Also reports, per seed, the integer price table so overlap can be inspected.
"""
import contextlib
import gzip
import importlib.util
import io
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import Model, TARGETS  # noqa: E402

CONE = HERE.parent / '2026-10-20-w7-count-cone-d5b8a86'


def seeds(m):
    res = json.load(gzip.open(CONE / 'sparse/warm2-44459/exact-dual-residual.json.gz', 'rt'))
    hk = {int(h): k for k, h in enumerate(m.hrow)}
    y13 = np.zeros(m.nh, np.int64)
    for h, v in res['halfrow_integer_weights']:
        y13[hk[h]] += v
    spec = importlib.util.spec_from_file_location('mm', HERE / 'c11_mismatch.py')
    with contextlib.redirect_stdout(io.StringIO()):
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)
    y0 = np.array([mm.pulled[int(h)] for h in m.hrow], np.int64)
    return y13, y0


def pairings(m, y):
    C = m.incidence().tocsc()
    col = np.rint(C.T @ y).astype(np.int64)
    w = y.reshape(-1, 3).sum(1)
    return w, col


def main():
    m = Model()
    y13, y0 = seeds(m)
    (w1, c1), (w0, c0) = pairings(m, y13), pairings(m, y0)
    tg = np.array([m.state_of[t] for t in TARGETS])
    nt = np.ones(m.ns, bool)
    nt[tg] = False
    # rows n with constraint n . (alpha, beta) <= 0
    N = np.r_[np.c_[c1, c0], -np.c_[w1, w0][nt]]
    N = np.unique(N[(N != 0).any(1)], axis=0)
    strict = -np.c_[w1, w0][tg]                   # need strict < 0
    rays = {(int(-b), int(a)) for a, b in N} | {(int(b), int(-a)) for a, b in N}
    rays = [np.array(d) for d in rays]
    ok = [d for d in rays if (N @ d <= 0).all()]
    cand = ok + [a + b for i, a in enumerate(ok) for b in ok[i + 1:]]
    found = [d.tolist() for d in cand if (N @ d <= 0).all() and (strict @ d < 0).all()]
    out = {
        'distinct_constraint_normals': len(N),
        'feasible_extreme_rays': [d.tolist() for d in ok],
        'certificate_directions': found[:4],
        'y13': {'target_w': w1[tg].tolist(), 'pos_price_cols': int((c1 > 0).sum()),
                'neg_z_nontarget': int((w1[nt] < 0).sum())},
        'y0': {'target_w': w0[tg].tolist(), 'pos_price_cols': int((c0 > 0).sum()),
               'neg_z_nontarget': int((w0[nt] < 0).sum())},
        'column_overlap_nonzero_both': int(((c1 != 0) & (c0 != 0)).sum()),
        'halfrow_overlap': int(((y13 != 0) & (y0 != 0)).sum()),
    }
    (HERE / 'logs/combine2.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
