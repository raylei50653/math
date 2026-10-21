#!/usr/bin/env python3
"""Numerical discovery on the normalized X-only model. Never a verdict.

    min c.X   s.t.  D X = 0,  q_l . X = 2,  X >= 0

D is model.difference(ref); q_l X = 2 P_l Z, so the row asks P_l Z = 1.
Z is recovered as Z = R X / 2 (model.zmap).  Only the checker decides.
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
from model import Model, LABELS  # noqa: E402


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def build(m, args):
    from scipy.sparse import vstack, csr_matrix
    ref = m.reference(args.ref)
    D = m.difference(ref)
    Q = m.positivity_rows(ref)
    # One positivity: equality q.X = 2.  Several: q_l.X >= 2 for each l.
    pos = list(range(10)) if args.positive < 0 else [args.positive]
    A = vstack([D, csr_matrix(Q[pos])], format='csr')
    lo = np.r_[np.zeros(D.shape[0]), np.full(len(pos), 2.0)]
    hi = lo.copy() if len(pos) == 1 else np.r_[np.zeros(D.shape[0]), np.full(len(pos), np.inf)]
    if args.objective == 'zero':
        c = np.zeros(m.nx)
    elif args.objective == 'sum':
        c = np.ones(m.nx)
    elif args.objective == 'size':
        c = np.diff(m.cptr).astype(float)
    else:
        c = np.random.default_rng(args.seed).uniform(1, 2, m.nx)
    return ref, A, (lo, hi), c


def run_highs(A, b, c, args, out):
    import highspy
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = A.shape[1], A.shape[0]
    lp.col_cost_ = c
    lp.col_lower_ = np.zeros(A.shape[1])
    lp.col_upper_ = np.full(A.shape[1], highspy.kHighsInf)
    lp.row_lower_ = b[0]
    lp.row_upper_ = np.where(np.isinf(b[1]), highspy.kHighsInf, b[1])
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = A.indptr
    lp.a_matrix_.index_ = A.indices
    lp.a_matrix_.value_ = A.data
    h = highspy.Highs()
    opts = {'solver': args.solver.split('-', 1)[1], 'time_limit': args.seconds,
            'threads': args.threads, 'random_seed': args.seed,
            'log_file': str(out / 'highs.log')}
    for kv in args.option:
        k, v = kv.split('=', 1)
        opts[k] = type(h.getOptionValue(k)[1])(v) if not isinstance(h.getOptionValue(k)[1], bool) else v == 'true'
    for k, v in opts.items():
        if h.setOptionValue(k, v) != highspy.HighsStatus.kOk:
            raise RuntimeError(('bad option', k, v))
    h.passModel(lp)
    h.run()
    info, sol = h.getInfo(), h.getSolution()
    st = h.getModelStatus()
    res = {'status': str(st), 'simplex_iterations': info.simplex_iteration_count,
           'ipm_iterations': info.ipm_iteration_count, 'pdlp_iterations': info.pdlp_iteration_count,
           'max_primal_infeasibility': info.max_primal_infeasibility,
           'max_dual_infeasibility': info.max_dual_infeasibility,
           'objective': info.objective_function_value,
           'value_valid': sol.value_valid, 'dual_valid': sol.dual_valid}
    arrays = {}
    if sol.value_valid:
        arrays['x'] = np.array(sol.col_value)
    if sol.dual_valid:
        arrays['y'] = np.array(sol.row_dual)
    if st == highspy.HighsModelStatus.kInfeasible:
        _, exists, ray = h.getDualRay()
        res['dual_ray_exists'] = bool(exists)
        if exists:
            arrays['farkas'] = np.array(ray)
    if h.getBasis().valid:
        h.writeBasis(str(out / 'basis.txt'))
    return res, arrays


def run_pdlp(A, b, c, args, out):
    from ortools.pdlp import solve_log_pb2, solvers_pb2
    from ortools.pdlp.python import pdlp
    qp = pdlp.QuadraticProgram()
    qp.resize_and_initialize(A.shape[1], A.shape[0])
    qp.objective_vector = c
    qp.constraint_matrix = A.tocsc()
    qp.constraint_lower_bounds = b[0]
    qp.constraint_upper_bounds = b[1]
    qp.variable_lower_bounds = np.zeros(A.shape[1])
    qp.variable_upper_bounds = np.full(A.shape[1], np.inf)
    p = solvers_pb2.PrimalDualHybridGradientParams()
    p.num_threads = args.threads
    p.verbosity_level = 2
    p.log_interval_seconds = 30
    p.termination_criteria.time_sec_limit = args.seconds
    p.termination_criteria.simple_optimality_criteria.eps_optimal_relative = args.eps
    p.termination_criteria.simple_optimality_criteria.eps_optimal_absolute = args.eps
    p.use_feasibility_polishing = args.polish
    if args.polish:
        p.handle_some_primal_gradients_on_finite_bounds_as_residuals = False
    p.presolve_options.use_glop = args.glop_presolve
    if args.warm:
        w = np.load(args.warm)
        init = pdlp.PrimalAndDualSolution()
        init.primal_solution = w['x']
        init.dual_solution = w['y']
        r = pdlp.primal_dual_hybrid_gradient(qp, p, initial_solution=init)
    else:
        r = pdlp.primal_dual_hybrid_gradient(qp, p)
    log = r.solve_log
    (out / 'pdlp-solve-log.txt').write_text(str(log))
    res = {'status': solve_log_pb2.TerminationReason.Name(log.termination_reason),
           'iterations': log.iteration_count, 'solve_time_sec': log.solve_time_sec}
    ci = log.solution_stats.convergence_information
    if ci:
        res['convergence'] = {f.name: v for f, v in ci[0].ListFields() if isinstance(v, float)}
    return res, {'x': np.array(r.primal_solution), 'y': np.array(r.dual_solution),
                 'reduced_costs': np.array(r.reduced_costs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True)
    ap.add_argument('--solver', default='highs-ipx',
                    choices=('highs-ipx', 'highs-simplex', 'highs-pdlp', 'ortools-pdlp'))
    ap.add_argument('--positive', type=int, default=9, help='0..9, or -1 for all ten')
    ap.add_argument('--objective', choices=('zero', 'sum', 'size', 'random'), default='sum')
    ap.add_argument('--ref', choices=('h2', 'mindeg'), default='mindeg')
    ap.add_argument('--seconds', type=float, default=600)
    ap.add_argument('--threads', type=int, default=8)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--eps', type=float, default=1e-8)
    ap.add_argument('--polish', action='store_true')
    ap.add_argument('--glop-presolve', action='store_true')
    ap.add_argument('--option', action='append', default=[])
    ap.add_argument('--warm', type=Path, help='vectors.npz of an earlier PDLP run on the same model')
    args = ap.parse_args()
    out = HERE / 'runs' / args.name
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.monotonic()
    m = Model()
    ref, A, b, c = build(m, args)
    meta = {'arguments': vars(args), 'positive_label': LABELS[args.positive] if args.positive >= 0 else 'all ten',
            'shape': list(A.shape), 'nnz': int(A.nnz), 'setup_seconds': time.monotonic() - t0,
            'python': sys.version.split()[0]}
    if args.solver.startswith('highs'):
        import highspy
        meta['highs_version'] = highspy.Highs().version()
    else:
        import ortools
        meta['ortools_version'] = ortools.__version__
    (out / 'input.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(json.dumps(meta), flush=True)
    t1 = time.monotonic()
    res, arrays = (run_highs if args.solver.startswith('highs') else run_pdlp)(A, b, c, args, out)
    res['solve_wall_seconds'] = time.monotonic() - t1
    res['peak_rss_mb'] = rss_mb()
    if 'x' in arrays and len(arrays['x']) == m.nx:
        x = arrays['x']
        ax = A @ x
        res['primal_residual_inf'] = float(np.maximum(b[0] - ax, ax - b[1]).max())
        res['min_x'] = float(x.min())
        res['support_1e-9'] = int((x > 1e-9).sum())
        res['support_1e-6'] = int((x > 1e-6).sum())
    np.savez_compressed(out / 'vectors.npz', ref=ref, **arrays)
    (out / 'result.json').write_text(json.dumps(res, indent=2) + '\n')
    print(json.dumps(res), flush=True)


if __name__ == '__main__':
    main()
