#!/usr/bin/env python3
"""HiGHS crossover on the full normalized model from a discovery primal-dual point.

Writes the resulting basis (col_status,row_status) for certify; never a verdict."""
import argparse, json, resource, sys, time
from pathlib import Path
from types import SimpleNamespace
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import Model
from solve_lp import build


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run', type=Path)
    ap.add_argument('--name', required=True)
    ap.add_argument('--seconds', type=float, default=1800)
    ap.add_argument('--threads', type=int, default=8)
    ap.add_argument('--simplex-after', action='store_true')
    args = ap.parse_args()
    import highspy
    out = HERE / 'runs' / args.name
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.monotonic()
    meta = json.loads((args.run / 'input.json').read_text())['arguments']
    m = Model()
    ref, A, (lo, hi), c = build(m, SimpleNamespace(**meta))
    v = np.load(args.run / 'vectors.npz')
    x = np.clip(v['x'], 0, None)
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = A.shape[1], A.shape[0]
    lp.col_cost_ = c
    lp.col_lower_ = np.zeros(A.shape[1])
    lp.col_upper_ = np.full(A.shape[1], highspy.kHighsInf)
    lp.row_lower_ = lo
    lp.row_upper_ = np.where(np.isinf(hi), highspy.kHighsInf, hi)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = A.indptr
    lp.a_matrix_.index_ = A.indices
    lp.a_matrix_.value_ = A.data
    h = highspy.Highs()
    for k, val in {'time_limit': args.seconds, 'threads': args.threads,
                   'log_file': str(out / 'highs.log')}.items():
        h.setOptionValue(k, val)
    h.passModel(lp)
    sol = highspy.HighsSolution()
    if 'y' in v.files and len(v['y']) == A.shape[0]:
        # Complementarity for IPX: keep the larger of x_j and its reduced cost.
        yy = v['y'].copy()
        yy[np.isinf(hi)] = np.clip(yy[np.isinf(hi)], 0, None)
        z = np.clip(c - A.T @ yy, 0, None)
        x = np.where(x >= z, x, 0.0)
    sol.col_value = list(x)
    sol.row_value = list(A @ x)
    sol.value_valid = True
    if 'y' in v.files and len(v['y']) == A.shape[0]:
        # Sign-feasible duals: inequality rows (lo finite, hi inf) need y>=0, and
        # reduced costs of x>=0 need c - A^T y >= 0; tiny violations are clipped.
        y = v['y'].copy()
        ineq = np.isinf(hi)
        y[ineq] = np.clip(y[ineq], 0, None)
        sol.row_dual = list(y)
        z = np.clip(c - A.T @ y, 0, None)
        sol.col_dual = list(np.where(x > 0, 0.0, z))
        sol.dual_valid = True
    (out / 'input.json').write_text(json.dumps({'from_run': str(args.run), 'arguments': vars(args) | {'run': str(args.run)},
                                                'model_arguments': meta, 'highs_version': h.version()}, indent=2) + '\n')
    st = h.crossover(sol)
    res = {'crossover_status': str(st), 'model_status': str(h.getModelStatus()),
           'basis_valid': h.getBasis().valid, 'crossover_seconds': time.monotonic() - t0}
    print(json.dumps(res), flush=True)
    if args.simplex_after and h.getBasis().valid:
        h.setOptionValue('solver', 'simplex')
        h.run()
        res['simplex_status'] = str(h.getModelStatus())
    info = h.getInfo()
    res.update(simplex_iterations=info.simplex_iteration_count, objective=info.objective_function_value,
               max_primal_infeasibility=info.max_primal_infeasibility,
               max_dual_infeasibility=info.max_dual_infeasibility,
               seconds=time.monotonic() - t0,
               peak_rss_mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
    b = h.getBasis()
    if b.valid:
        np.savez_compressed(out / 'basis.npz', ref=ref,
                            col_status=np.array([int(s) for s in b.col_status], dtype=np.int8),
                            row_status=np.array([int(s) for s in b.row_status], dtype=np.int8),
                            x=np.array(h.getSolution().col_value))
    (out / 'result.json').write_text(json.dumps(res, indent=2) + '\n')
    print(json.dumps(res), flush=True)


if __name__ == '__main__':
    main()
