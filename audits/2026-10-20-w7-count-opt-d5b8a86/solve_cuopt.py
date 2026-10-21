#!/usr/bin/env python3
"""GPU discovery (NVIDIA cuOpt) on exactly the model of solve_lp.build. Never a verdict."""
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
from solve_lp import build  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True)
    ap.add_argument('--method', choices=('concurrent', 'pdlp', 'dual', 'barrier', 'primal'), default='barrier')
    ap.add_argument('--positive', type=int, default=-1)
    ap.add_argument('--objective', choices=('zero', 'sum', 'size', 'random'), default='sum')
    ap.add_argument('--ref', choices=('h2', 'mindeg'), default='mindeg')
    ap.add_argument('--seconds', type=float, default=600)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--eps', type=float, default=1e-8)
    ap.add_argument('--crossover', action='store_true')
    ap.add_argument('--pdlp-mode', default='Stable3')
    ap.add_argument('--warm', type=Path, help='vectors.npz with x (and y) as initial point')
    args = ap.parse_args()
    from cuopt.linear_programming import data_model, solver, solver_settings as ss
    import cuopt
    out = HERE / 'runs' / args.name
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.monotonic()
    m = Model()
    ref, A, (lo, hi), c = build(m, args)
    A = A.tocsr()
    dm = data_model.DataModel()
    dm.set_csr_constraint_matrix(A.data.astype(np.float64), A.indices.astype(np.int32), A.indptr.astype(np.int32))
    dm.set_constraint_lower_bounds(lo)
    dm.set_constraint_upper_bounds(np.where(np.isinf(hi), np.inf, hi))
    dm.set_objective_coefficients(c)
    dm.set_variable_lower_bounds(np.zeros(m.nx))
    dm.set_variable_upper_bounds(np.full(m.nx, np.inf))
    if args.warm:
        w = np.load(args.warm)
        dm.set_initial_primal_solution(np.clip(w['x'], 0, None))
        if 'y' in w.files and len(w['y']) == A.shape[0]:
            dm.set_initial_dual_solution(w['y'])
    st = ss.SolverSettings()
    meth = {'concurrent': 0, 'pdlp': 1, 'dual': 2, 'barrier': 3, 'primal': 4}[args.method]
    st.set_parameter('method', ss.SolverMethod(meth))
    st.set_parameter('time_limit', args.seconds)
    st.set_parameter('crossover', args.crossover)
    st.set_parameter('random_seed', args.seed)
    st.set_parameter('log_file', str(out / 'cuopt.log'))
    st.set_parameter('log_to_console', True)
    st.set_parameter('pdlp_solver_mode', ss.PDLPSolverMode[args.pdlp_mode])
    for k in ('absolute_primal_tolerance', 'relative_primal_tolerance', 'absolute_dual_tolerance',
              'relative_dual_tolerance', 'absolute_gap_tolerance', 'relative_gap_tolerance'):
        st.set_parameter(k, args.eps)
    meta = {'arguments': {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
            'shape': list(A.shape), 'nnz': int(A.nnz),
            'cuopt_version': cuopt.__version__, 'setup_seconds': time.monotonic() - t0,
            'python': sys.version.split()[0]}
    (out / 'input.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(json.dumps(meta), flush=True)
    t1 = time.monotonic()
    sol = solver.Solve(dm, st)
    res = {'termination': str(sol.get_termination_reason()), 'status': str(sol.get_termination_status()),
           'solved_by': str(sol.get_solved_by()), 'solve_time': sol.get_solve_time(),
           'primal_objective': sol.get_primal_objective(), 'dual_objective': sol.get_dual_objective(),
           'lp_stats': {k: (float(v) if isinstance(v, (int, float, np.floating, np.integer)) else str(v))
                        for k, v in sol.get_lp_stats().items()},
           'solve_wall_seconds': time.monotonic() - t1,
           'peak_rss_mb': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024}
    x = np.asarray(sol.get_primal_solution(), dtype=float)
    y = np.asarray(sol.get_dual_solution(), dtype=float)
    rc = np.asarray(sol.get_reduced_cost(), dtype=float)
    if len(x) == m.nx:
        ax = A @ x
        res['primal_residual_inf'] = float(np.maximum(lo - ax, ax - hi).max())
        res['min_x'] = float(x.min())
        res['support_1e-9'] = int((x > 1e-9).sum())
    np.savez_compressed(out / 'vectors.npz', ref=ref, x=x, y=y, reduced_costs=rc)
    (out / 'result.json').write_text(json.dumps(res, indent=2) + '\n')
    print(json.dumps(res), flush=True)


if __name__ == '__main__':
    main()
