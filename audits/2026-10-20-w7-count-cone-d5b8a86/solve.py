#!/usr/bin/env python3
"""Numerical discovery only. An independent integer checker decides the result."""
import argparse
import gzip
import json
import pickle
import time
from pathlib import Path

import highspy
import numpy as np
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / '2026-10-20-r6-941-j1-five-edge-417732f/counting'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True)
    ap.add_argument('--solver', default='ipm')
    ap.add_argument('--seconds', type=float, default=600)
    ap.add_argument('--positive', choices=('target', 'all', 'none'), default='target')
    ap.add_argument('--objective', choices=('size', 'zero', 'target'), default='size')
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--simplex-strategy', type=int)
    args = ap.parse_args()
    out = HERE / args.name
    out.mkdir(exist_ok=False)
    start = time.monotonic()
    caps = json.load(gzip.open(INPUT / 'caps.json.gz', 'rt'))
    orb = json.load(gzip.open(INPUT / 'orbits.json.gz', 'rt'))
    live = orb['live']; li = {s: i for i, s in enumerate(live)}
    rowids = dict(orb['rowids'])
    rows = sorted(r for r, s in rowids.items() if s in li)
    ri = {r: i for i, r in enumerate(rows)}
    nz = len(live); nx = len(orb['columns']); nr = len(rows)
    ps = [np.array([caps['matrices']['G'][j][s] for s in live], dtype=float)
          for j in (0, 2, 3, 5, 7, 8, 9)]
    ps += [np.array([p[s] for s in live], dtype=float) for p in caps['sectors']]
    ps.append(np.array([s in (44459, 44466) for s in live], dtype=float))
    active_p = list(range(10)) if args.positive == 'all' else ([9] if args.positive == 'target' else [])
    rr = list(range(nr)); cc = [li[rowids[r]] for r in rows]; vv = [2.] * nr
    for j, col in enumerate(orb['columns']):
        rr.extend(ri[r] for r in col)
        cc.extend([nz + j] * len(col)); vv.extend([-1.] * len(col))
    for k, p in enumerate(active_p):
        inds = np.flatnonzero(ps[p])
        rr.extend([nr + k] * len(inds)); cc.extend(inds); vv.extend(ps[p][inds])
    a = coo_matrix((vv, (rr, cc)), shape=(nr + len(active_p), nz + nx)).tocsr()
    lp = highspy.HighsLp()
    lp.num_col_ = nz + nx; lp.num_row_ = a.shape[0]
    lp.col_cost_ = np.r_[np.ones(nz), np.zeros(nx)] if args.objective == 'size' else np.zeros(nz + nx)
    if args.objective == 'target':
        lp.col_cost_ = np.r_[-ps[9], np.zeros(nx)]
    lp.col_lower_ = np.zeros(nz + nx)
    lp.col_upper_ = np.full(nz + nx, highspy.kHighsInf)
    lp.row_lower_ = np.r_[np.zeros(nr), np.ones(len(active_p))]
    lp.row_upper_ = np.r_[np.zeros(nr), np.full(len(active_p), highspy.kHighsInf)]
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = a.indptr
    lp.a_matrix_.index_ = a.indices
    lp.a_matrix_.value_ = a.data
    h = highspy.Highs()
    options = {'solver': args.solver, 'time_limit': args.seconds, 'threads': args.threads,
               'random_seed': 0, 'log_file': str(out / 'highs.log')}
    if args.simplex_strategy is not None:
        options['simplex_strategy'] = args.simplex_strategy
    for k, v in options.items():
        status = h.setOptionValue(k, v)
        if status != highspy.HighsStatus.kOk:
            raise RuntimeError(('invalid solver option', k, v, str(status)))
    meta = {'arguments': vars(args), 'highs_version': h.version(), 'shape': a.shape,
            'nnz': a.nnz, 'active_positivities': active_p,
            'setup_seconds': time.monotonic() - start}
    (out / 'input.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(json.dumps(meta), flush=True)
    h.passModel(lp)
    h.run()
    sol = h.getSolution()
    info = h.getInfo()
    result = {'model_status': str(h.getModelStatus()), 'seconds': time.monotonic() - start,
              'primal_solution_status': info.primal_solution_status,
              'dual_solution_status': info.dual_solution_status,
              'simplex_iterations': info.simplex_iteration_count,
              'ipm_iterations': info.ipm_iteration_count,
              'max_primal_infeasibility': info.max_primal_infeasibility,
              'max_dual_infeasibility': info.max_dual_infeasibility,
              'objective': info.objective_function_value,
              'value_valid': sol.value_valid, 'dual_valid': sol.dual_valid}
    if sol.value_valid:
        result['positive_values'] = [float(p @ np.array(sol.col_value[:nz])) for p in ps]
        h.writeSolution(str(out / 'solution.txt'), 0)
    h.writeBasis(str(out / 'basis.txt'))
    if h.getModelStatus() == highspy.HighsModelStatus.kInfeasible:
        status, exists, ray = h.getDualRay()
        result['dual_ray_exists'] = bool(exists)
        if exists:
            with (out / 'dual-ray.pickle').open('xb') as f:
                pickle.dump((rows, active_p, ray), f)
    if h.getModelStatus() == highspy.HighsModelStatus.kUnbounded:
        status, exists, ray = h.getPrimalRay()
        result['primal_ray_exists'] = bool(exists)
        if exists:
            with (out / 'primal-ray.pickle').open('xb') as f:
                pickle.dump((live, ray), f)
    with (out / 'solution.pickle').open('xb') as f:
        pickle.dump({'live': live, 'rows': rows, 'active_p': active_p,
                     'col_value': sol.col_value, 'row_dual': sol.row_dual,
                     'col_dual': sol.col_dual, 'result': result}, f)
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
