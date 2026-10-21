#!/usr/bin/env python3
"""One bounded numerical feasibility-polishing trial using the W7 operator.

No explicit D/Q, no crossover, no certificate or cone verdict. All output lives
in an exclusive run directory. Warm x is retained as the initial best candidate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from w7_operator import W7Operator, ROOT, HERE


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def diagonal_steps(op, eta):
    """B=|L|C >= |A| gives safe diagonal row/column scaling.

    tau=eta/column_sum(B), sigma=eta/row_sum(B) imply
    ||sqrt(sigma) A sqrt(tau)||_2 <= eta < 1.
    """
    deg = np.bincount(op.cidx, minlength=op.nh).astype(float)
    state = np.arange(op.ns)
    refh = 3*state+op.ref
    others = (3*state[:, None]+np.arange(3))[np.arange(3)[None, :] != op.ref[:, None]].reshape(-1, 2)
    row = np.empty(op.shape[0])
    row[:2*op.ns] = (deg[others]+deg[refh, None]).reshape(-1)
    weight = np.ones(op.nh)
    weight[refh] = 2
    for l in range(len(op.positive)):
        p = slice(op.pp[l], op.pp[l+1])
        ss, vv = op.pi[p], op.pv[p]
        row[2*op.ns+l] = vv @ deg[refh[ss]]
        np.add.at(weight, refh[ss], vv)
    col = np.empty(op.nx)
    op.lib.unit_sum(op.nx, op.cptr, op.cidx, weight, col)
    if not 0 < eta < 1 or np.any(row <= 0) or np.any(col <= 0):
        raise ValueError('invalid diagonal scaling')
    return eta/col, eta/row, {
        'row_bound_min_max': [float(row.min()), float(row.max())],
        'column_bound_min_max': [float(col.min()), float(col.max())],
        'eta': eta, 'proof': 'B=|L|C majorizes abs(A); weighted Cauchy-Schwarz gives scaled norm <= eta'}


def metrics(op, x, w, ax):
    op.matvec_into(x, ax, w)
    d, q = ax[:2*op.ns], ax[2*op.ns:]
    balance = float(np.max(np.abs(d)))
    pos = float(np.maximum(2-q, 0).max())
    return {'balance_inf': balance, 'balance_l2': float(np.linalg.norm(d)),
            'positivity_violation': pos, 'primal_residual_inf': max(balance, pos, float(max(0, -x.min()))),
            'PZ_ten': (q/2).tolist(), 'sum_x': float(x.sum()), 'min_x': float(x.min()),
            'support_1e-9': int(np.count_nonzero(x > 1e-9))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True)
    ap.add_argument('--seconds', type=float, default=60.)
    ap.add_argument('--eta', type=float, default=.99)
    ap.add_argument('--warm', type=Path, default=ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86/runs/all-cu-pdlp/vectors.npz')
    args = ap.parse_args()
    if not 0 < args.seconds <= 300 or Path(args.name).name != args.name:
        raise ValueError('use a simple exclusive run name and 0 < seconds <= 300')
    out = HERE/'runs'/args.name
    out.mkdir(parents=True, exist_ok=False)
    setup = time.monotonic()
    op = W7Operator('direct')
    warm = np.load(args.warm)
    if 'ref' not in warm or not np.array_equal(warm['ref'], op.ref):
        raise ValueError('warm reference is not the frozen mindeg reference')
    x = np.asarray(warm['x'], dtype=np.float64).copy()
    if x.shape != (op.nx,) or not np.all(np.isfinite(x)):
        raise ValueError('invalid warm primal vector')
    x = np.maximum(x, 0)
    tau, sigma, scaling = diagonal_steps(op, args.eta)
    y = np.zeros(op.shape[0])  # feasibility objective c=0; old optimization dual is discarded
    xbar, xnew = x.copy(), np.empty_like(x)
    ax, grad, w = np.empty(op.shape[0]), np.empty(op.nx), op.workspace()
    initial = metrics(op, x, w, ax)
    best, best_x = dict(initial), x.copy()
    inp = {'model': 'frozen W7; min 0, D X=0, Q X>=2, X>=0; all ten positivity forms',
           'method': 'diagonally preconditioned PDHG, theta=1, warm primal and zero dual',
           'requested_seconds': args.seconds, 'warm': str(args.warm), 'warm_sha256': sha(args.warm),
           'source_sha256': {p.name: sha(p) for p in (HERE/'run_pdhg.py', HERE/'w7_operator.py', HERE/'kernels.cpp')},
           'scaling': scaling, 'initial': initial, 'setup_seconds': time.monotonic()-setup,
           'no_explicit_D_or_Q': True, 'necessary_cone': 'OPEN'}
    (out/'input.json').write_text(json.dumps(inp, indent=2)+'\n')
    print(json.dumps({'event': 'start', **initial}), flush=True)
    start = time.monotonic()
    last = start
    history = []
    it = 0
    while time.monotonic()-start < args.seconds:
        op.matvec_into(xbar, ax, w)
        ax[2*op.ns:] -= 2
        ax *= sigma
        y += ax
        np.minimum(y[2*op.ns:], 0, out=y[2*op.ns:])
        op.rmatvec_into(y, grad, w)
        np.multiply(tau, grad, out=xnew)
        np.subtract(x, xnew, out=xnew)
        np.maximum(xnew, 0, out=xnew)
        np.multiply(xnew, 2, out=xbar)
        xbar -= x
        x, xnew = xnew, x
        it += 1
        now = time.monotonic()
        if now-last >= 5:
            current = metrics(op, x, w, ax)
            if current['primal_residual_inf'] < best['primal_residual_inf']:
                best, best_x = current, x.copy()
            record = {'iterations': it, 'seconds': now-start, **current}
            history.append(record)
            print(json.dumps({'event': 'progress', **record}), flush=True)
            last = now
        if it % 100 == 0 and (not np.all(np.isfinite(x)) or not np.all(np.isfinite(y))):
            raise RuntimeError('nonfinite iterate; no numerical conclusion')
    elapsed = time.monotonic()-start
    final = metrics(op, x, w, ax)
    if final['primal_residual_inf'] < best['primal_residual_inf']:
        best, best_x = final, x.copy()
    np.savez_compressed(out/'vectors.npz', x=x, best_x=best_x, y=y, ref=op.ref)
    result = {'status': 'NUMERICAL ONLY; no certificate', 'necessary_cone': 'OPEN',
              'stop': 'time limit', 'iterations': it, 'seconds': elapsed,
              'iterations_per_second': it/elapsed, 'initial': initial, 'final': final,
              'best': best, 'initial_to_best_residual_ratio': initial['primal_residual_inf']/best['primal_residual_inf'],
              'history': history, 'solver_operator_forward_calls': it,
              'solver_operator_transpose_calls': it, 'no_source_or_feasibility_verdict': True}
    (out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'event': 'finish', **{k: v for k, v in result.items() if k != 'history'}}), flush=True)


if __name__ == '__main__':
    main()
