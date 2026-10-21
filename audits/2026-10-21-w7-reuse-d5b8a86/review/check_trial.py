#!/usr/bin/env python3
"""Explicit-model review of the one bounded PDHG trial; never runs a solver."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.sparse import csr_matrix, vstack

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
OPT = ROOT / 'audits/2026-10-20-w7-count-opt-d5b8a86'
SPECIAL = AUDIT / 'specialized'
RUN = SPECIAL / 'runs/feasibility-60s'
sys.path.insert(0, str(OPT))
sys.path.insert(0, str(SPECIAL))
from model import Model
from w7_operator import W7Operator
from run_pdhg import diagonal_steps


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics(A, x, ns):
    ax = A @ x
    d, q = ax[:2*ns], ax[2*ns:]
    balance = float(np.abs(d).max())
    pos = float(np.maximum(2-q, 0).max())
    return {'balance_inf': balance, 'balance_l2': float(np.linalg.norm(d)),
            'positivity_violation': pos,
            'primal_residual_inf': max(balance, pos, float(max(0, -x.min()))),
            'PZ_ten': (q/2).tolist(), 'sum_x': float(x.sum()), 'min_x': float(x.min()),
            'support_1e-9': int(np.count_nonzero(x > 1e-9))}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', action='store_true')
    args = ap.parse_args()
    inp = json.loads((RUN / 'input.json').read_text())
    result = json.loads((RUN / 'result.json').read_text())
    vectors = np.load(RUN / 'vectors.npz')
    warm_path = Path(inp['warm'])
    assert sha(warm_path) == inp['warm_sha256']
    for filename, value in inp['source_sha256'].items():
        assert sha(SPECIAL / filename) == value
    base = json.loads((AUDIT / 'BASE.json').read_text())
    pin = next(x for x in base['inputs'] if x['path'].endswith('cache/model.npz'))
    assert sha(ROOT / pin['path']) == pin['sha256']
    m = Model()
    ref = m.reference('mindeg')
    assert np.array_equal(ref, vectors['ref'])
    warm = np.load(warm_path)
    assert np.array_equal(ref, warm['ref'])
    D, Q = m.difference(ref), m.positivity_rows(ref)
    A = vstack([D, csr_matrix(Q)], format='csr')
    op = W7Operator('direct')
    tau, sigma, scaling = diagonal_steps(op, inp['scaling']['eta'])
    assert scaling == inp['scaling']
    eta = inp['scaling']['eta']
    row_bound, col_bound = eta/sigma, eta/tau
    row_abs = np.asarray(abs(A).sum(axis=1)).reshape(-1)
    col_abs = np.asarray(abs(A).sum(axis=0)).reshape(-1)
    assert np.all(row_abs <= row_bound + 1e-10)
    assert np.all(col_abs <= col_bound + 1e-10)
    checks = {}
    for name, x in (('initial', np.maximum(warm['x'], 0)),
                    ('final', vectors['x']), ('best', vectors['best_x'])):
        assert np.all(np.isfinite(x)) and x.min() >= 0
        explicit = metrics(A, x, m.ns)
        expected = result[name]
        max_error = 0.
        for key, value in explicit.items():
            error = float(np.max(np.abs(np.asarray(value)-np.asarray(expected[key]))))
            max_error = max(max_error, error)
            assert np.allclose(value, expected[key], rtol=1e-12, atol=1e-11), (name, key, value, expected[key])
        operator_error = float(np.abs(op.matvec(x)-A@x).max())
        assert operator_error < 1e-10
        checks[name] = dict(explicit_metrics=explicit,
                            max_reported_metric_absolute_difference=max_error,
                            max_operator_forward_absolute_difference=operator_error)
    assert result['stop'] == 'time limit'
    assert result['seconds'] >= inp['requested_seconds']
    assert result['no_source_or_feasibility_verdict'] is True
    assert result['necessary_cone'] == 'OPEN'
    assert checks['best']['explicit_metrics']['primal_residual_inf'] <= checks['initial']['explicit_metrics']['primal_residual_inf'] + 1e-11
    assert vectors['y'][2*m.ns:].max() <= 0
    assert np.all(np.isfinite(vectors['y']))
    report = dict(status='PASS; one numerical trial, no cone or source verdict',
                  implementation_review='PDHG signs, extrapolation, diagonal bounds and buffer reuse checked',
                  explicit_matrix_shape=list(A.shape), explicit_matrix_nnz=A.nnz,
                  warm_sha256_verified=inp['warm_sha256'], source_sha256_verified=inp['source_sha256'],
                  operator_row_bound_valid=True, operator_column_bound_valid=True,
                  iterations=result['iterations'], elapsed_seconds=result['seconds'],
                  checks=checks,
                  output_sha256={p.name: sha(p) for p in (RUN/'input.json', RUN/'result.json', RUN/'vectors.npz')})
    output = HERE / 'trial-review.json'
    if args.build:
        with output.open('x') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    else:
        assert report == json.loads(output.read_text()), 'saved trial review differs'
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
