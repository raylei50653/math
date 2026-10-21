#!/usr/bin/env python3
"""Fast path to an exact candidate (discovery only; check.py decides).

Pieces: 'target' asks q_9 X = 2; 'rest' asks q_l X >= 2 for l = 0..8.  An exact
X_target + X_rest is a joint point (all ten quantities are nonnegative forms).

  sparsify  GPU PDLP rounds with reweighted-L1 costs 1/(x+eps_r), warm-started
  vertex    restrict to the support, simplex vertex of the restricted LP
  exact     rational_solve on that basis, exact integer verification

Every stage writes runs/fp-<name>/<stage>.npz and appends to log.jsonl.
Restricted-support infeasibility is never a verdict.
"""
import argparse
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import Model  # noqa: E402

PIECES = {'target': [9], 'rest': list(range(9))}


def log(**kw):
    kw['t'] = round(time.monotonic() - T0, 2)
    kw['rss_mb'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
    print(json.dumps(kw), flush=True)
    with (OUT / 'log.jsonl').open('a') as f:
        f.write(json.dumps(kw) + '\n')


def system(m, piece):
    """(D, Q, lo, hi, ref): D X = 0 rows, piece positivity rows Q X in [lo, hi]."""
    from scipy.sparse import csr_matrix
    ref = m.reference('mindeg')
    D = m.difference(ref).tocsr()
    pos = PIECES[piece]
    Q = csr_matrix(m.positivity_rows(ref)[pos])
    lo = np.full(len(pos), 2.0)
    hi = lo.copy() if len(pos) == 1 else np.full(len(pos), np.inf)
    return D, Q, lo, hi, ref


def stats(m, D, ref, x, tol=1e-9):
    S = x > tol
    rows = np.diff(D[:, S].tocsr().indptr) > 0 if S.any() else np.zeros(D.shape[0], bool)
    z = m.zmap(ref) @ x / 2
    return dict(support=int(S.sum()), touched_rows=int(rows.sum()),
                states=int((z > tol).sum()), sum_x=float(x.sum()))


def cuopt(A, lo, hi, c, x0, seconds, eps, method='pdlp', crossover=False, logfile=None):
    from cuopt.linear_programming import data_model, solver, solver_settings as ss
    A = A.tocsr()
    dm = data_model.DataModel()
    dm.set_csr_constraint_matrix(A.data.astype(np.float64), A.indices.astype(np.int32),
                                 A.indptr.astype(np.int32))
    dm.set_constraint_lower_bounds(lo)
    dm.set_constraint_upper_bounds(hi)
    dm.set_objective_coefficients(c)
    dm.set_variable_lower_bounds(np.zeros(A.shape[1]))
    dm.set_variable_upper_bounds(np.full(A.shape[1], np.inf))
    if x0 is not None:
        dm.set_initial_primal_solution(x0)
    st = ss.SolverSettings()
    st.set_parameter('method', ss.SolverMethod(
        {'pdlp': 1, 'dual': 2, 'barrier': 3, 'primal': 4, 'concurrent': 0}[method]))
    st.set_parameter('time_limit', seconds)
    st.set_parameter('crossover', crossover)
    st.set_parameter('log_to_console', False)
    if logfile:
        st.set_parameter('log_file', str(logfile))
    st.set_parameter('pdlp_solver_mode', ss.PDLPSolverMode.Stable3)
    for k in ('absolute_primal_tolerance', 'relative_primal_tolerance', 'absolute_dual_tolerance',
              'relative_dual_tolerance', 'absolute_gap_tolerance', 'relative_gap_tolerance'):
        st.set_parameter(k, eps)
    t = time.monotonic()
    sol = solver.Solve(dm, st)
    x = np.clip(np.asarray(sol.get_primal_solution(), dtype=float), 0, None)
    ax = A @ x
    return x, dict(status=str(sol.get_termination_status()), seconds=round(time.monotonic() - t, 2),
                   objective=sol.get_primal_objective(),
                   residual=float(np.maximum(lo - ax, ax - hi).max()))


def sparsify(m, args):
    from scipy.sparse import vstack
    D, Q, lo, hi, ref = system(m, args.piece)
    A = vstack([D, Q], format='csr')
    lo_all = np.r_[np.zeros(D.shape[0]), lo]
    hi_all = np.r_[np.zeros(D.shape[0]), hi]
    x = None
    if args.warm:
        x = np.clip(np.load(args.warm)['x'], 0, None)
    c = np.ones(m.nx)
    for r in range(args.start, args.rounds):
        if x is not None and r > 0:
            e = args.eps0 * 10.0 ** (-r + 1) * x.max()
            c = 1.0 / (x + e)
            c /= np.median(c)
        last = r == args.rounds - 1
        x, info = cuopt(A, lo_all, hi_all, c, x, args.seconds, args.eps,
                        crossover=args.crossover and last, logfile=OUT / f'cuopt-r{r}.log')
        log(stage='sparsify', round=r, crossover=args.crossover and last, **info,
            nonzeros=int((x > 0).sum()), **stats(m, D, ref, x))
        np.savez_compressed(OUT / f'sparsify-r{r}.npz', x=x, ref=ref, c=c)


def vertex(m, args):
    """Restricted LP on S = {x > tau}: random costs (unique vertex), PDLP warm start + crossover."""
    from scipy.sparse import vstack
    D, Q, lo, hi, ref = system(m, args.piece)
    x = np.clip(np.load(args.warm)['x'], 0, None)
    S = np.flatnonzero(x > args.tau)
    DS = D[:, S].tocsr()
    rows = np.flatnonzero(np.diff(DS.indptr) > 0)
    A = vstack([DS[rows], Q[:, S]], format='csr')
    lo_all = np.r_[np.zeros(len(rows)), lo]
    hi_all = np.r_[np.zeros(len(rows)), hi]
    c = np.random.default_rng(args.seed).uniform(1, 2, len(S))
    log(stage='vertex-setup', columns=len(S), rows=len(rows), nnz=int(A.nnz))
    xs, info = cuopt(A, lo_all, hi_all, c, x[S], args.seconds, args.eps, method=args.method,
                     crossover=args.crossover, logfile=OUT / 'cuopt-vertex.log')
    xf = np.zeros(m.nx)
    xf[S] = xs
    log(stage='vertex', method=args.method, crossover=args.crossover, **info,
        nonzeros_1e12=int((xs > 1e-12).sum()), **stats(m, D, ref, xf))
    np.savez_compressed(OUT / 'vertex.npz', x=xf, ref=ref, S=S, rows=rows)


def exact(m, args):
    """Vertex support P (columns independent): solve M^T M x = M^T b exactly, M = [D_P; Q_P]."""
    import exact_tools as et
    from scipy.sparse import vstack
    D, Q, lo, hi, ref = system(m, args.piece)
    x = np.clip(np.load(args.warm)['x'], 0, None)
    P = np.flatnonzero(x > args.tau)
    DP = D[:, P].tocsr()
    rows = np.flatnonzero(np.diff(DP.indptr) > 0)
    QP = Q[:, P].tocsr()
    tight = np.flatnonzero(np.abs(QP @ x[P] - lo) <= 1e-6 * np.maximum(1, lo))
    M = vstack([DP[rows], QP[tight]], format='csr')
    b = [0] * len(rows) + [int(lo[i]) for i in tight]
    MtM = (M.T @ M).tocsc()
    Mtb = et.int_matvec(M.T.tocsr(), b)
    log(stage='exact-setup', support=len(P), rows=len(rows), tight_positivity=len(tight),
        mtm_nnz=int(MtM.nnz))
    sol = et.rational_solve(MtM, Mtb)
    if sol is None:
        return log(stage='exact', result='rational solve failed')
    num, den = sol
    ok = et.int_matvec(M, num) == [den * v for v in b]
    log(stage='exact', result='ok', consistent=ok, denominator_bits=den.bit_length(),
        max_num_bits=max(abs(v) for v in num).bit_length(), negatives=sum(v < 0 for v in num))
    if not ok or min(num) < 0:
        return
    X = np.zeros(m.nx, dtype=object)
    X[P] = num
    pos = et.int_matvec(Q[:, P].tocsr(), list(num))
    log(stage='exact-point', positivities_over_den=[v / den for v in pos],
        all_ok=all(v >= den * l for v, l in zip(pos, lo)))
    with (OUT / 'exact.json').open('w') as f:
        json.dump({'piece': args.piece, 'den': str(den),
                   'x': [[int(j), str(v)] for j, v in zip(P, num) if v]}, f)


def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=('sparsify', 'vertex', 'exact'))
    ap.add_argument('--name', required=True)
    ap.add_argument('--piece', choices=tuple(PIECES), default='target')
    ap.add_argument('--rounds', type=int, default=4)
    ap.add_argument('--seconds', type=float, default=120)
    ap.add_argument('--eps', type=float, default=1e-6)
    ap.add_argument('--eps0', type=float, default=1e-1, help='reweighting offset, relative to max x')
    ap.add_argument('--warm', type=Path)
    ap.add_argument('--start', type=int, default=0, help='first round index (reweighting uses it)')
    ap.add_argument('--tau', type=float, default=1e-9, help='absolute support threshold')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--method', default='pdlp')
    ap.add_argument('--crossover', action='store_true')
    args = ap.parse_args()
    OUT = HERE / 'runs' / f'fp-{args.name}'
    OUT.mkdir(parents=True, exist_ok=True)
    log(stage='start', arguments={k: str(v) for k, v in vars(args).items()})
    m = Model()
    {'sparsify': sparsify, 'vertex': vertex, 'exact': exact}[args.stage](m, args)


T0 = time.monotonic()
OUT = None
if __name__ == '__main__':
    main()
