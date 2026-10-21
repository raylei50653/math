#!/usr/bin/env python3
"""Restricted dual patch LP (discovery only; check.py decides).

y = alpha*y13 + beta*y0 + delta, alpha/beta/delta free, supp(delta) in H, plus ten
lambda_l >= 0 with sum lambda = 1.  Checker form (independent/README.md):
  2 w_s(y) - sum_l lambda_l P[l,s] >= 0   every live state s,
  col_j(y) <= 0                         every column j.
Only columns touching H or a seed's support can have nonzero pairing; the state
rows cover H, the seeds' support and every state in the support of some P_l (there
w = 0 still forces lambda.P[:,s] <= 0), so the LP holds every constraint that can bind; the exact
check afterwards still prices all 307,197 columns and all 61,308 states.
H = all half-rows of the states touched by columns where some seed pairs nonzero,
grown by --rings further rounds (states of columns touching H).
A restricted infeasibility only rules out this H; it is never a verdict.
"""
import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import Model  # noqa: E402
from combine2 import pairings, seeds  # noqa: E402


def grow(m, C, CT, states, rings):
    for _ in range(rings):
        hs = (3 * states[:, None] + np.arange(3)).reshape(-1)
        cols = np.unique(CT[:, hs].indices)
        states = np.union1d(states, np.unique(C[:, cols].indices // 3))
    return states


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rings', type=int, default=0)
    ap.add_argument('--seconds', type=float, default=1800)
    ap.add_argument('--name', default='h0')
    a = ap.parse_args()
    t0 = time.monotonic()
    m = Model()
    y13, y0 = seeds(m)
    (w1, c1), (w0, c0) = pairings(m, y13), pairings(m, y0)
    C = m.incidence().tocsc()
    CT = C.T.tocsc()                                  # column k = half-row k's columns
    seedcols = np.nonzero((c1 != 0) | (c0 != 0))[0]
    states = np.unique(C[:, seedcols].indices // 3)
    states = grow(m, C, CT, states, a.rings)
    H = (3 * states[:, None] + np.arange(3)).reshape(-1)
    cols = np.unique(np.r_[CT[:, H].indices, seedcols])
    st = np.unique(np.r_[states, np.nonzero((w1 != 0) | (w0 != 0))[0],
                         np.nonzero((m.P != 0).any(0))[0]])

    import highspy
    from scipy.sparse import csc_matrix, hstack, vstack
    nH = len(H)
    sel = csc_matrix((np.ones(nH), (H, np.arange(nH))), shape=(m.nh, nH))
    Ccols = C[:, cols].T.tocsr()                      # |cols| x nh
    Acol = hstack([csc_matrix(c1[cols, None].astype(float)), csc_matrix(c0[cols, None].astype(float)),
                   Ccols @ sel, csc_matrix((len(cols), 10))])
    S = csc_matrix((np.full(3 * m.ns, 2.0), (np.repeat(np.arange(m.ns), 3), np.arange(3 * m.ns))),
                   shape=(m.ns, m.nh))[st]            # rows: 2 w_s as a form in y
    Ast = hstack([csc_matrix((2 * w1[st])[:, None].astype(float)),
                  csc_matrix((2 * w0[st])[:, None].astype(float)),
                  S @ sel, csc_matrix(-m.P[:, st].T.astype(float))])
    Anorm = csc_matrix(np.r_[np.zeros(2 + nH), np.ones(10)][None, :])
    A = vstack([Acol, Ast, Anorm]).tocsc()
    nv = 2 + nH + 10
    lo_r = np.r_[np.full(len(cols), -np.inf), np.zeros(len(st)), 1.0]
    hi_r = np.r_[np.zeros(len(cols)), np.full(len(st), np.inf), 1.0]
    lo_v = np.r_[np.full(2 + nH, -np.inf), np.zeros(10)]
    hi_v = np.r_[np.full(2 + nH, np.inf), np.full(10, np.inf)]
    info = dict(name=a.name, rings=a.rings, H_states=len(states), H_halfrows=nH,
                cols=len(cols), states=len(st), nnz=int(A.nnz))
    print(json.dumps(info), flush=True)

    h = highspy.Highs()
    h.setOptionValue('time_limit', a.seconds)
    h.setOptionValue('solver', 'simplex')
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = nv, A.shape[0]
    lp.col_cost_ = np.zeros(nv)
    lp.col_lower_, lp.col_upper_ = lo_v, hi_v
    lp.row_lower_, lp.row_upper_ = lo_r, hi_r
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = A.indptr, A.indices, A.data
    h.passModel(lp)
    h.run()
    status = h.modelStatusToString(h.getModelStatus())
    info.update(status=status, seconds=round(time.monotonic() - t0, 1))
    out = HERE / f'runs/patch-{a.name}'
    out.mkdir(parents=True, exist_ok=True)
    if status == 'Optimal':
        x = np.array(h.getSolution().col_value)
        np.savez_compressed(out / 'float.npz', x=x, H=H)
        info.update(exact_attempt(m, C, y13, y0, H, x, out))
    (out / 'result.json').write_text(json.dumps(info, indent=1) + '\n')
    print(json.dumps(info, indent=1))


def exact_attempt(m, C, y13, y0, H, x, out):
    """Round to small rationals, scale to integers, check every state and column exactly."""
    from math import lcm
    nH = len(H)
    for den in (1, 2, 4, 8, 16, 64, 256, 4096):
        fr = [Fraction(v).limit_denominator(den) for v in x]
        fr[2 + nH:] = [max(f, Fraction(0)) for f in fr[2 + nH:]]
        L = lcm(*(f.denominator for f in fr))
        iv = [int(f * L) for f in fr]
        y = iv[0] * y13 + iv[1] * y0
        y[H] += np.array(iv[2:2 + nH], np.int64)
        lam = np.array(iv[2 + nH:], np.int64)
        assert np.abs(y).max() < 2 ** 40 and lam.max() < 2 ** 20
        col = (C.T.tocsr().astype(np.int64) @ y).astype(np.int64)
        w = y.reshape(-1, 3).sum(1)
        need = lam @ m.P
        bad_c, bad_z = int((col > 0).sum()), int((2 * w < need).sum())
        if bad_c == 0 and bad_z == 0 and lam.any():
            cert = {'kind': 'dual',
                    'y': [[int(m.hrow[k]), int(y[k])] for k in np.nonzero(y)[0]],
                    'lambda': lam.tolist()}
            (out / 'certificate.json').write_text(json.dumps(cert) + '\n')
            return dict(exact='candidate', denominator=den, scale=L,
                        y_support=int((y != 0).sum()), lambda_int=lam.tolist())
    return dict(exact='rounding failed', bad_cols=bad_c, bad_states=bad_z,
                lambda_float=x[2 + nH:].tolist())

if __name__ == '__main__':
    main()
